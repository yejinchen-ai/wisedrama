"""Shared Kimi K3 configuration for WiseDrama's creative agents."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env.local")
load_dotenv(PROJECT_ROOT / ".env")

DEFAULT_KIMI_MODEL = "k3"
DEFAULT_KIMI_BASE_URL = "https://api.kimi.com/coding/v1"


class KimiConfigurationError(RuntimeError):
    """Raised when a Kimi-backed agent is missing required configuration."""


def create_kimi_chat_model(
    *,
    model_name: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    temperature: float = 0.7,
    max_tokens: int | None = None,
) -> Any:
    """Create the OpenAI-compatible Kimi client used by creative agents."""
    resolved_key = api_key or os.getenv("KIMI_API_KEY")
    if not resolved_key:
        raise KimiConfigurationError("KIMI_API_KEY is required for Kimi creative agents")

    options: dict[str, Any] = {
        "model": model_name or os.getenv("KIMI_MODEL", DEFAULT_KIMI_MODEL),
        "api_key": resolved_key,
        "base_url": base_url or os.getenv("KIMI_BASE_URL", DEFAULT_KIMI_BASE_URL),
        "temperature": temperature,
        # Kimi Code requires clients to keep their real identity.
        "default_headers": {"User-Agent": "WiseDrama/1.0"},
    }
    if max_tokens is not None:
        options["max_tokens"] = max_tokens
    return ChatOpenAI(**options)
