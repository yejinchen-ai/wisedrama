"""Google Veo 3.1 video generation client."""

import base64
import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv("VEO3_API_KEY") or os.getenv("GOOGLE_API_KEY")
VEO_BASE_URL = os.getenv(
    "VEO_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta",
).rstrip("/")
VEO_MODEL = os.getenv("VEO_MODEL", "veo-3.1-generate-preview")


def _headers() -> dict:
    return {
        "x-goog-api-key": GOOGLE_API_KEY or "",
        "Content-Type": "application/json",
    }


def _resolution(value: str) -> str:
    value = (value or "").lower()
    return value if value in {"720p", "1080p", "4k"} else "1080p"


def _download_reference_image(image_url: str) -> dict | None:
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        mime_type = response.headers.get("Content-Type", "image/jpeg").split(";")[0]
        if not mime_type.startswith("image/"):
            mime_type = "image/jpeg"
        return {
            "inlineData": {
                "mimeType": mime_type,
                "data": base64.b64encode(response.content).decode("ascii"),
            }
        }
    except Exception as exc:
        print(f"⚠️ [Veo Director] 参考图下载失败，回退到文生视频: {exc}")
        return None


def generate_video_with_veo(
    prompt: str,
    image_url: str | None = None,
    model_version: str = VEO_MODEL,
    resolution: str = "1080p",
    aspect_ratio: str = "16:9",
):
    if not GOOGLE_API_KEY:
        print("❌ [Veo Director] 未配置 VEO3_API_KEY 或 GOOGLE_API_KEY。")
        return None
    if not prompt or not prompt.strip():
        print("❌ [Veo Director] 提示词不能为空。")
        return None

    instance = {"prompt": prompt.strip()}
    if image_url:
        image = _download_reference_image(image_url)
        if image:
            instance["image"] = image

    payload = {
        "instances": [instance],
        "parameters": {
            "aspectRatio": aspect_ratio,
            "resolution": _resolution(resolution),
            "personGeneration": "ALLOW_ADULT",
        },
    }

    print(f"🎬 [Veo Director] 调用 Google {model_version}...")
    try:
        response = requests.post(
            f"{VEO_BASE_URL}/models/{model_version}:predictLongRunning",
            json=payload,
            headers=_headers(),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("name"):
            print(f"✅ [Veo Director] 任务已提交: {data['name']}")
            return data
        print(f"❌ [Veo Director] 返回中没有 operation name: {data}")
    except Exception as exc:
        print(f"❌ [Veo Director] API 调用失败: {exc}")
    return None


def poll_operation(
    operation_name: str,
    download_dir: str | None = None,
    poll_interval: int = 10,
    timeout_seconds: int = 900,
):
    del download_dir  # Kept for backwards compatibility.
    if not GOOGLE_API_KEY:
        return None

    started_at = time.time()
    url = f"{VEO_BASE_URL}/{operation_name}"
    while time.time() - started_at < timeout_seconds:
        try:
            response = requests.get(url, headers=_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()
            if data.get("done"):
                if data.get("error"):
                    print(f"❌ [Veo Director] 视频生成失败: {data['error']}")
                    return None
                print("🎉 [Veo Director] 视频生成完成！")
                return data
        except Exception as exc:
            print(f"⚠️ [Veo Director] 轮询异常，将重试: {exc}")
        time.sleep(poll_interval)

    print("❌ [Veo Director] 轮询超时。")
    return None


def download_video(uri: str, filename: str):
    print(f"⬇️ [Veo Director] 下载视频到 {filename} ...")
    try:
        with requests.get(uri, headers={"x-goog-api-key": GOOGLE_API_KEY or ""}, stream=True, timeout=60) as response:
            response.raise_for_status()
            with open(filename, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=8192):
                    file_obj.write(chunk)
        print(f"✅ [Veo Director] 下载完成: {filename}")
        return True
    except Exception as exc:
        print(f"❌ [Veo Director] 下载失败: {exc}")
        return False


if __name__ == "__main__":
    result = generate_video_with_veo(
        "Cinematic tracking shot of a glowing blue flower blooming on Mars."
    )
    if result and result.get("name"):
        poll_operation(result["name"])
