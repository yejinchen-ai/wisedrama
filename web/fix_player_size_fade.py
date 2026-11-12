import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Update width and aspect ratio
# Change max-w-[600px] to max-w-[480px] or exactly 320px depending on design. Since we want mobile-like PiP, 360px x 202px is good for 16:9.
html = html.replace('max-w-[600px]', 'max-w-[360px]')
html = html.replace('aspect-[5/4]', 'aspect-video') # aspect-video is exactly 16:9

# 2. Remove the heavy radial mask that makes video transparent
mask_pattern = r'style="-webkit-mask-image: radial-gradient[^"]*"'
html = re.sub(mask_pattern, '', html)

# 3. Remove the harsh black inner gradients that cover the video sides/bottom
html = html.replace('<div class="absolute inset-y-0 left-0 w-16 bg-gradient-to-r from-black to-transparent pointer-events-none z-10"></div>', '')
html = html.replace('<div class="absolute inset-y-0 right-0 w-16 bg-gradient-to-l from-black to-transparent pointer-events-none z-10"></div>', '')
html = html.replace('<div class="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black to-transparent pointer-events-none z-10"></div>', '')

# 4. Enhance the top header (dragHeader) to be the one with the sleek gradient/blur fade
# We want the video to be fully opaque below the header, and the header itself to be a glass overlay on top of the video or just above it.
# Currently dragHeader is outside the video aspect container, but inside the main container.
# Let's make dragHeader an absolute overlay on TOP of the video, with a gradient fade downward.
old_header = r'<!-- Drag Header -->.*?</div>\s*<!-- Video Container'
new_header = """<!-- Drag Header (Overlay) -->
            <div id="dragHeader" class="absolute top-0 inset-x-0 h-20 bg-gradient-to-b from-black/80 via-black/40 to-transparent flex flex-col justify-start items-center cursor-move select-none group z-20 pointer-events-auto transition-opacity">
                <!-- Drag Handle -->
                <div class="w-12 h-1.5 rounded-full bg-white/30 group-hover:bg-brand-500/80 transition mt-2 mb-1"></div>
                <!-- Controls Row -->
                <div class="w-full px-4 flex justify-between items-center mt-1">
                    <div class="flex items-center gap-2 overflow-hidden pointer-events-none">
                        <div class="w-2 h-2 rounded-full bg-brand-500 animate-pulse shrink-0 shadow-[0_0_8px_rgba(21,209,114,1)]"></div>
                        <span id="floatTitle" class="text-[13px] font-bold text-white line-clamp-1 truncate drop-shadow-md">Video Title</span>
                    </div>
                    <div class="flex items-center gap-2 shrink-0 z-10">
                        <button onclick="useTemplateFromFloat()" class="text-[11px] font-bold bg-brand-500/90 text-white px-2.5 py-1 rounded-lg hover:bg-brand-400 transition flex items-center gap-1 shadow-sm backdrop-blur">
                            <i class="fa-solid fa-wand-magic-sparkles"></i> 做同款
                        </button>
                        <button onclick="closeFloatVideo()" class="text-white/80 hover:text-red-400 transition w-6 h-6 flex items-center justify-center rounded-full hover:bg-black/20 backdrop-blur">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Video Container"""
html = re.sub(old_header, new_header, html, flags=re.DOTALL)

# Make sure the container border and shadow are elegant
html = html.replace('rounded-[32px] shadow-[0_0_80px_rgba(21,209,114,0.25)] border border-white/10 flex flex-col overflow-hidden relative', 'rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] border border-white/10 flex flex-col overflow-hidden relative')
html = html.replace('class="absolute inset-0 border-[2px] border-white/10 rounded-[32px] pointer-events-none z-10"', 'class="absolute inset-0 border border-white/10 rounded-2xl pointer-events-none z-10"')

with open(html_path, "w") as f:
    f.write(html)
