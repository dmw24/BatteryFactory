#!/usr/bin/env python3
"""v2 city-level coordinates for rows without any (lead patch, improvement round T089).

Reuses the offline gazetteer matcher of scripts/geocode_sites.py, but writes a rebuildable patch
(data/patches/T089_geo.json, action "fix") instead of editing the DB. To limit wrong matches it reads only the
row's plant_name and id slug (not the notes, which often name HQ or partner cities). Every filled row gets
geo_precision "city" and a [GEO=city:...] note; unmatched rows stay null.

    python3 scripts/geocode_v2.py && python3 scripts/rebuild.py
"""
import json
import os
import re
import subprocess
import sys

import duckdb
import geonamescache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, "scripts")
from geocode_sites import ALIASES, best_city, build_country_index, norm  # noqa: E402

subprocess.run([sys.executable, "scripts/rebuild.py"], check=True, capture_output=True,
               env={**os.environ, "REBUILD_EXCLUDE": "T089_geo.json"})
gc = geonamescache.GeonamesCache()
country_by_name = {norm(v["name"]): k for k, v in gc.get_countries().items()}
country_by_name.update(ALIASES)
idx = build_country_index(gc.get_cities())
con = duckdb.connect("factories.db", read_only=True)
rows = con.execute("""SELECT id, plant_name, country, coalesce(operator,'') || ' ' || coalesce(parent_company,'') FROM factories
                      WHERE (latitude IS NULL OR longitude IS NULL) AND coalesce(project_state,'active')='active'""").fetchall()
out, miss = [], 0
# Matches rejected on lead review (2026-11-24): place names that collide with a different town of the same name
# (Wuwei Anhui vs Gansu; Ibaraki prefecture vs Ibaraki city, Osaka) or with an industrial-park/district name.
REJECT = {"dongliao", "huayuan", "lixin", "longquan", "nanchuan", "wuwei", "ibaraki"}


def rightmost_city(text, cand, banned):
    """City named LAST in the text (plant location usually ends the name), ignoring operator/parent words."""
    t = norm(text)
    ranked, recs = cand
    best = None
    for nn in ranked:
        if nn in banned or any(nn in b or b in nn for b in banned if len(b) >= 4):
            continue
        if nn in REJECT or len(recs[nn]) > 1:   # homonyms in the same country (e.g. Wuwei, Anhui vs Gansu): ambiguous, skip
            continue
        for mt in re.finditer(r"\b" + re.escape(nn) + r"\b", t):
            key = (mt.start(), len(nn))
            if best is None or key > best[0]:
                h = max(recs[nn], key=lambda r: r[2])
                best = (key, (nn, h[0], h[1], h[2]))
    return best[1] if best else None


for rid, name, country, opr in rows:
    iso = country_by_name.get(norm(country or ""))
    cand = idx.get(iso) if iso else None
    banned = {w for w in re.findall(r"[a-z]{4,}", norm(opr))}
    m = cand and rightmost_city(name or "", cand, banned)
    if not m:
        miss += 1
        continue
    cname, lat, lon, _ = m
    disp = cname.title()
    out.append({"id": rid, "action": "fix",
                "fields": {"latitude": round(float(lat), 5), "longitude": round(float(lon), 5), "geo_precision": "city"},
                "notes": f"[GEO=city:{disp}] approximate city-centroid of {disp}, {country} (offline geonamescache, "
                         f"matched on plant name/id; T089 2026-11-24) - NOT a verified plant location."})
json.dump({"task": "T089", "verified_on": "2026-11-24", "sources": {}, "rows": out},
          open("data/patches/T089_geo.json", "w"), indent=1, ensure_ascii=False)
print(f"T089: {len(out)} rows geocoded at city level, {miss} unmatched (left null)")
