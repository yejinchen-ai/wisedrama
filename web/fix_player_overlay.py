import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Force display: none to completely hide it initially
html = html.replace('style="top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95);"', 'style="display: none; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95);"')

# Update JS to toggle display
open_func = "            playerBox.style.display = 'flex';\n            playerBox.classList.remove('opacity-0', 'pointer-events-none');"
html = html.replace("playerBox.classList.remove('opacity-0', 'pointer-events-none');", open_func)

close_func = """            setTimeout(() => {
                videoEl.pause();
                videoEl.src = '';
                playerBox.style.display = 'none';
            }, 300);"""
html = html.replace("""            setTimeout(() => {
                videoEl.pause();
                videoEl.src = '';
            }, 300);""", close_func)

with open(html_path, "w") as f:
    f.write(html)
