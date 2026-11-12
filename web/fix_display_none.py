html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Make sure openVideo enables display:flex
old_open = "playerBox.classList.remove('opacity-0', 'pointer-events-none');"
new_open = "playerBox.style.display = 'flex';\n            playerBox.classList.remove('opacity-0', 'pointer-events-none');"
if "playerBox.style.display = 'flex';" not in html:
    html = html.replace(old_open, new_open)

# Make sure closeFloatVideo disables display
old_close = """            setTimeout(() => {
                videoEl.pause();
                videoEl.src = '';
            }, 300);"""
new_close = """            setTimeout(() => {
                videoEl.pause();
                videoEl.src = '';
                playerBox.style.display = 'none';
            }, 300);"""
if "playerBox.style.display = 'none';" not in html:
    html = html.replace(old_close, new_close)

with open(html_path, "w") as f:
    f.write(html)
