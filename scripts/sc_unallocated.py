#!/usr/bin/env python3
"""Company-disclosed totals vs the sum of that company's sites (supply-chain analogue of cell Series E, D-028).

data/supply_chain/company_totals.csv (verbatim-sourced company totals from filings, `asset_match` = regex on asset id)
-> sc_company_coverage.csv: company, step, metric, disclosed, sites_sum, n_sites, unallocated (floored at 0).
Unallocated capacity has no location; it is reported next to site totals, never mixed into asset rows.
"""
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    a = a[(a.status == "operational") & (a.project_state.fillna("active") == "active")]
    t = pd.read_csv(os.path.join(ROOT, "data/supply_chain/company_totals.csv"))
    out = []
    for r in t.itertuples():
        if not isinstance(r.asset_match, str) or not r.asset_match:
            continue
        s = a[(a.step == r.step) & a.id.str.contains(r.asset_match.replace("(", "(?:"), flags=re.I, regex=True)]
        if r.metric == "capacity":
            s = s[s.norm_unit == r.unit]
            v = s.installed_norm.fillna(s.capacity_norm)
        else:
            s = s[s.production_norm_unit == r.unit]
            v = s.production_norm
        sites = float(v.fillna(0).sum())
        out.append(dict(company=r.company, step=r.step, year=r.year, metric=r.metric, product=r.product,
                        disclosed=r.value, unit=r.unit, sites_sum=round(sites), n_sites=int(v.notna().sum()),
                        n_site_rows=len(s), unallocated=round(max(0.0, r.value - sites)),
                        source=f"{r.source_file} l.{r.line_ref}"))
    o = pd.DataFrame(out)
    o.to_csv(os.path.join(ROOT, "sc_company_coverage.csv"), index=False)
    print(o.groupby(["step", "metric", "unit"])[["disclosed", "sites_sum", "unallocated"]].sum().to_string())


if __name__ == "__main__":
    main()
