# Escalations

Questions only a human can answer. Agents add items and stop that line of work.
Mark blocking items with "blocking". The human ticks items and writes the answer.

- [ ] (example) T00X blocking: <what is needed> – <why it cannot be resolved without a human>

- [ ] T004 non-blocking: CALB Changzhou Jintan base – no open page gives built capacity; CALB 2025 annual report (HKEX, extracted to team/evidence/filings/CALB_3931_AR2025.txt) has no per-base GWh. Capacity left null, confidence 0.5. Would need a Jintan government phase table or company IR answer.
- [ ] T002 non-blocking: CATL Xiamen phase 1/2 and Xining capacity unconfirmed in open sources (null, conf 0.4). HKEX 2025 prospectus text might settle it.
- [ ] T005 non-blocking: Gotion stale/conflicting large plants kept below 0.6 by rule D-015 (Slovakia 8.4 vs 20, Morocco ph1 20 vs 10, Tongcheng/Liuzhou/Tangshan stale installed). Need fresher open sources; G4 will list them.
- [ ] T007/T009 cross-task duplicate: lanjun-new-energy-lanjun-new-energy-jiashan-base-china (T009) and rept-battero-rept-battero-jiaxing-plant-china (T007, renamed Jiashan) are the same site (16+16+45). Resolve in T007 rework: remove T007 row as duplicate_of the Lanjun id.
- [ ] T030 (lead): v1 researcher-supplied coordinates (geo_precision=site_unflagged, 33 rows) are unvalidated — Great Power Guangde carries the Shenzhen centroid. Distance-check each against its named city; null outliers.
- [ ] T017 non-blocking: Statevolt Imperial Valley (54 GWh announced, conf 0.35) — newest evidence 2023-01; AMS Oct 2024 reports the US project 'temporarily on hold' (T020 S11). Recommend project_state paused; owner to confirm.
- [ ] T041 follow-up: west-China sweep truncated by search budget (Ningxia, Xinjiang, Yunnan, Guizhou, Qinghai, Tibet unsearched). Puer Dianna (Yunnan, 2 GWh) cell vs pack unresolved.
- [ ] T044 follow-up: sweep truncated — rerun Canada, Mexico, South America, Africa, Oceania, Russia secondary makers, US small LFP/ESS, Poland/Baltics/Nordics. Leads: Saft Bordeaux solid-state lines, Ruien Inđija (Serbia), Liotech Novosibirsk.
- [ ] T042 follow-up: north-China sweep truncated — rerun Shandong (Weifang, Linyi, Dezhou, Liaocheng, Weihai, Taian, Zibo, Binzhou), Hebei, Shanxi, Tianjin, Beijing, NE China. Leads: Qingtao Wuhai (cell GWh?), Zhongbei Runliang location, Gotion Baotou (brochure only).
- [ ] T040 follow-up: Hubei and Henan prefecture sweeps not run (search budget); itdcw.com unreachable.
- [ ] T038 follow-up: Shanghai + Zhejiang prefectures + Wuxi/Zhenjiang/Suqian/Lianyungang unsearched; Pengcheng Wuxian location conflict (Yibin vs Xuzhou New District) — check whether there are two sites.
- [ ] T059: SVOLT Ma'anshan row says prismatic / 28 GWh nameplate; SVOLT June-2023 prospectus (lines ~9633-9637, ~10782) shows 21700 cylindrical winding lines of ~1 GWh combined with Shangrao. Re-check and correct.
- [ ] T057: Lishen Qingdao nameplate 40 GWh (Solarbe/Xinhua 2023 "40GWh的年生产能力") likely overstated — company 2024: Tianjin+Qingdao combined 8 GWh existing; 2019 full-site plan 10 GWh (EnergyTrend). Possible 40亿瓦时 (=4 GWh) misread. Recommend 10 GWh after confirming.
- [ ] T057: CALB Jintan nameplate 70 (reported) — no open phase GWh table; Sina 2025-06 says 三期 built + 25 GWh planned for 2026. Needs Jintan gov or HKEX source. CALB 2025 shipments ~116 GWh vs our C ~185 GWh.
- [ ] T056: BYD rows below 0.6 with ≥20 GWh — Xining 24 (2018 sources), Xi'an 30, Guiyang 20 (aggregator), Zhengzhou 40 (reported). BYD planned >500 GWh across 12 bases (Sina 2025-08-06) vs our ~275 GWh C; no open site-level installed totals. Guiyang vs Gui'an Fudi may be two entities.
- [ ] verify_quotes: T056:S5 (cnevpost ?p=55762) reported MISSING but all fragments present in article body on manual check (lead, 2026-11-20) — likely script-tag/JSON-LD stripping issue in the verifier.
- [ ] T060 residue: SVOLT Ma'anshan 28 GWh (2021 cells+PACK plan; prospectus 4-base forecast suggests scaled back) — needs 2024+ source. BYD Kengzi/Pingshan: entity exists, no cell-production evidence — owner: keep at status null or remove? BYD Xining current capacity unresolved. BYD Zhengzhou start_year 2024 vs production-from-2023 sources. jintan.gov.cn not reachable (network allowlist).
- [ ] T063: PPES Himeji row nameplate 30 GWh vs Newswitch 2025-10-20 "姫路工場の新ラインの生産能力は年間約７ギガワット時" — check whether 7 is only the new line. GS Yuasa Ibaraki 2 GWh: confirm cell (not system) scope. METI battery-plan PDFs (battery_17_2/17_3, kansai.meti 250311) return 403 here; DART (KR) capacity tables not readable — JP/KR site capacities stay largely unsourced.
- [ ] verify_quotes samples reported-tier sources (T063:S1 snippet) as MISSING — should skip tier=reported.
- [ ] T064: Jiahang Xinhui 35 GWh (groundbreaking 2025-05) vs CALB Jiangmen phase 2 35 GWh (Xinhui; EIA passed, construction pending 2026-02) — possible double count in pipeline; no source links them. Kexiang Daya Bay 8 GWh may bundle systems (D-026?).
- [ ] T065: Anneng Qisheng Linwu 20 GWh (vs earlier 50; cell vs pack unclear) and Nafang Yueyang 10 GWh sodium at 0.3 — need EIA/company source. Sany Redelephant Changsha "5GWh" cell scope unclear (nameplate null). Geely Ganzhou 42 GWh (2021) vs Farasis Ganzhou — overlap? (T066 ENERGEE). Lead: Dianna Pu'er 2 GWh sodium (Yunnan) not in DB. Hefei/Fuyang/Bengbu/Huainan/Chizhou only lightly covered — source-led pass (municipal 重点项目 lists, EIA notices) suggested.
