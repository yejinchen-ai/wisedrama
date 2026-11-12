import os
import time
import uuid
from dotenv import load_dotenv

load_dotenv()

SORA_API_KEY = os.getenv("SORA_API_KEY", os.getenv("OPENAI_API_KEY"))

def generate_video_with_sora(prompt: str, image_url: str = None):
    print(f"🎬 [Sora Director] 准备调用 Sora 2.0 接口...")
    
    task_id = f"sora_task_{uuid.uuid4()}"
    print(f"🚀 发送生成请求，获得任务ID: {task_id}")
    return {"name": task_id}

def poll_sora_operation(task_id: str):
    print(f"⏳ 开始轮询任务状态: {task_id}")
    
    # Simulate API processing delay
    time.sleep(15) 
    
    print(f"\n🎉 [Sora] 视频生成完成！")
    # Return a dummy video URL
    return {
        "done": True,
        "response": {
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    }
