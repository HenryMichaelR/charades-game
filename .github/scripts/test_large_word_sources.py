import json
import requests

HEADERS = {"User-Agent": "HenryMichaelR-charades-game-builder/1.0"}


def sparql(name, query):
    try:
        response = requests.get(
            "https://query.wikidata.org/sparql",
            params={"query": query, "format": "json"},
            headers=HEADERS,
            timeout=90,
        )
        response.raise_for_status()
        rows = response.json()["results"]["bindings"]
        labels = [row["itemLabel"]["value"] for row in rows]
        print(name, len(labels), labels[:12])
    except Exception as exc:
        print(name, "ERROR", repr(exc))


def mediawiki(name, host, category):
    try:
        titles = []
        continuation = None
        while len(titles) < 600:
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
            response = requests.get(host, params=params, headers=HEADERS, timeout=60)
            response.raise_for_status()
            data = response.json()
            titles.extend(member["title"] for member in data["query"]["categorymembers"])
            continuation = data.get("continue", {}).get("cmcontinue")
            if not continuation:
                break
        print(name, len(titles), titles[:12])
    except Exception as exc:
        print(name, "ERROR", repr(exc))


sparql("movies", '''
SELECT ?item ?itemLabel ?sitelinks WHERE {
  ?item wdt:P31/wdt:P279* wd:Q11424;
        wikibase:sitelinks ?sitelinks.
  FILTER(?sitelinks >= 20)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?sitelinks)
LIMIT 650
''')

sparql("games", '''
SELECT ?item ?itemLabel ?sitelinks WHERE {
  ?item wdt:P31/wdt:P279* wd:Q7889;
        wikibase:sitelinks ?sitelinks.
  FILTER(?sitelinks >= 10)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?sitelinks)
LIMIT 650
''')

sparql("animals", '''
SELECT ?item ?itemLabel ?sitelinks WHERE {
  ?item wdt:P31 wd:Q16521;
        wdt:P171+ wd:Q729;
        wikibase:sitelinks ?sitelinks.
  FILTER(?sitelinks >= 10)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?sitelinks)
LIMIT 650
''')

sparql("marvel", '''
SELECT ?item ?itemLabel ?sitelinks WHERE {
  ?item wdt:P31/wdt:P279* wd:Q95074;
        wdt:P1080 wd:Q931597;
        wikibase:sitelinks ?sitelinks.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?sitelinks)
LIMIT 650
''')

mediawiki("marvel_fandom", "https://marvel.fandom.com/api.php", "Category:Characters")
mediawiki("disney_fandom", "https://disney.fandom.com/api.php", "Category:Characters")
mediawiki("disney_wikipedia", "https://en.wikipedia.org/w/api.php", "Category:Disney_characters")
