#!/usr/bin/env python3
"""Capacity by year per supply-chain step (normalised units), v2 after SC audit 2 — rules in scripts/sc_core.py.

Columns: built (installed / sourced dated steps only), built_upper (built + rest of operational plans once their
reference year has passed — upper bound, not a completion), under_construction and announced (pipeline from reference
year). Nickel intermediates (MHP, matte) are a separate commodity label. Never sum across columns of different status.
Output: sc_capacity_by_year.csv."""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc_core import built_upper, commodity_label  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Y0, Y1 = 2015, 2030


def main():
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    a = a[(a.project_state.fillna("active") == "active") & a.norm_unit.notna()]
    rows = []
    for r in a.itertuples():
        lab = commodity_label(r)
        for y in range(Y0, Y1 + 1):
            if r.status == "operational":
                b, up = built_upper(r, y)
                if b or up:
                    rows.append(dict(step=r.step, commodity=lab, norm_unit=r.norm_unit, year=y, built=b, built_upper=up, id=r.id))
            elif getattr(r, "stale", False) is True or str(getattr(r, "stale", "")) == "True":
                continue   # D-114: stale pipeline rows (no progress evidence since 2024) are not in the pipeline columns
            else:
                cap = r.capacity_norm
                oy = int(r.capacity_ref_year) if pd.notna(r.capacity_ref_year) else None
                if pd.notna(cap) and oy and y >= oy:
                    rows.append(dict(step=r.step, commodity=lab, norm_unit=r.norm_unit, year=y, **{r.status: cap}, id=r.id))
    d = pd.DataFrame(rows).fillna(0)
    for c in ("built", "built_upper", "under_construction", "announced"):
        if c not in d:
            d[c] = 0.0
    g = d.groupby(["step", "commodity", "norm_unit", "year"])
    out = g[["built", "built_upper", "under_construction", "announced"]].sum()
    out["n_assets"] = g.id.nunique()
    out = out.reset_index().round(0)
    out.to_csv(os.path.join(ROOT, "sc_capacity_by_year.csv"), index=False)
    show = out[out.year.isin([2023, 2025, 2026])]
    print(show.pivot_table(index=["step", "commodity", "norm_unit"], columns="year", values=["built", "built_upper"], aggfunc="sum").round(-3).head(40).to_string())


if __name__ == "__main__":
    main()
