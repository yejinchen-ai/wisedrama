import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The issue with mobile scrolling is usually caused by:
# <body class="flex h-screen overflow-hidden text-gray-800">
# Wait, I previously changed it to `flex flex-col md:flex-row h-[100dvh]`
# But if there's an `overflow-hidden` on body, the main content MUST be properly scrollable.
# Let's check body class.
# In my `mobile_optimize.py` I did:
# html = html.replace('body class="flex h-screen', 'body class="flex flex-col md:flex-row h-[100dvh]')
# Let's see what body looks like now.
match = re.search(r'<body.*?>', html)
if match:
    print(match.group(0))

