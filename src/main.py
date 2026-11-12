import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure we can import from src
sys.path.append(str(Path(__file__).resolve().parent))

from utils.logger import logger
from agents.screenwriter import ScreenwriterAgent
from agents.prompter import PrompterAgent

load_dotenv()

def run_pipeline(idea: str, num_shots: int = 3):
    logger.info(f"🎬 WiseDrama Pipeline Started for idea: '{idea}'")
    
    try:
        # Step 1: Screenwriting (Idea -> Script)
        writer = ScreenwriterAgent()
        script = writer.write_script(idea=idea, num_shots=num_shots)
        
        logger.info(f"📝 Script Generated: {script.title}")
        for shot in script.shots:
            logger.info(f"   Shot {shot.shot_number}: {shot.scene_description[:50]}...")
            
        # Step 2: Prompt Engineering (Script -> Video Prompts)
        prompter = PrompterAgent()
        optimized_prompts = prompter.translate_to_video_prompts(script)
        
        logger.info("🪄 Prompts Optimized:")
        for op in optimized_prompts:
            logger.info(f"   [Shot {op.shot_number}] Prompt: {op.video_prompt}")
            logger.info(f"   [Shot {op.shot_number}] Voiceover: {op.voiceover}")
            
        # Step 3: Director (Prompts -> Video Generation API)
        # TODO: Integrate hailuo_director.py here to execute the prompts concurrently
        logger.info("⏳ Step 3 (Video Generation) is pending API quota...")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise e

    logger.info("✅ Pipeline executed successfully.")

if __name__ == "__main__":
    test_idea = "A lonely astronaut discovers a glowing blue flower on Mars."
    run_pipeline(test_idea)
