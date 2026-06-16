import os

files = ['app.js', 'admin.html', 'driver.html', 'super.html']
output = []

for filename in files:
    output.append(f"====== FILE: {filename} ======")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if 'motorcycle' in line.lower() or 'จักรยานยนต์' in line:
            output.append(f"{idx+1}: {line.strip()}")
    output.append("")

with open('motorcycle_search_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(output))
print("Done! Saved to motorcycle_search_results.txt")
