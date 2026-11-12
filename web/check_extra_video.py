html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re
matches = re.findall(r'<video[^>]*>', html)
for m in matches:
    print(m)

