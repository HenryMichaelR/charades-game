from pathlib import Path
import json

path = Path('words.js')
text = path.read_text(encoding='utf-8')

category_name = '华语电影'
if f'  "{category_name}": [' in text:
    raise SystemExit(f'{category_name} already exists')

movies = [
    "霸王别姬","无间道","无间道2","英雄本色","喋血双雄","纵横四海","辣手神探","枪火","暗战","黑社会",
    "窃听风云","寒战","拆弹专家","怒火·重案","九龙城寨之围城","警察故事","警察故事2","警察故事3：超级警察","红番区","醉拳",
    "醉拳2","A计划","功夫","少林足球","喜剧之王","食神","唐伯虎点秋香","九品芝麻官","国产凌凌漆","逃学威龙",
    "武状元苏乞儿","审死官","家有喜事","大话西游之月光宝盒","大话西游之大圣娶亲","赌神","赌侠","鹿鼎记","整蛊专家","回魂夜",
    "倩女幽魂","青蛇","黄飞鸿","黄飞鸿之二：男儿当自强","新龙门客栈","东方不败","笑傲江湖","东邪西毒","一代宗师","卧虎藏龙",
    "重庆森林","花样年华","春光乍泄","阿飞正传","旺角卡门","甜蜜蜜","胭脂扣","投名状","门徒","桃姐",
    "岁月神偷","志明与春娇","孤男寡女","瘦身男女","麦兜故事","十月围城","新警察故事","无双","少林寺","叶问",
    "叶问2","杀破狼","导火线","扫毒","追龙","春娇与志明","破·地狱",
    "饮食男女","喜宴","推手","一一","牯岭街少年杀人事件","海角七号","那些年，我们一起追的女孩","我的少女时代","不能说的秘密","艋舺",
    "赛德克·巴莱","听说","蓝色大门","阳光普照","返校","刻在你心底的名字","周处除三害","想见你","当男人恋爱时",
    "活着","红高粱","大红灯笼高高挂","秋菊打官司","有话好好说","英雄","十面埋伏","满城尽带黄金甲","山楂树之恋","归来",
    "影","悬崖之上","狙击手","第二十条","唐山大地震","集结号","芳华","一九四二","甲方乙方","手机",
    "天下无贼","非诚勿扰","让子弹飞","鬼子来了","阳光灿烂的日子","邪不压正","疯狂的石头","疯狂的赛车","无人区","心花路放",
    "我不是药神","人在囧途","泰囧","西虹市首富","夏洛特烦恼","羞羞的铁拳","独行月球","飞驰人生","飞驰人生2","你好，李焕英",
    "热辣滚烫","抓娃娃","年会不能停！","好东西","消失的她","孤注一掷","误杀","默杀","唐人街探案","唐人街探案2",
    "唐人街探案3","战狼","战狼2","流浪地球","流浪地球2","红海行动","湄公河行动","长津湖","八佰","中国机长",
    "夺冠","我和我的祖国","我和我的家乡","封神第一部：朝歌风云","满江红","长安三万里","西游记之大圣归来","哪吒之魔童降世","哪吒之魔童闹海","姜子牙",
    "大鱼海棠","白蛇：缘起","罗小黑战记","送你一朵小红花","人生大事","少年的你","七月与安生","后来的我们","前任3：再见前任","致我们终将逝去的青春",
    "北京遇上西雅图","失恋33天","无名之辈","扬名立万","爱情神话"
]

if len(movies) != 181:
    raise SystemExit(f'Expected 181 films, got {len(movies)}')
if len(set(movies)) != len(movies):
    raise SystemExit('Duplicate movie titles found')
if not all(any('\u4e00' <= ch <= '\u9fff' for ch in title) for title in movies):
    raise SystemExit('Every movie title must contain Chinese characters')

lines = [f'  "{category_name}": [']
for i, title in enumerate(movies):
    comma = ',' if i < len(movies) - 1 else ''
    lines.append(f'    {json.dumps(title, ensure_ascii=False)}{comma}')
lines.append('  ],')
block = '\n'.join(lines) + '\n'

marker = '  "Celebrity": ['
if marker not in text:
    raise SystemExit('Celebrity marker not found')

text = text.replace(marker, block + marker, 1)
path.write_text(text, encoding='utf-8')
print(f'Added {category_name}: {len(movies)} films')
