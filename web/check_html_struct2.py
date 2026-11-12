html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's find all script tags
import re
scripts = [(m.start(), m.group()) for m in re.finditer(r'<script.*?>', html)]
print("Scripts:", scripts)

