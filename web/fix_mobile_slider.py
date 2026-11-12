import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Looking at the mobile screenshot:
# The `1080p` box is next to the `Hailuo 2.3-Fast` box.
# But right next to `1080p` is a tiny, weird grey circle thing cutting off. That is the duration slider!
# Because of `flex items-center justify-between md:justify-start gap-2 md:gap-2.5 w-full md:w-auto`
# on mobile, they try to fit in one row but there is not enough space.
# We need the slider to wrap to its own row on mobile, or span full width.
# In `index.html`:
# <div class="flex items-center justify-between md:justify-start gap-2 md:gap-2.5 w-full md:w-auto">
#    <div class="model...">
#    <div class="resolution...">
#    <div class="slider...">

old_toolbar = r"""<!-- Bottom Toolbar -->
                <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 md:gap-0">
                    <!-- Left Selectors -->
                    <div class="flex items-center justify-between md:justify-start gap-2 md:gap-2.5 w-full md:w-auto">"""

new_toolbar = """<!-- Bottom Toolbar -->
                <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 md:gap-0">
                    <!-- Left Selectors -->
                    <div class="flex flex-wrap md:flex-nowrap items-center justify-start gap-2 md:gap-2.5 w-full md:w-auto">"""

html = html.replace(old_toolbar, new_toolbar)

# Also let's make the slider take full width on mobile if it wraps.
# The slider div currently is:
# class="flex items-center border border-gray-200 hover:border-gray-300 transition rounded-xl px-3 py-1.5 bg-white w-full md:w-64 shadow-sm gap-2 relative z-50 pointer-events-auto"
# If `w-full` is there, in flex-wrap it will wrap and take full width.

with open(html_path, "w") as f:
    f.write(html)
