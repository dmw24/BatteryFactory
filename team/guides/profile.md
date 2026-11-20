# Profile: dataset

For objectives whose main deliverable is a dataset: harmonising sources, building panels, estimating missing values, modelled or derived series.

## Defaults

- **Integration:** `merge` unless the team wants PR review history; data diffs in PRs are rarely read.
- **Boundaries:** one folder per source or per slice (`data/build/<slice>/`), plus pipeline code per stage. Raw downloads are write-once.
- **Contracts:** schema, units, keys and classifications (country codes, product lists, years), file layout and intermediate formats. Settle these before anything else.
- **Typical workstreams:** by pipeline stage (ingest, harmonise, estimate, validate) or by method; tasks by slice (region, sector, product).
- **Provenance:** every external parameter or value carries a source ID from `team/evidence/`. Add `team/scripts/check_provenance.py` to `check_command`.

## Task shapes

- Ingest one source: download, store raw with a manifest entry (URL, date, licence, checksum), parse to the intermediate format
- Harmonise one source to the shared schema and classifications
- Estimate or model one slice with a documented method
- Fill gaps for one slice, flagging every imputed value
- Reconcile: compare overlapping sources and record differences
- Validation task: benchmark reproduction for reference cases

## Default checks (`check_command`)

1. **Schema:** columns, types, units, allowed codes; no duplicate keys
2. **Coverage:** every required key (entity × period × variable) present or explicitly flagged missing
3. **Bounds and invariants:** non-negative where required, shares sum to 1, physical or logical limits, plausible growth rates
4. **Balances:** totals reconcile across levels (components sum to totals within tolerance)
5. **Benchmarks:** reproduces independent published figures for reference cases within stated tolerance
6. **Provenance:** every parameter has a source ID that resolves; every imputed value is flagged with its method
7. **Reproducibility:** pipeline rebuilds outputs from raw data with one command

## Audit probes

- Units and magnitudes: kilo vs mega, per-capita vs total, calendar vs fiscal year, nominal vs real
- Double counting across categories; inconsistent boundaries between sources
- Silent gap-filling: interpolated or carried-forward values not flagged
- Breaks in series where sources change; jumps that coincide with method switches
- Parameters copied from a source with a different scope (region, year, technology) without saying so
- Sample N values and re-derive each from raw data and cited sources by hand
- Results that are smoother or tidier than the underlying sources justify

## Worked example

**Objective:** a harmonised country-year dataset of installed renewable capacity by technology, 2000–2025, combining three public sources, with documented gap-filling.

**SPEC excerpt**
- In: all countries with a standard code; solar, wind, hydro, bioenergy, other; annual values; source and method flag per value.
- Out: sub-national data; monthly data; forecasts.
- Workstreams: ingest (one task per source), harmonise, gap-fill by region, validation.
- Licences: sources A and B allow redistribution; source C allows derived values only – store C's raw data outside the repo.

**ACCEPTANCE excerpt**

| ID | Check | How | Threshold |
|---|---|---|---|
| C1 | Schema valid | `python checks/schema.py` | exit 0 |
| C2 | Coverage | `python checks/coverage.py` | every country × year × tech present or flagged |
| C3 | Technologies sum to total | `python checks/balance.py` | within 0.5% for every country-year |
| C4 | Benchmarks | `python checks/benchmarks.py` | 10 reference countries within ±3% of source A totals |
| C5 | Provenance | `python team/scripts/check_provenance.py` | no unresolved source IDs |
| R1 | Gap-filling is defensible | auditor reviews method notes per region | each method justified, imputed share reported |

**Backlog**

| ID | Task | Files | Depends | Risk |
|---|---|---|---|---|
| T001 | Schema, codes, units and intermediate format (contract) | `schema/**`, `checks/schema.py` | – | high |
| T002 | Ingest source A + manifest | `data/raw/A/**`, `pipeline/ingest_a.py` | T001 | normal |
| T003 | Ingest source B + manifest | `data/raw/B/**`, `pipeline/ingest_b.py` | T001 | normal |
| T004 | Thin slice: harmonise A and B for 5 countries end to end | `pipeline/harmonise.py`, `data/build/pilot/**` | T002, T003 | high |
| T005 | Gap-fill method and Europe slice | `pipeline/gapfill.py`, `data/build/europe/**` | T004 | high |
| T006 | Gap-fill Asia slice | `data/build/asia/**` | T005 | normal |

**Sample audit verdict**

```
VERDICT: fail
TASK: T005
FAILURE TYPE: diligence
CRITERIA: C1 PASS · C2 PASS · C3 FAIL (3 country-years > 0.5%) · C4 PASS · C5 PASS · R1 FAIL (series break unflagged)
CHECKS RE-RUN: checks/* → C3 fails for 3 country-years
FINDINGS:
  1. [blocking] Linear interpolation across a source switch in 2011 for 4 countries creates a false trend – data/build/europe/wind.csv rows 212–219 – break the series at the switch and flag
  2. [blocking] 2024 values carried forward from 2023 without an imputation flag – pipeline/gapfill.py:88
  3. [minor] Method note doesn't state the imputed share per country
SAMPLED FROM SOURCE: 15 checked, 13 confirmed, 2 mismatches (both carried-forward values above)
ASSUMPTIONS REVIEWED: A-012 (hydro includes pumped storage) – consequential for totals; should have been escalated
NOT CHECKED: source C values (raw data not in repo by licence)
```

