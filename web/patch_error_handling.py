import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

old_catch = """            try {
                const res = await fetch(`${API_BASE}/api/generate`, {
                    method: 'POST',
                    body: JSON.stringify({ idea: idea, num_shots: parseInt(shots), model: model }),
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('wd_token')}` }
                });
                const data = await res.json();
                currentJobId = data.job_id;
                pollInterval = setInterval(pollJobStatus, 3000);
            } catch (e) {
                updateStatus("服务器连接失败", 0, "error");
                clearInterval(timerInterval);
                resetUI();
            }"""

new_catch = """            try {
                const res = await fetch(`${API_BASE}/api/generate`, {
                    method: 'POST',
                    body: JSON.stringify({ idea: idea, num_shots: parseInt(shots), model: model }),
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('wd_token')}` }
                });
                const data = await res.json();
                if (res.status === 402) {
                    updateStatus("余额不足，请充值", 0, "error");
                    document.getElementById('topProgress').classList.replace('bg-brand-500', 'bg-red-500');
                    clearInterval(timerInterval);
                    resetUI();
                    return;
                } else if (res.status === 401) {
                    showAuthModal();
                    resetUI();
                    clearInterval(timerInterval);
                    return;
                }
                
                currentJobId = data.job_id;
                pollInterval = setInterval(pollJobStatus, 3000);
            } catch (e) {
                updateStatus("服务器连接失败", 0, "error");
                clearInterval(timerInterval);
                resetUI();
            }"""

html = html.replace(old_catch, new_catch)

with open(html_path, "w") as f:
    f.write(html)
