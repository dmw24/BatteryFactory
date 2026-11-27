# Decisions and assumptions

Choices made and why, so no one relitigates them. Newest at the bottom.

- **decision** – made or approved by the lead or a human.
- **assumption** – made by any agent under the consequence test: a reasonable alternative would not materially change a deliverable and is cheap to undo. Record the alternative rejected. List the ID in the task's `assumptions` field. The auditor reviews assumptions; the lead batches open ones for the human at checkpoints.

| ID | Date | Type | Task | Choice | Alternative rejected | Why | By | Reviewed |
|---|---|---|---|---|---|---|---|---|

| D-001 | 2026-11-20 | decision | – | Profile dataset, tier Standard | Full tier | ~35 tasks with strong executable checks; Full's every-task audit doubles Opus spend | lead (owner delegated choices in chat) | pending owner |
| D-002 | 2026-11-20 | decision | – | Open data only: every row value must rest on a freely readable page; IEA/BNEF/Benchmark used only as benchmarks; hard-paywall domains blocked by C5 | allow paywalled trackers as sources | owner requirement (chat 2026-11-20) | owner | yes (owner stated) |
| D-003 | 2026-11-20 | decision | – | Keep `status` 3-valued (furthest stage reached) and add `project_state` active/paused/cancelled | add cancelled/paused to status | keeps CLAUDE.md rule 1 intact and backwards compatible; aggregates filter project_state=active | lead | pending owner |
| D-004 | 2026-11-20 | decision | – | No Haiku anywhere. Lead Opus/high, auditor Opus/high, workers Sonnet/high | Haiku for mechanical jobs | owner: "Sonnet and above, just in case" | owner | yes (owner stated) |
| D-005 | 2026-11-20 | decision | – | Staged budget: pilot (T002 CATL) → wave 1 majors → owner check-in → tails/discovery | run everything at once | owner wants to limit usage; majors carry ~75% of capacity | lead | pending owner |
| D-006 | 2026-11-20 | decision | – | Done-gate thresholds fixed before any v2 data: G2a 3.2–5.0 TWh installed, G2b China 75–90%, G1b 90% verified, G4 no ≥10 GWh plant below 0.6 | tighter IEA ±10% band | bottom-up from open sources legitimately undercounts small makers; band still catches the v1 5.8 TWh overshoot | lead | pending owner |
| D-007 | 2026-11-20 | decision | – | v1 export frozen as data/baseline/factories_v1.csv; all changes via data/patches/<task>.json applied by scripts/rebuild.py | keep editing factories.db via ad-hoc loaders | v1 export was not reproducible from repo files (6 capacity values and 1 removed row existed only in the export) | lead | pending owner |
| D-008 | 2026-11-20 | decision | – | Split capacity into installed_capacity_gwh (+installed_as_of) and nameplate_capacity_gwh | single nameplate | v1 operational nameplate 5.8 TWh vs IEA >4 TWh: future targets counted as operational | lead | pending owner |
| D-009 | 2026-11-20 | decision | – | Workers are web+file subagents with no shell; lead runs rebuild/checks and commits | workers run scripts | untrusted web content + shell is the risky combination | lead | pending owner |
| D-010 | 2026-11-20 | decision | – | Field-level provenance is enforced by checks/run_all.py C4 (url + verbatim quote per field) rather than the skill's SRC-ID evidence files; the skill's check_provenance.py stays enabled but has nothing to scan | SRC-ID evidence base in team/evidence | per-row web evidence fits patch files better than a shared evidence base | lead | pending owner |
| D-011 | 2026-11-20 | decision | – | All re-verification tasks share one contract (team/CONVENTIONS.md) instead of per-task contracts | per-task contract drafted by each worker | tasks are identical in shape; per-task contracts would add ~23 Opus review rounds for no new information | lead | pending owner |
| D-012 | 2026-11-20 | decision | T002 | capacity_ref_year falls back to the publication year of the nameplate source when no target year is given (noted in notes) | leave null (breaks CLAUDE.md rule 2) / drop nameplate | pilot nulled ref year on 9 rows; rule 2 requires it and a dated statement is the honest reference | lead | pending owner |
| D-013 | 2026-11-20 | decision | T003 | User-generated aggregator posts (e.g. Xueqiu) are open but unvetted: allowed as evidence only with confidence ≤ 0.5 and never as the sole source of a ≥10 GWh figure at ≥0.6 | ban aggregators / treat like press | no better open source exists for some BYD sites; low confidence keeps them out of G4-passing claims | lead | pending owner |
| D-014 | 2026-11-20 | decision | T004 | Nameplate = full current site plan: built + UC + every publicly stated site-specific phase with a GWh figure (dated or not), same for hubs; ref year = due year of last phase, else fallback with note | built+UC only (worker reading) / hub-only exception (D-012 text) | auditor T004 found the convention ambiguous; one rule for all rows; pipeline vs online is carried by installed_capacity_gwh | lead | pending owner |
| D-015 | 2026-11-20 | decision | T005 | Undated site totals without phase structure ("over time", "can later be doubled") are aspirations → notes, not nameplate; later company filings supersede earlier press figures; confidence capped at 0.5 for stale (>18 months) installed or unresolved >15% conflicts; never remove a row / flip is_cell to pass a check | count "over time" totals under D-014 | auditor T005: D-014 let 80+32 GWh of undated pipeline in; worker removed an existing plant after a lead hint that offered removal as an option to clear C2 | lead | pending owner |
| D-016 | 2026-11-20 | decision | T003 | Null status allowed on verified cell rows only at confidence ≤0.4 (C2 relaxed accordingly); env-disclosure-list battery entity ⇒ operational at ≤0.4; tax/subsidiary lists = existence only; teaser-visible quotes (MarkLines) acceptable if visible without login | keep C2 strict (forced guessing) / reject env list entirely | auditor T003: C2 + "null if unconfirmed" pushed workers to cite company names as status evidence. NOTE: this loosens C2 — flagged for owner review | lead | pending owner |
| D-017 | 2026-11-20 | decision | T008 | A site total whose phase structure has been superseded by a later company/official description (different phases/total) is treated as an aspiration: nameplate follows the later description, the old total goes to notes | keep the older larger total under D-014 | auditor T008 (Chengdu 60 vs later 2-phase 31.5 + company projection 19 GWh by 2025) | lead | pending owner |
| D-018 | 2026-11-20 | decision | T011/T015 | Built plants whose production is currently stopped (idle, retooling, bankruptcy) → project_state paused, installed null, last producing capacity in notes; partially idle → installed = producing lines only | keep installed at built capacity | installed means commissioned AND producing; otherwise Series A/B credit idle plants (Ford Kentucky, Lyten Ett) | lead | pending owner |
| D-019 | 2026-11-20 | decision | T016 | Long-duration / non-Li-ion chemistries whose "GWh" is not comparable to Li-ion/Na-ion cell output (iron-air, iron-flow, Ni-H2, liquid metal, zinc-based) stay in the database but are listed in data/reference/non_comparable.csv and excluded from headline capacity totals and benchmark comparisons (reported separately) | count them like Li-ion / drop them | Form Energy 50 GWh = 500 MW × 100 h would distort US totals; IEA/BNEF benchmarks are Li-ion cell capacity | lead | pending owner |
| D-020 | 2026-11-20 | decision | T020/T016 | under_construction requires confirmed physical site works (clearing, foundations, building); a purely ceremonial groundbreaking with nothing after stays announced; stopped construction stays under_construction + paused/cancelled | ceremony = under_construction / preparatory works = announced | auditors T016 (ABF), T020 (Northvolt Six, E-One Moli) found inconsistent readings | lead | pending owner |
| D-021 | 2026-11-20 | decision | T024 | When only some phases carry a due year, capacity_ref_year = latest stated phase year, noted "remainder undated"; a project total with only phase 1 described counts under D-014 if the total is site-specific and stated, else D-015 | publication-year fallback | auditor T024: phase-1 year made full nameplate look due early (Shengxi, Zoolnasm) | lead | pending owner |
| D-022 | 2026-11-20 | decision | FINAL | "up to X GWh" counts as nameplate when it is the stated design capacity of a specific plant/phase (PowerCo Salzgitter 20, Forge 3, Lyten Reno 10); it is an aspiration only when it describes undated future expansion | treat every "up to" as aspiration | design capacity is how plants are specified; CONVENTIONS example targeted expansion talk | lead | pending owner |
| D-023 | 2026-11-20 | decision | FINAL | Series A/B v2: A = only re-verified installed figures (dated), with v1 timeline history kept only before the anchor and capped at it; operational rows without a sourced installed figure count 0 in A (online_unquantified); B = A + full nameplate of operational active rows without a sourced figure (upper-bound fill). Non-operational, paused/cancelled (from 2025) and non-comparable rows contribute 0 | v1 timelines as-is (inflated A by ~1.5 TWh with unsupported points) | FINAL sweep finding 1–3 | lead | pending owner |
| D-024 | 2026-11-20 | decision | T031 | Confirmed vs reported: v1 values blanked only because they could not be re-confirmed are restored as REPORTED (reported_fields, evidence tier "reported" = v1 source_url, confidence ≤0.5 if status/capacity); values the v2 research contradicted/superseded stay null; paywalled v1 sources never restored. New Series C (best estimate) = confirmed where sourced, else reported v1 history capped at nameplate, else nameplate fill | keep strict nulls (owner: too strict) | owner request 2026-11-20 | owner | yes (owner stated) |
| D-025 | 2026-11-20 | decision | T035 | Stale but sourced installed figures are entered with their true installed_as_of as a dated floor (Series A carries them forward as a minimum); a dated floor noted as such does not trigger the D-015 confidence cap | leave null / cap confidence | a dated floor is real data and strictly better than null for A; staleness is explicit in the date | lead | pending owner |
| D-026 | 2026-11-20 | decision | T038/T042/T049 | Bundled-scope figures (cells + packs/systems/equipment/power station, no cell split) → row kept, nameplate null, figure in notes | count bundled GWh as cell capacity | Jiuxu 50, Tianpu 50, Yunshi Weilan 15, Baofeng 100–200 would inflate the pipeline with non-cell capacity | lead | pending owner |

