import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    content = f.read()

# Make JS robust against missing IDs
content = content.replace("document.getElementById('emptyState').classList.add('hidden');", "if(document.getElementById('emptyState')) document.getElementById('emptyState').classList.add('hidden');")
content = content.replace("document.getElementById('modelIndicator').innerHTML", "if(document.getElementById('modelIndicator')) document.getElementById('modelIndicator').innerHTML")

with open(html_path, "w") as f:
    f.write(content)
