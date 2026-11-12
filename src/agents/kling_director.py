"""Kling AI 3.0 video generation client."""

import base64
import hashlib
import hmac
import json
import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

KLING_ACCESS_KEY = os.getenv("KLING_ACCESS_KEY")
KLING_SECRET_KEY = os.getenv("KLING_SECRET_KEY")
KLING_API_TOKEN = os.getenv("KLING_API_TOKEN")
KLING_BASE_URL = os.getenv("KLING_BASE_URL", "https://api-beijing.klingai.com").rstrip("/")
KLING_MODEL = os.getenv("KLING_MODEL", "kling-v3")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _token() -> str | None:
    if KLING_API_TOKEN:
        return KLING_API_TOKEN
    if not KLING_ACCESS_KEY or not KLING_SECRET_KEY:
        return None

    now = int(time.time())
    header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64url(
        json.dumps(
            {"iss": KLING_ACCESS_KEY, "exp": now + 1800, "nbf": now - 5},
            separators=(",", ":"),
        ).encode()
    )
    signature = hmac.new(
        KLING_SECRET_KEY.encode(),
        f"{header}.{payload}".encode(),
        hashlib.sha256,
    ).digest()
    return f"{header}.{payload}.{_b64url(signature)}"


def _headers() -> dict | None:
    token = _token()
    if not token:
        return None
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def generate_video_with_kling(
    prompt: str,
    image_url: str | None = None,
    model_version: str = KLING_MODEL,
    duration: int = 5,
    aspect_ratio: str = "16:9",
    resolution: str = "1080p",
    mode: str | None = None,
):
    headers = _headers()
    if not headers:
        print("❌ [Kling Director] 请配置 KLING_ACCESS_KEY/KLING_SECRET_KEY 或 KLING_API_TOKEN。")
        return None
    if not prompt or not prompt.strip():
        return None

    task_type = "image2video" if image_url else "text2video"
    selected_mode = mode or (
        "pro" if (resolution or "").lower() in {"1080p", "2k", "4k"} else "std"
    )
    payload = {
        "model_name": model_version,
        "prompt": prompt.strip(),
        "mode": selected_mode,
        "duration": str(duration),
    }
    if image_url:
        payload["image"] = image_url
    else:
        payload["aspect_ratio"] = aspect_ratio

    print(f"🎬 [Kling Director] 调用 Kling {model_version} {task_type}...")
    try:
        response = requests.post(
            f"{KLING_BASE_URL}/v1/videos/{task_type}",
            json=payload,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        task_id = data.get("data", {}).get("task_id") or data.get("task_id")
        if task_id and data.get("code", 0) == 0:
            task_name = f"{task_type}:{task_id}"
            print(f"✅ [Kling Director] 任务已提交: {task_id}")
            return {
                "name": task_name,
                "task_id": task_id,
                "task_type": task_type,
                "raw": data,
            }
        print(f"❌ [Kling Director] 任务创建失败: {data}")
    except Exception as exc:
        print(f"❌ [Kling Director] API 调用失败: {exc}")
    return None


def poll_kling_operation(
    task_name: str,
    poll_interval: int = 10,
    timeout_seconds: int = 900,
):
    headers = _headers()
    if not headers:
        return None

    if ":" in task_name:
        task_type, task_id = task_name.split(":", 1)
    else:
        task_type, task_id = "text2video", task_name

    started_at = time.time()
    url = f"{KLING_BASE_URL}/v1/videos/{task_type}/{task_id}"
    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            task = data.get("data", data)
            status = str(task.get("task_status", "")).lower()
            if status in {"succeed", "succeeded", "success", "completed"}:
                videos = task.get("task_result", {}).get("videos", [])
                video_url = videos[0].get("url") if videos else None
                if not video_url:
                    return None
                print("🎉 [Kling Director] 视频生成完成！")
                return {"done": True, "response": {"video_url": video_url, "raw": data}}
            if status in {"failed", "error", "cancelled", "canceled"}:
                print(f"❌ [Kling Director] 视频生成失败: {data}")
                return None
        except Exception as exc:
            print(f"⚠️ [Kling Director] 轮询异常，将重试: {exc}")
        time.sleep(poll_interval)

    print("❌ [Kling Director] 轮询超时。")
    return None
