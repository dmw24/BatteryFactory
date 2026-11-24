#!/usr/bin/env python3
"""Series F — modelled history backfill (D-033, owner 2026-11-24: "really fix history"). LABELLED ESTIMATE.

Many plants are known to have produced for years before the first year our sourced series (D) credits them, because
open sources only state their recent capacity. Series F fills those years with an explicit, simple model and keeps
it separate from the sourced series:

  - Only operational, active plants with a known start_year s whose sourced D is 0 in some years s <= y < f, where
    f is the first year D > 0. Plants without a start_year are not modelled (counted in the report).
  - Ramp: modelled(y) = D(f) * (y - s + 1) / (f - s + 1)  (linear build-up from first production to the first
    sourced figure). Years where D > 0 are never changed.
  - Company cap: where a company discloses total capacity for year y (data/reference/company_capacity, same rules
    as D-028), its sites' D + modelled may not exceed the disclosed total — the modelled part is scaled down to fit.
  - Unallocated company capacity is then recomputed against D + modelled, so nothing is counted twice.
  F = D + modelled + unallocated_vs(D + modelled).

    python3 scripts/build_history_model.py     # after build_timeseries.py and build_unallocated.py
Writes table capacity_history_model (per plant/year) and capacity_by_year_f.csv.
"""
import csv
import glob
import os
from collections import defaultdict

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FIRST, LAST = 2015, 2025

con = duckdb.connect("factories.db")
rows = con.execute("""SELECT b.id, b.year, b.gwh_iea, f.start_year FROM capacity_by_year b
                      JOIN factories_active f ON f.id = b.id WHERE f.status = 'operational'""").fetchall()
d = defaultdict(dict)
start = {}
for i, y, g, s in rows:
    d[i][y] = g or 0.0
    start[i] = s
cmap = {r["id"]: r["company"] for r in csv.DictReader(open("data/reference/company_map.csv", encoding="utf-8"))
        if not r["company"].startswith("(")}

# disclosed company capacity (same selection rules as build_unallocated.py, disclosed figures only)
import sys
sys.path.insert(0, "scripts")
from company_aliases import ALIAS  # noqa: E402
disc = {}
for f in sorted(glob.glob("data/reference/company_capacity/*.csv")):
    if f.endswith("_estimates.csv"):
        continue
    for r in csv.DictReader(open(f, encoding="utf-8")):
        comp = ALIAS.get(r["company"].strip(), r["company"].strip())
        try:
            y, v = int(r["year"]), float(r["capacity_gwh"])
        except (ValueError, TypeError):
            continue
        sc, ba = (r.get("scope") or "").lower(), (r.get("basis") or "").lower()
        if r.get("metric") != "capacity" or ba not in ("year_end", "annual_effective"):
            continue
        if not (sc.startswith("global") or sc.startswith("china")):
            continue
        if any(t in sc for t in ("power_only", "consumer_only")) or ("ess_only" in sc and comp != "Hithium"):
            continue
        rank = 0 if ba == "year_end" else 1
        if (comp, y) not in disc or rank < disc[(comp, y)][0]:
            disc[(comp, y)] = (rank, v)

model = defaultdict(dict)
capped = set()   # (id, year) values limited by a company total: company-level remainder, not a plant estimate
unmodelled_no_start = 0.0
for i, ser in d.items():
    s = start.get(i)
    pos = sorted(y for y, g in ser.items() if g > 0 and y <= LAST)
    if not pos:
        continue
    f = pos[0]
    if s is None:
        if f > FIRST:
            unmodelled_no_start += ser[f]
        continue
    s = int(s)                      # true start year in the ramp fraction (T102: no clamping to FIRST)
    if s >= f:
        continue
    for y in range(max(s, FIRST), f):
        model[i][y] = ser[f] * (y - s + 1) / (f - s + 1)

# company cap: capacity in year y cannot exceed what the company disclosed for y or any LATER year (capacity grows),
# so the bound is the smallest disclosed total from y onward
comps = {c for c, _ in disc}
bound = {}
for comp in comps:
    ys = sorted(y for c, y in disc if c == comp)
    for y in range(FIRST, LAST + 1):
        if (comp, y) in disc:
            bound[(comp, y)] = (0, disc[(comp, y)][1])
            continue
        before = [yy for yy in ys if yy < y]
        after = [yy for yy in ys if yy > y]
        if before and after:        # T102: between two disclosures interpolate the company total (bound, labelled)
            y0, y1 = max(before), min(after)
            v0, v1 = disc[(comp, y0)][1], disc[(comp, y1)][1]
            bound[(comp, y)] = (0, v0 + (v1 - v0) * (y - y0) / (y1 - y0))
        elif after:                 # before the first disclosure: capacity cannot exceed the next disclosed total
            bound[(comp, y)] = (0, disc[(comp, min(after))][1])
for (comp, y), (_, v) in bound.items():
    ids = [i for i in d if cmap.get(i) == comp]
    site = sum(d[i].get(y, 0.0) for i in ids)
    mod = sum(model[i].get(y, 0.0) for i in ids)
    if mod <= 0:
        continue
    room = max(0.0, v - site)
    if mod > room:
        k = room / mod
        for i in ids:
            if y in model[i]:
                model[i][y] *= k
                capped.add((i, y))

out = [(i, y, round(g, 3), (i, y) in capped) for i in model for y, g in model[i].items() if g > 0]
con.execute("DROP TABLE IF EXISTS capacity_history_model")
con.execute("CREATE TABLE capacity_history_model (id VARCHAR, year INTEGER, gwh_modelled DOUBLE, company_capped BOOLEAN)")
if out:
    con.executemany("INSERT INTO capacity_history_model VALUES (?,?,?,?)", out)

# unallocated vs D + modelled
unalloc = defaultdict(float)
for (comp, y), (_, v) in disc.items():
    ids = [i for i in d if cmap.get(i) == comp]
    site = sum(d[i].get(y, 0.0) + model[i].get(y, 0.0) for i in ids)
    unalloc[y] += max(0.0, v - site)
dtot = defaultdict(float)
for i, y, g in con.execute("SELECT id, year, gwh_iea FROM capacity_by_year").fetchall():
    dtot[y] += g or 0.0
mtot = defaultdict(float)
for i, y, g, _c in out:
    mtot[y] += g
with open("capacity_by_year_f.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["year", "gwh_iea_like_D", "gwh_modelled_backfill", "gwh_unallocated_vs_D_plus_model", "gwh_series_f"])
    for y in range(2015, 2031):
        w.writerow([y, round(dtot[y]), round(mtot[y]), round(unalloc[y]), round(dtot[y] + mtot[y] + unalloc[y])])
print(f"modelled {len(model)} plants; capacity of operational plants first credited after 2015 without a start_year "
      f"(not modelled): {unmodelled_no_start:.0f} GWh")
for y in range(2018, 2026):
    print(y, round(dtot[y]), round(mtot[y]), round(unalloc[y]), round(dtot[y] + mtot[y] + unalloc[y]))
