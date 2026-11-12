import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Replace border-gray-200 with border-dashed and standard color
old_class = r"\.frame-upload \{ @apply w-24 h-\[104px\] bg-\[\#f8f9fa\] border border-gray-200 rounded-2xl flex flex-col items-center justify-center text-gray-400 cursor-pointer hover:bg-gray-100 transition relative overflow-hidden; \}"
new_class = r".frame-upload { @apply w-24 h-[104px] bg-[#fafafa] border-[1.5px] border-dashed border-gray-300 rounded-2xl flex flex-col items-center justify-center text-gray-400 cursor-pointer hover:bg-gray-50 hover:border-[#15d172] transition-colors relative overflow-hidden; }"

html = re.sub(old_class, new_class, html)

with open(html_path, "w") as f:
    f.write(html)
