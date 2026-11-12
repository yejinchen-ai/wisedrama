import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's see if the layout has an error like an unclosed string or a JS syntax error preventing renderShowcases from running.
# The user's screenshot has NO showcases. This means JS crashed BEFORE running `renderShowcases('推荐');`
# Or there is a syntax error in the script block.

# Check JS syntax manually by running a quick node script.
import subprocess
js_content = re.search(r'<script>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
# Wait, there are multiple script tags. Let's extract the main one.
for match in re.finditer(r'<script>(.*?)</script>', html, re.DOTALL):
    if "API_BASE" in match.group(1):
        js = match.group(1)
        with open("/tmp/test.js", "w") as f:
            f.write(js)
        # Check syntax using node
        out = subprocess.getoutput("node -c /tmp/test.js")
        print("JS SYNTAX CHECK:", out)

