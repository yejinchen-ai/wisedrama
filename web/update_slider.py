import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Look for the current duration block
old_duration_block_pattern = r'<div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white relative">.*?</div>\s*</div>\s*</div>'

# The new block will be just the slider, inline, without a popup.
new_duration_block = """<div class="flex flex-col border border-gray-200 rounded-xl px-4 py-2 bg-white w-full md:w-48 shadow-sm">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-[12px] font-bold text-gray-500"><i class="fa-regular fa-clock mr-1"></i> 短剧时长</span>
                                <span id="durationLabel" class="text-[13px] font-extrabold text-brand-500">3 分钟</span>
                            </div>
                            <input type="range" id="durationSlider" min="1" max="30" value="3" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500" oninput="updateDurationUI()">
                            <input type="hidden" id="shotsInput" value="30">
                        </div>"""

html = re.sub(old_duration_block_pattern, new_duration_block, html, flags=re.DOTALL)

# Update JS Logic for the slider
old_slider_js_pattern = r'let customShots = 150;.*?\}\);\s*// Auth Logic'

new_slider_js = """
        function updateDurationUI() {
            const slider = document.getElementById('durationSlider');
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
        
        // Initialize cost on load
        window.addEventListener('DOMContentLoaded', () => {
            updateDurationUI();
        });

        // Auth Logic"""

html = re.sub(old_slider_js_pattern, new_slider_js, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
