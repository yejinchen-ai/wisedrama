import re
file_path = "/home/jerry/codebase/wisedrama/src/api/auth.py"
with open(file_path, "r") as f:
    content = f.read()

# Add new imports
new_imports = """from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import bcrypt
import jwt
import datetime
import random
import time
from .db import get_db
from .mailer import send_email_code, send_sms_code"""

content = re.sub(r'from fastapi.*?from \.db import get_db', new_imports, content, flags=re.DOTALL)

# Add code dictionary
if "verification_codes =" not in content:
    content = content.replace('router = APIRouter()', 'router = APIRouter()\n\nverification_codes = {} # MVP in-memory store: {contact: {"code": str, "exp": float}}')

# Add SendCode endpoint and update Register
models_and_endpoints = """
class SendCodeReq(BaseModel):
    contact: str

@router.post("/send-code")
async def send_code(req: SendCodeReq):
    contact = req.contact.strip()
    if not contact:
        raise HTTPException(status_code=400, detail="Contact cannot be empty")
        
    code = str(random.randint(100000, 999999))
    verification_codes[contact] = {"code": code, "exp": time.time() + 300} # 5 minutes expiry
    
    if "@" in contact:
        success = send_email_code(contact, code)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        return {"message": "Email sent"}
    else:
        success = send_sms_code(contact, code)
        return {"message": "SMS mocked (Check server console)"}

class UserRegister(BaseModel):
    username: str
    password: str
    contact: str  # Email or Phone
    code: str     # Verification code

@router.post("/register")
async def register(user: UserRegister):
    # Verify code
    contact = user.contact.strip()
    record = verification_codes.get(contact)
    if not record or record["code"] != user.code.strip():
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    if time.time() > record["exp"]:
        raise HTTPException(status_code=400, detail="Verification code expired")
        
    # Clear the used code
    del verification_codes[contact]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? OR contact = ?", (user.username, contact))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or contact already registered")
        
    hashed_password = get_password_hash(user.password)
    cursor.execute("INSERT INTO users (username, password_hash, contact) VALUES (?, ?, ?)", (user.username, hashed_password, contact))
    conn.commit()
    conn.close()
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}
"""

# Replace old UserRegister and register endpoint
content = re.sub(r'class UserRegister.*?return \{"access_token": access_token, "token_type": "bearer", "username": user\.username\}', models_and_endpoints, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)
