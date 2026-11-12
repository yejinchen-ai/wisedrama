"""Volcengine Ark client for Seedance video generation."""

import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

SEEDANCE_API_KEY = os.getenv("SEEDANCE_API_KEY")
SEEDANCE_BASE_URL = os.getenv(
    "SEEDANCE_BASE_URL",
    "https://ark.cn-beijing.volces.com/api/v3",
).rstrip("/")
SEEDANCE_MODEL = os.getenv("SEEDANCE_MODEL", "doubao-seedance-2-0-260128")


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {SEEDANCE_API_KEY or ''}",
        "Content-Type": "application/json",
    }


def _resolution(value: str) -> str:
    value = (value or "").lower()
    if value in {"1080p", "2k", "4k"}:
        return "1080p"
    if value == "480p":
        return "480p"
    return "720p"


def generate_video_with_seedance(
    prompt: str,
    image_url: str | None = None,
    model_version: str = SEEDANCE_MODEL,
    resolution: str = "1080p",
    aspect_ratio: str = "16:9",
    duration: int = 5,
):
    if not SEEDANCE_API_KEY:
        print("❌ [Seedance Director] 未配置 SEEDANCE_API_KEY。")
        return None
    if not prompt or not prompt.strip():
        print("❌ [Seedance Director] 提示词不能为空。")
        return None

    content = [{"type": "text", "text": prompt.strip()}]
    if image_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            }
        )

    payload = {
        "model": model_version,
        "content": content,
        "ratio": aspect_ratio,
        "duration": duration,
        "resolution": _resolution(resolution),
        "watermark": False,
    }

    print(f"🎬 [Seedance Director] 调用 {model_version} ({payload['resolution']})...")
    try:
        response = requests.post(
            f"{SEEDANCE_BASE_URL}/contents/generations/tasks",
            json=payload,
            headers=_headers(),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        task_id = data.get("id") or data.get("task_id")
        if task_id:
            print(f"✅ [Seedance Director] 任务已提交: {task_id}")
            return {"name": task_id, "task_id": task_id, "raw": data}
        print(f"❌ [Seedance Director] 返回中没有任务 ID: {data}")
    except Exception as exc:
        print(f"❌ [Seedance Director] API 调用失败: {exc}")
    return None


def _video_url(data: dict) -> str | None:
    for container in (
        data.get("content"),
        data.get("output"),
        data.get("result"),
        data,
    ):
        if isinstance(container, dict) and container.get("video_url"):
            return container["video_url"]
    return None


def poll_seedance_operation(
    task_id: str,
    poll_interval: int = 10,
    timeout_seconds: int = 900,
):
    if not SEEDANCE_API_KEY:
        print("❌ [Seedance Director] 未配置 SEEDANCE_API_KEY。")
        return None

    started_at = time.time()
    url = f"{SEEDANCE_BASE_URL}/contents/generations/tasks/{task_id}"
    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(url, headers=_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()
            status = str(data.get("status", "")).lower()
            if status in {"succeeded", "success", "completed"}:
                url_value = _video_url(data)
                if not url_value:
                    print(f"❌ [Seedance Director] 成功响应缺少 video_url: {data}")
                    return None
                print("🎉 [Seedance Director] 视频生成完成！")
                return {
                    "done": True,
                    "response": {"video_url": url_value, "raw": data},
                }
            if status in {"failed", "cancelled", "canceled", "expired"}:
                print(f"❌ [Seedance Director] 视频生成失败: {data}")
                return None
        except Exception as exc:
            print(f"⚠️ [Seedance Director] 轮询异常，将重试: {exc}")

        time.sleep(poll_interval)

    print("❌ [Seedance Director] 轮询超时。")
    return None
