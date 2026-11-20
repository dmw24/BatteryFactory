#!/usr/bin/env python3
"""Definition-of-done gates (team/ACCEPTANCE.md G1–G5). Expected to FAIL until the end.

    python3 checks/done_gates.py      # reads factories_export.csv (run checks/run_all.py first)

Thresholds were fixed before any v2 results were seen (team/DECISIONS.md D-006).
"""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
d = pd.read_csv("factories_export.csv")
import os as _os
_nc = set(pd.read_csv("data/reference/non_comparable.csv").id) if _os.path.exists("data/reference/non_comparable.csv") else set()
act = d[(d.project_state == "active") & (d.is_cell_manufacturer != False) & ~d.id.isin(_nc)]
ver = act.last_verified.notna()
fails = []


def gate(gid, ok, msg):
    print(f"{'PASS' if ok else 'FAIL'} {gid} {msg}")
    if not ok:
        fails.append(gid)


# G1 verification coverage: every plant in the top 90% of nameplate, and >=90% of all active rows
cap = act.nameplate_capacity_gwh.fillna(0)
order = cap.sort_values(ascending=False)
top = order[order.cumsum() <= 0.9 * order.sum() + 1e-9].index.union(order.index[:1])
top_unver = act.loc[top][~ver.loc[top]]
gate("G1a", top_unver.empty, f"top-90%-capacity plants verified: {len(top) - len(top_unver)}/{len(top)}"
     + (f" – next: {', '.join(top_unver.sort_values('nameplate_capacity_gwh', ascending=False).id[:5])}" if len(top_unver) else ""))
gate("G1b", ver.mean() >= 0.9, f"active rows verified: {ver.sum()}/{len(act)} ({ver.mean():.0%}, need 90%)")

# G2 bottom-up installed capacity end-2025 vs IEA (>4 TWh nameplate, >80% China)
op = act[act.status == "operational"]
inst = op.installed_capacity_gwh
total = inst.sum()
china = inst[op.region == "China"].sum()
share = china / total if total else 0
gate("G2a", 3200 <= total <= 5000, f"operational installed capacity {total:,.0f} GWh/yr (band 3,200–5,000 vs IEA 2025 >4,000); "
     f"{inst.notna().sum()}/{len(op)} operational rows carry installed_capacity_gwh")
gate("G2b", 0.75 <= share <= 0.90, f"China share of installed {share:.0%} (band 75–90% vs IEA >80%)")

# G3 operator coverage: every publicly disclosed site of the reference operators is matched or excluded
import glob
ref_files = sorted(glob.glob("data/reference/operator_sites/*.csv"))
ref_path = "data/reference/operator_sites/*.csv"
if ref_files:
    ref = pd.concat([pd.read_csv(f) for f in ref_files], ignore_index=True)
    open_ = ref[ref.matched_id.isna() & ref.excluded_reason.isna()]
    unknown = ref[ref.matched_id.notna() & ~ref.matched_id.isin(d.id)]
    gate("G3", open_.empty and unknown.empty and ref.operator.nunique() >= 15,
         f"operator site lists: {ref.operator.nunique()} operators (need 15), {len(ref)} sites, "
         f"{len(open_)} unmatched, {len(unknown)} matched to unknown ids")
else:
    gate("G3", False, f"{ref_path} missing – built by coverage tasks")

# G4 no large active plant rests on weak evidence
weak = act[(act.nameplate_capacity_gwh >= 10) & (act.confidence < 0.6)]
gate("G4", weak.empty, f"active plants >=10 GWh/yr with confidence <0.6: {len(weak)}")

# G5 no row still carries a 'research blocked' v1 note
blocked = act[act.research_notes.fillna("").str.contains(r"BLOCKED|NO LIVE SOURCE|WEB ACCESS UNAVAILABLE|UNVERIFIED THIS SESSION", regex=True)]
gate("G5", blocked.empty, f"active rows still carrying blocked-research notes: {len(blocked)}")

print(f"{'PASS' if not fails else 'FAIL'} done-gates: {len(fails)} open {fails or ''}")
sys.exit(1 if fails else 0)
