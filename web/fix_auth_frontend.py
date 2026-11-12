import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix the missing headers in the register fetch call inside handleAuth
old_register_call = """                res = await fetch(`${API_BASE}/api/auth/register`, {
                    method: 'POST',
                    body: JSON.stringify({username: user, password: pass})
                });"""

new_register_call = """                res = await fetch(`${API_BASE}/api/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({username: user, password: pass})
                });"""

html = html.replace(old_register_call, new_register_call)

with open(html_path, "w") as f:
    f.write(html)
