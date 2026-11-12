html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re
import subprocess

with open("/tmp/test.js", "w") as f:
    f.write("")

script_blocks = re.findall(r'<script>(.*?)</script>', html, flags=re.DOTALL)
for i, block in enumerate(script_blocks):
    with open(f"/tmp/test_{i}.js", "w") as f:
        f.write(block)
    out = subprocess.getoutput(f"node -c /tmp/test_{i}.js")
    if "SyntaxError" in out or "Error" in out:
        print(f"BLOCK {i} ERROR:", out)
    else:
        print(f"BLOCK {i} OK!")

