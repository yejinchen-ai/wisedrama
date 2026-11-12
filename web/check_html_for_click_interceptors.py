html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's see if the main white box STILL has `onclick="..."` 
import re
match = re.search(r'class="mb-10 relative bg-white border border-gray-200.*?>', html)
if match:
    print("Main Input Wrapper:", match.group(0))

