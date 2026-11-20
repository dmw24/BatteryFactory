#!/usr/bin/env python3
"""Per-operator reconciliation: company-disclosed capacity (data/reference/operator_totals.csv)
vs the sum of that operator's site-level capacity in our series (A confirmed, C best estimate).
Writes data/reference/operator_gap.csv and prints the table. Gap = disclosed − C (positive = capacity
the company reports that we have not yet located at a site)."""
import duckdb, pandas as pd
KEYS = {"CATL": ["catl", "contemporary amperex", "times "], "REPT Battero": ["rept", "lanjun"],
        "Great Power": ["great power", "鹏辉"], "Zenergy": ["zenergy"], "Narada": ["narada", "nandu"],
        "Hithium": ["hithium"], "Chuneng": ["chuneng", "cornex"], "Ganfeng LiEnergy": ["ganfeng"],
        "Panasonic Energy": ["panasonic"], "Tesla": ["tesla"], "Verkor": ["verkor"], "Lyten (Northvolt Sweden)": ["lyten"]}
tot = pd.read_csv("data/reference/operator_totals.csv")
con = duckdb.connect("factories.db", read_only=True)
f = con.execute("""select f.id, lower(coalesce(f.operator,'')||' '||coalesce(f.parent_company,'')) o,
                          c.year, c.gwh_firm a, c.gwh_best cbest
                   from capacity_by_year c join factories f using(id)""").df()
rows = []
for op, keys in KEYS.items():
    t = tot[(tot.operator == op) & tot.built_gwh.notna()].sort_values("year")
    if t.empty:
        continue
    r = t.iloc[-1] if op != "Great Power" else t[t.year == 2025].iloc[0]
    yr = int(r.year)
    m = f[f.o.apply(lambda s: any(k in s for k in keys)) & (f.year == min(yr, 2026))]
    if op == "Panasonic Energy":
        m = m[m.id.str.contains("nevada")]
    rows.append(dict(operator=op, year=yr, disclosed=r.built_gwh, sites=m.id.nunique(),
                     A=round(m.a.sum(), 1), C=round(m.cbest.sum(), 1), gap_vs_C=round(r.built_gwh - m.cbest.sum(), 1),
                     basis=str(r.basis)[:60]))
g = pd.DataFrame(rows).sort_values("gap_vs_C", ascending=False)
g.to_csv("data/reference/operator_gap.csv", index=False)
print(g.to_string(index=False))
print("sum of positive gaps:", round(g.gap_vs_C.clip(lower=0).sum()), "GWh; sum of negative (site total > disclosed):", round(g.gap_vs_C.clip(upper=0).sum()))
