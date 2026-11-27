#!/usr/bin/env python3
"""Compare supply-chain asset totals with open benchmarks (data/supply_chain/benchmarks/aggregates.csv).

For each benchmark row: ours_production = operational assets' production_norm (production_year in [year-1, year],
same unit); ours_capacity = operational assets' installed_norm, else capacity_norm (same unit). Mining coverage =
ours_production / benchmark. Processing: capacity_ratio = ours_capacity / benchmark (≥1 expected against output;
≈1 against capacity). commodity "cathode (LFP)" filters product by the bracketed text. Writes sc_benchmark.csv.
"""
import os
import re

import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    b = pd.read_csv(os.path.join(ROOT, "data/supply_chain/benchmarks/aggregates.csv"))
    from sc_build import COUNTRY_ALIASES
    b["country"] = b["country"].map(lambda c: COUNTRY_ALIASES.get(c, c))
    a = a[(a.status == "operational") & (a.project_state.fillna("active") != "cancelled")]
    cc_path = os.path.join(ROOT, "sc_company_coverage.csv")
    cc = pd.read_csv(cc_path) if os.path.exists(cc_path) else pd.DataFrame(
        columns=["step", "metric", "unit", "unallocated", "disclosed", "year"])
    rows = []
    for r in b.itertuples():
        if r.country == "Other countries":
            continue
        m = re.match(r"([^(]+?)\s*(?:\((.+)\))?$", str(r.commodity))
        com, sub = m.group(1).strip(), m.group(2)
        s = a[(a.step == r.step) & (a.commodity == com)]
        if sub and com != "nickel":
            key = sub.split("/")[0]
            s = s[s["product"].fillna("").str.contains(key, case=False)]
        if r.country != "World":
            s = s[s.country == r.country]
        p = s[s.production_year.between(r.year - 1, r.year + 1) & (s.production_norm_unit == r.norm_unit)]
        c = s[s.norm_unit == r.norm_unit]
        cap = c.installed_norm.fillna(c.capacity_norm).sum()
        rows.append(dict(step=r.step, commodity=r.commodity, metric=r.metric, year=r.year, country=r.country,
                         benchmark=r.value, unit=r.norm_unit, ours_production=round(p.production_norm.sum()),
                         n_prod=len(p), ours_capacity=round(cap), n_cap=int(c.installed_norm.fillna(c.capacity_norm).notna().sum()),
                         production_coverage=round(p.production_norm.sum() / r.value, 2),
                         capacity_ratio=round(cap / r.value, 2),
                         unallocated_capacity=round(cc[(cc.step == r.step) & (cc.metric == "capacity") & (cc.unit == r.norm_unit) & (cc.year == r.year)].unallocated.sum()) if (r.step != "mining" and r.country in ("China", "World") and not sub) else 0,
                         company_disclosed_output=round(cc[(cc.step == r.step) & (cc.metric == "production") & (cc.unit == r.norm_unit) & (cc.year == r.year)].disclosed.sum()) if (r.step != "mining" and r.country in ("China", "World") and not sub) else 0,
                         unallocated_production=round(cc[(cc.step == r.step) & (cc.metric == "production") & (cc.unit == r.norm_unit) & (cc.year == r.year)].unallocated.sum()) if (r.country == "World" and not sub) else 0,
                         source=r.source))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(ROOT, "sc_benchmark.csv"), index=False)
    latest = out.sort_values("year").groupby(["step", "commodity", "metric", "country"]).tail(1)
    show = latest[latest.country.isin(["World", "China"]) | (latest.step == "mining")]
    print(show.drop(columns="source").to_string(index=False))


if __name__ == "__main__":
    main()
