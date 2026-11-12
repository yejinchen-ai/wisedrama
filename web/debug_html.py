html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The screenshot clearly shows the main area is just ONE HUGE VIDEO.
# Wait, look closely at the screenshot. The sidebar is intact. 
# Right next to the sidebar, taking up 100% width and height of the main content area, is a `<video>` tag.
# Is it `modalVideoPlayer` or `floatVideoPlayer` or `finalVideoPlayer`?
# Let's see what is inside the `<main>` tag right now.

import re
match = re.search(r'<main.*?</main>', html, flags=re.DOTALL)
if match:
    main_content = match.group(0)
    print("Video tags in <main>:")
    videos = re.findall(r'<video.*?>', main_content)
    for v in videos:
        print(v)
else:
    print("Could not find <main>")

