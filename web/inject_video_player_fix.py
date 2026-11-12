import re
import json

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

new_showcase_data = [
    {"id": 1, "title": "《霓虹深渊》- 赛博朋克微短剧", "img": "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2021/08/11/84705-587883204_tiny.mp4", "duration": "03:12", "views": "12.5w", "model": "Veo 2.0", "category": "赛博朋克"},
    {"id": 2, "title": "夜之城：失控的AI仿生人", "img": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2020/05/11/38722-421111626_tiny.mp4", "duration": "01:45", "views": "8.9w", "model": "Hailuo 2.3", "category": "赛博朋克"},
    {"id": 3, "title": "未来赛车：光速漂移", "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2021/08/11/84705-587883204_tiny.mp4", "duration": "00:58", "views": "21.3w", "model": "Sora", "category": "赛博朋克"},
    {"id": 4, "title": "《长风渡》- 国风仙侠短剧（饭制）", "img": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2023/11/27/191060-889814429_tiny.mp4", "duration": "05:40", "views": "8.2w", "model": "Hailuo 2.3", "category": "国风仙侠"},
    {"id": 5, "title": "剑气纵横三万里：水墨武侠", "img": "https://images.unsplash.com/photo-1576485290814-1c72aa4bbb8e?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2022/02/10/107297-676104443_tiny.mp4", "duration": "02:15", "views": "15.6w", "model": "Veo 2.0", "category": "国风仙侠"},
    {"id": 6, "title": "青丘狐妖：幻境唯美空镜", "img": "https://images.unsplash.com/photo-1615414050682-192a5d2109fb?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2023/11/27/191060-889814429_tiny.mp4", "duration": "01:20", "views": "3.4w", "model": "Hailuo 2.3", "category": "国风仙侠"},
    {"id": 7, "title": "《猫咪侦探局》- 萌宠悬疑剧", "img": "https://images.unsplash.com/photo-1580477667995-2b920625368a?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2023/04/09/158145-815801968_tiny.mp4", "duration": "02:30", "views": "5.6w", "model": "Veo 2.0", "category": "萌宠动画"},
    {"id": 8, "title": "柯基的奇幻太空漂流", "img": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2020/05/26/40141-424168097_tiny.mp4", "duration": "01:10", "views": "45.1w", "model": "Sora", "category": "萌宠动画"},
    {"id": 9, "title": "魔法少女的终极咏唱", "img": "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2022/11/05/137830-768390740_tiny.mp4", "duration": "03:45", "views": "11.2w", "model": "Hailuo 2.3", "category": "二次元"},
    {"id": 10, "title": "日系新海诚风：电车与黄昏", "img": "https://images.unsplash.com/photo-1494548162494-384bba4ab999?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2020/03/10/33420-396500589_tiny.mp4", "duration": "00:45", "views": "33.8w", "model": "Veo 2.0", "category": "二次元"},
    {"id": 11, "title": "《阿尔卑斯之恋》- 唯美情感短剧", "img": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2016/09/13/5049-181180026_tiny.mp4", "duration": "01:50", "views": "9.3w", "model": "Veo 2.0", "category": "微短剧"},
    {"id": 12, "title": "霸总的秘密协议：第一集", "img": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80", "video": "https://cdn.pixabay.com/video/2020/08/18/47413-450917637_tiny.mp4", "duration": "04:20", "views": "18.9w", "model": "Hailuo 2.3", "category": "微短剧"}
]

modal_html = """
    <!-- Video Player Modal -->
    <div id="videoModal" class="fixed inset-0 bg-black/95 z-[100] hidden flex flex-col items-center justify-center opacity-0 transition-opacity duration-300">
        <button onclick="closeVideo()" class="absolute top-6 right-6 text-white hover:text-brand-500 w-12 h-12 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 transition backdrop-blur z-50">
            <i class="fa-solid fa-xmark text-2xl"></i>
        </button>
        <div class="relative w-full max-w-5xl px-4 flex-1 flex flex-col justify-center items-center py-10">
            
            <div class="w-full bg-black rounded-2xl overflow-hidden shadow-[0_0_80px_rgba(21,209,114,0.15)] border border-white/10 relative group aspect-video">
                <!-- Top gradient overlay for text readability -->
                <div class="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-black/80 to-transparent z-10 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity"></div>
                
                <video id="showcasePlayer" class="w-full h-full object-contain bg-black z-0 relative" controls autoplay playsinline loop></video>
                
                <!-- Info overlay -->
                <div class="absolute top-4 left-4 right-4 flex justify-between items-start z-20 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <div class="bg-black/50 backdrop-blur-md px-4 py-2 rounded-xl pointer-events-auto border border-white/5">
                        <h3 id="modalTitle" class="text-white font-bold text-lg mb-1 drop-shadow-md">Video Title</h3>
                        <p class="text-gray-300 text-xs flex items-center gap-2">
                            <span id="modalModel" class="bg-brand-500/20 text-brand-500 px-1.5 py-0.5 rounded border border-brand-500/30">Model</span>
                            <span id="modalViews"><i class="fa-solid fa-play text-[10px] mr-1"></i> 0</span>
                        </p>
                    </div>
                    <button class="bg-brand-500 text-white px-5 py-2.5 rounded-xl font-bold text-sm pointer-events-auto shadow-lg shadow-brand-500/20 flex items-center gap-2 hover:bg-[#10b260] transition scale-100 hover:scale-105" onclick="useTemplate()">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> 一键做同款
                    </button>
                </div>
            </div>
            
        </div>
    </div>
"""

# Insert modal
if 'id="videoModal"' not in html:
    html = html.replace('</body>', modal_html + '\n</body>')

# Replace JSON string safely avoiding re.sub escape issues
import json
new_json_str = json.dumps(new_showcase_data, ensure_ascii=False)
html = re.sub(r'const showcaseData = \[.*?\];', lambda m: f'const showcaseData = {new_json_str};', html)

# Replace click logic
old_click_js = """                card.addEventListener('click', () => {
                    document.getElementById('ideaInput').value = `以【${item.title}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });"""
new_click_js = """                card.addEventListener('click', () => {
                    openVideo(item);
                });"""
html = html.replace(old_click_js, new_click_js)


# Add Modal functions
new_functions = """
        let currentShowcaseTitle = "";

        function openVideo(item) {
            currentShowcaseTitle = item.title;
            const modal = document.getElementById('videoModal');
            const player = document.getElementById('showcasePlayer');
            document.getElementById('modalTitle').innerText = item.title;
            document.getElementById('modalModel').innerText = item.model;
            document.getElementById('modalViews').innerHTML = `<i class="fa-solid fa-play text-[10px] mr-1"></i> ${item.views} 播放`;
            
            player.src = item.video;
            
            modal.classList.remove('hidden');
            setTimeout(() => {
                modal.classList.remove('opacity-0');
            }, 10);
        }

        function closeVideo() {
            const modal = document.getElementById('videoModal');
            const player = document.getElementById('showcasePlayer');
            modal.classList.add('opacity-0');
            setTimeout(() => {
                modal.classList.add('hidden');
                player.pause();
                player.src = '';
            }, 300);
        }
        
        function useTemplate() {
            closeVideo();
            document.getElementById('ideaInput').value = `以【${currentShowcaseTitle}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
"""
if "function openVideo(" not in html:
    html = html.replace("const API_BASE = window.location.origin;", "const API_BASE = window.location.origin;\n" + new_functions)

with open(html_path, "w") as f:
    f.write(html)
