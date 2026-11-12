import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The duplicates start after </script>. So let's split at </script>.
parts = html.split("</script>")
if len(parts) >= 2:
    # the last part is the stuff after the main script block
    # Actually, the modal/floating players are injected OUTSIDE the main script block.
    # Let's find exactly where the main script ends.
    main_script_end = html.rfind("</script>")
    base_html = html[:main_script_end + len("</script>")]
    
    # We will just reconstruct the end of the file properly.
    clean_html = base_html + """
    
    <!-- Floating Draggable Player -->
    <div id="floatingPlayer" class="fixed z-[100] w-[90%] max-w-[420px] bg-white rounded-3xl shadow-[0_30px_80px_rgba(0,0,0,0.2)] border border-gray-200 flex flex-col overflow-hidden opacity-0 pointer-events-none transition-all duration-300" style="display: none; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95);">
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
</body>
</html>
"""
    with open(html_path, "w") as f:
        f.write(clean_html)
