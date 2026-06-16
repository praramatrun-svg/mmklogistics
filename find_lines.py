with open('super.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'tab-drv-list' in line:
        print(f'{i+1}: {line.strip()}')
