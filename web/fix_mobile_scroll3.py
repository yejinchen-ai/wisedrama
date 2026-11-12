import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The combination of `h-[100dvh]` and `overflow-hidden` on body, plus `flex-1 h-full overflow-y-auto` on main
# SHOULD work perfectly. BUT on iOS Safari / WeChat browser, `-webkit-overflow-scrolling: touch` might be missing,
# OR the flex column structure is overflowing.
# Actually, the safest way to build responsive scrolling on mobile is NOT to restrict the body.
# Let's remove `h-[100dvh] overflow-hidden` from body and let the body scroll naturally on mobile, 
# while keeping it fixed on desktop if needed (or just let body scroll everywhere).

old_body = '<body class="flex flex-col md:flex-row h-[100dvh] overflow-hidden text-gray-800">'
new_body = '<body class="flex flex-col md:flex-row min-h-screen text-gray-800 bg-white">'
html = html.replace(old_body, new_body)

# Since body scrolls now, we don't need `<main>` to be `h-full overflow-y-auto`.
# We want `<main>` to just expand.
old_main = '<main class="flex-1 h-full overflow-y-auto bg-white relative">'
new_main = '<main class="flex-1 w-full bg-white relative pb-10">'
html = html.replace(old_main, new_main)

# And for the sidebar on desktop, if it should stick, we should make it `sticky top-0 h-screen`.
old_aside = '<aside class="hidden md:flex w-[96px] bg-white border-r border-gray-100 flex flex-col items-center py-6 h-full shrink-0 z-10 flex-shrink-0 flex-grow-0">'
new_aside = '<aside class="hidden md:flex w-[96px] bg-white border-r border-gray-100 flex-col items-center py-6 h-screen sticky top-0 shrink-0 z-10">'
html = html.replace(old_aside, new_aside)

with open(html_path, "w") as f:
    f.write(html)
