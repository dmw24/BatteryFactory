#!/usr/bin/env python3
"""Confirmed vs reported (owner decision 2026-11-20, D-024).

v2 re-verification set v1 values to null when they could not be re-confirmed. This script restores
such values as REPORTED (flagged in `reported_fields`, evidence tier 'reported' = the v1 source_url,
no re-confirmed quote) unless the v2 research contradicted or superseded them.

  python3 scripts/restore_reported.py      # writes data/patches/T031_reported.json

Capacity-relevant fields (status, nameplate_capacity_gwh + capacity_ref_year, capacity_by_year_json) are
restored only where data/reference/reported/capacity_decisions.csv says RESTORE (Opus review of each row's
notes). Descriptive fields (chemistry, cell_format, end_market, start_year, announced_year, jv_partners)
are restored by rule: value mapped to the controlled vocabulary, and not restored when the v2 notes flag
that field as wrong or the ownership/timing changed.
Confidence is capped at 0.5 when status or capacity becomes reported.
"""
import json
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
import subprocess, sys
# compute against a build WITHOUT this patch, so re-running is idempotent
subprocess.run([sys.executable, "scripts/rebuild.py"], check=True, capture_output=True,
               env={**os.environ, "REBUILD_EXCLUDE": "T031_reported.json"})
v1 = pd.read_csv("data/baseline/factories_v1.csv").set_index("id")
d = pd.read_csv("factories_export.csv").set_index("id")
PAYWALL = re.compile(r"bloomberg\.com|bnef\.com|ft\.com|wsj\.com|benchmarkminerals|sneresearch|nikkei\.com|spglobal|woodmac|fastmarkets|argusmedia|economist\.com|rhomotion")
dec_path = "data/reference/reported/capacity_decisions.csv"
dec = pd.read_csv(dec_path) if os.path.exists(dec_path) else pd.DataFrame(columns=["id", "field", "decision", "reason"])
restore_cap = {(r.id, r.field) for r in dec.itertuples() if str(r.decision).strip().upper() == "RESTORE"}


def norm_chem(v):
    t = str(v).lower()
    special = set()
    if "sodium" in t or "na-ion" in t:
        special.add("sodium-ion")
    if "semi-solid" in t or "semi solid" in t:
        special.add("semi-solid-state")
    elif "solid" in t:
        special.add("solid-state")
    has = {k for k, pat in {"LFP": r"\blfp\b|lifepo|iron phosphate|blade", "NMC": r"\bnmc\b|\bncm\b|ternary",
                            "NCA": r"\bnca\b", "LMFP": r"lmfp", "LTO": r"\blto\b|titanate", "LCO": r"\blco\b|cobalt oxide",
                            "LMO": r"\blmo\b|manganese oxide"}.items() if re.search(pat, t)}
    if "LMFP" in has:
        has.discard("LFP")
    has |= special          # fixed 2026-11-24: "LFP and sodium-ion" is mixed, not sodium-ion
    if len(has) == 1:
        return has.pop()
    if len(has) > 1 or "mixed" in t:
        return "mixed"
    return None


def norm_fmt(v):
    t = str(v).lower()
    k = {f for f in ("prismatic", "cylindrical", "pouch") if f in t or (f == "prismatic" and "blade" in t)}
    if len(k) == 1:
        return k.pop()
    if len(k) > 1 or "mixed" in t:
        return "mixed"
    return None


def norm_mkt(v):
    t = str(v).lower()
    ev = bool(re.search(r"\bev\b|electric vehicle|power batter|automotive|passenger", t))
    ess = bool(re.search(r"\bess\b|storage|bess|grid", t))
    con = bool(re.search(r"consumer|3c|electronics|power tool|e-bike|two-wheeler|light", t))
    n = ev + ess + con
    if n > 1 or "mixed" in t:
        return "mixed"
    return "EV" if ev else "ESS" if ess else "consumer" if con else None


