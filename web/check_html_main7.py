html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

import subprocess
with open("/tmp/test.html", "w") as f:
    f.write(html)

print("Checking diff...")
out = subprocess.getoutput("git -C /home/jerry/codebase/wisedrama diff HEAD web/index.html")
print(out)
