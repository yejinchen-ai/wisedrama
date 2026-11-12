import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's cleanly find the floatingPlayer element manually and delete it.
start_str = '<!-- Floating Draggable Player -->'
if start_str in html:
    start_idx = html.find(start_str)
    # the end of the floating player is before '<!-- Floating Card Player -->'
    end_str = '<!-- Floating Card Player -->'
    if end_str in html:
        end_idx = html.find(end_str)
        html = html[:start_idx] + html[end_idx:]
    else:
        # just nuke from start to </body>
        end_idx = html.find('</body>', start_idx)
        html = html[:start_idx] + "\n" + html[end_idx:]

with open(html_path, "w") as f:
    f.write(html)
