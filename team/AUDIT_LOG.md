# Audit log

One entry per audit. Used to tune the harness: which checks catch real problems,
which failure types recur, whether the model tiers are right.

| Date | Task | Verdict | Failure type (spec gap / capability / diligence / none) | What was caught |
|---|---|---|---|---|


## T002 (CATL pilot) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence (primary), 2 capability, 2 spec gaps. Quotes 26/26 on page; values 24/26 supported (Xiamen-80 ref year from a structure-completion date; Thuringia start_year pointed at wrong source). Blocking: Yichun status the worker itself doubted; operator site list built from news, not CATL's disclosure (Times-FAW Xiapu, Ampace Xiamen missing); Luoyang nulled although People's Daily 2023-09-25 gives phase 1 = 60 GWh. G4: 4 large rows < 0.6 not escalated.
Caught by: auditor value-vs-quote probe and independent search (checks C0–C6 could not catch any of these).
Harness changes: brief steps 6–8 (dig/escalate, open snippets, mine cited pages), self-check additions (quote contains number, ref-year from 达产 statement, phase arithmetic), D-012 narrowed, installed basis note, lead-side filings extraction (scripts/fetch_filings.py) because workers cannot read PDFs.

## T004 (CALB + Chuneng) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · capability/spec gap. 41/41 quotes verbatim (WebFetch-summary risk did not materialise). Blocking: single-site nameplate cut to built+UC although full plan stated (Xiangyang 100, Zaozhuang 100) → convention ambiguity, fixed by D-014; Zigong 50 quote lacks number; Sines under_construction unsupported (only ceremony + contract award); AR2025 entities (Luoyang, Thailand, Fujian) missing from site list. Verifier weakness found: gzip responses (fixed).
Caught by: auditor meaning-of-quote probe and filing cross-check.

## T002 (CATL) – audit 2 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence. All audit-1 blockers resolved; 43/43 quotes on page. Blocking: Times-FAW Xiapu capacity double-counted inside Ningde hub; Luoyuan newest evidence 2025-04 (fix available in AR). Minor: Zhaoqing fund reallocation, Liyang ref-year basis, Times-SAIC Liyang JV missing from DB (→ new add), CATL installed sum 26% above company end-2025 figure (G2 basis question for lead, T030).

## T002 – lead verification of audit-2 fixes – 2026-11-20 → merged
Times-FAW Xiapu capacity nulled (inside Ningde hub); Luoyuan/Dongying cite AR2025 guarantee (S50/S51 FOUND); D-014 applied (Ningde 500, Liyang 206, Yichun 120). Open minor: Yichun ref year 2022 fallback predates the 70 GWh phase-2 plan source — T030 sweep.

## T004 – lead verification of audit-1 fixes – 2026-11-20 → merged
Xiangyang 100, Zaozhuang 100 (ref 2028 estimated from 2-year build, noted), Wuhan 50, Yichang 195; Zigong quote now contains 50GWh (S44 FOUND); Sines → announced; CALB Fujian/Luoyang/Thailand in site list. verify_quotes 41/42 FOUND. Open: CALB Changzhou capacity null (escalated); many CALB operational rows lack installed figures (G2 undercount risk).
