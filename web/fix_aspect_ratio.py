import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Update max-width and aspect ratio
html = html.replace('max-w-[380px]', 'max-w-[600px]')
html = html.replace('aspect-[9/16]', 'aspect-[5/4]')

# The mask and gradient might be too aggressive for a wider player. Let's adjust them.
html = html.replace('style="-webkit-mask-image: linear-gradient(to bottom, black 85%, transparent 100%); mask-image: linear-gradient(to bottom, black 85%, transparent 100%);"', 
                    'style="-webkit-mask-image: radial-gradient(ellipse at center, black 60%, transparent 100%); mask-image: radial-gradient(ellipse at center, black 60%, transparent 100%);"')

# Remove the hardcoded left/right 12px black/80 gradients, as they might look weird. We'll rely on the radial mask or subtle inner shadows.
# Wait, let's keep the subtle edge fading.
html = html.replace('class="absolute inset-y-0 left-0 w-12 bg-gradient-to-r from-black/80 to-transparent pointer-events-none z-10"', 'class="absolute inset-y-0 left-0 w-16 bg-gradient-to-r from-black to-transparent pointer-events-none z-10"')
html = html.replace('class="absolute inset-y-0 right-0 w-12 bg-gradient-to-l from-black/80 to-transparent pointer-events-none z-10"', 'class="absolute inset-y-0 right-0 w-16 bg-gradient-to-l from-black to-transparent pointer-events-none z-10"')
html = html.replace('class="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-black to-transparent pointer-events-none z-10"', 'class="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black to-transparent pointer-events-none z-10"')
html = html.replace('class="absolute inset-0 border-[4px] border-black/40 rounded-3xl pointer-events-none z-10 mix-blend-overlay"', 'class="absolute inset-0 border-[2px] border-white/10 rounded-[32px] pointer-events-none z-10"')


with open(html_path, "w") as f:
    f.write(html)
