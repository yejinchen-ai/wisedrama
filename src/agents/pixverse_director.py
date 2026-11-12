import os
import time
import uuid

import requests
from dotenv import load_dotenv

load_dotenv()

PIXVERSE_API_KEY = os.getenv("PIXVERSE_API_KEY")
PIXVERSE_BASE_URL = os.getenv("PIXVERSE_BASE_URL", "https://app-api.pixverse.ai")
PIXVERSE_MODEL = os.getenv("PIXVERSE_MODEL", "v5.6")

STATUS_SUCCESS = 1
STATUS_PROCESSING = 5
STATUS_MODERATION_FAILED = 7
STATUS_FAILED = 8


def _trace_headers(content_type: str | None = "application/json") -> dict:
    headers = {
        "API-KEY": PIXVERSE_API_KEY or "",
        "Ai-trace-id": str(uuid.uuid4()),
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def _response_json(response: requests.Response) -> dict | None:
    try:
        return response.json()
    except ValueError:
        return None


def _extract_resp(response_json: dict | None) -> dict:
    if not response_json:
        return {}
    return response_json.get("Resp") or {}


def upload_image_to_pixverse(image_url: str) -> int | None:
    if not PIXVERSE_API_KEY:
        print("❌ [PixVerse Director] 未配置 PIXVERSE_API_KEY。")
        return None

    print(f"🖼️ [PixVerse Director] 上传参考图到 PixVerse: {image_url}")
    try:
        response = requests.post(
            f"{PIXVERSE_BASE_URL}/openapi/v2/image/upload",
            headers=_trace_headers(content_type=None),
            files={},
            data={"image_url": image_url},
            timeout=60,
        )
        data = _response_json(response)
        if response.status_code != 200:
            print(f"❌ [PixVerse Director] 上传图片失败 ({response.status_code}): {data or response.text}")
            return None

        if data and data.get("ErrCode") == 0:
            img_id = _extract_resp(data).get("img_id")
            print(f"✅ [PixVerse Director] 图片上传成功，img_id={img_id}")
            return img_id

        print(f"❌ [PixVerse Director] 上传图片返回异常: {data}")
        return None
    except Exception as exc:
        print(f"❌ [PixVerse Director] 上传图片异常: {exc}")
        return None


def generate_video_with_pixverse(
    prompt: str,
    image_url: str = None,
    model_version: str = PIXVERSE_MODEL,
    aspect_ratio: str = "16:9",
    duration: int = 5,
    quality: str = "720p",
    motion_mode: str = "normal",
    negative_prompt: str | None = None,
    seed: int | None = None,
):
    if not PIXVERSE_API_KEY:
        print("❌ [PixVerse Director] 未配置 PIXVERSE_API_KEY。")
        return None

    print(f"🎬 [PixVerse Director] 调用 PixVerse {model_version} 接口...")

    payload = {
        "duration": duration,
        "model": model_version,
        "prompt": prompt,
        "quality": quality,
    }
    if motion_mode:
        payload["motion_mode"] = motion_mode
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if seed is not None:
        payload["seed"] = seed

    endpoint = f"{PIXVERSE_BASE_URL}/openapi/v2/video/text/generate"
    if image_url:
        img_id = upload_image_to_pixverse(image_url)
        if img_id:
            endpoint = f"{PIXVERSE_BASE_URL}/openapi/v2/video/img/generate"
            payload["img_id"] = img_id
        else:
            print("⚠️ [PixVerse Director] 参考图上传失败，回退到文生视频。")
            payload["aspect_ratio"] = aspect_ratio
    else:
        payload["aspect_ratio"] = aspect_ratio

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=_trace_headers(),
            timeout=60,
        )
        data = _response_json(response)
        if response.status_code != 200:
            print(f"❌ [PixVerse Director] 请求失败 ({response.status_code}): {data or response.text}")
            return None

        if data and data.get("ErrCode") == 0:
            video_id = _extract_resp(data).get("video_id")
            if video_id is not None:
                print(f"✅ [PixVerse Director] 任务提交成功，video_id={video_id}")
                return {"name": str(video_id), "video_id": video_id, "raw": data}

        print(f"❌ [PixVerse Director] 返回异常: {data}")
        return None
    except Exception as exc:
        print(f"❌ [PixVerse Director] 请求异常: {exc}")
        return None


def poll_pixverse_operation(video_id: int | str, poll_interval: int = 10, timeout_seconds: int = 900):
    if not PIXVERSE_API_KEY:
        print("❌ [PixVerse Director] 未配置 PIXVERSE_API_KEY。")
        return None

    print(f"⏳ [PixVerse Director] 开始轮询任务状态: {video_id}")
    url = f"{PIXVERSE_BASE_URL}/openapi/v2/video/result/{video_id}"
    started_at = time.time()

    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(url, headers=_trace_headers(content_type=None), timeout=30)
            data = _response_json(response)
            if response.status_code != 200:
                print(f"❌ [PixVerse Director] 轮询失败 ({response.status_code}): {data or response.text}")
                return None

            if data and data.get("ErrCode") == 0:
                resp = _extract_resp(data)
                status = resp.get("status")
                if status == STATUS_SUCCESS:
                    print("🎉 [PixVerse Director] 视频生成完成！")
                    return {
                        "done": True,
                        "response": {
                            "video_url": resp.get("url"),
                            "video_id": resp.get("id"),
                            "status": status,
                            "raw": data,
                        },
                    }
                if status in (STATUS_MODERATION_FAILED, STATUS_FAILED):
                    print(f"❌ [PixVerse Director] 视频生成失败，status={status}, body={data}")
                    return None

            print("🔄 [PixVerse Director] 正在生成中，稍后重试。")
        except Exception as exc:
            print(f"❌ [PixVerse Director] 轮询异常: {exc}")

        time.sleep(poll_interval)

    print("❌ [PixVerse Director] 轮询超时。")
    return None


def poll_operation(video_id: int | str, poll_interval: int = 10, timeout_seconds: int = 900):
    return poll_pixverse_operation(video_id, poll_interval=poll_interval, timeout_seconds=timeout_seconds)


def download_video(url: str, filename: str):
    print(f"⬇️ [PixVerse Director] 下载视频到 {filename} ...")
    try:
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with open(filename, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=8192):
                    file_obj.write(chunk)
        print(f"✅ [PixVerse Director] 下载完成: {filename}")
    except Exception as exc:
        print(f"❌ [PixVerse Director] 下载失败: {exc}")


if __name__ == "__main__":
    test_prompt = "Cinematic tracking shot of a glowing blue flower blooming on the red sands of Mars."
    result = generate_video_with_pixverse(test_prompt)
    if result and result.get("video_id"):
        final_data = poll_pixverse_operation(result["video_id"])
        if final_data and final_data["response"].get("video_url"):
            download_video(final_data["response"]["video_url"], "pixverse_output.mp4")
