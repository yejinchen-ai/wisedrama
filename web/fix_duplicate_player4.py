html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "<!-- Floating Draggable Player -->" in line:
        skip = True
    if "<!-- Floating Card Player -->" in line:
        skip = False
    if "<!-- Drag Header (Overlay) -->" in line:
        skip = True
    # wait, there's no reliable way to parse HTML with lines if I don't know the exact structure.
    # Let's just find the floatVideoPlayer and trace back.
