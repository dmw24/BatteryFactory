#!/usr/bin/env python3
"""Fill MISSING site coordinates with city-centroid approximations, fully offline.

Direct geocoding APIs are blocked in this environment, but every un-geocoded row
carries a host city in `plant_name` and/or `research_notes` (e.g. "CATL Yibin ...",
"CALB Chengdu ..."). We match that against the offline geonamescache gazetteer
(~32k world cities, WGS-84) filtered to the row's country, and use the matched
city's centroid.

These are APPROXIMATE city-level coordinates, NOT verified plant locations. Every
row we fill gets an explicit provenance note in `research_notes` and a machine
marker `[GEO=city:<city>]`. Rows where no city resolves are left null (no
country-centroid guessing). The 33 pre-existing verified coordinates are never
touched. Row `confidence` is deliberately NOT altered (it describes the plant's
capacity/existence data, not geo-precision).

Writes the durable, in-repo `data/coordinates.csv` (id, latitude, longitude,
geo_note) so the gitignored DB stays rebuildable.

Run: python3 scripts/geocode_sites.py
"""
import csv
import re
import unicodedata
from datetime import date

import duckdb
import geonamescache

DB = "factories.db"
OUT = "data/coordinates.csv"
STAMP = "2026-07-20"

# Our free-text country -> ISO2. Built from the gazetteer's country list plus aliases.
ALIASES = {
    "united states": "US", "usa": "US", "u.s.": "US", "u.s.a.": "US",
    "south korea": "KR", "korea": "KR", "republic of korea": "KR",
    "united kingdom": "GB", "uk": "GB", "britain": "GB",
    "czech republic": "CZ", "czechia": "CZ",
    "vietnam": "VN", "viet nam": "VN",
}

# Tokens that are country/region/state names, NOT city centroids — never match these.
NON_CITY = {
    "china", "india", "japan", "korea", "germany", "france", "italy", "spain",
    "poland", "hungary", "sweden", "norway", "canada", "mexico", "brazil",
    "thailand", "indonesia", "malaysia", "vietnam", "morocco", "turkey",
    "kentucky", "georgia", "tennessee", "michigan", "ohio", "indiana", "nevada",
    "arizona", "kansas", "california", "carolina", "texas", "oklahoma",
    "jiangsu", "sichuan", "guangdong", "shandong", "zhejiang", "anhui", "fujian",
    "henan", "hubei", "hunan", "qinghai", "jiangxi", "hebei", "shaanxi", "yunnan",
    "guizhou", "gansu", "liaoning", "jilin", "guangxi", "haryana", "gujarat",
}


