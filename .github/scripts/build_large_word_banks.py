from __future__ import annotations

import csv
import html
import io
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "HenryMichaelR-charades-game-builder/1.0 (GitHub Pages word-bank build)"
}
TARGET = 500

ANIMAL_URL = "https://raw.githubusercontent.com/skjorrface/animals.txt/master/animals.txt"
MOVIE_URL = "https://gist.githubusercontent.com/T-Reiser/1118aa906c506aa00095288bfc8e854d/raw/24f2cbb864c3e963cef9cc8a4d66311ec416c6b8/TopTMDB.csv"
GAME_URL = "https://raw.githubusercontent.com/raghav-19/Video-Games-Sales-Data-Analysis/master/vgsales.csv"

SEEDS = {
    "Animals": [
        "Elephant", "Penguin", "Giraffe", "Kangaroo", "Dolphin", "Octopus",
        "Crocodile", "Flamingo", "Gorilla", "Butterfly", "Shark", "Tiger",
        "Lion", "Monkey", "Rabbit", "Turtle", "Snake", "Horse", "Zebra",
        "Owl", "Panda", "Koala", "Wolf", "Fox", "Bear", "Eagle",
        "Peacock", "Camel", "Hippo", "Rhino"
    ],
    "Movies": [
        "Titanic", "Avatar", "Frozen", "Shrek", "Jaws", "The Avengers",
        "Jurassic Park", "Toy Story", "The Lion King", "Finding Nemo",
        "Spider-Man", "Iron Man", "Black Panther", "The Dark Knight",
        "Home Alone", "Harry Potter", "The Hunger Games", "Star Wars",
        "The Matrix", "Ghostbusters", "Barbie", "Oppenheimer",
        "The Incredibles", "Moana", "Aladdin", "Cars", "Ratatouille",
        "The Notebook", "Mean Girls", "Interstellar"
    ],
    "Video Games": [
        "Minecraft", "Fortnite", "Mario Kart", "Pokémon", "Valorant",
        "Roblox", "The Sims", "Among Us", "Grand Theft Auto", "Call of Duty",
        "Super Mario", "The Legend of Zelda", "Overwatch", "Rocket League",
        "Fall Guys", "Animal Crossing", "Clash of Clans", "Apex Legends",
        "Terraria", "Wii Sports", "League of Legends", "Marvel Rivals",
        "Mortal Kombat", "Street Fighter", "Candy Crush", "Plants vs. Zombies",
        "Red Dead Redemption", "Halo", "Sonic the Hedgehog",
        "Five Nights at Freddy's"
    ],
    "Marvel": [
        "Spider-Man", "Iron Man", "Thor", "Hulk", "Black Widow", "Hawkeye",
        "Captain America", "Black Panther", "Doctor Strange", "Scarlet Witch",
        "Vision", "Thanos", "Loki", "Deadpool", "Wolverine", "Storm",
        "Cyclops", "Jean Grey", "Magneto", "Professor X", "Daredevil",
        "Moon Knight", "Ant-Man", "The Wasp", "Star-Lord", "Groot",
        "Rocket Raccoon", "Gamora", "Nebula", "Venom"
    ],
    "Disney": [
        "Mickey Mouse", "Minnie Mouse", "Donald Duck", "Goofy", "Cinderella",
        "Snow White", "Ariel", "Belle", "Aladdin", "Jasmine", "Simba",
        "Mufasa", "Elsa", "Anna", "Olaf", "Moana", "Maui", "Stitch",
        "Peter Pan", "Tinker Bell", "Buzz Lightyear", "Woody",
        "Lightning McQueen", "Nemo", "Dory", "Winnie the Pooh", "Tigger",
        "Rapunzel", "Cruella de Vil", "Maleficent"
    ],
}

BAD_PREFIXES = (
    "Category:", "File:", "Template:", "Portal:", "Help:", "User:",
    "List of ", "Lists of ", "Index of ", "Outline of ", "Timeline of ",
)
BAD_EXACT = {
    "References", "External links", "See also", "Notes", "Further reading",
    "Bibliography", "Publication history", "Fictional character biography",
    "Powers and abilities", "In other media", "Reception", "Development",
    "Description", "Appearances", "Character", "Characters", "Overview",
    "History", "Plot", "Cast", "Gameplay", "Legacy", "Other versions",
}


def get(url: str, **kwargs) -> requests.Response:
    response = requests.get(url, headers=HEADERS, timeout=75, **kwargs)
    response.raise_for_status()
    return response


