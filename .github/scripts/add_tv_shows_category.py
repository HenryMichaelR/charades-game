from __future__ import annotations

import json
import re
from pathlib import Path

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

shows = [
    "The Office",
    "Friends",
    "Breaking Bad",
    "Game of Thrones",
    "Stranger Things",
    "The Simpsons",
    "Family Guy",
    "South Park",
    "SpongeBob SquarePants (TV Series)",
    "The Big Bang Theory",
    "How I Met Your Mother",
    "Modern Family",
    "Grey's Anatomy",
    "The Walking Dead",
    "Squid Game",
    "Wednesday",
    "Bridgerton",
    "The Boys",
    "House of the Dragon",
    "Better Call Saul",
    "Sherlock",
    "Peaky Blinders",
    "Black Mirror",
    "The Crown",
    "Suits",
    "Dexter",
    "Lost",
    "Prison Break",
    "Gossip Girl",
    "Gilmore Girls",
    "Brooklyn Nine-Nine",
    "Parks and Recreation",
    "Community",
    "New Girl",
    "Schitt's Creek",
    "Seinfeld",
    "The Fresh Prince of Bel-Air",
    "Full House",
    "Malcolm in the Middle",
    "That '70s Show",
    "Two and a Half Men",
    "Glee",
    "Euphoria",
    "Riverdale",
    "Outer Banks",
    "The Vampire Diaries",
    "Teen Wolf",
    "Supernatural",
    "Smallville",
    "Arrow",
    "The Flash",
    "Daredevil (TV Series)",
    "Loki (TV Series)",
    "WandaVision",
    "The Mandalorian",
    "Doctor Who",
    "Star Trek",
    "The X-Files",
    "House",
    "Criminal Minds",
    "Law & Order",
    "The Sopranos",
    "Mad Men",
    "Succession",
    "The Last of Us",
    "Yellowstone",
    "The Bear",
    "Ted Lasso (TV Series)",
    "Cobra Kai",
    "Money Heist",
    "Narcos",
    "The Queen's Gambit",
    "Avatar: The Last Airbender",
    "Pokémon",
    "Dragon Ball Z",
    "Naruto",
    "One Piece",
    "Rick and Morty",
    "BoJack Horseman",
    "Futurama",
    "Scooby-Doo (TV Series)",
    "Tom and Jerry",
    "Bluey",
    "Sesame Street",
    "Survivor",
    "America's Got Talent",
    "MasterChef",
    "The Bachelor",
    "The Amazing Race",
    "Shark Tank",
]

characters = [
    "Michael Scott",
    "Dwight Schrute",
    "Jim Halpert",
    "Pam Beesly",
    "Rachel Green",
    "Ross Geller",
    "Joey Tribbiani",
    "Chandler Bing",
    "Monica Geller",
    "Phoebe Buffay",
    "Walter White",
    "Jesse Pinkman",
    "Saul Goodman",
    "Jon Snow",
    "Daenerys Targaryen",
    "Tyrion Lannister",
    "Cersei Lannister",
    "Eleven",
    "Steve Harrington",
    "Dustin Henderson",
    "Homer Simpson",
    "Bart Simpson",
    "Lisa Simpson",
    "Peter Griffin",
    "Stewie Griffin",
    "Eric Cartman",
    "Kenny McCormick",
    "SpongeBob SquarePants",
    "Patrick Star",
    "Sheldon Cooper",
    "Leonard Hofstadter",
    "Barney Stinson",
    "Ted Mosby",
    "Phil Dunphy",
    "Gloria Pritchett",
    "Meredith Grey",
    "Rick Grimes",
    "Daryl Dixon",
    "Negan",
    "Wednesday Addams",
    "Joe Goldberg",
    "Homelander",
    "Billy Butcher",
    "Daemon Targaryen",
    "Sherlock Holmes",
    "Thomas Shelby",
    "Harvey Specter",
    "Mike Ross",
    "Dexter Morgan",
    "Michael Scofield",
    "Blair Waldorf",
    "Serena van der Woodsen",
    "Lorelai Gilmore",
    "Jake Peralta",
    "Captain Holt",
    "Leslie Knope",
    "Ron Swanson",
    "Moira Rose",
    "David Rose",
    "Jerry Seinfeld",
    "George Costanza",
    "Carlton Banks",
    "Uncle Phil",
    "Malcolm Wilkerson",
    "Eric Forman",
    "Charlie Harper",
    "Rue Bennett",
    "Damon Salvatore",
    "Stefan Salvatore",
    "Dean Winchester",
    "Sam Winchester",
    "Clark Kent",
    "Oliver Queen",
    "Barry Allen",
    "The Doctor",
    "Spock",
    "Fox Mulder",
    "Dana Scully",
    "Gregory House",
    "Tony Soprano",
    "Don Draper",
    "Logan Roy",
    "Kendall Roy",
    "Joel Miller",
    "Ellie Williams",
    "Ted Lasso",
    "The Professor",
    "Beth Harmon",
    "Aang",
    "Zuko",
    "Ash Ketchum",
    "Goku",
    "Naruto Uzumaki",
    "Monkey D. Luffy",
    "Rick Sanchez",
    "Morty Smith",
    "Scooby-Doo",
    "Shaggy Rogers",
    "Bluey Heeler",
    "Elmo",
    "Grogu",
    "Din Djarin",
    "Loki",
    "Wanda Maximoff",
    "Daredevil",
]

tv_words = shows + characters


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


if len(shows) != 90:
    raise SystemExit(f"Expected 90 shows, found {len(shows)}")
if len(characters) != 105:
    raise SystemExit(f"Expected 105 characters, found {len(characters)}")
if len(tv_words) != 195:
    raise SystemExit(f"Expected 195 TV prompts, found {len(tv_words)}")

keys = [normalized(item) for item in tv_words]
if len(keys) != len(set(keys)):
    raise SystemExit("TV Shows category contains duplicate prompts")

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
existing_categories = {name: list(words) for name, words in categories.items()}

if "TV Shows" in categories:
    raise SystemExit("TV Shows category already exists")

categories["TV Shows"] = tv_words

for name, words in existing_categories.items():
    if categories.get(name) != words:
        raise SystemExit(f"Existing category changed unexpectedly: {name}")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print("Added TV Shows with 90 series and 105 iconic characters")
