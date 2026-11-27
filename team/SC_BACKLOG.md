# Supply-chain backlog (lead's running plan; resume from here after a wake-up)

Per wave: launch Sonnet `team-researcher` agents with team/briefs/SC_RESEARCHER.md → on hand-back run
`python3 checks/sc_checks.py` and `python3 checks/verify_quotes.py --sc --task SCxxx --sample 40` → fix/merge
(`team/scripts/set_status.py merged SCxxx ...`) → `python3 scripts/sc_benchmark.py` → commit + push.
After each step's waves: completeness pass (company + list cross-check), Opus audit sample, fixes.

| wave | tasks | step | state |
|---|---|---|---|
| 1 | SC001–SC008 | lithium mines (AU, S.Am brine, CN, Africa, rest) + refining (CN×2, ex-CN) | launched 2026-11-27 |
| 2 | SC009–SC014 | cathode CAM (CN NCM, CN LFP ×2, KR/JP, EU/NA/other) + pCAM/FePO4 | next |
| 3 | SC015–SC019 | anode (CN synthetic ×2, natural graphite anode/spherical, ex-CN) + natural graphite mines | |
| 4 | SC020–SC024 | nickel mines (Indonesia, PH/NC/AU/other) + refining (Indonesia HPAL/RKEF-matte, NiSO4 CN/other) | |
| 5 | SC025–SC027 | cobalt (DRC mines, refineries CN/other) | |
| 6 | SC028–SC030 | electrolyte + LiPF6; separators; copper foil | |
| 7 | SC031–SC032 | manganese (HPMSA, battery Mn) + recycling (black mass, hydromet) | |
| 8 | SC033+ | completeness passes per step, cross-step `feeds`, audits, report, charts | |
