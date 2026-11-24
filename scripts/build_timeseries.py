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


def _with_installed(r):
    """v2 (post-FINAL sweep): Series A uses only data the re-verification supports.
    - Plant must be operational. Otherwise no online capacity.
    - The anchor is installed_capacity_gwh at installed_as_of (v2, sourced). With no anchor the plant is
      'online_unquantified' (counted 0), never filled from v1 timelines.
    - v1 capacity_timeline firm points are kept only BEFORE the anchor year and capped at the anchor
      (sourced history), never after it.
    - The full nameplate at capacity_ref_year is a 'planned' point (pipeline only)."""
    if r.get("status") != "operational":
        pts = []
    else:
        inst, asof = r.get("installed_capacity_gwh"), r.get("installed_as_of")
        if inst is None or not asof:
            return json.dumps([{"year": int(r["start_year"] or 2025), "cumulative_gwh": 0.0, "basis": "operational"}]) \
                if r.get("start_year") else None
        y = int(str(asof)[:4])
        hist = []
        if r["capacity_timeline"]:
            try:
                hist = [p for p in json.loads(r["capacity_timeline"]) if isinstance(p, dict)
                        and p.get("basis") in FIRM_BASIS and p.get("year") and int(p["year"]) < y]
            except (json.JSONDecodeError, TypeError):
                hist = []
        for p in hist:
            if p.get("cumulative_gwh") is not None:
                p["cumulative_gwh"] = min(float(p["cumulative_gwh"]), float(inst))
        pts = [p for p in hist if p.get("cumulative_gwh") is not None] + \
              [{"year": y, "cumulative_gwh": float(inst), "basis": "operational"}]
    np, ry = r["nameplate_capacity_gwh"], r["capacity_ref_year"]
    if np is not None and ry is not None:
        pts.append({"year": int(ry), "cumulative_gwh": float(np), "basis": "planned"})
    return json.dumps(pts) if pts else None


