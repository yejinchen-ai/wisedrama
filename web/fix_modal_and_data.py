import re
import json

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Fix the modal CSS so it's truly hidden
# The issue was 'hidden flex' in tailwind makes it flex (visible) and breaks 'hidden'
html = html.replace('class="fixed inset-0 bg-black/95 z-[100] hidden flex flex-col', 'class="fixed inset-0 bg-black/95 z-[100] hidden flex-col')
html = html.replace("modal.classList.remove('hidden');", "modal.classList.remove('hidden');\n            modal.classList.add('flex');")
html = html.replace("modal.classList.add('hidden');", "modal.classList.remove('flex');\n                modal.classList.add('hidden');")

# Expanded Showcase Data
expanded_data = [
    # 赛博朋克
    {"id": 1, "title": "《霓虹深渊》- 赛博朋克微短剧", "img": "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4", "duration": "03:12", "views": "12.5w", "model": "Veo 2.0", "category": "赛博朋克"},
    {"id": 2, "title": "夜之城：失控的AI仿生人", "img": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", "duration": "01:45", "views": "8.9w", "model": "Hailuo 2.3", "category": "赛博朋克"},
    {"id": 3, "title": "未来赛车：光速漂移", "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", "duration": "00:58", "views": "21.3w", "model": "Sora", "category": "赛博朋克"},
    {"id": 13, "title": "赛博艺妓的复仇", "img": "https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4", "duration": "02:20", "views": "14.2w", "model": "Veo 2.0", "category": "赛博朋克"},
    {"id": 14, "title": "霓虹雨夜：骇客帝国", "img": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", "duration": "04:15", "views": "19.8w", "model": "Hailuo 2.3", "category": "赛博朋克"},
    
    # 国风仙侠
    {"id": 4, "title": "《长风渡》- 国风仙侠短剧（饭制）", "img": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4", "duration": "05:40", "views": "8.2w", "model": "Hailuo 2.3", "category": "国风仙侠"},
    {"id": 5, "title": "剑气纵横三万里：水墨武侠", "img": "https://images.unsplash.com/photo-1576485290814-1c72aa4bbb8e?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4", "duration": "02:15", "views": "15.6w", "model": "Veo 2.0", "category": "国风仙侠"},
    {"id": 6, "title": "青丘狐妖：幻境唯美空镜", "img": "https://images.unsplash.com/photo-1615414050682-192a5d2109fb?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", "duration": "01:20", "views": "3.4w", "model": "Hailuo 2.3", "category": "国风仙侠"},
    {"id": 15, "title": "大唐盛世：长安十二时辰", "img": "https://images.unsplash.com/photo-1582234372722-50d7ccc30ebd?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", "duration": "03:45", "views": "28.5w", "model": "Sora", "category": "国风仙侠"},
    {"id": 16, "title": "山海经：神兽降临", "img": "https://images.unsplash.com/photo-1614531341773-3bff8b7cb3fc?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4", "duration": "02:50", "views": "11.1w", "model": "Veo 2.0", "category": "国风仙侠"},
    
    # 二次元
    {"id": 9, "title": "魔法少女的终极咏唱", "img": "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4", "duration": "03:45", "views": "11.2w", "model": "Hailuo 2.3", "category": "二次元"},
    {"id": 10, "title": "日系新海诚风：电车与黄昏", "img": "https://images.unsplash.com/photo-1494548162494-384bba4ab999?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", "duration": "00:45", "views": "33.8w", "model": "Veo 2.0", "category": "二次元"},
    {"id": 17, "title": "机甲少女觉醒：破晓之战", "img": "https://images.unsplash.com/photo-1560972550-aba3456b5564?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", "duration": "04:30", "views": "42.1w", "model": "Hailuo 2.3", "category": "二次元"},
    {"id": 18, "title": "异世界转生：史莱姆大魔王", "img": "https://images.unsplash.com/photo-1612404730960-5c71577fca11?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4", "duration": "02:15", "views": "18.7w", "model": "Veo 2.0", "category": "二次元"},
    
    # 萌宠动画
    {"id": 7, "title": "《猫咪侦探局》- 萌宠悬疑剧", "img": "https://images.unsplash.com/photo-1580477667995-2b920625368a?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4", "duration": "02:30", "views": "5.6w", "model": "Veo 2.0", "category": "萌宠动画"},
    {"id": 8, "title": "柯基的奇幻太空漂流", "img": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", "duration": "01:10", "views": "45.1w", "model": "Sora", "category": "萌宠动画"},
    {"id": 19, "title": "柴犬武士：决战紫禁之巅", "img": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", "duration": "03:05", "views": "31.2w", "model": "Hailuo 2.3", "category": "萌宠动画"},
    {"id": 20, "title": "胖橘猫的偷吃大作战", "img": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4", "duration": "01:50", "views": "26.4w", "model": "Veo 2.0", "category": "萌宠动画"},
    
    # 微短剧
    {"id": 11, "title": "《阿尔卑斯之恋》- 唯美情感短剧", "img": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4", "duration": "01:50", "views": "9.3w", "model": "Veo 2.0", "category": "微短剧"},
    {"id": 12, "title": "霸总的秘密协议：第一集", "img": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", "duration": "04:20", "views": "18.9w", "model": "Hailuo 2.3", "category": "微短剧"},
    {"id": 21, "title": "重生之我才是真少爷", "img": "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", "duration": "05:15", "views": "105.2w", "model": "Hailuo 2.3", "category": "微短剧"},
    {"id": 22, "title": "逃离循环：时间囚徒", "img": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4", "duration": "03:40", "views": "34.6w", "model": "Sora", "category": "微短剧"},
    {"id": 23, "title": "豪门恩怨：婆媳风云", "img": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=600&q=80", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4", "duration": "02:55", "views": "56.8w", "model": "Veo 2.0", "category": "微短剧"}
]

# Update showcaseData JSON in JS safely
html = re.sub(r'const showcaseData = \[.*?\];', lambda m: f'const showcaseData = {json.dumps(expanded_data, ensure_ascii=False)};', html)

with open(html_path, "w") as f:
    f.write(html)
