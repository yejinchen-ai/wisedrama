import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# I will systematically nuke EVERYTHING after the main `</script>` tag, and reconstruct it cleanly.
script_close_idx = html.rfind('</script>')
if script_close_idx != -1:
    clean_html = html[:script_close_idx + len('</script>')]

    # Now we append exactly what is needed for the Floating Card Player (320x180) and NOTHING else.
    clean_html += """
    
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
</body>
</html>
"""
    with open(html_path, "w") as f:
        f.write(clean_html)
    print("Cleanup successful.")
else:
    print("Could not find </script>")

