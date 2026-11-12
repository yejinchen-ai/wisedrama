import re

html_path = "/home/jerry/codebase/wisedrama/web/index.html"
with open(html_path, "r") as f:
    html = f.read()

# Hongguo (Red Fruit) Short Drama App uses a striking Red-to-Orange gradient identity.
# Main color: Deep Red to Vibrant Orange.
# Backgrounds: Very dark grays or clean whites depending on mode.
# We will replace the "Qishui Neon Green" (#15d172) with "Hongguo Red/Orange"
# Primary Red: #F5303D (or #ff2a2a)
# Secondary Orange/Coral: #FF6B50 (or #ff7340)

# 1. Update Tailwind config
old_tw_config = """        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            500: '#15d172', // Purple for the main brand color
                            600: '#10b260',
                        }
                    }
                }
            }
        }"""
new_tw_config = """        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            500: '#ff2a2a', // Hongguo Red
                            600: '#e01e1e', // Darker Red for hover
                        }
                    }
                }
            }
        }"""
html = html.replace(old_tw_config, new_tw_config)

# 2. Update CSS vars/custom styling
html = html.replace('#15d172', '#ff2a2a') # Base color
html = html.replace('#10b260', '#ff6b50') # Hover/Secondary color -> make it gradient-friendly orange
html = html.replace('rgba(21, 209, 114', 'rgba(255, 42, 42') # Box shadows
html = html.replace('rgba(21,209,114', 'rgba(255,42,42')
html = html.replace('bg-[#eafff2]', 'bg-[#fff0f0]') # Light background for tags
html = html.replace('border-[#bbf7d0]', 'border-[#ffd6d6]') # Light border for tags
html = html.replace('text-[#10b260]', 'text-[#ff2a2a]') # Text color in tags

# 3. Update Sidebar Logo Gradient
# from from-[#15d172] via-[#059669] to-[#0ea5e9]
html = html.replace('from-[#ff2a2a] via-[#059669] to-[#0ea5e9]', 'from-[#ff2a2a] via-[#ff5b5b] to-[#ff8c42]') # This might have been partially replaced above. Let's do regex.
html = re.sub(r'from-\[#[0-9a-fA-F]+\] via-\[#[0-9a-fA-F]+\] to-\[#[0-9a-fA-F]+\]', 'from-[#ff2a2a] via-[#ff4d4d] to-[#ff7a33]', html)

# 4. Slogan gradient
# from-[#10b260] to-[#15d172] -> Already partially replaced to from-[#ff6b50] to-[#ff2a2a]
# Let's ensure the slogan gradient pops like the Hongguo app.
html = html.replace('from-[#ff6b50] to-[#ff2a2a]', 'from-[#ff7340] to-[#ff2a2a]')

# 5. Buttons and Accents
# The top buttons were `bg-[#15d172]`, now `bg-[#ff2a2a]`. That's good.
# Let's check the slider track background gradient.
# `background: linear-gradient(to right, #15d172 10%, #f3f4f6 10%);`
# We want it to be a fiery red-orange gradient.
html = html.replace('accent-[#15d172]', 'accent-[#ff2a2a]')
# The inline JS updates the slider background, we need to fix it there.
html = html.replace('#15d172 ${percentage}%', '#ff2a2a ${percentage}%')


with open(html_path, "w") as f:
    f.write(html)
