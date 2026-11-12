html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's inspect where `id="videoModal"` was injected the very first time.
# Look for anything between `</script>` and `<!-- Floating Card Player -->`
import re
match = re.search(r'</script>([\s\S]*?)<!-- Floating Card Player -->', html)
if match:
    print("=== GAP ===")
    print(match.group(1))