## D-027 — Series D: IEA-like commissioned nameplate (owner request 2026-11-22) — pending owner
Owner wants one series on the IEA definition (design nameplate of commissioned lines, utilisation ignored) as a
missing-plant check, alongside our sharper "producing" series. `capacity_by_year.gwh_iea` (D) = max(C, sourced dated
phase steps from capacity_by_year_json, full site nameplate once a DATED capacity_ref_year ≤ year) for operational
active plants; `gwh_iea_high` (D-high) also credits nameplate whose ref year is only the publication-year fallback
(upper bound). 2025: D 3,352 / D-high 4,029 GWh vs IEA >4,000. Earlier years stay well below the IEA (2023 D-high 1,726
vs 2,500; 2024 2,507 vs >3,000), so the 2025 match is partly a fallback-year artefact — treat D-high with care.

## D-028 — Unallocated company capacity, Series E (owner 2026-11-23)
Owner: allowed, provided nothing is double counted and no location is invented. Where a company discloses its
total cell production capacity for a year (filing/prospectus/IR; metric=capacity, basis year_end or
annual_effective; whole-business scope global or china), the excess over the Series D sum of all DB sites mapped
to it (data/reference/company_map.csv, one company per site, JV sites included → remainder can only be
understated) is stored as a company/year line in `capacity_unallocated` — no site, no plant id, no coordinates.
Negative differences are flagged, never netted. No interpolation between disclosed years. Series E = D +
unallocated (scripts/build_unallocated.py → capacity_unallocated.csv, capacity_by_year_e.csv). Planned/target
and segment-only figures are never used. Disclosed output/shipments are kept only as lower-bound checks.

