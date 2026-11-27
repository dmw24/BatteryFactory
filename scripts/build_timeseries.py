#!/usr/bin/env python3
"""Build a capacity-over-time (build-out) view from factories.db.

Per plant, capacity for each year is derived with this PRIORITY, best (real) first:

  1. capacity_timeline  — REAL dated, individually-sourced observations. Cumulative
     GWh is walked year by year from the sourced points (set on a cumulative_gwh
     point, increment on an added_gwh point) and carried forward at its last
     OBSERVED level between points. No ramp is invented. `basis` on the governing
     point marks each year firm (operational/commissioned) vs pipeline
     (announced_target/planned).  -> source_kind='real'
  2. capacity_by_year_json — phased figures researched as a single field.  -> 'phased'
  3. nameplate + online year — step to full nameplate at start_year/ref_year.
     A fallback where no real trajectory is published.  -> 'modelled'

A given year only includes plants online by then, so this is NOT a cross-status
nameplate sum. The `source_kind` and `firm` columns let us report exactly how
much of each year is real sourced data vs modelled fallback.
"""
import json
import re
import duckdb

DB = "factories.db"
HORIZON = 2030
FIRST = 2015
LAST_ACTUAL = 2025          # years <= this are "firm/online" for non-timeline plants

HUBRE = re.compile(r"hub-?level|company-?wide|aggregate.{0,20}capacit|multi-?base|"
                   r"across (several|multiple|adjacent) (sites|bases|facilities)", re.I)
FIRM_BASIS = {"operational", "commissioned"}
REF_FALLBACK = re.compile(r"ref_?year[^.;|]{0,40}fallback|fallback[^.;|]{0,20}ref_?year", re.I)
REF_PARTIAL = re.compile(r"remainder undated|latest dated phase", re.I)
REF_ANY = re.compile(r"ref_?year[^.;|]{0,40}fallback|fallback[^.;|]{0,20}ref_?year|remainder undated|latest dated phase", re.I)


def ref_basis(notes):
    """T083 audit fix: notes accumulate across tasks, so use the LAST statement about the reference year.
    'dated' = every phase in nameplate is dated -> D may credit full nameplate from capacity_ref_year;
    'partial' (D-021 'latest dated phase; remainder undated') and 'fallback' -> D credits dated steps only."""
    last = None
    for m in REF_ANY.finditer(notes or ""):
        last = m.group(0)
    if last is None:
        return "dated"
    return "partial" if REF_PARTIAL.fullmatch(last) or REF_PARTIAL.search(last) else "fallback"




