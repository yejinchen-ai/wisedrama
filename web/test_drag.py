import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Make absolutely sure the slider is not wrapped in any flex or other container that might kill its pointer events or height.
# I will use a very basic block layout for the slider.
pattern = r'(<div class="col-span-2 md:col-span-1 flex items-center border border-gray-200 hover:border-gray-300 transition rounded-xl px-3 py-1\.5 bg-white w-full md:w-64 shadow-sm gap-2">)(.*?)(</div>\s*</div>)'
replacement = r'''\1
                            <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider shrink-0 hidden md:block">生成时长</span>
                            <div style="flex: 1; min-width: 0; padding: 4px 8px; position: relative; z-index: 50; display: block; overflow: visible;">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" oninput="updateDurationUI()" class="w-full cursor-pointer" style="accent-color: #FF5C5C; display: block; position: relative; pointer-events: auto; touch-action: pan-y;">
                            </div>
                            <span id="durationLabel" class="text-[12px] font-black text-brand-500 shrink-0 w-12 text-right">3 分钟</span>
                            <input type="hidden" id="shotsInput" value="30">
                        \3'''
html = re.sub(pattern, replacement, html, flags=re.DOTALL)


# For the textarea focus issue, let's explicitly add an onclick handler to the entire outer wrapper, AND use `cursor-text` class to guide the user visually.
box_pattern = r'<div class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-\[0_4px_20px_rgba\(255,42,42,0\.1\)\] transition-all duration-300 input-box"'
box_repl = '<div class="mb-10 relative bg-white border border-gray-200 rounded-none md:rounded-xl p-4 md:p-5 shadow-sm focus-within:border-brand-500 focus-within:shadow-[0_4px_20px_rgba(255,42,42,0.1)] transition-all duration-300 input-box" onclick="if(!event.target.closest(\'.interactive-zone\')) { document.getElementById(\'ideaInput\').focus(); }" style="cursor: text;"'
html = re.sub(box_pattern + r'[^>]*>', box_repl + '>', html)

# Then we ensure inner elements don't block it. We will wrap the text area in a very simple flex container.
textarea_pattern = r'<!-- Right: Textarea -->.*?</div>\s*</div>\s*<div class="h-px'
textarea_repl = '''<!-- Right: Textarea -->
                    <div class="flex-1 md:ml-2 order-1 md:order-2 w-full min-h-[140px]" style="display: flex; flex-direction: column;">
                        <textarea id="ideaInput" name="idea_content" autocomplete="off" data-lpignore="true" spellcheck="false" 
                            class="w-full h-full resize-none outline-none text-[16px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent py-2 m-0 border-0 focus:ring-0" 
                            style="flex-grow: 1; min-height: 140px; display: block; cursor: text;"
                            placeholder="描述您想要生成的视频内容，例如，“一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。”"></textarea>
                    </div>
                </div>
                
                <div class="h-px'''
html = re.sub(textarea_pattern, textarea_repl, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