## D-029 — Benchmark set beyond IEA (owner question 2026-11-23)
Benchmarks are overlays, never data. Allowed: any figure on a page anyone can read free — including a paywalled
publisher's own free press release / insight page (BNEF, Benchmark, Rho Motion, SNE) or open press quoting it — with
url + verbatim quote + definition (nameplate/commissioned vs effective vs output; global vs region; cells vs packs).
Stored in data/reference/benchmarks/*.csv, merged by the lead into scripts/benchmarks.csv. The C5 paywall rule
still applies to plant evidence.

## D-030 — Converted company capacity as labelled estimates (owner 2026-11-24, improvement point 2)
Company capacity disclosed only in Ah may be converted to GWh when the chemistry mix makes the voltage defensible;
the result is stored in data/reference/company_capacity/*_estimates.csv, flagged `estimate` in capacity_unallocated,
and reported separately (capacity_by_year_e.csv: gwh_series_e = disclosed only; gwh_series_e_incl_estimates adds them).
A disclosed GWh figure for the same company-year always wins. Applied: Great Power 2021–2025 (亿Ah 年化 × 3.2 V LFP
nominal; cross-check: 2025 → 27.7 GWh vs press "annual capacity ~28.7 GWh" end-Q3 2025). NOT applied: EVE and Sunwoda
report capacity as cell counts (万只) mixing consumer cells of a few Wh with 280 Ah storage cells (and EVE's counts
include primary batteries) — no defensible per-cell energy; Gotion reports Ah output only, not capacity.

## D-031 — One rule for "cells + modules + PACK" wording (T083 audit, systemic issue 4; lead 2026-11-24) — pending owner
D-026 was applied inconsistently. Rule: a GWh figure for an integrated line that makes cells and assembles them into
modules/packs at the same site (电芯、模组和PACK; "cells, modules and packs") counts as CELL capacity — the GWh is
the cell throughput. D-026 (nameplate null) applies only when the figure adds different products (storage
systems/containers, power stations, equipment, materials) or when it is unclear that the site makes cells at all
(Geely Ganzhou: electrive says it is unclear whether Geely makes cells there → stays null).

## D-032 — Reference-year basis read from the latest statement; partial dating gets no full credit (T083 audit)
Series D credits a plant's full nameplate from capacity_ref_year only when the LAST reference-year statement in its
notes is neither "fallback" nor D-021 "latest dated phase; remainder undated". Otherwise D credits dated
capacity_by_year_json steps only (D-high still credits the full plan). Construction-complete (建设完成/厂房已完成),
IPO use-of-proceeds deadlines and construction-tracker completion estimates are not phase years.
Effect: D 2023/2024/2025 = 1,647 / 2,018 / 3,349 GWh (was 1,732 / 2,172 / 3,429).

## D-033 — Series F: modelled history backfill, labelled estimate (owner 2026-11-24: "really fix history")
For operational active plants with a known start_year whose sourced series (D) is zero before its first sourced
figure, years from start_year to that figure are filled with a linear ramp to the first sourced value. Company cap:
the modelled part of a company's sites may not push the company above its smallest disclosed total from that year
onward (capacity grows). Unallocated company capacity is recomputed against D + modelled. F = D + modelled +
unallocated. Stored separately (capacity_history_model, capacity_by_year_f.csv); never written into plant rows.
Also fixed (sourced series): rows now start at the online year (start_year or first sourced step) so dated pre-anchor
steps count, and plants with an installed anchor are never filled with full nameplate before that anchor.
Known remaining bias: plants that produced in 2016–2022 and later closed are largely absent (survivorship) → T095.

## D-034 — Series v3: explicit evidence precedence (T102 audit, 2026-11-24)
scripts/series_core.py replaces the per-plant logic. Precedence: confirmed installed anchor > confirmed v2 steps >
reported anchor/steps > v1 capacity_timeline (reported only, used only when the row has no v2 steps and is not on the
unsupported list). No capacity before an evidenced start_year, or before the first evidence year when start is
unknown; before an installed anchor only dated steps count (never the full plan); reported never overrides
confirmed; operational plants with nothing dated count as online-unquantified (no fill from the plan year); rejected
v1 histories get no nameplate fill. Series A now contains confirmed values only. Effect (D, sourced IEA basis): 2022
1,033→749, 2025 3,418→3,469 GWh; history now sits in the labelled Series F model where it is not sourced.
Series F fixes: company caps interpolated between disclosed years; true start year in the ramp; company-capped model
values flagged (company-level remainder, not plant estimates).

## D-035 — Series v4 (T111 audit, 2026-11-25) — pending owner
A = confirmed INSTALLED anchors only (the installed floor, as documented); dated phase steps move to C. Steps are
confirmed per step (a confirmed quote must contain the value); cumulative sums of quoted phases are "reported_step"
in C. v1 timeline points are rejected one by one (timeline_check NUMBER_MISSING); a row whose v1 history was rejected
is never plan-filled. A later reported v1 point may raise C (never A). B = A, else C when dated data exist, else the
nameplate fill (B now ≈ C; D-high is the upper bound). D's full-plan credit is withheld while a later confirmed installed
anchor is below the plan. Pipeline = target above C, 0 for inactive projects. Company maps carry valid_to (CALB
Luoyang 2021); unallocated subtracts paused rows too. Effect 2025: A 1,197 · C 3,342 · D 3,442 · D-high 4,332 · F 3,496.

## D-036 — Owner accepts G4 as a documented limit (owner 2026-11-27)
Owner: "accept g4". The 119 active plants ≥10 GWh below 0.6 confidence stay as they are, each with its reason/ESCALATE
in research_notes; G4 is closed by owner waiver, not by changing confidences. Network (T088): owner allowed the hosts;
from this session dart.fss.or.kr and jintan.gov.cn now respond (200); nrel.gov still refused by the proxy (may need a
new session); iea.org and meti.go.jp return 403 from the sites themselves (bot blocking — not bypassed).

## D-037 — Naming (owner 2026-11-27): "built nameplate" instead of "IEA basis"
Series D is called **built nameplate** (design capacity of built, commissioned lines, utilisation ignored), D-high its
upper bound; C **producing capacity**; A **confirmed installed**; the site field is **planned nameplate**. Export columns
renamed: gwh_built_nameplate(_high), gwh_producing, gwh_confirmed_installed, gwh_upper_fill_B; DB table columns
gwh_built_nameplate / built_basis / gwh_built_nameplate_high. Older log entries keep the old wording.

## D-038 — Output floors and the utilisation view (owner upgrade list, 2026-11-27)
A company's disclosed annual OUTPUT is a lower bound on its capacity. Where a company-year has disclosed output but no
usable disclosed capacity, Series E uses the output as a labelled floor (basis output_floor; flag in
capacity_unallocated). company_utilisation.csv sets disclosed output against disclosed capacity (utilisation) and against
our site-level producing capacity: output above our producing capacity proves missing site capacity (e.g. CATL 2022
output 325 GWh vs our sites 108; Ganfeng 2025 27 vs 10). Korean DART reports give utilisation only (LGES 2023–25:
69.3% / 57.8% / 47.6%), capacity in KRW.

## D-101 (2026-11-27, lead) Supply-chain phase: separate asset database
Supply-chain assets live in `supply_chain.db` / `sc_assets.csv`, built from `data/supply_chain/patches/` by
`scripts/sc_build.py`, checked by `checks/sc_checks.py` (spec: team/SPEC_SUPPLY_CHAIN.md). Regions use 11 values
suited to mining (Australia & Oceania, South America, Africa, …) instead of the 8 cell regions.
## D-102 (2026-11-27, lead) Unit normalisation
Capacity/production are recorded as stated; normalised values use data/supply_chain/units.csv (LiOH·H2O ×0.880 → LCE,
SC6 ×0.148 → LCE, NiSO4·6H2O ×0.2233 → Ni, CoSO4·7H2O ×0.2097 → Co). Concentrates of unstated grade are not normalised.
USGS lithium production is in t Li content (×5.323 → LCE).
## D-103 (2026-11-27, lead) Brine operations
A salar/salt-lake operation producing carbonate or chloride on site is one `mining` row (product = the chemical);
a separate downstream plant (e.g. off-salar carbonate/hydroxide plant) is a `refining` row. Refining comparisons count
both.
