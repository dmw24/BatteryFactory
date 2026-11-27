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

## T006 (EVE + Hithium) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence. Quotes 15/15 on page; Hithium figures site-level and confirmed (v1 Xiamen 56 was Chongqing's). Blocking: Jingmen nameplate = installed though own source says 212 GWh after super-factory phase 2; Shenyang operational on trial-production + pack-factory quotes; Qidong 50 GWh announced project matched to a null-capacity JV row (uncounted). Minor: Malaysia quote lacks number; Qujing ref year available in AR.

## T005 (Gotion) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence + spec gap. 23/23 quotes on page, 3 don't support their use. Blocking: Nantong removed as not_found though operating (stockstar 2026-09-18: phase 1 5 GWh 达产 2020) — partly induced by the lead's rework hint (lesson filed); Lujiang is_cell=false on a building name though autohome 2021 shows a 6 GWh line; Jinzhai installed/nameplate inconsistent; 4 large rows parked at 0.6 despite stale/conflicting data; v1 chemistry carried unquoted. Spec gap: undated "over time" targets under D-014 → D-015.
Caught by: auditor independent search (Nantong, Lujiang) — checks could not.

## T006 – lead verification of audit-1 fixes – 2026-11-20 → merged
All 3 blockers fixed and new quotes FOUND (J4, JM2, SY4, CD1, M2, A7); G2 hand-confirmed (punctuation). Jingmen ref year 2025 is a fallback (phase-2 due date not public).

## T005 – lead verification of audit-1 fixes – 2026-11-20 → merged
Nantong restored as operational 5/10 (S50 FOUND), Lujiang is_cell true with 6 GWh stale line (S51, cited by auditor; fetch blocked here), Jinzhai installed 5 as of 2025-02, D-015 applied (Morocco 20, Slovakia 8.4 per latest company filing), confidence caps applied.

