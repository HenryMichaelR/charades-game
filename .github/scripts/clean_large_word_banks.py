from __future__ import annotations

import csv
import html
import io
import json
import re
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup

TARGET = 500
HEADERS = {
    "User-Agent": "HenryMichaelR-charades-game-builder/1.0 (static word-bank cleanup)"
}
GAME_URL = (
    "https://raw.githubusercontent.com/raghav-19/"
    "Video-Games-Sales-Data-Analysis/master/vgsales.csv"
)
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
DISNEY_API = "https://disney.fandom.com/api.php"

BAD_COMMON = {
    "references",
    "external links",
    "see also",
    "notes",
    "further reading",
    "bibliography",
    "publication history",
    "fictional character biography",
    "powers and abilities",
    "reception",
    "development",
    "description",
    "appearances",
    "overview",
    "history",
    "plot",
    "cast",
    "gameplay",
    "legacy",
    "other versions",
}

BAD_DISNEY_TERMS = (
    "gallery",
    "category:",
    "template:",
    "user:",
    "file:",
    "list of ",
    "index of ",
    "characters/",
    "character collection",
    "articulated heads",
    "walk of fame",
    "animation academy",
    "disney interactive",
    "disney skyliner",
    "story collection",
    "storybook collection",
    "typing adventure",
    "parade",
    "show)",
    "(series)",
    "soundtrack",
    "album",
    "video game",
    "theme park",
)


def get(url: str, *, params: dict[str, str] | None = None) -> requests.Response:
    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=90,
    )
    response.raise_for_status()
    return response


def normalize_display(value: object) -> str | None:
    text = html.unescape(str(value or ""))
    text = re.sub(r"\s*\[edit\]\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[[^\]]*\]", "", text)
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
    if text.casefold() in BAD_COMMON:
        return None
    if text.startswith(("Category:", "Template:", "File:", "User:")):
        return None
    return text


def normalized_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def unique(values: Iterable[object], limit: int = TARGET) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = normalize_display(value)
        if not item:
            continue
        key = normalized_key(item)
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
        if len(output) >= limit:
            break
    return output


def load_existing() -> dict[str, list[str]]:
    text = Path("words.js").read_text(encoding="utf-8")
    prefix = "window.CHARADES_CATEGORIES = "
    if prefix not in text:
        raise RuntimeError("words.js assignment was not found")
    payload = text.split(prefix, 1)[1].rsplit(";", 1)[0]
    banks = json.loads(payload)
    return banks


def build_video_games(seed: list[str]) -> list[str]:
    text = get(GAME_URL).text.lstrip("\ufeff")
    rows = list(csv.DictReader(io.StringIO(text)))

    def global_sales(row: dict[str, str]) -> float:
        try:
            return float(row.get("Global_Sales") or 0)
        except (TypeError, ValueError):
            return 0

    rows.sort(key=global_sales, reverse=True)
    ranked_titles = [row.get("Name", "") for row in rows]
    games = unique(seed + ranked_titles)
    if len(games) != TARGET:
        raise RuntimeError(f"Video Games produced {len(games)} entries")
    return games


def wikipedia_marvel_names() -> list[str]:
    names: list[str] = []

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        page = f"List of Marvel Comics characters: {letter}"
        data = get(
            WIKIPEDIA_API,
            params={
                "action": "parse",
                "page": page,
                "prop": "text",
                "format": "json",
                "formatversion": "2",
                "redirects": "1",
            },
        ).json()
        parsed = data.get("parse", {}).get("text", "")
        soup = BeautifulSoup(parsed, "html.parser")

        # H2 headings are the actual A–Z character entries. H3 headings often
        # contain identities, adaptations, and other non-prompt sub-sections.
        for heading in soup.select("h2"):
            value = normalize_display(heading.get_text(" ", strip=True))
            if not value:
                continue
            lowered = value.casefold()
            if "in other media" in lowered or lowered in BAD_COMMON:
                continue
            if lowered.startswith(("list of ", "index of ")):
                continue
            names.append(value)

    return names


