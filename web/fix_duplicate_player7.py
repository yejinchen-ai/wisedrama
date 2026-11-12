import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I want to delete the chunk that has `<video id="floatVideoPlayer"`
# It's lingering because of previous bad regex.
# Let's find exactly the `<div class="relative w-full aspect-video bg-transparent flex items-center justify-center overflow-hidden">` all the way to its `</div></div></div>`
pattern = r'<div class="relative w-full aspect-video bg-transparent flex items-center justify-center overflow-hidden">[\s\S]*?<video id="floatVideoPlayer"[\s\S]*?</div>\s*</div>\s*</div>'
html = re.sub(pattern, '', html)

# And remove any random extra closing `</div>` that might be dangling
html = html.replace('\n    \n    </div>\n', '\n')

with open(html_path, "w") as f:
    f.write(html)

