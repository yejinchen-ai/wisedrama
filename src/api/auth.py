from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import bcrypt
import jwt
import datetime
import random
import re
import time
from .db import get_db
from .mailer import send_email_code, send_sms_code

SECRET_KEY = "wisedrama-secret-key-change-in-prod"
ALGORITHM = "HS256"

router = APIRouter()

verification_codes = {}
send_rate_limit = {}
RATE_LIMIT_SECONDS = 60


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def _is_phone(contact: str) -> bool:
    return bool(re.match(r"^1[3-9]\d{9}$", contact))


def _is_email(contact: str) -> bool:
    return "@" in contact and "." in contact


class SendCodeReq(BaseModel):
    contact: str


@router.post("/send-code")
async def send_code(req: SendCodeReq):
    contact = req.contact.strip()
    if not contact:
        raise HTTPException(status_code=400, detail="Contact cannot be empty")

    is_phone = _is_phone(contact)
    is_email = _is_email(contact)
    if not is_phone and not is_email:
        raise HTTPException(status_code=400, detail="Please enter a valid phone number or email")

    last_sent = send_rate_limit.get(contact, 0)
    elapsed = time.time() - last_sent
    if elapsed < RATE_LIMIT_SECONDS:
        wait = int(RATE_LIMIT_SECONDS - elapsed)
        raise HTTPException(status_code=429, detail=f"Please wait {wait}s")

    code = str(random.randint(100000, 999999))
    verification_codes[contact] = {"code": code, "exp": time.time() + 300, "attempts": 0}
    send_rate_limit[contact] = time.time()

    if is_phone:
        success = send_sms_code(contact, code)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send SMS")
        return {"message": "SMS sent", "channel": "sms"}
    else:
        success = send_email_code(contact, code)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        return {"message": "Email sent", "channel": "email"}


class UserRegister(BaseModel):
    username: str
    password: str
    contact: str
    code: str


@router.post("/register")
async def register(user: UserRegister):
    contact = user.contact.strip()
    username = user.username.strip()
    password = user.password.strip()
    code = user.code.strip()

    if not username or len(username) < 2:
        raise HTTPException(status_code=400, detail="Username must be at least 2 characters")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    record = verification_codes.get(contact)
    if not record:
        raise HTTPException(status_code=400, detail="Please request a verification code first")

    record["attempts"] = record.get("attempts", 0) + 1
    if record["attempts"] > 5:
        del verification_codes[contact]
        raise HTTPException(status_code=400, detail="Too many attempts, request a new code")

    if record["code"] != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    if time.time() > record["exp"]:
        del verification_codes[contact]
        raise HTTPException(status_code=400, detail="Verification code expired")

    del verification_codes[contact]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? OR contact = ?", (username, contact))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or contact already registered")

    hashed_password = get_password_hash(password)
    cursor.execute("INSERT INTO users (username, password_hash, contact) VALUES (?, ?, ?)",
                   (username, hashed_password, contact))
    conn.commit()
    conn.close()

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer", "username": username}


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(user: UserLogin):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ? OR contact = ?",
                   (user.username, user.username))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    actual_username = db_user["username"]
    access_token = create_access_token(data={"sub": actual_username})
    return {"access_token": access_token, "token_type": "bearer", "username": actual_username}


class PhoneLoginReq(BaseModel):
    phone: str
    code: str


@router.post("/phone-login")
async def phone_login(req: PhoneLoginReq):
    """Login or auto-register via phone + SMS code (PNVS flow)."""
    phone = req.phone.strip()
    code = req.code.strip()

    if not _is_phone(phone):
        raise HTTPException(status_code=400, detail="Invalid phone number")

    record = verification_codes.get(phone)
    if not record:
        raise HTTPException(status_code=400, detail="Please request a verification code first")

    record["attempts"] = record.get("attempts", 0) + 1
    if record["attempts"] > 5:
        del verification_codes[phone]
        raise HTTPException(status_code=400, detail="Too many attempts, request a new code")

    if record["code"] != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    if time.time() > record["exp"]:
        del verification_codes[phone]
        raise HTTPException(status_code=400, detail="Verification code expired")

    del verification_codes[phone]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE contact = ?", (phone,))
    db_user = cursor.fetchone()

    if db_user:
        username = db_user["username"]
    else:
        username = f"user_{phone[-4:]}{random.randint(100,999)}"
        hashed = get_password_hash(phone + str(random.randint(100000, 999999)))
        cursor.execute("INSERT INTO users (username, password_hash, contact) VALUES (?, ?, ?)",
                       (username, hashed, phone))
        conn.commit()

    conn.close()
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer", "username": username}


@router.get("/me")
async def read_users_me(username: str = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, tokens, contact, created_at FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user["username"],
        "tokens": user["tokens"],
        "contact": user["contact"] if user["contact"] else "",
        "created_at": user["created_at"]
    }
