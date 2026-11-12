import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The z-index of the modal might be intercepting clicks, or the pointer-events are messed up.
# Let's check pointer-events on the modal.
# The modal has `pointer-events-none` when hidden, but maybe it doesn't have `pointer-events-auto` on the child box?
# Wait! In `showAuthModal()`, I wrote:
# `modal.classList.remove('opacity-0', 'pointer-events-none');`
# This should make the modal clickable.
# Why can't you click "注册账号"? 
# Let's check the HTML for the buttons:
# `<button id="tabRegister" onclick="switchAuthTab('register')" class="flex-1 py-1.5 text-sm font-bold text-gray-500 hover:text-gray-700 rounded-lg transition">注册账号</button>`
# This looks perfectly fine.
# Is there an invisible overlay blocking it?
# Or maybe the JS `switchAuthTab` function is crashing or not defined properly?
# Let's check `switchAuthTab`.

# Ah, let's make sure the buttons have type="button" to prevent form submission if they are inside a form (they aren't, but good practice).
# Let's add pointer-events-auto just in case.
html = html.replace('onclick="switchAuthTab(\'login\')"', 'type="button" onclick="switchAuthTab(\'login\')"')
html = html.replace('onclick="switchAuthTab(\'register\')"', 'type="button" onclick="switchAuthTab(\'register\')"')

# Wait, maybe z-index is an issue?
# <div class="bg-white w-[90%] max-w-[400px] rounded-2xl shadow-2xl p-8 relative transform scale-95 transition-transform duration-300 pointer-events-auto" id="authBox">
html = html.replace('id="authBox"', 'id="authBox" style="pointer-events: auto;"')

# Let's also check the JS function.
# Maybe the function is missing in the DOM or something?
# I will inject a console log into `switchAuthTab` just to be sure.

with open(html_path, "w") as f:
    f.write(html)

