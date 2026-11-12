import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Is there an invisible pseudo element from the input box transition?
# "mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-[0_4px_20px_rgba(21,209,114,0.1)] transition-all duration-300"
# This looks fine.

# What about the script section?
# "function updateDurationUI()"
# Does it have any errors that freeze the UI?
