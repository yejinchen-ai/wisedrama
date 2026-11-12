import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Desktop sidebar user profile placeholder:
old_desktop_profile = """<div class="w-9 h-9 bg-[#1e40af] text-white rounded-full flex items-center justify-center mb-1 cursor-pointer shadow-md"><i class="fa-solid fa-c text-lg font-bold"></i></div>
            <span class="text-[10px] text-gray-500 font-bold mb-4">API</span>"""

new_desktop_profile = """<div id="desktopLoginBtn" onclick="showAuthModal()" class="w-10 h-10 bg-gray-100 text-gray-500 hover:text-brand-500 hover:bg-brand-50 rounded-full flex items-center justify-center mb-1 cursor-pointer shadow-sm transition">
                <i class="fa-regular fa-user text-lg"></i>
            </div>
            <span id="desktopUsername" class="text-[10px] text-gray-500 font-bold mb-4 truncate w-full text-center px-1">未登录</span>"""

html = html.replace(old_desktop_profile, new_desktop_profile)

# Update JS to handle desktopUsername
old_js_update = """            const loginBtn = document.getElementById('mobileLoginBtn');
            if (loginBtn) {
                loginBtn.innerHTML = `<i class="fa-regular fa-user"></i> ${username}`;
                loginBtn.onclick = () => {
                    if(confirm('确定要退出登录吗？')) {
                        localStorage.removeItem('wd_token');
                        window.location.reload();
                    }
                };
            }"""

new_js_update = """            const loginBtn = document.getElementById('mobileLoginBtn');
            if (loginBtn) {
                loginBtn.innerHTML = `<i class="fa-regular fa-user"></i> ${username}`;
                loginBtn.onclick = () => {
                    if(confirm('确定要退出登录吗？')) {
                        localStorage.removeItem('wd_token');
                        window.location.reload();
                    }
                };
            }
            
            const desktopUsername = document.getElementById('desktopUsername');
            const desktopLoginBtn = document.getElementById('desktopLoginBtn');
            if (desktopUsername && desktopLoginBtn) {
                desktopUsername.innerText = username;
                desktopLoginBtn.classList.add('bg-brand-50', 'text-brand-500');
                desktopLoginBtn.innerHTML = `<i class="fa-solid fa-user-check text-lg"></i>`;
                desktopLoginBtn.onclick = () => {
                    if(confirm('确定要退出登录吗？')) {
                        localStorage.removeItem('wd_token');
                        window.location.reload();
                    }
                };
            }"""

html = html.replace(old_js_update, new_js_update)

with open(html_path, "w") as f:
    f.write(html)
