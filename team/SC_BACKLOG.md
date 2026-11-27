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
SC021 nickel ex-Indonesia · SC032 manganese · SC150 offline geocoding.

## Next
1. Merge running tasks; re-run SC audit (audit 2) on the whole after fixes + new steps.
2. Gap passes where coverage is weakest (team/RECONCILIATION_SC.md): China processing site-level capacity (anode,
   cathode, separator, electrolyte — more filings: unlisted makers via MIIT + provincial EIA notices), China graphite mine
   output, Zimbabwe lithium, Indonesian cobalt in MHP, nickel/cobalt refining China per plant.
3. Cross-step links (`feeds`: mine → refinery → pCAM → CAM → cell plant, offtakes), supply-chain charts (Ember style),
   docs (docs/SUPPLY_CHAIN_METHODS.md, data dictionary section), FINAL report section; delete the recurring wake task when done.
