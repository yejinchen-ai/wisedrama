import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Update Tailwind Config colors
html = html.replace("'#7c3aed'", "'#15d172'") # brand-500 (Vibrant Green)
html = html.replace("'#6d28d9'", "'#10b260'") # brand-600 (Darker Green)

# Update hardcoded styles in CSS block and inline
html = html.replace("#7c3aed", "#15d172")
html = html.replace("#f5f3ff", "#eafff2") # Very light green background

# Update Slogan text gradient
html = html.replace("from-[#7143ff]", "from-[#10b260]")
html = html.replace("to-[#a855f7]", "to-[#15d172]")

# Update Tag colors (e.g. 科幻)
html = html.replace("bg-[#f3e8ff]", "bg-[#eafff2]")
html = html.replace("text-[#9333ea]", "text-[#10b260]")
html = html.replace("border-[#e9d5ff]", "border-[#bbf7d0]")

# Update Sidebar Logo Gradient
html = html.replace("from-[#FF4D4D] via-[#a855f7] to-[#3b82f6]", "from-[#15d172] via-[#059669] to-[#0ea5e9]")

with open(html_path, "w") as f:
    f.write(html)
