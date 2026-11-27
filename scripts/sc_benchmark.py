#!/usr/bin/env python3
"""Compare supply-chain asset totals with open benchmarks (data/supply_chain/benchmarks/aggregates.csv).

Mining: sum of operational assets' latest production_norm (production_year within 1 year of the benchmark year).
Processing: sum of operational assets' installed_norm (else capacity_norm) vs benchmark capacity or production.
Writes sc_benchmark.csv and prints a table. Never sums across statuses.
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    b = pd.read_csv(os.path.join(ROOT, "data/supply_chain/benchmarks/aggregates.csv"))
    a = a[(a.status == "operational")]
    rows = []
    for (step, com, metric, yr), g in b.groupby(["step", "commodity", "metric", "year"]):
        s = a[(a.step == step) & (a.commodity == com)]
        if metric == "production":
            s = s[s.production_year.between(yr - 1, yr) & s.production_norm.notna()]
            val = lambda d: d.production_norm.sum()
        else:
            s = s.assign(v=s.installed_norm.fillna(s.capacity_norm))
            val = lambda d: d.v.sum()
        for r in g.itertuples():
            sub = s if r.country == "World" else s[s.country == r.country]
            if r.country == "Other countries":
                continue
            ours = val(sub)
            rows.append(dict(step=step, commodity=com, metric=metric, year=yr, country=r.country, ours=round(ours),
                             n_assets=len(sub), benchmark=r.value, unit=r.norm_unit,
                             coverage=round(ours / r.value, 2) if r.value else None, source=r.source))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(ROOT, "sc_benchmark.csv"), index=False)
    if len(out):
        print(out[out.year == out.year.max()].to_string(index=False))


if __name__ == "__main__":
    main()
