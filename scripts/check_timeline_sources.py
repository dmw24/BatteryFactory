#!/usr/bin/env python3
"""Check v1 capacity_timeline points that feed Series C (best_basis = reported_v1_timeline):
fetch each cited source_url and test whether the point's GWh number appears on the page.
Writes data/reference/reported/timeline_check.csv (id, year, gwh, url, result). Network-dependent."""
import csv, json, os, re, sys
sys.path.insert(0, "checks")
import duckdb
from verify_quotes import fetch, norm
con = duckdb.connect("factories.db", read_only=True)
ids = [r[0] for r in con.execute("select distinct id from capacity_by_year where year=2025 and best_basis='reported_v1_timeline' and gwh_best>0").fetchall()]
rows = con.execute(f"select id, capacity_timeline from factories where id in ({','.join('?'*len(ids))})", ids).fetchall()
out, cache = [], {}
for rid, tl in rows:
    for p in json.loads(tl or "[]"):
        if not isinstance(p, dict) or p.get("basis") not in ("operational", "commissioned"):
            continue
        g = p.get("cumulative_gwh") if p.get("cumulative_gwh") is not None else p.get("added_gwh")
        url = p.get("source_url")
        if g is None or not url:
            continue
        try:
            if url not in cache:
                cache[url] = norm(fetch(url))
            page = cache[url]
            num = ("%g" % float(g))
            hit = bool(re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d])\s*(gwh|吉瓦时|gw)", page))
            res = "NUMBER_FOUND" if hit else "NUMBER_MISSING"
        except Exception as e:  # noqa: BLE001
            res = "FETCH_FAIL"
        out.append(dict(id=rid, year=p.get("year"), gwh=g, url=url, result=res))
os.makedirs("data/reference/reported", exist_ok=True)
with open("data/reference/reported/timeline_check.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "year", "gwh", "url", "result"]); w.writeheader(); w.writerows(out)
from collections import Counter
print(len(ids), "plants;", len(out), "points;", Counter(r["result"] for r in out))
