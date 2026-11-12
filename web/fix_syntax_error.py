html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix the dangling `);` and `}` around line 51 in the JS block.
html = html.replace("""        function useTemplateFromModal() {
            closeVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            const ideaInput = document.getElementById('ideaInput');
            ideaInput.focus();
            ideaInput.parentElement.classList.add('ring-2', 'ring-[#15d172]');
            setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);
        }

);
        }""", """        function useTemplateFromModal() {
            closeVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            const ideaInput = document.getElementById('ideaInput');
            ideaInput.focus();
            ideaInput.parentElement.classList.add('ring-2', 'ring-[#15d172]');
            setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);
        }""")

with open(html_path, "w") as f:
    f.write(html)
