#!/usr/bin/env python3
"""Company utilisation view (owner upgrade list item 4, 2026-11-27).

For each company-year with a disclosed OUTPUT (产量/production) and a disclosed CAPACITY in
data/reference/company_capacity/*.csv, compute disclosed utilisation = output / capacity, and set our site-level
built nameplate (Series D) and producing capacity (Series C) for the same company against both. Writes
company_utilisation.csv. Output figures are lower bounds on capacity; this is a plausibility view, not data.
"""
import csv
import glob
import os
import sys
from collections import defaultdict

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, "scripts")
from company_aliases import ALIAS  # noqa: E402

cap, out = {}, {}
for f in sorted(glob.glob("data/reference/company_capacity/*.csv")):
    if f.endswith("_estimates.csv"):
        continue
    for r in csv.DictReader(open(f, encoding="utf-8")):
        comp = ALIAS.get(r["company"].strip(), r["company"].strip())
        try:
            y, v = int(r["year"]), float(r["capacity_gwh"])
        except (ValueError, TypeError):
            continue
        sc = (r.get("scope") or "").lower()
        if not (sc.startswith("global") or sc.startswith("china")) or any(s in sc for s in ("power_only", "consumer_only")):
            continue
        if r.get("metric") == "capacity" and (r.get("basis") or "") in ("year_end", "annual_effective"):
            cap.setdefault((comp, y), v)
        elif r.get("metric") == "output":
            out.setdefault((comp, y), v)
cmap = {}
for r in csv.DictReader(open("data/reference/company_map.csv", encoding="utf-8")):
    if not r["company"].startswith("("):
        cmap[r["id"]] = (r["company"], int(r["valid_to"]) if (r.get("valid_to") or "").strip() else 9999)
con = duckdb.connect("factories.db", read_only=True)
d, c = defaultdict(float), defaultdict(float)
for i, y, gd, gc in con.execute("SELECT id, year, gwh_built_nameplate, gwh_best FROM capacity_by_year").fetchall():
    if i in cmap and y <= cmap[i][1]:
        d[(cmap[i][0], y)] += gd or 0
        c[(cmap[i][0], y)] += gc or 0
rows = []
for (comp, y) in sorted(set(cap) | set(out)):
    o, k = out.get((comp, y)), cap.get((comp, y))
    rows.append([comp, y, k, o, round(100 * o / k, 1) if (o and k) else "", round(d[(comp, y)], 1), round(c[(comp, y)], 1),
                 round(100 * o / c[(comp, y)], 1) if (o and c[(comp, y)]) else ""])
with open("company_utilisation.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["company", "year", "disclosed_capacity_gwh", "disclosed_output_gwh", "disclosed_utilisation_pct",
                "our_built_nameplate_gwh", "our_producing_gwh", "output_vs_our_producing_pct"])
    w.writerows(rows)
for r in rows:
    print(r)
