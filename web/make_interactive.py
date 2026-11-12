import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Make sidebar and tabs interactive
js_addition = """
        // Interactive UI logic
        document.querySelectorAll('.sidebar-icon').forEach(icon => {
            icon.addEventListener('click', () => {
                document.querySelectorAll('.sidebar-icon').forEach(i => i.classList.remove('active'));
                icon.classList.add('active');
            });
        });

        const tabSpans = document.querySelectorAll('.overflow-x-auto span');
        tabSpans.forEach(tab => {
            tab.addEventListener('click', () => {
                tabSpans.forEach(t => {
                    t.classList.remove('font-bold', 'text-gray-900', 'border-b-2', 'border-brand-500');
                    t.classList.add('font-medium', 'text-gray-500');
                });
                tab.classList.remove('font-medium', 'text-gray-500');
                tab.classList.add('font-bold', 'text-gray-900', 'border-b-2', 'border-brand-500');
            });
        });

        // Click showcase to load idea
        document.querySelectorAll('#shotsContainer .rounded-2xl').forEach(card => {
            card.addEventListener('click', () => {
                const title = card.querySelector('h4').innerText;
                document.getElementById('ideaInput').value = `以【${title}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });

        // Top nav buttons
        document.querySelectorAll('.gap-4 > button').forEach(btn => {
            if(!btn.classList.contains('bg-[#7c3aed]')) {
                btn.addEventListener('click', () => {
                    alert('功能正在开发中，敬请期待！');
                });
            }
        });
"""

if "// Interactive UI logic" not in html:
    html = html.replace("const API_BASE = window.location.origin;", "const API_BASE = window.location.origin;\n" + js_addition)

with open(html_path, "w") as f:
    f.write(html)
