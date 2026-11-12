html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re

# Nuke everything between `<script>` and `<!-- Floating Card Player -->` except the actual closing tags for <main> or whatever.
# Wait, let's just use regex to remove `<!-- Drag Header (Overlay) -->` to `</div>\s*</div>\s*</div>`
html = re.sub(r'<!-- Drag Header \(Overlay\) -->.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
