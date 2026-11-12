import re
import json

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Generate the showcase data mimicking Hailuo and Jimeng
showcases = [
    # 赛博朋克
    {"id": 1, "title": "《霓虹深渊》- 赛博朋克微短剧", "img": "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?auto=format&fit=crop&w=600&q=80", "duration": "03:12", "views": "12.5w", "model": "Veo 2.0", "category": "赛博朋克"},
    {"id": 2, "title": "夜之城：失控的AI仿生人", "img": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=600&q=80", "duration": "01:45", "views": "8.9w", "model": "Hailuo 2.3", "category": "赛博朋克"},
    {"id": 3, "title": "未来赛车：光速漂移", "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "duration": "00:58", "views": "21.3w", "model": "Sora", "category": "赛博朋克"},
    
    # 国风仙侠
    {"id": 4, "title": "《长风渡》- 国风仙侠短剧（饭制）", "img": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=600&q=80", "duration": "05:40", "views": "8.2w", "model": "Hailuo 2.3", "category": "国风仙侠"},
    {"id": 5, "title": "剑气纵横三万里：水墨武侠", "img": "https://images.unsplash.com/photo-1576485290814-1c72aa4bbb8e?auto=format&fit=crop&w=600&q=80", "duration": "02:15", "views": "15.6w", "model": "Veo 2.0", "category": "国风仙侠"},
    {"id": 6, "title": "青丘狐妖：幻境唯美空镜", "img": "https://images.unsplash.com/photo-1615414050682-192a5d2109fb?auto=format&fit=crop&w=600&q=80", "duration": "01:20", "views": "3.4w", "model": "Hailuo 2.3", "category": "国风仙侠"},
    
    # 萌宠动画
    {"id": 7, "title": "《猫咪侦探局》- 萌宠悬疑剧", "img": "https://images.unsplash.com/photo-1580477667995-2b920625368a?auto=format&fit=crop&w=600&q=80", "duration": "02:30", "views": "5.6w", "model": "Veo 2.0", "category": "萌宠动画"},
    {"id": 8, "title": "柯基的奇幻太空漂流", "img": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?auto=format&fit=crop&w=600&q=80", "duration": "01:10", "views": "45.1w", "model": "Sora", "category": "萌宠动画"},
    
    # 二次元
    {"id": 9, "title": "魔法少女的终极咏唱", "img": "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=600&q=80", "duration": "03:45", "views": "11.2w", "model": "Hailuo 2.3", "category": "二次元"},
    {"id": 10, "title": "日系新海诚风：电车与黄昏", "img": "https://images.unsplash.com/photo-1494548162494-384bba4ab999?auto=format&fit=crop&w=600&q=80", "duration": "00:45", "views": "33.8w", "model": "Veo 2.0", "category": "二次元"},
    
    # 情感微短剧
    {"id": 11, "title": "《阿尔卑斯之恋》- 唯美情感短剧", "img": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=600&q=80", "duration": "01:50", "views": "9.3w", "model": "Veo 2.0", "category": "微短剧"},
    {"id": 12, "title": "霸总的秘密协议：第一集", "img": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80", "duration": "04:20", "views": "18.9w", "model": "Hailuo 2.3", "category": "微短剧"}
]

# Update tabs in HTML
tabs_html = """
            <div class="flex items-center gap-8 overflow-x-auto no-scrollbar mb-6 border-b border-gray-100 pb-3 mt-4 text-[15px]" id="categoryTabs">
                <span class="tab-item active font-bold text-gray-900 border-b-2 border-brand-500 pb-3 -mb-[14px] cursor-pointer whitespace-nowrap" data-category="推荐">🔥 热门推荐</span>
                <span class="tab-item font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap" data-category="赛博朋克">赛博朋克 <span class="text-[9px] bg-[#f3e8ff] text-[#9333ea] px-1 rounded-sm ml-0.5 border border-[#e9d5ff]">科幻</span></span>
                <span class="tab-item font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap" data-category="国风仙侠">国风仙侠</span>
                <span class="tab-item font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap" data-category="二次元">二次元</span>
                <span class="tab-item font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap" data-category="萌宠动画">萌宠动画</span>
                <span class="tab-item font-medium text-gray-500 hover:text-gray-800 pb-3 cursor-pointer whitespace-nowrap" data-category="微短剧">微短剧</span>
            </div>
"""

# Replace old tabs
html = re.sub(r'<div class="flex items-center gap-8 overflow-x-auto no-scrollbar mb-6 border-b border-gray-100 pb-3 mt-4 text-\[15px\]".*?</div>', tabs_html, html, flags=re.DOTALL)

# Empty the static showcases container and add an ID
html = re.sub(r'<div id="shotsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 pb-20">.*?</div>', '<div id="shotsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 pb-20"></div>', html, flags=re.DOTALL)


js_logic = f"""
        const showcaseData = {json.dumps(showcases)};
        
        function renderShowcases(category) {{
            const container = document.getElementById('shotsContainer');
            container.innerHTML = '';
            
            let filtered = showcaseData;
            if (category !== '推荐') {{
                filtered = showcaseData.filter(item => item.category === category);
            }}
            
            filtered.forEach(item => {{
                const card = document.createElement('div');
                card.className = "rounded-2xl overflow-hidden bg-white border border-gray-100 shadow-sm hover:shadow-md transition cursor-pointer group";
                card.innerHTML = `
                    <div class="relative w-full aspect-[4/3] overflow-hidden">
                        <img src="${{item.img}}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute bottom-2 right-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded backdrop-blur">${{item.duration}}</div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-bold text-[14px] text-gray-800 mb-1 line-clamp-1">${{item.title}}</h4>
                        <div class="flex items-center justify-between text-[11px] text-gray-500">
                            <span><i class="fa-solid fa-play text-[10px] mr-1"></i> ${{item.views}} 播放</span>
                            <span class="bg-gray-100 px-1.5 rounded">${{item.model}}</span>
                        </div>
                    </div>
                `;
                
                card.addEventListener('click', () => {{
                    document.getElementById('ideaInput').value = `以【${{item.title}}】为灵感，生成一段充满视觉张力、构图巧妙的高质量AI视频。`;
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }});
                
                container.appendChild(card);
            }});
        }}
        
        // Initial render
        renderShowcases('推荐');
        
        // Tab switching logic
        document.querySelectorAll('.tab-item').forEach(tab => {{
            tab.addEventListener('click', (e) => {{
                // Remove active classes
                document.querySelectorAll('.tab-item').forEach(t => {{
                    t.classList.remove('font-bold', 'text-gray-900', 'border-b-2', 'border-brand-500');
                    t.classList.add('font-medium', 'text-gray-500');
                }});
                // Add active classes
                const target = e.currentTarget;
                target.classList.remove('font-medium', 'text-gray-500');
                target.classList.add('font-bold', 'text-gray-900', 'border-b-2', 'border-brand-500');
                
                // Render category
                const category = target.getAttribute('data-category');
                renderShowcases(category);
            }});
        }});
"""

# Insert JS logic before closing script tag
html = html.replace("</script>\n</body>", js_logic + "\n</script>\n</body>")

with open(html_path, "w") as f:
    f.write(html)
