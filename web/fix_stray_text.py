import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I see a random piece of HTML text left over:
# `            <!-- Video Container: Vertical aspect ratio 9:16 -->`
# This text is just floating in the DOM between `</script>` and the modal, but it isn't wrapped in a hidden div, and maybe there's an unclosed tag.
# Wait, look at the end:
# `</script>`
# `            <!-- Video Container: Vertical aspect ratio 9:16 -->`
# `    <!-- Floating Card Player -->`
# `    <div id="videoModal"`

# Let's clean everything between `</script>` and `<!-- Floating Card Player -->`
clean_html = re.sub(r'</script>.*?<!-- Floating Card Player -->', '</script>\n\n    <!-- Floating Card Player -->', html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(clean_html)
