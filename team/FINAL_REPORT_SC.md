# Battery supply-chain asset database — status report (2026-11-27, lead)

Owner request: "the supply chain in full … asset level overview like we now have for battery factories … well
benchmarked". Spec team/SPEC_SUPPLY_CHAIN.md; methods docs/SUPPLY_CHAIN_METHODS.md; coverage team/RECONCILIATION_SC.md.

## What exists
- **901 assets** (809 active): mining 212, refining 278, precursor 23, cathode 137, anode 68, electrolyte/LiPF6 54,
  separator 45, copper foil 29, recycling 55 — lithium, nickel, cobalt, graphite, manganese and all battery materials.
- **2,600 evidence links** (url + verbatim quote); 755 rows confirmed tier, the rest reported-tier and capped at 0.5.
  Every merged task's quotes re-checked by `checks/verify_quotes.py --sc` (filing passes: ~100% found).
- 498 assets with coordinates (site/town/city precision flagged); 25 sourced supply links (mine → refinery → pCAM →
  CAM → cell plant, incl. cell-plant ids from the cell database); 92 company-level disclosures (company_totals.csv).
- Benchmarks with provenance: USGS MCS 2026 (Li, Ni, Co, graphite, Mn by country), MIIT/industry China output,
  Cobalt Institute, INSG, ICC, Mysteel/Fraunhofer (recycling).
- Outputs: sc_assets.csv / supply_chain.db, sc_benchmark.csv, sc_company_coverage.csv, sc_capacity_by_year.csv,
  charts/sc_asset_map.png, charts/sc_coverage.png. Rebuild: `python3 scripts/sc_build_all.py`; checks: 14/14 pass.

## How good is it (vs open benchmarks)
- Lithium mine output: ~81% of USGS world 2025 (Chile/Mali/Argentina/Canada ≥80%; China ~47%, Zimbabwe 0% — operators
  publish no mine-level output).
- Cobalt mine output: ~53% incl. CMOC's group total; nickel mines: Canada 86%, Brazil ~94%, US ~99%; Indonesia via
  smelters (CGS dataset + filings). Graphite: ex-China partly, China mines largely undisclosed.
- China processing (2025): companies whose annual reports were read produce roughly half of China's cathode and anode
  output and less for lithium chemicals; "built" plant capacity is a confirmed-date floor (installed/dated only).

## Quality process
Three independent Opus audits (AUDIT_LOG: SC audit 1–3). All found no fabricated quotes; each FAIL was on comparability
or rule application, fixed as rules (scripts/sc_core.py: one "built" definition; intermediates separate; D-101–D-111).

## Known limits / next
Plant-level capacity for many Chinese bases (companies disclose totals only); Zimbabwe and Chinese lepidolite/graphite
mine output; Indonesian cobalt in MHP; more supply links; HPMSA plants. See team/SC_BACKLOG.md.
