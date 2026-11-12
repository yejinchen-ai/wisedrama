import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Simplify the slider to match the single-line format
old_slider = r'<div class="flex flex-col border border-gray-200 hover:border-gray-300 transition rounded-xl px-4 py-2\.5 bg-white w-full md:w-56 shadow-\[0_2px_10px_rgba\(0,0,0,0\.02\)\] group">.*?<input type="hidden" id="shotsInput" value="30">\s*</div>'

new_slider = """<div class="flex items-center border border-gray-200 hover:border-gray-300 transition rounded-xl px-3 py-1.5 bg-white w-full md:w-64 shadow-sm gap-3 group">
                            <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider shrink-0 hidden md:block">生成时长</span>
                            <div class="relative flex items-center flex-1 h-2 mx-1">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" class="absolute w-full h-1.5 bg-gray-100 rounded-full appearance-none cursor-pointer z-20 outline-none" style="background: linear-gradient(to right, #15d172 10%, #f3f4f6 10%);" oninput="updateDurationUI()">
                            </div>
                            <span id="durationLabel" class="text-[12px] font-black text-brand-500 shrink-0 w-12 text-right">3 分钟</span>
                            <input type="hidden" id="shotsInput" value="30">
                        </div>"""
html = re.sub(old_slider, new_slider, html, flags=re.DOTALL)

# 2. Add text to the token cost
old_cost = r'<div class="text-\[14px\] font-bold text-gray-800 flex items-center gap-1\.5">\s*<i class="fa-brands fa-product-hunt text-black"></i> 15\s*</div>'
new_cost = """<div class="text-[13px] font-bold text-gray-800 flex items-center gap-1.5 whitespace-nowrap">
                            <span class="text-[11px] text-gray-400 font-normal mr-1">预估消耗</span>
                            <i class="fa-brands fa-product-hunt text-black"></i> <span id="tokenCostDisplay">450</span>
                        </div>"""
html = re.sub(old_cost, new_cost, html, flags=re.DOTALL)

# 3. Update the JS to target the new tokenCostDisplay ID
old_update_js = r'const costEl = document\.querySelector\(\'\.fa-brands\.fa-product-hunt\.text-black\'\)\.nextSibling;\s*if\(costEl\) \{\s*costEl\.textContent = ` \$\{cost\}`;\s*\}'
new_update_js = """const costEl = document.getElementById('tokenCostDisplay');
            if(costEl) {
                costEl.innerText = cost;
            }"""
html = re.sub(old_update_js, new_update_js, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
