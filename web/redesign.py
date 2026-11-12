import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    original_html = f.read()

# Extract the script tag content
script_match = re.search(r'<script>(.*?)</script>', original_html, re.DOTALL)
js_content = script_match.group(1) if script_match else ""
# Remove the tailwind config from js_content
js_content = re.sub(r'tailwind\.config\s*=\s*\{.*?\};', '', js_content, flags=re.DOTALL).strip()

new_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiseDrama - Hailuo Style</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            500: '#14b8a6', // Teal/Cyan like some modern AI tools
                            600: '#0d9488',
                        }},
                        dark: {{
                            950: '#050505',
                            900: '#121212',
                            800: '#1E1E1E',
                            700: '#2D2D2D'
                        }}
                    }},
                    fontFamily: {{
                        sans: ['Inter', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body {{ background-color: #050505; color: #E5E5E5; font-family: 'Inter', sans-serif; }}
        .glass-panel {{
            background: rgba(30, 30, 30, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .input-glow:focus-within {{
            box-shadow: 0 0 0 1px rgba(20, 184, 166, 0.5), 0 0 20px rgba(20, 184, 166, 0.1);
            border-color: rgba(20, 184, 166, 0.5);
        }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 4px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #333; border-radius: 4px; }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{ background: #555; }}
        
        .spinner {{
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body class="min-h-screen flex flex-col font-sans antialiased">
    <!-- Top Navbar -->
    <header class="h-16 border-b border-white/10 flex items-center justify-between px-6 bg-dark-950/80 backdrop-blur sticky top-0 z-50">
        <div class="flex items-center gap-3 cursor-pointer" onclick="window.location.reload()">
            <div class="text-brand-500">
                <i class="fa-solid fa-layer-group text-2xl"></i>
            </div>
            <span class="text-xl font-bold tracking-tight text-white">WiseDrama</span>
            <span class="text-[10px] uppercase bg-dark-800 text-gray-400 px-1.5 py-0.5 rounded border border-white/5 ml-1">Beta</span>
        </div>
        <nav class="hidden md:flex gap-8 text-sm font-medium text-gray-400">
            <a href="#" class="text-white">Text to Video</a>
            <a href="#" class="hover:text-white transition">Image to Video</a>
            <a href="#" class="hover:text-white transition">My Library</a>
        </nav>
        <div class="flex items-center gap-4">
            <button class="bg-white text-black hover:bg-gray-200 px-4 py-1.5 rounded font-medium text-sm transition">Login</button>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 w-full max-w-5xl mx-auto px-4 py-10 flex flex-col items-center">
        
        <h1 class="text-3xl md:text-5xl font-bold text-white mb-2 text-center">Dream it. Generate it.</h1>
        <p class="text-gray-500 mb-10 text-center">Transform your ideas into cinematic short dramas with agentic AI.</p>
        
        <!-- Input Area -->
        <div class="w-full bg-dark-900 border border-white/10 rounded-2xl p-1 input-glow transition-all duration-300 shadow-2xl">
            <textarea id="ideaInput" rows="4" class="w-full bg-transparent text-white placeholder-gray-600 p-4 outline-none resize-none text-lg custom-scrollbar" placeholder="Describe your short drama idea in detail..."></textarea>
            
            <div class="flex items-center justify-between px-4 pb-3 pt-2 border-t border-white/5 mt-2">
                <div class="flex items-center gap-4">
                    <select id="modelInput" class="bg-dark-800 text-gray-300 text-sm rounded-lg px-3 py-1.5 border border-white/5 outline-none hover:bg-dark-700 transition appearance-none cursor-pointer">
                        <option value="veo">Veo 2.0 (Google)</option>
                        <option value="hailuo">Hailuo AI</option>
                        <option value="sora">Sora (Coming Soon)</option>
                    </select>
                    
                    <div class="flex items-center gap-2 text-sm text-gray-400 bg-dark-800 px-3 py-1.5 rounded-lg border border-white/5">
                        <i class="fa-solid fa-film"></i>
                        <select id="shotsInput" class="bg-transparent outline-none text-gray-200 cursor-pointer">
                            <option value="3">3 Shots</option>
                            <option value="5">5 Shots</option>
                            <option value="10">10 Shots</option>
                        </select>
                    </div>
                </div>
                
                <div class="flex items-center gap-3">
                    <button onclick="randomIdea()" class="text-gray-500 hover:text-white transition w-8 h-8 flex items-center justify-center rounded-full hover:bg-dark-800" title="Surprise Me">
                        <i class="fa-solid fa-dice"></i>
                    </button>
                    <button id="generateBtn" onclick="startGeneration()" class="bg-brand-500 hover:bg-brand-600 text-black px-6 py-2 rounded-lg font-semibold text-sm transition flex items-center shadow-[0_0_15px_rgba(20,184,166,0.4)]">
                        <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> Generate
                    </button>
                </div>
            </div>
        </div>

        <!-- Status & Progress -->
        <div id="statusPanel" class="w-full mt-8 hidden">
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-3">
                    <div id="statusSpinner" class="spinner w-4 h-4 border-2 border-dark-700 border-l-brand-500"></div>
                    <span id="statusText" class="text-brand-500 text-sm font-medium tracking-wide uppercase">Initializing pipeline...</span>
                </div>
                <div class="flex items-center gap-4">
                    <span id="timerText" class="text-xs font-mono text-gray-500">00:00</span>
                    <button id="cancelBtn" onclick="location.reload()" class="text-xs text-gray-500 hover:text-white uppercase tracking-wider">Cancel</button>
                </div>
            </div>
            <div class="w-full h-1 bg-dark-800 rounded-full overflow-hidden">
                <div id="topProgress" class="h-full bg-brand-500 w-0 transition-all duration-500 ease-out"></div>
            </div>
            
            <!-- Terminal Log -->
            <div class="mt-4 bg-dark-900 border border-white/5 rounded-xl p-3 h-32 overflow-y-auto custom-scrollbar" id="logConsole">
                <!-- Logs will appear here -->
            </div>
        </div>

        <!-- Shots Gallery -->
        <div id="shotsContainer" class="w-full mt-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 hidden">
            <!-- Rendered shots will appear here -->
        </div>

        <!-- Final Video -->
        <div id="finalVideoContainer" class="w-full mt-10 hidden flex flex-col items-center">
            <h2 class="text-2xl font-bold text-white mb-6 flex items-center"><i class="fa-solid fa-clapperboard text-brand-500 mr-3"></i> Final Masterpiece</h2>
            <div class="w-full max-w-4xl relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl bg-black">
                <video id="finalVideoPlayer" controls class="w-full aspect-video object-contain"></video>
            </div>
            <a id="finalDownloadBtn" href="#" download class="mt-6 bg-white text-black hover:bg-gray-200 px-6 py-2.5 rounded-lg font-semibold transition flex items-center">
                <i class="fa-solid fa-download mr-2"></i> Download Final Cut
            </a>
        </div>
        
    </main>

    <script>
        {js_content}

        // Override renderShots to fit the grid layout
        function renderShots(shots) {{
            if(!shots || shots.length === 0) return;
            const container = document.getElementById('shotsContainer');
            
            // If it's the first time rendering, keep the script header if we want, or just render grid.
            // Let's clear and render purely as a grid of cards.
            container.innerHTML = '';

            shots.forEach(shot => {{
                const isDone = shot.status === 'completed';
                const isProcessing = shot.status === 'processing';
                const isFailed = shot.status === 'failed';
                
                let mediaHtml = '';
                if(isDone && shot.video_url) {{
                    mediaHtml = `
                        <video src="${{shot.video_url}}" controls loop muted class="w-full aspect-video object-cover bg-black"></video>
                        <a href="${{shot.video_url}}" target="_blank" download class="absolute top-2 right-2 bg-black/60 hover:bg-brand-500 backdrop-blur text-white w-7 h-7 flex items-center justify-center rounded transition shadow">
                            <i class="fa-solid fa-download text-[10px]"></i>
                        </a>
                    `;
                }} else if (isProcessing) {{
                    mediaHtml = `
                        <div class="w-full aspect-video bg-dark-800 flex flex-col items-center justify-center text-gray-400">
                            <div class="spinner mb-2 border-2 border-dark-600 border-l-brand-500 w-5 h-5"></div>
                            <span class="text-[10px] uppercase tracking-widest">Rendering...</span>
                        </div>
                    `;
                }} else if (isFailed) {{
                    mediaHtml = `
                        <div class="w-full aspect-video bg-red-950/20 flex flex-col items-center justify-center text-red-400">
                            <i class="fa-solid fa-xmark text-xl mb-1"></i>
                            <span class="text-[10px] uppercase tracking-widest">Failed</span>
                        </div>
                    `;
                }} else {{
                    mediaHtml = `
                        <div class="w-full aspect-video bg-dark-900/50 flex flex-col items-center justify-center text-gray-600">
                            <i class="fa-solid fa-hourglass-half text-sm mb-1 opacity-50"></i>
                            <span class="text-[9px] uppercase tracking-widest">Waiting</span>
                        </div>
                    `;
                }}

                const card = document.createElement('div');
                card.className = "bg-dark-900 border border-white/5 rounded-xl overflow-hidden hover:border-white/10 transition group flex flex-col";
                card.innerHTML = `
                    <div class="relative w-full shrink-0 border-b border-white/5">
                        ${{mediaHtml}}
                    </div>
                    <div class="p-4 flex flex-col flex-1">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Shot ${{shot.shot_number}}</span>
                        </div>
                        <p class="text-xs text-gray-300 line-clamp-3 mb-2 flex-1" title="${{shot.prompt}}">${{shot.prompt}}</p>
                        <p class="text-[10px] text-gray-500 italic">"${{shot.voiceover}}"</p>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}
        
        // Override resetUI for Hailuo style
        function resetUI() {{
            document.getElementById('generateBtn').disabled = false;
            document.getElementById('generateBtn').classList.remove('opacity-50', 'cursor-not-allowed');
            document.getElementById('generateBtn').innerHTML = '<i class="fa-solid fa-wand-magic-sparkles mr-2"></i> Generate';
        }}
    </script>
</body>
</html>
"""

with open(html_path, "w") as f:
    f.write(new_html)

print("HTML redesigned successfully.")
