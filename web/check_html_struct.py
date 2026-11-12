html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# See where the "<!-- Floating Card Player -->" is.
idx = html.find('<!-- Floating Card Player -->')
print("Index of Floating Card:", idx)

idx_main_close = html.find('</main>')
print("Index of </main>:", idx_main_close)

idx_script_open = html.find('<script>')
print("Index of <script>:", idx_script_open)
