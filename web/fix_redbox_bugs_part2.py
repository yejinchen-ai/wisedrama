import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix double comment
html = html.replace('<!-- Right: Textarea -->\n                    <!-- Right: Textarea -->', '<!-- Right: Textarea -->')

# Make the slider fully native to fix drag on all browsers
html = html.replace('class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"', 
                    'class="w-full cursor-pointer"')

# We also make sure the `w-full h-full min-h-[120px]` container doesn't have a stray `relative z-20` that might conflict with the `z-30` inside, though `z-index` shouldn't break drag unless it covers something else.
# But just to be safe:
html = html.replace('class="flex-1 md:ml-2 order-1 md:order-2 flex flex-col w-full h-full min-h-[120px] relative z-20"',
                    'class="flex-1 md:ml-2 order-1 md:order-2 flex flex-col w-full h-full min-h-[120px]"')

html = html.replace('class="w-full h-full min-h-[140px] resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0 block relative z-30"',
                    'class="w-full h-full min-h-[140px] resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0 block"')

with open(html_path, "w") as f:
    f.write(html)
