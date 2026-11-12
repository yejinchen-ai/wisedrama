from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import uuid
import sys
import os
import traceback
import requests
import json
from copy import deepcopy
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from agents.screenwriter import ScreenwriterAgent
from agents.storyboard import StoryboardAgent
from agents.art_director import ArtDirectorAgent
from agents.veo_director import generate_video_with_veo, poll_operation as poll_veo
from agents.hailuo_director import generate_video_with_hailuo, poll_hailuo_operation
from agents.runway_director import generate_video_with_runway, poll_runway_operation
from agents.sora_director import generate_video_with_sora, poll_sora_operation
from agents.seedance_director import generate_video_with_seedance, poll_seedance_operation
from agents.pixverse_director import generate_video_with_pixverse, poll_pixverse_operation
from agents.kling_director import generate_video_with_kling, poll_kling_operation
from agents.happyhorse_director import generate_video_with_happyhorse, poll_happyhorse_operation
from utils.video_editor import stitch_videos

# Setup static directory for generated videos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PUBLIC_DIR = BASE_DIR / "public" / "videos"
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

# Create a jobs directory to persist state (so we don't lose jobs on restart)
JOBS_DIR = BASE_DIR / "logs" / "jobs"
JOBS_DIR.mkdir(parents=True, exist_ok=True)

from api.db import init_db, get_db
from api.auth import router as auth_router, get_current_user
from api.projects import load_project, router as projects_router, require_owner, save_project, update_project
from fastapi import Depends

init_db()
app = FastAPI(title="WiseDrama API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/videos", StaticFiles(directory=str(PUBLIC_DIR)), name="videos")
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
@app.get("/")
async def serve_index():
    return FileResponse(str(BASE_DIR / "web" / "index.html"))


@app.get("/studio")
async def serve_studio():
    return FileResponse(str(BASE_DIR / "web" / "studio.html"))

# We also mount web directory just in case there are static assets in it later
# app.mount("/web", StaticFiles(directory=str(BASE_DIR / "web")), name="web")


jobs = {}

SUPPORTED_MODELS = {
    "hailuo", "hailuo-2.3", "hailuo-h3", "h3",
    "veo", "veo-3.1",
    "pixverse",
    "runway",
    "sora",
    "seedance", "seedance-2.0",
    "kling", "kling-3.0",
    "happyhorse", "happyhorse-1.1",
}

# Load jobs from disk on startup
for job_file in JOBS_DIR.glob("*.json"):
    try:
        with open(job_file, "r") as f:
            job_data = json.load(f)
            jobs[job_data["id"]] = job_data
    except:
        pass

def save_job(job_id):
    if job_id in jobs:
        jobs[job_id]["id"] = job_id
        with open(JOBS_DIR / f"{job_id}.json", "w") as f:
            json.dump(jobs[job_id], f)

class DramaRequest(BaseModel):
    idea: str
    num_shots: int = 3
    model: str = "veo-3.1"
    resolution: str = "1080p"
    project_id: str | None = None


class ProjectPlanRequest(BaseModel):
    instruction: str = ""
    num_shots: int = 10


@app.post("/api/projects/{project_id}/plan")
async def plan_project(
    project_id: str,
    req: ProjectPlanRequest,
    background_tasks: BackgroundTasks,
    username: str = Depends(get_current_user),
):
    project = require_owner(project_id, username)
    if not 1 <= req.num_shots <= 30:
        raise HTTPException(status_code=400, detail="num_shots must be between 1 and 30")
    base_idea = (project.get("prompt") or "").strip()
    instruction = req.instruction.strip()
    idea = base_idea
    if instruction and instruction not in {"先规划剧本和分镜，不要生成视频", "仅规划"}:
        idea = f"{base_idea}\n\n本次分镜调整要求：{instruction}" if base_idea else instruction
    if not idea:
        raise HTTPException(status_code=400, detail="Project prompt cannot be empty")
    project["status"] = "planning"
    project["agent_events"].append(
        {"type": "plan", "message": "Agent 正在规划剧本、角色与分镜，不会生成视频。"}
    )
    save_project(project)
    background_tasks.add_task(run_project_plan, project_id, idea, req.num_shots)
    return {"project_id": project_id, "status": "planning"}


