import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# If both the slider AND the textarea above it are completely unclickable, there is 100% an invisible div overlapping the ENTIRE input box.
# What could overlap the entire input box?
# Let's check the structure:
# `<div class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-[0_4px_20px_rgba(21,209,114,0.1)] transition-all duration-300">`
# Inside it:
# `<div class="flex flex-col md:flex-row gap-4 mb-4 min-h-[100px] md:min-h-[140px]">`
# `<div class="h-px bg-gray-100 w-full mb-4"></div>`
# `<div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 md:gap-0">` (Bottom Toolbar)

# Let's check if there's any absolute div inside the input box wrapper that covers it.
match = re.search(r'<div class="mb-10 relative bg-white.*?>(.*?)<!-- Horizontal Banners -->', html, flags=re.DOTALL)
if match:
    print(match.group(1))