def norm(s):
    """lowercase, strip accents, drop apostrophes, collapse whitespace."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("’", "")
    return re.sub(r"\s+", " ", s).strip()


def build_country_index(cities):
    """iso2 -> (ranked_names, records) where records maps normalized_name ->
    list of homonym (lat, lon, population, admin1code); ranked_names is the name
    list sorted longest-first then highest-pop so specific/large cities win."""
    recs = {}
    for c in cities.values():
        cc = c["countrycode"]
        names = {c["name"], *[a for a in c.get("alternatenames", []) if a.isascii()]}
        for nm in names:
            nn = norm(nm)
            if len(nn) < 4 or nn in NON_CITY or not re.fullmatch(r"[a-z][a-z \-]+", nn):
                continue
            recs.setdefault(cc, {}).setdefault(nn, []).append(
                (c["latitude"], c["longitude"], c["population"], c.get("admin1code")))
    out = {}
    for cc, d in recs.items():
        ranked = sorted(d, key=lambda nn: (-len(nn), -max(r[2] for r in d[nn])))
        out[cc] = (ranked, d)
    return out


def best_city(text, cand, states_in_text=None):
    """Return (name, lat, lon, pop) for the best gazetteer city named as a whole
    word in text, else None. Iterates candidate names longest/largest-first and
    returns the first that yields an acceptable record. For US, a homonym whose
    state contradicts a state explicitly named in the text is rejected."""
    t = norm(text)
    ranked, recs = cand
    for nn in ranked:
        if not re.search(r"\b" + re.escape(nn) + r"\b", t):
            continue
        homonyms = recs[nn]
        if states_in_text:
            in_state = [h for h in homonyms if h[3] in states_in_text]
            if in_state:                       # state named and a homonym matches it
                h = max(in_state, key=lambda r: r[2])
                return (nn, h[0], h[1], h[2])
            if any(h[3] for h in homonyms):     # state named but NO homonym matches -> reject
                continue
        h = max(homonyms, key=lambda r: r[2])   # else highest population
        return (nn, h[0], h[1], h[2])
    return None


def main():
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    country_by_name = {norm(v["name"]): k for k, v in gc.get_countries().items()}
    country_by_name.update(ALIASES)
    idx = build_country_index(cities)
    # US state name -> postal code, for homonym disambiguation
    us_state_code = {norm(s["name"]): s["code"] for s in gc.get_us_states().values()}

    con = duckdb.connect(DB)
    rows = con.execute("""SELECT id, plant_name, country, region, research_notes
        FROM factories WHERE latitude IS NULL OR longitude IS NULL""").fetchall()

    filled, nulls, no_country = 0, [], 0
    by_region = {}
    coord_rows = []
    for rid, name, country, region, notes in rows:
        iso = country_by_name.get(norm(country or ""))
        cand = idx.get(iso) if iso else None
        if not cand:
            no_country += 1
            nulls.append((rid, region, "no-gazetteer-for-country"))
            continue
        # For US rows, note which states are named so homonyms in the wrong state
        # (e.g. De Soto TX vs the intended De Soto KS) are rejected.
        sit = None
        if iso == "US":
            blob = norm((name or "") + " " + (notes or "")[:600])
            sit = {code for sn, code in us_state_code.items()
                   if re.search(r"\b" + re.escape(sn) + r"\b", blob)}
        # Prefer a city named in plant_name; fall back to research_notes.
        m = best_city(name or "", cand, sit) or best_city((notes or "")[:600], cand, sit)
        if not m:
            nulls.append((rid, region, "no-city-match"))
            by_region.setdefault(region, [0, 0])[1] += 1
            continue
        cname, lat, lon, _pop = m
        disp = cname.title()
        note = (f"[GEO=city:{disp}] Coordinates: approximate city-centroid of {disp}, "
                f"{country} via offline geonamescache gazetteer ({STAMP}) - NOT a verified plant location.")
        newnotes = ((notes + "\n\n") if notes else "") + note
        con.execute("UPDATE factories SET latitude=?, longitude=?, research_notes=? WHERE id=?",
                    [round(float(lat), 5), round(float(lon), 5), newnotes, rid])
        coord_rows.append((rid, round(float(lat), 5), round(float(lon), 5), note))
        filled += 1
        by_region.setdefault(region, [0, 0])[0] += 1

    # durable in-repo store: existing verified coords + the new approximate ones
    verified = con.execute("""SELECT id, latitude, longitude FROM factories
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
          AND id NOT IN (SELECT id FROM factories WHERE research_notes LIKE '%[GEO=city:%')
        """).fetchall()
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "latitude", "longitude", "geo_note"])
        for vid, la, lo in verified:
            w.writerow([vid, la, lo, "verified (from researcher / prior source)"])
        for cr in coord_rows:
            w.writerow(cr)

    print(f"filled {filled} city-centroid coords; {len(nulls)} still null "
          f"({no_country} had no gazetteer country match)")
    print("by region (filled / still-null):")
    for r, (fl, nu) in sorted(by_region.items()):
        print(f"  {r:14} {fl:4} / {nu}")
    print(f"wrote {OUT} ({len(verified)} verified + {len(coord_rows)} approximate)")
    con.close()


if __name__ == "__main__":
    main()
