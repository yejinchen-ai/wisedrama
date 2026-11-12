html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re
import subprocess

with open("/tmp/test.js", "w") as f:
    f.write("")

# We must meticulously find what is breaking JS.
script_blocks = re.findall(r'<script>(.*?)</script>', html, flags=re.DOTALL)
for i, block in enumerate(script_blocks):
    with open(f"/tmp/test_{i}.js", "w") as f:
        f.write(block)
    out = subprocess.getoutput(f"node -c /tmp/test_{i}.js")
    if "SyntaxError" in out or "Error" in out:
        print(f"BLOCK {i} ERROR:", out)
        
        # Print the exact location
        lines = block.split('\n')
        print("Surrounding lines:")
        for j, line in enumerate(lines):
            print(f"{j+1}: {line}")