def clean(value: object) -> str | None:
    text = html.unescape(str(value or ""))
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\s+", " ", text).strip(" \t\r\n–—-|:")
    text = re.sub(
        r"\s*\((?:character|Marvel Comics|Disney|film|video game|franchise|fictional character)\)\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    if not text or text in BAD_EXACT or text.startswith(BAD_PREFIXES):
        return None
    if len(text) < 2 or len(text) > 70:
        return None
    if not re.search(r"[A-Za-z]", text):
        return None
    if text.lower().endswith((" disambiguation", " redirects here")):
        return None
    return text


def unique(values: Iterable[object], limit: int = TARGET) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = clean(value)
        if not item:
            continue
        key = re.sub(r"[^a-z0-9]+", "", item.lower())
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
        if len(output) >= limit:
            break
    return output


def build_animals() -> list[str]:
    text = get(ANIMAL_URL).text
    source = [line.strip() for line in text.splitlines()]
    return unique(SEEDS["Animals"] + source)


def build_movies() -> list[str]:
    text = get(MOVIE_URL).text.lstrip("\ufeff")
    rows = list(csv.DictReader(io.StringIO(text)))

    def score(row: dict[str, str]) -> tuple[float, float]:
        try:
            popularity = float(row.get("popularity") or 0)
        except ValueError:
            popularity = 0
        try:
            votes = float(row.get("vote_count") or 0)
        except ValueError:
            votes = 0
        return popularity, votes

    rows.sort(key=score, reverse=True)
    source = [row.get("title") or row.get("original_title") for row in rows]
    return unique(SEEDS["Movies"] + source)


def build_games() -> list[str]:
    text = get(GAME_URL).text.lstrip("\ufeff")
    rows = list(csv.DictReader(io.StringIO(text)))

    def rank(row: dict[str, str]) -> float:
        try:
            return float(row.get("Rank") or 10**9)
        except ValueError:
            return 10**9

    rows.sort(key=rank)
    source = [row.get("Name") for row in rows]
    return unique(SEEDS["Video Games"] + source)


def wikipedia_marvel_headings() -> list[str]:
    names: list[str] = []
    api = "https://en.wikipedia.org/w/api.php"
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        page = f"List of Marvel Comics characters: {letter}"
        try:
            data = get(
                api,
                params={
                    "action": "parse",
                    "page": page,
                    "prop": "text",
                    "format": "json",
                    "formatversion": "2",
                    "redirects": "1",
                },
            ).json()
        except Exception as exc:
            print(f"Marvel page {letter} failed: {exc}")
            continue
        parsed = data.get("parse", {}).get("text", "")
        soup = BeautifulSoup(parsed, "html.parser")
        for heading in soup.select("h2, h3"):
            text = heading.get_text(" ", strip=True)
            text = re.sub(r"\s*\[edit\]\s*$", "", text)
            names.append(text)
        if len(unique(SEEDS["Marvel"] + names, TARGET)) >= TARGET:
            break
    return names


def fandom_category(host: str, categories: list[str], maximum: int = 1200) -> list[str]:
    names: list[str] = []
    for category in categories:
        continuation = None
        while len(names) < maximum:
            params = {
                "action": "query",
                "list": "categorymembers",
                "cmtitle": category,
                "cmnamespace": "0",
                "cmlimit": "500",
                "format": "json",
                "formatversion": "2",
            }
            if continuation:
                params["cmcontinue"] = continuation
            try:
                data = get(host, params=params).json()
            except Exception as exc:
                print(f"Category {category} failed: {exc}")
                break
            members = data.get("query", {}).get("categorymembers", [])
            names.extend(member.get("title", "") for member in members)
            continuation = data.get("continue", {}).get("cmcontinue")
            if not continuation or not members:
                break
        if len(names) >= maximum:
            break
    return names


def build_marvel() -> list[str]:
    headings = wikipedia_marvel_headings()
    if len(unique(SEEDS["Marvel"] + headings, TARGET)) < TARGET:
        headings.extend(
            fandom_category(
                "https://marvel.fandom.com/api.php",
                ["Category:Characters", "Category:Heroes", "Category:Villains"],
            )
        )
    return unique(SEEDS["Marvel"] + headings)


def fandom_search(host: str, query: str, maximum: int = 1000) -> list[str]:
    names: list[str] = []
    offset = 0
    while len(names) < maximum:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": "0",
            "srlimit": "500",
            "sroffset": str(offset),
            "format": "json",
            "formatversion": "2",
        }
        try:
            data = get(host, params=params).json()
        except Exception as exc:
            print(f"Search {query} failed: {exc}")
            break
        rows = data.get("query", {}).get("search", [])
        names.extend(row.get("title", "") for row in rows)
        if not rows or "continue" not in data:
            break
        offset = int(data["continue"].get("sroffset", offset + len(rows)))
    return names


def build_disney() -> list[str]:
    api = "https://disney.fandom.com/api.php"
    names = fandom_search(api, 'incategory:"Disney characters"')
    names.extend(
        fandom_category(
            api,
            ["Category:Disney characters", "Category:Characters"],
            maximum=1800,
        )
    )
    return unique(SEEDS["Disney"] + names)


def patch_index() -> None:
    path = Path("index.html")
    text = path.read_text(encoding="utf-8")

    if '<script src="words.js"></script>' not in text:
        marker = "  <script>\n    const categories = {"
        if marker not in text:
            raise RuntimeError("Could not find the inline category script")
        text = text.replace(
            marker,
            '  <script src="words.js"></script>\n\n  <script>\n    const categories = {',
            1,
        )

    start = text.find("    const categories = {")
    end_marker = "\n\n    const categorySelect ="
    end = text.find(end_marker, start)
    if start < 0 or end < 0:
        raise RuntimeError("Could not locate inline categories block")
    text = (
        text[:start]
        + "    const categories = window.CHARADES_CATEGORIES;"
        + text[end:]
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    builders = {
        "Animals": build_animals,
        "Movies": build_movies,
        "Video Games": build_games,
        "Marvel": build_marvel,
        "Disney": build_disney,
    }

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {name: pool.submit(builder) for name, builder in builders.items()}
        categories = {name: future.result() for name, future in futures.items()}

    for name, words in categories.items():
        if len(words) != TARGET:
            raise RuntimeError(f"{name} produced {len(words)} words, expected {TARGET}")
        if len({word.casefold() for word in words}) != TARGET:
            raise RuntimeError(f"{name} contains duplicates")
        print(f"{name}: {len(words)} words; sample: {words[:8]}")

    js = (
        "// Generated static word banks. The live game does not call external APIs.\n"
        "window.CHARADES_CATEGORIES = "
        + json.dumps(categories, ensure_ascii=False, indent=2)
        + ";\n"
    )
    Path("words.js").write_text(js, encoding="utf-8")
    patch_index()


if __name__ == "__main__":
    main()
