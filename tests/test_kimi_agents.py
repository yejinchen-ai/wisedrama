from unittest.mock import patch

from agents.kimi import create_kimi_chat_model
from agents.prompter import PrompterAgent
from agents.screenwriter import ScreenwriterAgent
from agents.storyboard import StoryboardAgent


def test_kimi_factory_uses_k3_and_official_code_endpoint():
    with patch("agents.kimi.ChatOpenAI") as client:
        create_kimi_chat_model(api_key="test-key")

    options = client.call_args.kwargs
    assert options["model"] == "k3"
    assert options["base_url"] == "https://api.kimi.com/coding/v1"
    assert options["default_headers"]["User-Agent"] == "WiseDrama/1.0"


def test_screenwriter_accepts_injected_llm_without_credentials():
    fake_llm = object()
    agent = ScreenwriterAgent(llm=fake_llm)

    assert agent.llm is fake_llm
    assert agent.model_name == "k3"


def test_prompter_name_remains_backward_compatible():
    assert PrompterAgent is StoryboardAgent
