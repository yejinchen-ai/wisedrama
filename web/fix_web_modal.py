import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# In the mobile optimization, I changed the large modal to:
# `<div class="flex flex-col md:flex-row w-full h-full p-0 md:p-10 gap-0 md:gap-10 relative">`
# And the left video container to:
# `class="w-full h-[40vh] md:flex-1 flex flex-col justify-center items-center relative md:h-full bg-black shrink-0"`
# Wait, if md:flex-1 is applied, it should take up the remaining space on desktop.
# BUT I also added `bg-black shrink-0`. In flex row, if it's flex-1 it should fill the left side.
# Let's see the screenshot: The video player on the left is a massive tall black rectangle, taking up the whole height and a lot of width, pushing the right side.
# Actually, the user's screenshot shows the black area has NO padding on top/bottom, it touches the edges of the modal.
# Wait, look at the original code before mobile optimization for the modal:
# `<div class="flex w-full h-full p-10 gap-10">`
# `<div class="flex-1 flex flex-col justify-center items-center relative h-full">`
# `<div class="w-full max-w-[1000px] aspect-video bg-black rounded-3xl overflow-hidden relative shadow-...">`
# Ah! In the mobile optimization script, I did:
# `html = html.replace('class="flex-1 flex flex-col justify-center items-center relative h-full"', 'class="w-full h-[40vh] md:flex-1 flex flex-col justify-center items-center relative md:h-full bg-black shrink-0"')`
# Wait, I accidentally replaced the WRONG div, or I added `bg-black` to the WRONG container!
# In the original, the `flex-1` div was a TRANSPARENT flex container. Inside it was a `max-w-[1000px] aspect-video bg-black` container.
# By making the `flex-1` container `bg-black`, I made the entire left side of the screen a black block instead of just the 16:9 video player!

old_str = 'class="w-full h-[40vh] md:flex-1 flex flex-col justify-center items-center relative md:h-full bg-black shrink-0"'
new_str = 'class="w-full h-[40vh] md:flex-1 flex flex-col justify-center items-center relative md:h-full shrink-0"'
html = html.replace(old_str, new_str)

# Also check if I messed up the inner video container:
# In mobile script I did: `html = html.replace('rounded-3xl', 'rounded-none md:rounded-3xl')` which is fine.

# Wait, is the video player size too big or too small? The user says "视频播放器大小。修复调整优化".
# Looking at the screenshot, the black box is huge. Removing `bg-black` from the wrapper will make the background white again, leaving only the `aspect-video` inner box black.
# Wait, the inner box has `w-full max-w-[1000px] aspect-video bg-black`.
# So the video will be 16:9 and centered vertically, which is exactly what we want.

# Wait, I should also make sure the mobile layout still works.
# For mobile, the wrapper is `h-[40vh]`. The inner box is `w-full max-w-[1000px] aspect-video bg-black`.
# Since the wrapper is h-[40vh], and inner is w-full aspect-video, on mobile the inner might be taller than 40vh or shorter.
# Actually, the inner box in mobile should just be w-full and h-full bg-black.
# Let's fix the inner box classes.
# Original inner: `<div class="w-full max-w-[1000px] aspect-video bg-black rounded-none md:rounded-3xl overflow-hidden relative shadow-[0_20px_60px_rgba(0,0,0,0.15)] ring-1 ring-black/5" style="box-shadow: 0 0 40px rgba(0,0,0,0.1), inset 0 0 0 1px rgba(255,255,255,0.1);">`

# For mobile, it should be h-full w-full, but on desktop aspect-video max-w-[1000px].
inner_old = 'class="w-full max-w-[1000px] aspect-video bg-black rounded-none md:rounded-3xl overflow-hidden relative shadow-[0_20px_60px_rgba(0,0,0,0.15)] ring-1 ring-black/5"'
inner_new = 'class="w-full h-full md:h-auto md:max-w-[1000px] md:aspect-video bg-black rounded-none md:rounded-3xl overflow-hidden relative shadow-none md:shadow-[0_20px_60px_rgba(0,0,0,0.15)] md:ring-1 md:ring-black/5"'
html = html.replace(inner_old, inner_new)

with open(html_path, "w") as f:
    f.write(html)

