"""MiniMax Hailuo video generation client."""

import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

HAILUO_API_KEY = os.getenv("HAILUO_API_KEY")
HAILUO_BASE_URL = os.getenv("HAILUO_BASE_URL", "https://api.minimax.io")
HAILUO_MODEL = os.getenv("HAILUO_MODEL", "MiniMax-Hailuo-2.3")
HAILUO_H3_MODEL = os.getenv("HAILUO_H3_MODEL", "MiniMax-H3")


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {HAILUO_API_KEY or ''}",
        "Content-Type": "application/json",
    }


def _resolution(value: str) -> str:
    return "1080P" if (value or "").lower() in {"1080p", "2k", "4k"} else "720P"


def _h3_resolution(value: str) -> str:
    """Map the application's resolution choices to the H3 V2 API."""
    return "768P" if (value or "").lower() in {"720p", "768p"} else "2K"


def _is_h3(model_version: str) -> bool:
    return model_version.lower() in {"minimax-h3", "h3", "hailuo-h3"}


def generate_video_with_hailuo(
    prompt: str,
    image_url: str | None = None,
    model_version: str = HAILUO_MODEL,
    duration: int = 6,
    resolution: str = "1080p",
):
    if not HAILUO_API_KEY:
        print("❌ [Hailuo Director] 未配置 HAILUO_API_KEY。")
        return None
    if not prompt or not prompt.strip():
        print("❌ [Hailuo Director] 提示词不能为空。")
        return None

    if _is_h3(model_version):
        content = [{"type": "text", "text": prompt.strip()}]
        if image_url:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                    "role": "first_frame",
                }
            )
        payload = {
            "model": HAILUO_H3_MODEL,
            "content": content,
            "duration": min(15, max(4, duration)),
            "resolution": _h3_resolution(resolution),
            # Text-to-video requires an explicit ratio; an image determines its own ratio.
            "ratio": "adaptive" if image_url else "16:9",
        }
        endpoint = "/v2/video_generation"
    else:
        payload = {
            "model": model_version,
            "prompt": prompt.strip(),
            "duration": duration,
            "resolution": _resolution(resolution),
            "prompt_optimizer": True,
        }
        if image_url:
            payload["first_frame_image"] = image_url
        endpoint = "/v1/video_generation"

    print(f"🎬 [Hailuo Director] 调用 {model_version} ({payload['resolution']})...")
    try:
        response = requests.post(
            f"{HAILUO_BASE_URL}{endpoint}",
            json=payload,
            headers=_headers(),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        task_id = data.get("task_id")
        if task_id:
            print(f"✅ [Hailuo Director] 任务已提交: {task_id}")
            task_name = f"h3:{task_id}" if _is_h3(model_version) else task_id
            return {"name": task_name, "task_id": task_id, "raw": data}
        print(f"❌ [Hailuo Director] 返回中没有 task_id: {data}")
    except Exception as exc:
        print(f"❌ [Hailuo Director] API 调用失败: {exc}")
    return None


def poll_hailuo_operation(
    task_id: str,
    poll_interval: int = 10,
    timeout_seconds: int = 900,
):
    if not HAILUO_API_KEY:
        print("❌ [Hailuo Director] 未配置 HAILUO_API_KEY。")
        return None

    started_at = time.time()
    is_h3 = task_id.startswith("h3:")
    raw_task_id = task_id.removeprefix("h3:")
    query_url = (
        f"{HAILUO_BASE_URL}/v2/query/video_generation/{raw_task_id}"
        if is_h3
        else f"{HAILUO_BASE_URL}/v1/query/video_generation?task_id={raw_task_id}"
    )
    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(query_url, headers=_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()
            if is_h3:
                task = data.get("task", {})
                status = task.get("status")
                if status == "succeeded":
                    download_url = task.get("content", {}).get("url")
                    if not download_url:
                        print(f"❌ [Hailuo Director] H3 成功响应缺少视频 URL: {data}")
                        return None
                    print("🎉 [Hailuo Director] H3 视频生成完成！")
                    return {
                        "done": True,
                        "response": {"video_url": download_url, "raw": data},
                    }
                if status in {"failed", "cancelled"}:
                    print(f"❌ [Hailuo Director] H3 视频生成失败: {data}")
                    return None
                time.sleep(poll_interval)
                continue

            status = data.get("status")

            if status == "Success":
                file_id = data.get("file_id")
                if not file_id:
                    print(f"❌ [Hailuo Director] 成功响应缺少 file_id: {data}")
                    return None
                file_response = requests.get(
                    f"{HAILUO_BASE_URL}/v1/files/retrieve?file_id={file_id}",
                    headers=_headers(),
                    timeout=30,
                )
                file_response.raise_for_status()
                download_url = file_response.json().get("file", {}).get("download_url")
                if not download_url:
                    return None
                print("🎉 [Hailuo Director] 视频生成完成！")
                return {
                    "done": True,
                    "response": {"video_url": download_url, "raw": data},
                }

            if status in {"Fail", "Failed"}:
                print(f"❌ [Hailuo Director] 视频生成失败: {data}")
                return None
        except Exception as exc:
            print(f"⚠️ [Hailuo Director] 轮询异常，将重试: {exc}")

        time.sleep(poll_interval)

    print("❌ [Hailuo Director] 轮询超时。")
    return None
