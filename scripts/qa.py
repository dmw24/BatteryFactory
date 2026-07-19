#!/usr/bin/env python3
"""Step 4 QA — generate qa_report.md from factories.db.

Flags, per the brief:
  1. Suspected duplicate sites under different names.
  2. Rows whose capacity looks like a hub/company-wide aggregate (double-count risk)
     or whose phased ramp exceeds the stated nameplate.
  3. Rows with confidence < 0.5.
  4. Totals by status and by region x status — NEVER summed across status.
Plus: non-cell sites flagged by researchers (is_cell_manufacturer = false).
"""
import re
import json
import duckdb

DB = "factories.db"
OUT = "qa_report.md"

STOP = {
    "plant", "factory", "gigafactory", "giga", "battery", "batteries", "cell",
    "cells", "base", "works", "energy", "new", "power", "the", "co", "ltd",
    "manufacturing", "storage", "lfp", "nmc", "ncm", "ternary", "sodium", "ion",
    "production", "line", "phase", "complex", "park", "industrial", "site",
    "company", "solutions", "technology", "technologies", "gwh", "north",
    "south", "corridor", "super", "systems", "group", "inc",
    # generic branding / industrial-park words seen in Chinese & JV plant names
    "and", "times", "zero", "carbon", "net", "smart", "intelligent", "city",
    "blade", "project", "area", "type", "scib", "ppes", "eastern", "central",
    "advanced", "green", "clean", "district", "zone", "hi", "tech", "high",
    "cylindrical", "prismatic", "pouch", "ev", "ess", "findreams",
    # Chinese provinces / regions — cause province-level (not site-level) matches
    "sichuan", "qinghai", "jiangsu", "guangdong", "zhejiang", "anhui", "hubei",
    "hunan", "shandong", "henan", "hebei", "fujian", "jiangxi", "gansu",
    "shaanxi", "yunnan", "guizhou", "liaoning", "jilin", "heilongjiang",
    "guangxi", "mongolia", "xinjiang", "ningxia", "hainan", "shanxi",
}


def toks(s):
    words = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split()
    return {w for w in words if w not in STOP and len(w) > 2 and not w.isdigit()}


def op_core(s):
    # first two significant tokens of the operator, order-independent set
    return frozenset(list(toks(s))[:3])


