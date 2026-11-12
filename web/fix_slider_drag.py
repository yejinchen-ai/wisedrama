import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The slider is `absolute w-full h-1.5` inside a `relative flex items-center flex-1 h-2 mx-1`
# If z-index or absolute positioning is messing up hit detection on some browsers, let's simplify it.
# Change to block-level relative.

old_slider_container = """<div class="relative flex items-center flex-1 h-2 mx-1">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" class="absolute w-full h-1.5 bg-gray-100 rounded-full appearance-none cursor-pointer z-20 outline-none" style="background: linear-gradient(to right, #15d172 10%, #f3f4f6 10%);" oninput="updateDurationUI()">
                            </div>"""

new_slider_container = """<div class="flex items-center flex-1 h-6 mx-1">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" class="w-full h-1.5 bg-gray-100 rounded-full appearance-none cursor-pointer outline-none relative z-10" style="background: linear-gradient(to right, #15d172 10%, #f3f4f6 10%);" oninput="updateDurationUI()">
                            </div>"""

html = html.replace(old_slider_container, new_slider_container)

with open(html_path, "w") as f:
    f.write(html)