def series_for(r):
    """Return ({year: firm_gwh}, {year: pipeline_gwh}, source_kind) or (None,)*3."""
    tl = _with_installed(r)
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
    cby = None  # v2: phased/modelled firm paths disabled; pipeline-only rows handled below
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
    if np is not None and r.get("status") != "operational":
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
    bad_hist = set()
    if _os.path.exists(tc_path):
        tc = list(_csv.DictReader(open(tc_path)))
        ids_ = {x["id"] for x in tc}
        bad_hist = {i for i in ids_ if all(x["result"] == "NUMBER_MISSING" for x in tc if x["id"] == i)}
    excluded = [r for r in R if r["id"] in non_comparable]
    R = [r for r in R if r["id"] not in non_comparable]
    print(f"excluded {len(excluded)} non-comparable rows (D-019), nameplate "
          f"{sum(r['nameplate_capacity_gwh'] or 0 for r in excluded):.1f} GWh")

    con.execute("DROP TABLE IF EXISTS capacity_by_year")
    con.execute("""CREATE TABLE capacity_by_year (
        id VARCHAR, year INTEGER, gwh_firm DOUBLE, gwh_pipeline DOUBLE,
        gwh_nameplate DOUBLE, region VARCHAR, status VARCHAR, source_kind VARCHAR, hub_flag BOOLEAN,
        gwh_best DOUBLE, best_basis VARCHAR, gwh_iea DOUBLE, iea_basis VARCHAR, gwh_iea_high DOUBLE)""")

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
        if (r.get("project_state") or "active") != "active":
            # D-018 / cancelled: no online capacity from the current year on, no pipeline
            for y in list(firm):
                if y >= LAST_ACTUAL:
                    firm[y] = 0.0
                    pipe[y] = 0.0
        kinds[kind] += 1
        hub = (r["is_single_site"] is False) or bool(HUBRE.search(r["research_notes"] or ""))
        # Series B — installed nameplate (IEA/BNEF basis): full nameplate of an
        # OPERATIONAL plant credited from the year it came online, held to HORIZON.
        np = r["nameplate_capacity_gwh"]
        oy = online_year(r)
        active = (r.get("project_state") or "active") == "active"
        reported_hist = {}
        if kind != "real" and r["capacity_timeline"]:
            try:
                reported_hist = _walk([p for p in json.loads(r["capacity_timeline"])
                                       if isinstance(p, dict) and p.get("basis") in FIRM_BASIS and p.get("year")])
            except (json.JSONDecodeError, TypeError):
                reported_hist = {}
        if kind != "real" and not reported_hist and r["capacity_by_year_json"]:
            try:  # reported/phased ramp, carried flat; only years up to the current year count as online
                m = {int(k): float(v) for k, v in json.loads(r["capacity_by_year_json"]).items() if v is not None}
                last = 0.0
                for yy in range(min(m), HORIZON + 1):
                    last = m.get(yy, last) if yy <= LAST_ACTUAL + 1 else last
                    reported_hist[yy] = last
            except (ValueError, json.JSONDecodeError, AttributeError, TypeError):
                reported_hist = {}
        has_sourced = kind in ("real", "phased")
        # Series D (IEA-like, D-027): design nameplate of commissioned lines. Credits the full site nameplate once
        # its last phase is due (capacity_ref_year <= y) when that year is a DATED phase year (not the
        # publication-year fallback), plus sourced dated phase steps (capacity_by_year_json); never less than C.
        ry = r["capacity_ref_year"]
        ry_fallback = ref_basis(r["research_notes"]) != "dated"
        steps = {}
        if r["capacity_by_year_json"]:
            try:
                steps = {int(k): float(v) for k, v in json.loads(r["capacity_by_year_json"]).items() if v is not None}
            except (ValueError, json.JSONDecodeError, AttributeError, TypeError):
                steps = {}
        for y in firm:
            if kind == "real":
                npl = firm[y]                       # v2: sourced installed level
            else:
                npl = (np if (np is not None and r["status"] == "operational" and (active or y <= LAST_ACTUAL)
                              and oy is not None and y >= oy) else 0.0)
            # Series C (best estimate, D-024): confirmed level where sourced; else reported v1 history
            # (capped at nameplate); else the nameplate fill used by B.
            if kind == "real":
                best, basis = firm[y], "confirmed"
            elif r["id"] in bad_hist:
                best, basis = 0.0, "unsupported_v1_timeline"
            elif npl and reported_hist:
                best, basis = min(reported_hist.get(y, 0.0), np or 1e9), "reported_v1_timeline"
            else:
                best, basis = npl, ("nameplate_fill" if npl else "none")
            iea, ibasis = best, "as_best"
            if r["status"] == "operational" and (active or y < LAST_ACTUAL) and oy is not None and y >= oy:
                step = max([v for k, v in steps.items() if k <= y] or [0.0])
                if np is not None:
                    step = min(step, np)
                if step > iea:
                    iea, ibasis = step, "dated_phase_step"
                if np is not None and ry is not None and int(ry) <= y and not ry_fallback and np > iea:
                    iea, ibasis = np, "full_nameplate_dated"
            # D-high: also credits plans whose ref year is only the publication-year fallback (upper bound)
            iea_high = iea
            if (r["status"] == "operational" and (active or y < LAST_ACTUAL) and np is not None and ry is not None
                    and int(ry) <= y and oy is not None and y >= oy):
                iea_high = max(iea, np)
            ins.append((r["id"], y, firm[y], pipe.get(y, 0.0), npl,
                        r["region"], r["status"], kind, hub, best, basis, iea, ibasis, iea_high))
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
               round(sum(gwh_firm),0) AS gwh_online_achieved,
               round(sum(gwh_firm) FILTER (WHERE source_kind IN ('real','online_unquantified')),0) AS gwh_online_real_sourced,
               round(sum(gwh_nameplate),0) AS gwh_installed_nameplate,
               round(sum(gwh_best),0) AS gwh_best_estimate,
               round(sum(gwh_iea),0) AS gwh_iea_like_commissioned,
               round(sum(gwh_iea_high),0) AS gwh_iea_like_high,
               round(sum(gwh_pipeline),0) AS gwh_pipeline_additional,
               round(sum(gwh_firm) FILTER (WHERE region='China'),0) AS gwh_online_china
        FROM capacity_by_year GROUP BY year ORDER BY year)
        TO 'capacity_by_year.csv' (HEADER, DELIMITER ',')""")
    con.execute("""COPY (
        SELECT year, region,
               round(sum(gwh_firm),0) AS gwh_online_firm,
               round(sum(gwh_pipeline),0) AS gwh_pipeline,
               round(sum(gwh_best),0) AS gwh_best_estimate,
               round(sum(gwh_iea),0) AS gwh_iea_like_commissioned,
               round(sum(gwh_iea_high),0) AS gwh_iea_like_high
        FROM capacity_by_year GROUP BY year, region ORDER BY year, region)
        TO 'capacity_by_year_region.csv' (HEADER, DELIMITER ',')""")
    print("\nWrote capacity_by_year.csv and capacity_by_year_region.csv")
    con.close()


if __name__ == "__main__":
    main()
