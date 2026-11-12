"""Alibaba Cloud Model Studio HappyHorse 1.1 video client."""

import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

HAPPYHORSE_API_KEY = os.getenv("HAPPYHORSE_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
HAPPYHORSE_BASE_URL = os.getenv(
    "HAPPYHORSE_BASE_URL",
    "https://dashscope-intl.aliyuncs.com",
).rstrip("/")
HAPPYHORSE_T2V_MODEL = os.getenv("HAPPYHORSE_T2V_MODEL", "happyhorse-1.1-t2v")
HAPPYHORSE_I2V_MODEL = os.getenv("HAPPYHORSE_I2V_MODEL", "happyhorse-1.1-i2v")


def _headers(async_request: bool = False) -> dict:
    headers = {
        "Authorization": f"Bearer {HAPPYHORSE_API_KEY or ''}",
        "Content-Type": "application/json",
    }
    if async_request:
        headers["X-DashScope-Async"] = "enable"
    return headers


def _resolution(value: str) -> str:
    return "1080P" if (value or "").lower() in {"1080p", "2k", "4k"} else "720P"


def generate_video_with_happyhorse(
    prompt: str,
    image_url: str | None = None,
    resolution: str = "1080p",
    aspect_ratio: str = "16:9",
    duration: int = 5,
):
    if not HAPPYHORSE_API_KEY:
        print("❌ [HappyHorse Director] 请配置 HAPPYHORSE_API_KEY 或 DASHSCOPE_API_KEY。")
        return None
    if not prompt or not prompt.strip():
        return None

    model = HAPPYHORSE_I2V_MODEL if image_url else HAPPYHORSE_T2V_MODEL
    input_data = {"prompt": prompt.strip()}
    parameters = {"resolution": _resolution(resolution), "duration": duration}
    if image_url:
        input_data["media"] = [{"type": "first_frame", "url": image_url}]
    else:
        parameters["ratio"] = aspect_ratio

    payload = {"model": model, "input": input_data, "parameters": parameters}
    print(f"🎬 [HappyHorse Director] 调用 Alibaba {model}...")
    try:
        response = requests.post(
            f"{HAPPYHORSE_BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis",
            json=payload,
            headers=_headers(async_request=True),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        task_id = data.get("output", {}).get("task_id")
        if task_id:
            print(f"✅ [HappyHorse Director] 任务已提交: {task_id}")
            return {"name": task_id, "task_id": task_id, "raw": data}
        print(f"❌ [HappyHorse Director] 返回中没有 task_id: {data}")
    except Exception as exc:
        print(f"❌ [HappyHorse Director] API 调用失败: {exc}")
    return None


def poll_happyhorse_operation(
    task_id: str,
    poll_interval: int = 15,
    timeout_seconds: int = 900,
):
    if not HAPPYHORSE_API_KEY:
        return None

    started_at = time.time()
    url = f"{HAPPYHORSE_BASE_URL}/api/v1/tasks/{task_id}"
    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(url, headers=_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()
            output = data.get("output", {})
            status = str(output.get("task_status", "")).upper()
            if status == "SUCCEEDED":
                video_url = output.get("video_url")
                if not video_url:
                    return None
                print("🎉 [HappyHorse Director] 视频生成完成！")
                return {"done": True, "response": {"video_url": video_url, "raw": data}}
            if status in {"FAILED", "CANCELED", "CANCELLED", "UNKNOWN"}:
                print(f"❌ [HappyHorse Director] 视频生成失败: {data}")
                return None
        except Exception as exc:
            print(f"⚠️ [HappyHorse Director] 轮询异常，将重试: {exc}")
        time.sleep(poll_interval)

    print("❌ [HappyHorse Director] 轮询超时。")
    return None
