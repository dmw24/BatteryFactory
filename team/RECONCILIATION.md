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
