import re

files = ['driver.html', 'super.html']
output_lines = []

targets = ['drivers', 'maxWeight', 'weight', 'capacity', 'assignedDriverId']

for filename in files:
    output_lines.append(f"====== FILE: {filename} ======")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()
    for target in targets:
        output_lines.append(f"=== Matches for '{target}' ===")
        matches = []
        for idx, line in enumerate(lines):
            if target.lower() in line.lower():
                matches.append((idx + 1, line.strip()))
        for line_num, text in matches:
            output_lines.append(f"{line_num}: {text}")
        output_lines.append("")

with open('search_all_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(output_lines))
print("Done! Saved to search_all_results.txt")
