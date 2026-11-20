#!/usr/bin/env python3
"""Integrity checks for the factories dataset. Must pass after every merged task.

    python3 checks/run_all.py          # rebuild from baseline + patches, then check
    python3 checks/run_all.py --no-rebuild

Hard rules apply to rows re-verified by the team (last_verified set). v1 rows that
break them are counted as WARN (legacy debt) – they are fixed by re-verification,
which is what checks/done_gates.py measures.

Output: one line per check, `PASS`/`FAIL`/`WARN` + reason; detail in logs/checks_detail.log.
"""
import json
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

REGIONS = {"China", "USA", "Europe", "South Korea", "Japan", "India", "Southeast Asia", "Rest of World"}
STATUS = {"announced", "under_construction", "operational"}
STATE = {"active", "paused", "cancelled"}
SITE_TYPE = {"single_site", "hub"}
FORMATS = {"prismatic", "cylindrical", "pouch", "mixed"}
MARKETS = {"EV", "ESS", "consumer", "mixed"}
CHEMS = {"LFP", "LMFP", "NMC", "NCA", "LCO", "LMO", "LTO", "sodium-ion", "solid-state",
         "semi-solid-state", "lithium-metal", "zinc", "other", "mixed"}
# Hard-paywall / subscription data vendors. Open-data rule: a row may not rest on these.
PAYWALL = re.compile(r"(^|\.)(bloomberg\.com|bnef\.com|ft\.com|wsj\.com|benchmarkminerals\.com|"
                     r"sneresearch\.com|nikkei\.com|asia\.nikkei\.com|theinformation\.com|spglobal\.com|"
                     r"woodmac\.com|fastmarkets\.com|argusmedia\.com|economist\.com|rhomotion\.com)$")
# Fields that, when non-null on a verified row, must carry evidence in data/field_evidence.csv.
KEY_FIELDS = ["status", "nameplate_capacity_gwh", "installed_capacity_gwh", "start_year"]
CURRENT_YEAR = 2026

results, detail = [], []


def report(cid, ok, msg, rows=(), warn=False):
    tag = "PASS" if ok else ("WARN" if warn else "FAIL")
    results.append((cid, tag))
    print(f"{tag} {cid} {msg}")
    for r in list(rows)[:200]:
        detail.append(f"{cid} {r}")


