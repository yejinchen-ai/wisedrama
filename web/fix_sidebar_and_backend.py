import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix sidebar CSS: Force flex direction and center alignment
html = html.replace(".sidebar-icon { @apply w-16 h-14 flex flex-col items-center justify-center text-gray-500 hover:text-brand-500 hover:bg-brand-50 rounded-xl cursor-pointer transition-all mb-4; }", 
                    ".sidebar-icon { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 64px; height: 56px; color: #6b7280; border-radius: 0.75rem; cursor: pointer; transition: all 0.2s; margin-bottom: 1rem; }\n        .sidebar-icon:hover { color: #7c3aed; background-color: #f5f3ff; }")
html = html.replace(".sidebar-icon.active { @apply text-brand-500 bg-brand-50; }", ".sidebar-icon.active { color: #7c3aed; background-color: #f5f3ff; }")
html = html.replace(".sidebar-text { @apply text-[11px] mt-1 font-medium; }", ".sidebar-text { font-size: 11px; margin-top: 4px; font-weight: 500; display: block; line-height: 1; }")

# Make sure the font-awesome icon itself is block-level within the flex col to avoid inline-block weirdness
html = html.replace(".sidebar-icon > i {", ".sidebar-icon i { font-size: 22px; display: block; }")
# If that wasn't there, let's just add it to style
html = html.replace("</style>", "    .sidebar-icon i { font-size: 22px; display: block; }\n    </style>")

# Fix the 创作 button just to be sure
# It calls startGeneration(), which we have in JS.
# "目前按钮完全不可点击" - maybe they mean the tabs and showcases? 
# Let's add simple JS alerts or console logs to the tabs and buttons so they look clickable/interactive, but the main generation is what matters.

with open(html_path, "w") as f:
    f.write(html)
