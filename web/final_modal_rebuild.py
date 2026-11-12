import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I am completely replacing the `videoModal` with exactly what is in the new image.
# The new image shows: 
# It's an overlay covering the entire screen. The sidebar is slightly visible, meaning the modal covers the MAIN content area, or it covers the whole screen with a white background.
# Wait, look at the image: the modal is a FULL SCREEN white background overlay that slides over the main area! 
# The sidebar on the left is still the original sidebar. This means the modal is `absolute` or `fixed` inside the `<main>` or it just covers the page but is styled exactly like the main page layout.
# Let's just make it a fixed full-screen white overlay.
# Left side: Big video player with rounded corners.
# Right side: Info panel (Title, Prompt, Action button).
# Close button ("X") on the top right.

new_modal = """
    <!-- Large Detail Modal (Full Page Overlay) -->
    <div id="videoModal" class="fixed inset-y-0 right-0 z-[100] bg-white/95 backdrop-blur-3xl flex transition-all duration-500 transform translate-x-full opacity-0" style="display: none; width: calc(100% - 96px);">
        
        <!-- Close Button -->
        <button onclick="closeVideo()" class="absolute top-6 right-8 text-gray-400 hover:text-black transition p-2 z-50">
            <i class="fa-solid fa-xmark text-2xl"></i>
        </button>

        <div class="flex w-full h-full p-10 gap-10">
            <!-- Left: Huge Video Player -->
            <div class="flex-1 flex flex-col justify-center items-center relative h-full">
                <!-- Outer glow / glass edge effect using box-shadow -->
                <div class="w-full max-w-[1000px] aspect-video bg-black rounded-3xl overflow-hidden relative shadow-[0_20px_60px_rgba(0,0,0,0.15)] ring-1 ring-black/5" style="box-shadow: 0 0 40px rgba(0,0,0,0.1), inset 0 0 0 1px rgba(255,255,255,0.1);">
                    <video id="modalVideoPlayer" class="w-full h-full object-contain" controls autoplay playsinline loop></video>
                    <!-- Gradual transparent edge on the video container itself -->
                    <div class="absolute inset-x-0 top-0 h-16 bg-gradient-to-b from-black/40 to-transparent pointer-events-none"></div>
                    <div class="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/60 to-transparent pointer-events-none"></div>
                </div>
            </div>

            <!-- Right: Info Panel -->
            <div class="w-[420px] flex flex-col h-full pt-4 pr-4 shrink-0">
                <!-- User Info Row -->
                <div class="flex items-center justify-between mb-8">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-brand-500 text-white flex items-center justify-center font-bold text-sm shadow-md">W</div>
                        <span class="text-sm font-bold text-gray-800">WiseDrama</span>
                        <span class="bg-gray-100 text-gray-600 hover:text-gray-800 cursor-pointer text-[12px] font-medium px-3 py-1 rounded-full transition border border-gray-200">+ 关注</span>
                    </div>
                    <div class="flex items-center gap-4 text-gray-500">
                        <span class="flex items-center gap-1.5 hover:text-red-500 cursor-pointer transition"><i class="fa-regular fa-heart"></i> <span id="modalViews" class="text-[14px]">229</span></span>
                        <i class="fa-solid fa-ellipsis cursor-pointer hover:text-gray-800 transition text-lg"></i>
                    </div>
                </div>

                <!-- Content -->
                <h2 id="modalTitle" class="text-[22px] font-extrabold text-gray-900 mb-4 leading-snug">视频标题</h2>
                <p id="modalPrompt" class="text-[15px] text-gray-500 leading-relaxed mb-6 font-normal">
                    视频提示词将在这里显示...
                </p>
                <div class="text-[13px] text-gray-400 mb-auto">
                    2026-03-11 | 内容由 <span id="modalModel" class="font-medium text-brand-500">AI</span> 生成
                </div>

                <!-- Action Footer -->
                <div class="pt-6 border-t border-gray-100 mt-auto pb-8">
                    <button onclick="useTemplateFromModal()" class="w-full bg-[#15d172] hover:bg-[#10b260] text-white py-4 rounded-2xl font-bold text-[16px] transition flex items-center justify-center gap-2 shadow-lg shadow-brand-500/20 active:scale-95">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> 一键做同款
                    </button>
                </div>
            </div>
        </div>
    </div>
"""

# Find and replace the old floating card player
old_modal_pattern = r'<!-- Floating Card Player -->.*?</div>\s*</div>'
html = re.sub(old_modal_pattern, new_modal, html, flags=re.DOTALL)


# Update JS logic to animate this slide-in overlay correctly
js_funcs = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            
            document.getElementById('modalTitle').innerText = item.title;
            document.getElementById('modalModel').innerText = item.model;
            document.getElementById('modalViews').innerText = item.views.replace('w', 'k');
            document.getElementById('modalPrompt').innerText = `以【${item.title}】为主题，画面呈现出极致的电影级光影质感。主体细节丰富，色彩饱满。镜头缓慢推进，展现出极强的电影感，每一帧都充满视觉张力与叙事深度...`;
            videoEl.src = item.video;
            
            modal.style.display = 'flex';
            
            // Trigger reflow to animate
            void modal.offsetWidth;
            
            modal.classList.remove('opacity-0', 'translate-x-full');
            document.body.style.overflow = 'hidden';
        }

        function closeVideo() {
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            
            modal.classList.add('opacity-0', 'translate-x-full');
            
            setTimeout(() => {
                modal.style.display = 'none';
                videoEl.pause();
                videoEl.src = '';
                document.body.style.overflow = '';
            }, 500);
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

html = re.sub(r'let currentShowcaseTitle = "";.*?1500\);\s*\}', js_funcs, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
