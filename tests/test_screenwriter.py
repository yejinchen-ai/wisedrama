import json

import pytest

from agents.screenwriter import (
    MAX_IDEA_LENGTH,
    ScreenwriterAgent,
    ScreenwriterGenerationError,
    Shot,
)


class FakeLLM:
    def __init__(self, responses):
        self.responses = list(responses)
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt.to_string())
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def make_script_json(count, shot_numbers=None):
    shot_numbers = shot_numbers or list(range(1, count + 1))
    return json.dumps(
        {
            "title": "霓虹追踪",
            "style_guideline": "电影级赛博朋克，蓝红霓虹，潮湿街道，2.39:1 构图",
            "shots": [
                {
                    "shot_number": shot_numbers[index],
                    "scene_description": f"奥利奥穿过第 {index + 1} 条霓虹街巷。",
                    "character_description": "橘猫奥利奥，翠绿色眼睛，蓝色小围巾，左耳有一道小缺口",
                    "camera_movement": "低机位缓慢跟拍",
                    "voiceover": None if index == 0 else "我一定会找到它。",
                }
                for index in range(count)
            ],
        },
        ensure_ascii=False,
    )


def test_generates_valid_script_and_canonicalizes_shot_numbers():
    llm = FakeLLM([make_script_json(3, shot_numbers=[7, 7, 99])])
    agent = ScreenwriterAgent(llm=llm, max_attempts=1)

    script = agent.write_script("  一只橘猫寻找遗失的小鱼干  ", num_shots=3)

    assert [shot.shot_number for shot in script.shots] == [1, 2, 3]
    assert script.shots[0].voiceover == "None"
    assert "EXACTLY 3 shots" in llm.prompts[0]
    assert "一只橘猫寻找遗失的小鱼干" in llm.prompts[0]


def test_retries_with_validation_feedback_when_shot_count_is_wrong():
    llm = FakeLLM([make_script_json(1), make_script_json(2)])
    agent = ScreenwriterAgent(llm=llm, max_attempts=2)

    script = agent.write_script("雨夜中的重逢", num_shots=2)

    assert len(script.shots) == 2
    assert len(llm.prompts) == 2
    assert "expected exactly 2 shots" in llm.prompts[1]
    assert "exact count of 2 shots" in llm.prompts[1]


@pytest.mark.parametrize(
    ("idea", "num_shots", "expected_message"),
    [
        ("", 3, "non-empty"),
        ("   ", 3, "non-empty"),
        ("story", 0, "between 1 and 30"),
        ("story", 31, "between 1 and 30"),
        ("story", True, "must be an integer"),
        ("x" * (MAX_IDEA_LENGTH + 1), 3, "must not exceed"),
    ],
)
def test_rejects_invalid_inputs_before_calling_llm(idea, num_shots, expected_message):
    llm = FakeLLM([make_script_json(3)])
    agent = ScreenwriterAgent(llm=llm)

    with pytest.raises(ValueError, match=expected_message):
        agent.write_script(idea, num_shots=num_shots)

    assert llm.prompts == []


def test_raises_domain_error_after_all_attempts_fail():
    llm = FakeLLM(["not json", RuntimeError("provider unavailable")])
    agent = ScreenwriterAgent(llm=llm, max_attempts=2)

    with pytest.raises(ScreenwriterGenerationError, match="after 2 attempts"):
        agent.write_script("太空站最后一夜", num_shots=2)

    assert len(llm.prompts) == 2


def test_shot_strips_text_and_normalizes_empty_voiceover():
    shot = Shot(
        shot_number=1,
        scene_description="  主角推开舱门。  ",
        character_description="  黑色短发，白色宇航服  ",
        camera_movement="  缓慢推近  ",
        voiceover="   ",
    )

    assert shot.scene_description == "主角推开舱门。"
    assert shot.character_description == "黑色短发，白色宇航服"
    assert shot.camera_movement == "缓慢推近"
    assert shot.voiceover == "None"
