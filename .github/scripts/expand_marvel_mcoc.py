from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

marvel = [
    "Spider-Man",
    "Spider-Man (Miles Morales)",
    "Spider-Gwen",
    "Spider-Man (Stark Enhanced)",
    "Spider-Man 2099",
    "Spider-Man (Stealth Suit)",
    "Spider-Ham",
    "Silk",
    "Scorpion",
    "Spot",
    "Iron Man",
    "Iron Man (Infinity War)",
    "Iron Man (Infamous)",
    "Captain America",
    "Captain America (Infinity War)",
    "Thor",
    "Thor (Ragnarok)",
    "Hulk",
    "Hulk (Ragnarok)",
    "Immortal Hulk",
    "Black Widow",
    "Black Widow (Deadly Origin)",
    "Hawkeye",
    "Black Panther",
    "Black Panther (Civil War)",
    "Doctor Strange",
    "Scarlet Witch",
    "Vision",
    "Ant-Man",
    "Wasp",
    "Captain Marvel (Movie)",
    "Falcon",
    "Winter Soldier",
    "War Machine",
    "Nick Fury",
    "Shang-Chi",
    "She-Hulk",
    "Luke Cage",
    "Daredevil",
    "Daredevil (Hell's Kitchen)",
    "Punisher",
    "Blade",
    "Moon Knight",
    "Ghost Rider",
    "Deadpool",
    "Wolverine",
    "Wolverine (X-23)",
    "Wolverine (Weapon X)",
    "Old Man Logan",
    "Professor X",
    "Magneto",
    "Magneto (House of X)",
    "Storm",
    "Cyclops (Blue Team)",
    "Jean Grey",
    "Phoenix",
    "Emma Frost",
    "Beast",
    "Rogue",
    "Gambit",
    "Nightcrawler",
    "Colossus",
    "Iceman",
    "Archangel",
    "Psylocke",
    "Bishop",
    "Cable",
    "Domino",
    "Apocalypse",
    "Namor",
    "Quicksilver",
    "Star-Lord",
    "Gamora",
    "Drax",
    "Rocket Raccoon",
    "Groot",
    "King Groot",
    "Nebula",
    "Mantis",
    "Adam Warlock",
    "Venom",
    "Carnage",
    "Anti-Venom",
    "Knull",
    "Silver Surfer",
    "Hercules",
    "Hyperion",
    "Medusa",
    "Black Bolt",
    "Corvus Glaive",
    "Proxima Midnight",
    "Cosmic Ghost Rider",
    "Gorr",
    "Galan",
    "Odin",
    "Hela",
    "Ronan",
    "Doctor Doom",
    "Loki",
    "Magik",
    "Black Widow (Claire Voyant)",
    "Juggernaut",
    "Dormammu",
    "Mordo",
    "Mephisto",
    "Guillotine",
    "Symbiote Supreme",
    "Tigra",
    "Wong",
    "America Chavez",
    "Wiccan",
    "Absorbing Man",
    "Enchantress",
    "Kushala",
    "Werewolf By Night",
    "Mister Fantastic",
    "Invisible Woman",
    "Human Torch",
    "Thing",
    "Doctor Octopus",
    "Green Goblin",
    "Vulture",
    "Mysterio",
    "Kingpin",
    "Bullseye",
    "Kraven",
    "Black Cat",
    "Kate Bishop",
    "Hit-Monkey",
    "Killmonger",
    "Korg",
    "Gwenpool",
    "Ægon",
    "Ultron",
    "Sentinel",
    "Nimrod",
    "Warlock",
    "Omega Sentinel",
    "Peni Parker",
    "Shuri",
    "Ghost",
    "Hulkbuster",
    "Thanos",
    "Red Skull",
    "Abomination",
    "Sentry",
    "Void",
    "Electro",
    "Sandman",
    "Rhino",
    "Kang",
    "Yondu",
    "Okoye",
    "M'Baku",
    "Silver Sable"
]


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


if len(marvel) != 155:
    raise SystemExit(f"Expected 155 Marvel champions, found {len(marvel)}")

keys = [normalized(name) for name in marvel]
if len(keys) != len(set(keys)):
    raise SystemExit("Marvel list contains duplicate names")

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

print("Marvel rebuilt with 155 recognizable MCOC champions")
