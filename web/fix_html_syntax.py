html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix the broken HTML attribute syntax caused by my previous replacement
html = html.replace('class="fixed inset-0 bg-black/95 z-[100] flex-col" style="display: none;" items-center justify-center opacity-0 transition-opacity duration-300"', 
                    'class="fixed inset-0 bg-black/95 z-[100] flex-col items-center justify-center opacity-0 transition-opacity duration-300" style="display: none;"')

with open(html_path, "w") as f:
    f.write(html)
