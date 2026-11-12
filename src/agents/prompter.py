from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import json

from .screenwriter import Script, Shot
# Since ArtDirection is not directly importable from art_director (it's defined inside art_director.py),
# we will just use Any for typing or import it correctly.
from .art_director import ArtDirection
from .kimi import create_kimi_chat_model

load_dotenv()

class OptimizedPrompt(BaseModel):
    shot_number: int = Field(description="The sequential number of the shot")
    video_prompt: str = Field(description="A highly descriptive, cinematic, and comma-separated prompt optimized for Veo/Sora.")
    voiceover: str = Field(description="The voiceover for the shot")
    reference_image_url: Optional[str] = None

class EnhancedPrompts(BaseModel):
    prompts: List[OptimizedPrompt]

class StoryboardAgent:
    """Turn a screenplay into generation-ready, continuity-aware storyboards."""

    def __init__(self, model_name: str | None = None, *, llm=None):
        self.llm = llm or create_kimi_chat_model(model_name=model_name, temperature=0.7)
        self.parser = PydanticOutputParser(pydantic_object=EnhancedPrompts)

    def translate_to_video_prompts(self, script: Script, art_direction: ArtDirection = None, reference_images: dict = None) -> List[OptimizedPrompt]:
        """
        Uses an LLM to smartly upsample and rewrite the raw script into professional cinematic prompts.
        It also ensures 'Temporal Consistency' by asking the LLM to naturally link the end of Shot N with the start of Shot N+1.
        """
        print(f"🪄 [Prompter] 启动智能提示词引擎 (Prompt Upsampling & Temporal Smoothing)...")
        
        optimized_prompts = []
        
        # Prepare context for the LLM
        script_context = []
        for shot in script.shots:
            char_desc = shot.character_description
            image_url = None
            if art_direction:
                locked_chars = []
                for profile in art_direction.character_profiles:
                    if profile.name.lower() in shot.character_description.lower() or profile.name.lower() in shot.scene_description.lower():
                        locked_chars.append(f"[{profile.name}: {profile.appearance_prompt}]")
                        if reference_images and profile.name in reference_images and not image_url:
                            image_url = reference_images[profile.name]
                if locked_chars:
                    char_desc = " ".join(locked_chars) + " " + char_desc
            
            script_context.append({
                "shot_number": shot.shot_number,
                "camera": shot.camera_movement,
                "action": shot.scene_description,
                "character": char_desc,
                "voiceover": shot.voiceover,
                "image_url": image_url
            })

        global_style = art_direction.style_guideline if art_direction else script.style_guideline
        
        template = """
        You are WiseDrama's lead storyboard director and AI video prompt engineer.
        Convert the screenplay into a production-ready shot list while preserving its language,
        narrative intent, character identity, spatial continuity, and exact shot count.
        
        ALGORITHM RULES (Temporal Consistency & Upsampling):
        1. Add professional camera lens terminology (e.g., 50mm lens, f/1.8, cinematic lighting, volumetric fog, dynamic motion).
        2. Ensure the action in Shot N naturally flows from the end of Shot N-1 (Temporal Smoothing).
        3. Keep the exact character locked prompts (enclosed in brackets like [Name: ...]) untouched in the text so the model recognizes them.
        4. Make the visual description as detailed as possible to prevent hallucination by the Video AI.
        5. Output strictly in the requested JSON format.
        6. Return exactly one prompt for every raw shot, in the same order and with the same shot_number.
        7. Keep dialogue and voiceover unchanged. Do not invent spoken lines.
        
        Global Style: {style}
        Raw Shots Context:
        {shots_json}
        
        {format_instructions}
        """
        
        prompt_chain = PromptTemplate(
            template=template,
            input_variables=["style", "shots_json"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        ) | self.llm | self.parser
        
        print(f"🧠 [Prompter] 正在进行上下文感知重写 (Context-Aware Rewriting) 和镜头平滑过渡计算...")
        try:
            enhanced_result = prompt_chain.invoke({
                "style": global_style,
                "shots_json": json.dumps(script_context, indent=2)
            })

            if len(enhanced_result.prompts) != len(script_context):
                raise ValueError(
                    f"expected {len(script_context)} storyboard prompts, "
                    f"got {len(enhanced_result.prompts)}"
                )
            
            # Map the reference URLs back
            for i, p in enumerate(enhanced_result.prompts):
                p.shot_number = script_context[i]["shot_number"]
                p.voiceover = script_context[i]["voiceover"]
                p.reference_image_url = script_context[i]["image_url"]
                optimized_prompts.append(p)
                
            print(f"✅ [Prompter] 提示词升维 (Upsampling) 处理完成，输出了 {len(optimized_prompts)} 个强化分镜。")
            return optimized_prompts
        except Exception as e:
            print(f"⚠️ [Prompter] LLM提示词优化失败，回退到基础拼接算法: {e}")
            for ctx in script_context:
                prompt_str = f"{global_style}. {ctx['camera']}. {ctx['character']}. {ctx['action']}."
                optimized_prompts.append(OptimizedPrompt(
                    shot_number=ctx["shot_number"],
                    video_prompt=prompt_str,
                    voiceover=ctx["voiceover"],
                    reference_image_url=ctx["image_url"]
                ))
            return optimized_prompts


# Backward-compatible name for callers outside the main pipeline.
PrompterAgent = StoryboardAgent
