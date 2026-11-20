#!/usr/bin/env python3
"""One-off (lead): build team/tasks.json and team/assignments.json from the v1 baseline.

Every baseline id is assigned to exactly one re-verification task, grouped by operator
family (majors) or by region (tails). Re-running overwrites both files – only do so
before work starts.
"""
import json

import pandas as pd

d = pd.read_csv("data/baseline/factories_v1.csv")
s = (d.operator.fillna("").astype(str) + " " + d.parent_company.fillna("").astype(str)).str.lower()
groups = [
    ("T002", "CATL (pilot)", ["catl", "contemporary amperex"]),
    ("T003", "BYD / FinDreams", ["byd", "findreams"]),
    ("T004", "CALB + Chuneng", ["calb", "china lithium battery", "chuneng"]),
    ("T005", "Gotion", ["gotion"]),
    ("T006", "EVE Energy + Hithium", ["eve energy", "hithium"]),
    ("T007", "Sunwoda + REPT Battero", ["sunwoda", "rept"]),
    ("T008", "SVOLT + Great Power", ["svolt", "great power"]),
    ("T010", "LG Energy Solution (incl. Ultium, L-H JVs)", ["lg energy", "lges", "ultium", "l-h battery", "lg chem"]),
    ("T011", "SK On + Samsung SDI (incl. BlueOval SK, StarPlus)", ["sk on", "sk battery", "samsung sdi", "blueoval", "starplus"]),
    ("T012", "Envision AESC", ["envision", "aesc"]),
    ("T013", "Panasonic, Toyota, Tesla, Honda, PPES", ["panasonic", "toyota", "tesla", "prime planet", "honda", "primearth"]),
    ("T009", "China mid-tier: Lishen, Farasis, Ganfeng, Zenergy, Lanjun, BAK, Tianneng",
     ["lishen", "farasis", "ganfeng", "zenergy", "lanjun", "bak battery", "cbak", "tianneng"]),
]
assign = {}
for t, _, keys in groups:
    for rid, txt in zip(d.id, s):
        if rid not in assign and any(k in txt for k in keys):
            assign[rid] = t
rest = d[~d.id.isin(assign)]


def chunk(df, names):
    df = df.sort_values(["country", "operator"])
    per = -(-len(df) // len(names))
    for k, t in enumerate(names):
        for rid in df.id.iloc[k * per:(k + 1) * per]:
            assign[rid] = t


chunk(rest[rest.region == "China"], ["T021", "T022", "T023", "T024"])
chunk(rest[rest.region == "Europe"], ["T014", "T015"])
chunk(rest[rest.region == "USA"], ["T016", "T017"])
chunk(rest[rest.region == "India"], ["T018"])
chunk(rest[rest.region.isin(["Japan", "South Korea", "Southeast Asia"])], ["T019"])
chunk(rest[rest.region == "Rest of World"], ["T020"])
assert len(assign) == len(d), (len(assign), len(d))
a = {}
for rid, t in assign.items():
    a.setdefault(t, []).append(rid)
json.dump({t: sorted(v) for t, v in sorted(a.items())}, open("team/assignments.json", "w"), indent=1)

titles = {g[0]: g[1] for g in groups}
titles.update({"T021": "China tail batch 1", "T022": "China tail batch 2", "T023": "China tail batch 3",
               "T024": "China tail batch 4", "T014": "Europe tail A (status & cancellation refresh)",
               "T015": "Europe tail B (status & cancellation refresh)", "T016": "USA tail A (status & cancellation refresh)",
               "T017": "USA tail B (status & cancellation refresh)", "T018": "India",
               "T019": "Japan / South Korea / Southeast Asia tail", "T020": "Rest of World"})
majors = {g[0] for g in groups}


def task(id, title, ws, files, deps, acc, risk, status="pending"):
    return {"id": id, "title": title, "workstream": ws, "owner": None, "files": files, "depends_on": deps,
            "acceptance": acc, "risk": risk, "contract": {"path": "team/CONVENTIONS.md", "approved": True}, "status": status,
            "branch": None, "pr": None, "attempts": 0, "assumptions": [],
            "audit": {"verdict": None, "by": None, "notes": None}}


common = ["Every assigned id in team/assignments.json appears exactly once in the patch (update or remove)",
          "python3 checks/run_all.py exits 0 with the patch applied (C1-C5)",
          "Auditor sample: >=90% of sampled quotes found on page; 0 values contradicted by their own quote (R1)",
          "Installed vs nameplate separated; hub/component double counts resolved (R2, R3)",
          "Active non-operational rows carry evidence dated >=2025-06 or a note that none exists (R4)"]
tasks = [task("T001", "Contracts: baseline snapshot, rebuild.py, checks, CONVENTIONS", "D. Integration",
              ["scripts/rebuild.py", "checks/**", "team/CONVENTIONS.md", "data/baseline/**"], [],
              ["rebuild reproduces v1 capacity_by_year.csv exactly", "checks/run_all.py exits 0 on baseline"], "high",
              status="in_review")]
tasks[0].update(owner="lead", contract={"path": "team/CONVENTIONS.md", "approved": True})
for t in sorted(a):
    op = t in majors
    files = [f"data/patches/{t}.json"] + ([f"data/reference/operator_sites/{t}.csv"] if op else [])
    acc = common + ([f"Operator's own disclosed site list in data/reference/operator_sites/{t}.csv; "
                     "every site matched or excluded (G3)"] if op else [])
    tasks.append(task(t, f"Re-verify: {titles[t]} ({len(a[t])} rows)", "A. Majors" if op else "B. Tails", files,
                      ["T001"] if t == "T002" else ["T002"], acc, "high" if op else "normal"))
for t, reg in [("T025", "China"), ("T026", "Europe + USA"), ("T027", "India, Japan, South Korea, Southeast Asia"),
               ("T028", "Rest of World")]:
    tasks.append(task(t, f"Discovery: cell plants in {reg} announced/started 2023-2026 missing from the DB",
                      "C. Discovery", [f"data/reference/candidates/{t}.csv"], ["T002"],
                      ["Every candidate has an open source_url and is checked against factories_export.csv",
                       "Each candidate is a cell plant (not pack/materials)"], "normal"))
tasks.append(task("T029", "Lead: turn discovery candidates into add-tasks", "D. Integration",
                  ["team/tasks.json", "team/assignments.json"], ["T025", "T026", "T027", "T028"],
                  ["Each candidate assigned to an add-task or rejected with reason"], "normal"))
tasks.append(task("T030", "Lead: benchmark reconciliation, installed-capacity timeseries, refresh QA/report/chart/map, CLAUDE.md schema",
                  "D. Integration", ["scripts/build_timeseries.py", "scripts/qa.py", "scripts/build_report.py",
                                     "scripts/make_chart_png.py", "scripts/make_map.py", "CLAUDE.md", "qa_report.md", "report.html"],
                  sorted(a), ["checks/done_gates.py exits 0",
                              "Region and chemistry comparison vs IEA/BNEF documented in qa_report.md"], "high"))
json.dump({"objective": "Battery cell gigafactory DB v2 (see team/SPEC.md)", "tasks": tasks},
          open("team/tasks.json", "w"), indent=2)
for t in sorted(a):
    print(t, len(a[t]), round(d[d.id.isin(a[t])].nameplate_capacity_gwh.sum()), titles[t])
