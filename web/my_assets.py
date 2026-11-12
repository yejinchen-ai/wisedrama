import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Update the Sidebar to link "资产" to the correct UI state, or just make a functional placeholder.
# First, let's find the Sidebar item for assets.
# `<div class="sidebar-icon"><i class="fa-regular fa-folder-open text-[22px]"></i><span class="sidebar-text">资产</span></div>`
old_asset_icon = '<div class="sidebar-icon"><i class="fa-regular fa-folder-open text-[22px]"></i><span class="sidebar-text">资产</span></div>'
new_asset_icon = '<div class="sidebar-icon" onclick="showAssets()"><i class="fa-regular fa-folder-open text-[22px]"></i><span class="sidebar-text">我的资产</span></div>'
html = html.replace(old_asset_icon, new_asset_icon)

# Make "首页" clickable to return
old_home_icon = '<div class="sidebar-icon"><i class="fa-solid fa-house text-[22px]"></i><span class="sidebar-text">首页</span></div>'
new_home_icon = '<div class="sidebar-icon" onclick="window.location.reload()"><i class="fa-solid fa-house text-[22px]"></i><span class="sidebar-text">首页</span></div>'
html = html.replace(old_home_icon, new_home_icon)


# 2. In JS, when a video is done, save it to LocalStorage so we can view it in "我的资产"
js_save_asset = """
                    if(job.final_video_url) {
                        const finalContainer = document.getElementById('finalVideoContainer');
                        finalContainer.classList.remove('hidden');
                        document.getElementById('finalVideoPlayer').src = API_BASE + job.final_video_url;
                        document.getElementById('finalDownloadBtn').href = API_BASE + job.final_video_url;
                        
                        // Save to My Assets
                        saveToAssets(job);
                    }
"""

html = re.sub(r'if\(job\.final_video_url\) \{[\s\S]*?document\.getElementById\(\'finalDownloadBtn\'\)\.href = API_BASE \+ job\.final_video_url;\s*\}', js_save_asset, html)

js_asset_funcs = """
        // Asset Management
        function saveToAssets(job) {
            let assets = JSON.parse(localStorage.getItem('wiseDramaAssets') || '[]');
            // Avoid duplicates
            if (!assets.some(a => a.id === job.id)) {
                assets.unshift({
                    id: job.id,
                    title: job.script ? job.script.title : '未命名短剧',
                    video: API_BASE + job.final_video_url,
                    date: new Date().toLocaleDateString(),
                    model: job.model,
                    views: '1',
                    duration: '00:00'
                });
                localStorage.setItem('wiseDramaAssets', JSON.stringify(assets));
            }
        }

        function showAssets() {
            // Hide main generation UI
            document.querySelector('.input-box').classList.add('hidden');
            document.querySelector('.mb-6 h1').innerHTML = '我的资产<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-[#10b260] to-[#15d172]">个人创作库</span>';
            document.querySelectorAll('.flex.flex-col.md\\:flex-row.gap-3').forEach(el => el.classList.add('hidden')); // banners
            document.getElementById('categoryTabs').classList.add('hidden');
            document.getElementById('finalVideoContainer').classList.add('hidden');
            
            // Render assets
            const container = document.getElementById('shotsContainer');
            container.innerHTML = '';
            
            let assets = JSON.parse(localStorage.getItem('wiseDramaAssets') || '[]');
            if (assets.length === 0) {
                container.innerHTML = '<div class="col-span-full text-center py-20 text-gray-400">暂无生成的短剧资产，快去创作吧！</div>';
                return;
            }
            
            assets.forEach(item => {
                const card = document.createElement('div');
                card.className = "rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group";
                card.innerHTML = `
                    <div class="relative w-full aspect-[4/3] overflow-hidden bg-black">
                        <video src="${item.video}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" preload="metadata"></video>
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">本地存盘</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">${item.title}</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-calendar-days text-[10px] mr-1"></i> ${item.date}</span>
                            <span class="bg-brand-50 text-brand-500 border border-brand-100 px-1.5 rounded">${item.model}</span>
                        </div>
                    </div>
                `;
                
                card.addEventListener('click', () => {
                    openVideo(item);
                });
                
                container.appendChild(card);
            });
        }
"""
html = html.replace('// Interactive UI logic', js_asset_funcs + '\n        // Interactive UI logic')

with open(html_path, "w") as f:
    f.write(html)
