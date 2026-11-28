#!/usr/bin/env python3
"""Audit 6 guard: built capacity for years <= 2025 must not fall versus the accepted baseline unless the lead accepts it
(SC_ACCEPT_BUILT=1 rewrites data/supply_chain/built_baseline.csv). Drops > 1% per step/commodity/unit fail the build."""
import os, sys
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cur = pd.read_csv(os.path.join(ROOT, "sc_capacity_by_year.csv"))
cur = cur[cur.year <= 2025][["step", "commodity", "norm_unit", "year", "built"]]
bp = os.path.join(ROOT, "data/supply_chain/built_baseline.csv")
if os.environ.get("SC_ACCEPT_BUILT") or not os.path.exists(bp):
    cur.to_csv(bp, index=False); print("built baseline written"); sys.exit(0)
base = pd.read_csv(bp)
m = base.merge(cur, on=["step", "commodity", "norm_unit", "year"], how="left", suffixes=("_base", "_cur")).fillna({"built_cur": 0})
drop = m[m.built_cur < m.built_base * 0.99]
if len(drop):
    print("FAIL built capacity fell vs baseline (set SC_ACCEPT_BUILT=1 only if a patch deliberately rejects earlier values):")
    print(drop.to_string(index=False)); sys.exit(1)
print("built guard OK")
