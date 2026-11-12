"""Screenwriter agent for turning a story idea into a validated shot list."""

from __future__ import annotations

import os
from typing import Any, List

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .kimi import KimiConfigurationError, create_kimi_chat_model


load_dotenv()

MAX_IDEA_LENGTH = 5_000
MAX_SHOTS = 30


class ScreenwriterError(RuntimeError):
    """Base exception raised by the screenwriter agent."""


class ScreenwriterConfigurationError(ScreenwriterError):
    """Raised when the screenwriter cannot be configured."""


class ScreenwriterGenerationError(ScreenwriterError):
    """Raised when every script generation attempt fails."""


class Shot(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    shot_number: int = Field(ge=1, description="The sequential number of the shot")
    scene_description: str = Field(
        min_length=1,
        description="Visual description of the scene, action, and end state",
    )
    character_description: str = Field(
        min_length=1,
        description=(
            "Locked physical description of every visible character; repeated verbatim "
            "whenever that character appears"
        ),
    )
    camera_movement: str = Field(
        min_length=1,
        description="A physically achievable camera framing and movement",
    )
    voiceover: str = Field(
        description=(
            "Narration or dialogue for this shot; use the literal string 'None' when silent"
        ),
    )

    @field_validator("voiceover", mode="before")
    @classmethod
    def normalize_voiceover(cls, value: Any) -> str:
        if value is None or not str(value).strip():
            return "None"
        return str(value).strip()


class Script(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, description="The title of the short drama")
    style_guideline: str = Field(
        min_length=1,
        description=(
            "A reusable global visual style covering medium, palette, lighting, texture, "
            "and aspect-ratio composition"
        ),
    )
    shots: List[Shot] = Field(
        min_length=1,
        description="Ordered shots that form a complete visual story",
    )


SCREENWRITER_PROMPT = """
You are the lead screenwriter and storyboard director for an AI short-drama studio.
Turn the user's idea into a complete, emotionally coherent, highly visual script that can
be handed directly to text-to-video models such as Veo, Sora, Hailuo, and Seedance.

STORY REQUIREMENTS:
1. Write in the same language as the user's idea unless the idea explicitly requests another language.
2. Create a clear setup, escalation, climax, and resolution across EXACTLY {num_shots} shots.
3. Give every shot one primary, filmable action. State the environment, subject placement,
   visible action, and the shot's ending visual state. Never rely on abstract or invisible concepts.
4. Make adjacent shots flow naturally: the beginning of a shot must be compatible with the
   ending state, location, props, time of day, and character positions established previously.
5. Treat each shot as a concise video clip. Avoid scene changes or multiple unrelated actions
   inside a single shot.

CONTINUITY BIBLE (MANDATORY):
1. Before writing, silently define one canonical appearance for every recurring character:
   apparent age, face, hair/fur, body build, signature clothing, colors, and persistent accessories.
2. In character_description, repeat a character's canonical appearance VERBATIM every time
   that character is visible. Do not shorten, paraphrase, recolor, or change clothing between shots
   unless the story explicitly depicts the change on screen.
3. Include only visible characters in character_description. Use the literal string "None"
   for shots without visible characters.
4. Keep recurring locations, props, weather, and lighting visually consistent unless the story
   explicitly shows a transition.

SHOT AND AUDIO RULES:
1. Number shots sequentially from 1 through {num_shots} with no gaps or duplicates.
2. camera_movement must describe one achievable framing/movement (for example, static wide shot,
   slow dolly-in, handheld medium close-up, or overhead crane shot). Do not combine incompatible moves.
3. Keep dialogue/voiceover short enough to fit the visual clip. Use the literal string "None" when silent.
4. style_guideline must be a single reusable visual specification, not a plot summary.
5. Do not include markdown, commentary, safety notes, or fields outside the requested schema.

User idea:
{idea}

Feedback from the previous attempt:
{validation_feedback}

{format_instructions}
"""


class ScreenwriterAgent:
    """Generate and validate structured short-drama scripts."""

    def __init__(
        self,
        model_name: str | None = None,
        *,
        llm: Any | None = None,
        api_key: str | None = None,
        temperature: float = 0.7,
        max_attempts: int = 3,
    ) -> None:
        if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")

        self.model_name = model_name or os.getenv("KIMI_MODEL", "k3")
        self.max_attempts = max_attempts
        self.parser = PydanticOutputParser(pydantic_object=Script)
        self.prompt = PromptTemplate(
            template=SCREENWRITER_PROMPT,
            input_variables=["idea", "num_shots", "validation_feedback"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
            },
        )

        if llm is not None:
            self.llm = llm
            return

        try:
            self.llm = create_kimi_chat_model(
                model_name=self.model_name,
                api_key=api_key,
                temperature=temperature,
            )
        except KimiConfigurationError as exc:
            raise ScreenwriterConfigurationError(
                "KIMI_API_KEY is required to initialize ScreenwriterAgent"
            ) from exc

    def write_script(self, idea: str, num_shots: int = 5) -> Script:
        """Expand an idea into an exact, validated, shot-by-shot script."""
        normalized_idea = self._validate_inputs(idea, num_shots)
        print(
            f"✍️ [Screenwriter] 正在将灵感扩写为 {num_shots} 个分镜: "
            f"'{normalized_idea}'..."
        )

        validation_feedback = "None. This is the first attempt."
        last_error: Exception | None = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                prompt_value = self.prompt.invoke(
                    {
                        "idea": normalized_idea,
                        "num_shots": num_shots,
                        "validation_feedback": validation_feedback,
                    }
                )
                raw_response = self.llm.invoke(prompt_value)
                script = self.parser.invoke(raw_response)
                script = self._finalize_script(script, num_shots)

                print(
                    f"✅ [Screenwriter] 剧本完成！标题: {script.title}, "
                    f"共 {len(script.shots)} 个分镜。"
                )
                return script
            except Exception as exc:
                last_error = exc
                compact_error = self._compact_error(exc)
                validation_feedback = (
                    f"Attempt {attempt} was rejected: {compact_error}. Regenerate the entire "
                    f"script and obey every rule, especially the exact count of {num_shots} shots."
                )
                if attempt < self.max_attempts:
                    print(
                        f"⚠️ [Screenwriter] 第 {attempt} 次输出未通过校验，正在重试: "
                        f"{compact_error}"
                    )

        message = (
            f"Screenwriter failed to generate a valid {num_shots}-shot script after "
            f"{self.max_attempts} attempts"
        )
        if last_error is not None:
            message = f"{message}: {self._compact_error(last_error)}"
        raise ScreenwriterGenerationError(message) from last_error

    @staticmethod
    def _validate_inputs(idea: str, num_shots: int) -> str:
        if not isinstance(idea, str) or not idea.strip():
            raise ValueError("idea must be a non-empty string")

        normalized_idea = idea.strip()
        if len(normalized_idea) > MAX_IDEA_LENGTH:
            raise ValueError(f"idea must not exceed {MAX_IDEA_LENGTH} characters")

        if isinstance(num_shots, bool) or not isinstance(num_shots, int):
            raise ValueError("num_shots must be an integer")
        if not 1 <= num_shots <= MAX_SHOTS:
            raise ValueError(f"num_shots must be between 1 and {MAX_SHOTS}")

        return normalized_idea

    @staticmethod
    def _finalize_script(script: Script, num_shots: int) -> Script:
        actual_count = len(script.shots)
        if actual_count != num_shots:
            raise ValueError(
                f"expected exactly {num_shots} shots, but the model returned {actual_count}"
            )

        # The list order is the narrative order. Canonical numbering protects all downstream
        # agents from harmless model mistakes such as duplicated or skipped shot numbers.
        for shot_number, shot in enumerate(script.shots, start=1):
            shot.shot_number = shot_number

        return script

    @staticmethod
    def _compact_error(error: Exception) -> str:
        message = " ".join(str(error).split()) or error.__class__.__name__
        return message[:500]


if __name__ == "__main__":
    try:
        agent = ScreenwriterAgent()
        test_script = agent.write_script(
            "一只叫奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干",
            num_shots=3,
        )
        print(test_script.model_dump_json(indent=2))
    except ScreenwriterError as exc:
        print(f"Screenwriter test skipped: {exc}")
