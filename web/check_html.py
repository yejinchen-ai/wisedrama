html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I want to check if there are dangling open tags.
# Is the `main` tag closed?
print("</main>" in html)
# Is `videoModal` placed AFTER `</main>`?
if "</main>" in html:
    idx_main = html.find("</main>")
    idx_modal = html.find('id="videoModal"')
    print("modal after main?", idx_modal > idx_main)

