#!/usr/bin/env python3
"""Capacity by year per supply-chain step (normalised units), the supply-chain analogue of cell Series D (built nameplate)
and pipeline. Rules (same spirit as series_core v4): only sourced, dated information; never sum across statuses.

Per active asset with capacity_norm (or installed_norm):
- built[y]: dated steps (capacity_by_year_json, scaled by capacity_norm/capacity) where present; else installed_norm from
  installed_as_of; else for operational rows the full capacity from capacity_ref_year when that year has passed, and
  from start_year only if the plan has no later reference year (otherwise the undated part is pipeline);
- under_construction[y] / announced[y]: capacity_norm from capacity_ref_year (by status) — pipeline, kept separate.
Output: sc_capacity_by_year.csv (step, commodity, norm_unit, year, built, under_construction, announced, n_assets)."""
import json, os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Y0, Y1 = 2015, 2030


def steps(js):
    try:
        return {int(k): float(v) for k, v in json.loads(js).items() if v is not None}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def main():
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    a = a[(a.project_state.fillna("active") == "active") & a.norm_unit.notna()]
    rows = []
    for r in a.itertuples():
        cap = r.capacity_norm if pd.notna(r.capacity_norm) else r.installed_norm
        if pd.isna(cap):
            continue
        ry = int(r.capacity_ref_year) if pd.notna(r.capacity_ref_year) else None
        series = {}
        if r.status == "operational":
            st = steps(r.capacity_by_year_json)
            scale = (r.capacity_norm / r.capacity) if pd.notna(r.capacity_norm) and pd.notna(r.capacity) and r.capacity else 1.0
            ia = int(str(r.installed_as_of)[:4]) if pd.notna(r.installed_as_of) else None
            sy = int(r.start_year) if pd.notna(r.start_year) else None
            for y in range(Y0, Y1 + 1):
                v = 0.0
                if st:
                    ks = [k for k in st if k <= y]
                    v = st[max(ks)] * scale if ks else 0.0
                if pd.notna(r.installed_norm) and ia and y >= ia:
                    v = max(v, r.installed_norm)
                if ry and y >= ry and not (pd.notna(r.installed_norm) and ia and ia >= y and r.installed_norm < cap):
                    v = max(v, cap)
                if not st and pd.isna(r.installed_norm) and sy and y >= sy and (ry is None or ry <= sy):
                    v = max(v, cap)
                series[y] = ("built", v, max(0.0, (cap - v)) if (ry and y >= ry) else 0.0)
        else:
            oy = ry or (int(r.start_year) if pd.notna(r.start_year) else None)
            for y in range(Y0, Y1 + 1):
                series[y] = (r.status, cap if (oy and y >= oy) else 0.0, 0.0)
        for y, (kind, v, _) in series.items():
            if v:
                rows.append(dict(step=r.step, commodity=r.commodity, norm_unit=r.norm_unit, year=y, kind=kind, value=v, id=r.id))
    d = pd.DataFrame(rows)
    out = d.pivot_table(index=["step", "commodity", "norm_unit", "year"], columns="kind", values="value", aggfunc="sum", fill_value=0)
    out["n_assets"] = d.groupby(["step", "commodity", "norm_unit", "year"]).id.nunique()
    out = out.reset_index()
    for c in ("built", "under_construction", "announced"):
        if c not in out:
            out[c] = 0.0
    out[["step", "commodity", "norm_unit", "year", "built", "under_construction", "announced", "n_assets"]].round(0).to_csv(
        os.path.join(ROOT, "sc_capacity_by_year.csv"), index=False)
    show = out[out.year.isin([2020, 2023, 2025, 2028, 2030])]
    print(show.pivot_table(index=["step", "commodity", "norm_unit"], columns="year", values="built", aggfunc="sum").round(-3).to_string())


if __name__ == "__main__":
    main()
