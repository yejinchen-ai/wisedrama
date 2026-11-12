import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The current player is:
# max-w-[360px] aspect-video
# The user wants exactly this layout from the screenshot:
# A white card. Top is header. Middle is Video. Bottom is Prompt + Button.

new_floating_card = """
    <!-- Floating Card Player -->
    <div id="videoModal" class="fixed z-[100] w-[320px] bg-white rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.15)] border border-gray-100 flex flex-col overflow-hidden transition-all duration-300 opacity-0 pointer-events-none" style="display: none; bottom: 30px; right: 30px; transform: translateY(20px);">
        
        <!-- Header: Title and Close -->
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-100 flex justify-between items-center z-10 shrink-0">
            <div class="flex items-center gap-2 overflow-hidden">
                <div class="w-1.5 h-1.5 rounded-full bg-[#15d172] animate-pulse shrink-0"></div>
                <span id="modalTitle" class="text-[13px] font-bold text-gray-800 line-clamp-1 truncate">视频标题</span>
            </div>
            <button onclick="closeVideo()" class="text-gray-400 hover:text-red-500 transition w-6 h-6 flex items-center justify-center rounded-full hover:bg-gray-200">
                <i class="fa-solid fa-xmark text-sm"></i>
            </button>
        </div>

        <!-- Video Player (16:9) -->
        <div class="relative w-full aspect-video bg-black shrink-0">
            <video id="modalVideoPlayer" class="w-full h-full object-contain" controls autoplay playsinline loop></video>
        </div>

        <!-- Footer: Prompt and Action -->
        <div class="p-4 bg-white flex flex-col gap-3 shrink-0">
            <p id="modalPrompt" class="text-[11px] text-gray-500 leading-relaxed line-clamp-2">
                视频提示词将在这里显示...
            </p>
            <button onclick="useTemplateFromModal()" class="w-full bg-[#15d172] hover:bg-[#10b260] text-white py-2.5 rounded-xl font-bold text-[13px] transition flex items-center justify-center gap-1.5 shadow-sm">
                <i class="fa-solid fa-wand-magic-sparkles"></i> 做同款
            </button>
        </div>
    </div>
"""

# Replace the whole Floating Draggable Player block
html = re.sub(r'<!-- Floating Draggable Player -->.*?</div>\s*</div>\s*</div>', new_floating_card, html, flags=re.DOTALL)

# Update JS logic to use videoModal
js_funcs = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            
            document.getElementById('modalTitle').innerText = item.title;
            document.getElementById('modalPrompt').innerText = `以【${item.title}】为主题，画面呈现出极致的电影级光影质感。主体细节丰富，色彩饱满，每一帧都仿佛是一幅精美的壁纸...`;
            videoEl.src = item.video;
            
            modal.style.display = 'flex';
            
            // Trigger reflow to animate
            void modal.offsetWidth;
            
            modal.classList.remove('opacity-0', 'pointer-events-none');
            modal.style.transform = 'translateY(0)';
        }

        function closeVideo() {
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            
            modal.classList.add('opacity-0', 'pointer-events-none');
            modal.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                modal.style.display = 'none';
                videoEl.pause();
                videoEl.src = '';
            }, 300);
        }
        
        function useTemplateFromModal() {
            closeVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            const ideaInput = document.getElementById('ideaInput');
            ideaInput.focus();
            ideaInput.parentElement.classList.add('ring-2', 'ring-[#15d172]');
            setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);
        }
"""

html = re.sub(r'let currentShowcaseTitle = "";.*?// --- Draggable Logic ---.*?\}\s*\}', js_funcs, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
