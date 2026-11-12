"""Persistent project workspace API inspired by professional video production tools."""

from __future__ import annotations

import json
import threading
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .auth import get_current_user


PROJECTS_DIR = Path(__file__).resolve().parents[2] / "logs" / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
_LOCK = threading.RLock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _path(project_id: str) -> Path:
    if not project_id or any(char not in "0123456789abcdef-" for char in project_id.lower()):
        raise HTTPException(status_code=400, detail="Invalid project id")
    return PROJECTS_DIR / f"{project_id}.json"


def load_project(project_id: str) -> dict[str, Any]:
    path = _path(project_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    with _LOCK, path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_project(project: dict[str, Any]) -> dict[str, Any]:
    project["updated_at"] = _now()
    path = _path(project["id"])
    temporary = path.with_suffix(".tmp")
    with _LOCK, temporary.open("w", encoding="utf-8") as handle:
        json.dump(project, handle, ensure_ascii=False, indent=2)
    temporary.replace(path)
    return project


def update_project(project_id: str, **changes: Any) -> dict[str, Any]:
    project = load_project(project_id)
    project.update(changes)
    return save_project(project)


def require_owner(project_id: str, username: str) -> dict[str, Any]:
    project = load_project(project_id)
    if project.get("username") != username:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


class ProjectCreate(BaseModel):
    title: str = Field(default="Untitled Project", max_length=120)
    prompt: str = Field(default="", max_length=5000)
    model: str = "hailuo-h3"
    resolution: str = "2k"
    ratio: str = "16:9"
    duration_minutes: int = Field(default=1, ge=1, le=30)
    language: str = "中文"
    style: str = "电影感写实"


class SpecUpdate(BaseModel):
    ratio: str | None = None
    duration_minutes: int | None = Field(default=None, ge=1, le=30)
    language: str | None = None
    style: str | None = None
    model: str | None = None
    resolution: str | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    prompt: str | None = Field(default=None, max_length=5000)


class ShotUpdate(BaseModel):
    scene_description: str | None = None
    camera_movement: str | None = None
    character_description: str | None = None
    voiceover: str | None = None
    video_prompt: str | None = None


class ShotCreate(BaseModel):
    after_shot_number: int | None = Field(default=None, ge=1)
    scene_description: str = ""
    camera_movement: str = ""
    character_description: str = ""
    voiceover: str = ""
    video_prompt: str = ""
    duration: int = Field(default=6, ge=1, le=60)


class ShotReorder(BaseModel):
    shot_numbers: list[int]


router = APIRouter()


@router.post("")
async def create_project(req: ProjectCreate, username: str = Depends(get_current_user)):
    project_id = str(uuid.uuid4())
    timestamp = _now()
    project = {
        "id": project_id,
        "username": username,
        "title": req.title.strip() or "Untitled Project",
        "prompt": req.prompt.strip(),
        "status": "draft",
        "active_job_id": None,
        "parent_project_id": None,
        "spec": {
            "ratio": req.ratio,
            "duration_minutes": req.duration_minutes,
            "language": req.language,
            "style": req.style,
            "model": req.model,
            "resolution": req.resolution,
        },
        "script": None,
        "elements": [],
        "shots": [],
        "media": [],
        "timeline": [],
        "agent_events": [
            {"time": timestamp, "type": "project_created", "message": "项目已创建，等待创作指令。"}
        ],
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    return save_project(project)


@router.get("")
async def list_projects(username: str = Depends(get_current_user)):
    projects = []
    for path in PROJECTS_DIR.glob("*.json"):
        try:
            with path.open(encoding="utf-8") as handle:
                project = json.load(handle)
            if project.get("username") == username:
                projects.append(project)
        except (OSError, json.JSONDecodeError):
            continue
    projects.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    return {"projects": projects}


@router.get("/{project_id}")
async def get_project(project_id: str, username: str = Depends(get_current_user)):
    return require_owner(project_id, username)


@router.patch("/{project_id}")
async def patch_project(project_id: str, req: ProjectUpdate, username: str = Depends(get_current_user)):
    project = require_owner(project_id, username)
    changes = req.model_dump(exclude_none=True)
    if "title" in changes:
        changes["title"] = changes["title"].strip()
    if "prompt" in changes:
        changes["prompt"] = changes["prompt"].strip()
    project.update(changes)
    return save_project(project)


@router.patch("/{project_id}/spec")
async def patch_spec(project_id: str, req: SpecUpdate, username: str = Depends(get_current_user)):
    project = require_owner(project_id, username)
    project["spec"].update(req.model_dump(exclude_none=True))
    return save_project(project)


@router.patch("/{project_id}/shots/{shot_number}")
async def patch_shot(
    project_id: str,
    shot_number: int,
    req: ShotUpdate,
    username: str = Depends(get_current_user),
):
    project = require_owner(project_id, username)
    shot = next((item for item in project["shots"] if item.get("shot_number") == shot_number), None)
    if shot is None:
        raise HTTPException(status_code=404, detail="Shot not found")
    shot.update(req.model_dump(exclude_none=True))
    if req.video_prompt is not None:
        shot["prompt"] = req.video_prompt
    shot["edited_by_user"] = True
    return save_project(project)


def _renumber_shots(project: dict[str, Any], ordered_shots: list[dict[str, Any]]) -> None:
    """Renumber shots and keep all shot-linked workspace data consistent."""
    number_map = {
        shot.get("shot_number"): index
        for index, shot in enumerate(ordered_shots, start=1)
    }
    for index, shot in enumerate(ordered_shots, start=1):
        shot.setdefault("id", str(uuid.uuid4()))
        shot["shot_number"] = index
    project["shots"] = ordered_shots

    timeline_by_number = {
        item.get("shot_number"): item for item in project.get("timeline", [])
    }
    project["timeline"] = []
    for old_number, new_number in number_map.items():
        item = timeline_by_number.get(old_number)
        if item:
            item["shot_number"] = new_number
            project["timeline"].append(item)

    for asset in project.get("media", []):
        old_number = asset.get("shot_number")
        if old_number in number_map:
            asset["shot_number"] = number_map[old_number]


@router.post("/{project_id}/shots")
async def create_shot(
    project_id: str,
    req: ShotCreate,
    username: str = Depends(get_current_user),
):
    project = require_owner(project_id, username)
    shots = project.setdefault("shots", [])
    insert_at = len(shots)
    if req.after_shot_number is not None:
        insert_at = next(
            (i + 1 for i, shot in enumerate(shots) if shot.get("shot_number") == req.after_shot_number),
            -1,
        )
        if insert_at < 0:
            raise HTTPException(status_code=404, detail="Shot not found")
    prompt = req.video_prompt or req.scene_description
    shot = {
        "id": str(uuid.uuid4()),
        "shot_number": 0,
        "scene_description": req.scene_description,
        "camera_movement": req.camera_movement,
        "character_description": req.character_description,
        "voiceover": req.voiceover,
        "video_prompt": prompt,
        "prompt": prompt,
        "duration": req.duration,
        "status": "planned",
        "video_url": None,
        "local_path": None,
        "edited_by_user": True,
    }
    shots.insert(insert_at, shot)
    _renumber_shots(project, shots)
    project.setdefault("agent_events", []).append(
        {"time": _now(), "type": "shot_created", "message": f"新增镜头 {shot['shot_number']}。"}
    )
    return save_project(project)


@router.patch("/{project_id}/shot-order")
async def reorder_shots(
    project_id: str,
    req: ShotReorder,
    username: str = Depends(get_current_user),
):
    project = require_owner(project_id, username)
    shots = project.get("shots", [])
    current = [shot.get("shot_number") for shot in shots]
    if len(req.shot_numbers) != len(set(req.shot_numbers)) or set(req.shot_numbers) != set(current):
        raise HTTPException(status_code=400, detail="shot_numbers must contain every shot exactly once")
    by_number = {shot["shot_number"]: shot for shot in shots}
    _renumber_shots(project, [by_number[number] for number in req.shot_numbers])
    project.setdefault("agent_events", []).append(
        {"time": _now(), "type": "shots_reordered", "message": "已更新分镜和时间线顺序。"}
    )
    return save_project(project)


@router.delete("/{project_id}/shots/{shot_number}")
async def delete_shot(project_id: str, shot_number: int, username: str = Depends(get_current_user)):
    project = require_owner(project_id, username)
    shots = project.get("shots", [])
    if not any(shot.get("shot_number") == shot_number for shot in shots):
        raise HTTPException(status_code=404, detail="Shot not found")
    remaining = [shot for shot in shots if shot.get("shot_number") != shot_number]
    project["timeline"] = [
        item for item in project.get("timeline", []) if item.get("shot_number") != shot_number
    ]
    for asset in project.get("media", []):
        if asset.get("shot_number") == shot_number:
            asset["shot_number"] = None
            asset["purpose"] = "unassigned"
    _renumber_shots(project, remaining)
    project.setdefault("agent_events", []).append(
        {"time": _now(), "type": "shot_deleted", "message": f"已删除镜头 {shot_number}，素材保留在素材库。"}
    )
    return save_project(project)


@router.post("/{project_id}/branch")
async def branch_project(project_id: str, username: str = Depends(get_current_user)):
    source = require_owner(project_id, username)
    branch = deepcopy(source)
    branch["id"] = str(uuid.uuid4())
    branch["title"] = f"{source['title']} · 分支"
    branch["parent_project_id"] = source["id"]
    branch["active_job_id"] = None
    branch["status"] = "draft"
    branch["created_at"] = _now()
    branch["agent_events"].append(
        {"time": _now(), "type": "branched", "message": f"从项目 {source['title']} 创建分支。"}
    )
    return save_project(branch)