## T003 – lead verification of audit-1 fixes – 2026-11-20 → merged
D-016 applied (Zhengzhou/Shenzhen/Xi'an null status at 0.3; env-list rows ≤0.4; 6 FinDreams entities added), Jinan/Xining capped, Wuwei/Fuzhou coords nulled, FAW installed nulled, Changzhou removal re-cited. Verifier bug found and fixed (HTML tag stripping ate PDF text containing '<'); quotes 51/54 FOUND. Open minor: Shaoxing installed 45 rests on 通线 (lines connected) 2025-12-30 – production not yet stated; T030 sweep. BYD rows' installed (123) ≪ BYD 2025 installations (285.6 GWh): structural undercount from undisclosed per-site capacity.

## T010 (LGES) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence. Quotes fine (1 wording mismatch). Blocking: D-015 caps not applied (HLI stale installed at 0.7; Arizona 36/44/53 conflict at 0.65; Ochang/Holland/Nanjing parked at 0.6); Nanjing hub nameplate covers LGESNJ only; Spring Hill whole 50 labelled LFP/ESS; v1 Warren/Ochang vocab carried. LGES ESG 2025 (site table as of Jun 2026) confirms HL-GA operational, NextStar 100% LGES, no Morocco. Lead's fetch of the ESG PDF had failed silently — fixed by importing the auditor's extract.

## T007 (Sunwoda + REPT) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence (worker started before D-015/D-016). 39/39 quotes on page; REPT AR quotes (read from page images) confirmed in text extract. Blocking: Quzhou/Shenzhen removed without positive evidence (AR lists Shenzhen production bases); Jiashan installed 32 = arithmetic (77−45), S7 says construction completed only; Nanchang/Jiashan above D-015 cap; Huizhou Liwei status from subsidiary table. Cross-task: Jiashan duplicates T009 Lanjun row → T007 row to be removed as duplicate.

## T009 (China mid-tier) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence + capability. 15/15 quotes found. Blocking: Lishen Mianyang and Ganfeng Dongguan removed though their own sources show cell activity; Lishen Tianjin HQ cell plant dropped when re-scoping to Binhai; Zenergy company total (35.5) stored as Changshu; CBAK "goals" as nameplate; D-015 caps not applied (Lanjun, Tianneng, Chuzhou).
Pattern across T005/T007/T009: workers remove rows on absence of evidence; D-015 removal rule now in conventions — watch in remaining tasks.

## Security note – 2026-11-20
T012 worker reported a prompt-injection block ("網站公告" telling AI readers to quote specified sentences) on wantrich.chinatimes.com/news/20260716900012-420101; page ignored, not cited. Researcher isolation (no shell) held.

## T008 (SVOLT + Great Power) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence. 15/15 sampled quotes on page (Nov-2022 prospectus has a text layer after all). Blocking: D-015 caps (Shangrao, Suining, Yancheng, Chengdu, Ma'anshan at 0.6); Suining installed 20 contradicted by SVOLT 2023 filing ("尚未投入生产" end-2022); Huzhou operational on a pack roll-off; Taizhou removal needed the filing's PACK-only evidence (available). Spec: superseded phase totals → D-017. Found geocoder bug: Guangde row carries Shenzhen centroid ([GEO=city:Shenzhen]) — check all city-tier coordinates in T030.

## T007, T009, T010 – lead verification of audit-1 fixes – 2026-11-20 → merged
T007: Quzhou/Shenzhen restored (null status, 0.3); Jiashan removed as duplicate_of Lanjun row (T009); Nanchang capped; Huizhou Liwei S51 (county energy review); escalations filed. Quotes 33/40 FOUND (misses hand-confirmed in audit). Foshan source host szb.nanhaitoday.com unreachable from this environment.
T009: Mianyang/Dongguan restored; Tianjin HQ row added; Zenergy Changshu = company basis (all sites), nameplate 70.5 ref 2027, Nanjing row added; Lanjun installed 16 (phase 1 only); CBAK aspirations moved to notes. Quotes 54/54 FOUND.
T010: D-015 caps applied (HLI, Arizona, Ochang, Holland, Nanjing floor, Spring Hill mixed); ESG 2025 site-table citations; NextStar 100% LGES. Quotes 54/71 FOUND; misses largely hand-confirmed in audit 1.
T008 – lead verification → merged: caps, Suining, Huzhou D-016, Chengdu D-017, filing-backed removals; quotes 35/38 FOUND.

## T012 (Envision AESC) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence. 21/23 quotes on page (1 paraphrase). Blocking: Ordos nameplate 30.5 vs company 10.5 on the cited page (D-015/017), parked at 0.62; Ibaraki 20 is an undated 'eventually' total. Minor: Smyrna 3 vs AESC 7; Shiyan supersession weak; Sunderland Plant 1 status; Cangzhou ramp step.

## T013 (Japan majors + Tesla) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · capability + diligence. 41/41 quotes on page. Blocking: Tesla Nevada LFP 'Early Ramp' 7 GWh stored as installed though footnote says it includes expected capacity; Blue Energy ref year (Honda: ramp through 2030); TBMNC cell question resolvable from open press; Kaizuka/Miyagi status from plan/2018 quotes; NCA applied from a non-site source.

T012 – lead verification → merged (Ordos 10.5 company figure, Ibaraki 6, Smyrna 7, Sunderland P1 status null).
T014 – waived (sampled out, normal risk); lead fixed one id typo in patch (integration fix); FAAM start_year nulled after C3.
T013 – lead verification → merged (fixes verified; S49–S51 FOUND; 8 misses were hand-confirmed in audit 1).

## T011 (SK On + Samsung SDI) – audit 1 – 2026-11-20
VERDICT fail · diligence. 21/23 sources confirmed. Blocking: StarPlus Plant 2 (34 GWh) on hold per Samsung SDI CEO 2026-03-18 but still in nameplate; v1 chemistry/format carried unquoted on 7 rows; Komárom Plant 1 possibly idle. Spec gap: idle/retooling plants → D-018.
T015 – waived (sampled out); D-018 applied before merge.
T011 – lead verification → merged (D-018 applied; StarPlus 33; R6 nulls).
T017 – waived (sampled out); lead quote spot-check 26/40 FOUND, 4 MISSING, 10 FETCH_FAIL.
T018 – waived (sampled out); quotes 24/30; India v1 city coords found wrong on 4 rows and nulled by worker.

## T016 (USA tail A) – audit 1 – 2026-11-20
VERDICT fail · diligence. 20/20 quotes. Blocking: installed=0 instead of null on closed rows (D-018); Eos Turtle Creek still active/2 GWh though Line 1 dismantled; 2 unchecked v1 fields. Spec gap: long-duration non-Li 'GWh' (Form iron-air 500 MW x 100 h) not comparable → D-019.
T016 – lead verification → merged (no installed=0 left; Eos paused; Form via D-019).
T019 – waived (sampled out); APB chemistry vocab fix before merge.

## T021 (China tail 1) – audit 1 – 2026-11-20
VERDICT fail · diligence. 15/15 quotes. Blocking: Zhongna storage line counted as cells; Camel Xiangyang operational on low-voltage lines while AR shows 2 GWh storage-cell phase at 54.76%; Chuanhong parked at 0.6. Integration note: build_timeseries online_year falls back to capacity_ref_year for operational rows without start_year (T030).

## T020 (Rest of World) – audit 1 – 2026-11-20
VERDICT fail · diligence. 26/26 quotes on page; 4 removals hold. Blocking: Megamillion 32 GWh undated aspiration as nameplate; no ESCALATE for Statevolt/Megamillion; E-One Moli status contradicts its quote. Spec: D-020 (site works vs ceremony).

## T023 (China tail 3) – audit 1 – 2026-11-20
VERDICT fail · diligence. 29/29 quotes on page. Blocking: Pylontech Shanghai removed on MES-coverage quote while AR shows a manufacturing subsidiary; Narada Hangzhou evidence in AR ignored; Alxa nameplate quote lacks number; missing ESCALATE lines.
T021 – lead verification → merged.

## T022 (China tail 2) – audit 1 – 2026-11-20
VERDICT fail · capability+diligence. 24/24 quotes; adds real. Blocking: Jinglan/Guoke ref years; Veken D-013 cap; Tafel company figure as site; Microvast pouch unsourced.
T020 – lead verification → merged (Megamillion 1 GWh, D-020 statuses, S4 trimmed by lead to verbatim-confirmed fragments).
T022 – lead verification → merged (ref years, Tafel nulls, Veken cap; new quotes FOUND).
T023 – lead verification → merged (Pylontech Shanghai restored, Narada Nandu Power operational ≤0.4 with AR evidence, Alxa quote).

## T024 (China tail 4) – audit 1 – 2026-11-20
VERDICT fail · diligence. 21/21 quotes. Blocking: Qingtao 10.5 arithmetic vs source's 10; Wanxiang 80 vision (2019–2035) as nameplate with ref 2024 (stated phases 24+32=56). Spec gap → D-021.
T024 – lead verification → merged.

## T039 (southeast China sweep) – audit – 2026-11-20
VERDICT pass · 13/14 quotes; no duplicates; minors fixed by lead (ATL Wikipedia-only status → reported; S14 apostrophe).

## T083 — independent audit of T056–T085, T082, T089 (Opus, 2026-11-24) — verdict FAIL → fixed by lead (T090)
Sampled ~40 rows, 31 sources re-fetched (30 verbatim, 1 not), all 100 T089 coordinates. Found: 3 unearned confidence
rises (Wanxiang, Statevolt, Zenergy Xiangcheng), deadline/construction-complete dates used as phase years (Zenergy
2027, Wanxiang, Mengguli 2020, Hohhot 2026, Lanjun 2024 step), a derived sum as a step (EVE Jingmen 2023), 3 homonym
coordinates (Yizhuang, Mimarsinan, Bartow) + a state centroid, 18 rows parked at 0.6, inconsistent D-026. Passed:
CATL company capacity 6/6, Great Power conversion, company_map, Inpower/Xiangyang/FAW. Systemic fixes: D-032 ref-year
basis (build_timeseries ref_basis), C8 warning for 0.6 parking, D-031 PACK rule. Remaining: T091 (17 rows at 0.6).

## T102 — checkpoint audit of the history round (Opus, 2026-11-24) — verdict FAIL → fixed (T104, D-034)
Patches mostly sound (quotes ~60/62 found) but corrections never reached the series: build_timeseries read v1
capacity_timeline ahead of v2 steps and labelled it "confirmed" (~0.3 TWh of D 2022 on rejected points); the online-year
extension credited capacity before start_year; F used CATL's 2019 total as its 2018 value. Data: Chuneng Xiaogan
2025-vs-2023 start, DFD Nanning sum, Aoyou budget figure, Guoneng inferred status, SVOLT Wuhan idle, Farasis Zhenjiang
start, Envision Wuxi/Tangshan ref years, SVOLT Shangrao installed, Gotion Liuzhou start 2024 vs 2022. All fixed
(T104 + series_core rewrite). Open: T096/T100 'no news' rows ≥10 GWh with one search → T105.

## T111 — checkpoint audit (Opus, 2026-11-25) — verdict FAIL → fixed (T113, D-035)
Per-field tiers made reported steps "confirmed" (CALB Xiamen 2023:10/2027:60 after T110 added a 2021 quote); partly
rejected v1 rows still used rejected points (Lyten 2021, Yaoning Jianhu 2023); A included phase steps while documented as
installed floor; B plan-filled before first step; D ignored newer lower anchors; pipeline overlapped C; CALB Luoyang
mapped after its sale; Zenergy Nanjing idle since 2022; XCMG via an unconfirmed v1 plan point; Yaoning 0.62. All fixed.
Passed: F caps and ramp, 22/22 company figures vs filings, T107–T109.

## SC audit 1 (supply chain, Opus auditor) — 2026-11-27 — FAIL → fixed
Sample 68 rows; 0 fabricated quotes; 21% rows with a defect, 10% number-changing. Benchmark layer FAIL (not like-for-like).
Fixed (SCZ_lead_fixes.json, scripts): SQM Carmen LCE double count; Tengyuan group capacities moved to company_totals;
SKIET Poland company-wide capacity nulled; Jianxiawo estimate removed from data; Qinghai 40 kt and Huixin → under
construction (trial runs); Albemarle Atacama production quote demoted; Shanshan Anning ref year; Mitsubishi installed date;
Jade Bay duplicate removed; CGS construction points → town precision. sc_benchmark v2: built vs plan-only capacity,
nickel one stage per chain (intermediates separate), D-103 brine chemicals in Li refining, China-only vs incl.-overseas
company totals, active rows only; scripts/sc_build_all.py regenerates every derived file. Open: CNGR Indonesian
smelter chain links (part_of), Goulamina design-grade norm, Wanrun Hubei aggregate row.

## SC audit 2 (Opus) — 2026-11-27 — FAIL → fixed
New rows sample 52: 21% number-changing defects, no fabricated quotes. Fixed as rules (scripts/sc_core.py shared by
benchmark and timeseries): built = installed/dated steps only (D1/D5), rest of plan = upper bound; nickel intermediates
split in the timeseries (D2); CGS patch renamed SA0_ so filings override it, KPS/Huake capacity overrides dropped (D3);
D-103 brine regex tightened (D8); reported-tier built shown separately (systemic D). Rows: Pomalaa production (D4),
GEM QMB park totals → company_totals (D6), CNGR high-matte conversion part_of (D7), Novonix → under construction (D9),
Jinchuan group → company_totals (D10), target steps removed (D11), unsupported feeds removed (D12). Open: ref_basis is
still not a field (rule now avoids needing it); Electra CoSO4 unit; Harita ore sales as production (labelled).

## SC audit 3 (Opus, focused) — 2026-11-27 — FAIL → fixed
Sample 25 rows: 0% number-changing; systemic misses fixed: D-103 regex regression (Chinese salt-lake plants restored to
Li refining), intermediates excluded from nickel production too (sc_core.is_intermediate), GEM QMB park capacity nulled,
POSCO Sejong step = quoted 24 kt, stale evidence dropped at build, 14 unsourced feeds removed (S4 covers feeds),
SA0 task id, D-110 precedence, reconciliation notes rewritten (built = confirmed-date floor).

## SC audit 4 (Opus) — 2026-11-27 — FAIL → fixed
Installed rows 11% number-changing, links 36% company-level. Fixed: Ceria/Huafei and CGS-only installed values nulled
(D-111 amended: second source required), D-112 trial production rule (Huixin, Qinghai 40 kt, Jiabusi, Arcadia sulphate),
Tianhua line 2 / Weiling / Hengxinrong / Fengxin installed nulled, Sal de Oro step, GEM NiSO4 mixed-metal unit,
Harjavalta capacity evidence, superseded evidence retired (drop_evidence), company-level links → feeds_company (D-113),
FINAL_REPORT_SC figures now generated by scripts/sc_status.py, reconciliation notes corrected.
