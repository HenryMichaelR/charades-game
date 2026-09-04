from pathlib import Path
import json
import re

path = Path("words.js")
text = path.read_text(encoding="utf-8")

MARVEL_CN = [
    "蜘蛛侠","蜘蛛侠（迈尔斯·莫拉莱斯）","蜘蛛格温","梅姨","玛丽·简","蜘蛛侠（史塔克加强版）","蜘蛛侠2099","蜘蛛侠（潜行战衣）","蜘蛛猪侠","蛛丝","蝎子","斑点","钢铁侠","钢铁侠（无限战争）","恶名钢铁侠","美国队长","美国队长（无限战争）","佩吉·卡特","雷神索尔","雷神索尔（诸神黄昏）","绿巨人浩克","浩克（诸神黄昏）","不朽浩克","黑寡妇","黑寡妇（致命起源）","鹰眼","黑豹","黑豹（内战）","奇异博士","猩红女巫","幻视","蚁人","黄蜂女","惊奇队长（电影版）","猎鹰","冬日战士","战争机器","佩珀·波茨","哈皮·霍根","尼克·弗瑞","尚气","女浩克","卢克·凯奇","夜魔侠","夜魔侠（地狱厨房）","惩罚者","刀锋战士","月光骑士","幽灵骑士","死侍","金刚狼","金刚狼（X-23）","金刚狼（武器X）","老年罗根","X教授","万磁王","万磁王（X阵营）","暴风女","镭射眼（蓝队）","琴·格蕾","凤凰","艾玛·弗斯特","野兽","小淘气","牌皇","夜行者","钢力士","冰人","大天使","灵蝶","毕肖普","电索","多米诺","天启","纳摩","快银","星爵","卡魔拉","德拉克斯","火箭浣熊","格鲁特","格鲁特王","星云","螳螂女","亚当术士","毒液","屠杀","反毒液","纳尔","银影侠","海格力斯","亥伯龙","美杜莎","黑蝠王","亡刃将军","暗夜比邻星","宇宙恶灵骑士","屠神者格尔","加兰","奥丁","海拉","罗南","毁灭博士","洛基","魔术女","黑寡妇（克莱尔·瓦扬）","红坦克","多玛姆","莫度","墨菲斯托","断头台","至尊共生体","蒂格拉","王","阿美莉卡·查韦斯","巫术","吸收人","魅惑魔女","库沙拉","暗夜狼人","神奇先生","隐形女","霹雳火","石头人","章鱼博士","绿魔","秃鹫","神秘客","金并","靶眼","猎人克莱文","黑猫","凯特·毕肖普","杀手猴","克尔芒戈","科格","格温扑","埃贡","奥创","机械卫兵","宁录","术士","终极哨兵","潘妮·帕克","舒莉","幽灵","反浩克装甲","灭霸","红骷髅","憎恶","哨兵","虚无","电光人","沙人","犀牛人","征服者康","勇度","奥科耶","姆巴库","银貂"
]

DISNEY_CN = [
    "米奇","米妮","唐老鸭","黛丝","高飞","布鲁托","奇奇","蒂蒂","白雪公主","邪恶皇后","灰姑娘","仙女教母","白马王子","爱洛","玛琳菲森","皮诺丘","吉明尼蟋蟀","小飞象","小鹿斑比","爱丽丝","疯帽子","柴郡猫","彼得·潘","奇妙仙子","胡克船长","小熊维尼","跳跳虎","屹耳","小猪","爱丽儿","塞巴斯丁","小比目鱼","乌苏拉","贝儿","野兽","加斯顿","卢米亚","阿拉丁","茉莉","精灵","贾方","阿布","辛巴","娜娜","木法沙","刀疤","丁满","彭彭","拉飞奇","宝嘉康蒂","花木兰","木须龙","海格力斯","哈迪斯","泰山","史迪奇","莉萝","库伊拉","杰克·斯派洛","蒂安娜","纳文王子","乐佩","弗林·莱德","葛朵妈妈","艾莎","安娜","雪宝","克斯托夫","斯特","莫阿娜","毛伊","米拉贝","布鲁诺","路易莎","大白","拉尔夫","云妮洛普","兔朱迪","狐尼克","胡迪","巴斯光年","翠丝","抱抱龙","蛋头先生","尼莫","逗逗","马林","苏利文（毛怪）","大眼仔","闪电麦坤","板牙","小米","瓦力","伊娃","超能先生","超能太太","巴小倩","巴小飞","巴小杰","衣夫人","乐乐","忧忧","米格","卡尔·费迪逊","小罗","梅莉达"
]


def category_array_bounds(source, name):
    needle = f'  {json.dumps(name, ensure_ascii=False)}: ['
    start = source.index(needle)
    open_index = source.index('[', start)
    depth = 0
    in_string = False
    escaped = False
    for i in range(open_index, len(source)):
        ch = source[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                return open_index, i
    raise RuntimeError(f"Could not find end of {name}")


def get_category(source, name):
    start, end = category_array_bounds(source, name)
    return json.loads(source[start:end + 1])


def add_after(source, source_name, new_name, values):
    _, end = category_array_bounds(source, source_name)
    rendered = ',\n  ' + json.dumps(new_name, ensure_ascii=False) + ': [\n'
    rendered += ',\n'.join('    ' + json.dumps(v, ensure_ascii=False) for v in values)
    rendered += '\n  ]'
    return source[:end + 1] + rendered + source[end + 1:]

for name in ("Marvel (Chinese version)", "Disney (Chinese version)"):
    if f'"{name}"' in text:
        raise SystemExit(f"{name} already exists")

marvel_original = get_category(text, "Marvel")
disney_original = get_category(text, "Disney")

assert len(marvel_original) == 160, len(marvel_original)
assert len(disney_original) == 106, len(disney_original)
assert marvel_original[0] == "Spider-Man" and marvel_original[-1] == "Silver Sable"
assert disney_original[0] == "Mickey Mouse" and disney_original[-1] == "Merida"
assert len(MARVEL_CN) == len(marvel_original)
assert len(DISNEY_CN) == len(disney_original)
assert len(set(MARVEL_CN)) == len(MARVEL_CN)
assert len(set(DISNEY_CN)) == len(DISNEY_CN)
assert all(re.search(r'[\u4e00-\u9fff]', value) for value in MARVEL_CN)
assert all(re.search(r'[\u4e00-\u9fff]', value) for value in DISNEY_CN)

text = add_after(text, "Marvel", "Marvel (Chinese version)", MARVEL_CN)
text = add_after(text, "Disney", "Disney (Chinese version)", DISNEY_CN)

assert get_category(text, "Marvel") == marvel_original
assert get_category(text, "Disney") == disney_original
assert get_category(text, "Marvel (Chinese version)") == MARVEL_CN
assert get_category(text, "Disney (Chinese version)") == DISNEY_CN

path.write_text(text, encoding="utf-8")
print(f"Added {len(MARVEL_CN)} Marvel and {len(DISNEY_CN)} Disney Mainland Chinese prompts")
