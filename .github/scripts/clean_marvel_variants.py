from pathlib import Path
import re

path = Path('words.js')
text = path.read_text(encoding='utf-8')
original = text


def parse_category(source: str, name: str):
    marker = f'  "{name}": ['
    start = source.index(marker)
    body_start = start + len(marker)
    end = source.index('\n  ],', body_start)
    body = source[body_start:end]
    items = re.findall(r'^    "(.*)"(?:,)?$', body, flags=re.M)
    return start, body_start, end, items


def render(items):
    return '\n' + ',\n'.join(f'    "{item}"' for item in items)


def dedupe(items):
    seen = set()
    out = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out

english_special = {
    'Spider-Man (Miles Morales)': 'Miles Morales',
    'Wolverine (X-23)': 'X-23',
    'Black Widow (Claire Voyant)': 'Claire Voyant',
}

chinese_special = {
    '蜘蛛侠（迈尔斯·莫拉莱斯）': '迈尔斯·莫拉莱斯',
    '金刚狼（X-23）': 'X-23',
    '黑寡妇（克莱尔·瓦扬）': '克莱尔·瓦扬',
}


def clean_english(items):
    cleaned = []
    for item in items:
        if item in english_special:
            item = english_special[item]
        else:
            item = re.sub(r'\s*\([^)]*\)\s*$', '', item).strip()
        cleaned.append(item)
    return dedupe(cleaned)


def clean_chinese(items):
    cleaned = []
    for item in items:
        if item in chinese_special:
            item = chinese_special[item]
        else:
            item = re.sub(r'（[^）]*）\s*$', '', item).strip()
        cleaned.append(item)
    return dedupe(cleaned)

# Replace later category first so character offsets for Marvel stay valid.
_, body_start, end, chinese_items = parse_category(text, 'Marvel (Chinese version)')
new_chinese = clean_chinese(chinese_items)
text = text[:body_start] + render(new_chinese) + text[end:]

_, body_start, end, english_items = parse_category(text, 'Marvel')
new_english = clean_english(english_items)
text = text[:body_start] + render(new_english) + text[end:]

if text == original:
    raise SystemExit('No changes made')

# Validate requested cleanup.
_, _, _, marvel = parse_category(text, 'Marvel')
_, _, _, marvel_cn = parse_category(text, 'Marvel (Chinese version)')

assert all('(' not in item and ')' not in item for item in marvel), marvel
assert all('（' not in item and '）' not in item for item in marvel_cn), marvel_cn
assert len(marvel) == len(set(x.casefold() for x in marvel))
assert len(marvel_cn) == len(set(x.casefold() for x in marvel_cn))

for required in ['Spider-Man', 'Miles Morales', 'X-23', 'Iron Man', 'Captain America', 'Thor', 'Hulk', 'Black Panther', 'Captain Marvel', 'Cyclops', 'Claire Voyant']:
    assert required in marvel, required

for forbidden in ['Spider-Man (Stark Enhanced)', 'Iron Man (Infinity War)', 'Thor (Ragnarok)', 'Black Panther (Civil War)', 'Magneto (House of X)']:
    assert forbidden not in marvel, forbidden

for required in ['蜘蛛侠', '迈尔斯·莫拉莱斯', 'X-23', '钢铁侠', '美国队长', '雷神索尔', '绿巨人浩克', '黑豹', '惊奇队长', '镭射眼', '克莱尔·瓦扬']:
    assert required in marvel_cn, required

for forbidden in ['蜘蛛侠（史塔克加强版）', '钢铁侠（无限战争）', '雷神索尔（诸神黄昏）', '黑豹（内战）', '万磁王（X阵营）']:
    assert forbidden not in marvel_cn, forbidden

path.write_text(text, encoding='utf-8')
print(f'Marvel: {len(english_items)} -> {len(new_english)}')
print(f'Marvel Chinese: {len(chinese_items)} -> {len(new_chinese)}')