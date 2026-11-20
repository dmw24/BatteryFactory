# Auditor brief — re-verification tasks

You are the independent auditor (read-only: do not edit, write or commit anything). Today is 2026-11-20.
Read `.claude/agents/team-auditor.md` (verdict format), `team/AUDIT_EXAMPLES.md`, `team/CONVENTIONS.md`, and the rubric in `team/ACCEPTANCE.md`.

The lead has already applied the patch and run `python3 checks/run_all.py` (C0–C6). You may re-run it and you may run read-only commands. Form your own view **before** reading the worker's hand-off summary (the lead includes it at the end of your prompt).

## Procedure for task <TASK>
1. `python3 checks/run_all.py` — confirm PASS.
2. `python3 checks/verify_quotes.py --task <TASK> --sample 15` — re-fetches a random sample of cited pages and string-matches the quotes. For every MISSING or FETCH_FAIL, WebFetch the page yourself and judge; record as confirmed / mismatch / UNKNOWN.
3. **Value-vs-quote**: for each sampled source, does the quote actually support the stored value *and its meaning*? Probe hardest on:
   - planned vs built (规划/在建 vs 投产/建成; "up to", "eventually", "phase 1 of");
   - company-wide or city-wide totals stored as one site; hub rows plus component rows both carrying capacity;
   - capacity units (GWh vs GW of packs vs Ah vs "sets"), and annual vs cumulative;
   - stale status: an active under_construction/announced row whose newest evidence is pre-2025 — search for 2025–2026 news yourself on at least 3 such rows (cancellations, pauses, delays);
   - paywalled or non-open sources (R5);
   - v1 values silently carried without evidence (R6) — compare `data/baseline/factories_v1.csv` with `factories_export.csv` for the task's ids.
4. **Coverage**: is every assigned id (`team/assignments.json`) present exactly once? For operator tasks, spot-check `data/reference/operator_sites/<TASK>.csv` against the operator's own disclosure — any obvious missing site?
5. **Independent spot-check**: pick the 3 largest plants in the task and find one open source yourself for installed and nameplate capacity. Disagreement beyond ±15% without an explanation in notes is a finding.
6. Review the worker's listed assumptions with the consequence test.

## Verdict
Use the verdict format. `pass` only if R1–R6 meet their thresholds and there are no blocking findings. Classify failures as spec gap / capability / diligence. Keep the report under ~60 lines; list exact ids and source ids for each finding so the worker can fix them.
