import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Remove the old full-screen modal
modal_pattern = r'<!-- Video Player Modal -->.*?</div>\s*</div>\s*</div>'
html = re.sub(modal_pattern, '', html, flags=re.DOTALL)

# 2. Add the new floating mini-player
floating_player_html = """
    <!-- Floating Mini Player -->
    <div id="floatingPlayer" class="fixed bottom-6 right-6 w-[360px] bg-white rounded-2xl shadow-[0_20px_60px_rgba(0,0,0,0.15)] border border-gray-200 z-[100] transition-all duration-500 translate-y-[150%] opacity-0 flex flex-col overflow-hidden group">
        <div class="px-4 py-2.5 bg-gray-50/90 backdrop-blur border-b border-gray-100 flex justify-between items-center">
            <div class="flex items-center gap-2 overflow-hidden">
                <div class="w-2 h-2 rounded-full bg-brand-500 animate-pulse shrink-0"></div>
                <span id="floatTitle" class="text-[13px] font-bold text-gray-800 line-clamp-1 truncate">Video Title</span>
            </div>
            <div class="flex items-center gap-3 shrink-0">
                <button onclick="useTemplateFromFloat()" class="text-[11px] font-bold bg-brand-500 text-white px-2.5 py-1 rounded-md hover:bg-[#10b260] transition flex items-center gap-1 shadow-sm">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> 同款
                </button>
                <button onclick="closeFloatVideo()" class="text-gray-400 hover:text-red-500 transition w-6 h-6 flex items-center justify-center rounded-full hover:bg-red-50">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
        </div>
        <div class="relative w-full aspect-video bg-black">
            <video id="floatVideoPlayer" class="w-full h-full object-contain" controls autoplay playsinline loop></video>
        </div>
    </div>
"""

html = html.replace('</body>', floating_player_html + '\n</body>')

# 3. Replace the old JS functions with the new floating player logic
old_js_funcs = r'let currentShowcaseTitle = "";.*?window\.scrollTo\(\{ top: 0, behavior: \'smooth\' \}\);\s*\}'
new_js_funcs = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const playerBox = document.getElementById('floatingPlayer');
            const videoEl = document.getElementById('floatVideoPlayer');
            
            document.getElementById('floatTitle').innerText = item.title;
            videoEl.src = item.video;
            
            // Slide up and fade in
            playerBox.classList.remove('translate-y-[150%]', 'opacity-0');
            playerBox.classList.add('translate-y-0', 'opacity-100');
        }

        function closeFloatVideo() {
            const playerBox = document.getElementById('floatingPlayer');
            const videoEl = document.getElementById('floatVideoPlayer');
            
            // Slide down and fade out
            playerBox.classList.remove('translate-y-0', 'opacity-100');
            playerBox.classList.add('translate-y-[150%]', 'opacity-0');
            
            setTimeout(() => {
                videoEl.pause();
                videoEl.src = '';
            }, 500);
        }
        
        function useTemplateFromFloat() {
            closeFloatVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
"""

html = re.sub(old_js_funcs, new_js_funcs, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
