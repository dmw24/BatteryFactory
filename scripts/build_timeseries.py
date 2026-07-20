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


def _walk(pts):
    """Cumulative level by year from sourced points (set on cumulative, add on
    added), carried forward to HORIZON. Returns {year: gwh} or {}."""
    if not pts:
        return {}
    pts = sorted(pts, key=lambda p: (p["year"], 0 if p.get("cumulative_gwh") is None else 1))
    level, per_year = None, {}
    for p in pts:
        y = int(p["year"])
        if p.get("cumulative_gwh") is not None:
            level = float(p["cumulative_gwh"])
        elif p.get("added_gwh") is not None:
            level = (level or 0) + float(p["added_gwh"])
        if level is not None:
            per_year[y] = level
    if not per_year:
        return {}
    out, cur = {}, None
    for y in range(min(per_year), HORIZON + 1):
        if y in per_year:
            cur = per_year[y]
        if cur is not None:
            out[y] = cur
    return out


def timeline_series(tl):
    """Return {year: (firm_gwh, pipeline_gwh)}. Firm = operational/commissioned
    capacity actually online; pipeline = additional announced/planned capacity.
    Planned points NEVER count as online (fixes early-year inflation)."""
    pts = [p for p in tl if isinstance(p, dict) and p.get("year")]
    firm = _walk([p for p in pts if p.get("basis") in FIRM_BASIS])
    allp = _walk(pts)                      # firm + planned/announced
    if not firm and not allp:
        return None
    years = range(min([*firm, *allp]), HORIZON + 1)
    out = {}
    for y in years:
        f = firm.get(y, 0.0)
        tgt = allp.get(y, 0.0)
        out[y] = (f, max(0.0, tgt - f))    # pipeline = target above firm
    return out


def series_for(r):
    """Return ({year: firm_gwh}, {year: pipeline_gwh}, source_kind) or (None,)*3."""
    tl = r["capacity_timeline"]
    if tl:
        try:
            arr = json.loads(tl)
        except (json.JSONDecodeError, TypeError):
            arr = None
        if arr:
            s = timeline_series(arr)
            if s:
                return ({y: v[0] for y, v in s.items()},
                        {y: v[1] for y, v in s.items()}, "real")
    cby = r["capacity_by_year_json"]
    if cby:
        try:
            m = {int(y): float(v) for y, v in json.loads(cby).items()}
        except (ValueError, json.JSONDecodeError, AttributeError):
            m = None
        if m:
            carried, last = {}, 0.0
            for y in range(min(m), HORIZON + 1):
                if y in m:
                    last = m[y]
                carried[y] = last
            frozen = carried.get(LAST_ACTUAL, carried[max(y for y in carried if y <= LAST_ACTUAL)] if any(y <= LAST_ACTUAL for y in carried) else 0.0)
            firm = {y: (carried[y] if y <= LAST_ACTUAL else frozen) for y in carried}
            pipe = {y: max(0.0, carried[y] - firm[y]) for y in carried}
            return firm, pipe, "phased"
    np = r["nameplate_capacity_gwh"]
    if np is not None:
        oy = next((int(r[k]) for k in ("start_year", "capacity_ref_year", "announced_year")
                   if r[k] is not None), None)
        if oy is None:
            return None, None, None
        g = {y: np for y in range(max(oy, FIRST), HORIZON + 1)}
        online_now = oy <= LAST_ACTUAL
        firm = {y: (np if online_now else 0.0) for y in g}
        pipe = {y: (0.0 if online_now else np) for y in g}
        return firm, pipe, "modelled"
    return None, None, None


