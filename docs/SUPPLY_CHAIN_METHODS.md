# Methods — open battery supply-chain asset database

Companion to the cell gigafactory database (docs/METHODS.md). Spec: team/SPEC_SUPPLY_CHAIN.md; decisions D-101–D-113
in team/DECISIONS.md; coverage and caveats in team/RECONCILIATION_SC.md (regenerated).

## What is in it
One row per physical asset for every step of the lithium-ion supply chain outside cells: mining (lithium, nickel,
cobalt, graphite, manganese), refining (lithium chemicals, nickel/cobalt intermediates and refined products, manganese
sulphate, spherical graphite), precursor (pCAM, iron phosphate), cathode, anode, electrolyte and LiPF6, separator,
copper foil, recycling. Status `operational` / `under_construction` / `announced`, project_state `active` / `paused` /
`cancelled`; never summed across statuses.

## Evidence
Every status, capacity, installed, production and phase value cites a source with a verbatim quote (≤300 chars,
original language) in `data/supply_chain/field_evidence.csv`; search-snippet-only values are tier `reported` and cap the
row at confidence 0.5. Quotes are re-checked by `checks/verify_quotes.py --sc`; unmatched quotes are demoted to reported.
Sources, in order of use: company annual reports (≈80 Chinese 2025 reports fetched from cninfo as text, plus 10-K/20-F,
ASX, HKEX, TSX filings), official lists (China MIIT 锂离子电池行业规范条件 lists, state/provincial pages), open datasets
(CGS Nickel Smelter Dataset, CC BY 4.0), and open press. Paywalled report bodies are never evidence.

## Units
Values are stored as reported (`capacity_unit`, `production_unit`) and normalised with `data/supply_chain/units.csv`
(D-102): lithium to t LCE (LiOH·H2O ×0.880, Li2SO4 ×0.672, SC6 ×0.148, Li ×5.323), nickel to t Ni (NiSO4·6H2O ×0.2233),
cobalt to t Co, manganese to t Mn. Concentrates of unstated grade are not normalised; grade assumptions are written in
the row notes (D-104). Brine operations that make carbonate on site are one mining row (D-103).

## Capacity concepts
`capacity` = full current plan for the asset with `capacity_ref_year`; `installed_capacity` = built and running at
`installed_as_of`; `capacity_by_year_json` = dated sourced steps; `production` = latest reported annual output. Project
rows at a site whose base capacity is undisclosed carry `part_of` (D-107). Company totals disclosed only at group level are
kept in `data/supply_chain/company_totals.csv` and shown as *unallocated* company capacity/output (no location), with
`geo_scope` china/global so China benchmarks are not inflated by overseas plants.

## Benchmarks (comparison only)
USGS Mineral Commodity Summaries 2026 (mine production by country), MIIT and industry statistics via open press (China
output of cathode, anode, separator, electrolyte, lithium chemicals), Cobalt Institute, INSG, ICC/EVTank/GGII figures
quoted in filings, Mysteel and Fraunhofer ISI (recycling). `scripts/sc_benchmark.py` compares like with like: mining =
reported output; processing = built capacity (installed, or plan whose reference year has passed), with unbuilt phases
and nickel intermediates shown separately.

## Rebuild and checks
`python3 scripts/sc_build_all.py` (build → company coverage → benchmarks → report → charts); `python3 checks/sc_checks.py`
(14 checks); `python3 checks/verify_quotes.py --sc --task SCxxx`.

## Known limitations
- Most Chinese processing companies disclose company totals, not plant capacity: site-level capacity understates China,
  company-level figures close much of the gap but have no location.
- Mine output is missing where operators publish none (Zimbabwe lithium, many Chinese lepidolite and graphite mines,
  Philippine/Indonesian nickel ore grades).
- Coordinates: ~half of assets, mostly city-level approximations (D-108).
- Benchmarks are themselves estimates with differing scopes (capacity vs output vs shipments; years).

## Capacity by year (sc_capacity_by_year.csv, scripts/sc_timeseries.py)
Built capacity per step/commodity/unit by year from sourced dated steps, installed dates and dated plan years; under
construction and announced projects from their reference year, kept as separate columns (never added to built).
History before ~2022 is thin because few assets disclose start years or dated phases; treat it as a floor.
