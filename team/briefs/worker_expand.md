# Worker brief — find and add missing cell plants (geographic sweep)

You are a research worker on the battery cell gigafactory database v2. Today is 2026-11-20. Goal: **add every battery-cell manufacturing site in your geography that is not yet in the database** — operational, under construction or announced (announced = a dated, site-specific project with a stated capacity; a bare MoU/signing with no site or capacity does not count).

## Read first
1. `team/CONVENTIONS.md` — binding (status D-020, capacity D-014/D-015/D-021, project_state, vocabulary, and **"Confirmed vs reported evidence"**).
2. `team/AUDIT_EXAMPLES.md`.
3. `factories_export.csv` and `data/removed.csv` — before adding anything, Grep operator names (Chinese and English), city and county names. A plant already present (even under another name, or as part of a hub row) must not be added again; mention it in your hand-off instead.
4. Leads already collected: `data/reference/operator_sites/*.csv` rows with an `excluded_reason` like `no_open_source` in your geography (real company sites we never added), and `team/candidate_routing.csv`.

## Ownership
You own **only plants physically located in your geography** (listed in your task prompt). If you find a plant elsewhere, list it in the hand-off; don't add it.

## How to search
- Chinese: by province and prefecture city — e.g. "<省/市> 锂电池 电芯 项目 投产 GWh", "储能电芯 开工 <市>", "钠离子电池 项目 <省>", provincial 重点项目 lists (2024–2026), government news (政府网), 环评/竣工验收 notices, exchange announcements of listed makers; trade press (energytrend, gg-lb.com 高工锂电, sohu/sina/163 finance, bjx, solarbe, cnevpost, SMM).
- Other regions: national/regional press in the local language, government investment-promotion releases, company releases, electrive, ess-news, pv-magazine.
- Company filings already extracted: `team/evidence/filings/*.txt` (Grep for 生产基地/产能/子公司).

## What to write
`data/patches/<TASK>.json` with `add` rows (row-level id `<operator>-<plant>-<country>` slug). Required per add: plant_name, operator, parent_company (if known), country, region, status, project_state, site_type, confidence, notes; status/nameplate/installed/start_year evidence. Capacity in GWh/yr of **cells** (not packs/systems/Ah/MW). Coordinates only if you located the site itself (`[GEO=site:...]` in notes) — otherwise leave null.
Evidence: confirmed preferred; reported allowed (CONVENTIONS). Adds resting on reported evidence: confidence ≤ 0.5.
Do not use Bash. Do not edit any other file.

## Efficiency
Prioritise by size: plants ≥ 5 GWh first, then 1–5 GWh; skip sub-0.5 GWh pilot lines unless notable. Stop a line of search when it only returns plants already in the DB.

## Hand-off
Counts (added by status; confirmed vs reported), the 15 largest adds, plants found that already exist (id), out-of-geography finds, ESCALATE lines.
