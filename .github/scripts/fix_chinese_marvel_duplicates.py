from pathlib import Path

path = Path('words.js')
text = path.read_text(encoding='utf-8')
original = text

for line in [
    '    "恶名钢铁侠",\n',
    '    "浩克",\n',
]:
    if text.count(line) != 1:
        raise SystemExit(f'Expected exactly one occurrence of {line.strip()!r}, found {text.count(line)}')
    text = text.replace(line, '', 1)

if text == original:
    raise SystemExit('No changes made')

start = text.index('  "Marvel (Chinese version)": [')
end = text.index('\n  ],', start)
block = text[start:end]
assert '（' not in block and '）' not in block
assert '恶名钢铁侠' not in block
assert '\n    "浩克",' not in block
assert '    "绿巨人浩克",' in block

path.write_text(text, encoding='utf-8')
print('Removed Chinese-only Marvel variant leftovers')