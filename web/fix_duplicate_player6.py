import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's cleanly remove from `</script>` down to `<!-- Floating Card Player -->`
pattern = r'(</script>).*?(<!-- Floating Card Player -->)'
html = re.sub(pattern, r'\1\n\2', html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
