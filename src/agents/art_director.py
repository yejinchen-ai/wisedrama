from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class CharacterProfile(BaseModel):
    name: str = Field(description="Name of the character")
    appearance_prompt: str = Field(description="A highly detailed visual description of the character (e.g., age, ethnicity, facial features, hair, clothing) optimized for image generation to maintain exact visual consistency.")
    role: str = Field(description="The character's role in the story")

class ArtDirection(BaseModel):
    style_guideline: str = Field(description="Global visual style (e.g., Cinematic lighting, 8k resolution, Cyberpunk, Watercolor)")
    character_profiles: List[CharacterProfile] = Field(description="List of characters and their fixed appearance prompts")

class ArtDirectorAgent:
    def __init__(self, model_name: str = "gemini-2.5-pro"):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7, api_key=GOOGLE_API_KEY)
        self.parser = PydanticOutputParser(pydantic_object=ArtDirection)

    def extract_profiles(self, script_text: str) -> ArtDirection:
        """
        Analyzes the script and creates locked-down character prompts (Global Prompt Locking).
        """
        template = """
        You are an expert Art Director for AI video generation.
        Your task is to analyze the following script and extract the main characters.
        For each character, you must create a highly detailed 'appearance_prompt' that will be injected into every shot they appear in, ensuring visual consistency (Prompt Locking).
        Also, define the global visual style.
        
        Script: {script}
        
        {format_instructions}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["script"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm | self.parser
        
        print("🎨 [ArtDirector] 正在提取角色特征并锁定提示词 (Prompt Locking)...")
        art_direction = chain.invoke({"script": script_text})
        print(f"✅ [ArtDirector] 美术设定完成！提取了 {len(art_direction.character_profiles)} 个主要角色。")
        
        return art_direction
    
    def generate_reference_images(self, art_direction: ArtDirection) -> Dict[str, str]:
        """
        Calls a T2I model (e.g. mock implementation for now) to generate reference images 
        for Image-to-Video generation (I2V).
        """
        print("🖼️ [ArtDirector] 正在生成角色参考定妆照 (Reference Images)...")
        reference_images = {}
        for profile in art_direction.character_profiles:
            # TODO: Integrate actual T2I API (Flux, DALL-E 3, Imagen 3, etc.)
            # For now, return a placeholder URL or generic image
            mock_url = f"https://image.pollinations.ai/prompt/{profile.appearance_prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
            reference_images[profile.name] = mock_url
            print(f"   - {profile.name}: {mock_url}")
            
        return reference_images

if __name__ == "__main__":
    try:
        agent = ArtDirectorAgent()
        sample_script = "A cyberpunk story about Leo, a 25-year-old hacker with neon blue hair and a leather jacket."
        art = agent.extract_profiles(sample_script)
        refs = agent.generate_reference_images(art)
        print(art.model_dump_json(indent=2))
        print(refs)
    except Exception as e:
        print(f"Test skipped: {e}")
