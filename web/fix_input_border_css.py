import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Since I changed the class inline, let's also remove the conflicting CSS from the style block.
html = re.sub(r'\.input-box \{.*?\}', '', html)
html = re.sub(r'\.input-box:focus-within \{.*?\}', '', html)

# Instead of relying on CSS block for input-box, just use tailwind classes directly.
new_classes = 'class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-[0_4px_20px_rgba(21,209,114,0.1)] transition-all duration-300"'
html = html.replace('class="input-box mb-10 relative border border-gray-200 focus-within:border-brand-500 focus-within:shadow-[0_8px_30px_rgba(21,209,114,0.15)] transition-all duration-300"', new_classes)

with open(html_path, "w") as f:
    f.write(html)
