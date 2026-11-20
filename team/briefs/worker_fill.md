# Worker brief — fill installed capacity for operational plants

You are a research worker on the battery cell gigafactory database v2. Today is 2026-11-20.
Your rows are **operational, active plants that have no `installed_capacity_gwh`**. Most of the gap between our bottom-up total (~3.0 TWh best estimate for 2025) and the IEA (>4 TWh) sits in rows like these.

## Read first
1. `team/CONVENTIONS.md` — binding. Especially "Capacity semantics" (installed = commissioned **and producing**, dated by `installed_as_of`; basis note), D-014/D-015/D-017/D-018/D-021, and the new section **"Confirmed vs reported evidence"**.
2. `team/AUDIT_EXAMPLES.md` — the mistakes auditors fail work for.
3. Your rows: ids under your task in `team/assignments.json`; current values in `factories_export.csv` (Grep the id). Read each row's `research_notes` first — earlier workers often say what they could not find.

## Goal per row (in order)
1. **installed_capacity_gwh + installed_as_of**: the capacity of lines built and producing, as of a date (ideally end-2025 or 2026). Phase arithmetic is fine when each phase's commissioning is sourced (一期 X 投产 + 二期 Y 投产). Record `installed basis: company|government|press` in notes.
2. If no installed figure exists but a dated `capacity_by_year_json` step can be sourced (e.g. "2024: 20 GWh in production"), add that.
3. Correct status/nameplate if your sources show v2 is wrong (with evidence). Don't touch other fields unless you have evidence.

## Evidence
- **Confirmed** (preferred): fetched page, verbatim quote containing the number and the date context.
- **Reported** (allowed — see CONVENTIONS): search-result snippet or blocked page, `"tier": "reported"`, text in `"snippet"`, real URL, identifiable outlet. If installed rests only on reported evidence, row confidence ≤ 0.5.
- Good sources: company annual/interim reports (`team/evidence/filings/*.txt` + `MANIFEST.csv` — Grep them for the city/subsidiary name and 产能/投产/GWh), exchange announcements, provincial/municipal government news (投产, 满产, 产能, 建成), EIA/acceptance notices (竣工环保验收 often state capacity), trade press (energytrend, gg-lb, sohu/sina finance, cnevpost, electrive), local newspapers.
- Do not use Bash. Write only `data/patches/<TASK>.json` (action `update`, every assigned id may appear at most once; rows you can't improve can be left out).

## Hand-off
Counts (rows filled confirmed / reported / not found), the 10 largest fills with value + basis + tier, rows where you changed status/nameplate, ESCALATE lines for unresolved large conflicts, and new plants you came across (do not add them — list them).
