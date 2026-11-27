# Supply-chain backlog (lead's running plan; resume from here after a wake-up)

Loop per task: validate (`python3 -c json.load`, `team/scripts/sc_demote.py TASK`), `python3 scripts/sc_build_all.py`,
`python3 checks/sc_checks.py`, `python3 checks/verify_quotes.py --sc --task TASK --sample 60` → demote MISSING sources
(`team/scripts/sc_demote.py TASK S1 S2`) → record company totals (data/supply_chain/company_totals.csv, geo_scope) →
mark merged in team/tasks.json → commit + push.
Lessons: ≤3 WebSearch-heavy researchers per lead turn (shared 200/turn budget); filing passes (local cninfo text via
scripts/fetch_filings.py) need no search; open datasets mirrored via team/evidence/open_datasets/LOCAL.csv.

## Done (2026-11-27)
Lithium mines/refining (SC001–008, SC101–102, SC106–107, SC120–121, SC030), cathode/pCAM (SC009–014, SC103–105, SC122),
anode/graphite (SC015, SC016, SC110), nickel Indonesia (SC020 + CGS dataset), cobalt (SC025, SC113), electrolyte/
separator/foil (SC028, SC111, SC112), recycling (SC031), MIIT completeness (SC130), dedupe (SC140), benchmarks (SC090),
SC audit 1 (FAIL → fixed, AUDIT_LOG).

## Running
SC191 installed capacity (filings) · SC192 installed capacity (web, ex-China).

## Also done since
SC021 nickel ex-Indonesia, SC032 manganese, SC150/SC160 coordinates, SC161 China plant capacities, SC170 supply links,
SC180 HKEX filings, sc_timeseries, charts, docs; SC audits 2 and 3 (FAIL → fixed; built = confirmed-date floor).

## Next (as of 2026-11-27 evening; 905 assets, 14/14 checks, audits 1–3 fixed)
1. Built-capacity evidence for remaining Chinese bases (EIA 竣工验收 notices; HKEX prospectuses of A+H listings —
   route in team/lessons/hkex-filings.md: Hunan Yuneng, Capchem, Tinci, CNGR H, Lopal H).
2. Mine output gaps: Zimbabwe lithium (national only), China lepidolite/graphite, Indonesian ore grades (nickel),
   South Africa/Gabon manganese grades.
3. More plant-level supply links where contracts name plants (current: 40 rows with feeds).
4. HPMSA producers in China; cobalt refineries China per plant; Electra CoSO4 unit check.
5. Opus audit 4 on SC191–SC195 + any new passes; refresh FINAL_REPORT_SC.md and charts; delete recurring wake task
   when the owner's 2-day window ends or nothing material remains.
