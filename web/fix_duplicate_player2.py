import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I see both floatVideoPlayer AND videoModal.
# Ah, earlier I nuked `id="videoModal"` but the PREVIOUS player was `id="floatingPlayer"`!
# So `floatingPlayer` is STILL THERE and taking up space or causing styling issues.

old_floating = r'<!-- Floating Draggable Player -->.*?</div>\s*</div>\s*</div>'
html = re.sub(old_floating, '', html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)

