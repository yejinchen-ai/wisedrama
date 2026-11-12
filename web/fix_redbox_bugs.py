import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Redo the textarea to completely kill autofill and ensure it fills the space naturally.
# We will give it a completely random name or no name, remove spellcheck, add a wrapping label that acts as a full-height block but no `for` attribute.
old_textarea_section = """
                    <!-- Right: Textarea -->
                    <div class="flex-1 md:ml-2 order-1 md:order-2 flex flex-col w-full h-full min-h-[120px]">
                        <textarea id="ideaInput" name="prompt" autocomplete="off" data-lpignore="true" autocorrect="off" spellcheck="false" 
                            class="w-full h-full flex-1 resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0 block" 
                            placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”"></textarea>
                    </div>
"""

new_textarea_section = """
                    <!-- Right: Textarea -->
                    <div class="flex-1 md:ml-2 order-1 md:order-2 flex flex-col w-full h-full min-h-[120px] relative z-20">
                        <textarea id="ideaInput" autocomplete="new-password" autocorrect="off" autocapitalize="off" spellcheck="false" 
                            class="w-full h-full min-h-[140px] resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0 block relative z-30" 
                            placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”" style="min-height: 140px;"></textarea>
                    </div>
"""
if old_textarea_section.strip() in html:
    html = html.replace(old_textarea_section.strip(), new_textarea_section.strip())
else:
    # Fallback regex
    html = re.sub(r'<!-- Right: Textarea -->.*?</div>\s*</div>', new_textarea_section.strip() + '\n                </div>', html, flags=re.DOTALL)

# 2. Fix the slider completely.
# Remove ALL relative z-index absolute positioning hacks from the slider. They are probably breaking mobile/safari drag.
# Native range inputs work best when they are just normal blocks.
slider_container_old = """
                        <div class="col-span-2 md:col-span-1 flex items-center border border-gray-200 hover:border-gray-300 transition rounded-xl px-3 py-1.5 bg-white w-full md:w-64 shadow-sm gap-2 relative z-[60]">
                            <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider shrink-0 hidden md:block">生成时长</span>
                            <div class="flex-1 px-2 flex items-center relative z-20">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" oninput="updateDurationUI()" class="w-full cursor-pointer block" style="accent-color: #FF5C5C;">
                            </div>
                            <span id="durationLabel" class="text-[12px] font-black text-brand-500 shrink-0 w-12 text-right">3 分钟</span>
                            <input type="hidden" id="shotsInput" value="30">
                        </div>
"""
slider_container_new = """
                        <div class="col-span-2 md:col-span-1 flex items-center border border-gray-200 hover:border-gray-300 transition rounded-xl px-3 py-1.5 bg-white w-full md:w-64 shadow-sm gap-2">
                            <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider shrink-0 hidden md:block">生成时长</span>
                            <div class="flex-1 px-2 flex items-center h-full w-full">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" oninput="updateDurationUI()" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" style="accent-color: #FF5C5C;">
                            </div>
                            <span id="durationLabel" class="text-[12px] font-black text-brand-500 shrink-0 w-12 text-right">3 分钟</span>
                            <input type="hidden" id="shotsInput" value="30">
                        </div>
"""
if slider_container_old.strip() in html:
    html = html.replace(slider_container_old.strip(), slider_container_new.strip())
else:
    # Just regex replace the range input
    html = re.sub(r'<input type="range" id="durationSlider"[^>]*>', 
                  '<input type="range" id="durationSlider" min="1" max="30" value="3" oninput="updateDurationUI()" class="w-full h-2 bg-gray-200 rounded-lg cursor-pointer" style="accent-color: #FF5C5C; pointer-events: auto;">', html)
    # And strip z-indexes from its parents
    html = re.sub(r' relative z-\[60\]', '', html)
    html = re.sub(r' relative z-20', '', html)

with open(html_path, "w") as f:
    f.write(html)
