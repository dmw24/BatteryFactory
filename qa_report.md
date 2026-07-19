# Battery Gigafactory Database — QA report

Generated from `factories.db`. Total rows: **378**. Confirmed cell manufacturers: **354**. Flagged non-cell (pack/material/recycling, kept and tagged): **24**.

> Capacity is annual GWh/year at nameplate. Totals are grouped by status and are **never summed across statuses** — announced, under-construction and operational capacity are distinct and must not be added together.


## 4. Totals by status (capacity never summed across status)

| status | plants | Σ nameplate GWh/yr |
|---|---:|---:|
| operational | 266 | 5808.0 |
| under_construction | 62 | 1881.0 |
| announced | 36 | 614.0 |
| (unknown) | 14 | 30.0 |

### Region × status matrix

| region | status | plants | Σ nameplate GWh/yr |
|---|---|---:|---:|
| China | (unknown) | 8 | — |
| China | announced | 8 | 117.0 |
| China | operational | 149 | 4454.0 |
| China | under_construction | 16 | 488.0 |
| Europe | (unknown) | 3 | 30.0 |
| Europe | announced | 7 | 202.0 |
| Europe | operational | 25 | 436.0 |
| Europe | under_construction | 17 | 525.0 |
| India | announced | 7 | 72.0 |
| India | operational | 6 | 23.0 |
| India | under_construction | 8 | 192.0 |
| Japan | announced | 1 | — |
| Japan | operational | 19 | 80.0 |
| Japan | under_construction | 3 | 46.0 |
| Rest of World | announced | 8 | 151.0 |
| Rest of World | operational | 11 | 55.0 |
| Rest of World | under_construction | 3 | 250.0 |
| South Korea | (unknown) | 2 | — |
| South Korea | operational | 11 | 68.0 |
| South Korea | under_construction | 1 | 16.0 |
| Southeast Asia | (unknown) | 1 | — |
| Southeast Asia | announced | 1 | 8.0 |
| Southeast Asia | operational | 11 | 83.0 |
| Southeast Asia | under_construction | 3 | 37.0 |
| USA | announced | 4 | 64.0 |
| USA | operational | 34 | 610.0 |
| USA | under_construction | 11 | 327.0 |

## 1. Suspected duplicate sites (1 pair/group)

Review these — they may be the same physical site under different names, or legitimately distinct sites of the same operator.

| signal | plants | ids |
|---|---|---|
| same operator + shared location token 'hangzhou' | Narada Hangzhou Lin'an Plant ⟷ Nandu Power (Narada) Hangzhou/Fuyang Lithium Cell Base | narada-power-zhejiang-narada-power-source-co-ltd-narada-hangzhou-lin-an-plant-china, narada-power-nandu-power-nandu-power-narada-hangzhou-fuyang-lithium-cell-base-china |

## 2. Capacity double-count / consistency flags (20 rows)

