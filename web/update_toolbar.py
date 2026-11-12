import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Update the Model Selector
old_model = """<div class="flex items-center gap-1.5 px-2.5 py-1 text-[13px] text-gray-700 font-medium">
                                <i class="fa-solid fa-cube text-gray-400"></i>
                                <select id="modelInput" class="bg-transparent outline-none cursor-pointer appearance-none pr-4">
                                    <option value="hailuo">Hailuo 2.3-Fast</option>
                                    <option value="veo">Veo 2.0 (Google)</option>
                                </select>
                            </div>"""
new_model = """<div class="flex items-center gap-2 px-3 py-1.5 text-[13px] text-gray-700 font-medium">
                                <span class="text-gray-400 text-[11px] font-bold uppercase tracking-wider hidden md:block">Models</span>
                                <i class="fa-solid fa-cube text-brand-500 md:hidden"></i>
                                <select id="modelInput" class="bg-transparent font-bold outline-none cursor-pointer appearance-none pr-2">
                                    <option value="hailuo">Hailuo 2.3-Fast</option>
                                    <option value="veo">Veo 2.0 (Google)</option>
                                </select>
                                <i class="fa-solid fa-chevron-down text-[9px] text-gray-400"></i>
                            </div>"""
html = html.replace(old_model, new_model)

# 2. Update Resolution Selector
old_res = '<div class="pill-btn cursor-default bg-white"><i class="fa-solid fa-compress text-gray-400"></i> 768p</div>'
new_res = """<div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white hover:border-gray-300 transition">
                            <div class="flex items-center gap-2 px-3 py-1.5 text-[13px] text-gray-700 font-medium">
                                <span class="text-gray-400 text-[11px] font-bold uppercase tracking-wider hidden md:block">分辨率</span>
                                <i class="fa-solid fa-compress text-brand-500 md:hidden"></i>
                                <select id="resolutionInput" class="bg-transparent font-bold outline-none cursor-pointer appearance-none pr-2">
                                    <option value="720p">720p</option>
                                    <option value="1080p" selected>1080p</option>
                                    <option value="2k">2K</option>
                                    <option value="4k">4K</option>
                                </select>
                                <i class="fa-solid fa-chevron-down text-[9px] text-gray-400"></i>
                            </div>
                        </div>"""
html = html.replace(old_res, new_res)

# 3. Update the Duration Slider
old_slider = """<div class="flex flex-col border border-gray-200 rounded-xl px-4 py-2 bg-white w-full md:w-48 shadow-sm">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-[12px] font-bold text-gray-500"><i class="fa-regular fa-clock mr-1"></i> 短剧时长</span>
                                <span id="durationLabel" class="text-[13px] font-extrabold text-brand-500">3 分钟</span>
                            </div>
                            <input type="range" id="durationSlider" min="1" max="30" value="3" class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500" oninput="updateDurationUI()">
                            <input type="hidden" id="shotsInput" value="30">
                        </div>"""

new_slider = """<div class="flex flex-col border border-gray-200 hover:border-gray-300 transition rounded-xl px-4 py-2.5 bg-white w-full md:w-56 shadow-[0_2px_10px_rgba(0,0,0,0.02)] group">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider">生成时长</span>
                                <span id="durationLabel" class="text-[13px] font-black text-brand-500 bg-brand-50 px-2 py-0.5 rounded-md border border-brand-100">3 分钟</span>
                            </div>
                            <div class="relative flex items-center h-2">
                                <input type="range" id="durationSlider" min="1" max="30" value="3" class="absolute w-full h-1.5 bg-gray-100 rounded-full appearance-none cursor-pointer z-20 outline-none" style="background: linear-gradient(to right, #15d172 10%, #f3f4f6 10%);" oninput="updateDurationUI()">
                            </div>
                            <input type="hidden" id="shotsInput" value="30">
                        </div>"""
html = html.replace(old_slider, new_slider)

# 4. Update the updateDurationUI JS to dynamically update the slider track background gradient
old_update_js = """        function updateDurationUI() {
            const slider = document.getElementById('durationSlider');
            if(!slider) return;
            const val = parseInt(slider.value);
            document.getElementById('durationLabel').innerText = `${val} 分钟`;"""

new_update_js = """        function updateDurationUI() {
            const slider = document.getElementById('durationSlider');
            if(!slider) return;
            const val = parseInt(slider.value);
            document.getElementById('durationLabel').innerText = `${val} 分钟`;
            
            // Update slider background track color
            const percentage = ((val - slider.min) / (slider.max - slider.min)) * 100;
            slider.style.background = `linear-gradient(to right, #15d172 ${percentage}%, #f3f4f6 ${percentage}%)`;
"""
html = html.replace(old_update_js, new_update_js)

# Replace slider thumb CSS
style_block = """
        .sidebar-icon i { font-size: 22px; display: block; }
"""
new_style = """
        .sidebar-icon i { font-size: 22px; display: block; }
        
        /* Custom Slider Thumb */
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
        }
"""
html = html.replace(style_block, new_style)

with open(html_path, "w") as f:
    f.write(html)
