#!/usr/bin/env python3
"""Merge per-region list-builder CSVs into a deduped candidates.csv.

Each region file lives in data/seed/<region>.csv with rows:
    plant_name,operator,country
(no header required; a header row is auto-detected and skipped).

Dedupe key = normalised (plant_name + operator + country).
Region is inferred from the filename and written as a 4th column.
"""
import csv
import glob
import os
import re
import sys

SEED_DIR = "data/seed"
OUT = "candidates.csv"

REGION_FROM_FILE = {
    "china": "China",
    "usa": "USA",
    "europe": "Europe",
    "south_korea": "South Korea",
    "japan": "Japan",
    "india": "India",
    "southeast_asia": "Southeast Asia",
    "rest_of_world": "Rest of World",
}

# Authoritative country -> region map. Region is derived from the country field
# so a file may mix countries (e.g. a combined Japan+Korea seed) without
# mislabelling. Falls back to the filename-inferred region if a country is
# unknown (log it and fix the map).
COUNTRY_TO_REGION = {
    "china": "China",
    "united states": "USA", "usa": "USA", "us": "USA",
    "south korea": "South Korea", "korea": "South Korea",
    "japan": "Japan",
    "india": "India",
    # Europe
    "germany": "Europe", "france": "Europe", "hungary": "Europe",
    "poland": "Europe", "spain": "Europe", "italy": "Europe",
    "sweden": "Europe", "norway": "Europe", "united kingdom": "Europe",
    "uk": "Europe", "slovakia": "Europe", "serbia": "Europe",
    "turkey": "Europe", "portugal": "Europe", "netherlands": "Europe",
    "austria": "Europe", "finland": "Europe", "switzerland": "Europe",
    "czechia": "Europe", "czech republic": "Europe", "romania": "Europe",
    "greece": "Europe", "belgium": "Europe", "denmark": "Europe",
    # Southeast Asia
    "indonesia": "Southeast Asia", "thailand": "Southeast Asia",
    "malaysia": "Southeast Asia", "vietnam": "Southeast Asia",
    "philippines": "Southeast Asia", "singapore": "Southeast Asia",
    "laos": "Southeast Asia", "cambodia": "Southeast Asia",
    "myanmar": "Southeast Asia",
    # Rest of World
    "canada": "Rest of World", "mexico": "Rest of World",
    "brazil": "Rest of World", "morocco": "Rest of World",
    "united arab emirates": "Rest of World", "uae": "Rest of World",
    "saudi arabia": "Rest of World", "australia": "Rest of World",
    "new zealand": "Rest of World", "israel": "Rest of World",
    "kazakhstan": "Rest of World", "egypt": "Rest of World",
    "south africa": "Rest of World", "argentina": "Rest of World",
    "chile": "Rest of World", "qatar": "Rest of World",
}


NOISE = (
    "plant|plants|factory|gigafactory|facility|works|base|line|park|pilot|"
    "battery|batteries|cell|cells|energy|storage|sodium|ion|lithium|"
    "lfp|nmc|nca|super|new|the|inc|ltd|co|corp|technology|technologies|"
    "group|industrial|solutions|company|and|of"
)


def norm(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    # collapse common noise words that cause false distinct keys
    s = re.sub(rf"\b({NOISE})\b", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def key(plant, operator, country):
    return (norm(plant), norm(operator), norm(country))


def looks_like_header(row):
    joined = ",".join(row).lower()
    return "plant_name" in joined and "operator" in joined


def main():
    files = sorted(glob.glob(os.path.join(SEED_DIR, "*.csv")))
    if not files:
        print(f"No seed files in {SEED_DIR}/", file=sys.stderr)
        sys.exit(1)

    seen = {}
    rows = []
    per_region = {}
    dropped_dupes = 0
    unknown_countries = set()

    def region_for(base):
        # exact match first, then longest known-prefix match (handles
        # wave-2 filenames like china_wave2a, europe_extra, etc.)
        if base in REGION_FROM_FILE:
            return REGION_FROM_FILE[base]
        for token in sorted(REGION_FROM_FILE, key=len, reverse=True):
            if base.startswith(token):
                return REGION_FROM_FILE[token]
        return base

    for fp in files:
        base = os.path.splitext(os.path.basename(fp))[0]
        region = region_for(base)
        with open(fp, newline="") as fh:
            reader = csv.reader(fh)
            for raw in reader:
                if not raw or not any(c.strip() for c in raw):
                    continue
                if looks_like_header(raw):
                    continue
                plant = raw[0].strip() if len(raw) > 0 else ""
                operator = raw[1].strip() if len(raw) > 1 else ""
                country = raw[2].strip() if len(raw) > 2 else ""
                if not plant:
                    continue
                # region from country first, else filename-inferred
                row_region = COUNTRY_TO_REGION.get(country.strip().lower(), region)
                if country.strip().lower() not in COUNTRY_TO_REGION:
                    unknown_countries.add(country)
                k = key(plant, operator, country)
                if k in seen:
                    dropped_dupes += 1
                    continue
                seen[k] = True
                rows.append([plant, operator, country, row_region])
                per_region[row_region] = per_region.get(row_region, 0) + 1

    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["plant_name", "operator", "country", "region"])
        w.writerows(rows)

    print(f"Wrote {OUT}: {len(rows)} candidates ({dropped_dupes} duplicates dropped)")
    for reg, n in sorted(per_region.items(), key=lambda x: -x[1]):
        print(f"  {reg:16} {n}")
    if unknown_countries:
        print("WARNING unknown countries (defaulted to filename region):",
              sorted(unknown_countries))


if __name__ == "__main__":
    main()
