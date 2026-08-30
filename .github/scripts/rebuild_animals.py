from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

animals = [
    "Dog", "Cat", "Elephant", "Lion", "Tiger", "Bear", "Panda", "Giraffe", "Zebra", "Horse",
    "Cow", "Pig", "Sheep", "Goat", "Chicken", "Duck", "Goose", "Turkey", "Donkey", "Rabbit",
    "Hamster", "Guinea Pig", "Mouse", "Rat", "Squirrel", "Chipmunk", "Raccoon", "Skunk", "Fox", "Wolf",
    "Coyote", "Deer", "Moose", "Reindeer", "Camel", "Llama", "Alpaca", "Kangaroo", "Koala", "Sloth",
    "Monkey", "Gorilla", "Chimpanzee", "Orangutan", "Baboon", "Lemur", "Meerkat", "Otter", "Beaver", "Hedgehog",
    "Porcupine", "Armadillo", "Anteater", "Platypus", "Hippo", "Rhino", "Buffalo", "Bison", "Antelope", "Gazelle",
    "Cheetah", "Leopard", "Jaguar", "Panther", "Hyena", "Wild Boar", "Warthog", "Mole", "Bat", "Ferret",
    "Seal", "Sea Lion", "Walrus", "Dolphin", "Whale", "Killer Whale", "Shark", "Hammerhead Shark", "Stingray", "Manta Ray",
    "Octopus", "Squid", "Jellyfish", "Starfish", "Seahorse", "Crab", "Lobster", "Shrimp", "Clam", "Oyster",
    "Snail", "Slug", "Turtle", "Sea Turtle", "Tortoise", "Crocodile", "Alligator", "Snake", "Lizard", "Chameleon",
    "Iguana", "Gecko", "Komodo Dragon", "Frog", "Toad", "Salamander", "Axolotl", "Eagle", "Owl", "Hawk",
    "Falcon", "Parrot", "Penguin", "Flamingo", "Peacock", "Ostrich", "Emu", "Pelican", "Swan", "Pigeon",
    "Seagull", "Crow", "Robin", "Hummingbird", "Woodpecker", "Toucan", "Vulture", "Butterfly", "Moth", "Bee",
    "Wasp", "Ant", "Spider", "Scorpion", "Beetle", "Ladybug", "Grasshopper", "Cricket", "Dragonfly", "Caterpillar",
    "Cockroach", "Centipede", "Millipede", "Earthworm", "Mosquito", "Fly", "Firefly", "Praying Mantis", "Pufferfish", "Eel"
]


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


if len(animals) != 150:
    raise SystemExit(f"Expected 150 animals, found {len(animals)}")

keys = [normalized(animal) for animal in animals]
if len(keys) != len(set(keys)):
    raise SystemExit("Animals list contains duplicates")

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
if "Animals" not in categories:
    raise SystemExit("Animals category is missing")

other_categories = {
    name: list(words)
    for name, words in categories.items()
    if name != "Animals"
}

categories["Animals"] = animals

if {
    name: list(words)
    for name, words in categories.items()
    if name != "Animals"
} != other_categories:
    raise SystemExit("A non-Animals category changed unexpectedly")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print("Animals rebuilt with 150 familiar animal names")
