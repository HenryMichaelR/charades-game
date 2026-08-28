from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

DISNEY = [
    "Mickey Mouse", "Minnie Mouse", "Donald Duck", "Daisy Duck", "Goofy", "Pluto", "Chip", "Dale",
    "Snow White", "The Evil Queen", "Cinderella", "Fairy Godmother", "Prince Charming",
    "Aurora", "Maleficent", "Pinocchio", "Jiminy Cricket", "Dumbo", "Bambi",
    "Alice", "Mad Hatter", "Cheshire Cat", "Peter Pan", "Tinker Bell", "Captain Hook",
    "Winnie the Pooh", "Tigger", "Eeyore", "Piglet",
    "Ariel", "Sebastian", "Flounder", "Ursula",
    "Belle", "The Beast", "Gaston", "Lumiere",
    "Aladdin", "Jasmine", "Genie", "Jafar", "Abu",
    "Simba", "Nala", "Mufasa", "Scar", "Timon", "Pumbaa", "Rafiki",
    "Pocahontas", "Mulan", "Mushu", "Hercules", "Hades",
    "Tarzan", "Stitch", "Lilo", "Cruella de Vil", "Jack Sparrow",
    "Tiana", "Prince Naveen", "Rapunzel", "Flynn Rider", "Mother Gothel",
    "Elsa", "Anna", "Olaf", "Kristoff", "Sven",
    "Moana", "Maui", "Mirabel", "Bruno", "Luisa",
    "Baymax", "Ralph", "Vanellope", "Judy Hopps", "Nick Wilde",
    "Woody", "Buzz Lightyear", "Jessie", "Rex", "Mr. Potato Head",
    "Nemo", "Dory", "Marlin", "Sulley", "Mike Wazowski",
    "Lightning McQueen", "Mater", "Remy", "Wall-E", "Eve",
    "Mr. Incredible", "Elastigirl", "Violet Parr", "Dash Parr", "Jack-Jack", "Edna Mode",
    "Joy", "Sadness", "Miguel", "Carl Fredricksen", "Russell", "Merida"
]

MARVEL = [
    "Spider-Man", "Miles Morales", "Spider-Gwen", "Iron Man", "Captain America", "Thor", "Hulk",
    "Black Widow", "Hawkeye", "Black Panther", "Doctor Strange", "Scarlet Witch", "Vision",
    "Ant-Man", "The Wasp", "Captain Marvel", "Falcon", "Winter Soldier", "War Machine",
    "Nick Fury", "Shuri", "Okoye", "M'Baku", "Wong", "Shang-Chi", "She-Hulk", "Ms. Marvel",
    "Moon Knight", "Daredevil", "The Punisher", "Jessica Jones", "Luke Cage", "Iron Fist",
    "Blade", "Ghost Rider", "Deadpool", "Wolverine", "Professor X", "Magneto", "Storm",
    "Cyclops", "Jean Grey", "Mystique", "Beast", "Rogue", "Gambit", "Nightcrawler", "Colossus",
    "Mr. Fantastic", "Invisible Woman", "Human Torch", "The Thing", "Silver Surfer",
    "Star-Lord", "Gamora", "Drax", "Rocket Raccoon", "Groot", "Nebula", "Mantis",
    "Loki", "Thanos", "Ultron", "Red Skull", "Green Goblin", "Doctor Octopus", "Venom",
    "Carnage", "Mysterio", "Vulture", "Electro", "Sandman", "Kingpin", "Killmonger",
    "Hela", "Abomination", "Kang the Conqueror", "Galactus", "Dormammu", "Ronan the Accuser",
    "Agatha Harkness", "Adam Warlock", "Namor", "Aunt May", "Mary Jane", "Pepper Potts",
    "Happy Hogan", "Peggy Carter", "Yondu"
]


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def validate_unique(label: str, values: list[str]) -> None:
    keys = [normalized(value) for value in values]
    if len(keys) != len(set(keys)):
        raise SystemExit(f"{label} contains duplicate names")


validate_unique("Disney", DISNEY)
validate_unique("Marvel", MARVEL)

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
for required_category in ("Disney", "Marvel"):
    if required_category not in categories:
        raise SystemExit(f"Missing category: {required_category}")

other_categories = {
    name: list(words)
    for name, words in categories.items()
    if name not in {"Disney", "Marvel"}
}

categories["Disney"] = DISNEY
categories["Marvel"] = MARVEL

if {
    name: list(words)
    for name, words in categories.items()
    if name not in {"Disney", "Marvel"}
} != other_categories:
    raise SystemExit("A category other than Disney or Marvel changed unexpectedly")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print(f"Disney rebuilt with {len(DISNEY)} recognizable characters")
print(f"Marvel rebuilt with {len(MARVEL)} recognizable characters")
