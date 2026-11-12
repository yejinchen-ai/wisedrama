import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# The JS replace in advanced_auth.py failed completely because the `old_js_logic` regex didn't match. 
# So the OLD JS is still there (`handleAuth()`, instead of `handleAuthSubmit()`).

# Let's replace the entire Auth JS block cleanly.
old_block_pattern = r'// Auth Logic.*?window\.addEventListener\(\'DOMContentLoaded\', checkAuth\);'

new_block = """// Auth Logic
        let currentAuthMode = 'login';
        let currentUserInfo = null;

        function switchAuthTab(mode) {
            currentAuthMode = mode;
            document.getElementById('authError').classList.add('hidden');
            if(mode === 'login') {
                document.getElementById('tabLogin').classList.replace('text-gray-500', 'text-gray-800');
                document.getElementById('tabLogin').classList.replace('hover:text-gray-700', 'bg-white');
                document.getElementById('tabLogin').classList.add('bg-white', 'shadow-sm');
                
                document.getElementById('tabRegister').classList.replace('text-gray-800', 'text-gray-500');
                document.getElementById('tabRegister').classList.remove('bg-white', 'shadow-sm');
                
                document.getElementById('loginForm').classList.remove('hidden');
                document.getElementById('registerForm').classList.add('hidden');
                document.getElementById('authTitle').innerText = "登录 WiseDrama";
                document.getElementById('authBtnText').innerText = "立即登录";
            } else {
                document.getElementById('tabRegister').classList.replace('text-gray-500', 'text-gray-800');
                document.getElementById('tabRegister').classList.replace('hover:text-gray-700', 'bg-white');
                document.getElementById('tabRegister').classList.add('bg-white', 'shadow-sm');
                
                document.getElementById('tabLogin').classList.replace('text-gray-800', 'text-gray-500');
                document.getElementById('tabLogin').classList.remove('bg-white', 'shadow-sm');
                
                document.getElementById('registerForm').classList.remove('hidden');
                document.getElementById('loginForm').classList.add('hidden');
                document.getElementById('authTitle').innerText = "注册新账号";
                document.getElementById('authBtnText').innerText = "立即注册";
            }
        }

        function checkAuth() {
            const token = localStorage.getItem('wd_token');
            if (token) {
                fetch(`${API_BASE}/api/auth/me`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                }).then(res => res.json()).then(data => {
                    if (data.username) {
                        currentUserInfo = data;
                        updateUserUI(data.username, data.tokens);
                    } else {
                        localStorage.removeItem('wd_token');
                    }
                }).catch(() => localStorage.removeItem('wd_token'));
            }
        }

        function updateUserUI(username, tokens) {
            document.querySelectorAll('.mt-2.text-\\[12px\\], .mt-2.text-\\[14px\\]').forEach(el => {
                if(!isNaN(parseInt(el.innerText))) { el.innerText = tokens; }
            });
            
            const loginBtn = document.getElementById('mobileLoginBtn');
            if (loginBtn) {
                loginBtn.innerHTML = `<i class="fa-regular fa-user"></i> ${username}`;
                loginBtn.onclick = showAccountModal;
            }
            
            const desktopUsername = document.getElementById('desktopUsername');
            const desktopLoginBtn = document.getElementById('desktopLoginBtn');
            if (desktopUsername && desktopLoginBtn) {
                desktopUsername.innerText = username;
                desktopLoginBtn.classList.add('bg-brand-50', 'text-brand-500');
                desktopLoginBtn.innerHTML = `<i class="fa-solid fa-user-check text-lg"></i>`;
                desktopLoginBtn.onclick = showAccountModal;
            }
        }

        function showAuthModal() {
            const modal = document.getElementById('authModal');
            const box = document.getElementById('authBox');
            modal.classList.remove('opacity-0', 'pointer-events-none');
            box.classList.remove('scale-95');
            box.classList.add('scale-100');
        }

        function closeAuthModal() {
            const modal = document.getElementById('authModal');
            const box = document.getElementById('authBox');
            modal.classList.add('opacity-0', 'pointer-events-none');
            box.classList.remove('scale-100');
            box.classList.add('scale-95');
        }

        function showAccountModal() {
            if(!currentUserInfo) return;
            const modal = document.getElementById('accountModal');
            const box = document.getElementById('accountBox');
            
            document.getElementById('accAvatar').innerText = currentUserInfo.username.charAt(0).toUpperCase();
            document.getElementById('accUsername').innerText = currentUserInfo.username;
            document.getElementById('accContact').innerText = currentUserInfo.contact;
            document.getElementById('accTokens').innerText = currentUserInfo.tokens;
            
            modal.classList.remove('opacity-0', 'pointer-events-none');
            box.classList.remove('scale-95');
            box.classList.add('scale-100');
        }

        function closeAccountModal() {
            const modal = document.getElementById('accountModal');
            const box = document.getElementById('accountBox');
            modal.classList.add('opacity-0', 'pointer-events-none');
            box.classList.remove('scale-100');
            box.classList.add('scale-95');
        }

        function logout() {
            localStorage.removeItem('wd_token');
            window.location.reload();
        }

        async function handleAuthSubmit() {
            const errorEl = document.getElementById('authError');
            errorEl.classList.add('hidden');
            
            let url, payload;
            
            if (currentAuthMode === 'login') {
                const user = document.getElementById('loginUsername').value.trim();
                const pass = document.getElementById('loginPassword').value.trim();
                if (!user || !pass) { errorEl.innerText = "请输入账号和密码"; errorEl.classList.remove('hidden'); return; }
                url = `${API_BASE}/api/auth/login`;
                payload = { username: user, password: pass };
            } else {
                const contact = document.getElementById('regContact').value.trim();
                const user = document.getElementById('regUsername').value.trim();
                const pass = document.getElementById('regPassword').value.trim();
                if (!contact || !user || !pass) { errorEl.innerText = "请填写所有必填项"; errorEl.classList.remove('hidden'); return; }
                url = `${API_BASE}/api/auth/register`;
                payload = { username: user, password: pass, contact: contact };
            }

            const btnText = document.getElementById('authBtnText');
            const originalText = btnText.innerText;
            btnText.innerText = "处理中...";

            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (res.ok) {
                    localStorage.setItem('wd_token', data.access_token);
                    closeAuthModal();
                    checkAuth();
                    window.location.reload();
                } else {
                    errorEl.innerText = data.detail || "操作失败，请重试";
                    errorEl.classList.remove('hidden');
                }
            } catch(e) {
                errorEl.innerText = "网络请求失败";
                errorEl.classList.remove('hidden');
            }
            btnText.innerText = originalText;
        }

        window.addEventListener('DOMContentLoaded', checkAuth);"""

html = re.sub(old_block_pattern, new_block, html, flags=re.DOTALL)

# Let's also make sure we fix the onclick button binding
html = html.replace('onclick="handleAuth()"', 'onclick="handleAuthSubmit()"')

with open(html_path, "w") as f:
    f.write(html)
