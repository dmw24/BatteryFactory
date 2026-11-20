#!/usr/bin/env python3
"""Flag coordinates that sit far from the city named in the plant name (lead QA, T030).

    python3 scripts/geo_check.py [--km 150] [--write data/patches/T030_geo.json]

Uses the offline geonamescache gazetteer (same matcher as scripts/geocode_sites.py). Only rows
whose plant_name names a gazetteer city in the row's country are testable. With --write, emits a
lead `fix` patch nulling flagged coordinates (never guessing a replacement).
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import geonamescache
import geocode_sites as g

def hav(a, b, c, d):
    r = math.radians
    x = math.sin(r(c - a) / 2) ** 2 + math.cos(r(a)) * math.cos(r(c)) * math.sin(r(d - b) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(x))

km = float(sys.argv[sys.argv.index("--km") + 1]) if "--km" in sys.argv else 150
gc = geonamescache.GeonamesCache()
idx = g.build_country_index(gc.get_cities())
cby = {g.norm(v["name"]): k for k, v in gc.get_countries().items()}
cby.update(g.ALIASES)
d = pd.read_csv("factories_export.csv")
flag, tested = [], 0
for _, r in d[d.latitude.notna()].iterrows():
    cc = cby.get(g.norm(str(r.country)))
    if not cc or cc not in idx:
        continue
    hit = g.best_city(str(r.plant_name), idx[cc])
    if not hit:
        continue
    tested += 1
    dist = hav(r.latitude, r.longitude, hit[1], hit[2])
    if dist > km:
        flag.append((r.id, hit[0], round(dist), r.geo_precision))
print(f"tested {tested} rows; {len(flag)} more than {km:.0f} km from the city in their name")
for f in flag:
    print("FLAG", *f)
if "--write" in sys.argv:
    out = sys.argv[sys.argv.index("--write") + 1]
    rows = [{"id": i, "action": "fix", "fields": {"latitude": None, "longitude": None, "geo_precision": "none"},
             "notes": f"coordinates nulled: {dist} km from '{city}' named in plant_name (scripts/geo_check.py)"}
            for i, city, dist, _ in flag]
    json.dump({"task": "T030", "verified_on": "2026-11-20", "sources": {}, "rows": rows}, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {out}")
