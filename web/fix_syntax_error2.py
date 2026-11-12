html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's just blindly remove the `);\n        }` block.
import re
html = re.sub(r'\);\s*\}', '', html, count=1) # wait, this might match something else

# Let's find exactly the line after useTemplateFromModal
old_str = """        function useTemplateFromModal() {
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
        
# It seems the replacement failed because the text was slightly different.
# Let's use regex to find useTemplateFromModal and delete anything up to `// Interactive UI logic`
new_str = """        function useTemplateFromModal() {
            closeVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            const ideaInput = document.getElementById('ideaInput');
            ideaInput.focus();
            ideaInput.parentElement.classList.add('ring-2', 'ring-[#15d172]');
            setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);
        }"""

pattern = r'function useTemplateFromModal\(\) \{[\s\S]*?\}\s*\);\s*\}\s*// Interactive UI logic'
repl = new_str + "\n\n        // Interactive UI logic"
html = re.sub(pattern, repl, html)

with open(html_path, "w") as f:
    f.write(html)
