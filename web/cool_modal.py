import re
import json

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Enhance modal animation: backdrop-blur, scale in, better box shadow.
old_modal = 'class="fixed inset-0 bg-black/95 z-[100] flex-col items-center justify-center opacity-0 transition-opacity duration-300" style="display: none;"'
new_modal = 'class="fixed inset-0 bg-black/80 backdrop-blur-xl z-[100] flex-col items-center justify-center opacity-0 transition-all duration-500" style="display: none;"'
html = html.replace(old_modal, new_modal)

# Add scale-in to the video container
old_container = 'class="w-full bg-black rounded-2xl overflow-hidden shadow-[0_0_80px_rgba(21,209,114,0.15)] border border-white/10 relative group aspect-video"'
new_container = 'id="modalContent" class="w-full bg-black rounded-3xl overflow-hidden shadow-[0_0_120px_rgba(21,209,114,0.25)] border border-white/10 relative group aspect-video scale-95 transition-transform duration-500"'
html = html.replace(old_container, new_container)

# Update openVideo JS
old_open = """            setTimeout(() => {
                modal.classList.remove('opacity-0');
            }, 10);"""
new_open = """            setTimeout(() => {
                modal.classList.remove('opacity-0');
                document.getElementById('modalContent').classList.remove('scale-95');
                document.getElementById('modalContent').classList.add('scale-100');
            }, 10);"""
html = html.replace(old_open, new_open)

# Update closeVideo JS
old_close = """            modal.classList.add('opacity-0');
            setTimeout(() => {"""
new_close = """            modal.classList.add('opacity-0');
            document.getElementById('modalContent').classList.remove('scale-100');
            document.getElementById('modalContent').classList.add('scale-95');
            setTimeout(() => {"""
html = html.replace(old_close, new_close)

with open(html_path, "w") as f:
    f.write(html)