def flagged(notes, words):
    """notes say this field was wrong/changed"""
    t = str(notes).lower()
    return any(re.search(w, t) for w in words)


rows = []
stats = {}
for i in v1.index.intersection(d.index):
    r1, r2 = v1.loc[i], d.loc[i]
    notes = r2.research_notes
    fields, rep_ev, reported = {}, {}, []
    if not isinstance(r1.source_url, str) or PAYWALL.search(r1.source_url):
        continue  # open-data rule: a paywalled v1 source cannot back a reported value

    def put(f, val):
        fields[f] = val
        rep_ev[f] = r1.source_url
        reported.append(f)
        stats[f] = stats.get(f, 0) + 1

    # capacity-relevant, from the reviewed decisions
    for f in ("status", "nameplate_capacity_gwh", "capacity_by_year_json"):
        if pd.notna(r1[f]) and pd.isna(r2[f]) and (i, f) in restore_cap:
            val = r1[f] if f != "nameplate_capacity_gwh" else float(r1[f])
            put(f, val)
            if f == "nameplate_capacity_gwh" and pd.isna(r2.capacity_ref_year) and pd.notna(r1.capacity_ref_year):
                put("capacity_ref_year", int(r1.capacity_ref_year))
    # descriptive fields, by rule
    for f, normf, words in (("chemistry", norm_chem, [r"chemistry[^.]{0,60}(wrong|incorrect|not )"]),
                            ("cell_format", norm_fmt, [r"format[^.]{0,60}(wrong|incorrect|conflict)"]),
                            ("end_market", norm_mkt, [r"end.?market[^.]{0,60}(wrong|incorrect)"])):
        if pd.notna(r1[f]) and pd.isna(r2[f]) and not flagged(notes, words):
            val = normf(r1[f])
            if val:
                put(f, val)
    status_now = fields.get("status", r2.status)
    if pd.notna(r1.start_year) and pd.isna(r2.start_year) and status_now == "operational" and int(r1.start_year) <= 2026 \
            and not flagged(notes, [r"start.?year[^.]{0,60}(wrong|incorrect|conflict|not )"]):
        if pd.isna(r2.announced_year) or int(r2.announced_year) <= int(r1.start_year):
            put("start_year", int(r1.start_year))
    if pd.notna(r1.announced_year) and pd.isna(r2.announced_year):
        sy = fields.get("start_year", r2.start_year)
        if pd.isna(sy) or int(r1.announced_year) <= int(sy):
            put("announced_year", int(r1.announced_year))
    if pd.notna(r1.jv_partners) and pd.isna(r2.jv_partners) and not flagged(
            notes, [r"100\s?%", r"sold", r"dissolv", r"bought", r"exit", r"stake", r"wholly", r"jv_partners"]):
        put("jv_partners", r1.jv_partners)
    if not fields:
        continue
    prev = []
    if isinstance(r2.get("reported_fields"), str):
        prev = json.loads(r2.reported_fields)
    fields["reported_fields"] = json.dumps(sorted(set(prev + reported)))
    if set(reported) & {"status", "nameplate_capacity_gwh"} and r2.confidence > 0.5:
        fields["confidence"] = 0.5
    why = "; ".join(f"{f}: {dec[(dec.id == i) & (dec.field == f)].reason.iloc[0]}" for f in reported
                    if ((dec.id == i) & (dec.field == f)).any())
    rows.append({"id": i, "action": "fix", "fields": fields, "reported_evidence": rep_ev,
                 "notes": f"REPORTED (D-024): restored v1 value(s) for {', '.join(reported)} — v1 source not re-confirmed in v2"
                          + (f"; review: {why}" if why else "")})

json.dump({"task": "T031", "verified_on": "2026-11-20", "sources": {}, "rows": rows},
          open("data/patches/T031_reported.json", "w"), indent=1, ensure_ascii=False, default=str)
print(f"T031: {len(rows)} rows, restored per field: {stats}")
