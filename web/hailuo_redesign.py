import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"

new_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiseDrama - 创作视频 (Hailuo Style)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            500: '#7c3aed', // Purple for the main brand color
                            600: '#6d28d9',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #ffffff; color: #111; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
        .sidebar-icon { @apply w-12 h-12 flex flex-col items-center justify-center text-gray-500 hover:text-brand-500 hover:bg-brand-50 rounded-xl cursor-pointer transition-all mb-4; }
        .sidebar-icon.active { @apply text-brand-500 bg-brand-50; }
        .sidebar-text { @apply text-[11px] mt-1 font-medium; }
        .input-box { @apply bg-white border border-gray-200 rounded-3xl p-5 shadow-[0_2px_15px_rgba(0,0,0,0.04)] transition-shadow duration-300; }
        .input-box:focus-within { @apply border-brand-500/50 shadow-[0_8px_30px_rgba(124,58,237,0.08)]; }
        .frame-upload { @apply w-24 h-[104px] bg-[#f8f9fa] border border-gray-200 rounded-2xl flex flex-col items-center justify-center text-gray-400 cursor-pointer hover:bg-gray-100 transition relative overflow-hidden; }
        .pill-btn { @apply flex items-center gap-1.5 px-3 py-1.5 border border-gray-200 rounded-xl text-[13px] font-medium text-gray-600 bg-white hover:bg-gray-50 cursor-pointer transition; }
        /* Hide scrollbar for gallery tabs */
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>
<body class="flex h-screen overflow-hidden text-gray-800">
    
    <!-- Sidebar (Left) -->
    <aside class="w-[88px] bg-white border-r border-gray-100 flex flex-col items-center py-6 h-full shrink-0 z-10 flex-shrink-0 flex-grow-0">
        <!-- Logo Icon -->
        <div class="w-12 h-12 rounded-2xl flex items-center justify-center mb-8 bg-gradient-to-br from-[#FF4D4D] via-[#a855f7] to-[#3b82f6] shadow-sm">
            <i class="fa-solid fa-dharmachakra text-white text-2xl"></i>
        </div>
        
        <div class="sidebar-icon"><i class="fa-solid fa-house text-[22px]"></i><span class="sidebar-text">首页</span></div>
        <div class="sidebar-icon"><i class="fa-solid fa-infinity text-[22px]"></i><span class="sidebar-text">Agent</span></div>
        <div class="sidebar-icon"><i class="fa-regular fa-folder-open text-[22px]"></i><span class="sidebar-text">资产</span></div>
        
        <div class="w-8 h-px bg-gray-100 my-2"></div>
        
        <div class="sidebar-icon active relative">
            <i class="fa-solid fa-video text-[22px]"></i><span class="sidebar-text">视频</span>
            <span class="absolute -top-0 -right-2 text-brand-500 font-bold text-[10px]">New</span>
        </div>
        <div class="sidebar-icon"><i class="fa-regular fa-image text-[22px]"></i><span class="sidebar-text">图片</span></div>
        <div class="sidebar-icon"><i class="fa-solid fa-music text-[22px]"></i><span class="sidebar-text">音频</span></div>
        
        <div class="mt-auto flex flex-col items-center w-full relative">
            <div class="w-full flex justify-center mb-6">
                <div class="border border-brand-500 text-brand-500 rounded-[10px] px-2 py-8 text-[11px] font-bold flex flex-col items-center justify-between h-20 bg-brand-50 relative cursor-pointer">
                    <span class="absolute -top-2 bg-brand-500 text-white px-1.5 rounded-sm text-[9px] leading-tight">SALE</span>
                    <span class="mt-2 text-[14px]">0</span>
                    <span class="text-[10px]">升级</span>
                </div>
            </div>
            
            <div class="w-9 h-9 bg-[#1e40af] text-white rounded-full flex items-center justify-center mb-1 cursor-pointer shadow-md"><i class="fa-solid fa-c text-lg font-bold"></i></div>
            <span class="text-[10px] text-gray-500 font-bold mb-4">API</span>
            <div class="text-gray-400 cursor-pointer hover:text-gray-600"><i class="fa-solid fa-ellipsis"></i></div>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 h-full overflow-y-auto bg-white relative">
        <div class="max-w-[1280px] mx-auto px-10 py-8">
            
            <!-- Top Tabs -->
            <div class="flex items-center gap-4 mb-10 w-full">
                <button class="bg-[#7c3aed] text-white px-8 py-3 rounded-full font-bold text-[15px] flex items-center gap-2 shadow-md hover:bg-[#6d28d9] transition w-[240px] justify-center relative overflow-hidden group">
                    创作视频
                    <img src="https://cdn-icons-png.flaticon.com/512/3208/3208573.png" class="absolute right-2 top-1/2 -translate-y-1/2 w-16 opacity-30 group-hover:scale-110 transition-transform" alt="camera">
                </button>
                <button class="bg-[#f3f4f6] text-gray-700 px-8 py-3 rounded-full font-bold text-[15px] hover:bg-gray-200 transition w-[240px] justify-center">
                    创作图片
                </button>
                <button class="bg-[#f3f4f6] text-gray-700 px-8 py-3 rounded-full font-bold text-[15px] hover:bg-gray-200 transition w-[240px] justify-center">
                    海螺Agent
                </button>
            </div>

            <!-- Hero Title -->
            <div class="mb-6">
                <h1 class="text-[34px] font-bold leading-[1.3] tracking-tight text-[#111827]">
                    让你的创意<br>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#7143ff] to-[#a855f7]">变成视觉大片</span>
                </h1>
            </div>

            <!-- Main Input Area -->
            <div class="input-box mb-10 relative border-2 border-transparent focus-within:border-[#e5e7eb] focus-within:shadow-[0_8px_30px_rgba(0,0,0,0.06)]">
                <div class="flex gap-4 mb-4 min-h-[140px]">
                    <!-- Left: First/Last Frames -->
                    <div class="flex items-center gap-3 shrink-0 ml-1 mt-1">
                        <div class="frame-upload">
                            <i class="fa-solid fa-plus text-[24px] text-gray-400 font-light mb-1"></i>
                            <span class="text-[12px] text-gray-400">首帧</span>
                        </div>
                        <div class="flex flex-col gap-1 items-center text-gray-300">
                            <i class="fa-solid fa-arrow-right-arrow-left text-[10px]"></i>
                        </div>
                        <div class="frame-upload">
                            <i class="fa-solid fa-plus text-[24px] text-gray-400 font-light mb-1"></i>
                            <span class="text-[12px] text-gray-400">尾帧</span>
                        </div>
                    </div>
                    
                    <!-- Right: Textarea -->
                    <div class="flex-1 ml-2">
                        <textarea id="ideaInput" class="w-full h-full resize-none outline-none text-[15px] leading-relaxed placeholder-[#9ca3af] text-gray-800 bg-transparent pt-2" placeholder="描述您想要生成的视频内容，例如，“一个孩子在公园里放风筝，金色阳光，镜头上移。”"></textarea>
                    </div>
                </div>
                
                <div class="h-px bg-gray-100 w-full mb-4"></div>
                
                <!-- Bottom Toolbar -->
                <div class="flex items-center justify-between">
                    <!-- Left Selectors -->
                    <div class="flex items-center gap-2.5">
                        <div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white">
                            <div class="flex items-center gap-1.5 px-2.5 py-1 text-[13px] text-gray-700 font-medium">
                                <i class="fa-solid fa-cube text-gray-400"></i>
                                <select id="modelInput" class="bg-transparent outline-none cursor-pointer appearance-none pr-4">
                                    <option value="hailuo">Hailuo 2.3-Fast</option>
                                    <option value="veo">Veo 2.0 (Google)</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="pill-btn cursor-default bg-white"><i class="fa-solid fa-compress text-gray-400"></i> 768p</div>
                        
                        <div class="flex items-center border border-gray-200 rounded-xl px-1 py-1 bg-white">
                            <div class="flex items-center gap-1.5 px-2.5 py-1 text-[13px] text-gray-700 font-medium">
                                <i class="fa-regular fa-clock text-gray-400"></i>
                                <select id="shotsInput" class="bg-transparent outline-none cursor-pointer appearance-none pr-4">
                                    <option value="3">3s (3 分镜)</option>
                                    <option value="5">5s (5 分镜)</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Right Create Button -->
                    <div class="flex items-center gap-5">
                        <div class="text-[14px] font-bold text-gray-800 flex items-center gap-1.5">
                            <i class="fa-brands fa-product-hunt text-black"></i> 15
                        </div>
                        <button id="generateBtn" onclick="startGeneration()" class="bg-[#111827] hover:bg-black text-white px-7 py-2.5 rounded-full font-bold text-[14px] transition flex items-center gap-1.5 shadow-md">
                            <i class="fa-solid fa-wand-magic-sparkles text-[12px]"></i> 创作
                        </button>
                    </div>
                </div>
                
                <!-- Status Panel (Hidden by default) -->
                <div id="statusPanel" class="hidden mt-4 border-t border-gray-100 pt-4 pb-1">
                    <div class="flex items-center justify-between text-[13px] font-medium text-gray-600 mb-2">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-circle-notch text-brand-500 animate-spin"></i>
                            <span id="statusText">正在提交生成任务...</span>
                        </div>
                        <span id="timerText" class="font-mono text-gray-400">00:00</span>
                    </div>
                    <div class="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div id="topProgress" class="h-full bg-brand-500 w-0 transition-all duration-300"></div>
                    </div>
                </div>
            </div>

            <!-- Horizontal Banners -->
            <div class="flex flex-col md:flex-row gap-5 mb-10 w-full">
                <div class="flex-1 bg-gradient-to-r from-[#80d0c7] to-[#13547a] h-[160px] rounded-2xl overflow-hidden relative shadow-sm cursor-pointer group">
                    <div class="absolute inset-0 p-6 text-white z-10 flex flex-col justify-center">
                        <div class="flex items-center gap-2 mb-2">
                            <div class="bg-white/20 backdrop-blur-md px-2 py-0.5 rounded text-[10px] font-bold">Hailuo AI x 人民日报新媒体</div>
                        </div>
                        <h3 class="font-bold text-[22px] leading-tight mb-1">人民日报·未来已来AI创意<br>大比拼活动专区</h3>
                        <p class="text-[12px] opacity-80 mt-1">用海螺AI畅想未来的中国</p>
                    </div>
                    <div class="absolute right-4 top-1/2 -translate-y-1/2 w-[180px] h-[180px] bg-[url('https://cdn3d.iconscout.com/3d/premium/thumb/astronaut-5842018-4897933.png')] bg-contain bg-no-repeat opacity-90 group-hover:scale-105 transition-transform duration-500 z-10"></div>
                </div>
                
                <div class="flex-1 bg-black h-[160px] rounded-2xl overflow-hidden relative shadow-sm cursor-pointer group">
                     <div class="absolute inset-0 p-6 text-white z-10 flex flex-col justify-center">
                        <div class="flex items-center gap-2 mb-2">
                            <i class="fa-solid fa-wave-square text-xs"></i> <span class="text-[12px] font-bold text-gray-300">MINIMAX × Hailuo AI</span>
                        </div>
                        <h3 class="font-bold text-[24px] leading-tight">MiniMax Hailuo 2.3 / 2.3<br>Fast</h3>
                    </div>
                    <!-- Right image placeholder for banner -->
                    <div class="absolute right-0 top-0 bottom-0 w-3/5 bg-[url('https://images.unsplash.com/photo-1542204165-65bf26472b9b?auto=format&fit=crop&w=600&q=80')] bg-cover bg-center opacity-70 group-hover:opacity-90 transition-opacity"></div>
                    <div class="absolute right-0 top-0 bottom-0 w-3/5 bg-gradient-to-r from-black via-black/50 to-transparent"></div>
                </div>
            </div>

            <!-- Gallery Category Tabs -->
            <div class="flex items-center gap-8 overflow-x-auto no-scrollbar mb-6 border-b border-gray-100 pb-3 mt-4 text-[15px]">
                <span class="font-bold text-gray-900 border-b-2 border-brand-500 pb-3 -mb-[14px] cursor-pointer whitespace-nowrap">推荐</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">海影节 <span class="text-[9px] bg-[#f3e8ff] text-[#9333ea] px-1 rounded-sm ml-0.5 border border-[#e9d5ff]">展映</span></span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">变身写真</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">搞怪整活</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">风格转绘</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">广告电商</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">怦然心动</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">萌宠来袭</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">Q版童趣</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">炫酷场景</span>
            </div>

            <!-- Real-time Generated Results Area -->
            <div id="finalVideoContainer" class="hidden mb-10 mt-6 bg-[#f9fafb] border border-gray-200 rounded-3xl p-6 shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2"><i class="fa-solid fa-film text-brand-500"></i> 成片首映</h2>
                    <a id="finalDownloadBtn" href="#" download class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-800 px-4 py-2 rounded-xl text-sm font-bold transition flex items-center gap-2 shadow-sm">
                        <i class="fa-solid fa-download"></i> 下载
                    </a>
                </div>
                <video id="finalVideoPlayer" controls class="w-full rounded-2xl aspect-video object-contain bg-black shadow-md"></video>
            </div>

            <div id="shotsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 pb-20">
                <!-- Fallback Static Cards matching the screenshot if no jobs active -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer">
                    <img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=400&q=80" class="w-full aspect-[4/3] object-cover">
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">Hailuo 2.3/2.3Fast</h4>
                    </div>
                </div>
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer">
                    <img src="https://images.unsplash.com/photo-1618331835717-801e976710b2?auto=format&fit=crop&w=400&q=80" class="w-full aspect-[4/3] object-cover">
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">Hailuo 2.3/2.3Fast</h4>
                    </div>
                </div>
            </div>
            
        </div>
    </main>

    <script>
        const API_BASE = window.location.origin;
        let currentJobId = null;
        let pollInterval = null;
        let timerInterval = null;
        let secondsElapsed = 0;

        function formatTime(sec) {
            const m = Math.floor(sec / 60).toString().padStart(2, '0');
            const s = (sec % 60).toString().padStart(2, '0');
            return `${m}:${s}`;
        }

        async function startGeneration() {
            const idea = document.getElementById('ideaInput').value.trim();
            const shots = document.getElementById('shotsInput').value;
            const model = document.getElementById('modelInput').value;
            
            if(!idea) {
                document.getElementById('ideaInput').classList.add('ring-2', 'ring-red-400');
                setTimeout(() => document.getElementById('ideaInput').classList.remove('ring-2', 'ring-red-400'), 1000);
                document.getElementById('ideaInput').focus();
                return;
            }

            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-circle-notch animate-spin"></i> 创作中...';
            btn.classList.add('opacity-80', 'cursor-not-allowed');
            
            document.getElementById('statusPanel').classList.remove('hidden');
            document.getElementById('shotsContainer').innerHTML = '';
            document.getElementById('finalVideoContainer').classList.add('hidden');
            
            secondsElapsed = 0;
            document.getElementById('timerText').innerText = "00:00";
            if(timerInterval) clearInterval(timerInterval);
            timerInterval = setInterval(() => {
                secondsElapsed++;
                document.getElementById('timerText').innerText = formatTime(secondsElapsed);
            }, 1000);
            
            updateStatus("Agent 正在规划剧本与美术设定...", 10);

            try {
                const res = await fetch(`${API_BASE}/api/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ idea: idea, num_shots: parseInt(shots), model: model })
                });
                const data = await res.json();
                currentJobId = data.job_id;
                pollInterval = setInterval(pollJobStatus, 3000);
            } catch (e) {
                updateStatus("服务器连接失败", 0, "error");
                clearInterval(timerInterval);
                resetUI();
            }
        }

        async function pollJobStatus() {
            if(!currentJobId) return;
            try {
                const res = await fetch(`${API_BASE}/api/job/${currentJobId}`);
                const job = await res.json();

                if(job.status === "writing_script") {
                    updateStatus("编剧Agent正在撰写分镜...", 20);
                } else if(job.status === "generating_art_direction") {
                    updateStatus("美术Agent正在生成锁定设定图...", 35);
                } else if(job.status === "generating_prompts") {
                    updateStatus("提示词工程师正在平滑过渡...", 45);
                } else if(job.status.startsWith("generating_videos")) {
                    updateStatus("导演Agent正在调用视觉模型渲染...", 65);
                    renderShots(job.shots);
                } else if(job.status === "stitching_videos") {
                    updateStatus("剪辑Agent正在合成最终成片...", 90);
                    renderShots(job.shots);
                } else if(job.status === "completed") {
                    updateStatus("生成完成！", 100);
                    if(job.final_video_url) {
                        const finalContainer = document.getElementById('finalVideoContainer');
                        finalContainer.classList.remove('hidden');
                        document.getElementById('finalVideoPlayer').src = API_BASE + job.final_video_url;
                        document.getElementById('finalDownloadBtn').href = API_BASE + job.final_video_url;
                    }
                    renderShots(job.shots); 
                    clearInterval(pollInterval);
                    clearInterval(timerInterval);
                    resetUI();
                    setTimeout(() => document.getElementById('statusPanel').classList.add('hidden'), 5000);
                } else if(job.status.startsWith("failed")) {
                    updateStatus("任务失败: " + job.status, 100);
                    document.getElementById('topProgress').classList.replace('bg-brand-500', 'bg-red-500');
                    clearInterval(pollInterval);
                    clearInterval(timerInterval);
                    resetUI();
                }
            } catch (e) {}
        }

        function updateStatus(text, percent) {
            document.getElementById('statusText').innerText = text;
            if(percent !== undefined) {
                document.getElementById('topProgress').style.width = `${percent}%`;
            }
        }

        function resetUI() {
            const btn = document.getElementById('generateBtn');
            btn.disabled = false;
            btn.classList.remove('opacity-80', 'cursor-not-allowed');
            btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles text-[12px]"></i> 创作';
        }

        function renderShots(shots) {
            if(!shots || shots.length === 0) return;
            const container = document.getElementById('shotsContainer');
            container.innerHTML = '';

            shots.forEach(shot => {
                const isDone = shot.status === 'completed';
                const isProcessing = shot.status === 'processing';
                const isFailed = shot.status === 'failed';
                
                let mediaHtml = '';
                if(isDone && shot.video_url) {
                    mediaHtml = `
                        <video src="${shot.video_url}" controls loop muted class="w-full aspect-[4/3] object-cover bg-black"></video>
                    `;
                } else if (isProcessing) {
                    mediaHtml = `
                        <div class="w-full aspect-[4/3] bg-gray-50 flex flex-col items-center justify-center text-brand-500 border-b border-gray-100">
                            <i class="fa-solid fa-circle-notch animate-spin text-2xl mb-2"></i>
                            <span class="text-[11px] font-bold tracking-widest uppercase">渲染中</span>
                        </div>
                    `;
                } else if (isFailed) {
                    mediaHtml = `
                        <div class="w-full aspect-[4/3] bg-red-50 flex flex-col items-center justify-center text-red-400 border-b border-red-100">
                            <i class="fa-solid fa-circle-xmark text-2xl mb-2"></i>
                            <span class="text-[11px] font-bold tracking-widest uppercase">渲染失败</span>
                        </div>
                    `;
                } else {
                    mediaHtml = `
                        <div class="w-full aspect-[4/3] bg-gray-50 flex flex-col items-center justify-center text-gray-400 border-b border-gray-100">
                            <i class="fa-solid fa-hourglass-half text-xl mb-2 opacity-50"></i>
                            <span class="text-[10px] font-bold tracking-widest uppercase">排队中</span>
                        </div>
                    `;
                }

                const card = document.createElement('div');
                card.className = "rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition flex flex-col";
                card.innerHTML = `
                    <div class="relative w-full shrink-0 group">
                        ${mediaHtml}
                        ${isDone ? `<a href="${shot.video_url}" download target="_blank" class="absolute top-2 right-2 bg-black/50 hover:bg-black/80 text-white w-7 h-7 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition"><i class="fa-solid fa-download text-[10px]"></i></a>` : ''}
                    </div>
                    <div class="p-4 flex flex-col flex-1">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[11px] font-bold text-gray-800 bg-gray-100 px-2 py-0.5 rounded-md">分镜 ${shot.shot_number}</span>
                        </div>
                        <p class="text-[13px] text-gray-600 line-clamp-3 mb-2 flex-1" title="${shot.prompt}">${shot.prompt}</p>
                    </div>
                `;
                container.appendChild(card);
            });
        }
    </script>
</body>
</html>
"""

with open(html_path, "w") as f:
    f.write(new_html)

print("HTML redesigned with bright Hailuo AI style successfully.")
