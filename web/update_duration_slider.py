import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Currently the UI has this block for duration:
# <div class="flex items-center gap-1.5 px-2.5 py-1 text-[13px] text-gray-700 font-medium">
#     <i class="fa-regular fa-clock text-gray-400"></i>
#     <select id="shotsInput" class="bg-transparent outline-none cursor-pointer appearance-none pr-4">
#         <option value="3">3s (3 分镜)</option>
#         <option value="5">5s (5 分镜)</option>
#     </select>
# </div>

old_duration_block = r'<div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white">\s*<div class="flex items-center gap-1\.5 px-2\.5 py-1 text-\[13px\] text-gray-700 font-medium">\s*<i class="fa-regular fa-clock text-gray-400"></i>\s*<select id="shotsInput" class="bg-transparent outline-none cursor-pointer appearance-none pr-4">\s*<option value="3">3s \(3 分镜\)</option>\s*<option value="5">5s \(5 分镜\)</option>\s*</select>\s*</div>\s*</div>'

# We replace it with a comprehensive dropdown containing minute-level options and a Custom option that shows a slider.
# Actually, since it's a dropdown, let's keep it simple first.
new_duration_block = """<div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white relative">
                            <div class="flex items-center gap-1.5 px-2.5 py-1 text-[13px] text-gray-700 font-medium">
                                <i class="fa-regular fa-clock text-gray-400"></i>
                                <select id="shotsInput" class="bg-transparent outline-none cursor-pointer appearance-none pr-4" onchange="handleDurationChange()">
                                    <option value="20">2 分钟</option>
                                    <option value="30">3 分钟</option>
                                    <option value="50">5 分钟</option>
                                    <option value="100">10 分钟</option>
                                    <option value="custom">自定义时长...</option>
                                </select>
                            </div>
                            
                            <!-- Slider Popup -->
                            <div id="customDurationPopup" class="absolute bottom-full left-0 mb-2 w-64 bg-white border border-gray-200 shadow-xl rounded-2xl p-4 hidden z-50">
                                <div class="flex justify-between items-center mb-3">
                                    <span class="text-sm font-bold text-gray-800">自定义短剧时长</span>
                                    <span id="sliderValueText" class="text-sm font-bold text-brand-500">15 分钟</span>
                                </div>
                                <input type="range" id="durationSlider" min="2" max="30" value="15" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500" oninput="updateSliderValue()">
                                <div class="flex justify-between text-xs text-gray-400 mt-2">
                                    <span>2min</span>
                                    <span>30min</span>
                                </div>
                            </div>
                        </div>"""

html = re.sub(old_duration_block, new_duration_block, html)

# We need to add logic for the handleDurationChange and updateSliderValue
slider_js = """
        let customShots = 150; // default 15min (approx 10 shots per minute)
        
        function handleDurationChange() {
            const select = document.getElementById('shotsInput');
            const popup = document.getElementById('customDurationPopup');
            if(select.value === 'custom') {
                popup.classList.remove('hidden');
            } else {
                popup.classList.add('hidden');
            }
            updateCost();
        }

        function updateSliderValue() {
            const slider = document.getElementById('durationSlider');
            const val = slider.value;
            document.getElementById('sliderValueText').innerText = `${val} 分钟`;
            // Calculate equivalent shots (rough estimate: 1 min = 10 shots)
            customShots = val * 10;
            updateCost();
        }
        
        function updateCost() {
            const select = document.getElementById('shotsInput');
            let shots = select.value === 'custom' ? customShots : parseInt(select.value);
            // Every shot costs 15 tokens roughly
            const cost = shots * 15;
            const costEl = document.querySelector('.fa-brands.fa-product-hunt.text-black').nextSibling;
            if(costEl) {
                costEl.textContent = ` ${cost}`;
            }
        }
        
        // Hide popup when clicking outside
        document.addEventListener('click', (e) => {
            const popup = document.getElementById('customDurationPopup');
            const select = document.getElementById('shotsInput');
            if (popup && !popup.classList.contains('hidden')) {
                if (!popup.contains(e.target) && e.target !== select) {
                    popup.classList.add('hidden');
                    // Reset to a default if they didn't really interact? 
                    // No, let it stay 'custom' but just hide the UI so it doesn't block.
                }
            }
        });
"""

# Let's find where to inject this JS
# Before `async function startGeneration()`
html = html.replace('async function startGeneration()', slider_js + '\n        async function startGeneration()')

# Also, update startGeneration to use the correct shots value
old_shots_get = "const shots = document.getElementById('shotsInput').value;"
new_shots_get = "const shotsSelect = document.getElementById('shotsInput').value;\n            const shots = shotsSelect === 'custom' ? customShots : shotsSelect;"
html = html.replace(old_shots_get, new_shots_get)

with open(html_path, "w") as f:
    f.write(html)
