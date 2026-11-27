# Data dictionary — open battery cell gigafactory database (v2)

Rebuild everything with `python3 scripts/build_all.py`. Rules and definitions: `docs/METHODS.md`; decisions: `team/DECISIONS.md`.

## factories_export.csv — one row per physical cell-manufacturing site
| column | meaning |
|---|---|
| `id` | stable slug `<operator>-<plant>-<country>` |
| `plant_name`, `operator`, `parent_company`, `jv_partners` | site name; entity running it; ultimate owner; JV partners (one row per site, never per partner) |
| `country`, `region` | country; one of China, USA, Europe, South Korea, Japan, India, Southeast Asia, Rest of World |
| `latitude`, `longitude`, `geo_precision` | coordinates; precision `site` / `town` / `city` (most are town or city approximations; OSM-derived ones credited in notes) |
| `status` | furthest stage reached: `announced` / `under_construction` (site works confirmed) / `operational` (commercial cell production). Never sum across statuses. |
| `project_state` | `active` / `paused` (idle, halted) / `cancelled`. Aggregates use active rows (`factories_active` view). |
| `announced_year`, `start_year` | year announced; first year of commercial cell production |
| `nameplate_capacity_gwh`, `capacity_ref_year` | **planned nameplate**: the site's full current plan, GWh/yr; year the last included phase is due (notes say if it is a publication-year fallback or only the latest dated phase) |
| `installed_capacity_gwh`, `installed_as_of` | capacity of lines built **and producing** at that date (confirmed installed) |
| `capacity_by_year_json` | dated cumulative capacity steps, e.g. `{"2021": 8, "2023": 24}` — sourced, never interpolated |
| `chemistry`, `cell_format`, `end_market` | LFP / NMC / … / mixed; prismatic / cylindrical / pouch / mixed; EV / ESS / consumer / mixed |
| `is_cell_manufacturer`, `site_type` | cell plant flag; `single_site` or `hub` (several adjacent plants reported together) |
| `source_url`, `source_date`, `source_published_date` | strongest single source for the row; access date; publication date |
| `confidence` | 0–1 (0.9+ two independent sources; 0.6–0.8 one reputable source; ≤0.5 inferred/dated/conflicting) |
| `evidence_tier`, `reported_fields` | `reported` when status or capacity rests on an unconfirmed (v1/snippet) source; list of such fields |
| `last_verified`, `verified_by_task` | v2 re-verification stamp |
| `research_notes` | what was found, conflicts, ESCALATE lines, `[GEO=…]` coordinate notes |
| `capacity_timeline`, `is_single_site` | legacy v1 fields (history used only as *reported*, point by point) |

## data/field_evidence.csv — field-level provenance
`id, field, task, source_id, url, publisher, published, accessed, language, quote, tier` — every status/capacity value
has at least one row with a verbatim quote (≤300 chars, original language), or `tier = reported`.

## capacity_by_year.csv — global series by year (GWh/yr; active comparable plants)
| column | series |
|---|---|
| `gwh_confirmed_installed` | A — confirmed installed capacity only (floor) |
| `gwh_producing` | C — best estimate of capacity actually producing |
| `gwh_built_nameplate` | D — design capacity of built, commissioned lines (the IEA/BNEF basis) |
| `gwh_built_nameplate_high` | D-high — also counts plan phases whose completion year is unknown (upper bound) |
| `gwh_upper_fill_B` | B — legacy upper fill (≈ C under the v4 rules) |
| `gwh_pipeline_additional` | planned target above producing capacity (active projects) |
| `gwh_online_china` | A for China |
`capacity_by_year_region.csv` — the same by plant region.

## capacity_by_year_e.csv / capacity_by_year_f.csv
E = built nameplate + **unallocated** company capacity (a company's disclosed total — or disclosed output as a floor —
minus its sites; no location); Ah-converted estimates in a separate column. F = E + **modelled history** (linear ramp from
a plant's start year to its first sourced figure, capped by company disclosures) — a labelled estimate.

## capacity_unallocated.csv
`company, year, disclosed_gwh, sites_gwh, unallocated_gwh, region, scope, basis, flag, source_url, quote` — flags:
`estimate` (Ah conversion), `output_floor`, `sites_exceed_disclosed`.

## company_utilisation.csv, capacity_by_hq.csv
Disclosed output vs capacity per company-year; capacity by cell maker's headquarters × plant region.

## Reference files
`data/reference/company_capacity/*.csv` (disclosed company capacity/output with quotes), `company_map.csv`
(site → company, `valid_to` when ownership ended), `operator_totals.csv`, `non_comparable.csv` (excluded chemistries),
`benchmarks/` and `scripts/benchmarks.csv` (IEA/BNEF/Benchmark — comparison only, not data), `team/evidence/miit/`
(official MIIT lists), `team/evidence/filings/MANIFEST.csv` (company filings used).

# Supply-chain asset database (sc_assets.csv / supply_chain.db table `assets`)
Rebuild: `python3 scripts/sc_build_all.py`. Methods: docs/SUPPLY_CHAIN_METHODS.md.
| column | meaning |
|---|---|
| `id`, `asset_name`, `part_of` | slug `<operator>-<asset>-<country>`; site/asset name; site id when the row is a project at that site (D-107) |
| `step`, `commodity`, `product`, `asset_type`, `feedstock`, `chemistry` | mining / refining / precursor / cathode / anode / electrolyte / separator / foil / recycling; lithium, nickel, cobalt, graphite, manganese, cathode, … |
| `operator`, `parent_company`, `jv_partners`, `ownership_json` | operator, group, JV partners (one row per asset) |
| `country`, `region`, `province_state`, `latitude`, `longitude`, `geo_precision` | 11 regions (D-101); coordinates with precision site/town/city |
| `status`, `project_state`, `announced_year`, `start_year` | as in the cell database |
| `capacity`, `capacity_unit`, `capacity_ref_year`, `capacity_norm`, `norm_unit` | full plan as reported + normalised value (units.csv) |
| `installed_capacity`, `installed_as_of`, `installed_norm`, `capacity_by_year_json` | built and running; dated steps |
| `production`, `production_unit`, `production_year`, `production_norm`, `production_norm_unit` | latest annual output |
| `reserves_resources`, `feeds`, `offtakers`, `end_market` | context; `feeds` = ids this asset supplies when sourced |
| `source_url`, `source_date`, `source_published_date`, `confidence`, `evidence_tier`, `reported_fields`, `research_notes` | as in the cell database |
Other files: `data/supply_chain/field_evidence.csv` (quotes), `company_totals.csv` (company-level disclosures, `geo_scope`),
`sc_company_coverage.csv` (company totals vs sites), `sc_benchmark.csv` (comparisons), `data/supply_chain/benchmarks/aggregates.csv`
(benchmarks with URL and quote), `team/RECONCILIATION_SC.md`, charts/sc_asset_map.png, charts/sc_coverage.png.
