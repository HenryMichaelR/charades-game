from __future__ import annotations

import csv
import html
import io
import json
import re
from pathlib import Path
from typing import Iterable

import requests

TARGET = 500
HEADERS = {
    "User-Agent": "HenryMichaelR-charades-game-builder/1.0 (static word-bank cleanup)"
}
GAME_URL = (
    "https://raw.githubusercontent.com/raghav-19/"
    "Video-Games-Sales-Data-Analysis/master/vgsales.csv"
)
MARVEL_API = "https://marvel.fandom.com/api.php"
DISNEY_API = "https://disney.fandom.com/api.php"

BAD_PAGE_TERMS = (
    "gallery",
    "category:",
    "template:",
    "user:",
    "file:",
    "list of ",
    "index of ",
    "character index",
    "characters/",
    "in other media",
    "character collection",
    "articulated heads",
    "walk of fame",
    "animation academy",
    "interactive",
    "skyliner",
    "storybook collection",
    "story collection",
    "typing adventure",
    "parade",
    "soundtrack",
    "album",
    "theme park",
)


def get(url: str, *, params: dict[str, str] | None = None) -> requests.Response:
    response = requests.get(url, params=params, headers=HEADERS, timeout=90)
    response.raise_for_status()
    return response


def key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def basic_clean(value: object) -> str | None:
    text = html.unescape(str(value or ""))
    text = re.sub(r"\s+", " ", text).strip(" \t\r\n–—-|:")
    text = re.sub(
        r"\s*\((?:character|Marvel Comics|Disney character)\)\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    if not text or len(text) < 2 or len(text) > 70:
        return None
    if not re.search(r"[A-Za-z]", text):
        return None
    if text.startswith(("Category:", "Template:", "File:", "User:")):
        return None
    return text


def unique(values: Iterable[object], cleaner=basic_clean, limit: int = TARGET) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = cleaner(value)
        if not item:
            continue
        normalized = key(item)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        output.append(item)
        if len(output) >= limit:
            break
    return output


def load_banks() -> dict[str, list[str]]:
    text = Path("words.js").read_text(encoding="utf-8")
    prefix = "window.CHARADES_CATEGORIES = "
    payload = text.split(prefix, 1)[1].rsplit(";", 1)[0]
    return json.loads(payload)


def category_members(api: str, category: str, maximum: int = 3000) -> list[str]:
    titles: list[str] = []
    continuation: str | None = None
    while len(titles) < maximum:
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
        data = get(api, params=params).json()
        rows = data.get("query", {}).get("categorymembers", [])
        titles.extend(row.get("title", "") for row in rows)
        continuation = data.get("continue", {}).get("cmcontinue")
        if not continuation or not rows:
            break
    return titles


def build_games(seed: list[str]) -> list[str]:
    rows = list(csv.DictReader(io.StringIO(get(GAME_URL).text.lstrip("\ufeff"))))

    def sales(row: dict[str, str]) -> float:
        try:
            return float(row.get("Global_Sales") or 0)
        except (TypeError, ValueError):
            return 0

    rows.sort(key=sales, reverse=True)
    games = unique(seed + [row.get("Name", "") for row in rows])
    if len(games) != TARGET:
        raise RuntimeError(f"Video Games produced {len(games)}")
    return games


def clean_marvel(value: object) -> str | None:
    item = basic_clean(value)
    if not item:
        return None
    lowered = item.casefold()
    if "/" in item or any(term in lowered for term in BAD_PAGE_TERMS):
        return None
    if item[0] in ".'\"0123456789":
        return None

    # Remove wiki qualifiers such as (Earth-616), (Legion Personality), and
    # alternate identity notes, leaving the playable character name.
    item = re.sub(r"\s*\([^()]+\)\s*$", "", item).strip()
    if not item or len(item) < 2 or item[0] in ".'\"0123456789":
        return None
    return item


def build_marvel(seed: list[str]) -> list[str]:
    source: list[str] = []
    for category in ("Category:Characters", "Category:Heroes", "Category:Villains"):
        source.extend(category_members(MARVEL_API, category))
        if len(unique(seed + source, clean_marvel, TARGET)) >= TARGET:
            break
    marvel = unique(seed + source, clean_marvel, TARGET)
    if len(marvel) != TARGET:
        raise RuntimeError(f"Marvel produced {len(marvel)}")
    return marvel


def clean_disney(value: object) -> str | None:
    item = basic_clean(value)
    if not item:
        return None
    lowered = item.casefold()
    if "/" in item or any(term in lowered for term in BAD_PAGE_TERMS):
        return None
    if item[0] in ".'\"0123456789":
        return None
    if lowered in {"characters", "disney characters", "pixar characters"}:
        return None
    item = re.sub(r"\s*\(character\)\s*$", "", item, flags=re.IGNORECASE).strip()
    return item or None


def build_disney(seed: list[str]) -> list[str]:
    canon = unique(
        category_members(
            DISNEY_API,
            "Category:Characters in the Disney animated features canon",
        ),
        clean_disney,
        1600,
    )
    pixar = unique(
        category_members(DISNEY_API, "Category:Pixar characters"),
        clean_disney,
        1600,
    )

    mixed: list[str] = []
    for index in range(max(len(canon), len(pixar))):
        if index < len(canon):
            mixed.append(canon[index])
        if index < len(pixar):
            mixed.append(pixar[index])

    disney = unique(seed + mixed, clean_disney, TARGET)
    if len(disney) != TARGET:
        raise RuntimeError(
            f"Disney produced {len(disney)} (canon={len(canon)}, pixar={len(pixar)})"
        )
    return disney


def write_banks(banks: dict[str, list[str]]) -> None:
    text = (
        "// Generated static word banks. The live game does not call external APIs.\n"
        "window.CHARADES_CATEGORIES = "
        + json.dumps(banks, ensure_ascii=False, indent=2)
        + ";\n"
    )
    Path("words.js").write_text(text, encoding="utf-8")


def main() -> None:
    banks = load_banks()
    banks["Video Games"] = build_games(banks["Video Games"][:30])
    banks["Marvel"] = build_marvel(banks["Marvel"][:30])
    banks["Disney"] = build_disney(banks["Disney"][:30])

    for name, words in banks.items():
        if len(words) != TARGET:
            raise RuntimeError(f"{name}: {len(words)}")
        if len({key(word) for word in words}) != TARGET:
            raise RuntimeError(f"{name}: normalized duplicates")
        print(f"{name}: {len(words)}; sample={words[:12]}")

    write_banks(banks)


if __name__ == "__main__":
    main()
