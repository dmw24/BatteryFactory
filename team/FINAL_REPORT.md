# Final report — Battery cell gigafactory database v2

Date: 2026-11-20 · Tier: standard · Profile: dataset · Branch: `claude/inspiring-hypatia-c9j8ju`
Status: **awaiting owner sign-off** (two done-gates open by design — see "Decisions for the owner").

## What was built
- **Every v1 row re-verified from open sources** (438 rows: 378 v1 − 26 removed with evidence + 86 added). All 384 active comparable cell plants carry `last_verified`; 157/157 plants making up 90% of nameplate verified.
- **Field-level provenance**: 1,673 evidence links (702 distinct open URLs) in `data/field_evidence.csv`, each with a verbatim quote; company filings (cninfo/HKEX/SEC/ESG) extracted for 20 operators (`team/evidence/filings/MANIFEST.csv`).
- **Reproducible build**: frozen v1 baseline + 26 patch files → `scripts/rebuild.py`; integrity checks `checks/run_all.py` (C0–C7, all pass); done-gates `checks/done_gates.py`; quote re-fetcher `checks/verify_quotes.py`.
- **Schema v2**: `project_state` (41 paused/cancelled projects, ~480 GWh nameplate now excluded from totals), `installed_capacity_gwh` + date (separate from full-plan nameplate), `site_type`, `geo_precision`; view `factories_active`; long-duration non-Li chemistries flagged non-comparable (D-019).
- **Current to Nov 2026**: cancellations/pauses (ACC Kaiserslautern/Termoli, Northvolt Drei/Six, Britishvolt, Italvolt, Freyr, Cellforce, iM3NY, Natron, Amprius Brighton, BlueOval Kentucky retooling, StarPlus plant 2 on hold…), JV ownership changes (BlueOval SK split, NextStar → 100% LGES, SynergyCells → Samsung SDI), and 86 new plants (Chuneng Yichang/Xiangyang/Wuhan, CALB Zigong/Zaozhuang, Hyundai–SK Bartow, Qingna Guangde, Pengcheng Yibin, Guoke Lanzhou/Meishan, Shengxi…).

## Headline numbers (active comparable plants, never summed across status)
| status | plants | nameplate GWh/yr (full plan) | sourced installed GWh/yr |
|---|---:|---:|---:|
| operational | 248 | 6,204 | 2,767 (103 plants) |
| under construction | 64 | 1,613 | – |
| announced | 44 | 761 | – |

2025 capacity online (D-023/D-024): **A confirmed 2,083 GWh** (52% of IEA) · **C best estimate 2,996 GWh** (75%: confirmed + 832 reported v1 history + 81 nameplate fill) · **B upper fill 3,511 GWh** (88%) · IEA >4,000 GWh. China 83% of A, 75% of C.

**Confirmed vs reported (owner request, D-024):** v1 values that v2 blanked only because they could not be re-confirmed were restored as *reported* (flagged, v1 source, confidence ≤0.5 where status/capacity): 18 nameplates, 14 statuses, 42 ramps (after an Opus review of each row's notes; 107 capacity values stayed null because v2 contradicted/superseded them) plus ~600 descriptive values (chemistry, format, end market, years) by rule. 29 rows have evidence_tier = reported. v1 had claimed 5,518 (Series B) — that overshoot came from future targets counted as online and unsupported timeline points.

## How it was verified
Each task: worker (Sonnet) → integrity checks → independent auditor (Opus, fresh context) re-fetching sources and judging value-vs-quote meaning → fixes → lead verification. 24 Opus audits + a FINAL sweep; 5 tail tasks waived by the 50% sampling rule, then spot-checked in the FINAL sweep (85% of their sampled quotes confirmed — below the 90% bar; residual misses are mostly 403/geo-blocked pages).

## What the harness caught (from team/AUDIT_LOG.md)
- Checks (C0–C7): id typos, vocab, missing ref years, unparseable CSVs, null-status rows — cheap, every merge.
- Auditors (the main value): planned-vs-built misreads (规划 vs 投产), structure-completion dates used as full-capacity years, company-wide totals stored as one site, hub + component double counts (CATL Ningde/Fuding/Times-FAW), removals without evidence (Nantong, Mianyang, Pylontech Shanghai), confidence parked at the 0.6 gate, a prompt-injection page (ignored), and a summary-derived quote.
- FINAL sweep: the lead's own Series A was inflated ~1.5 TWh by unsupported v1 timeline points → fixed (D-023).
- Verifier bugs fixed along the way: gzip pages, PDF text containing `<`.

## Decisions & assumptions
23 decisions logged in `team/DECISIONS.md` (D-001…D-023), most marked **pending owner** — notably D-003 (project_state beside status), D-014/015/017/021 (what counts as nameplate), D-016 (status evidence strength), D-018 (idle plants), D-019 (non-comparable chemistries), D-023 (Series A/B v2).

## Decisions for the owner (close-out gate)
1. **G2a (bottom-up ≥3.2 TWh)** fails: open sources only document ~2.1–2.8 TWh for 2025 vs IEA >4 TWh. Accept as a documented coverage gap, or fund a further pass (e.g. Chinese provincial/EIA filings for BYD, CALB, Gotion bases)?
2. **G4 (no large plant <0.6 confidence)** fails: 88 plants ≥10 GWh sit below 0.6 because no open source settles them (escalated per row in notes). Accept, or target the top ~20 by capacity?
3. Review the pending decisions in DECISIONS.md, especially D-019 (excluding Form/ESS/Eos etc. from totals) and D-022 ("up to" = design capacity).
4. Licence/publication: choose a dataset licence (e.g. CC BY 4.0) before publishing.

## Known limitations
- Installed capacity is sourced for only 103 of 248 operational plants; chemistry/format were nulled where unconfirmed (most operational capacity now has null chemistry, so chemistry splits are weak).
- Coordinates: 299 city-centroid, 33 unvalidated v1 points; several wrong points were nulled.
- PNG chart/map (`capacity_chart*.png`, `capacity_map.png`) are stale v1 images: their scripts need the `ember_style` module, which is not in this repo. `report.html`, `qa_report.md` and CSVs are regenerated.
- Some sources were blocked from this environment (energy-storage.news, english.etnews.com, several gov sites).

## Spend (approximate, from sub-agent usage reports)
~38 worker runs/reworks (Sonnet, ~7M tokens) and ~25 audits (Opus, ~3.7M tokens), plus the lead session. No Haiku used (D-004).
