# Definition of done

`check_command` = `python3 checks/run_all.py` must exit 0 after every merge (integrity).
The project is done when, in addition, `python3 checks/done_gates.py` exits 0 and the rubric passes at close-out.

## Automated checks — integrity (`checks/run_all.py`, every merge)

| ID | Check | Threshold |
|---|---|---|
| C0 | Rebuild from baseline + patches succeeds | exit 0 |
| C1 | Schema: unique ids, required fields, allowed region/status/project_state/site_type, coordinate & confidence bounds | 0 problems |
| C2 | Controlled vocab (chemistry, cell_format, end_market) and site_type on verified rows | 0 problems |
| C3 | Invariants on verified rows: installed ≤ nameplate; no installed on announced; operational start_year ≤ 2026; announced_year ≤ start_year; nameplate has capacity_ref_year; ramp ≤ nameplate; single site ≤ 1000 GWh | 0 violations |
| C4 | Field provenance on verified rows: every non-null status / nameplate / installed / start_year (and non-active project_state) has ≥1 evidence item with url + verbatim quote + accessed date; confidence ≥ 0.9 needs ≥ 2 domains | 0 gaps |
| C5 | Open data: no hard-paywall domain in evidence or on verified rows | 0 |
| C6 | Duplicate sites (same name, or same operator + same coordinates) | WARN; auditor reviews |

## Done gates (`checks/done_gates.py`)

| ID | Gate | Threshold |
|---|---|---|
| G1a | Every active plant in the top 90% of nameplate re-verified | 100% |
| G1b | Active rows re-verified | ≥ 90% |
| G2a | Σ installed_capacity_gwh, operational active rows (end-2025/now) | 3,200–5,000 GWh/yr (IEA 2025 >4 TWh nameplate) |
| G2b | China share of installed | 75–90% (IEA >80%) |
| G3 | Operator site lists for ≥ 15 largest operators; every listed site matched to an id or excluded with reason | 0 open |
| G4 | Active plants ≥ 10 GWh/yr with confidence < 0.6 | 0 |
| G5 | Active rows still carrying v1 "research blocked" notes | 0 |

## Rubric (auditor)

| ID | Criterion | Pass means | Threshold | Fail examples |
|---|---|---|---|---|
| R1 | Values match sources | Sampled quotes appear on the cited page (`checks/verify_quotes.py` + manual WebFetch) and support the value | ≥ 90% of sampled sources FOUND or hand-confirmed; 0 values contradicted by their own quote | quote says "规划 40GWh" (planned) but stored as installed |
| R2 | Installed vs nameplate separated | installed reflects commissioned lines at a date; nameplate is the full plan | every sampled plant | 2030 target stored as installed |
| R3 | No double counting | hub rows and component rows not both carrying capacity; JV recorded once | 0 instances | CATL Ningde hub 330 incl. Fuding + Fuding row 120 |
| R4 | Status current | latest evidence for active non-operational rows dated ≥ 2025-06; cancellations/pauses reflected | every sampled row | Britishvolt still "under_construction" |
| R5 | Open source | every cited page readable without subscription | 0 paywalled | Bloomberg article cited |
| R6 | Nulls honest | unconfirmed values are null with lowered confidence, not carried silently from v1 | 0 unsupported carried values in sample | v1 capacity kept with no evidence |

## Provenance
Field-level, stored in `data/field_evidence.csv` (from patch files). The auditor samples ≥ 15 sources per audited task.

## Benchmarks
`scripts/benchmarks.csv` (IEA 2021–2025, BNEF 2023). Overlay only; never a row source.

## Out of scope for "done"
Exact site coordinates for the long tail; capacity timelines for every plant (timelines refreshed only for re-verified majors); utilisation/production volumes.
