html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Let's inspect the end of the file.
print("=== END OF FILE ===")
print(html[-1000:])
