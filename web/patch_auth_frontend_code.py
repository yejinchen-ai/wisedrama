import re
file_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(file_path, "r") as f:
    html = f.read()

# Update the register form HTML to include the code input and button
old_reg_contact = """                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">邮箱 / 手机号 <span class="text-red-500">*</span></label>
                    <div class="flex gap-2">
                        <input type="text" id="regContact" class="flex-1 border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="用于找回密码和接收通知">
                    </div>
                </div>"""

new_reg_contact = """                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">邮箱 / 手机号 <span class="text-red-500">*</span></label>
                    <input type="text" id="regContact" class="w-full border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="输入邮箱或手机号">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">验证码 <span class="text-red-500">*</span></label>
                    <div class="flex gap-2">
                        <input type="text" id="regCode" class="flex-1 border border-gray-300 rounded-xl px-4 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition" placeholder="6位验证码">
                        <button type="button" id="sendCodeBtn" onclick="sendVerifyCode()" class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 rounded-xl font-bold text-sm transition whitespace-nowrap border border-gray-200">获取验证码</button>
                    </div>
                </div>"""

html = html.replace(old_reg_contact, new_reg_contact)

# Add sendVerifyCode JS and update handleAuthSubmit
old_handle_auth = "const pass = document.getElementById('regPassword').value.trim();"
new_handle_auth = """const pass = document.getElementById('regPassword').value.trim();
                const code = document.getElementById('regCode').value.trim();
                if (!contact || !user || !pass || !code) { errorEl.innerText = "请填写所有必填项及验证码"; errorEl.classList.remove('hidden'); return; }
                url = `${API_BASE}/api/auth/register`;
                payload = { username: user, password: pass, contact: contact, code: code };"""
                
html = re.sub(r'const pass = document\.getElementById\(\'regPassword\'\)\.value\.trim\(\);\s*if \(!contact \|\| !user \|\| !pass\) \{.*?\}\s*url = `\$\{API_BASE\}/api/auth/register`;\s*payload = \{ username: user, password: pass, contact: contact \};', new_handle_auth, html, flags=re.DOTALL)

# Add sendVerifyCode function before handleAuthSubmit
send_code_js = """
        async function sendVerifyCode() {
            const contact = document.getElementById('regContact').value.trim();
            const errorEl = document.getElementById('authError');
            if (!contact) {
                errorEl.innerText = "请先输入邮箱或手机号";
                errorEl.classList.remove('hidden');
                return;
            }
            
            const btn = document.getElementById('sendCodeBtn');
            btn.disabled = true;
            btn.innerText = "发送中...";
            
            try {
                const res = await fetch(`${API_BASE}/api/auth/send-code`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ contact: contact })
                });
                
                if (res.ok) {
                    errorEl.classList.add('hidden');
                    let countdown = 60;
                    const timer = setInterval(() => {
                        btn.innerText = `${countdown}s 后重试`;
                        countdown--;
                        if (countdown < 0) {
                            clearInterval(timer);
                            btn.disabled = false;
                            btn.innerText = "获取验证码";
                        }
                    }, 1000);
                } else {
                    const data = await res.json();
                    errorEl.innerText = data.detail || "发送失败，请重试";
                    errorEl.classList.remove('hidden');
                    btn.disabled = false;
                    btn.innerText = "获取验证码";
                }
            } catch(e) {
                errorEl.innerText = "网络请求失败";
                errorEl.classList.remove('hidden');
                btn.disabled = false;
                btn.innerText = "获取验证码";
            }
        }
"""
html = html.replace('async function handleAuthSubmit()', send_code_js + '\n        async function handleAuthSubmit()')

with open(file_path, "w") as f:
    f.write(html)
