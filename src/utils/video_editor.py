import os
import subprocess
from pathlib import Path

def stitch_videos(video_paths, output_path):
    if not video_paths:
        return False
        
    print(f"✂️ [Editor Agent] 准备将 {len(video_paths)} 段视频拼接成正片，并进行 Web 串流优化...")
    
    list_file_path = output_path + ".txt"
    with open(list_file_path, "w") as f:
        for vp in video_paths:
            f.write(f"file '{vp}'\n")
            
    try:
        # Instead of just -c copy, we need to ensure the MOOV atom is at the beginning of the file for fast web playback (faststart)
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
            "-i", list_file_path, 
            "-c", "copy",
            "-movflags", "faststart",
            output_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"✅ [Editor Agent] 拼接并优化完成: {output_path}")
            os.remove(list_file_path)
            return True
        else:
            print(f"❌ [Editor Agent] FFmpeg 报错: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ [Editor Agent] 拼接抛出异常: {e}")
        return False
