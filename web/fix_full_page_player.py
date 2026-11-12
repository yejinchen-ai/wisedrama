import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I likely replaced something wrong, causing the modal to override the whole layout, 
# or I accidentally nested the modal incorrectly.
# Let's inspect where `id="videoModal"` is placed.
# Ah, the modal is placed right before `</body>`. If it was placed there, `fixed inset-0` should just overlay.
# The issue: "style="display: none;"" might have been stripped, or `videoModal` was placed INSIDE a grid?
# Looking at the image, the video takes up the ENTIRE page, EXCEPT the sidebar.
# Wait, if the sidebar is visible, that means the modal is NOT `fixed inset-0`, but somehow taking up the `<main>` space!
# Let's check where it got injected.

if 'id="videoModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50' in html:
    pass

# We can enforce it to be absolutely at the end of body.
# Wait, look at the previous script where I did: `html = html.replace('</body>', new_modal_html)`
# `new_modal_html` contained `</body>` inside it, so `</body>` was added.
# BUT I probably accidentally overwrote something or there was an open tag.

# Let's completely nuke `id="videoModal"` and rebuild it safely.
modal_pattern = r'<!-- Large Detail Modal.*?</div>\s*</div>\s*</div>'
html = re.sub(modal_pattern, '', html, flags=re.DOTALL)

# Clean up any duplicate </body>
html = re.sub(r'</body>\s*</body>', '</body>', html)

# The correct floating player from the user's PREVIOUS message (320x180 overlay on the bottom right/center)
# The user said: "上面显示标题，下方显示视频生成的提示词(不需要全部展示)，和做同款按钮。"
# And they provided an image. The image showed a floating player, not a full screen one.
# But wait, the image in THIS message shows a giant black video player taking over the ENTIRE right side of the screen (main content area).
# This means my code accidentally replaced the entire `<main>` or something.
# Let's just fix it by injecting a pristine, isolated, fixed PiP (Picture in Picture) player that matches their exact spec.

# Actually, the user's previous request: "推荐尺寸（16:9 黄金比例）标准悬浮（推荐）：320px × 180px； 上面显示标题，下方显示视频生成的提示词(不需要全部展示)，和做同款按钮。"
# I should build a 320px wide floating card with Video + Text + Button stacked vertically.

new_floating_card = """
    <!-- Floating Card Player -->
    <div id="videoModal" class="fixed z-[100] w-[320px] bg-white rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.15)] border border-gray-100 flex flex-col overflow-hidden transition-all duration-300 opacity-0 pointer-events-none" style="display: none; bottom: 30px; right: 30px; transform: translateY(20px);">
        
        <!-- Header: Title and Close -->
        <div class="px-4 py-2.5 bg-gray-50 border-b border-gray-100 flex justify-between items-center z-10">
            <div class="flex items-center gap-2 overflow-hidden">
                <div class="w-1.5 h-1.5 rounded-full bg-[#15d172] animate-pulse shrink-0"></div>
                <span id="modalTitle" class="text-[13px] font-bold text-gray-800 line-clamp-1 truncate">视频标题</span>
            </div>
            <button onclick="closeVideo()" class="text-gray-400 hover:text-red-500 transition w-6 h-6 flex items-center justify-center rounded-full hover:bg-gray-200">
                <i class="fa-solid fa-xmark text-sm"></i>
            </button>
        </div>

        <!-- Video Player (16:9) -->
        <div class="relative w-full aspect-video bg-black">
            <video id="modalVideoPlayer" class="w-full h-full object-contain" controls autoplay playsinline loop></video>
        </div>

        <!-- Footer: Prompt and Action -->
        <div class="p-4 bg-white flex flex-col gap-3">
            <p id="modalPrompt" class="text-[11px] text-gray-500 leading-relaxed line-clamp-2">
                视频提示词将在这里显示...
            </p>
            <button onclick="useTemplateFromModal()" class="w-full bg-[#15d172] hover:bg-[#10b260] text-white py-2 rounded-xl font-bold text-[13px] transition flex items-center justify-center gap-1.5 shadow-sm">
                <i class="fa-solid fa-wand-magic-sparkles"></i> 做同款
            </button>
        </div>
    </div>
"""

# Let's insert this safely right before </body>
html = html.replace('</body>', new_floating_card + '\n</body>')

# Ensure JS logic is correct for this new modal ID
old_js_funcs = r'let currentShowcaseTitle = "";.*?window\.scrollTo\(\{ top: 0, behavior: \'smooth\' \}\);\s*\}[\s\S]*?// --- Draggable Logic ---.*?\}\s*\}'
if 'function openVideo' not in html:
    # We might have nuked it if it matched old_js_funcs incorrectly.
    pass

# We will just rewrite the JS logic cleanly.
clean_js = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const modal = document.getElementById('videoModal');
            const videoEl = document.getElementById('modalVideoPlayer');
            
            document.getElementById('modalTitle').innerText = item.title;
            // Mock prompt
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

# Try to replace the old JS block if it exists
match_js = re.search(r'let currentShowcaseTitle = "";.*?setTimeout\(\(\) => ideaInput.*?1500\);\s*\}', html, flags=re.DOTALL)
if match_js:
    html = html.replace(match_js.group(0), clean_js)
else:
    # Just append it before </script>
    html = html.replace('</script>\n</body>', clean_js + '\n</script>\n</body>')

with open(html_path, "w") as f:
    f.write(html)