def build_marvel(seed: list[str]) -> list[str]:
    marvel = unique(seed + wikipedia_marvel_names())
    if len(marvel) != TARGET:
        raise RuntimeError(f"Marvel produced {len(marvel)} entries")

    forbidden = [name for name in marvel if "in other media" in name.casefold()]
    if forbidden:
        raise RuntimeError(f"Marvel contains non-character headings: {forbidden[:5]}")
    return marvel


def category_members(category: str, maximum: int = 1600) -> list[str]:
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

        data = get(DISNEY_API, params=params).json()
        rows = data.get("query", {}).get("categorymembers", [])
        titles.extend(row.get("title", "") for row in rows)

        continuation = data.get("continue", {}).get("cmcontinue")
        if not continuation or not rows:
            break

    return titles


def clean_disney_title(value: object) -> str | None:
    item = normalize_display(value)
    if not item:
        return None

    lowered = item.casefold()
    if "/" in item:
        return None
    if item[0] in ".'\"0123456789":
        return None
    if any(term in lowered for term in BAD_DISNEY_TERMS):
        return None
    if lowered in {"disney characters", "pixar characters", "characters"}:
        return None
    return item


def unique_disney(values: Iterable[object], limit: int | None = None) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = clean_disney_title(value)
        if not item:
            continue
        key = normalized_key(item)
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
        if limit is not None and len(output) >= limit:
            break
    return output


def build_disney(seed: list[str]) -> list[str]:
    canon = unique_disney(
        category_members("Category:Characters in the Disney animated features canon")
    )
    pixar = unique_disney(category_members("Category:Pixar characters"))

    # Interleave the two franchises so the final bank is not dominated by one
    # alphabetical category listing.
    mixed: list[str] = []
    maximum = max(len(canon), len(pixar))
    for index in range(maximum):
        if index < len(canon):
            mixed.append(canon[index])
        if index < len(pixar):
            mixed.append(pixar[index])

    disney = unique_disney(seed + mixed, TARGET)
    if len(disney) != TARGET:
        raise RuntimeError(
            f"Disney produced {len(disney)} entries "
            f"(canon={len(canon)}, pixar={len(pixar)})"
        )

    bad = [
        name for name in disney
        if "/" in name or any(term in name.casefold() for term in BAD_DISNEY_TERMS)
    ]
    if bad:
        raise RuntimeError(f"Disney contains non-character pages: {bad[:5]}")
    return disney


def write_banks(banks: dict[str, list[str]]) -> None:
    output = (
        "// Generated static word banks. The live game does not call external APIs.\n"
        "window.CHARADES_CATEGORIES = "
        + json.dumps(banks, ensure_ascii=False, indent=2)
        + ";\n"
    )
    Path("words.js").write_text(output, encoding="utf-8")


def main() -> None:
    banks = load_existing()

    # Keep the hand-picked first 30 prompts at the top of each regenerated bank.
    game_seed = banks["Video Games"][:30]
    marvel_seed = banks["Marvel"][:30]
    disney_seed = banks["Disney"][:30]

    banks["Video Games"] = build_video_games(game_seed)
    banks["Marvel"] = build_marvel(marvel_seed)
    banks["Disney"] = build_disney(disney_seed)

    expected_order = ["Animals", "Movies", "Video Games", "Marvel", "Disney"]
    if list(banks) != expected_order:
        raise RuntimeError(f"Unexpected category order: {list(banks)}")

    for name, words in banks.items():
        if len(words) != TARGET:
            raise RuntimeError(f"{name}: expected 500, found {len(words)}")
        if len({normalized_key(word) for word in words}) != TARGET:
            raise RuntimeError(f"{name}: normalized duplicates found")
        print(f"{name}: {len(words)}; sample={words[:12]}")

    write_banks(banks)


if __name__ == "__main__":
    main()
