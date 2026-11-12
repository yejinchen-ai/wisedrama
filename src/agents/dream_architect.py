import os
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class DreamShot(BaseModel):
    shot_number: int = Field(description="Sequential shot number starting from 1.")
    scene_description: str = Field(description="Visual description of what is happening in the scene. Highly descriptive, focusing on surrealism and visual elements.")
    camera_movement: str = Field(description="Camera instructions (e.g., 'Slow zoom in', 'POV perspective', 'Dutch angle').")
    emotion: str = Field(description="The underlying emotion or mood of the shot.")

class DreamScript(BaseModel):
    title: str = Field(description="A poetic or mysterious title for the dream.")
    theme: str = Field(description="The core theme (e.g., 'Surreal Discovery', 'Nightmare').")
    shots: List[DreamShot] = Field(description="List of video shots making up the dream sequence.")

class DreamArchitectAgent:
    def __init__(self):
        # We will use Google Gemini (veo/flash/pro) via LangChain.
        # Ensure GOOGLE_API_KEY is in .env
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            max_output_tokens=2048,
        )
        self.parser = PydanticOutputParser(pydantic_object=DreamScript)
        
        system_template = """You are a Master Dream Architect. 
Your job is to take a user's disjointed, surreal, or emotional dream description and translate it into a visually stunning, coherent (yet dreamlike) sequence of video shots.
Focus heavily on surrealism, ethereal lighting, first-person perspectives (POV), cinematic visuals, and impossible physics. 
Dreams often have abrupt transitions and strong emotional undertones.

{format_instructions}

User's Dream Description: {dream_text}
Please break it down into exactly {num_shots} shots.
"""
        self.prompt = ChatPromptTemplate.from_template(system_template)

    def analyze_dream(self, dream_text: str, num_shots: int = 3) -> DreamScript:
        print(f"🧠 [Dream Architect] Analyzing dream with LLM: '{dream_text}'")
        try:
            chain = self.prompt | self.llm | self.parser
            result = chain.invoke({
                "dream_text": dream_text,
                "num_shots": num_shots,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"❌ [Dream Architect] Error calling LLM: {e}")
            raise e

    def generate_video_prompts(self, script: DreamScript) -> List[str]:
        prompts = []
        for shot in script.shots:
            # Construct a highly optimized prompt for Veo/Pixverse
            prompt = f"{shot.scene_description} Camera movement: {shot.camera_movement}. Mood: {shot.emotion}. Cinematic lighting, 8k resolution, photorealistic yet surreal, dreamcore aesthetic, volumetric fog, ethereal atmosphere."
            prompts.append(prompt)
        return prompts
