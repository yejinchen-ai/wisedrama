import json

from agents import hailuo_director as hailuo
from agents import happyhorse_director as happyhorse
from agents import kling_director as kling
from agents import seedance_director as seedance
from agents import veo_director as veo
from api import server


class DummyResponse:
    def __init__(self, payload=None, status_code=200, content=b"image-bytes", headers=None):
        self._payload = payload or {}
        self.status_code = status_code
        self.content = content
        self.headers = headers or {"Content-Type": "image/png"}
        self.text = json.dumps(self._payload)

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def test_seedance_20_create_and_poll(monkeypatch):
    calls = []
    monkeypatch.setattr(seedance, "SEEDANCE_API_KEY", "seedance-key")
    monkeypatch.setattr(
        seedance.requests,
        "post",
        lambda url, **kwargs: calls.append((url, kwargs)) or DummyResponse({"id": "sd-1"}),
    )
    monkeypatch.setattr(
        seedance.requests,
        "get",
        lambda url, **kwargs: DummyResponse(
            {"status": "succeeded", "content": {"video_url": "https://example.com/sd.mp4"}}
        ),
    )

    task = seedance.generate_video_with_seedance(
        "A hero walks through rain.", image_url="https://example.com/ref.jpg", resolution="4k"
    )
    result = seedance.poll_seedance_operation(task["name"], poll_interval=0, timeout_seconds=1)

    assert task["task_id"] == "sd-1"
    assert calls[0][1]["json"]["model"] == "doubao-seedance-2-0-260128"
    assert calls[0][1]["json"]["resolution"] == "1080p"
    assert calls[0][1]["json"]["content"][1]["type"] == "image_url"
    assert result["response"]["video_url"].endswith("sd.mp4")


def test_hailuo_23_create_payload(monkeypatch):
    calls = []
    monkeypatch.setattr(hailuo, "HAILUO_API_KEY", "hailuo-key")
    monkeypatch.setattr(
        hailuo.requests,
        "post",
        lambda url, **kwargs: calls.append((url, kwargs)) or DummyResponse({"task_id": "hl-1"}),
    )

    task = hailuo.generate_video_with_hailuo(
        "Camera pushes toward the subject.", image_url="https://example.com/ref.jpg"
    )

    assert task["task_id"] == "hl-1"
    assert calls[0][0] == "https://api.minimax.io/v1/video_generation"
    assert calls[0][1]["json"]["model"] == "MiniMax-Hailuo-2.3"
    assert calls[0][1]["json"]["first_frame_image"].endswith("ref.jpg")


def test_hailuo_h3_uses_v2_multimodal_api(monkeypatch):
    calls = []
    monkeypatch.setattr(hailuo, "HAILUO_API_KEY", "hailuo-key")
    monkeypatch.setattr(
        hailuo.requests,
        "post",
        lambda url, **kwargs: calls.append((url, kwargs)) or DummyResponse({"task_id": "h3-1"}),
    )

    task = hailuo.generate_video_with_hailuo(
        "A singer performs on stage.",
        image_url="https://example.com/singer.jpg",
        model_version="MiniMax-H3",
        duration=20,
        resolution="2k",
    )

    payload = calls[0][1]["json"]
    assert task["name"] == "h3:h3-1"
    assert calls[0][0] == "https://api.minimax.io/v2/video_generation"
    assert payload["model"] == "MiniMax-H3"
    assert payload["resolution"] == "2K"
    assert payload["duration"] == 15
    assert payload["ratio"] == "adaptive"
    assert payload["content"][1] == {
        "type": "image_url",
        "image_url": {"url": "https://example.com/singer.jpg"},
        "role": "first_frame",
    }


def test_hailuo_h3_poll_returns_v2_video_url(monkeypatch):
    calls = []
    monkeypatch.setattr(hailuo, "HAILUO_API_KEY", "hailuo-key")
    monkeypatch.setattr(
        hailuo.requests,
        "get",
        lambda url, **kwargs: calls.append(url)
        or DummyResponse(
            {
                "task": {
                    "status": "succeeded",
                    "content": {"url": "https://example.com/h3.mp4"},
                }
            }
        ),
    )

    result = hailuo.poll_hailuo_operation("h3:task-1", poll_interval=0, timeout_seconds=1)

    assert calls == ["https://api.minimax.io/v2/query/video_generation/task-1"]
    assert result["response"]["video_url"] == "https://example.com/h3.mp4"


def test_kling_30_uses_signed_auth_and_image_endpoint(monkeypatch):
    calls = []
    monkeypatch.setattr(kling, "KLING_ACCESS_KEY", "access")
    monkeypatch.setattr(kling, "KLING_SECRET_KEY", "secret")
    monkeypatch.setattr(kling, "KLING_API_TOKEN", None)
    monkeypatch.setattr(
        kling.requests,
        "post",
        lambda url, **kwargs: calls.append((url, kwargs))
        or DummyResponse({"code": 0, "data": {"task_id": "kl-1"}}),
    )

    task = kling.generate_video_with_kling(
        "A dancer turns toward camera.", image_url="https://example.com/ref.jpg"
    )

    assert task["name"] == "image2video:kl-1"
    assert calls[0][0].endswith("/v1/videos/image2video")
    assert calls[0][1]["json"]["model_name"] == "kling-v3"
    assert calls[0][1]["json"]["mode"] == "pro"
    assert calls[0][1]["headers"]["Authorization"].startswith("Bearer ey")


def test_happyhorse_11_create_payload(monkeypatch):
    calls = []
    monkeypatch.setattr(happyhorse, "HAPPYHORSE_API_KEY", "happy-key")
    monkeypatch.setattr(
        happyhorse.requests,
        "post",
        lambda url, **kwargs: calls.append((url, kwargs))
        or DummyResponse({"output": {"task_id": "hh-1", "task_status": "PENDING"}}),
    )

    task = happyhorse.generate_video_with_happyhorse(
        "A cardboard city wakes up.", image_url="https://example.com/ref.jpg"
    )

    assert task["task_id"] == "hh-1"
    assert calls[0][1]["json"]["model"] == "happyhorse-1.1-i2v"
    assert calls[0][1]["json"]["input"]["media"][0]["type"] == "first_frame"
    assert calls[0][1]["headers"]["X-DashScope-Async"] == "enable"


def test_veo_31_uses_official_model_and_inline_reference(monkeypatch):
    calls = []
    monkeypatch.setattr(veo, "GOOGLE_API_KEY", "veo-key")
    monkeypatch.setattr(
        veo.requests,
        "get",
        lambda url, **kwargs: DummyResponse(content=b"png", headers={"Content-Type": "image/png"}),
    )
    monkeypatch.setattr(
        veo.requests,
        "post",
        lambda url, **kwargs: calls.append((url, kwargs)) or DummyResponse({"name": "operations/veo-1"}),
    )

    task = veo.generate_video_with_veo(
        "A glowing flower blooms.", image_url="https://example.com/ref.png", resolution="4k"
    )

    assert task["name"] == "operations/veo-1"
    assert "/models/veo-3.1-generate-preview:predictLongRunning" in calls[0][0]
    assert calls[0][1]["json"]["parameters"]["resolution"] == "4k"
    assert calls[0][1]["json"]["instances"][0]["image"]["inlineData"]["mimeType"] == "image/png"


def test_server_exposes_new_models():
    assert {
        "seedance-2.0",
        "kling-3.0",
        "hailuo-2.3",
        "hailuo-h3",
        "veo-3.1",
        "happyhorse-1.1",
    }.issubset(server.SUPPORTED_MODELS)
