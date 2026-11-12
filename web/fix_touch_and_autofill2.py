import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I will try to structure the textarea area using a label for native behavior, but ensure no conflicting HTML structure.
# Also use absolute positioning to cover the empty areas to capture clicks natively without JS.
textarea_pattern = r'<!-- Right: Textarea -->\s*<div class="flex-1 md:ml-2 order-1 md:order-2 w-full min-h-\[140px\]" style="display: flex; flex-direction: column;">\s*<textarea id="ideaInput" name="idea_content" autocomplete="off" data-lpignore="true" spellcheck="false" \s*class="w-full h-full resize-none outline-none text-\[16px\] leading-relaxed placeholder-\[#9ca3af\] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0" \s*style="flex-grow: 1; min-height: 140px; display: block; cursor: text;"\s*placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”"></textarea>\s*</div>'

textarea_new = """<!-- Right: Textarea -->
                    <label class="flex-1 md:ml-2 order-1 md:order-2 w-full flex flex-col cursor-text relative">
                        <textarea id="ideaInput" spellcheck="false" 
                            class="w-full flex-1 resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0 block min-h-[140px]" 
                            placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”"></textarea>
                    </label>"""
html = re.sub(textarea_pattern, textarea_new, html, flags=re.DOTALL)

# For the slider, let's just make it a completely standard setup.
slider_pattern = r'<div class="flex-1 px-2 w-full">\s*<input type="range" id="durationSlider"[^>]*>\s*</div>'
slider_new = '''<div class="flex-1 px-2">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" oninput="updateDurationUI()" class="w-full h-2 rounded-lg cursor-pointer" style="accent-color: #FF5C5C;">
                            </div>'''
html = re.sub(slider_pattern, slider_new, html, flags=re.DOTALL)

# Let's remove ANY interactive-zone / onclick event delegation hacks on the input-box container.
box_pattern = r'<div class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-\[0_4px_20px_rgba\(255,42,42,0\.1\)\] transition-all duration-300 input-box"[^>]*>'
box_new = '<div class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-[0_4px_20px_rgba(255,42,42,0.1)] transition-all duration-300 input-box">'
html = re.sub(box_pattern, box_new, html)

with open(html_path, "w") as f:
    f.write(html)
