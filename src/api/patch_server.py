import re

file_path = "/home/jerry/codebase/wisedrama/src/api/server.py"
with open(file_path, "r") as f:
    content = f.read()

# Add imports for auth and db
if "from .db import init_db" not in content:
    content = content.replace("app = FastAPI(title=\"WiseDrama API\")", 
    "from api.db import init_db, get_db\nfrom api.auth import router as auth_router, get_current_user\nfrom fastapi import Depends\n\ninit_db()\napp = FastAPI(title=\"WiseDrama API\")")

if "app.include_router(auth_router" not in content:
    content = content.replace('app.mount("/videos", StaticFiles(directory=str(PUBLIC_DIR)), name="videos")',
    'app.mount("/videos", StaticFiles(directory=str(PUBLIC_DIR)), name="videos")\napp.include_router(auth_router, prefix="/api/auth", tags=["auth"])')

# Protect the /api/generate endpoint and deduct tokens
generate_endpoint = """@app.post("/api/generate")
async def start_generation(req: DramaRequest, background_tasks: BackgroundTasks, username: str = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT tokens FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user or user["tokens"] < req.num_shots * 15:
        conn.close()
        raise HTTPException(status_code=402, detail="Insufficient tokens")
        
    new_tokens = user["tokens"] - (req.num_shots * 15)
    cursor.execute("UPDATE users SET tokens = ? WHERE username = ?", (new_tokens, username))
    conn.commit()
    conn.close()

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "writing_script",
        "idea": req.idea,
        "model": req.model,
        "script": None,
        "character_profiles": {},
        "reference_images": {},
        "shots": [],
        "final_video_url": None,
        "completed": False,
        "username": username
    }"""

old_generate = """@app.post("/api/generate")
async def start_generation(req: DramaRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "writing_script",
        "idea": req.idea,
        "model": req.model,
        "script": None,
        "character_profiles": {},
        "reference_images": {},
        "shots": [],
        "final_video_url": None,
        "completed": False
    }"""

content = content.replace(old_generate, generate_endpoint)

with open(file_path, "w") as f:
    f.write(content)
