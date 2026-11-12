import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# We also need to define standard Mozilla slider thumb just in case
old_css = """/* Custom Slider Thumb */
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #ffffff;
            border: 2px solid #15d172;
            cursor: pointer;
            box-shadow: 0 0 5px rgba(21, 209, 114, 0.4);
            transition: transform 0.1s;
        }
        input[type=range]::-webkit-slider-thumb:hover {
            transform: scale(1.2);
        }"""

new_css = """/* Custom Slider Thumb */
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #ffffff;
            border: 3px solid #15d172;
            cursor: ew-resize;
            box-shadow: 0 0 6px rgba(21, 209, 114, 0.5);
            transition: transform 0.1s;
            position: relative;
            z-index: 30;
        }
        input[type=range]::-webkit-slider-thumb:hover {
            transform: scale(1.3);
        }
        
        input[type=range]::-moz-range-thumb {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #ffffff;
            border: 3px solid #15d172;
            cursor: ew-resize;
            box-shadow: 0 0 6px rgba(21, 209, 114, 0.5);
            transition: transform 0.1s;
        }
        input[type=range]::-moz-range-thumb:hover {
            transform: scale(1.3);
        }"""

html = html.replace(old_css, new_css)

# Update the calculation in updateDurationUI because slider thumb is now bigger, but JS math is fine.
# 10% is hardcoded for 3 out of 30, but logic uses percentage. That's fine.

with open(html_path, "w") as f:
    f.write(html)