def run_project_plan(project_id: str, idea: str, num_shots: int) -> None:
    try:
        writer = ScreenwriterAgent()
        script = writer.write_script(idea, num_shots=num_shots)
        art_director = ArtDirectorAgent()
        art_direction = art_director.extract_profiles(script.model_dump_json())
        refs = art_director.generate_reference_images(art_direction)
        storyboard_agent = StoryboardAgent()
        prompts = storyboard_agent.translate_to_video_prompts(
            script, art_direction=art_direction, reference_images=refs
        )
        project = load_project(project_id)
        project["script"] = script.model_dump()
        project["elements"] = art_direction.model_dump().get("character_profiles", [])
        project["shots"] = [
            {
                "shot_number": item.shot_number,
                "prompt": item.video_prompt,
                "video_prompt": item.video_prompt,
                "voiceover": item.voiceover,
                "reference_image_url": item.reference_image_url,
                "status": "planned",
                "video_url": None,
                "local_path": None,
            }
            for item in prompts
        ]
        project["media"] = [
            {
                "id": f"reference-{item.shot_number}",
                "shot_number": item.shot_number,
                "type": "reference_image",
                "url": item.reference_image_url,
                "purpose": "reference_image",
                "status": "ready",
            }
            for item in prompts
            if item.reference_image_url
        ]
        project["timeline"] = []
        project["status"] = "storyboard_ready"
        project["agent_events"].append(
            {"type": "milestone", "message": f"已完成 {len(prompts)} 个分镜，等待确认后再生成视频。"}
        )
        save_project(project)
    except Exception as exc:
        project = load_project(project_id)
        project["status"] = "planning_failed"
        project["agent_events"].append({"type": "error", "message": str(exc)})
        save_project(project)

@app.post("/api/generate")
async def start_generation(req: DramaRequest, background_tasks: BackgroundTasks, username: str = Depends(get_current_user)):
    if req.model not in SUPPORTED_MODELS:
        raise HTTPException(status_code=400, detail=f"Unsupported video model: {req.model}")
    if req.project_id:
        require_owner(req.project_id, username)

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
        "resolution": req.resolution,
        "script": None,
        "character_profiles": {},
        "reference_images": {},
        "shots": [],
        "final_video_url": None,
        "completed": False,
        "username": username,
        "project_id": req.project_id,
    }
    save_job(job_id)
    if req.project_id:
        update_project(
            req.project_id,
            status="running",
            active_job_id=job_id,
            prompt=req.idea,
        )
    background_tasks.add_task(run_pipeline_task, job_id, req.idea, req.num_shots, req.model, req.resolution)
    return {"job_id": job_id, "message": "Generation started"}

@app.get("/api/job/{job_id}")
async def get_job_status(job_id: str, username: str = Depends(get_current_user)):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    if jobs[job_id].get("username") != username:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

def update_job_status(job_id, status):
    jobs[job_id]["status"] = status
    save_job(job_id)
    project_id = jobs[job_id].get("project_id")
    if project_id:
        try:
            project = load_project(project_id)
            project["status"] = status
            project["agent_events"].append({"type": "status", "message": status})
            save_project(project)
        except Exception as exc:
            print(f"Failed to sync project status: {exc}")


def sync_project_from_job(job_id: str) -> None:
    project_id = jobs[job_id].get("project_id")
    if not project_id:
        return
    try:
        project = load_project(project_id)
        job = jobs[job_id]
        project["status"] = job["status"]
        project["script"] = job.get("script")
        profiles = job.get("character_profiles") or {}
        project["elements"] = profiles.get("character_profiles", [])
        project["shots"] = deepcopy(job.get("shots", []))
        project["media"] = [
            {
                "id": f"shot-{shot['shot_number']}",
                "shot_number": shot["shot_number"],
                "type": "video" if shot.get("video_url") else "reference_image",
                "url": shot.get("video_url") or shot.get("reference_image_url"),
                "purpose": "final_video" if shot.get("video_url") else "reference_image",
                "status": shot.get("status"),
            }
            for shot in job.get("shots", [])
            if shot.get("video_url") or shot.get("reference_image_url")
        ]
        project["timeline"] = [
            {
                "shot_number": shot["shot_number"],
                "url": shot.get("video_url"),
                "duration": 6,
                "status": shot.get("status"),
            }
            for shot in job.get("shots", [])
        ]
        project["final_video_url"] = job.get("final_video_url")
        save_project(project)
    except Exception as exc:
        print(f"Failed to sync project workspace: {exc}")


