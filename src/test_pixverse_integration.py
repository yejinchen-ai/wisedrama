import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agents import pixverse_director as pd
from api import server


class DummyResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


def test_pixverse_director_requests():
    calls = []
    original_post = pd.requests.post
    original_get = pd.requests.get
    original_key = pd.PIXVERSE_API_KEY

    def fake_post(url, headers=None, json=None, files=None, data=None, timeout=None):
        calls.append(("POST", url, headers, json, data))
        if url.endswith("/openapi/v2/video/text/generate"):
            return DummyResponse(payload={"ErrCode": 0, "Resp": {"video_id": 101}})
        if url.endswith("/openapi/v2/image/upload"):
            return DummyResponse(payload={"ErrCode": 0, "Resp": {"img_id": 202}})
        if url.endswith("/openapi/v2/video/img/generate"):
            return DummyResponse(payload={"ErrCode": 0, "Resp": {"video_id": 303}})
        raise AssertionError(f"Unexpected POST url: {url}")

    def fake_get(url, headers=None, timeout=None):
        calls.append(("GET", url, headers, None, None))
        return DummyResponse(payload={"ErrCode": 0, "Resp": {"id": 303, "status": 1, "url": "https://example.com/pixverse.mp4"}})

    try:
        pd.PIXVERSE_API_KEY = "test-pixverse-key"
        pd.requests.post = fake_post
        pd.requests.get = fake_get

        text_job = pd.generate_video_with_pixverse("A fox runs through neon rain.", quality="1080p")
        assert text_job["video_id"] == 101

        image_job = pd.generate_video_with_pixverse(
            "Animate a still portrait into a cinematic shot.",
            image_url="https://example.com/ref.png",
            quality="720p",
        )
        assert image_job["video_id"] == 303

        result = pd.poll_pixverse_operation(303, poll_interval=0, timeout_seconds=1)
        assert result["done"] is True
        assert result["response"]["video_url"] == "https://example.com/pixverse.mp4"

        text_call = next(call for call in calls if call[1].endswith("/openapi/v2/video/text/generate"))
        assert text_call[2]["API-KEY"] == "test-pixverse-key"
        assert text_call[3]["aspect_ratio"] == "16:9"
        assert text_call[3]["quality"] == "1080p"

        upload_call = next(call for call in calls if call[1].endswith("/openapi/v2/image/upload"))
        assert upload_call[4]["image_url"] == "https://example.com/ref.png"

        image_call = next(call for call in calls if call[1].endswith("/openapi/v2/video/img/generate"))
        assert image_call[3]["img_id"] == 202
        assert "aspect_ratio" not in image_call[3]
    finally:
        pd.requests.post = original_post
        pd.requests.get = original_get
        pd.PIXVERSE_API_KEY = original_key


class FakeScript:
    def dict(self):
        return {"title": "PixVerse Test"}

    def model_dump_json(self):
        return "{}"


class FakeArtDirection:
    def model_dump(self):
        return {"characters": []}


class FakePrompt:
    shot_number = 1
    video_prompt = "A cinematic sunrise over a futuristic city."
    voiceover = "The city wakes up."
    reference_image_url = "https://example.com/reference.jpg"


class FakeScreenwriterAgent:
    def write_script(self, idea, num_shots=3):
        return FakeScript()


class FakeArtDirectorAgent:
    def extract_profiles(self, _script_json):
        return FakeArtDirection()

    def generate_reference_images(self, _art_direction):
        return {"hero": "https://example.com/reference.jpg"}


class FakeStoryboardAgent:
    def translate_to_video_prompts(self, _script, art_direction=None, reference_images=None):
        return [FakePrompt()]


def test_server_pixverse_branch():
    original_writer = server.ScreenwriterAgent
    original_art = server.ArtDirectorAgent
    original_storyboard = server.StoryboardAgent
    original_generate = server.generate_video_with_pixverse
    original_poll = server.poll_pixverse_operation
    original_download = server.download_video
    original_stitch = server.stitch_videos

    try:
        server.ScreenwriterAgent = FakeScreenwriterAgent
        server.ArtDirectorAgent = FakeArtDirectorAgent
        server.StoryboardAgent = FakeStoryboardAgent
        server.generate_video_with_pixverse = lambda prompt, image_url=None, quality="720p": {
            "video_id": 999,
            "quality": quality,
            "prompt": prompt,
            "image_url": image_url,
        }
        server.poll_pixverse_operation = lambda video_id: {
            "done": True,
            "response": {"video_url": "https://example.com/generated.mp4"},
        }
        server.download_video = lambda url, dest_path: True
        server.stitch_videos = lambda local_videos, final_video_path: False

        job_id = "pixverse-test-job"
        server.jobs[job_id] = {
            "status": "queued",
            "idea": "Test PixVerse integration",
            "model": "pixverse",
            "resolution": "4k",
            "script": None,
            "character_profiles": {},
            "reference_images": {},
            "shots": [],
            "final_video_url": None,
            "completed": False,
            "username": "tester",
        }

        server.run_pipeline_task(job_id, "Test PixVerse integration", 1, "pixverse", "4k")

        job = server.jobs[job_id]
        assert job["completed"] is True
        assert job["status"] == "completed"
        assert job["shots"][0]["status"] == "completed"
        assert job["shots"][0]["video_url"] == "https://example.com/generated.mp4"
    finally:
        server.ScreenwriterAgent = original_writer
        server.ArtDirectorAgent = original_art
        server.StoryboardAgent = original_storyboard
        server.generate_video_with_pixverse = original_generate
        server.poll_pixverse_operation = original_poll
        server.download_video = original_download
        server.stitch_videos = original_stitch


if __name__ == "__main__":
    test_pixverse_director_requests()
    test_server_pixverse_branch()
    print("PixVerse integration tests passed.")
