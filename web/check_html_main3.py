import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's see if the BANNERS exist in the file.
print("Banners:", "Horizontal Banners" in html)

# Let's see if the TABS exist in the file.
print("Tabs:", "Gallery Category Tabs" in html)

# If they don't exist, I accidentally deleted them in my `fix_clean_rebuild2.py` or earlier when I reverted to 8f7f977 and then reapplied things.
# I reverted to 8f7f977! Did 8f7f977 HAVE the tabs?
# The tabs were added in commit `941ce1e` "feat: implement dynamic showcase tabs...".
# The player fixes were after that.
# Let's check git log.
import subprocess
print(subprocess.getoutput("git -C /home/jerry/codebase/wisedrama log --oneline | head -n 10"))