def main():
    con = duckdb.connect(DB)
    rows = con.execute("""
        SELECT id, plant_name, operator, parent_company, country, region, status,
               nameplate_capacity_gwh, capacity_ref_year, capacity_by_year_json,
               latitude, longitude, confidence, is_cell_manufacturer, research_notes
        FROM factories
    """).fetchall()
    cols = [d[0] for d in con.description]
    R = [dict(zip(cols, r)) for r in rows]

    # ---- 1. Suspected duplicates ----
    dupes = []
    # (a) shared coordinates (rounded to ~11 km)
    coord = {}
    for r in R:
        if r["latitude"] is not None and r["longitude"] is not None:
            k = (round(r["latitude"], 1), round(r["longitude"], 1))
            coord.setdefault(k, []).append(r)
    for k, grp in coord.items():
        if len(grp) > 1:
            dupes.append(("same coordinates ~" + str(k), [g["plant_name"] for g in grp],
                          [g["id"] for g in grp]))
    # (b) same country + related operator + a shared LOCATION token.
    # Location tokens exclude the operator/parent name, so two different plants of
    # the same operator (e.g. "CATL Ningde" vs "CATL Liyang") are NOT flagged;
    # only ones that also share a place word (a genuine same-site risk) are.
    def loc_tokens(r):
        return toks(r["plant_name"]) - toks(r["operator"]) - toks(r["parent_company"])
    # A place word should be rare across the DB; a token appearing in many plants
    # is a branding/descriptor word, not a location. Count global doc-frequency.
    from collections import Counter
    docfreq = Counter()
    for r in R:
        for t in loc_tokens(r):
            docfreq[t] += 1
    seen_pairs = set()
    for i in range(len(R)):
        for j in range(i + 1, len(R)):
            a, b = R[i], R[j]
            if a["country"] != b["country"]:
                continue
            oa, ob = toks(a["operator"]), toks(b["operator"])
            if not (oa & ob):                      # operators must be related
                continue
            shared = loc_tokens(a) & loc_tokens(b)  # ...and share a place word
            shared = {t for t in shared if docfreq[t] <= 3}  # rare => a real place
            if not shared:
                continue
            key = tuple(sorted((a["id"], b["id"])))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            dupes.append(("same operator + shared location token '" + "/".join(sorted(shared)) + "'",
                          [a["plant_name"], b["plant_name"]], [a["id"], b["id"]]))

    # ---- 2. Capacity / double-count flags ----
    AGG = re.compile(
        r"hub-?level|hub level|company-?wide|aggregate (operational |nameplate )?capacit|"
        r"combined [\w -]{0,30}capacit|total [\w -]{0,20}capacit[\w ]{0,20}(across|spanning)|"
        r"spanning (several|multiple|adjacent)|across (several|multiple|adjacent) "
        r"(sites|bases|facilities|buildings|plants)|sum of|should not be summed|"
        r"not be summed|company-total|company total", re.I)
    cap_flags = []
    for r in R:
        notes = r["research_notes"] or ""
        np = r["nameplate_capacity_gwh"]
        if np is not None and AGG.search(notes):
            cap_flags.append((r, "capacity may be a hub/company-wide aggregate (double-count risk)"))
            continue
        # phased ramp exceeds nameplate
        cby = r["capacity_by_year_json"]
        if np is not None and cby:
            try:
                m = max(float(v) for v in json.loads(cby).values())
                if m > np * 1.01:
                    cap_flags.append((r, f"phased ramp max {m} GWh exceeds nameplate {np} GWh"))
            except (ValueError, json.JSONDecodeError, AttributeError):
                pass

    # missing capacity on live cell sites
    missing_cap = [r for r in R if r["is_cell_manufacturer"]
                   and r["status"] in ("operational", "under_construction")
                   and r["nameplate_capacity_gwh"] is None]

    # ---- 3. Low confidence ----
    lowconf = sorted([r for r in R if (r["confidence"] or 0) < 0.5],
                     key=lambda x: x["confidence"] or 0)

    # ---- non-cell flagged ----
    noncell = [r for r in R if r["is_cell_manufacturer"] is False]

    # ---- 4. Totals by status (capacity NEVER summed across status) ----
    status_tot = con.execute("""
        SELECT COALESCE(status,'(unknown)') s, count(*) n,
               round(sum(nameplate_capacity_gwh),0) gwh
        FROM factories GROUP BY 1 ORDER BY n DESC
    """).fetchall()
    region_status = con.execute("""
        SELECT region, COALESCE(status,'(unknown)') s, count(*) n,
               round(sum(nameplate_capacity_gwh),0) gwh
        FROM factories GROUP BY 1,2 ORDER BY region, s
    """).fetchall()

    # ---- write report ----
    L = []
    w = L.append
    w("# Battery Gigafactory Database — QA report\n")
    w(f"Generated from `factories.db`. Total rows: **{len(R)}**. "
      f"Confirmed cell manufacturers: **{sum(1 for r in R if r['is_cell_manufacturer'])}**. "
      f"Flagged non-cell (pack/material/recycling, kept and tagged): **{len(noncell)}**.\n")
    w("> Capacity is annual GWh/year at nameplate. Totals are grouped by status and "
      "are **never summed across statuses** — announced, under-construction and "
      "operational capacity are distinct and must not be added together.\n")

    w("\n## 4. Totals by status (capacity never summed across status)\n")
    w("| status | plants | Σ nameplate GWh/yr |")
    w("|---|---:|---:|")
    for s, n, g in status_tot:
        w(f"| {s} | {n} | {g if g is not None else '—'} |")
    w("\n### Region × status matrix\n")
    w("| region | status | plants | Σ nameplate GWh/yr |")
    w("|---|---|---:|---:|")
    for reg, s, n, g in region_status:
        w(f"| {reg} | {s} | {n} | {g if g is not None else '—'} |")

    w(f"\n## 1. Suspected duplicate sites ({len(dupes)} "
      f"{'pair/group' if len(dupes) == 1 else 'pairs/groups'})\n")
    if dupes:
        w("Review these — they may be the same physical site under different names, "
          "or legitimately distinct sites of the same operator.\n")
        w("| signal | plants | ids |")
        w("|---|---|---|")
        for sig, names, ids in dupes:
            w(f"| {sig} | {' ⟷ '.join(names)} | {', '.join(ids)} |")
    else:
        w("None detected.\n")

    w(f"\n## 2. Capacity double-count / consistency flags ({len(cap_flags)} rows)\n")
    if cap_flags:
        w("| plant | operator | region | nameplate GWh | flag |")
        w("|---|---|---|---:|---|")
        for r, msg in cap_flags:
            w(f"| {r['plant_name']} | {r['operator']} | {r['region']} | "
              f"{r['nameplate_capacity_gwh']} | {msg} |")
    else:
        w("None detected.\n")
    w(f"\n### Live cell sites missing a nameplate figure ({len(missing_cap)})\n")
    w("Genuine cell plants (operational/under-construction) with no sourced capacity — "
      "capacity left null per the no-guessing rule.\n")
    if missing_cap:
        w("| plant | operator | region | status |")
        w("|---|---|---|---|")
        for r in missing_cap:
            w(f"| {r['plant_name']} | {r['operator']} | {r['region']} | {r['status']} |")

    w(f"\n## 3. Rows with confidence < 0.5 ({len(lowconf)})\n")
    if lowconf:
        w("| plant | operator | country | conf | is_cell | note |")
        w("|---|---|---|---:|:---:|---|")
        for r in lowconf:
            note = (r["research_notes"] or "").replace("\n", " ")
            note = (note[:90] + "…") if len(note) > 90 else note
            w(f"| {r['plant_name']} | {r['operator']} | {r['country']} | "
              f"{r['confidence']} | {'Y' if r['is_cell_manufacturer'] else 'N'} | {note} |")

    w(f"\n## Appendix — non-cell sites flagged by researchers ({len(noncell)})\n")
    w("Kept in the DB and tagged `is_cell_manufacturer = false`. Filter these out for "
      "a pure cell-manufacturing view; they are pack-assembly, material or "
      "corporate-HQ entries surfaced by the wide-net seed list.\n")
    if noncell:
        w("| plant | operator | country | why flagged (note excerpt) |")
        w("|---|---|---|---|")
        for r in noncell:
            note = (r["research_notes"] or "").replace("\n", " ")
            note = (note[:110] + "…") if len(note) > 110 else note
            w(f"| {r['plant_name']} | {r['operator']} | {r['country']} | {note} |")

    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"Wrote {OUT}")
    print(f"  duplicates: {len(dupes)}  capacity flags: {len(cap_flags)}  "
          f"missing-cap: {len(missing_cap)}  low-conf: {len(lowconf)}  non-cell: {len(noncell)}")
    con.close()


if __name__ == "__main__":
    main()
