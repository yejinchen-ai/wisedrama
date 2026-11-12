import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

old_floating_player_pattern = r'<!-- Floating Draggable Player -->.*?</div>\s*</body>'

new_floating_player = """
    <!-- Floating Draggable Player -->
    <div id="floatingPlayer" class="fixed z-[100] w-[90%] max-w-[380px] flex flex-col opacity-0 pointer-events-none transition-all duration-300" style="display: none; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95);">
        
        <div class="w-full bg-black/60 backdrop-blur-3xl rounded-[32px] shadow-[0_0_80px_rgba(21,209,114,0.25)] border border-white/10 flex flex-col overflow-hidden relative" style="-webkit-mask-image: linear-gradient(to bottom, black 85%, transparent 100%); mask-image: linear-gradient(to bottom, black 85%, transparent 100%);">
            
            <!-- Drag Header -->
            <div id="dragHeader" class="px-5 py-4 bg-transparent flex justify-between items-center cursor-move select-none group relative z-20">
                <div class="absolute inset-x-0 top-1.5 flex justify-center">
                    <div class="w-12 h-1.5 rounded-full bg-white/20 group-hover:bg-brand-500/50 transition"></div>
                </div>
                <div class="flex items-center gap-2 overflow-hidden pointer-events-none mt-2">
                    <div class="w-2 h-2 rounded-full bg-brand-500 animate-pulse shrink-0 shadow-[0_0_8px_rgba(21,209,114,1)]"></div>
                    <span id="floatTitle" class="text-[14px] font-bold text-white line-clamp-1 truncate drop-shadow-md">Video Title</span>
                </div>
                <div class="flex items-center gap-3 shrink-0 z-10 mt-2">
                    <button onclick="useTemplateFromFloat()" class="text-[12px] font-bold bg-brand-500/90 text-white px-3 py-1.5 rounded-xl hover:bg-brand-400 transition flex items-center gap-1.5 shadow-[0_0_15px_rgba(21,209,114,0.4)] backdrop-blur">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> 做同款
                    </button>
                    <button onclick="closeFloatVideo()" class="text-white/60 hover:text-white transition w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/10 backdrop-blur">
                        <i class="fa-solid fa-xmark text-lg"></i>
                    </button>
                </div>
            </div>
            
            <!-- Video Container: Vertical aspect ratio 9:16 -->
            <div class="relative w-full aspect-[9/16] bg-transparent flex items-center justify-center overflow-hidden">
                <!-- Inner edge fade overlays to make it blend with the glass container -->
                <div class="absolute inset-0 border-[4px] border-black/40 rounded-3xl pointer-events-none z-10 mix-blend-overlay"></div>
                <div class="absolute inset-y-0 left-0 w-12 bg-gradient-to-r from-black/80 to-transparent pointer-events-none z-10"></div>
                <div class="absolute inset-y-0 right-0 w-12 bg-gradient-to-l from-black/80 to-transparent pointer-events-none z-10"></div>
                <div class="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-black to-transparent pointer-events-none z-10"></div>
                
                <video id="floatVideoPlayer" class="w-full h-full object-cover scale-[1.02]" controls autoplay playsinline loop></video>
            </div>
        </div>
    </div>
</body>"""

html = re.sub(old_floating_player_pattern, new_floating_player, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
