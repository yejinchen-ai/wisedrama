import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Replace HTML structure
old_floating_player = r'<!-- Floating Mini Player -->.*?</div>\s*</div>'
new_floating_player = """
    <!-- Floating Draggable Player -->
    <div id="floatingPlayer" class="fixed z-[100] w-[90%] max-w-[420px] bg-white rounded-3xl shadow-[0_30px_80px_rgba(0,0,0,0.2)] border border-gray-200 flex flex-col overflow-hidden opacity-0 pointer-events-none transition-all duration-300" style="top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95);">
        <!-- Drag Header -->
        <div id="dragHeader" class="px-5 py-3.5 bg-gray-50/90 backdrop-blur border-b border-gray-100 flex justify-between items-center cursor-move select-none group relative">
            <div class="absolute inset-x-0 top-1 flex justify-center">
                <div class="w-10 h-1 rounded-full bg-gray-300 opacity-50"></div>
            </div>
            <div class="flex items-center gap-2 overflow-hidden pointer-events-none z-10">
                <i class="fa-solid fa-grip-vertical text-gray-300 group-hover:text-brand-500 transition mr-1"></i>
                <div class="w-2 h-2 rounded-full bg-brand-500 animate-pulse shrink-0"></div>
                <span id="floatTitle" class="text-[14px] font-bold text-gray-800 line-clamp-1 truncate">Video Title</span>
            </div>
            <div class="flex items-center gap-3 shrink-0 z-10">
                <button onclick="useTemplateFromFloat()" class="text-[12px] font-bold bg-brand-500 text-white px-3 py-1.5 rounded-lg hover:bg-[#10b260] transition flex items-center gap-1.5 shadow-sm">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> 做同款
                </button>
                <button onclick="closeFloatVideo()" class="text-gray-400 hover:text-red-500 transition w-7 h-7 flex items-center justify-center rounded-full hover:bg-red-50">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>
        </div>
        <div class="relative w-full aspect-[4/3] bg-black">
            <video id="floatVideoPlayer" class="w-full h-full object-contain" controls autoplay playsinline loop></video>
        </div>
    </div>
"""

html = re.sub(old_floating_player, new_floating_player, html, flags=re.DOTALL)

# 2. Replace JS Logic
old_js_funcs = r'let currentShowcaseTitle = "";.*?window\.scrollTo\(\{ top: 0, behavior: \'smooth\' \}\);\s*\}'
new_js_funcs = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const playerBox = document.getElementById('floatingPlayer');
            const videoEl = document.getElementById('floatVideoPlayer');
            
            document.getElementById('floatTitle').innerText = item.title;
            videoEl.src = item.video;
            
            // Reset position to center and animate in
            playerBox.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            playerBox.style.top = '50%';
            playerBox.style.left = '50%';
            playerBox.style.transform = 'translate(-50%, -50%) scale(1)';
            
            playerBox.classList.remove('opacity-0', 'pointer-events-none');
        }

        function closeFloatVideo() {
            const playerBox = document.getElementById('floatingPlayer');
            const videoEl = document.getElementById('floatVideoPlayer');
            
            playerBox.style.transition = 'all 0.3s ease-in';
            playerBox.style.transform = playerBox.style.transform.replace('scale(1)', 'scale(0.95)');
            playerBox.classList.add('opacity-0', 'pointer-events-none');
            
            setTimeout(() => {
                videoEl.pause();
                videoEl.src = '';
            }, 300);
        }
        
        function useTemplateFromFloat() {
            closeFloatVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // --- Draggable Logic ---
        const dragHeader = document.getElementById('dragHeader');
        const floatingPlayer = document.getElementById('floatingPlayer');
        let isDragging = false;
        let startX, startY, initialLeft, initialTop;

        if (dragHeader && floatingPlayer) {
            dragHeader.addEventListener('mousedown', (e) => {
                // Ignore clicks on buttons
                if(e.target.tagName.toLowerCase() === 'button' || e.target.closest('button')) return;
                
                isDragging = true;
                floatingPlayer.style.transition = 'none'; // Disable transition for 1:1 mouse tracking
                
                const rect = floatingPlayer.getBoundingClientRect();
                initialLeft = rect.left;
                initialTop = rect.top;
                startX = e.clientX;
                startY = e.clientY;
                
                // Convert from translate(-50%, -50%) to absolute pixels to avoid dragging math offset issues
                floatingPlayer.style.transform = 'scale(1)'; 
                floatingPlayer.style.left = initialLeft + 'px';
                floatingPlayer.style.top = initialTop + 'px';
                
                document.body.style.userSelect = 'none'; // Prevent text selection while dragging
            });

            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const dx = e.clientX - startX;
                const dy = e.clientY - startY;
                
                floatingPlayer.style.left = (initialLeft + dx) + 'px';
                floatingPlayer.style.top = (initialTop + dy) + 'px';
            });

            document.addEventListener('mouseup', () => {
                if (isDragging) {
                    isDragging = false;
                    document.body.style.userSelect = '';
                }
            });
        }
"""

html = re.sub(old_js_funcs, new_js_funcs, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