def domain(u):
    try:
        return urlparse(str(u)).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def main():
    if "--no-rebuild" not in sys.argv:
        r = subprocess.run([sys.executable, "scripts/rebuild.py"], capture_output=True, text=True)
        if r.returncode:
            print(f"FAIL C0 rebuild failed: {(r.stdout + r.stderr).strip().splitlines()[-1]}")
            sys.exit(1)
        print(f"PASS C0 {r.stdout.strip()}")
    d = pd.read_csv("factories_export.csv")
    ev = pd.read_csv("data/field_evidence.csv")
    ver = d["last_verified"].notna()

    # C1 schema and allowed values (all rows)
    bad = []
    if d.id.duplicated().any():
        bad += [f"duplicate id {i}" for i in d.id[d.id.duplicated()]]
    for c in ["plant_name", "operator", "country", "region", "source_url", "source_date", "confidence"]:
        bad += [f"{i}: {c} is null" for i in d.id[d[c].isna()]]
    for c, allowed in [("region", REGIONS), ("status", STATUS), ("project_state", STATE), ("site_type", SITE_TYPE)]:
        m = d[c].notna() & ~d[c].isin(allowed)
        bad += [f"{i}: {c}={v!r} not in {sorted(allowed)}" for i, v in zip(d.id[m], d[c][m])]
    m = d.latitude.notna() & ~d.latitude.between(-90, 90) | d.longitude.notna() & ~d.longitude.between(-180, 180)
    bad += [f"{i}: lat/lon out of range" for i in d.id[m]]
    m = ~d.confidence.between(0, 1)
    bad += [f"{i}: confidence out of [0,1]" for i in d.id[m]]
    report("C1", not bad, f"schema/allowed values: {len(bad)} problems" + (" – fix the patch values" if bad else ""), bad)

    # C2 controlled vocabulary on verified rows (v1 free text is legacy)
    bad = []
    for c, allowed in [("cell_format", FORMATS), ("end_market", MARKETS), ("chemistry", CHEMS)]:
        m = ver & d[c].notna() & ~d[c].isin(allowed)
        bad += [f"{i}: {c}={v!r} not in vocab" for i, v in zip(d.id[m], d[c][m])]
    m = ver & d.status.isna() & (d.is_cell_manufacturer != False)
    bad += [f"{i}: verified cell plant with null status" for i in d.id[m]]
    m = ver & d.site_type.isna()
    bad += [f"{i}: verified row needs site_type single_site|hub" for i in d.id[m]]
    report("C2", not bad, f"vocabulary on verified rows: {len(bad)} problems (see team/CONVENTIONS.md vocab)", bad)

    # C3 invariants. Hard on verified rows, WARN on v1 rows.
    def invariants(rows):
        out = []
        for _, r in rows.iterrows():
            n, inst = r.nameplate_capacity_gwh, r.installed_capacity_gwh
            if pd.notna(n) and n < 0 or pd.notna(inst) and inst < 0:
                out.append(f"{r.id}: negative capacity")
            if pd.notna(n) and n > 1000:
                out.append(f"{r.id}: nameplate {n} > 1000 GWh/yr for one site – hub/company total?")
            if pd.notna(n) and pd.notna(inst) and inst > n * 1.001:
                out.append(f"{r.id}: installed {inst} > nameplate {n}")
            if r.status == "announced" and pd.notna(inst) and inst > 0:
                out.append(f"{r.id}: announced plant with installed capacity {inst}")
            if r.status == "operational" and pd.notna(r.start_year) and r.start_year > CURRENT_YEAR:
                out.append(f"{r.id}: operational but start_year {r.start_year} is in the future")
            if pd.notna(r.announced_year) and pd.notna(r.start_year) and r.announced_year > r.start_year:
                out.append(f"{r.id}: announced_year {r.announced_year} after start_year {r.start_year}")
            if pd.notna(n) and pd.isna(r.capacity_ref_year):
                out.append(f"{r.id}: nameplate without capacity_ref_year")
            if pd.notna(r.capacity_by_year_json):
                try:
                    cy = json.loads(r.capacity_by_year_json)
                    if pd.notna(n) and any(float(v) > n * 1.05 for v in cy.values() if v is not None):
                        out.append(f"{r.id}: capacity_by_year_json exceeds nameplate")
                except Exception:
                    out.append(f"{r.id}: capacity_by_year_json not valid JSON")
        return out
    hard, legacy = invariants(d[ver]), invariants(d[~ver])
    report("C3", not hard, f"invariants on verified rows: {len(hard)} violations", hard)
    report("C3v1", not legacy, f"invariants on unverified v1 rows: {len(legacy)} (legacy debt, fixed by re-verification)",
           legacy, warn=True)

    # C4 provenance on verified rows: every non-null key field has evidence with url+quote+accessed
    bad = []
    evk = ev.assign(ok=ev.url.notna() & ev.quote.fillna("").str.strip().ne("") & ev.accessed.notna())
    good = set(zip(evk.id[evk.ok], evk.field[evk.ok]))
    for _, r in d[ver].iterrows():
        for f in KEY_FIELDS + (["project_state"] if r.project_state != "active" else []):
            if pd.notna(r[f]) and (r.id, f) not in good:
                bad.append(f"{r.id}: {f}={r[f]} has no evidence (url+verbatim quote+accessed)")
        if r.confidence >= 0.9:
            doms = {domain(u) for u in ev.url[(ev.id == r.id) & ev.field.isin(["status", "nameplate_capacity_gwh"])]}
            if len(doms) < 2:
                bad.append(f"{r.id}: confidence {r.confidence} needs >=2 independent domains for status/capacity")
    bad += [f"evidence row with empty quote: {i}/{f}" for i, f in zip(evk.id[~evk.ok], evk.field[~evk.ok])]
    report("C4", not bad, f"field provenance on {ver.sum()} verified rows: {len(bad)} gaps", bad)

    # C5 open-data rule: no subscription-only source anywhere
    bad = [f"{i}: source_url {u}" for i, u in zip(d.id, d.source_url) if PAYWALL.search(domain(u))]
    bad += [f"{i}/{f}: evidence {u}" for i, f, u in zip(ev.id, ev.field, ev.url) if PAYWALL.search(domain(u))]
    hard = [b for b in bad if b.split(":")[0].split("/")[0] in set(d.id[ver]) or "evidence" in b]
    report("C5", not hard, f"open-data sources: {len(bad)} paywalled ({len(hard)} on verified rows)", bad)

    # C6 duplicates: exact name dupes, or same operator + same rounded site coordinates
    bad = []
    nm = d.plant_name.str.lower().str.strip()
    bad += [f"duplicate plant_name {n}" for n in nm[nm.duplicated()]]
    precise = d[d.geo_precision.isin(["site", "town", "site_unflagged"])].copy()
    precise["k"] = precise.operator.str.lower().str[:12] + precise.latitude.round(2).astype(str) + precise.longitude.round(2).astype(str)
    dup = precise[precise.k.duplicated(keep=False)]
    bad += [f"same operator+site coords: {', '.join(g.id)}" for _, g in dup.groupby("k")]
    report("C6", not bad, f"duplicate sites: {len(bad)} suspected (merge with action=remove reason=duplicate_of:<id>)",
           bad, warn=True)

    # C7 reference CSVs parse and have the contract columns
    import glob
    bad = []
    need = {"operator_sites": ["operator", "site_name", "matched_id", "excluded_reason"],
            "candidates": ["plant_name", "operator", "country", "source_url"]}
    for kind, cols in need.items():
        for f in sorted(glob.glob(f"data/reference/{kind}/*.csv")):
            try:
                t = pd.read_csv(f)
                miss = [c for c in cols if c not in t.columns]
                if miss:
                    bad.append(f"{f}: missing columns {miss}")
            except Exception as e:  # noqa: BLE001
                bad.append(f"{f}: does not parse ({str(e)[:80]}) – quote fields containing commas")
    report("C7", not bad, f"reference CSVs: {len(bad)} problems", bad)

    os.makedirs("logs", exist_ok=True)
    open("logs/checks_detail.log", "w").write("\n".join(detail) + "\n")
    fails = [c for c, t in results if t == "FAIL"]
    print(f"{'FAIL' if fails else 'PASS'} summary: {len(results)} checks, {len(fails)} failed {fails or ''}"
          f" – detail in logs/checks_detail.log")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
