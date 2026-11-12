html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Force display: none inline to override any tailwind cascading conflicts
html = html.replace('id="videoModal" class="fixed inset-0 bg-black/95 z-[100] hidden flex-col', 'id="videoModal" class="fixed inset-0 bg-black/95 z-[100] flex-col" style="display: none;"')
html = html.replace("modal.classList.remove('hidden');", "modal.style.display = 'flex';")
html = html.replace("modal.classList.add('flex');", "")
html = html.replace("modal.classList.add('hidden');", "modal.style.display = 'none';")
html = html.replace("modal.classList.remove('flex');", "")

with open(html_path, "w") as f:
    f.write(html)
