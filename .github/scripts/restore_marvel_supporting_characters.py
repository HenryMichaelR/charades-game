from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
if "Marvel" not in categories:
    raise SystemExit("Marvel category is missing")

other_categories = {
    name: list(words)
    for name, words in categories.items()
    if name != "Marvel"
}

marvel = list(categories["Marvel"])
original = list(marvel)

insertions = [
    ("Spider-Gwen", ["Aunt May", "Mary Jane"]),
    ("War Machine", ["Pepper Potts", "Happy Hogan"]),
    ("Captain America (Infinity War)", ["Peggy Carter"]),
]

for anchor, names in insertions:
    if anchor not in marvel:
        raise SystemExit(f"Missing insertion anchor: {anchor}")

    position = marvel.index(anchor) + 1
    for name in names:
        if name in marvel:
            continue
        marvel.insert(position, name)
        position += 1

expected = {"Aunt May", "Mary Jane", "Pepper Potts", "Happy Hogan", "Peggy Carter"}
if not expected.issubset(marvel):
    raise SystemExit("Not all supporting characters were restored")

if len(marvel) != len(original) + sum(name not in original for name in expected):
    raise SystemExit("Unexpected Marvel category size change")

normalized = [re.sub(r"[^a-z0-9]+", "", name.casefold()) for name in marvel]
if len(normalized) != len(set(normalized)):
    raise SystemExit("Marvel category contains duplicate names")

categories["Marvel"] = marvel

if {
    name: list(words)
    for name, words in categories.items()
    if name != "Marvel"
} != other_categories:
    raise SystemExit("A non-Marvel category changed unexpectedly")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print(f"Restored five recognizable Marvel supporting characters; total={len(marvel)}")
