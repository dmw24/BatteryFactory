#!/usr/bin/env python3
"""Build a capacity-over-time (build-out) view from factories.db.

Each plant's capacity is placed in the year it comes online, so a given year's
total only includes plants actually online by then. This is the correct way to
get a comparable time series — it is NOT the (forbidden) cross-status sum of
nameplates. Timing model, per plant:

  * If capacity_by_year_json exists -> use it directly (GWh/yr per listed year),
    carried forward to HORIZON (the ramp already encodes the phase-in).
  * Else if a nameplate + an online year is known -> step to full nameplate in
    the online year (start_year, else capacity_ref_year, else announced_year),
    held flat to HORIZON.
  * Else -> undated: cannot be placed on the timeline (counted separately).

Writes table `capacity_by_year(id, year, gwh_online, region, status, hub_flag)`
and prints yearly totals. `hub_flag` marks rows whose capacity looks like a
hub/company-wide aggregate (double-count risk) so a conservative series can
exclude them.
"""
import json
import re
import duckdb

DB = "factories.db"
HORIZON = 2030
FIRST = 2015

HUB = re.compile(r"hub-?level|hub level|company-?wide|aggregate.{0,20}capacit|"
                 r"spanning (several|multiple|adjacent)|across (several|multiple|adjacent) "
                 r"(sites|bases|facilities|buildings)|company total|company-total", re.I)


def online_year(r):
    for k in ("start_year", "capacity_ref_year", "announced_year"):
        if r[k] is not None:
            return int(r[k])
    return None


def series_for(r):
    """Return {year: gwh_online} for one plant, or None if undated."""
    cby = r["capacity_by_year_json"]
    if cby:
        try:
            m = {int(y): float(v) for y, v in json.loads(cby).items()}
        except (ValueError, json.JSONDecodeError, AttributeError):
            m = None
        if m:
            out, last = {}, 0.0
            for y in range(min(m), HORIZON + 1):
                if y in m:
                    last = m[y]
                out[y] = last
            return out
    np = r["nameplate_capacity_gwh"]
    if np is not None:
        oy = online_year(r)
        if oy is None:
            return None
        return {y: np for y in range(max(oy, FIRST), HORIZON + 1)}
    return None


def main():
    con = duckdb.connect(DB)
    rows = con.execute("""
        SELECT id, region, status, nameplate_capacity_gwh, capacity_ref_year,
               start_year, announced_year, capacity_by_year_json, research_notes
        FROM factories
    """).fetchall()
    cols = [d[0] for d in con.description]
    R = [dict(zip(cols, r)) for r in rows]

    con.execute("DROP TABLE IF EXISTS capacity_by_year")
    con.execute("""CREATE TABLE capacity_by_year (
        id VARCHAR, year INTEGER, gwh_online DOUBLE,
        region VARCHAR, status VARCHAR, hub_flag BOOLEAN)""")

    undated = 0
    placed = 0
    ins = []
    for r in R:
        s = series_for(r)
        if s is None:
            if r["nameplate_capacity_gwh"] is not None:
                undated += 1
            continue
        placed += 1
        hub = bool(HUB.search(r["research_notes"] or ""))
        for y, g in s.items():
            ins.append((r["id"], y, g, r["region"], r["status"], hub))
    con.executemany("INSERT INTO capacity_by_year VALUES (?,?,?,?,?,?)", ins)

    print(f"Placed {placed} plants on the timeline; {undated} have a nameplate but "
          f"no datable online year (excluded from the curve).")

    print("\n=== Global capacity online by year (GWh/yr) ===")
    print(f"{'year':>6} | {'all rows':>10} | {'excl. hub-aggregates':>20} | {'China':>8}")
    for y in range(2018, HORIZON + 1):
        allv = con.execute("SELECT round(sum(gwh_online),0) FROM capacity_by_year WHERE year=?", [y]).fetchone()[0] or 0
        conserv = con.execute("SELECT round(sum(gwh_online),0) FROM capacity_by_year WHERE year=? AND NOT hub_flag", [y]).fetchone()[0] or 0
        chn = con.execute("SELECT round(sum(gwh_online),0) FROM capacity_by_year WHERE year=? AND region='China'", [y]).fetchone()[0] or 0
        print(f"{y:>6} | {allv:>10,.0f} | {conserv:>20,.0f} | {chn:>8,.0f}")

    # export
    con.execute("""COPY (
        SELECT year, round(sum(gwh_online),0) AS gwh_all,
               round(sum(gwh_online) FILTER (WHERE NOT hub_flag),0) AS gwh_excl_hub,
               round(sum(gwh_online) FILTER (WHERE region='China'),0) AS gwh_china
        FROM capacity_by_year GROUP BY year ORDER BY year)
        TO 'capacity_by_year.csv' (HEADER, DELIMITER ',')""")
    con.execute("""COPY (
        SELECT year, region, round(sum(gwh_online),0) AS gwh_online
        FROM capacity_by_year GROUP BY year, region ORDER BY year, region)
        TO 'capacity_by_year_region.csv' (HEADER, DELIMITER ',')""")
    print("\nWrote capacity_by_year.csv and capacity_by_year_region.csv")
    con.close()


if __name__ == "__main__":
    main()
