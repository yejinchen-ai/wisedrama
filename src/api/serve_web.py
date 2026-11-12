import re
file_path = "/home/jerry/codebase/wisedrama/src/api/server.py"
with open(file_path, "r") as f:
    content = f.read()

if "from fastapi.responses import FileResponse" not in content:
    content = content.replace("from fastapi.staticfiles import StaticFiles", "from fastapi.staticfiles import StaticFiles\nfrom fastapi.responses import FileResponse")

if 'app.mount("/videos"' in content and '@app.get("/")' not in content:
    route = """
@app.get("/")
async def serve_index():
    return FileResponse(str(BASE_DIR / "web" / "index.html"))

# We also mount web directory just in case there are static assets in it later
# app.mount("/web", StaticFiles(directory=str(BASE_DIR / "web")), name="web")
"""
    content = content.replace('app.mount("/videos", StaticFiles(directory=str(PUBLIC_DIR)), name="videos")', 'app.mount("/videos", StaticFiles(directory=str(PUBLIC_DIR)), name="videos")' + route)

with open(file_path, "w") as f:
    f.write(content)
