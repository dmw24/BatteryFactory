#!/usr/bin/env python3
"""Unallocated company capacity (D-028, owner request 2026-11-23).

For companies that disclose their total cell production capacity for a year, the part of that total that our
site-level rows do not account for is recorded as UNALLOCATED capacity: a company/year line with no site, no
coordinates and no plant id. It is added on top of the IEA-like Series D as Series E.

    python3 scripts/build_unallocated.py      # after scripts/build_timeseries.py

Inputs
  data/reference/company_capacity/*.csv   disclosed figures (worker brief: team/briefs/worker_company_capacity.md)
  data/reference/company_map.csv          DB id -> company (one company per id; JV sites included)
Rules (no double counting, no invention)
  - Only metric=capacity with basis year_end or annual_effective is used; planned/target figures never are.
    Per company-year, year_end is preferred over annual_effective; scope must be the company's whole lithium
    battery business (segment-only figures are skipped and reported).
  - Site sum = Series D (gwh_iea) of every active DB row mapped to the company, INCLUDING JV sites, restricted
    to China when the disclosed scope is china. Subtracting JV sites can only understate the remainder.
  - unallocated = max(0, disclosed - site sum). A negative difference is reported ("sites exceed disclosed"),
    never used to reduce anything.
  - Years without a disclosed figure get nothing (no interpolation or carry-forward).
Outputs: DuckDB table capacity_unallocated, capacity_unallocated.csv, and capacity_by_year_e.csv (Series E by year).
"""
import csv
import glob
import os

import sys

import duckdb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
from company_aliases import ALIAS  # noqa: E402
SINGLE_SEGMENT = {"Hithium": "ess_only"}   # companies whose whole cell business is one segment
HOME_REGION = {"LGES": "South Korea", "Samsung SDI": "South Korea", "SK On": "South Korea", "Panasonic": "Japan",
               "Envision AESC": "China"}

disc = []
for f in sorted(glob.glob("data/reference/company_capacity/*.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        r["_file"] = os.path.basename(f)
        r["_estimate"] = f.endswith("_estimates.csv")  # D-030: converted from Ah etc.; labelled, reported separately
        r["company"] = ALIAS.get((r.get("company") or "").strip(), (r.get("company") or "").strip())
        disc.append(r)
cmap, valid_to = {}, {}
for _r in csv.DictReader(open("data/reference/company_map.csv", encoding="utf-8")):
    if not _r["company"].startswith("("):
        cmap[_r["id"]] = _r["company"]
        if (_r.get("valid_to") or "").strip():
            valid_to[_r["id"]] = int(_r["valid_to"])   # ownership ended (e.g. CALB Luoyang 2021)

con = duckdb.connect("factories.db")
# all comparable rows (paused/cancelled rows carry capacity before 2025 in D, so they must be subtracted too — T111)
site = con.execute("""SELECT b.id, b.year, b.gwh_iea, f.region FROM capacity_by_year b
                      JOIN factories f ON f.id = b.id""").fetchall()


def site_sum(company, year, china_only):
    return sum(g or 0 for i, y, g, reg in site
               if y == year and cmap.get(i) == company and (not china_only or reg == "China")
               and y <= valid_to.get(i, 9999))


chosen, skipped = {}, []
for r in disc:
    if r.get("metric") != "capacity":
        continue
    scope = (r.get("scope") or "").lower()
    basis = (r.get("basis") or "").lower()
    try:
        val, year = float(r["capacity_gwh"]), int(r["year"])
    except (ValueError, KeyError, TypeError):
        skipped.append((r.get("company"), r.get("year"), "unparseable")); continue
    if basis not in ("year_end", "annual_effective"):
        skipped.append((r["company"], year, f"basis {basis}")); continue
    if any(s in scope for s in ("power_only", "ess_only", "consumer_only")) and SINGLE_SEGMENT.get(r["company"]) not in scope:
        skipped.append((r["company"], year, f"segment scope {scope}")); continue
    if not (scope.startswith("global") or scope.startswith("china")):
        skipped.append((r["company"], year, f"scope {scope}")); continue
    key = (r["company"], year)
    rank = 0 if basis == "year_end" else 1
    rank += 10 if r["_estimate"] else 0   # a disclosed GWh figure always beats a converted estimate
    if key not in chosen or rank < chosen[key][0]:
        chosen[key] = (rank, val, scope, basis, r)

out = []
for (company, year), (_, val, scope, basis, r) in sorted(chosen.items()):
    china_only = scope.startswith("china")
    ss = site_sum(company, year, china_only)
    un = max(0.0, val - ss)
    region = "China" if china_only else HOME_REGION.get(company, "China")
    out.append((company, year, val, round(ss, 1), round(un, 1), region, scope, basis,
                ("estimate;" if r["_estimate"] else "") + ("sites_exceed_disclosed" if val < ss else ""), r.get("source_url", ""), r.get("quote", "")[:300]))

con.execute("DROP TABLE IF EXISTS capacity_unallocated")
con.execute("""CREATE TABLE capacity_unallocated (company VARCHAR, year INTEGER, disclosed_gwh DOUBLE,
               sites_gwh DOUBLE, unallocated_gwh DOUBLE, region VARCHAR, scope VARCHAR, basis VARCHAR,
               flag VARCHAR, source_url VARCHAR, quote VARCHAR)""")
if out:
    con.executemany("INSERT INTO capacity_unallocated VALUES (?,?,?,?,?,?,?,?,?,?,?)", out)
con.execute("COPY (SELECT * FROM capacity_unallocated ORDER BY company, year) TO 'capacity_unallocated.csv' (HEADER)")
con.execute("""COPY (
    SELECT d.year, d.gwh_iea_like, coalesce(u.unalloc, 0) - coalesce(u.est, 0) AS gwh_unallocated_disclosed,
           coalesce(u.est, 0) AS gwh_unallocated_estimate,
           d.gwh_iea_like + coalesce(u.unalloc, 0) - coalesce(u.est, 0) AS gwh_series_e,
           d.gwh_iea_like + coalesce(u.unalloc, 0) AS gwh_series_e_incl_estimates
    FROM (SELECT year, round(sum(gwh_iea)) AS gwh_iea_like FROM capacity_by_year GROUP BY year) d
    LEFT JOIN (SELECT year, round(sum(unallocated_gwh)) AS unalloc,
                      round(sum(unallocated_gwh) FILTER (WHERE flag LIKE 'estimate%')) AS est
               FROM capacity_unallocated GROUP BY year) u
      USING (year) ORDER BY year) TO 'capacity_by_year_e.csv' (HEADER)""")
print(f"{len(out)} company-years used; skipped {len(skipped)}")
for row in out:
    print(f"  {row[0]:<14} {row[1]}  disclosed {row[2]:>7.1f}  sites {row[3]:>7.1f}  unallocated {row[4]:>7.1f} {row[8]}")
for s in skipped:
    print("  skipped:", s)
con.close()
