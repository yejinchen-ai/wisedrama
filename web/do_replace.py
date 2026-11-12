import sys
HTML_FILE = '/home/jerry/codebase/wisedrama/web/index.html'
NEW_FILE = '/home/jerry/codebase/wisedrama/web/new_section.html'
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    content = f.read()
sm = '            <!-- Main Input Area -->'
em = '\n\n            <!-- Horizontal Banners -->'
si = content.find(sm)
ei = content.find(em)
if si < 0 or ei < 0:
    print(f"ERROR: markers not found (start={si}, end={ei})")
    sys.exit(1)
with open(NEW_FILE, 'r', encoding='utf-8') as f:
    ns = f.read()
result = content[:si] + ns + content[ei:]
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(result)
print(f"OK replaced {ei-si} chars with {len(ns)} chars")
