#!/usr/bin/env python3
"""Compare supply-chain asset totals with open benchmarks (data/supply_chain/benchmarks/aggregates.csv). v2 after SC audit 1.

Active assets only (project_state active), operational status. Per benchmark row:
- ours_production: production_norm with production_year in [year-1, year+1] (D-104), same unit;
- ours_capacity (built): installed_norm, else capacity_norm when capacity_ref_year <= benchmark year (dated/built);
- plan_only_capacity: capacity_norm of operational rows whose ref year is later (unbuilt phases) — reported separately;
- lithium refining also counts on-site brine chemical plants (mining rows whose product is a lithium chemical, D-103);
- nickel vs INSG primary nickel: intermediates (t Ni in MHP / matte) are excluded and shown separately (one stage per chain);
- company-level figures (sc_company_coverage.csv): for a China benchmark only companies whose totals are China-only
  (geo_scope = china) count in *_china columns; *_incl_overseas columns are upper bounds.
"""
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc_build import COUNTRY_ALIASES  # noqa: E402
from sc_core import built_upper  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERMEDIATE = {"t Ni in MHP", "t Ni in matte"}
LI_CHEM = re.compile(r"carbonate|chloride|hydroxide|Li2CO3|LiOH|LiCl|lithium salt", re.I)
BRINE = re.compile(r"brine|salar|salt.?lake|盐湖", re.I)


def main():
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv"))
    b = pd.read_csv(os.path.join(ROOT, "data/supply_chain/benchmarks/aggregates.csv"))
    b["country"] = b["country"].map(lambda c: COUNTRY_ALIASES.get(c, c))
    a = a[(a.status == "operational") & (a.project_state.fillna("active") == "active")]
    cc_path = os.path.join(ROOT, "sc_company_coverage.csv")
    cc = pd.read_csv(cc_path) if os.path.exists(cc_path) else pd.DataFrame(
        columns=["step", "metric", "unit", "unallocated", "disclosed", "year", "geo_scope"])
    rows = []
    for r in b.itertuples():
        if r.country == "Other countries" or not str(r.year).isdigit():
            continue
        yr = int(r.year)
        m = re.match(r"([^(]+?)\s*(?:\((.+)\))?$", str(r.commodity))
        com, sub = m.group(1).strip(), m.group(2)
        s = a[(a.step == r.step) & (a.commodity == com)]
        if r.step == "refining" and com == "lithium":
            onsite = a[(a.step == "mining") & (a.commodity == "lithium") & a["product"].fillna("").str.contains(LI_CHEM)
                       & ~a["product"].fillna("").str.contains("brine|concentrate", case=False)
                       & (a.feedstock.fillna("") + " " + a.asset_type.fillna("") + " " + a.asset_name.fillna("")).str.contains(BRINE)]
            s = pd.concat([s, onsite])   # D-103: on-site brine chemical plants only (audit 2 D8)
        if sub and com != "nickel":
            s = s[s["product"].fillna("").str.contains(sub.split("/")[0], case=False)]
        if r.country != "World":
            s = s[s.country == r.country]
        inter = 0.0
        if com == "nickel" and r.step == "refining":
            im = s.capacity_unit.isin(INTERMEDIATE)
            si = s[im]
            inter = sum(built_upper(x, yr)[0] for x in si.itertuples())
            s = s.assign(norm_unit=s.norm_unit.where(~im, "t Ni (intermediate)"))
        p = s[s.production_year.between(yr - 1, yr + 1) & (s.production_norm_unit == r.norm_unit)]
        c = s[s.norm_unit == r.norm_unit]
        bu = [built_upper(x, yr) for x in c.itertuples()]
        built = pd.Series([v[0] for v in bu], index=c.index, dtype=float)
        plan = pd.Series([v[1] - v[0] for v in bu], index=c.index, dtype=float)
        built_rep = built[c.evidence_tier == "reported"].sum()
        cco = cc[(cc.step == r.step) & (cc.unit == r.norm_unit) & (cc.year == yr)] if (r.country in ("China", "World") and not sub) else cc.iloc[0:0]
        china = cco[cco.geo_scope == "china"] if r.country == "China" else cco
        rows.append(dict(step=r.step, commodity=r.commodity, metric=r.metric, year=yr, country=r.country,
                         benchmark=r.value, unit=r.norm_unit,
                         ours_production=round(p.production_norm.sum()), n_prod=len(p),
                         ours_capacity=round(built.sum()), plan_only_capacity=round(plan.sum()),
                         built_reported_tier=round(built_rep),
                         intermediate_capacity=round(inter),
                         production_coverage=round(p.production_norm.sum() / r.value, 2),
                         capacity_ratio=round(built.sum() / r.value, 2),
                         unallocated_capacity=round(china[china.metric == "capacity"].unallocated.sum()),
                         unallocated_production=round(china[china.metric == "production"].unallocated.sum()) if r.country == "World" or r.step != "mining" else 0,
                         company_disclosed_output=round(china[china.metric == "production"].disclosed.sum()),
                         company_disclosed_output_incl_overseas=round(cco[cco.metric == "production"].disclosed.sum()),
                         source=r.source))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(ROOT, "sc_benchmark.csv"), index=False)
    print(f"sc_benchmark: {len(out)} comparisons")


if __name__ == "__main__":
    main()
