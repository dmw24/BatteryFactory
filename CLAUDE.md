# Battery Gigafactory Database

A pipeline that produces a database of the world's battery **cell** manufacturing
plants (gigafactories). The orchestrator (main Claude session) fans work out to
parallel sub-agents; sub-agents do the research; the orchestrator validates and
loads results into DuckDB.

## Scope

- **Cell manufacturing only.** Include plants that manufacture battery *cells*.
  Exclude pure pack-assembly, module, cathode/anode/precursor material, or
  recycling sites unless they also make cells (note mixed sites in `end_market`).
- One row per **physical site**.

## Pipeline

1. **Scaffold** — `scripts/init_db.py` creates `factories.db`.
2. **Seed list** — `list-builder` sub-agents (one per region) return distinct
   plants; merged and deduped into `candidates.csv`.
3. **Research** — `factory-researcher` sub-agents research one plant each;
   the orchestrator (`scripts/orchestrator.py`) validates JSON and loads rows.
4. **QA** — `scripts/qa.py` / `qa_report.md`.

## Schema — `factories` table

| column | type | notes |
|---|---|---|
| `id` | VARCHAR PK | stable slug `<operator>-<plant>-<country>`, lowercase, hyphenated |
| `plant_name` | VARCHAR | site name (required) |
| `operator` | VARCHAR | entity running the site |
| `parent_company` | VARCHAR | ultimate owner / group |
| `country` | VARCHAR | |
| `region` | VARCHAR | one of the eight regions below |
| `latitude` | DOUBLE | decimal degrees |
| `longitude` | DOUBLE | decimal degrees |
| `status` | VARCHAR | `announced` \| `under_construction` \| `operational` |
| `announced_year` | INTEGER | |
| `start_year` | INTEGER | first production year |
| `nameplate_capacity_gwh` | DOUBLE | annual GWh/**year** at full nameplate |
| `capacity_ref_year` | INTEGER | the year `nameplate_capacity_gwh` refers to |
| `capacity_by_year_json` | VARCHAR | JSON map `{"2024":10,"2025":20}` GWh/yr, phased ramp |
| `chemistry` | VARCHAR | LFP, NMC, NCA, sodium-ion, solid-state, mixed … |
| `cell_format` | VARCHAR | `prismatic` \| `cylindrical` \| `pouch` \| `mixed` |
| `end_market` | VARCHAR | `EV` \| `ESS` \| `consumer` \| `mixed` |
| `jv_partners` | VARCHAR | comma-separated partners if a JV |
| `source_url` | VARCHAR | primary source (required) |
| `source_date` | VARCHAR | ISO date published/accessed (required) |
| `confidence` | DOUBLE | 0–1 |

**Regions** (exactly these eight): `China`, `USA`, `Europe`, `South Korea`,
`Japan`, `India`, `Southeast Asia`, `Rest of World`.

## NON-NEGOTIABLE RULES

1. **Status is one of `announced` | `under_construction` | `operational`.**
   NEVER sum capacity across different statuses. Any aggregate must be grouped
   by status.
2. **`nameplate_capacity_gwh` is annual GWh/year.** Always record the year it
   refers to in `capacity_ref_year`. Do not mix cumulative and annual figures.
3. **Do NOT double-count JV plants under both partners.** One row per physical
   site. If it is a JV, list partners in `jv_partners` and pick a single
   `operator` — do not create a second row for the other partner.
4. **Report phased ramp-ups in `capacity_by_year_json`, not as day-one
   capacity.** `nameplate_capacity_gwh` is the full nameplate; the JSON shows how
   it ramps year by year.
5. **Every row needs a real `source_url` and `source_date`.** If a value is not
   confirmed by a source, leave it `null` and lower `confidence`. Never invent a
   figure, coordinate, or date. A guessed value is worse than a null.

## Confidence guidance

- `0.9–1.0` — value confirmed by company/official or multiple reputable sources.
- `0.6–0.8` — single reputable tracker/news source, plausible and specific.
- `0.3–0.5` — inferred, dated, or conflicting sources.
- `< 0.3` — weak/speculative; most fields null.

## Files

- `factories.db` — the DuckDB database (gitignored; rebuildable).
- `candidates.csv` — seed list of plants (Step 2 output).
- `scripts/init_db.py` — create the DB.
- `scripts/orchestrator.py` — validate researcher JSON and load rows.
- `data/researched/*.json` — raw per-plant researcher outputs.
- `failures.csv` — plants that failed validation, with reason.
- `qa_report.md` — Step 4 quality report.
