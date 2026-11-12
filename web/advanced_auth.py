import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Replace the old authModal with a tabbed version
old_auth_modal = r'<!-- Auth Modal -->.*?</div>\s*</div>\s*</div>'

new_auth_modal = """
    <!-- Auth Modal -->
    <div id="authModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/60 backdrop-blur-sm transition-all duration-300 opacity-0 pointer-events-none">
        <div class="bg-white w-[90%] max-w-[400px] rounded-2xl shadow-2xl p-8 relative transform scale-95 transition-transform duration-300" id="authBox">
            <button onclick="closeAuthModal()" class="absolute top-4 right-4 text-gray-400 hover:text-gray-800 transition">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
            <div class="text-center mb-6">
                <div class="w-12 h-12 mx-auto rounded-2xl flex items-center justify-center bg-gradient-to-br from-[#15d172] to-[#0ea5e9] shadow-sm mb-3">
                    <i class="fa-solid fa-dharmachakra text-white text-2xl"></i>
                </div>
                <h2 class="text-2xl font-bold text-gray-900" id="authTitle">登录 WiseDrama</h2>
            </div>
            
            <div class="flex bg-gray-100 p-1 rounded-xl mb-6">
                <button id="tabLogin" onclick="switchAuthTab('login')" class="flex-1 py-1.5 text-sm font-bold bg-white text-gray-800 rounded-lg shadow-sm">登录</button>
                <button id="tabRegister" onclick="switchAuthTab('register')" class="flex-1 py-1.5 text-sm font-bold text-gray-500 hover:text-gray-700 rounded-lg transition">注册账号</button>
            </div>

            <!-- Login Form -->
            <div id="loginForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">邮箱/手机号/用户名</label>
                    <input type="text" id="loginUsername" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="请输入账号">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
                    <input type="password" id="loginPassword" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="请输入密码">
                </div>
            </div>

            <!-- Register Form -->
            <div id="registerForm" class="space-y-4 hidden">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">邮箱 / 手机号 <span class="text-red-500">*</span></label>
                    <div class="flex gap-2">
                        <input type="text" id="regContact" class="flex-1 border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="用于找回密码和接收通知">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">用户名 <span class="text-red-500">*</span></label>
                    <input type="text" id="regUsername" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="设置一个炫酷的昵称">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">密码 <span class="text-red-500">*</span></label>
                    <input type="password" id="regPassword" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="设置密码">
                </div>
            </div>

            <div id="authError" class="text-red-500 text-xs hidden mt-3 text-center"></div>
            
            <button onclick="handleAuthSubmit()" class="w-full bg-brand-500 hover:bg-brand-600 text-white font-bold py-3 rounded-xl transition shadow-md mt-6 flex justify-center items-center gap-2">
                <span id="authBtnText">立即登录</span>
                <i class="fa-solid fa-arrow-right"></i>
            </button>
        </div>
    </div>

    <!-- Account Info Modal -->
    <div id="accountModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/60 backdrop-blur-sm transition-all duration-300 opacity-0 pointer-events-none">
        <div class="bg-white w-[90%] max-w-[360px] rounded-3xl shadow-2xl p-8 relative transform scale-95 transition-transform duration-300" id="accountBox">
            <button onclick="closeAccountModal()" class="absolute top-4 right-4 text-gray-400 hover:text-gray-800 transition bg-gray-100 rounded-full w-8 h-8 flex justify-center items-center">
                <i class="fa-solid fa-xmark"></i>
            </button>
            <div class="flex flex-col items-center">
                <div class="w-20 h-20 bg-gradient-to-tr from-brand-500 to-blue-500 rounded-full text-white flex justify-center items-center text-3xl font-bold shadow-lg mb-4" id="accAvatar">W</div>
                <h2 class="text-xl font-extrabold text-gray-900" id="accUsername">Username</h2>
                <span class="text-xs text-gray-500 mt-1 bg-gray-100 px-2 py-0.5 rounded-md" id="accContact">contact@email.com</span>
                
                <div class="w-full bg-brand-50 rounded-2xl p-4 mt-6 border border-brand-100 flex justify-between items-center">
                    <div>
                        <div class="text-brand-600 text-xs font-bold mb-1">可用算力 Token</div>
                        <div class="text-3xl font-black text-brand-500 flex items-center gap-1">
                            <i class="fa-brands fa-product-hunt text-xl"></i> <span id="accTokens">0</span>
                        </div>
                    </div>
                    <button class="bg-white text-brand-500 border border-brand-200 px-4 py-1.5 rounded-lg text-sm font-bold shadow-sm hover:shadow transition">充值</button>
                </div>
                
                <button onclick="logout()" class="w-full mt-6 py-2.5 text-gray-500 hover:bg-red-50 hover:text-red-500 font-bold rounded-xl transition border border-transparent hover:border-red-100">
                    退出登录
                </button>
            </div>
        </div>
    </div>
"""

html = re.sub(old_auth_modal, new_auth_modal, html, flags=re.DOTALL)

# Replace old JS Auth logic
old_js_logic = r'function checkAuth\(\) \{[\s\S]*?\}\s*window\.addEventListener\(\'DOMContentLoaded\', checkAuth\);'
new_js_logic = """
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

        window.addEventListener('DOMContentLoaded', checkAuth);
"""
html = re.sub(old_js_logic, new_js_logic, html, flags=re.DOTALL)

with open(html_path, "w") as f:
    f.write(html)
