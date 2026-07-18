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


def norm(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    # collapse common noise words that cause false distinct keys
    s = re.sub(r"\b(plant|factory|gigafactory|facility|the|inc|ltd|co|corp)\b", "", s)
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

    for fp in files:
        base = os.path.splitext(os.path.basename(fp))[0]
        region = REGION_FROM_FILE.get(base, base)
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
                k = key(plant, operator, country)
                if k in seen:
                    dropped_dupes += 1
                    continue
                seen[k] = True
                rows.append([plant, operator, country, region])
                per_region[region] = per_region.get(region, 0) + 1

    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["plant_name", "operator", "country", "region"])
        w.writerows(rows)

    print(f"Wrote {OUT}: {len(rows)} candidates ({dropped_dupes} duplicates dropped)")
    for reg, n in sorted(per_region.items(), key=lambda x: -x[1]):
        print(f"  {reg:16} {n}")


if __name__ == "__main__":
    main()
