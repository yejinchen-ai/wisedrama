import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Update document title
html = html.replace('<title>WiseDrama - 创作短剧 (Hailuo Style)</title>', '<title>WiseDrama - 创作短剧</title>')

# Make sure there are no other accidental "Hailuo Style" texts visible
html = html.replace('Hailuo Style', '')

with open(html_path, "w") as f:
    f.write(html)
