html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re

print("Looking for all unclosed divs or extra open tags...")

# The screenshot shows the sidebar is fine. The content of main is completely taken over by a video.
# BUT `finalVideoPlayer` has a wrapper `div id="finalVideoContainer" class="hidden mb-10 mt-6 bg-[#f9fafb]..."`
# If that container lost its `hidden` class incorrectly, it would show up.
# Wait! Look at the second screenshot! The video is NOT `finalVideoPlayer`.
# Notice there is NO "成片首映" header above the video. It's just a raw black video box.
# Let's check `floatVideoPlayer` - wait, I found `floatVideoPlayer` in the output of the first grep! 
# `<video id="floatVideoPlayer" class="w-full h-full object-cover scale-[1.02]" controls autoplay playsinline loop></video>`
# Where is `floatVideoPlayer` located in the file right now?

idx = html.find('floatVideoPlayer')
if idx != -1:
    print("Found floatVideoPlayer at", idx)
    print(html[idx-500:idx+200])

