import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from agents.dream_architect import DreamArchitectAgent
from agents.pixverse_director import generate_video_with_pixverse, poll_operation, download_video
from utils.logger import logger

def run_dream_pipeline(dream_text: str):
    logger.info(f"🌙 Starting RealDreams Pipeline for dream: '{dream_text}'")
    
    architect = DreamArchitectAgent()
    try:
        # Step 1: LLM parses the dream into a structured script
        script = architect.analyze_dream(dream_text=dream_text, num_shots=2)
        
        logger.info(f"🧠 Dream Title: {script.title}")
        logger.info(f"🎭 Theme: {script.theme}")
        for shot in script.shots:
            logger.info(f"   Shot {shot.shot_number}: {shot.scene_description} | {shot.camera_movement} | {shot.emotion}")

        # Step 2: Generate Prompts
        prompts = architect.generate_video_prompts(script)
        
        # Step 3: Run the Video Generators (Simulated output for now, uncomment to run real APIs)
        for i, prompt in enumerate(prompts):
            logger.info(f"🎬 Generating Dream Video Fragment {i+1} with Pixverse...")
            logger.info(f"📝 Prompt sent to API: {prompt}")
            
            # UNCOMMENT TO ACTUALLY SPEND CREDITS
            # res = generate_video_with_pixverse(prompt, model_version="v3.5")
            # if res and res.get("task_id"):
            #     final_data = poll_operation(res["task_id"])
            #     if final_data and final_data.get("video_url"):
            #         download_video(final_data["video_url"], f"dream_fragment_{i+1}.mp4")
            #         logger.info(f"✅ Dream {i+1} Materialized!")
    except Exception as e:
        logger.error(f"❌ RealDreams Pipeline Error: {e}")

if __name__ == "__main__":
    my_dream = "I was falling through a sky made of liquid gold, and there were giant jellyfish floating around me singing an old lullaby."
    run_dream_pipeline(my_dream)
