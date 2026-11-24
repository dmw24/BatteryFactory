# Reconciliation with the IEA — 2025 cell manufacturing capacity

Date: 2026-11-20. Basis: active, comparable cell plants (`factories_active`), `capacity_by_year` for 2025.
External benchmark: IEA Global EV Outlook 2026, ">4 TWh" commissioned nameplate in 2025 (`scripts/benchmarks.csv`).

## Headline
| series | 2025 GWh | share of IEA (~4,000) |
|---|---:|---:|
| A — confirmed installed (floor) | 2,468 | 62% |
| C — best estimate (confirmed, else reported history, else nameplate) | 3,094 | 77% |
| B — upper fill (A + full nameplate where installed unknown) | 3,435 | 86% |

C by basis: confirmed 2,468 · reported v1 history 465 · nameplate fill 160 GWh.
C by region: China 2,342 · USA 289 · Europe 275 · Southeast Asia 69 · Rest of World 53 · South Korea 49 · Japan 16 · India 3.
(Region values are capacity physically located there, so Korean firms' US/European plants count under USA/Europe.)

## IEA-like definition (Series D, D-027)
Design nameplate of commissioned lines, ignoring utilisation — the IEA basis.

| year | C producing | D IEA-like | D-high | IEA |
|---|---:|---:|---:|---:|
| 2023 | 1,514 | 1,585 | 1,726 | 2,500 |
| 2024 | 1,929 | 2,051 | 2,507 | >3,000 |
| 2025 | 3,094 | 3,352 | 4,029 | >4,000 |

D-high credits full plans whose completion year is undated (ref year = source publication year), so it is an upper
bound and is inflated in 2025, when many such sources were published. The consistent ~25–35% shortfall in 2023–24
suggests real missing capacity, mostly in China. Checks since (T062–T073, 2026-11-23): second geographic passes in
every Chinese province and region, the CABIA top-15 installers, MIIT 规范条件 lists (55/83 cell makers matched; the
28 unmatched are small consumer/e-bike makers), open non-China trackers (~60 sites, 3 small adds) and a history fill
for the 26 largest plants lacking a start year (histories confirmed, totals unchanged). ~45 plants were added, almost
all announced/under construction or <15 GWh. Conclusion: the remaining 2023–24 shortfall is mainly undisclosed
capacity at plants we already list (76 operational plants have no capacity figure; many large Chinese bases disclose
only current, not historical, capacity), not missing plants. Official lists that would close it (miit.gov.cn,
nrel.gov, METI) are unreachable from this environment.

## Producing vs commissioned: why C sits below the IEA
1. **Our series measure lines producing; the IEA credits full nameplate of every commissioned line.**
   Global cell output in 2025 was ~2.15 TWh — about 50–55% of the IEA's capacity figure. Our installed
   figures are usually the operator's effective capacity, which sits between the two.
2. **Company cross-checks show we are at or above each company's real output.** Output is a lower bound
   on capacity, so these do not prove over-counting, but they show the gap is not in these companies:

| company | disclosed 2025 figure (open source) | our C 2025 |
|---|---|---:|
| CATL | 772 GWh capacity (annual report) | 835 |
| BYD / FinDreams | ~285 GWh installations (reported) + >60 GWh ESS system shipments (annual report) | 366 |
| CALB | ~116 GWh shipments (press citing annual report) | 185 |
| EVE | 121 GWh output | 189 |
| Gotion | 53.5 GWh EV installations + >30 GWh ESS shipments | 142 |
| Sunwoda | 43 GWh output | 112 |
| SVOLT | 41 GWh shipments | 105 |

   Sources and quotes: `data/reference/operator_totals.csv`; per-operator gaps: `data/reference/operator_gap.csv`.
3. **Where real coverage gaps remain:** operators that disclose capacity above our site sum (REPT +48 GWh,
   Ganfeng +30, Great Power +17) and long-tail Chinese makers without open site-level figures. Together
   these are likely in the low hundreds of GWh, not ~900.

## How to quote these numbers
- Quote **C (~3.1 TWh)** as the bottom-up best estimate and **A (~2.5 TWh)** as the confirmed floor.
- Do not present A or C as like-for-like with the IEA without the caveat above.
- Never sum across statuses; pipeline (under construction / announced) is reported separately.

## Open items affecting these totals
See `team/ESCALATIONS.md`: Lishen Qingdao corrected 40→10 GWh (T060); SVOLT Ma'anshan format corrected to
cylindrical, its 28 GWh plan still unconfirmed; CALB Jintan 70 GWh confirmed as a six-phase plan; low-confidence BYD rows remain. These corrections did not change
the 2025 totals (affected rows were already counted at their confirmed installed figures).

## Series E — IEA-like plus unallocated company capacity (D-028, 2026-11-23)
Company-disclosed total capacity minus the Series D sum of that company's mapped sites (JV sites included), floored at
0, as company/year lines with no location (`capacity_unallocated.csv`). Usable disclosures: CATL 2020–2025 (annual
report 产能 table, 电池系统), Narada 2022–2025, REPT 2024–2025, Hithium 2024, Zenergy 2025, SVOLT 2020–2022.
EVE, Great Power and Sunwoda disclose capacity only in cells or Ah (not converted); BYD, CALB, Gotion (one unclear
prose figure), LGES, Samsung SDI, SK On and Panasonic disclose no company-wide GWh capacity.

| year | D IEA-like | unallocated | E | IEA | E/IEA |
|---|---:|---:|---:|---:|---:|
| 2021 | 472 | 49 | 521 | 1,140 (derived) | 46% |
| 2022 | 1,033 | 131 | 1,164 | 1,720 (derived) | 68% |
| 2023 | 1,599 | 259 | 1,858 | 2,500 | 74% |
| 2024 | 2,078 | 348 | 2,426 | >3,000 | ≤81% |
| 2025 | 3,383 | 54 | 3,437 | >4,000 | ≤86% |

Reading: almost all of the unallocated capacity is CATL in 2020–2024 (its disclosed capacity exceeds our dated site
history; in 2025 our CATL sites, 875 GWh on the IEA basis, exceed its disclosed 772 GWh effective capacity). That
confirms the 2021–24 shortfall is largely missing *history* at known sites, not missing plants. The rest of the gap is
companies that disclose no GWh capacity (BYD, CALB, Gotion, EVE, Korean/Japanese makers).

## Benchmarks beyond IEA (T079, D-029; quotes re-fetched and string-matched by the lead 2026-11-23)
Global capacity (GWh):

| year | ours C | ours D | ours D-high | ours E | IEA | BNEF | Benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2020 | 193 | 235 | 241 | 299 | – | – | 734 |
| 2023 | 1,516 | 1,599 | 1,751 | 1,858 | 2,500 | ~2,600 | – |
| 2024 | 1,943 | 2,078 | 2,543 | 2,426 | 3,000 | 3,100 (fully commissioned) | – |
| 2025 | 3,113 | 3,383 | 4,070 | 3,437 | >4,000 | – | 4,800 (output 2,200) |

By region:

| year | region | ours C / D / D-high / E | benchmark |
|---|---|---|---|
| 2023 | China | 1,202 / 1,268 / 1,414 / 1,527 | BNEF 2,200 nameplate (end-2023) |
| 2024 | China | 1,503 / 1,620 / 2,064 / 1,968 | CRU >2,000 |
| 2024 | USA | 148 / 158 / 178 / 158 | IEA >200 |
| 2025 | Europe | 275 / 282 / 282 / 282 | Bruegel 251; Roland Berger ~200 |

Reading: Europe and the US are at or near the benchmarks (Europe slightly above — we count some ramping plants at
nameplate). The gap is China, and it is largest in the early years (2020: ours ~0.3 TWh vs Benchmark 0.73 TWh;
2023 China: ~1.5 vs BNEF 2.2 TWh), shrinking by 2024–25. That pattern fits missing *history* at Chinese plants we
already list (dated capacity only from recent years) plus non-disclosing companies, rather than missing plants.
Output cross-checks: Benchmark 2025 cell production 2.2 TWh vs capacity 4.8 TWh (≈46% utilisation); our C (3.1 TWh)
sits between output and benchmark capacity. Pipelines (BNEF 7.9 TWh announced for 2025, Benchmark >10 TWh for 2030)
are not capacity. No open source gave an LFP/NMC capacity split.

## Benchmark provenance check (owner question 2026-11-23)
- IEA 2025 ">4 TWh": verified verbatim in the IEA GEVO 2026 PDF (open copy on cleanenergyministerial.org; iea.org itself
  returns 403). IEA states "up roughly 30% compared to 2024", China >80%, EU and US 6–7% each; its data are "IEA
  analysis based on data from Benchmark Mineral Intelligence" — so IEA and Benchmark are not independent checks.
- IEA 2024 "3 TWh" and 2023 "around 2.5 TWh": IEA wording seen via secondary pages/search results (iea.org blocked).
- IEA 2021/2022 (1,140 / 1,720) are NOT IEA figures — lead arithmetic from stated annual additions; approximate.
- BNEF 2023 "close to 2,600 GWh", China 2023 "2.2 TWh" nameplate, 2024 "3.1 TWh fully commissioned"; Benchmark 2020
  "around 734GWh", 2025 "4.8TWh": all string-matched on the publishers' own free pages.
The round numbers are the publishers' own ("more than 4 TWh", "close to 2,600 GWh"): they publish rounded headlines,
not plant-level tables (those sit behind subscriptions). Treat them as ±5–10%.

## After the improvement round and T083 audit (2026-11-24)
Stricter Series D (D-032: no full-plan credit for partly dated plants) plus history fills (T080/T081/T085):
D 2023/2024/2025 = 1,647 / 2,018 / 3,349 GWh; E = 1,851 / 2,366 / 3,403 GWh (Great Power Ah estimates +22/+24/+16 reported
separately). CATL basis note (audit): CATL's disclosed 产能 is the utilisation denominator (effective, year-average),
while our site sums are year-end government-basis design capacity, so CATL's unallocated remainder in 2020–2024 is
understated; in 2025 our CATL sites (875) exceed its 772 by 13% — Series D likely over-credits some CATL sites
(Ningde 330, Yibin 210 on government basis), and part of CATL's 2024→2025 jump in E is that basis switch.

## Outlook: planned capacity vs published pipelines (2026-11-24)
By status (never summed into one figure): operational plants' full site plans 6.84 TWh; under construction 1.73 TWh
(1.68 due by 2030); announced 1.08 TWh. Benchmarks: IEA "around 9.4 TWh by 2030 if all announced plants are built"
(Batteries and Secure Energy Transitions, via search result); Benchmark ">10 TWh" 2030 pipeline (free page); BNEF
7.9 TWh announced for end-2025. Our planned totals are of the same order. Freshness: 48 non-operational projects have
no source after mid-2025 (T096 checks them). Series D/D-high by year: 2026 4.4/5.9, 2027 4.7/6.2, 2030 4.8/6.3 TWh.

## History status after round 2 (2026-11-24)
Sourced D / F (D + modelled backfill + unallocated), TWh: 2018 0.07/0.17 · 2020 0.23/0.36 · 2021 0.48/0.56 · 2022 1.04/1.23 ·
2023 1.77/2.06 · 2024 2.11/2.52 · 2025 3.42/3.47. Benchmarks: Benchmark 2020 0.73; IEA 2022 ~1.5 (GEVO 2023) or ~1.72 (implied by
the 2024 report); IEA/BNEF 2023 2.5/2.6; 2024 3.0/3.1; 2025 >4.0. F reaches ~49% (2020), ~72–82% (2022), ~80% (2023), ~82% (2024),
~87% (2025). What was done: series bug fixed (pre-anchor sourced steps now count; no full-plan credit before an installed anchor);
~40 plant histories sourced (T073, T080–T081, T092–T094, T099); company histories from IPO prospectuses (CATL 2015–2017, 2019;
Farasis 2017–2019); survivorship search (T095: Waterma, Aoyou, Guoneng, JEVE… — only company-level totals exist).
Remaining gap is concentrated in China 2018–2022: closed tier-2/3 makers whose site capacity was never published, and plants
whose current capacity is known but whose ramp is not. Open sources do not close it plant by plant.
Regional 2030 pipeline (active, by status, ref year ≤2030): Europe 369 operational-site plans / 296 under construction / 75
announced GWh (≈0.74 TWh); North America 527 / 252 / 24 (≈0.80 TWh). Benchmark's 2023-vintage 2030 pipelines were 1.2 TWh
(Europe) and 1.3 TWh (North America); since then we record 223 GWh (Europe) and 301 GWh (North America) as paused or
cancelled — the pipelines have shrunk, consistent with the gap.

## After series v3 (D-034) and history round 3 (2026-11-24)
Global TWh, D (sourced) / E (+company totals) / F (+labelled modelled history): 2020 0.16/0.23/0.36 · 2022 0.75/1.04/1.22 ·
2023 1.69/1.95/2.07 · 2024 2.08/2.45/2.54 · 2025 3.48/3.54/3.54. China only (F, approx.): 2022 ~1.0, 2023 ~1.8 (BNEF 2.2
nameplate → ~80%), 2024 ~2.2 (CRU ">2 TWh" → consistent), 2025 ~2.8 (IEA ">80% of >4 TWh" → ~87%). The sourced series is
now strict (no rejected v1 history, nothing before start year); the remaining early-year gap is explicit in F/E.
