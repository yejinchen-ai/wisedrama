import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Replace the HTML block
old_html_block = r'<div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white relative">.*?</div>\s*</div>\s*</div>'
new_html_block = """<div class="flex flex-col border border-gray-200 rounded-xl px-4 py-2 bg-white w-full md:w-48 shadow-sm shrink-0">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-[12px] font-bold text-gray-500"><i class="fa-regular fa-clock mr-1"></i> 短剧时长</span>
                                <span id="durationLabel" class="text-[13px] font-extrabold text-brand-500">3 分钟</span>
                            </div>
                            <input type="range" id="durationSlider" min="1" max="30" value="3" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500" oninput="updateDurationUI()">
                            <input type="hidden" id="shotsInput" value="30">
                        </div>"""

html = re.sub(old_html_block, new_html_block, html, flags=re.DOTALL)

# Replace the JS block
old_js = r'let customShots = 150;[\s\S]*?// Hide popup when clicking outside[\s\S]*?\}\);\s*'
new_js = """
        function updateDurationUI() {
            const slider = document.getElementById('durationSlider');
            if(!slider) return;
            const val = parseInt(slider.value);
            document.getElementById('durationLabel').innerText = `${val} 分钟`;
            
            // 1 minute roughly equals 10 shots
            const shots = val * 10;
            document.getElementById('shotsInput').value = shots;
            
            // Update cost: 1 shot = 15 tokens
            const cost = shots * 15;
            const costEl = document.querySelector('.fa-brands.fa-product-hunt.text-black').nextSibling;
            if(costEl) {
                costEl.textContent = ` ${cost}`;
            }
        }
        
        window.addEventListener('DOMContentLoaded', () => {
            updateDurationUI();
        });
        
"""

html = re.sub(old_js, new_js, html)

# Fix startGeneration shots fetch
html = html.replace("const shotsSelect = document.getElementById('shotsInput').value;\n            const shots = shotsSelect === 'custom' ? customShots : shotsSelect;", "const shots = document.getElementById('shotsInput').value;")

with open(html_path, "w") as f:
    f.write(html)
