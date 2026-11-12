import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Wait, `onclick="document.getElementById('ideaInput').focus()"` on the MAIN wrapper means it intercepts ALL clicks inside it!
# If you click the SLIDER, the click event bubbles up to the wrapper, which immediately calls `.focus()` on the textarea, 
# stealing the focus away from the slider and thus canceling the drag action instantly!
# OH MY GOD! That's exactly why the slider is completely frozen! Every time you try to click/drag the slider, you are actually focusing the text area!

# Let's remove the `onclick` from the main wrapper!
old_wrapper = r'class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-\[0_4px_20px_rgba\(21,209,114,0\.1\)\] transition-all duration-300 cursor-text" onclick="document\.getElementById\(\'ideaInput\'\)\.focus\(\)"'
new_wrapper = 'class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-[0_4px_20px_rgba(21,209,114,0.1)] transition-all duration-300"'
html = re.sub(old_wrapper, new_wrapper, html)

# To fix the textarea not focusing when clicking the blank area, we should just use `<label>` or make the flex container of the textarea expand fully.
# The textarea is: `<div class="flex-1 md:ml-2 order-1 md:order-2 min-h-[120px] flex flex-col relative z-20 pointer-events-auto">`
# Let's wrap the textarea in a label that takes full width and height.
old_textarea = r'<div class="flex-1 md:ml-2 order-1 md:order-2 min-h-\[120px\] flex flex-col relative z-20 pointer-events-auto">\s*<textarea id="ideaInput" class="w-full flex-1 resize-none outline-none text-\[16px\] leading-relaxed placeholder-\[\#9ca3af\] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0" placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”"></textarea>\s*</div>'
new_textarea = """<label for="ideaInput" class="flex-1 md:ml-2 order-1 md:order-2 min-h-[120px] flex flex-col relative z-20 cursor-text">
                        <textarea id="ideaInput" class="w-full flex-1 resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0" placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”"></textarea>
                    </label>"""
html = re.sub(old_textarea, new_textarea, html)

with open(html_path, "w") as f:
    f.write(html)
