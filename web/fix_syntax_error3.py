html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Wait! The JS error `);\n        }` was introduced in commit `b1d6eab` (the large modal), and my previous attempts to fix it accidentally broke the `setTimeout` closure!
# Since we checked out `web/index.html`, let's just find and cleanly fix that ONE syntax error in HEAD.

old_str = """            setTimeout(() => {
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

);
        }"""

new_str = """            setTimeout(() => {
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
        }"""

if old_str in html:
    html = html.replace(old_str, new_str)
    with open(html_path, "w") as f:
        f.write(html)
    print("Syntax error fixed.")
else:
    print("Could not find the exact syntax error block.")