def main():
    con = duckdb.connect(DB)
    rows = con.execute("""
        SELECT id, region, status, nameplate_capacity_gwh, capacity_ref_year,
               start_year, announced_year, capacity_by_year_json, capacity_timeline,
               research_notes, is_single_site
        FROM factories
    """).fetchall()
    cols = [d[0] for d in con.description]
    R = [dict(zip(cols, r)) for r in rows]

    con.execute("DROP TABLE IF EXISTS capacity_by_year")
    con.execute("""CREATE TABLE capacity_by_year (
        id VARCHAR, year INTEGER, gwh_firm DOUBLE, gwh_pipeline DOUBLE,
        gwh_nameplate DOUBLE, region VARCHAR, status VARCHAR, source_kind VARCHAR, hub_flag BOOLEAN)""")

    def online_year(r):
        """First operational/commissioned timeline year, else start/ref/announced."""
        tl = r["capacity_timeline"]
        if tl:
            try:
                pts = [p for p in json.loads(tl)
                       if isinstance(p, dict) and p.get("basis") in FIRM_BASIS and p.get("year")]
                if pts:
                    return min(int(p["year"]) for p in pts)
            except (json.JSONDecodeError, TypeError):
                pass
        for k in ("start_year", "capacity_ref_year", "announced_year"):
            if r[k] is not None:
                return int(r[k])
        return None

    ins = []
    kinds = {"real": 0, "phased": 0, "modelled": 0, "online_unquantified": 0, "undated": 0}
    for r in R:
        firm, pipe, kind = series_for(r)
        if firm is None:
            if r["nameplate_capacity_gwh"] is not None:
                kinds["undated"] += 1
            continue
        # Coverage bucket: operational-status plant with a timeline but no firm capacity
        # anywhere through the current year => we know it is online but cannot quantify it.
        if (kind == "real" and r["status"] == "operational"
                and max([firm[y] for y in firm if y <= LAST_ACTUAL] or [0]) == 0):
            kind = "online_unquantified"
        kinds[kind] += 1
        hub = (r["is_single_site"] is False) or bool(HUBRE.search(r["research_notes"] or ""))
        # Series B — installed nameplate (IEA/BNEF basis): full nameplate of an
        # OPERATIONAL plant credited from the year it came online, held to HORIZON.
        np = r["nameplate_capacity_gwh"]
        oy = online_year(r)
        for y in firm:
            npl = (np if (np is not None and r["status"] == "operational"
                          and oy is not None and y >= oy) else 0.0)
            ins.append((r["id"], y, firm[y], pipe.get(y, 0.0), npl,
                        r["region"], r["status"], kind, hub))
    con.executemany("INSERT INTO capacity_by_year VALUES (?,?,?,?,?,?,?,?,?)", ins)

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
        b = s("gwh_nameplate"); chn = s("gwh_firm", "AND region='China'"); pipe = s("gwh_pipeline")
        pct = (100 * real / a) if a else 0
        iea = bench.get(y, {}).get("IEA", ""); bnef = bench.get(y, {}).get("BNEF", "")
        print(f"{y:>6} | {a:>8,.0f} | {pct:>4.0f}% | {b:>11,.0f} | {str(int(iea)) if iea else '-':>5} | {str(int(bnef)) if bnef else '-':>5} | {chn:>7,.0f} | {pipe:>6,.0f}")

    con.execute("""COPY (
        SELECT year,
               round(sum(gwh_firm),0) AS gwh_online_achieved,
               round(sum(gwh_firm) FILTER (WHERE source_kind IN ('real','online_unquantified')),0) AS gwh_online_real_sourced,
               round(sum(gwh_nameplate),0) AS gwh_installed_nameplate,
               round(sum(gwh_pipeline),0) AS gwh_pipeline_additional,
               round(sum(gwh_firm) FILTER (WHERE region='China'),0) AS gwh_online_china
        FROM capacity_by_year GROUP BY year ORDER BY year)
        TO 'capacity_by_year.csv' (HEADER, DELIMITER ',')""")
    con.execute("""COPY (
        SELECT year, region,
               round(sum(gwh_firm),0) AS gwh_online_firm,
               round(sum(gwh_pipeline),0) AS gwh_pipeline
        FROM capacity_by_year GROUP BY year, region ORDER BY year, region)
        TO 'capacity_by_year_region.csv' (HEADER, DELIMITER ',')""")
    print("\nWrote capacity_by_year.csv and capacity_by_year_region.csv")
    con.close()


if __name__ == "__main__":
    main()
