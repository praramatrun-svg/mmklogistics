import re
import sys

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

targets = ['tab-drivers', 'driverTable', 'driverList', 'renderDrivers', 'upload', 'excel', 'import', 'weight', 'capacity', 'optimize', 'route', 'swap', 'change', 'assign']
output_lines = []

for target in targets:
    output_lines.append(f"=== Matches for '{target}' ===")
    matches = []
    for idx, line in enumerate(lines):
        if target.lower() in line.lower():
            matches.append((idx + 1, line.strip()))
    for line_num, text in matches:
        output_lines.append(f"{line_num}: {text}")
    output_lines.append("")

with open('search_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(output_lines))
print("Done! Saved to search_results.txt")
