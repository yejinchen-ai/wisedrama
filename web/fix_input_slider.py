import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Make the textarea container clickable
# <label for="ideaInput" class="flex-1 md:ml-2 order-1 md:order-2 min-h-[120px] flex flex-col cursor-text">
html = html.replace('<label for="ideaInput" class="flex-1 md:ml-2 order-1 md:order-2 min-h-[120px] flex flex-col cursor-text">',
                    '<label for="ideaInput" class="flex-1 md:ml-2 order-1 md:order-2 min-h-[120px] flex flex-col cursor-text" onclick="document.getElementById(\'ideaInput\').focus();">')

# 2. Make the textarea fill its container
html = html.replace('<textarea id="ideaInput" class="w-full flex-1 resize-none',
                    '<textarea id="ideaInput" class="w-full h-full flex-1 resize-none')

# 3. Fix the slider drag issue
# The slider is in:
# <div class="col-span-2 md:col-span-1 flex items-center border border-gray-200 hover:border-gray-300 transition rounded-xl px-3 py-1.5 bg-white w-full md:w-64 shadow-sm gap-2 relative z-50 pointer-events-auto">
# Let's remove pointer-events-auto from the container because maybe it breaks the child slider in some browsers?
# Actually, let's wrap the slider in a clearer container and make sure z-index is correct.
html = html.replace('relative z-50 pointer-events-auto', 'relative z-[60]')
html = html.replace('style="width: 100%; cursor: pointer; accent-color: #FF5C5C;"', 'style="width: 100%; cursor: grab; accent-color: #FF5C5C; position: relative; z-index: 60;" onmousedown="this.style.cursor=\'grabbing\'" onmouseup="this.style.cursor=\'grab\'"')

with open(html_path, "w") as f:
    f.write(html)
