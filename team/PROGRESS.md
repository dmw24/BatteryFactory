# Progress log

Append-only. Newest at the bottom. Every session adds one entry.

Format:
## YYYY-MM-DD HH:MM – <role>/<name> – <task id>
- Did: (only what a tool result in this session shows)
- Checks: <command> → <result>
- Not verified:
- Discoveries affecting other tasks:
- Next / handoff:

---


## 2026-11-20 13:00 – lead – T001
- Did: bootstrapped team-in-a-box (standard/dataset/merge); froze v1 export as data/baseline/factories_v1.csv; wrote scripts/rebuild.py (baseline + patches → DB/export/field_evidence/removed), checks/run_all.py (C0–C6), checks/done_gates.py (G1–G5), checks/verify_quotes.py; SPEC, ACCEPTANCE, CONVENTIONS, DECISIONS D-001..D-011; backlog of 30 tasks with every v1 id assigned once (team/assignments.json).
- Checks: python3 checks/run_all.py → PASS (C3v1 WARN 3 legacy rows, C5 1 paywalled v1 source); rebuild reproduces v1 capacity_by_year.csv byte-identical; done_gates → 7 open (expected).
- Not verified: CI workflow not run (no push yet).
- Discoveries: v1 CATL Ningde hub (330 GWh) note says it includes Fuding, which also has its own 120 GWh row → likely double count; for T002.

## 2026-11-20 – lead – T002/T025-T029 integration
- Did: discovery T025–T028 committed (80 candidates, routed in team/candidate_routing.csv; T026 cites unfetched search links → hints only). T002 audit 1 = fail (diligence); brief/conventions calibrated; cninfo annual reports for 11 makers extracted (scripts/fetch_filings.py). T002 rework received: run_all → C2 fails 1 row (Lingang null status), sent back.
- Discovery affecting T030: installed_capacity_gwh carries mixed dates (installed_as_of 2025-12 … 2026-10) and mixed basis (government 建成 vs company). CATL rows sum 973 GWh installed vs company 772 GWh end-2025. G2 (end-2025 vs IEA) must use a dated measure: capacity_by_year_json["2025"] or installed with installed_as_of ≤ 2025-12-31, and reconcile per operator against data/reference/operator_totals.csv.

## 2026-11-20 – lead – checkpoint after T002/T004 merge
- Done gates: G1a 61/159 top plants verified; G1b 24%; G2a installed 1,871 GWh but only 34/256 operational rows carry installed_capacity_gwh → G2 as defined will undercount; T030 must define the 2025 online measure (installed where sourced; else a flagged estimate) and possibly revise G2 with owner awareness. G4 19, G5 5 open.
- Added C7 (reference CSVs parse) after T002.csv broke done_gates.
- Spend so far (subagent tokens, approx): workers ~2.3M, auditors ~0.8M.

## 2026-11-20 – lead – T030 prep (geo QA)
- scripts/geo_check.py: 295 rows testable against the city in their name; 16 flagged >150 km, of which 15 are US homonym false positives (Florence SC/AL etc. — checker lacks state disambiguation) and 1 real error (Zoolnasm Guangde at Yangzhou) → lead `fix` patch data/patches/T030_geo.json. Chinese GEO=city tags vs names: 5 mismatches, 4 legitimate (county→prefecture), 1 the same Zoolnasm row. Great Power Guangde (v1 site_unflagged at Shenzhen) already nulled by T008.
- rebuild.py: new lead-only `fix` action (changes fields without stamping re-verification).

## 2026-11-20 – lead – T030 prep (timeseries v2)
- build_timeseries.py v2: excludes non-cell rows; merges re-verified installed_capacity_gwh (dated by installed_as_of) into each plant's sourced timeline and the full nameplate at capacity_ref_year as a planned point; inactive (paused/cancelled, D-018) plants stop counting after 2025; Series B = sourced level where it exists, else nameplate for active operational plants.
- Interim result (mid-run, tails pending): 2025 Series A 3,731 GWh (90% from sourced points) vs IEA >4,000 (93%); Series B 3,746; China 78% of A. v1 Series B 2025 was 5,518.

## 2026-11-20 – lead – T030 integration (partial)
- All 436 rows re-verified (G1a 158/158, G1b 100%); G2b 86%, G3, G5 pass. Open: G2a (as defined it sums undated installed figures: 2,774 GWh; dated Series A 2025 = ~3.7 TWh) and G4 (87 large plants <0.6 — open-source limit). Both go to owner at close-out.
- rebuild.py: view `factories_active` (cell, active, comparable). build_report.py/qa.py now aggregate on it; removed a cross-status nameplate sum in build_report (rule 1) and switched China share to sourced installed.
- PNG chart/map scripts import `ember_style`, which is not in the repo or this environment → PNGs not regenerated (capacity_chart.png, capacity_map.png are stale v1 images). report.html, qa_report.md and CSVs are regenerated.