def main():
    con = duckdb.connect(DB)
    rows = con.execute("""
        SELECT id, region, status, nameplate_capacity_gwh, capacity_ref_year,
               start_year, announced_year, capacity_by_year_json, capacity_timeline,
               research_notes, is_single_site, installed_capacity_gwh, installed_as_of,
               project_state, is_cell_manufacturer, site_type, chemistry
        FROM factories
        WHERE coalesce(is_cell_manufacturer, true)
    """).fetchall()
    cols = [d[0] for d in con.description]
    R = [dict(zip(cols, r)) for r in rows]
    # D-019: long-duration / non-Li chemistries are excluded from headline totals
    import csv as _csv, os as _os
    nc_path = "data/reference/non_comparable.csv"
    non_comparable = {row["id"] for row in _csv.DictReader(open(nc_path))} if _os.path.exists(nc_path) else set()
    # v1 timeline points whose cited page does not contain the number (scripts/check_timeline_sources.py)
    tc_path = "data/reference/reported/timeline_check.csv"
    bad_hist, bad_points = set(), set()
    if _os.path.exists(tc_path):
        tc = list(_csv.DictReader(open(tc_path)))
        ids_ = {x["id"] for x in tc}
        bad_hist = {i for i in ids_ if all(x["result"] == "NUMBER_MISSING" for x in tc if x["id"] == i)}
        bad_points = {(x["id"], int(x["year"])) for x in tc if x["result"] == "NUMBER_MISSING"}
    excluded = [r for r in R if r["id"] in non_comparable]
    R = [r for r in R if r["id"] not in non_comparable]
    print(f"excluded {len(excluded)} non-comparable rows (D-019), nameplate "
          f"{sum(r['nameplate_capacity_gwh'] or 0 for r in excluded):.1f} GWh")

    con.execute("DROP TABLE IF EXISTS capacity_by_year")
    con.execute("""CREATE TABLE capacity_by_year (
        id VARCHAR, year INTEGER, gwh_firm DOUBLE, gwh_pipeline DOUBLE,
        gwh_nameplate DOUBLE, region VARCHAR, status VARCHAR, source_kind VARCHAR, hub_flag BOOLEAN,
        gwh_best DOUBLE, best_basis VARCHAR, gwh_built_nameplate DOUBLE, built_basis VARCHAR, gwh_built_nameplate_high DOUBLE)""")


    # v3 (T102 audit): all per-plant logic lives in scripts/series_core.py (evidence precedence, no credit before
    # start, reported never overrides confirmed). Field tiers come from data/field_evidence.csv.
    import sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from series_core import compute
    tiers, step_quotes = {}, {}
    for e in _csv.DictReader(open("data/field_evidence.csv", encoding="utf-8")):
        if e["field"] == "capacity_by_year_json" and (e.get("tier") or "").strip() != "reported":
            step_quotes.setdefault(e["id"], []).append(e.get("quote") or "")
        k = tiers.setdefault(e["id"], {})
        tier = "reported" if (e.get("tier") or "").strip() == "reported" else "confirmed"
        if k.get(e["field"]) != "confirmed":
            k[e["field"]] = tier
    rf = {i: f for i, f in con.execute("SELECT id, reported_fields FROM factories").fetchall()}
    ins = []
    kinds = {}
    for r in R:
        r["reported_fields"] = rf.get(r["id"])
        ser = compute(r, tiers, step_quotes, bad_points, ref_basis(r["research_notes"]) == "dated")
        if not ser:
            continue
        hub = (r["is_single_site"] is False) or bool(HUBRE.search(r["research_notes"] or ""))
        kind = next(iter(ser.values()))["kind"]
        kinds[kind] = kinds.get(kind, 0) + 1
        for y, v in sorted(ser.items()):
            ins.append((r["id"], y, v["firm"], v["pipe"], v["npl"], r["region"], r["status"], v["kind"], hub,
                        v["best"], v["basis"], v["iea"], v["ibasis"], v["iea_high"]))
    con.executemany("INSERT INTO capacity_by_year VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ins)

    print("plants by data source:", kinds)
    # external benchmarks for side-by-side
    bench = {}
    try:
        import csv as _csv
        for row in _csv.DictReader(l for l in open("scripts/benchmarks.csv") if not l.startswith("#")):
            bench.setdefault(int(row["year"]), {})[row["source"]] = float(row["gwh"])
    except OSError:
        pass
    print("\n=== Capacity by year (GWh/yr): A=achieved online (floor) · B=installed nameplate (IEA/BNEF basis) · benchmarks ===")
    print(f"{'year':>6} | {'A online':>8} | {'%real':>5} | {'B nameplate':>11} | {'IEA':>5} | {'BNEF':>5} | {'China A':>7} | {'+pipe':>6}")
    for y in range(2018, HORIZON + 1):
        def s(col="gwh_firm", where=""):
            return con.execute(f"SELECT round(sum({col}),0) FROM capacity_by_year WHERE year={y} {where}").fetchone()[0] or 0
        a = s(); real = s("gwh_firm", "AND source_kind IN ('real','online_unquantified')")
        b = s("gwh_nameplate"); chn = s("gwh_firm", "AND region='China'"); pipe = s("gwh_pipeline"); cbest = s("gwh_best")
        pct = (100 * real / a) if a else 0
        iea = bench.get(y, {}).get("IEA", ""); bnef = bench.get(y, {}).get("BNEF", "")
        print(f"{y:>6} | {a:>8,.0f} | C {cbest:>6,.0f} | {pct:>4.0f}% | {b:>11,.0f} | {str(int(iea)) if iea else '-':>5} | {str(int(bnef)) if bnef else '-':>5} | {chn:>7,.0f} | {pipe:>6,.0f}")

    con.execute("""COPY (
        SELECT year,
               round(sum(gwh_firm),0) AS gwh_confirmed_installed,
               round(sum(gwh_firm) FILTER (WHERE source_kind IN ('real','online_unquantified')),0) AS gwh_confirmed_installed_sourced,
               round(sum(gwh_nameplate),0) AS gwh_upper_fill_B,
               round(sum(gwh_best),0) AS gwh_producing,
               round(sum(gwh_built_nameplate),0) AS gwh_built_nameplate,
               round(sum(gwh_built_nameplate_high),0) AS gwh_built_nameplate_high,
               round(sum(gwh_pipeline),0) AS gwh_pipeline_additional,
               round(sum(gwh_firm) FILTER (WHERE region='China'),0) AS gwh_online_china
        FROM capacity_by_year GROUP BY year ORDER BY year)
        TO 'capacity_by_year.csv' (HEADER, DELIMITER ',')""")
    con.execute("""COPY (
        SELECT year, region,
               round(sum(gwh_firm),0) AS gwh_confirmed_installed,
               round(sum(gwh_pipeline),0) AS gwh_pipeline,
               round(sum(gwh_best),0) AS gwh_producing,
               round(sum(gwh_built_nameplate),0) AS gwh_built_nameplate,
               round(sum(gwh_built_nameplate_high),0) AS gwh_built_nameplate_high
        FROM capacity_by_year GROUP BY year, region ORDER BY year, region)
        TO 'capacity_by_year_region.csv' (HEADER, DELIMITER ',')""")
    print("\nWrote capacity_by_year.csv and capacity_by_year_region.csv")
    con.close()


if __name__ == "__main__":
    main()
