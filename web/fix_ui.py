import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix Slogan
html = html.replace("让你的创意<br>", "每一个想法<br>")
html = html.replace(">变成视觉大片</span>", ">都是一部大片</span>")
html = html.replace("让你的创意\n                    <br>\n                    <span class=\"text-transparent bg-clip-text bg-gradient-to-r from-[#7143ff] to-[#a855f7]\">变成视觉大片</span>", "每一个想法<br>\n                    <span class=\"text-transparent bg-clip-text bg-gradient-to-r from-[#7143ff] to-[#a855f7]\">都是一部大片</span>")


# Fix Sidebar alignment
# Currently: .sidebar-icon { @apply w-12 h-12 flex flex-col items-center justify-center text-gray-500 hover:text-brand-500 hover:bg-brand-50 rounded-xl cursor-pointer transition-all mb-4; }
# Let's change sidebar-icon to ensure flex-col, and maybe increase width or text size.
# Actually, the screenshot shows "首页" next to the icon, maybe because fontawesome icons are inline by default and flex-col isn't applied if tailwind fails? No, it's just that flex-col works but maybe the text is too wide.
# Let's make the sidebar a bit wider or text smaller, and ensure flex-col is applied properly.
html = html.replace("w-[88px]", "w-[96px]")
html = html.replace(".sidebar-icon { @apply w-12 h-12 flex flex-col items-center justify-center", ".sidebar-icon { @apply w-16 h-14 flex flex-col items-center justify-center")

# Update top buttons (Remove HailuoAgent and use something related to WiseDrama)
html = html.replace("创作视频", "创作短剧")
html = html.replace("创作图片", "创作分镜")
html = html.replace("海螺Agent", "编剧Agent")

# Update placeholder text
html = html.replace("一个孩子在公园里放风筝，金色阳光，镜头上移。", "一只叫做奥利奥的橘猫，在赛博朋克城市里寻找遗失的小鱼干，霓虹灯闪烁，推镜头。")

# Update tabs
old_tabs = """<span class="font-bold text-gray-900 border-b-2 border-brand-500 pb-3 -mb-[14px] cursor-pointer whitespace-nowrap">推荐</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">海影节 <span class="text-[9px] bg-[#f3e8ff] text-[#9333ea] px-1 rounded-sm ml-0.5 border border-[#e9d5ff]">展映</span></span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">变身写真</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">搞怪整活</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">风格转绘</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">广告电商</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">怦然心动</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">萌宠来袭</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">Q版童趣</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">炫酷场景</span>"""

new_tabs = """<span class="font-bold text-gray-900 border-b-2 border-brand-500 pb-3 -mb-[14px] cursor-pointer whitespace-nowrap">🔥 热门推荐</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">赛博朋克 <span class="text-[9px] bg-[#f3e8ff] text-[#9333ea] px-1 rounded-sm ml-0.5 border border-[#e9d5ff]">科幻</span></span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">星际史诗</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">悬疑惊悚</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">古风仙侠</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">都市情感</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">日式动漫</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">魔幻奇幻</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">末日废土</span>
                <span class="font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap">搞笑喜剧</span>"""

html = html.replace(old_tabs, new_tabs)

# Update showcases
old_showcases = """<div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer">
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
                </div>"""

new_showcases = """
                <!-- Showcase 1 -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1605810230434-7631ac76ec81?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">03:12</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">《霓虹深渊》- 赛博朋克微短剧</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> 12.5w 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">Veo 2.0</span>
                        </div>
                    </div>
                </div>
                <!-- Showcase 2 -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">05:40</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">《长风渡》- 国风仙侠短剧（饭制）</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> 8.2w 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">Hailuo 2.3</span>
                        </div>
                    </div>
                </div>
                <!-- Showcase 3 -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1506443432602-ac2fcd6f54e0?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">01:15</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">《火星漂流》- 硬核科幻预告片</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> 24.1w 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">Sora</span>
                        </div>
                    </div>
                </div>
                <!-- Showcase 4 -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1580477667995-2b920625368a?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">02:30</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">《猫咪侦探局》- 萌宠悬疑剧</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> 5.6w 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">Veo 2.0</span>
                        </div>
                    </div>
                </div>
                <!-- Showcase 5 -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">04:20</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">《末日拾荒者》- 废土生存短剧</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> 18.9w 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">Hailuo 2.3</span>
                        </div>
                    </div>
                </div>
                <!-- Showcase 6 -->
                <div class="rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group">
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">01:50</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">《阿尔卑斯之恋》- 唯美情感短剧</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> 9.3w 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">Veo 2.0</span>
                        </div>
                    </div>
                </div>
"""

html = html.replace(old_showcases, new_showcases)

# Ensure proper banner text
html = html.replace("让你的创意<br>", "每一个想法<br>")
html = html.replace("让你的创意\n                    <br>", "每一个想法\n                    <br>")
html = html.replace(">变成视觉大片</span>", ">都是一部大片</span>")


with open(html_path, "w") as f:
    f.write(html)
