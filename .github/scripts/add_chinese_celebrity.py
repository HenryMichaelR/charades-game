from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

chinese_celebrities = [
    "成龙", "周润发", "周星驰", "刘德华", "梁朝伟", "张学友", "黎明", "郭富城", "张国荣", "梅艳芳",
    "林青霞", "张曼玉", "王祖贤", "关之琳", "吴孟达", "古天乐", "郑伊健", "谢霆锋", "吴彦祖", "陈冠希",
    "梁家辉", "刘青云", "张家辉", "任达华", "曾志伟", "黄秋生", "陈奕迅", "容祖儿", "邓紫棋", "杨千嬅",
    "郑秀文", "陈慧琳", "莫文蔚", "王菲", "林忆莲", "许冠杰", "谭咏麟", "张敬轩", "黄家驹", "刘嘉玲",
    "张柏芝", "朱茵", "蔡少芬", "袁咏仪", "陈小春", "甄子丹", "王家卫", "徐克", "吴宇森", "杜琪峰",
    "陈可辛", "尔冬升", "许鞍华", "黄子华", "林峯", "张卫健", "李若彤", "佘诗曼", "郑少秋", "汪明荃",
    "周杰伦", "蔡依林", "王力宏", "张惠妹", "罗志祥", "王心凌", "杨丞琳", "萧敬腾", "田馥甄", "林志玲",
    "林志颖", "林心如", "霍建华", "陈乔恩", "陈妍希", "彭于晏", "赵又廷", "阮经天", "桂纶镁", "张震",
    "苏有朋", "吴奇隆", "费玉清", "庾澄庆", "吴宗宪", "徐熙媛", "徐熙娣", "蔡康永", "李安", "侯孝贤",
    "欧阳娜娜", "张信哲", "任贤齐", "张韶涵", "陶喆", "刘若英", "林俊杰", "孙燕姿", "梁静茹", "周华健",
    "李宗盛", "罗大佑", "伍佰", "齐秦", "陈绮贞", "潘玮柏", "阿信", "赵薇", "章子怡", "巩俐",
    "李连杰", "周迅", "范冰冰", "李冰冰", "黄晓明", "杨幂", "刘亦菲", "胡歌", "陈坤", "邓超",
    "孙俪", "吴京", "沈腾", "马丽", "黄渤", "徐峥", "王宝强", "贾玲", "葛优", "陈道明",
    "姜文", "张国立", "陈宝国", "张艺谋", "陈凯歌", "冯小刚", "宁浩", "易烊千玺", "王一博", "肖战",
    "杨洋", "李现", "朱一龙", "白敬亭", "张艺兴", "鹿晗", "王俊凯", "王源", "迪丽热巴", "赵丽颖",
    "杨紫", "刘诗诗", "唐嫣", "倪妮", "杨颖", "周冬雨", "舒淇", "汤唯", "雷佳音", "张译",
    "黄轩", "张若昀", "刘欢", "那英", "韩红", "汪峰", "李宇春", "周深", "华晨宇", "刀郎",
    "张杰", "朴树", "许巍", "毛不易", "薛之谦", "凤凰传奇", "单依纯", "时代少年团", "李荣浩", "张靓颖"
]


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value)


def contains_chinese(value: str) -> bool:
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", value))


if len(chinese_celebrities) != 180:
    raise SystemExit(f"Expected 180 names, found {len(chinese_celebrities)}")

keys = [normalized(name) for name in chinese_celebrities]
if len(keys) != len(set(keys)):
    raise SystemExit("Chinese Celebrity list contains duplicate names")

for name in chinese_celebrities:
    if not contains_chinese(name):
        raise SystemExit(f"Name does not contain Chinese characters: {name}")
    if re.search(r"[A-Za-z]", name):
        raise SystemExit(f"Name contains Latin letters: {name}")

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
other_categories = {
    name: list(words)
    for name, words in categories.items()
    if name != "Chinese Celebrity"
}

categories["Chinese Celebrity"] = chinese_celebrities

if {
    name: list(words)
    for name, words in categories.items()
    if name != "Chinese Celebrity"
} != other_categories:
    raise SystemExit("An existing category changed unexpectedly")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print("Added Chinese Celebrity with 180 recognizable Chinese-language names")
