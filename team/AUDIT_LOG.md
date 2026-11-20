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
