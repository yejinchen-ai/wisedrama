html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Cleanly remove the block around line 51 that has `);`
# Let's find: `setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);\n        }\n\n);\n        }`
# And replace with `setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);\n        }`

html = html.replace("""setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);
        }
);
        }""", """setTimeout(() => ideaInput.parentElement.classList.remove('ring-2', 'ring-[#15d172]'), 1500);
        }""")

with open(html_path, "w") as f:
    f.write(html)
