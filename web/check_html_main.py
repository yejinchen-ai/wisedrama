html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import re

# Does `id="videoModal"` have `fixed`?
# In the file right now:
# <div id="videoModal" class="fixed z-[100] w-[320px] bg-white rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.15)] border border-gray-100 flex flex-col overflow-hidden transition-all duration-300 opacity-0 pointer-events-none" style="display: none; bottom: 30px; right: 30px; transform: translateY(20px);">
# This looks perfectly fine for a fixed popup.

# If the user says "showcase内容都没了" (Showcases are all gone), and the screenshot shows the sidebar is there but the whole main body is blank EXCEPT for the video player...
# Wait, look at the screenshot again carefully!
# The screenshot in the user's message shows:
# Sidebar is visible.
# Main content area has "每一个想法都是一部大片" and the input box.
# BUT below the input box... there are NO Banners, NO Tabs, and NO Showcases!
# Ahhhh! The JS `renderShowcases('推荐')` might be failing or the DOM might be broken, or I deleted the banners!

# Let's check what is in the HTML right after the input box.
idx_input = html.find('id="ideaInput"')
print(html[idx_input:idx_input+2000])