def map_pixverse_quality(resolution: str) -> str:
    resolution = (resolution or "").lower()
    return {
        "720p": "720p",
        "1080p": "1080p",
        "2k": "1080p",
        "4k": "1080p",
    }.get(resolution, "720p")

def download_video(url, dest_path):
    try:
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Failed to download video: {e}")
    return False

def run_pipeline_task(job_id: str, idea: str, num_shots: int, model: str, resolution: str = "1080p"):
    try:
        writer = ScreenwriterAgent()
        script = writer.write_script(idea, num_shots=num_shots)
        
        jobs[job_id]["script"] = script.dict()
        sync_project_from_job(job_id)
        update_job_status(job_id, "generating_art_direction")

        art_director = ArtDirectorAgent()
        # Convert script to string for analysis
        art_direction = art_director.extract_profiles(script.model_dump_json())
        refs = art_director.generate_reference_images(art_direction)

        jobs[job_id]["character_profiles"] = art_direction.model_dump()
        jobs[job_id]["reference_images"] = refs
        sync_project_from_job(job_id)
        
        update_job_status(job_id, "generating_prompts")
        
        storyboard_agent = StoryboardAgent()
        prompts = storyboard_agent.translate_to_video_prompts(
            script, art_direction=art_direction, reference_images=refs
        )
        
        for p in prompts:
            jobs[job_id]["shots"].append({
                "shot_number": p.shot_number,
                "prompt": p.video_prompt,
                "voiceover": p.voiceover,
                "reference_image_url": p.reference_image_url,
                "status": "pending",
                "video_url": None,
                "local_path": None
            })
        sync_project_from_job(job_id)
            
        update_job_status(job_id, f"generating_videos_with_{model}")
        
        for i, shot in enumerate(jobs[job_id]["shots"]):
            jobs[job_id]["shots"][i]["status"] = "processing"
            save_job(job_id)
            sync_project_from_job(job_id)
            
            if model in {"hailuo", "hailuo-2.3", "hailuo-h3", "h3"}:
                op_data = generate_video_with_hailuo(
                    shot["prompt"],
                    image_url=shot.get("reference_image_url"),
                    model_version="MiniMax-H3" if model in {"hailuo-h3", "h3"} else "MiniMax-Hailuo-2.3",
                    resolution=resolution,
                )
                if op_data and "name" in op_data:
                    result = poll_hailuo_operation(op_data["name"])
                    if result and result.get("done"):
                        url = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["video_url"] = url
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else:
                        jobs[job_id]["shots"][i]["status"] = "failed"
                else:
                    jobs[job_id]["shots"][i]["status"] = "failed"
            elif model in {"kling", "kling-3.0"}:
                op_data = generate_video_with_kling(
                    shot["prompt"],
                    image_url=shot.get("reference_image_url"),
                    resolution=resolution,
                )
                if op_data and "name" in op_data:
                    result = poll_kling_operation(op_data["name"])
                    if result and result.get("done") and result["response"].get("video_url"):
                        jobs[job_id]["shots"][i]["video_url"] = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else:
                        jobs[job_id]["shots"][i]["status"] = "failed"
                else:
                    jobs[job_id]["shots"][i]["status"] = "failed"
            elif model == "runway":
                op_data = generate_video_with_runway(shot["prompt"], image_url=shot.get("reference_image_url"))
                if op_data and "name" in op_data:
                    result = poll_runway_operation(op_data["name"])
                    if result and result.get("done"):
                        jobs[job_id]["shots"][i]["video_url"] = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else: jobs[job_id]["shots"][i]["status"] = "failed"
                else: jobs[job_id]["shots"][i]["status"] = "failed"
            elif model == "sora":
                op_data = generate_video_with_sora(shot["prompt"], image_url=shot.get("reference_image_url"))
                if op_data and "name" in op_data:
                    result = poll_sora_operation(op_data["name"])
                    if result and result.get("done"):
                        jobs[job_id]["shots"][i]["video_url"] = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else: jobs[job_id]["shots"][i]["status"] = "failed"
                else: jobs[job_id]["shots"][i]["status"] = "failed"
            elif model in {"seedance", "seedance-2.0"}:
                op_data = generate_video_with_seedance(
                    shot["prompt"],
                    image_url=shot.get("reference_image_url"),
                    resolution=resolution,
                )
                if op_data and "name" in op_data:
                    result = poll_seedance_operation(op_data["name"])
                    if result and result.get("done"):
                        jobs[job_id]["shots"][i]["video_url"] = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else: jobs[job_id]["shots"][i]["status"] = "failed"
                else: jobs[job_id]["shots"][i]["status"] = "failed"
            elif model in {"happyhorse", "happyhorse-1.1"}:
                op_data = generate_video_with_happyhorse(
                    shot["prompt"],
                    image_url=shot.get("reference_image_url"),
                    resolution=resolution,
                )
                if op_data and "name" in op_data:
                    result = poll_happyhorse_operation(op_data["name"])
                    if result and result.get("done") and result["response"].get("video_url"):
                        jobs[job_id]["shots"][i]["video_url"] = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else:
                        jobs[job_id]["shots"][i]["status"] = "failed"
                else:
                    jobs[job_id]["shots"][i]["status"] = "failed"
            elif model == "pixverse":
                op_data = generate_video_with_pixverse(
                    shot["prompt"],
                    image_url=shot.get("reference_image_url"),
                    quality=map_pixverse_quality(resolution),
                )
                if op_data and op_data.get("video_id") is not None:
                    result = poll_pixverse_operation(op_data["video_id"])
                    if result and result.get("done") and result["response"].get("video_url"):
                        jobs[job_id]["shots"][i]["video_url"] = result["response"]["video_url"]
                        jobs[job_id]["shots"][i]["status"] = "completed"
                    else:
                        jobs[job_id]["shots"][i]["status"] = "failed"
                else:
                    jobs[job_id]["shots"][i]["status"] = "failed"
            elif model in {"veo", "veo-3.1"}:
                op_data = generate_video_with_veo(
                    shot["prompt"],
                    image_url=shot.get("reference_image_url"),
                    resolution=resolution,
                )
                if op_data and "name" in op_data:
                    result = poll_veo(op_data["name"])
                    if result and result.get("done"):
                        try:
                            uri = result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                            veo_key = os.getenv("VEO3_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
                            separator = "&" if "?" in uri else "?"
                            auth_uri = f"{uri}{separator}key={veo_key}"
                            jobs[job_id]["shots"][i]["video_url"] = auth_uri
                            jobs[job_id]["shots"][i]["status"] = "completed"
                        except Exception:
                            jobs[job_id]["shots"][i]["status"] = "failed"
                    else:
                        jobs[job_id]["shots"][i]["status"] = "failed"
                else:
                    jobs[job_id]["shots"][i]["status"] = "failed"
            else:
                jobs[job_id]["shots"][i]["status"] = "failed"
            
            save_job(job_id)
            sync_project_from_job(job_id)
            
            if jobs[job_id]["shots"][i]["status"] == "completed" and jobs[job_id]["shots"][i]["video_url"]:
                local_path = PUBLIC_DIR / f"{job_id}_shot_{i+1}.mp4"
                if download_video(jobs[job_id]["shots"][i]["video_url"], str(local_path)):
                    jobs[job_id]["shots"][i]["local_path"] = str(local_path)
                    save_job(job_id)
                    sync_project_from_job(job_id)
                
        update_job_status(job_id, "stitching_videos")
        
        local_videos = [s["local_path"] for s in jobs[job_id]["shots"] if s.get("local_path")]
        if len(local_videos) > 0:
            final_video_name = f"final_{job_id}.mp4"
            final_video_path = str(PUBLIC_DIR / final_video_name)
            success = stitch_videos(local_videos, final_video_path)
            if success:
                jobs[job_id]["final_video_url"] = f"/videos/{final_video_name}"
                
        jobs[job_id]["completed"] = True
        sync_project_from_job(job_id)
        update_job_status(job_id, "completed")

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Pipeline crashed: {error_trace}")
        jobs[job_id]["completed"] = True
        update_job_status(job_id, f"failed: {str(e)}")
        
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
