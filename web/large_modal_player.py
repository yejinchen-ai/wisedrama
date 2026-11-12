import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Remove the old floating player entirely
old_floating_pattern = r'<!-- Floating Draggable Player -->.*?</div>\s*</div>\s*</div>'
html = re.sub(old_floating_pattern, '', html, flags=re.DOTALL)

# 2. Inject the new Large Detail Modal
new_modal_html = """
    <!-- Large Detail Modal (Desktop Style) -->
    <div id="videoModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm transition-all duration-300 opacity-0" style="display: none;">
        <div id="modalContent" class="w-[92vw] max-w-[1280px] h-[85vh] max-h-[800px] bg-white rounded-2xl shadow-2xl flex flex-col md:flex-row overflow-hidden scale-95 transition-transform duration-300 relative">
            
            <!-- Close Button -->
            <button onclick="closeVideo()" class="absolute top-5 right-5 z-50 w-9 h-9 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 text-gray-500 transition">
                <i class="fa-solid fa-xmark text-lg"></i>
            </button>

            <!-- Left: Large Video Player -->
            <div class="flex-1 bg-[#050505] flex items-center justify-center relative">
                <video id="modalVideoPlayer" class="w-full h-full object-contain" controls autoplay playsinline loop></video>
            </div>

            <!-- Right: Info Panel -->
            <div class="w-full md:w-[380px] bg-white p-8 flex flex-col h-full overflow-y-auto shrink-0">
                <!-- User / Meta Info -->
                <div class="flex items-center justify-between mb-8 pr-10">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-brand-500 text-white flex items-center justify-center font-bold text-sm shadow-md">W</div>
                        <span class="text-sm font-bold text-gray-800">WiseDrama</span>
                        <span class="bg-gray-100 text-gray-500 hover:text-gray-700 cursor-pointer text-[11px] font-medium px-2.5 py-1 rounded-full transition">+ 关注</span>
                    </div>
                    <div class="flex items-center gap-4 text-gray-400 text-sm">
                        <span class="flex items-center gap-1.5 hover:text-red-500 cursor-pointer transition"><i class="fa-regular fa-heart"></i> <span id="modalViews" class="text-[13px]">229</span></span>
                        <i class="fa-solid fa-ellipsis cursor-pointer hover:text-gray-600 transition"></i>
                    </div>
                </div>

                <!-- Title -->
                <h2 id="modalTitle" class="text-xl font-bold text-gray-900 mb-4 leading-snug">视频标题</h2>

                <!-- Prompt -->
                <p id="modalPrompt" class="text-[14px] text-gray-500 leading-relaxed mb-6 line-clamp-6">
                    这里是视频的提示词。画面中光影交错，色彩鲜艳，完美还原了设定的细节。镜头缓慢推进，展现出极强的电影感，每一帧都充满视觉张力...
                </p>

                <!-- Tags / Meta -->
                <div class="text-[12px] text-gray-400 mb-auto">
                    <span id="modalDate">2026-03-11</span> | 内容由 <span id="modalModel" class="font-medium text-brand-500">Veo 2.0</span> 生成
                </div>

                <!-- Action Button -->
                <div class="pt-6 border-t border-gray-100 mt-6">
                    <button onclick="useTemplateFromModal()" class="w-full bg-brand-500 hover:bg-[#10b260] text-white py-3.5 rounded-xl font-bold text-[15px] transition flex items-center justify-center gap-2 shadow-lg shadow-brand-500/20 active:scale-95">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> 一键做同款
                    </button>
                </div>
            </div>
        </div>
    </div>
</body>
"""

html = html.replace('</body>', new_modal_html)

# 3. Update JS Logic to use the new modal
old_js_funcs = r'let currentShowcaseTitle = "";.*?window\.scrollTo\(\{ top: 0, behavior: \'smooth\' \}\);\s*\}[\s\S]*?// --- Draggable Logic ---.*?\}\s*\}'
new_js_funcs = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            const modalContent = document.getElementById('modalContent');
            
            document.getElementById('modalTitle').innerText = item.title;
            document.getElementById('modalModel').innerText = item.model;
            document.getElementById('modalViews').innerText = item.views.replace('w', 'k'); // Just to mock the number slightly
            
            // Mock a prompt based on the title
            document.getElementById('modalPrompt').innerText = `以【${item.title}】为主题，画面呈现出极致的电影级光影质感。主体细节丰富，色彩饱满。随着镜头的缓慢推拉与摇摄，场景的深度被完美拉扯出来，每一帧都仿佛是一幅精美的壁纸，充满强烈的视觉张力与叙事感。`;
            
            videoEl.src = item.video;
            
            modal.style.display = 'flex';
            // Trigger reflow
            void modal.offsetWidth;
            
            modal.classList.remove('opacity-0');
            modalContent.classList.remove('scale-95');
            modalContent.classList.add('scale-100');
            
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        }

        function closeVideo() {
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            const modalContent = document.getElementById('modalContent');
            
            modal.classList.add('opacity-0');
            modalContent.classList.remove('scale-100');
            modalContent.classList.add('scale-95');
            
            setTimeout(() => {
                modal.style.display = 'none';
                videoEl.pause();
                videoEl.src = '';
                document.body.style.overflow = ''; // Restore background scrolling
            }, 300);
        }
        
        function useTemplateFromModal() {
            closeVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // Highlight the input box briefly
            const ideaInput = document.getElementById('ideaInput');
            ideaInput.focus();
            ideaInput.parentElement.classList.add('ring-2', 'ring-brand-500');
            setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-brand-500'), 1500);
        }
"""

html = re.sub(old_js_funcs, new_js_funcs, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)

