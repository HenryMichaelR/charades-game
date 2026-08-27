from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

video_games = [
    "Minecraft",
    "Fortnite",
    "Roblox",
    "Grand Theft Auto V",
    "Call of Duty",
    "Call of Duty: Warzone",
    "Mario Kart",
    "Super Mario Bros.",
    "Pokémon",
    "Pokémon GO",
    "The Legend of Zelda",
    "The Legend of Zelda: Breath of the Wild",
    "Animal Crossing",
    "Wii Sports",
    "Super Smash Bros.",
    "Mario Party",
    "Among Us",
    "Fall Guys",
    "Rocket League",
    "Valorant",
    "Overwatch",
    "Apex Legends",
    "League of Legends",
    "Counter-Strike",
    "PUBG",
    "Marvel Rivals",
    "Genshin Impact",
    "World of Warcraft",
    "The Sims",
    "Candy Crush",
    "Subway Surfers",
    "Clash of Clans",
    "Clash Royale",
    "Angry Birds",
    "Temple Run",
    "Fruit Ninja",
    "Plants vs. Zombies",
    "Geometry Dash",
    "Flappy Bird",
    "Crossy Road",
    "Jetpack Joyride",
    "Cut the Rope",
    "Hill Climb Racing",
    "My Talking Tom",
    "Wordle",
    "Tetris",
    "Pac-Man",
    "Pong",
    "Space Invaders",
    "Snake",
    "Minesweeper",
    "Solitaire",
    "Sonic the Hedgehog",
    "Crash Bandicoot",
    "Spyro the Dragon",
    "Donkey Kong",
    "Kirby",
    "Luigi's Mansion",
    "Splatoon",
    "Nintendogs",
    "Cooking Mama",
    "Just Dance",
    "Guitar Hero",
    "Rock Band",
    "Dance Dance Revolution",
    "Wii Fit",
    "Red Dead Redemption 2",
    "The Last of Us",
    "God of War",
    "Marvel's Spider-Man",
    "Batman: Arkham City",
    "Assassin's Creed",
    "The Elder Scrolls V: Skyrim",
    "Fallout 4",
    "Cyberpunk 2077",
    "Elden Ring",
    "Dark Souls",
    "The Witcher 3",
    "Resident Evil",
    "Silent Hill",
    "Tomb Raider",
    "Uncharted",
    "Far Cry",
    "Hogwarts Legacy",
    "Star Wars Battlefront",
    "LEGO Star Wars",
    "Detroit: Become Human",
    "Hitman",
    "Portal",
    "Halo",
    "Destiny",
    "Doom",
    "Diablo",
    "SimCity",
    "Stardew Valley",
    "Terraria",
    "Five Nights at Freddy's",
    "Poppy Playtime",
    "Hello Neighbor",
    "Cuphead",
    "Undertale",
    "Dead by Daylight",
    "EA Sports FC / FIFA",
    "NBA 2K",
    "Madden NFL",
    "NHL",
    "WWE 2K",
    "Forza Horizon",
    "Gran Turismo",
    "Need for Speed",
    "Tony Hawk's Pro Skater",
    "Mortal Kombat",
    "Street Fighter",
    "Tekken",
    "Final Fantasy VII",
    "Kingdom Hearts",
    "LEGO Batman",
    "The Simpsons: Hit & Run",
    "Club Penguin",
    "Mario & Sonic at the Olympic Games",
]


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


if len(video_games) != 120:
    raise SystemExit(f"Expected 120 games, found {len(video_games)}")

keys = [normalized(game) for game in video_games]
if len(keys) != len(set(keys)):
    raise SystemExit("Video Games list contains duplicate names")

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
if "Video Games" not in categories:
    raise SystemExit("Video Games category is missing")

other_categories = {
    name: list(words)
    for name, words in categories.items()
    if name != "Video Games"
}

categories["Video Games"] = video_games

if {
    name: list(words)
    for name, words in categories.items()
    if name != "Video Games"
} != other_categories:
    raise SystemExit("A non-Video Games category changed unexpectedly")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print("Video Games rebuilt with 120 mainstream titles")
