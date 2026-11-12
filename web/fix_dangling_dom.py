import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# We need to remove everything between `<div id="shotsContainer"...></div>` and `</main>` or `<script>`
# Let's find exactly what's there.
pattern = r'(<div id="shotsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 pb-20"></div>)[\s\S]*?(        </div>\n    </main>)'
match = re.search(pattern, html)
if match:
    html = html.replace(match.group(0), match.group(1) + "\n" + match.group(2))
    print("Dangling DOM removed successfully!")
else:
    print("Could not find the dangling DOM pattern.")

with open(html_path, "w") as f:
    f.write(html)
