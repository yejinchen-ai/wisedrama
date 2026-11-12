import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# If `overflow-hidden` is on the body, then `<main>` must handle the scrolling.
# Let's check what `<main>` looks like.
match_main = re.search(r'<main.*?>', html)
if match_main:
    print(match_main.group(0))

