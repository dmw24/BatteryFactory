# Methods — open battery cell gigafactory database (v2)

Short guide for readers of the data. Decisions are numbered (D-0xx) in `team/DECISIONS.md`.

## What is in it
One row per physical **cell** manufacturing site (packs, modules and materials-only sites excluded), worldwide,
operational / under construction / announced, with project_state active / paused / cancelled. Built only from open
sources anyone can read: company filings and releases, government and environmental-permit notices, and press.
Every capacity and status value links to a source with a verbatim quote (`data/field_evidence.csv`).

## Key fields
- `nameplate_capacity_gwh` — the site's full current plan in GWh per year (built + under construction + every stated
  phase); `capacity_ref_year` — when the last dated phase is due ("fallback" = only a publication year is known).
- `installed_capacity_gwh` + `installed_as_of` — lines built **and producing** at a date.
- `capacity_by_year_json` — dated, sourced phase steps (cumulative GWh), never interpolated.
- `confidence` 0–1; `evidence_tier = reported` when status or capacity rests on an unconfirmed (v1, snippet-only)
  source; such rows are capped at 0.5.

## Five capacity series (`capacity_by_year`, `capacity_by_year_e.csv`)
| series | meaning | use |
|---|---|---|
| A | confirmed producing capacity only | floor |
| C | best estimate of capacity actually producing | "how much is running" |
| D | IEA basis: design capacity of commissioned lines (dated phases only) | compare with IEA/BNEF |
| D-high | D plus plans whose completion year is undated | upper bound of D |
| E | D plus *unallocated* company capacity: a company's disclosed total minus its sites in the database (no location) | closest to IEA/BNEF |
Ah-converted company figures (Great Power, D-030) are labelled estimates and reported separately from E.
Rules: never sum across statuses; aggregates use `factories_active` (active, comparable chemistries; D-019).

## How it compares (global, TWh per year)
| year | C | D | D-high | E | IEA | BNEF | Benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 1.52 | 1.65 | 1.81 | 1.85 | ~2.5 | ~2.6 | – |
| 2024 | 1.94 | 2.02 | 2.54 | 2.37 | 3.0 | 3.1 | – |
| 2025 | 3.11 | 3.35 | 4.10 | 3.40 | >4.0 | – | 4.8 |
Europe and the US match the benchmarks; the gap is China, mostly capacity history at known plants and companies
that disclose no GWh capacity (BYD, CALB, Gotion, EVE, Korean makers). IEA data are based on Benchmark Mineral
Intelligence, so those two are not independent. Provenance of each benchmark: `scripts/benchmarks.csv`.

## Completeness checks done
Two geographic passes (every Chinese province, every region), operator site lists for the top makers, China's
CABIA top-15 and ESS rankings, the official MIIT 锂离子电池行业规范条件 lists (batches 1–9; ~81 cell makers, 68
matched, ~13 tiny makers with no public information), open trackers outside China. See `team/COVERAGE.md`.

## Known limitations
- Chemistry is "mixed" or unknown for much of the capacity: no clean LFP/NMC split from open sources.
- Japan/Korea site capacities are rarely published; some official sources are blocked from the build environment.
- Coordinates are mostly city-level approximations (`geo_precision`), ~100 sites have none.
- About 120 plants ≥10 GWh remain below 0.6 confidence; reasons are in each row's notes.

## Rebuild
`python3 scripts/build_all.py` (rebuild → series → unallocated → QA → report → charts); checks:
`python3 checks/run_all.py`, `python3 checks/verify_quotes.py --task Txxx`.
