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
