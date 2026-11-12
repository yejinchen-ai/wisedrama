import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The user wants the border around the main input area to be visible by default, not just on focus.
# Currently it is: `border-2 border-transparent focus-within:border-[#e5e7eb]`
# In the screenshot, it has a solid light gray border natively.

old_classes = r'class="input-box mb-10 relative border-2 border-transparent focus-within:border-\[\#e5e7eb\] focus-within:shadow-\[0_8px_30px_rgba\(0,0,0,0\.06\)\]"'
new_classes = 'class="input-box mb-10 relative border border-gray-200 focus-within:border-brand-500 focus-within:shadow-[0_8px_30px_rgba(21,209,114,0.15)] transition-all duration-300"'

html = re.sub(old_classes, new_classes, html)

with open(html_path, "w") as f:
    f.write(html)
