import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The videos from Pixabay might be giving 403 Forbidden.
# Let's replace the pixabay domains with Google's robust video test bucket.
replacements = [
    "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4"
]

import json

# Extract showcaseData json string
match = re.search(r'const showcaseData = (\[.*?\]);', html, re.DOTALL)
if match:
    data_str = match.group(1)
    try:
        data = json.loads(data_str)
        for i, item in enumerate(data):
            item["video"] = replacements[i % len(replacements)]
            
        new_data_str = json.dumps(data, ensure_ascii=False)
        html = html.replace(data_str, new_data_str)
        with open(html_path, "w") as f:
            f.write(html)
        print("Video URLs successfully replaced with robust Google Storage URLs.")
    except Exception as e:
        print("Error parsing JSON:", e)
else:
    print("Could not find showcaseData array.")

