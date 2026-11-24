# Licence proposal for the dataset (owner to decide)

Status: **proposal, not yet adopted.** Nothing in the repo is licensed for publication until the owner chooses.

## Recommendation: CC BY 4.0 for the data, MIT for the code
- **Data** (`factories_export.csv`, `data/field_evidence.csv`, `capacity_by_year*.csv`, `capacity_unallocated.csv`):
  Creative Commons Attribution 4.0 — reuse with credit, matching IEA's own licence for its charts (CC BY 4.0) and
  the usual choice for open energy datasets.
- **Code** (`scripts/`, `checks/`): MIT.

## Things to check before publishing
- **Quotes** in `data/field_evidence.csv` are short verbatim excerpts (≤300 characters) of third-party pages,
  included as evidence. Short quotation for verification is normally fine, but they stay the publishers' text.
  Legal or comms should confirm; otherwise publish URLs without quotes.
- **Company filings** text under `team/evidence/filings/` is gitignored and must not be published.
- **Benchmarks** (IEA, BNEF, Benchmark) are cited figures, not our data; keep them out of the licensed files or mark
  them as third-party.
- Alternatives: CC BY-SA 4.0 (share-alike; less reuse-friendly), ODbL (database-oriented, share-alike).
