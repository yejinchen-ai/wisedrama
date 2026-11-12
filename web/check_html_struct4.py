html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's inspect the area around the script tag at 16141
print("=== MIDDLE OF FILE ===")
print(html[16100:16200])

