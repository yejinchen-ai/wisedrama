import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# 1. Viewport Meta (prevent scaling on WeChat/mobile)
html = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">', 
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">')

# 2. Body height to 100dvh to fix Safari/WeChat bottom bar issues
html = html.replace('body class="flex h-screen', 'body class="flex flex-col md:flex-row h-[100dvh]')

# 3. Sidebar -> Hide on mobile, show on md (we'll add a mobile header instead)
html = html.replace('aside class="w-[96px]', 'aside class="hidden md:flex w-[96px]')

# Add a simple mobile header
mobile_header = """
    <!-- Mobile Header -->
    <header class="md:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-gray-100 shrink-0 z-50">
        <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-gradient-to-br from-[#15d172] to-[#0ea5e9] shadow-sm">
                <i class="fa-solid fa-dharmachakra text-white text-lg"></i>
            </div>
            <span class="font-bold text-gray-800 text-[15px]">WiseDrama</span>
        </div>
        <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
            <i class="fa-solid fa-bars text-gray-600"></i>
        </div>
    </header>
"""
html = html.replace('<!-- Main Content Area -->', mobile_header + '\n    <!-- Main Content Area -->')

# 4. Main Padding
html = html.replace('max-w-[1280px] mx-auto px-10 py-8', 'max-w-[1280px] mx-auto px-4 py-4 md:px-10 md:py-8')

# 5. Top Tabs (Create Video, etc) - scrollable on mobile
html = html.replace('class="flex items-center gap-4 mb-10 w-full"', 'class="flex items-center gap-3 md:gap-4 mb-6 md:mb-10 w-full overflow-x-auto no-scrollbar pb-2"')
html = html.replace('w-[240px]', 'w-auto md:w-[240px] whitespace-nowrap shrink-0 px-5 md:px-8')

# 6. Hero Title size
html = html.replace('text-[34px]', 'text-[28px] md:text-[34px]')

# 7. Input Box Layout (flex-col on mobile)
html = html.replace('<div class="flex gap-4 mb-4 min-h-[140px]">', '<div class="flex flex-col md:flex-row gap-4 mb-4 min-h-[100px] md:min-h-[140px]">')
# Frame upload container
html = html.replace('<div class="flex items-center gap-3 shrink-0 ml-1 mt-1">', '<div class="flex items-center justify-center md:justify-start gap-3 shrink-0 md:ml-1 md:mt-1 order-2 md:order-1">')
# Textarea container
html = html.replace('<div class="flex-1 ml-2">', '<div class="flex-1 md:ml-2 order-1 md:order-2 h-[80px] md:h-auto">')

# 8. Bottom Toolbar (wrap on mobile)
html = html.replace('<div class="flex items-center justify-between">', '<div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 md:gap-0">')
html = html.replace('<div class="flex items-center gap-2.5">', '<div class="flex items-center justify-between md:justify-start gap-2 md:gap-2.5 w-full md:w-auto">')
html = html.replace('<div class="flex items-center gap-5">', '<div class="flex items-center justify-between md:justify-end gap-5 w-full md:w-auto mt-2 md:mt-0">')
html = html.replace('px-7 py-2.5', 'px-5 py-2 md:px-7 md:py-2.5 flex-1 md:flex-none')

# 9. Horizontal Banners (stack on mobile)
html = html.replace('<div class="flex flex-col md:flex-row gap-5 mb-10 w-full">', '<div class="flex flex-col md:flex-row gap-3 md:gap-5 mb-6 md:mb-10 w-full">')
html = html.replace('h-[160px]', 'h-[120px] md:h-[160px]')

# 10. Large Modal adjustments for mobile
# Modal container
html = html.replace('style="display: none; width: calc(100% - 96px);"', 'style="display: none;" class="w-full md:w-[calc(100%-96px)]"')
# Find the exact modal div and update classes
old_modal_start = r'<div id="videoModal" class="fixed inset-y-0 right-0 z-\[100\] bg-white/95 backdrop-blur-3xl flex transition-all duration-500 transform translate-x-full opacity-0" style="display: none; width: calc\(100% - 96px\);">'
new_modal_start = r'<div id="videoModal" class="fixed inset-y-0 right-0 w-full md:w-[calc(100%-96px)] z-[100] bg-white/95 backdrop-blur-3xl flex flex-col md:flex-row transition-all duration-500 transform translate-x-full opacity-0" style="display: none;">'
html = re.sub(old_modal_start, new_modal_start, html)

# Modal close button
html = html.replace('absolute top-6 right-8', 'absolute top-3 right-3 md:top-6 md:right-8 bg-black/20 md:bg-transparent rounded-full md:rounded-none text-white md:text-gray-400')

# Modal layout inside (flex-col on mobile)
html = html.replace('<div class="flex w-full h-full p-10 gap-10">', '<div class="flex flex-col md:flex-row w-full h-full p-0 md:p-10 gap-0 md:gap-10 relative">')

# Left video player
html = html.replace('class="flex-1 flex flex-col justify-center items-center relative h-full"', 'class="w-full h-[40vh] md:flex-1 flex flex-col justify-center items-center relative md:h-full bg-black shrink-0"')
html = html.replace('rounded-3xl', 'rounded-none md:rounded-3xl')

# Right info panel
html = html.replace('class="w-[420px] flex flex-col h-full pt-4 pr-4 shrink-0"', 'class="w-full md:w-[420px] flex flex-col flex-1 pt-6 px-5 md:px-0 md:pr-4 shrink-0 overflow-y-auto pb-6"')

# Showcase Grid
html = html.replace('grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4', 'grid-cols-2 md:grid-cols-3 lg:grid-cols-4')
# Card paddings for mobile
html = html.replace('class="p-3"', 'class="p-2.5 md:p-3"')
html = html.replace('text-[14px]', 'text-[12px] md:text-[14px]')
html = html.replace('text-[11px]', 'text-[9px] md:text-[11px]')

with open(html_path, "w") as f:
    f.write(html)

print("Mobile optimization script applied.")
