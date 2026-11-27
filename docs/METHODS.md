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

## Naming (owner, 2026-11-27)
**Planned nameplate** = a site's full plan (`nameplate_capacity_gwh`). **Built nameplate** = design capacity of lines already built and commissioned, regardless of how much they run (the basis IEA/BNEF use; Series D). **Producing capacity** = lines confirmed built and running (Series C). **Actual output** = cells produced (not in the database). Export columns: `gwh_confirmed_installed` (A), `gwh_producing` (C), `gwh_built_nameplate` / `_high` (D / D-high).

## Five capacity series (`capacity_by_year`, `capacity_by_year_e.csv`)
| series | meaning | use |
|---|---|---|
| A | confirmed installed anchors only (D-035) | floor |
| C | best estimate of capacity actually producing | "how much is running" |
| D | built nameplate: design capacity of commissioned lines (dated phases only) | compare with IEA/BNEF |
| D-high | D plus plans whose completion year is undated | upper bound of D |
| E | D plus *unallocated* company capacity: a company's disclosed total minus its sites in the database (no location) | closest sourced figure to IEA/BNEF |
| F | E plus a modelled history backfill (linear ramp from a plant's start year to its first sourced figure, capped by company disclosures) | labelled estimate for history |
Ah-converted company figures (Great Power, D-030) are labelled estimates and reported separately from E.
Rules: never sum across statuses; aggregates use `factories_active` (active, comparable chemistries; D-019).

## How it compares (global, TWh per year)
| year | A | C | D | D-high | E | F (modelled) | IEA | BNEF | Benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2020 | 0.04 | 0.15 | 0.17 | 0.17 | 0.24 | 0.35 | – | – | 0.73 |
| 2022 | 0.15 | 0.74 | 0.77 | 0.93 | 1.07 | 1.21 | ~1.5–1.7 | – | – |
| 2023 | 0.26 | 1.66 | 1.69 | 2.07 | 1.94 | 2.03 | ~2.5 | ~2.6 | – |
| 2024 | 0.40 | 2.05 | 2.09 | 2.68 | 2.47 | 2.51 | 3.0 | 3.1 | – |
| 2025 | 1.20 | 3.34 | 3.44 | 4.33 | 3.50 | 3.50 | >4.0 | – | 4.8 |

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
