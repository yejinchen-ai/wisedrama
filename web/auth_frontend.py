import re
html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Add Login Modal HTML
login_modal = """
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
                <p class="text-sm text-gray-500 mt-1" id="authSubtitle">未注册账号将自动创建</p>
            </div>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
                    <input type="text" id="authUsername" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="请输入用户名">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
                    <input type="password" id="authPassword" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="请输入密码">
                </div>
                <div id="authError" class="text-red-500 text-xs hidden">用户名或密码错误</div>
                <button onclick="handleAuth()" class="w-full bg-brand-500 hover:bg-brand-600 text-white font-bold py-3 rounded-xl transition shadow-md mt-2 flex justify-center items-center gap-2">
                    <span id="authBtnText">进入工作室</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </div>
    </div>
"""

if 'id="authModal"' not in html:
    html = html.replace('</body>', login_modal + '\n</body>')

# 2. Add auth logic to JS
auth_js = """
        // Auth Logic
        function checkAuth() {
            const token = localStorage.getItem('wd_token');
            if (token) {
                fetch(`${API_BASE}/api/auth/me`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                }).then(res => res.json()).then(data => {
                    if (data.username) {
                        updateUserUI(data.username, data.tokens);
                    } else {
                        localStorage.removeItem('wd_token');
                    }
                }).catch(() => localStorage.removeItem('wd_token'));
            }
        }

        function updateUserUI(username, tokens) {
            // Update token balances in sidebar and header if possible
            document.querySelectorAll('.mt-2.text-\\[12px\\], .mt-2.text-\\[14px\\]').forEach(el => {
                if(el.innerText.trim() === '0' || !isNaN(parseInt(el.innerText))) {
                    el.innerText = tokens;
                }
            });
            // Update auth state in UI
            const loginBtn = document.getElementById('mobileLoginBtn');
            if (loginBtn) {
                loginBtn.innerHTML = `<i class="fa-regular fa-user"></i> ${username}`;
                loginBtn.onclick = () => {
                    if(confirm('确定要退出登录吗？')) {
                        localStorage.removeItem('wd_token');
                        window.location.reload();
                    }
                };
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

        async function handleAuth() {
            const user = document.getElementById('authUsername').value.trim();
            const pass = document.getElementById('authPassword').value.trim();
            if (!user || !pass) return;
            
            document.getElementById('authError').classList.add('hidden');
            const btnText = document.getElementById('authBtnText');
            btnText.innerText = "处理中...";

            // Try Login first
            let res = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({username: user, password: pass})
            });

            if (!res.ok) {
                // If login fails, try register
                res = await fetch(`${API_BASE}/api/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({username: user, password: pass})
                });
            }

            if (res.ok) {
                const data = await res.json();
                localStorage.setItem('wd_token', data.access_token);
                closeAuthModal();
                checkAuth();
            } else {
                document.getElementById('authError').classList.remove('hidden');
                document.getElementById('authError').innerText = "登录或注册失败";
            }
            btnText.innerText = "进入工作室";
        }
        
        // Call checkAuth on load
        window.addEventListener('DOMContentLoaded', checkAuth);
"""

if 'function checkAuth()' not in html:
    html = html.replace('// Interactive UI logic', auth_js + '\n        // Interactive UI logic')

# 3. Add token header to generate request
html = html.replace("body: JSON.stringify({ idea: idea, num_shots: parseInt(shots), model: model })", 
                    "body: JSON.stringify({ idea: idea, num_shots: parseInt(shots), model: model }),\n                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('wd_token')}` }")
html = html.replace("headers: { 'Content-Type': 'application/json' },\n                    body: JSON.stringify", "body: JSON.stringify") # Cleanup duplicate header

# 4. Prompt login before generating
login_check = """
            if(!localStorage.getItem('wd_token')) {
                showAuthModal();
                return;
            }
"""
html = html.replace("const idea = document.getElementById('ideaInput').value.trim();", login_check + "\n            const idea = document.getElementById('ideaInput').value.trim();")

# 5. Fix mobile login button to trigger modal
html = html.replace('<div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">', '<div id="mobileLoginBtn" onclick="showAuthModal()" class="px-3 py-1.5 bg-gray-100 rounded-full flex items-center justify-center text-xs font-bold text-gray-700 cursor-pointer hover:bg-gray-200">登录</div><div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center hidden">')

with open(html_path, "w") as f:
    f.write(html)
