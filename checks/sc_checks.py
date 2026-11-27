#!/usr/bin/env python3
"""Integrity checks for the supply-chain asset database (rebuilds first). Exit 1 on any FAIL.

    python3 checks/sc_checks.py
"""
import json
import os
import subprocess
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sc_build import REGIONS, STATES, STATUS, STEPS, units  # noqa: E402


def main():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts/sc_build.py")], capture_output=True, text=True)
    if r.returncode:
        print("FAIL S0 build:", r.stdout[-500:], r.stderr[-1500:])
        sys.exit(1)
    df = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    ev = pd.read_csv(os.path.join(ROOT, "data/supply_chain/field_evidence.csv"))
    u = units()
    res = []

    def check(code, name, bad):
        res.append((code, name, bad))

    check("S1", "required fields (asset_name, step, commodity, country, region, status, source_url, source_date)",
          [i for i, x in df.iterrows() if any(pd.isna(x[c]) for c in
           ["asset_name", "step", "commodity", "country", "region", "status", "source_url", "source_date"])])
    check("S2", "enums (step, status, project_state, region)",
          [x.id for _, x in df.iterrows() if x.step not in STEPS or x.status not in STATUS
           or x.project_state not in STATES or x.region not in REGIONS])
    check("S3", "units in data/supply_chain/units.csv",
          [x.id for _, x in df.iterrows() for c in ("capacity_unit", "production_unit")
           if isinstance(x[c], str) and x[c] not in u]
          + [x.id for _, x in df.iterrows() if (pd.notna(x.capacity) and not isinstance(x.capacity_unit, str))
             or (pd.notna(x.production) and not isinstance(x.production_unit, str))])
    have = set(zip(ev.id, ev.field))
    need = ["status", "capacity", "installed_capacity", "production", "capacity_by_year_json", "feeds"]
    check("S4", "every status/capacity/installed/production/steps value has evidence",
          [f"{x.id}:{f}" for _, x in df.iterrows() for f in need if pd.notna(x[f]) and (x.id, f) not in have])
    conf = ev[ev.tier == "confirmed"]
    check("S5", "confirmed evidence has a quote <=300 chars and a url",
          [f"{x.id}:{x.field}" for _, x in conf.iterrows()
           if not isinstance(x.quote, str) or not x.quote.strip() or len(x.quote) > 300 or not isinstance(x.url, str)])
    check("S6", "reported-tier rows capped at confidence 0.5",
          [x.id for _, x in df.iterrows() if x.evidence_tier == "reported" and (x.confidence or 0) > 0.5])
    check("S7", "coordinates in range and paired; precision given",
          [x.id for _, x in df.iterrows() if (pd.isna(x.latitude) != pd.isna(x.longitude))
           or (pd.notna(x.latitude) and (abs(x.latitude) > 90 or abs(x.longitude) > 180 or pd.isna(x.geo_precision)))])
    check("S8", "capacity has a ref year; installed has a date; production has a year",
          [x.id for _, x in df.iterrows() if (pd.notna(x.capacity) and pd.isna(x.capacity_ref_year))
           or (pd.notna(x.installed_capacity) and pd.isna(x.installed_as_of))
           or (pd.notna(x.production) and pd.isna(x.production_year))])

    def bad_json(s):
        if not isinstance(s, str):
            return False
        try:
            d = json.loads(s)
            return not isinstance(d, dict) or any(not k.isdigit() for k in d)
        except json.JSONDecodeError:
            return True
    check("S9", "capacity_by_year_json is a {year: value} map", [x.id for _, x in df.iterrows() if bad_json(x.capacity_by_year_json)])
    check("S10", "installed <= planned capacity (same unit); operational rows not without a start or capacity note",
          [x.id for _, x in df.iterrows() if pd.notna(x.installed_capacity) and pd.notna(x.capacity)
           and x.installed_capacity > x.capacity * 1.001])
    key = df.assign(k=df.asset_name.str.lower().str.replace(r"[^a-z0-9]", "", regex=True) + "|" + df.country + "|" + df.step + "|" + df["product"].fillna(""))
    check("S11", "no duplicate asset name+country+step+product", list(key[key.k.duplicated(keep=False)].id))
    check("S12", "confidence in [0,1]", [x.id for _, x in df.iterrows() if pd.isna(x.confidence) or not 0 <= x.confidence <= 1])
    ORE = {"t ore", "t spodumene concentrate", "t SC6", "t lepidolite concentrate", "t petalite concentrate", "t Mn ore"}
    check("S13", "normalised LCE/metal values plausible vs ore/concentrate tonnes (norm <= 20% of gross)",
          [f"{x.id}:{c}" for _, x in df.iterrows() for c, gu in (("production_norm", "production_unit"), ("capacity_norm", "capacity_unit"))
           if x[gu] in ORE and x["production_norm_unit" if c == "production_norm" else "norm_unit"] not in ORE and pd.notna(x[c]) and pd.notna(x[c.replace("_norm", "")]) and x[c] > 0.2 * x[c.replace("_norm", "")]])
    cells = set(pd.read_csv(os.path.join(ROOT, "factories_export.csv")).id) if os.path.exists(os.path.join(ROOT, "factories_export.csv")) else set()
    ids = set(df.id)
    check("S14", "feeds point to existing assets (or cell:<factories id>)",
          [f"{x.id}->{f}" for _, x in df.iterrows() if isinstance(x.feeds, str)
           for f in [t.strip() for t in x.feeds.split(",") if t.strip()]
           if not ((f.startswith("cell:") and f[5:] in cells) or f in ids)])
    fails = 0
    for code, name, bad in res:
        ok = not bad
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} {code} {name}: {len(bad)}" + ("" if ok else f"  e.g. {bad[:5]}"))
    print(f"{'PASS' if not fails else 'FAIL'} summary: {len(res)} checks, {fails} failed, {len(df)} assets")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
