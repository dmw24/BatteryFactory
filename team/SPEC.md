# Spec — Battery cell gigafactory database v2

> Signed off by: project owner (chat, 2026-11-20): "Sonnet and above… I'll leave it to you to decide the best thing to do" + open-data and bring-up-to-date requirements. Recorded as D-001.

## Profile and tier
Profile: dataset · Tier: standard · Why: ~35 tasks over ~378 existing rows plus discovery; output will be published, so audit is heavier than Lite, but each task has strong executable checks, so Full's every-task audit is not needed.

## Objective
Turn the v1 database (378 rows, median confidence 0.7, single-source rows, 26 rows researched while web access was blocked, operational nameplate 5.8 TWh vs IEA >4 TWh) into a v2 that is **re-verified row by row from open sources, current to November 2026, with field-level provenance**, and whose bottom-up installed capacity lands in the same order of magnitude as IEA/BNEF.

## Audience and use
Published by Ember as an open dataset; used for capacity-by-region / chemistry analysis and charts. Errors in big plants move headline numbers, so they are the priority.

## Scope
- In: every v1 row (re-verify, correct, or remove with reason); new plants announced or discovered up to Nov 2026; cancelled/paused projects; installed-now vs eventual nameplate; field-level sources with verbatim quotes.
- Out: pack/module/materials plants (kept only if already present and flagged non-cell); monthly production/utilisation; forecasts beyond company-announced plans; paid data.

## Inputs and sources
- **Open data only (D-002).** Every value must rest on a page anyone can read free: company sites, filings and annual reports (incl. Chinese exchange filings, cninfo/HKEX), government/provincial releases, permit filings, open news (electrive, cnevpost, energytrend, ess-news, Reuters, local press, Wikipedia as a pointer only).
- IEA / BNEF / Benchmark / SNE: **benchmarks only**, never a row source. Hard-paywall domains are blocked by check C5.
- Baseline: `data/baseline/factories_v1.csv` (frozen v1 export).

## Method
- Each worker task owns one **operator family** (or a regional tail batch) and re-verifies all of its rows, adds missing sites the company itself discloses, and records the company's own site list in `data/reference/operator_sites/<task>.csv`. Grouping by operator is what exposes hub totals counted twice.
- Changes are **patch files** (`data/patches/<task>.json`) on top of the baseline; `scripts/rebuild.py` regenerates DB + export. Nothing is edited in place.
- Two capacity measures per plant: `installed_capacity_gwh` (commissioned now, with `installed_as_of`) and `nameplate_capacity_gwh` (full eventual nameplate). This replaces "operational at full future nameplate", the main cause of the v1 overshoot.
- `project_state` (active | paused | cancelled) is added beside `status`; `status` keeps its three values and means the furthest stage reached (D-003).

## Contracts
`team/CONVENTIONS.md` (patch format, vocabularies, evidence rules) — fixed before any worker starts.

## Workstreams
| Workstream | Owns (paths) | Notes |
|---|---|---|
| A. Majors (China, Korea, Japan, US cos.) | `data/patches/T0xx.json`, `data/reference/operator_sites/T0xx.csv` | one task per operator family, high risk |
| B. Regional tails & status refresh | same pattern | Europe/USA/India cancellations, China tail |
| C. Discovery | `data/reference/candidates/T0xx.csv` | finds plants not in DB; lead turns them into add-tasks |
| D. Integration (lead) | `scripts/`, `checks/`, docs, charts | benchmark reconciliation, report refresh |

## Constraints
- Models: Sonnet or above for every role (D-004). Workers Sonnet/high; auditor and lead Opus/high.
- Budget: staged — wave 1 (majors) first, owner reviews before tail waves (D-005).
- Workers have web + file tools only, no shell (untrusted web content).

## Risks and known unknowns
- Chinese company/provincial sites often block or rate-limit; quotes may be in Chinese (allowed, `language` recorded).
- "Capacity" in Chinese press often mixes planned and built (规划 vs 已投产) — key audit probe.
- Hub vs individual sites: company-level or city-level totals being stored as one site, or a hub row plus its component rows both kept.
- Open sources undercount small Chinese makers → bottom-up total may sit below IEA; that is acceptable if explained (G2 band).
