html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re
import subprocess

for match in re.finditer(r'<script>(.*?)</script>', html, re.DOTALL):
    if "API_BASE" in match.group(1):
        js = match.group(1)
        with open("/tmp/test.js", "w") as f:
            f.write(js)
        # Check syntax using node
        out = subprocess.getoutput("node -c /tmp/test.js")
        print("JS SYNTAX CHECK:", out)