| plant | operator | region | nameplate GWh | flag |
|---|---|---|---:|---|
| CATL Ningde plant (Ningde manufacturing hub) | CATL | China | 330.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| CATL Zhaoqing plant | CATL | China | 25.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| CATL Guiyang (Gui'an) battery production base | CATL | China | 60.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| CATL Jining plant (Shandong Times energy storage and power battery base) | CATL | China | 160.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| BYD FinDreams Xining plant (Qinghai FinDreams Battery Co., Ltd.) | BYD | China | 24.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| BYD FinDreams Shenzhen plant (Kengzi/Pingshan base) | FinDreams Battery (BYD) | China | 50.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Qingdao Gotion Battery plant (Laixi) | Gotion High-tech | China | 3.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Lishen Tianjin plant (Tianjin Binhai New Energy Industry Base) | Tianjin Lishen Battery Joint-Stock Co., Ltd. | China | 24.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| CATL Fuding (Fuding Shidai) production base | CATL | China | 120.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Weichai-FinDreams (Yantai) New Energy Power Industrial Park | Weichai-FinDreams | China | 50.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Zenergy Changshu Plant | Jiangsu Zenergy | China | 50.5 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Phylion Suzhou Plant (Suzhou manufacturing base) | Phylion Battery (Xingheng Power Co., Ltd.) | China | 2.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| DFD Jiaozuo Plant (Do-Fluoride New Energy, Henan base) | Do-Fluoride New Energy Technology Co., Ltd. (DFD) | China | 10.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Great Power Ulanqab energy storage and semi-solid-state cell plant | Great Power | China | 11.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Samsung SDI Göd | Samsung SDI | Europe | 60.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| SK On Komárom | SK On | Europe | 17.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| JSW Energy Cell Gigafactory | JSW Energy | India | 30.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Eos Energy Turtle Creek | Eos Energy Enterprises | USA | 1.25 | capacity may be a hub/company-wide aggregate (double-count risk) |
| EnerVenue Shelby County | EnerVenue | USA | 1.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Talent New Energy Chongqing Solid-State Plant | Talent New Energy | China | 2.2 | capacity may be a hub/company-wide aggregate (double-count risk) |

### Live cell sites missing a nameplate figure (55)

Genuine cell plants (operational/under-construction) with no sourced capacity — capacity left null per the no-guessing rule.

| plant | operator | region | status |
|---|---|---|---|
| EVE Energy Huizhou plant (Zhongkai High-tech Zone production base) | EVE Energy | China | operational |
| SVOLT Baoding plant (R&D centre) | SVOLT (Honeycomb Energy / 蜂巢能源) | China | operational |
| EVE Energy Ningbo plant | EVE Energy | China | operational |
| Gotion New Energy (Chuzhou) high-end manufacturing base | Gotion (Chuzhou Gotion New Energy Power Co., Ltd.) | China | under_construction |
| Lishen Mianyang Southwest Production Base | Tianjin Lishen Battery | China | operational |
| Narada Hangzhou Lin'an Plant | Narada Power (Zhejiang Narada Power Source Co., Ltd.) | China | operational |
| CosMX Zhuhai Plant (Zhuhai headquarters / polymer lithium-ion battery base) | Zhuhai CosMX Battery Co., Ltd. | China | operational |
| CosMX Chongqing Plant | Zhuhai CosMX Battery | China | operational |
| Zhuoneng Shenzhen Plant | Shenzhen Zhuoneng New Energy Co., Ltd | China | operational |
| Veken Ningbo sodium-ion plant | Veken Technology | China | operational |
| Pylontech Shanghai LFP cell base | Pylontech (Pylon Technologies Co., Ltd.) | China | operational |
| Beyonder Battery Center (Forus/Sandnes) | Beyonder AS | Europe | operational |
| Customcells Itzehoe | Customcells | Europe | operational |
| Customcells Tübingen | CustomCells | Europe | operational |
| Toshiba Kashiwazaki Operations (SCiB) | Toshiba Infrastructure Systems & Solutions Corporation | Japan | operational |
| Murata Yasu Plant | Murata Manufacturing | Japan | operational |
| Toshiba Yokohama Plant (SCiB) | Toshiba Infrastructure Systems & Solutions Corporation | Japan | operational |
| Ono Works | Maxell | Japan | operational |
| Kawasaki Plant | Eliiy Power | Japan | operational |
| Washizu Plant (Kosai) | FDK Energy Co., Ltd. (FDK Corporation) | Japan | operational |
| Daejeon all-solid-state pilot line | SK On | South Korea | operational |
| Suwon S-Line all-solid-state pilot | Samsung SDI | South Korea | operational |
| Siheung Plant | Kokam | South Korea | operational |
| Cheonan Plant | EIG (Energy Innovation Group Ltd.) | South Korea | operational |
| Daejeon flexible battery pilot | LiBEST | South Korea | operational |
| Amperex Technology Sohna Cell Plant | Amperex Technology Limited (ATL India Technology Pvt Ltd) | India | operational |
| TDS Lithium-Ion Battery Gujarat (Hansalpur) | TDS Lithium-Ion Battery Gujarat Pvt Ltd (TDSG) | India | operational |
| Macsen Sodium-Ion Cell Pilot Line (Udaipur) | Macsen Labs | India | under_construction |
| Panasonic Energy Kaizuka Factory | Panasonic Energy Kaizuka Co., Ltd. | Japan | operational |
| PPES Tokushima Plant | Prime Planet Energy & Solutions | Japan | operational |
| Toyota Teiho Plant | Toyota Motor Corporation | Japan | operational |
| Toyota Battery (PEVE) Kosai Plant | Toyota Battery Co., Ltd. (formerly Primearth EV Energy / PEVE) | Japan | operational |
| Toyota Battery (PEVE) Miyagi Plant | Toyota Battery Co., Ltd. (formerly Primearth EV Energy) | Japan | operational |
| Sodium Batteries Australia pilot manufacturing facility | Sodium Batteries Australia | Rest of World | operational |
| Allegro Energy Warners Bay (pilot line at The Melt, Dashworks) | Allegro Energy | Rest of World | operational |
| Salient Energy Dartmouth | Salient Energy | Rest of World | operational |
| e-Zinc Mississauga Pilot Manufacturing Facility | e-Zinc | Rest of World | operational |
| Samsung SDI Cheonan Plant | Samsung SDI | South Korea | operational |
| QuantumScape San Jose (Eagle Line / QS-0) | QuantumScape | USA | operational |
| Solid Power Louisville EV Cell Pilot Line | Solid Power | USA | operational |
| Natron Energy Holland | Natron Energy | USA | operational |
| Ambri Marlborough | Ambri | USA | operational |
| UNIGRID San Diego | UNIGRID Battery | USA | under_construction |
| Inlyte Energy Hayward | Inlyte Energy | USA | operational |
| Zeta Energy Houston | Zeta Energy | USA | operational |
| Sunwoda Huizhou plant (Huizhou Liwei New Energy) | Huizhou Liwei New Energy Technology Co., Ltd. (Sunwoda) | China | operational |
| Sunwoda Quzhou plant | Sunwoda | China | operational |
| Gotion Sodium Plant Tangshan | Gotion High-tech | China | operational |
| Gotion Gnascent Sodium-Ion Plant Hefei | Gotion High-tech | China | operational |
| Nandu Power (Narada) Hangzhou/Fuyang Lithium Cell Base | Narada Power (Nandu Power) | China | operational |
| Shenzhen BetterPower Shenzhen Plant (Longhua base) | Shenzhen BetterPower Battery Co., Ltd | China | operational |
| Chilwee Changxing Lithium Cell Plant | Chilwee (Chaowei Group) | China | operational |
| Gree Titan Zhuhai LTO Cell Plant | Gree Titan (Gree Titanium New Energy, formerly Yinlong New Energy) | China | operational |
| Deligreen Shanghai Cylindrical Cell Plant | Shanghai Deligreen Power | China | operational |
| Tianpeng Power Zhangjiagang Cell Plant | Jiangsu Tianpeng Power Supply Co. (Tenpower) | China | operational |

## 3. Rows with confidence < 0.5 (36)

| plant | operator | country | conf | is_cell | note |
|---|---|---|---:|:---:|---|
| Nyobolt Sunderland | Nyobolt | United Kingdom | 0.1 | Y | NO EVIDENCE OF A NYOBOLT SITE IN SUNDERLAND — this candidate appears to be a seed-list err… |
| Nonsan Plant | Vitzrocell | South Korea | 0.15 | N | Could not confirm the existence of any Vitzrocell plant in Nonsan. Vitzrocell (KRX:082920)… |
| Hithium Chongqing plant | Hithium | China | 0.2 | Y | NO LIVE SOURCE COULD BE VERIFIED THIS SESSION. The organization's egress proxy returned 40… |
| Hithium Heze plant | Hithium | China | 0.2 | Y | LIVE RESEARCH BLOCKED: WebSearch budget fully exhausted (200/200) and the session egress p… |
| REPT Battero Liuzhou plant | REPT Battero | China | 0.2 | Y | RESEARCH BLOCKED: Could not verify any figure for this site. The session's WebSearch budge… |
| REPT Battero Foshan plant | REPT Battero | China | 0.2 | Y | RESEARCH BLOCKED - values unverified. This session's WebSearch budget was fully exhausted … |
| REPT Battero Chongqing plant | REPT Battero | China | 0.2 | Y | RESEARCH BLOCKED: This session had no usable web access. The WebSearch budget was fully ex… |
| Sunwoda Shenzhen plant | Sunwoda | China | 0.2 | N | COULD NOT VERIFY VIA LIVE SOURCES. This session had no working web access: the WebSearch b… |
| Sunwoda Zaozhuang plant | Sunwoda EVB (Sunwoda Electronic) | China | 0.2 | Y | UNVERIFIED THIS SESSION. All outbound web access was blocked: every external host (Wikiped… |
| Narada Wuxi LFP cell plant | Narada Power | China | 0.2 | N | Could NOT confirm any Narada Power battery CELL manufacturing plant in Wuxi. The only Nara… |
| REPT Battero Jiaxing plant | REPT Battero | China | 0.25 | Y | WEB ACCESS UNAVAILABLE THIS SESSION: the WebSearch budget was fully exhausted (200/200) be… |
| Durapower Singapore | Durapower | Singapore | 0.25 | N | Durapower Holdings is a Singapore-headquartered lithium-ion battery maker (founded 2009; H… |
| Hithium Xiamen plant (Xiamen production base) | Hithium | China | 0.3 | Y | WEB ACCESS BLOCKED: every external host returned HTTP 403 policy denials via this session'… |
| REPT Battero Wenzhou plant | REPT Battero | China | 0.3 | Y | IMPORTANT DATA-QUALITY CAVEAT: I could not verify any live source. All outbound HTTPS was … |
| EVE Energy Ningbo plant | EVE Energy | China | 0.3 | Y | Ningbo (Zhejiang province) is consistently listed as one of EVE Energy's ~12 domestic prod… |
| EVLOMO Nong Yai Battery Plant | EVLOMO | Thailand | 0.3 | Y | Announced April 2021 as an 8 GWh lithium-ion battery cell gigafactory ("gigafab") to be bu… |
| LG Energy Solution Morocco | LG Energy Solution | Morocco | 0.3 | N | No confirmed battery CELL manufacturing site for LG Energy Solution exists in Morocco. As … |
| Samsung SDI Giheung Plant | Samsung SDI | South Korea | 0.3 | N | Giheung (150-20 Gongse-ro, Giheung-gu, Yongin-si, Gyeonggi-do) is Samsung SDI's corporate … |
| Inlyte Energy Hayward | Inlyte Energy | United States | 0.3 | Y | Inlyte Energy is a US (San Francisco Bay Area) startup making sodium metal chloride / iron… |
| Narada Hangzhou Lin'an Plant | Narada Power (Zhejiang Narada Power Source Co., Ltd.) | China | 0.35 | Y | Lin'an District, Hangzhou (registered address: 666 Xiangfu Road, Qingshan Lake Street, Lin… |
| Liacon Itzehoe | Liacon | Germany | 0.35 | N | Itzehoe is Liacon GmbH's registered HQ and R&D base (co-located with Fraunhofer ISIT, from… |
| SVOLT Baoding plant (R&D centre) | SVOLT (Honeycomb Energy / 蜂巢能源) | China | 0.4 | Y | SVOLT's Baoding (Hebei) site is primarily the company's R&D centre and origin (spun out of… |
| SVOLT Taizhou plant | SVOLT (Honeycomb Energy) | China | 0.4 | N | The SVOLT "Taizhou plant" is a battery module/pack ASSEMBLY facility co-located with Great… |
| BYD FinDreams Huizhou plant | BYD FinDreams | China | 0.4 | Y | Huizhou BYD Battery Co., Ltd. (惠州比亚迪电池有限公司), part of BYD's FinDreams (弗迪) battery arm, is … |
| BYD FinDreams Changzhou plant | BYD (Changzhou / East China base) | China | 0.4 | N | Could not confirm a FinDreams (弗迪电池) battery CELL plant in Changzhou. BYD's Changzhou site… |
| Ford-LG Kocaeli (Ford / LG Energy Solution / Koç Holding battery cell JV — cancelled) | Ford Otosan | Turkey | 0.4 | Y | CANCELLED PROJECT. Announced 21 Feb 2023 as a non-binding MOU between Ford, LG Energy Solu… |
| JSW Energy Cell Gigafactory | JSW Energy | India | 0.4 | Y | Announced-stage Li-ion battery CELL manufacturing plan by JSW (JSW Group, via JSW Energy /… |
| Sodium Batteries Australia pilot manufacturing facility | Sodium Batteries Australia | Australia | 0.4 | Y | Sodium Batteries Australia describes itself as a sovereign Australian manufacturer of sodi… |
| Peak Energy Sacramento | Peak Energy | United States | 0.4 | N | NOT a cell manufacturer — out of scope for a battery-cell database. Announced 9 July 2026,… |
| Deligreen Shanghai Cylindrical Cell Plant | Shanghai Deligreen Power | China | 0.4 | Y | Best real-world match for the candidate is 上海德朗能动力电池有限公司 (Shanghai DLG Power Battery Co., … |
| Farasis Wuhu plant | Farasis Energy | China | 0.45 | Y | Announced Aug/Sep 2021: Farasis Energy signed an investment cooperation agreement with the… |
| Ritto film battery pilot line | Sekisui Chemical | Japan | 0.45 | N | MISCLASSIFICATION — this is NOT a battery cell plant. The "Ritto film battery pilot line" … |
| Cheonan Plant | EIG (Energy Innovation Group Ltd.) | South Korea | 0.45 | Y | EIG (Energy Innovation Group Ltd.) is a South Korean manufacturer of large-format pouch li… |
| Toyota Teiho Plant | Toyota Motor Corporation | Japan | 0.45 | Y | The Teiho Plant is Toyota's production-engineering / "startup" hub in Teihocho, Toyota Cit… |
| Statevolt Imperial Valley Gigafactory | Statevolt | United States | 0.45 | Y | Statevolt (founder/CEO Lars Carlstrom, also behind the collapsed Britishvolt and Italvolt … |
| Nandu Power (Narada) Hangzhou/Fuyang Lithium Cell Base | Narada Power (Nandu Power) | China | 0.45 | Y | Nandu Power = Narada Power (Zhejiang Narada Power Source Co., Ltd., SZSE 300068), HQ in Fu… |

## Appendix — non-cell sites flagged by researchers (24)

Kept in the DB and tagged `is_cell_manufacturer = false`. Filter these out for a pure cell-manufacturing view; they are pack-assembly, material or corporate-HQ entries surfaced by the wide-net seed list.

| plant | operator | country | why flagged (note excerpt) |
|---|---|---|---|
| EVE Energy Wuhan plant (Wuhan R&D Branch / Energy Storage Institute) | EVE Energy | China | EVE Energy's Wuhan presence is an R&D facility, NOT a battery cell manufacturing plant. Two related establishm… |
| SVOLT Taizhou plant | SVOLT (Honeycomb Energy) | China | The SVOLT "Taizhou plant" is a battery module/pack ASSEMBLY facility co-located with Great Wall Motor's Taizho… |
| Sunwoda Shenzhen plant | Sunwoda | China | COULD NOT VERIFY VIA LIVE SOURCES. This session had no working web access: the WebSearch budget was fully exha… |
| BYD FinDreams Changzhou plant | BYD (Changzhou / East China base) | China | Could not confirm a FinDreams (弗迪电池) battery CELL plant in Changzhou. BYD's Changzhou site (华东/East China base… |
| Ganfeng LiEnergy Dongguan Base (赣锋锂电东莞科技 10GWh new-type lithium battery & ESS HQ base) | Ganfeng LiEnergy | China | Located in Machong town (麻涌镇), Dongguan, Guangdong. Entity: 赣锋锂电(东莞)科技有限公司, a subsidiary of Ganfeng LiEnergy (… |
| Liacon Itzehoe | Liacon | Germany | Itzehoe is Liacon GmbH's registered HQ and R&D base (co-located with Fraunhofer ISIT, from which Liacon spun o… |
| Altris Sandviken (Ferrum) | Altris | Sweden | Altris Sandviken, branded the "Ferrum" facility, is a CATHODE MATERIAL plant, NOT a battery cell manufacturing… |
| Ritto film battery pilot line | Sekisui Chemical | Japan | MISCLASSIFICATION — this is NOT a battery cell plant. The "Ritto film battery pilot line" is Sekisui Chemical'… |
| Nonsan Plant | Vitzrocell | South Korea | Could not confirm the existence of any Vitzrocell plant in Nonsan. Vitzrocell (KRX:082920) is a lithium PRIMAR… |
| Durapower Singapore | Durapower | Singapore | Durapower Holdings is a Singapore-headquartered lithium-ion battery maker (founded 2009; HQ at 10 Kallang Sect… |
| StB Giga Factory | StB Giga Factory, Inc. | Philippines | Located at Filinvest Innovation Park, New Clark City, Tarlac, Philippines. Australia–China JV between StB Capi… |
| Narada Wuxi LFP cell plant | Narada Power | China | Could NOT confirm any Narada Power battery CELL manufacturing plant in Wuxi. The only Narada-Wuxi link found i… |
| Naxion Energy Coimbatore Plant | Naxion Energy | India | IMPORTANT SCOPE MISMATCH: The candidate names a "Naxion Sodium-Ion Cell Plant (Coimbatore)", but the Coimbator… |
| LG Energy Solution Morocco | LG Energy Solution | Morocco | No confirmed battery CELL manufacturing site for LG Energy Solution exists in Morocco. As of July 2024, LGES w… |
| Energy Renaissance Tomago (Renaissance One) | Energy Renaissance | Australia | Site at Tomago, NSW, Australia ("Renaissance One", ~4,500 sqm). Operational since 2022. IMPORTANT: as currentl… |
| PowerCap Queensland | PowerCap | Australia | PowerCap is a Brisbane / south-east Queensland based sodium-ion battery company. Multiple reputable sources (p… |
| Addionics Israel pilot line | Addionics | Israel | NOT a battery cell manufacturer. Addionics is an Israeli startup (founded 2018) that produces "Smart 3D Electr… |
| Samsung SDI Giheung Plant | Samsung SDI | South Korea | Giheung (150-20 Gongse-ro, Giheung-gu, Yongin-si, Gyeonggi-do) is Samsung SDI's corporate headquarters and R&D… |
| SVOLT Thailand (Sriracha) | SVOLT Energy Technology (Thailand) | Thailand | This Sriracha (Chonburi) site is a battery MODULE and PACK ASSEMBLY plant, NOT a cell manufacturing facility -… |
| NV Gotion Thailand (Rayong) | NV Gotion Co., Ltd. | Thailand | NOT a cell manufacturer. NV Gotion's Rayong plant (Siam Eastern Industrial Park 2, Pluak Daeng, Rayong, Thaila… |
| Amprius Colorado (Brighton) | Amprius Technologies | United States | CANCELLED — never built. Announced March 2023: Amprius Technologies selected Brighton, Colorado for its first … |
| Peak Energy Sacramento | Peak Energy | United States | NOT a cell manufacturer — out of scope for a battery-cell database. Announced 9 July 2026, this 183,000 sq ft … |
| SES AI Woburn | SES AI | United States | SES AI's Woburn, MA site is the company's global headquarters and human R&D centre, home to its "Electrolyte F… |
| Sunwoda Maoming (Dianbai) automotive electronics base | Sunwoda | China | This site is NOT a battery cell plant. The Sunwoda base in Dianbai district, Maoming (Guangdong) is an automot… |
