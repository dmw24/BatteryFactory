# Battery Gigafactory Database — QA report

Generated from `factories.db`. Total rows: **553**. Confirmed cell manufacturers: **345**. Flagged non-cell (pack/material/recycling, kept and tagged): **7**.

> Capacity is annual GWh/year at nameplate. Totals are grouped by status and are **never summed across statuses** — announced, under-construction and operational capacity are distinct and must not be added together.


## 4. Totals by status (capacity never summed across status)

Active, comparable cell plants only (view `factories_active`: excludes non-cell rows, paused/cancelled projects and non-comparable long-duration chemistries, D-019).

| status | plants | Σ nameplate GWh/yr | Σ sourced installed GWh/yr |
|---|---:|---:|---:|
| operational | 305 | 6840.0 | 3235.0 |
| announced | 87 | 1043.0 | — |
| under_construction | 77 | 1731.0 | — |
| (unknown) | 18 | 6.0 | — |

### Paused and cancelled projects (excluded from the totals above)

| project_state | furthest status | plants | Σ nameplate GWh/yr (not counted) |
|---|---|---:|---:|
| cancelled | (unknown) | 1 | — |
| cancelled | announced | 12 | 161.0 |
| cancelled | operational | 7 | 2.0 |
| cancelled | under_construction | 6 | 95.0 |
| paused | announced | 6 | 125.0 |
| paused | operational | 11 | 39.0 |
| paused | under_construction | 9 | 195.0 |

### Region × status matrix

| region | status | plants | Σ nameplate GWh/yr |
|---|---|---:|---:|
| China | (unknown) | 7 | 3.0 |
| China | announced | 57 | 797.0 |
| China | operational | 202 | 5683.0 |
| China | under_construction | 47 | 1015.0 |
| Europe | (unknown) | 4 | 2.0 |
| Europe | announced | 9 | 75.0 |
| Europe | operational | 26 | 369.0 |
| Europe | under_construction | 13 | 328.0 |
| India | (unknown) | 1 | — |
| India | announced | 10 | 81.0 |
| India | operational | 5 | 33.0 |
| India | under_construction | 5 | 91.0 |
| Japan | (unknown) | 2 | 1.0 |
| Japan | announced | 2 | 16.0 |
| Japan | operational | 19 | 43.0 |
| Japan | under_construction | 1 | 20.0 |
| Rest of World | announced | 4 | 51.0 |
| Rest of World | operational | 7 | 59.0 |
| Rest of World | under_construction | 2 | 110.0 |
| South Korea | (unknown) | 1 | — |
| South Korea | operational | 9 | 68.0 |
| Southeast Asia | announced | 1 | — |
| Southeast Asia | operational | 14 | 108.0 |
| Southeast Asia | under_construction | 2 | 6.0 |
| USA | (unknown) | 3 | 0.0 |
| USA | announced | 4 | 24.0 |
| USA | operational | 23 | 477.0 |
| USA | under_construction | 7 | 162.0 |

## 1. Suspected duplicate sites (92 pairs/groups)

Review these — they may be the same physical site under different names, or legitimately distinct sites of the same operator.

| signal | plants | ids |
|---|---|---|
| same coordinates ~(36.6, 101.8) | Agricultural Development Holding (Beijing) Xining Nanchuan 6 GWh rare-earth lithium battery and PACK project ⟷ BYD FinDreams Xining plant (Qinghai FinDreams Battery Co., Ltd.) ⟷ CATL Xining plant (Qinghai Times New Energy Technology Co., Ltd.) | agricultural-development-holding-beijing-xining-nanchuan-6gwh-rare-earth-lithium-battery-and-pack-project-china, byd-byd-findreams-xining-plant-qinghai-findreams-battery-co-ltd-china, catl-catl-xining-plant-qinghai-times-new-energy-technology-co-ltd-china |
| same coordinates ~(23.0, 113.7) | ATL Dongguan cell plant ⟷ Easton Sodium-ion Cell Plant Dongguan (Songshan Lake) ⟷ Ganfeng LiEnergy Dongguan Base (赣锋锂电东莞科技 10GWh new-type lithium battery & ESS HQ base) | amperex-technology-limited-atl-dongguan-cell-plant-china, easton-east-group-easton-sodium-ion-cell-plant-dongguan-songshan-lake-china, ganfeng-lienergy-ganfeng-lienergy-dongguan-base-10gwh-new-type-lithium-battery-ess-hq-base-china |
| same coordinates ~(37.5, -122.0) | Amprius Fremont ⟷ Enovix Fremont (Fab-1) | amprius-technologies-amprius-fremont-united-states, enovix-enovix-fremont-fab-1-united-states |
| same coordinates ~(30.0, 103.8) | Guoke Energy (Sichuan) Meishan 20 GWh ESS cell project ⟷ CALB Meishan power battery and energy storage base (Pengshan, Meishan, Sichuan) | anhui-guoke-energy-guoke-energy-sichuan-meishan-china, calb-calb-meishan-power-battery-and-energy-storage-base-pengshan-meishan-sichuan-china |
| same coordinates ~(30.9, 119.4) | Anhui Qingna Energy Guangde large-cylindrical sodium-ion base ⟷ Great Power Guangde plant ⟷ Zoolnasm (Zhongna Energy) Guangde sodium-ion battery base | anhui-qingna-energy-guangde-sodium-ion-base-china, great-power-great-power-guangde-plant-china, zoolnasm-zhongna-energy-zoolnasm-zhongna-energy-guangde-sodium-ion-battery-base-china |
| same coordinates ~(31.7, 115.9) | Anhui Volt Era (伏特时代) Jinzhai 10 GWh semi-solid / solid-state battery project ⟷ Jinzhai Gotion storage cell base (Lu'an, Anhui) | anhui-volt-era-new-energy-volt-era-jinzhai-semi-solid-battery-base-china, gotion-jinzhai-gotion-new-energy-jinzhai-storage-cell-base-china |
| same coordinates ~(30.5, 117.0) | Anhui Yichuang Energy Anqing 20 GWh power battery project (Anqing Economic and Technological Development Zone) ⟷ Chaowei Anqing Chaoren Sodium-Ion Battery Plant (Phase I) ⟷ Guoke Energy Anqing base (phase 1 running, phase 2 5 GWh storage cell line) | anhui-yichuang-energy-technology-yichuang-anqing-20gwh-power-battery-project-china, anqing-chaoren-energy-technology-co-ltd-chaowei-anqing-chaoren-sodium-ion-battery-plant-phase-i-china, guoke-energy-guoke-energy-anqing-base-china |
| same coordinates ~(31.0, 118.8) | Anhui Yijiatong (EIKTO) Xuancheng cell plant ⟷ Ningguo Times New Energy - Geely Ningguo 12 GWh power battery plant (Ningguo Economic Development Zone, Xuancheng, Anhui) | anhui-yijiatong-battery-eikto-xuancheng-plant-china, ningguo-times-new-energy-ningguo-12gwh-power-battery-plant-china |
| same coordinates ~(34.8, 113.6) | BAK Zhengzhou Plant ⟷ BYD FinDreams (Fudi) Zhengzhou battery plant | bak-battery-bak-zhengzhou-plant-china, byd-findreams-battery-zhengzhou-fudi-battery-co-ltd-byd-findreams-fudi-zhengzhou-battery-plant-china |
| same coordinates ~(31.8, 120.0) | BAK Battery Changzhou large-cylindrical base ⟷ CALB Changzhou (Jintan) battery base ⟷ Cubenergy Changzhou energy storage intelligent manufacturing base (15 GWh) ⟷ EnerVenue Changzhou ⟷ Great Power Changzhou plant ⟷ Beijing BESK Technology (BEST) Changzhou battery plant (SK / BAIC JV) | bak-battery-changzhou-large-cylindrical-base-china, calb-calb-changzhou-jintan-battery-base-china, cubenergy-cubenergy-changzhou-energy-storage-intelligent-manufacturing-base-china, enervenue-enervenue-changzhou-china, great-power-great-power-changzhou-plant-china, sk-on-beijing-besk-changzhou-battery-plant-china |
| same coordinates ~(22.5, 114.1) | BAK Shenzhen Plant (BAK Industrial Park) ⟷ BYD FinDreams Shenzhen plant (Kengzi/Pingshan base) ⟷ Shenzhen BetterPower Shenzhen Plant (Longhua base) ⟷ Zhuoneng Shenzhen Plant ⟷ Sunwoda Shenzhen plant | bak-battery-shenzhen-bak-power-battery-bak-shenzhen-plant-bak-industrial-park-china, findreams-battery-byd-byd-findreams-shenzhen-plant-kengzi-pingshan-base-china, shenzhen-betterpower-battery-co-ltd-shenzhen-betterpower-shenzhen-plant-longhua-base-china, shenzhen-zhuoneng-new-energy-co-ltd-zhuoneng-shenzhen-plant-china, sunwoda-sunwoda-shenzhen-plant-china |
| same coordinates ~(30.9, 120.1) | WeLion New Energy Huzhou Semi-Solid Plant ⟷ JEVE (捷威动力) Changxing (Huzhou) 12 GWh battery base ⟷ Microvast Huzhou Plant ⟷ SVOLT Huzhou plant (South Taihu New Area) ⟷ Tianneng Changxing (South Taihu) Lithium Battery Base | beijing-welion-new-energy-welion-new-energy-huzhou-semi-solid-plant-china, jeve-jeve-changxing-huzhou-battery-base-china, microvast-power-systems-huzhou-co-ltd-microvast-huzhou-plant-china, svolt-honeycomb-energy-svolt-huzhou-plant-south-taihu-new-area-china, tianneng-new-energy-huzhou-co-ltd-zhejiang-tianneng-energy-storage-co-tianneng-changxing-south-taihu-lithium-battery-base-china |
| same coordinates ~(23.1, 114.4) | BYD FinDreams Huizhou plant ⟷ EVE Energy Huizhou plant (Zhongkai High-tech Zone production base) ⟷ EVE Sodium Energy HQ and manufacturing base (Huizhou) ⟷ EVE Energy Huizhou Zhongkai 60GWh energy storage (power) battery project ⟷ Desay Huizhou Plant (consumer soft-pack cell project) ⟷ Highpower International Huizhou Plant (Longhu/Tonghu Industrial Park) ⟷ Sunwoda Huizhou plant (Huizhou Liwei New Energy) ⟷ Kexiang Sodium Energy Industrial Park, 8 GWh sodium-ion energy storage battery project (Daya Bay, Huizhou) | byd-findreams-byd-findreams-huizhou-plant-china, eve-energy-eve-energy-huizhou-plant-zhongkai-high-tech-zone-production-base-china, eve-energy-eve-sodium-energy-huizhou-hq-china, eve-energy-huizhou-tonghu-zhongkai-60gwh-china, huizhou-desay-battery-co-ltd-desay-huizhou-plant-consumer-soft-pack-cell-project-china, huizhou-highpower-technology-highpower-international-huizhou-plant-longhu-tonghu-industrial-park-china, huizhou-liwei-new-energy-technology-co-ltd-sunwoda-sunwoda-huizhou-plant-huizhou-liwei-new-energy-china, kexiang-kexiang-daya-bay-8gwh-sodium-ion-energy-storage-battery-project-china |
| same coordinates ~(30.7, 104.1) | CALB Chengdu plant (Sichuan base) ⟷ EVE Energy Chengdu power and energy storage battery base ⟷ SVOLT Chengdu plant (Chengdu Eastern New Area base) | calb-calb-chengdu-plant-sichuan-base-china, eve-energy-eve-energy-chengdu-power-and-energy-storage-battery-base-china, svolt-energy-technology-honeycomb-energy-svolt-chengdu-plant-chengdu-eastern-new-area-base-china |
| same coordinates ~(31.9, 117.3) | CALB Hefei plant (Changfeng/Xiatang battery base) ⟷ Gotion Hefei plant (VW unified/standard cell base, Xinzhan district) ⟷ Pylontech Hefei Feixi LFP cell plant (10GWh lithium battery R&D and manufacturing base) | calb-calb-hefei-plant-changfeng-xiatang-battery-base-china, hefei-gotion-high-tech-power-energy-co-ltd-gotion-hefei-plant-vw-unified-standard-cell-base-xinzhan-district-china, pylontech-pylon-technologies-pylontech-hefei-feixi-lfp-cell-plant-10gwh-lithium-battery-r-d-and-manufacturing-base-china |
| same coordinates ~(30.6, 114.3) | CALB Wuhan Base (Zhonghang Xinhang Wuhan power and energy storage battery base) ⟷ Chuneng New Energy Wuhan Base ⟷ HiNa Battery Wuhan Jiangxia 10 GWh sodium-ion production base | calb-calb-wuhan-base-zhonghang-xinhang-wuhan-power-and-energy-storage-battery-base-china, chuneng-new-energy-wuhan-base-china, hina-battery-hina-wuhan-jiangxia-sodium-ion-base-china |
| same coordinates ~(24.5, 118.1) | CALB Xiamen battery base ⟷ CATL Xiamen battery base (Xiamen Times New Energy) ⟷ CATL Xiamen Times high-performance lithium battery project (Tongxiang, Dongliao section) ⟷ Hithium Xiamen plant (Xiamen production base) | calb-calb-xiamen-battery-base-china, catl-catl-xiamen-battery-base-xiamen-times-new-energy-china, catl-catl-xiamen-times-high-performance-lithium-battery-project-china, hithium-hithium-xiamen-plant-xiamen-production-base-china |
| same coordinates ~(32.0, 112.1) | Camel Xiangyang New Energy Low-Carbon Industrial Park ⟷ FinDreams Xiangyang battery plant | camel-group-camel-xiangyang-new-energy-low-carbon-industrial-park-china, xiangyang-findreams-battery-findreams-xiangyang-battery-plant-china |
| same coordinates ~(47.5, 21.6) | CATL Debrecen ⟷ EVE Energy Debrecen | catl-catl-debrecen-hungary, eve-energy-eve-power-hungary-kft-eve-energy-debrecen-hungary |
| same coordinates ~(31.4, 119.5) | CATL Liyang plant (Jiangsu Contemporary Amperex Technology) ⟷ Times SAIC (时代上汽) power battery plant, Liyang | catl-catl-liyang-plant-jiangsu-contemporary-amperex-technology-china, times-saic-power-battery-liyang-plant-china |
| same coordinates ~(31.2, 121.5) | CATL Shanghai Lingang battery base (Nanhui New City) ⟷ Pylontech Shanghai LFP cell base ⟷ Deligreen Shanghai Cylindrical Cell Plant | catl-catl-shanghai-lingang-battery-base-nanhui-new-city-china, pylontech-pylon-technologies-co-ltd-pylontech-shanghai-lfp-cell-base-china, shanghai-deligreen-power-deligreen-shanghai-cylindrical-cell-plant-china |
| same coordinates ~(28.8, 104.6) | CATL Yibin power battery base ⟷ Pengcheng Wuxian Yibin Energy Storage Cell Base | catl-catl-yibin-power-battery-base-china, pengcheng-wuxian-new-energy-technology-sichuan-co-ltd-pengcheng-wuxian-yibin-energy-storage-cell-base-china |
| same coordinates ~(27.8, 114.4) | CATL Yichun battery production base ⟷ Yichun Gotion Battery plant | catl-catl-yichun-battery-production-base-china, yichun-gotion-yichun-gotion-battery-plant-china |
| same coordinates ~(23.0, 112.5) | CATL Zhaoqing plant ⟷ Fenghua New Energy Zhaoqing cell plant (Duanzhou; polymer and aluminium-shell consumer cells) | catl-catl-zhaoqing-plant-china, guangdong-fenghua-new-energy-fenghua-zhaoqing-cell-plant-china |
| same coordinates ~(48.5, 9.1) | Cellforce Kirchentellinsfurt ⟷ Customcells Tübingen | cellforce-group-cellforce-kirchentellinsfurt-germany, customcells-customcells-t-bingen-germany |
| same coordinates ~(28.3, 112.6) | BYD FinDreams Changsha plant (Ningxiang) ⟷ Shengxi Technology Ningxiang lithium battery base | changsha-findreams-battery-findreams-battery-byd-findreams-changsha-plant-ningxiang-china, zhejiang-shengxi-technology-ningxiang-base-china |
| same coordinates ~(31.4, 118.4) | Chery Wuhu all-solid-state battery line (first 1.25 GWh line) ⟷ Farasis Wuhu plant ⟷ Wuhu Gotion 20GWh New Energy Battery Base (Gotion Wuhu plant) ⟷ Rongjie Energy Wuhu Cell Plant (Wuhu Tianyi Energy / ETC Battery) | chery-automobile-deyi-wuhu-all-solid-state-battery-line-china, farasis-energy-farasis-wuhu-plant-china, wuhu-gotion-power-technology-co-ltd-wuhu-gotion-20gwh-new-energy-battery-base-gotion-wuhu-plant-china, wuhu-tianyi-energy-technology-co-ltd-etc-battery-rongjie-energy-wuhu-cell-plant-wuhu-tianyi-energy-etc-battery-china |
| same coordinates ~(29.6, 105.1) | Chuanhong New Energy Southwest Battery Production Base (Longchang, Neijiang) ⟷ Haisida Sodium Star (Naxing) Neijiang 6 GWh sodium-ion base (海四达钠星) | chuanhong-new-energy-chuanhong-longchang-neijiang-southwest-battery-base-china, haisida-sodium-star-haisida-naxing-neijiang-sodium-ion-plant-china |
| same coordinates ~(30.7, 111.3) | Chuneng New Energy Yichang Base (Yiling, Longquan) ⟷ Envision AESC Yichang storage super factory ⟷ Sunwoda Yichang power battery production base | chuneng-new-energy-yichang-base-china, envision-aesc-envision-aesc-yichang-storage-super-factory-china, sunwoda-sunwoda-yichang-power-battery-production-base-china |
| same coordinates ~(53.9, 9.5) | Customcells Itzehoe ⟷ Liacon Itzehoe | customcells-customcells-itzehoe-germany, liacon-liacon-itzehoe-germany |
| same coordinates ~(22.8, 108.3) | DFD Nanning Plant (Guangxi Ningfu New Energy, 20GWh lithium battery project) ⟷ FinDreams Guangxi battery plant (广西弗迪电池) | dfd-new-energy-guangxi-ningfu-new-energy-technology-co-ltd-dfd-nanning-plant-guangxi-ningfu-new-energy-20gwh-lithium-battery-project-china, guangxi-findreams-battery-findreams-guangxi-battery-plant-china |
| same coordinates ~(39.5, -119.8) | Dragonfly Energy Reno ⟷ Lyten Reno Lithium-Sulfur Gigafactory | dragonfly-energy-dragonfly-energy-reno-united-states, lyten-lyten-reno-lithium-sulfur-gigafactory-united-states |
| same coordinates ~(13.0, 77.6) | e-TRNL Cell Pilot Line (Bengaluru) ⟷ Exide Energy Solutions Bengaluru Gigafactory ⟷ International Battery Company Bengaluru Gigafactory ⟷ Log9 Materials Bengaluru Cell Facility | e-trnl-energy-e-trnl-cell-pilot-line-bengaluru-india, exide-energy-solutions-exide-energy-solutions-bengaluru-gigafactory-india, international-battery-company-international-battery-company-bengaluru-gigafactory-india, log9-materials-log9-materials-bengaluru-cell-facility-india |
| same coordinates ~(38.9, 100.5) | Easton (EAST Group) Zhangye sodium-ion cell plant (new energy-storage equipment demonstration project, Phase II) ⟷ Jueshi New Energy Zhangye 5 GWh sodium-ion battery manufacturing project (Zhangye Economic and Technological Development Zone) | easton-east-group-easton-zhangye-sodium-ion-cell-plant-china, jueshi-new-energy-jueshi-zhangye-5gwh-sodium-ion-battery-project-china |
| same coordinates ~(36.8, 127.2) | Cheonan Plant ⟷ Samsung SDI Cheonan Plant | eig-energy-innovation-group-ltd-cheonan-plant-south-korea, samsung-sdi-samsung-sdi-cheonan-plant-south-korea |
| same coordinates ~(32.3, 118.3) | Enli Power Anhui Fengyang 2 GWh solid-state / semi-solid battery base (Chuzhou) ⟷ Gotion New Energy (Chuzhou) high-end manufacturing base ⟷ Phylion Chuzhou Plant ⟷ Lishen Chuzhou base (Quanjiao) ⟷ Trina Storage Chuzhou LFP cell gigafactory | enli-power-enli-anhui-fengyang-solid-state-battery-base-china, gotion-chuzhou-gotion-new-energy-power-co-ltd-gotion-new-energy-chuzhou-high-end-manufacturing-base-china, phylion-battery-xingheng-power-phylion-chuzhou-plant-china, tianjin-lishen-battery-lishen-chuzhou-base-quanjiao-china, trina-storage-trina-storage-chuzhou-lfp-cell-gigafactory-china |
| same coordinates ~(54.9, -1.4) | AESC Sunderland Plant 1 (original gigafactory) ⟷ Envision AESC Sunderland Gigafactory | envision-aesc-aesc-sunderland-plant-1-united-kingdom, envision-aesc-envision-aesc-sunderland-gigafactory-united-kingdom |
| same coordinates ~(39.6, 109.8) | Envision AESC Ordos Plant (Ordos-Envision Net Zero Industrial Park) ⟷ Jianheng Aoneng Dalate Banner sodium-ion battery base (Ordos supply-chain area) ⟷ Ordos Juungar Banner sodium-ion battery and energy storage industrial park (Juungar Economic Development Zone) ⟷ Tianpu Technology Ordos lithium-ion battery and system intelligent manufacturing project (50 GWh) | envision-aesc-envision-aesc-ordos-plant-ordos-envision-net-zero-industrial-park-china, inner-mongolia-jianheng-aoneng-technology-jianheng-aoneng-dalate-sodium-ion-base-china, inner-mongolia-xinjing-new-energy-technology-ordos-juungar-sodium-ion-park-china, tianpu-technology-tianpu-ordos-lithium-ion-battery-and-system-project-china |
| same coordinates ~(31.0, 112.2) | EVE Energy Jingmen production base ⟷ EVE Power Jingmen (Shayang) 60GWh power and storage battery project | eve-energy-eve-energy-jingmen-production-base-china, eve-energy-jingmen-shayang-60gwh-power-storage-china |
| same coordinates ~(29.9, 121.5) | EVE Energy Ningbo plant ⟷ Veken Ningbo sodium-ion plant | eve-energy-eve-energy-ningbo-plant-china, veken-technology-veken-ningbo-sodium-ion-plant-china |
| same coordinates ~(31.8, 121.7) | EVE Energy Qidong plant (EVE-Linyang) ⟷ Highstar Qidong Plant | eve-energy-eve-energy-qidong-plant-eve-linyang-china, jiangsu-highstar-battery-manufacturing-co-ltd-highstar-battery-highstar-qidong-plant-china |
| same coordinates ~(5.4, 100.6) | EVE Energy Malaysia (Kulim, Kedah) ⟷ Highstar Malaysia Tabless Cell Base (Kulim) | eve-energy-malaysia-sdn-bhd-eve-energy-malaysia-kulim-kedah-malaysia, jiangsu-highstar-battery-manufacturing-co-ltd-highstar-malaysia-tabless-cell-base-kulim-malaysia |
| same coordinates ~(13.4, 101.0) | EVLOMO Nong Yai Battery Plant ⟷ Sunwoda Chonburi cell plant | evlomo-evlomo-nong-yai-battery-plant-thailand, sunwoda-automotive-energy-thailand-sunwoda-chonburi-cell-plant-thailand |
| same coordinates ~(23.1, 113.2) | Farasis Energy Guangzhou Super Factory (30 GWh power battery base) ⟷ Great Power Guangzhou (Panyu) plant ⟷ Greater Bay Technology Nansha Plant ⟷ Inpower Panyu Intelligent Manufacturing Base (GAC smart-connected NEV park, Panyu, Guangzhou) | farasis-energy-farasis-energy-guangzhou-super-factory-30-gwh-power-battery-base-china, great-power-great-power-guangzhou-panyu-plant-china, greater-bay-technology-guangzhou-juwan-technology-research-greater-bay-technology-nansha-plant-china, inpower-battery-inpower-panyu-intelligent-manufacturing-base-china |
| same coordinates ~(43.9, 125.3) | FAW-FinDreams Changchun plant (一汽弗迪 Changchun power battery base) ⟷ Dongchi New Energy Jilin Solid-State Plant | faw-findreams-new-energy-technology-co-ltd-faw-findreams-changchun-plant-changchun-power-battery-base-china, jilin-dongchi-new-energy-technology-co-ltd-dongchi-new-energy-jilin-solid-state-plant-china |
| same coordinates ~(34.7, 137.5) | Washizu Plant (Kosai) ⟷ Toyota Battery (PEVE) Kosai Plant | fdk-energy-co-ltd-fdk-corporation-washizu-plant-kosai-japan, toyota-battery-co-ltd-formerly-primearth-ev-energy-peve-toyota-battery-peve-kosai-plant-japan |
| same coordinates ~(29.6, 106.6) | BYD FinDreams Chongqing (Bishan) Blade Battery Plant ⟷ Ganfeng New Lithium Battery Technology Industrial Park (Chongqing) ⟷ Hithium Chongqing plant ⟷ REPT Battero Chongqing plant ⟷ Talent New Energy Chongqing Solid-State Plant ⟷ CosMX Chongqing Plant | findreams-battery-co-ltd-byd-findreams-chongqing-bishan-blade-battery-plant-china, ganfeng-lienergy-ganfeng-new-lithium-battery-technology-industrial-park-chongqing-china, hithium-hithium-chongqing-plant-china, rept-battero-rept-battero-chongqing-plant-china, talent-new-energy-talent-new-energy-chongqing-solid-state-plant-china, zhuhai-cosmx-battery-cosmx-chongqing-plant-china |
| same coordinates ~(39.9, 32.9) | Ford-LG Kocaeli (Ford / LG Energy Solution / Koç Holding battery cell JV — cancelled) ⟷ Pomega Gigafactory (Polatlı, Ankara) ⟷ YİĞİT AKÜ-Ganfeng gigafactory | ford-otosan-ford-lg-kocaeli-ford-lg-energy-solution-ko-holding-battery-cell-jv-cancelled-turkey, pomega-energy-storage-technologies-pomega-gigafactory-polatl-ankara-turkey, yi-i-t-ak-ganfeng-lienergy-jv-yi-i-t-ak-ganfeng-gigafactory-turkey |
| same coordinates ~(27.8, 114.9) | Ganfeng LiEnergy Fenyi 10 GWh pouch cell and zero-carbon industrial base (Fenyi County, Xinyu) ⟷ Ganfeng LiEnergy Xinyu Plant (Jiangxi New-type Lithium Battery Technology Industrial Park) | ganfeng-lienergy-fenyi-10gwh-pouch-cell-zero-carbon-base-china, ganfeng-lienergy-ganfeng-lienergy-xinyu-plant-jiangxi-new-type-lithium-battery-technology-industrial-park-china |
| same coordinates ~(28.7, 115.9) | Ganfeng LiEnergy Nanchang energy-storage cell base (588Ah line) ⟷ Veken Nanchang Industrial Park (Nanchang Veken sodium battery base) ⟷ Sunwoda Nanchang power battery production base | ganfeng-lienergy-nanchang-ess-cell-base-china, nanchang-veken-battery-co-ltd-veken-nanchang-industrial-park-nanchang-veken-sodium-battery-base-china, sunwoda-sunwoda-nanchang-power-battery-production-base-china |
| same coordinates ~(17.4, 78.5) | Godi Energy Hyderabad Gigafactory ⟷ Naxion Sodium-Ion Cell Pilot Plant (Hyderabad) | godi-india-godi-energy-hyderabad-gigafactory-india, naxion-energy-naxion-sodium-ion-cell-pilot-plant-hyderabad-india |
| same coordinates ~(36.1, 120.4) | Qingdao Gotion Battery plant (Laixi) ⟷ Great Power Qingdao Energy Storage Battery Zero-Carbon Manufacturing Base ⟷ Lishen Qingdao plant (Lishen (Qingdao) New Energy; renamed China Auto New Energy (Qingdao) Battery Technology, "中汽新能", July 2025) | gotion-high-tech-qingdao-gotion-battery-plant-laixi-china, great-power-qingdao-great-power-qingdao-energy-storage-battery-zero-carbon-manufacturing-base-china, lishen-qingdao-new-energy-co-ltd-now-china-auto-new-energy-qingdao-battery-technology-co-ltd-lishen-qingdao-plant-lishen-qingdao-new-energy-renamed-china-auto-new-energy-qingdao-battery-technology-july-2025-china |
| same coordinates ~(33.0, 114.0) | Great Power Zhengyang (Zhumadian) 120Ah cell plant ⟷ Great Power Zhumadian plant (Zhumadian production base) | great-power-great-power-zhengyang-120ah-cell-plant-china, great-power-guangzhou-great-power-energy-technology-co-ltd-penghui-energy-great-power-zhumadian-plant-zhumadian-production-base-china |
| same coordinates ~(24.3, 109.4) | Great Power Liuzhou Smart Energy Storage and Power Battery Manufacturing Base ⟷ Gotion Liuzhou power battery base ⟷ REPT Battero Liuzhou plant | great-power-guangzhou-great-power-energy-technology-great-power-liuzhou-smart-energy-storage-and-power-battery-manufacturing-base-china, liuzhou-gotion-battery-co-ltd-gotion-high-tech-subsidiary-gotion-liuzhou-power-battery-base-china, rept-battero-rept-battero-liuzhou-plant-china |
| same coordinates ~(30.5, 105.6) | Suining sodium-ion battery plant ⟷ SVOLT Suining plant | guangde-qingna-technology-suining-sodium-ion-battery-plant-china, svolt-svolt-energy-technology-svolt-suining-plant-china |
| same coordinates ~(22.3, 113.6) | Highstar Zhuhai Energy Storage Battery Base (Fushan Industrial Park) ⟷ Sunwoda Zhuhai plant ⟷ CosMX Zhuhai Plant (Zhuhai headquarters / polymer lithium-ion battery base) | guangdong-highstar-haisida-power-highstar-zhuhai-energy-storage-battery-base-fushan-industrial-park-china, sunwoda-sunwoda-evb-sunwoda-power-sunwoda-zhuhai-plant-china, zhuhai-cosmx-battery-co-ltd-cosmx-zhuhai-plant-zhuhai-headquarters-polymer-lithium-ion-battery-base-china |
| same coordinates ~(40.8, 111.7) | Guyi New Energy Tumd Left Banner 2.2 GWh high-safety solid-state battery project (Taigemu Town, Hohhot) ⟷ Hohhot 50 GWh sodium-ion battery and energy storage industrial park (Hohhot Economic and Technological Development Zone) | guyi-new-energy-inner-mongolia-technology-guyi-tumd-left-banner-2-2gwh-solid-state-china, inner-mongolia-juneng-zhengxin-energy-storage-technology-hohhot-50gwh-sodium-ion-park-china |
| same coordinates ~(-6.3, 107.3) | HLI Green Power Karawang Battery Cell Plant ⟷ CATL CATIB Karawang Battery Cell Plant | hli-green-power-hli-green-power-karawang-battery-cell-plant-indonesia, pt-contemporary-amperex-technology-indonesia-battery-catib-catl-catib-karawang-battery-cell-plant-indonesia |
| same coordinates ~(55.8, 37.6) | INESIS gigafactory, New Moscow (planned; possibly the second Krasnaya Pakhra plant) ⟷ Rosatom Moscow gigafactory (Krasnaya Pakhra) | inesis-inesis-gigafactory-new-moscow-russia, rosatom-rosatom-moscow-gigafactory-russia |
| same coordinates ~(32.1, 118.8) | Jiangsu Tafel New Energy Nanjing Plant ⟷ Sunwoda Nanjing power battery base (Lishui) ⟷ SVOLT Nanjing plant (Lishui base) | jiangsu-tafel-new-energy-jiangsu-tafel-new-energy-nanjing-plant-china, sunwoda-sunwoda-nanjing-power-battery-base-lishui-china, svolt-svolt-nanjing-plant-lishui-base-china |
| same coordinates ~(33.4, 120.2) | Yuanhang Jinli (Genlead) Yancheng Yandu cell plant ⟷ SKOJ Yancheng battery plant (SK On; formerly SK On–EVE Energy JV) ⟷ SKOY Yancheng battery plant (SK On, wholly owned) ⟷ SVOLT Yancheng plant ⟷ Trina Storage Dafeng base (Yancheng) ⟷ Yaoning New Energy Jianhu (Shanggang) Base | jiangsu-yuanhang-jinli-new-energy-yuanhang-jinli-yancheng-yandu-cell-plant-china, sk-on-skoj-yancheng-battery-plant-sk-on-eve-energy-jv-china, sk-on-skoy-yancheng-battery-plant-china, svolt-svolt-energy-technology-svolt-yancheng-plant-china, trina-storage-trina-storage-dafeng-base-china, yao-ning-new-energy-jianhu-yaoning-new-energy-technology-yaoning-new-energy-jianhu-shanggang-base-china |
| same coordinates ~(31.6, 120.7) | Zenergy new 50 GWh battery base (Changshu High-tech Zone per Jiemian/STCN; English press says Xiangcheng, Suzhou) ⟷ Zenergy Changshu Plant | jiangsu-zenergy-suzhou-xiangcheng-plant-china, jiangsu-zenergy-zenergy-changshu-plant-china |
| same coordinates ~(25.0, 101.5) | Jinglan New Energy Chuxiong sodium-ion base ⟷ Yunnan Junhe Yuanxin Nanhua County (Chuxiong) cell line project, Phase 1 (Laogaoba Industrial Park) | jinglan-new-energy-chuxiong-sodium-ion-base-china, yunnan-junhe-yuanxin-new-energy-nanhua-chuxiong-1gwh-cell-line-china |
| same coordinates ~(42.8, -86.1) | LG Energy Solution Michigan (Holland) ⟷ Natron Energy Holland | lg-energy-solution-michigan-inc-lg-energy-solution-michigan-holland-united-states, natron-energy-natron-energy-holland-united-states |
| same coordinates ~(-38.1, 144.4) | Li-S Energy Geelong (Phase 3) ⟷ Recharge Industries Geelong (Avalon) Gigafactory | li-s-energy-li-s-energy-geelong-phase-3-australia, recharge-industries-recharge-industries-geelong-avalon-gigafactory-australia |
| same coordinates ~(36.3, 127.4) | Daejeon flexible battery pilot ⟷ Daejeon all-solid-state pilot line | libest-daejeon-flexible-battery-pilot-south-korea, sk-on-daejeon-all-solid-state-pilot-line-south-korea |
| same coordinates ~(31.3, 120.6) | Lishen Battery (Suzhou) plant ⟷ Phylion Suzhou Plant (Suzhou manufacturing base) | lishen-battery-suzhou-co-ltd-lishen-battery-suzhou-plant-china, phylion-battery-xingheng-power-co-ltd-phylion-suzhou-plant-suzhou-manufacturing-base-china |
| same coordinates ~(37.3, -121.9) | Lyten San Jose ⟷ QuantumScape San Jose (Eagle Line / QS-0) ⟷ Sakuu Silicon Valley | lyten-lyten-san-jose-united-states, quantumscape-quantumscape-san-jose-eagle-line-qs-0-united-states, sakuu-sakuu-silicon-valley-united-states |
| same coordinates ~(30.3, 120.2) | Nandu Power (Narada) Hangzhou/Fuyang Lithium Cell Base ⟷ Narada Hangzhou Lin'an Plant ⟷ Wanxiang A123 Hangzhou Plant (Wanxiang Innovation Energy City) ⟷ Xinjie Energy (欣界能源) Hangzhou lithium-metal solid-state base | narada-power-nandu-power-nandu-power-narada-hangzhou-fuyang-lithium-cell-base-china, narada-power-zhejiang-narada-power-source-co-ltd-narada-hangzhou-lin-an-plant-china, wanxiang-a123-wanxiang-a123-hangzhou-plant-wanxiang-innovation-energy-city-china, xinjie-energy-xinjie-hangzhou-lithium-metal-solid-state-base-china |
| same coordinates ~(51.0, 2.4) | ProLogium Dunkirk Gigafactory ⟷ Verkor Gigafactory (Bourbourg, Dunkirk) | prologium-prologium-dunkirk-gigafactory-france, verkor-verkor-gigafactory-bourbourg-dunkirk-france |
| same coordinates ~(29.0, 118.9) | Great Power Quzhou energy storage battery base (Quzhou Smart Manufacturing New City) ⟷ Sunwoda Quzhou plant ⟷ Zeekr Golden Brick Quzhou Cell Plant | quzhou-great-power-energy-technology-co-ltd-great-power-quzhou-energy-storage-battery-base-quzhou-smart-manufacturing-new-city-china, sunwoda-sunwoda-quzhou-plant-china, zeekr-vremt-weirui-jidian-factory-zeekr-golden-brick-quzhou-cell-plant-china |
| same coordinates ~(28.0, 120.7) | REPT Battero Wenzhou plant ⟷ BYD FinDreams Wenzhou battery base (Qiaotou, Yongjia) ⟷ Zhejiang Guansheng Dongchi Wenzhou (Ouhai) 4 GWh semi-solid LFP battery base | rept-battero-rept-battero-wenzhou-plant-china, wenzhou-findreams-battery-co-ltd-byd-findreams-wenzhou-battery-base-qiaotou-yongjia-china, zhejiang-guansheng-dongchi-energy-wenzhou-ouhai-semi-solid-lfp-base-china |
| same coordinates ~(37.5, 121.4) | Weichai-FinDreams (Yantai) New Energy Power Industrial Park ⟷ Lihua Power Yantai 46-series large cylindrical battery plant (Huanghai-Bohai New Area) | weichai-findreams-weichai-findreams-yantai-new-energy-power-industrial-park-china, yantai-lihua-power-supply-technology-lihua-huanghai-bohai-large-cylindrical-battery-project-china |
| same coordinates ~(30.8, 120.8) | Zhejiang Dangzhuo Energy anode-free solid-state cell project (Nanhu, Jiaxing) ⟷ Hu Na Energy Sodium-ion Battery and System Project (Jiaxing) | zhejiang-dangzhuo-energy-jiaxing-nanhu-anode-free-solid-state-project-china, zhejiang-hu-na-energy-co-ltd-hu-na-energy-sodium-ion-battery-and-system-project-jiaxing-china |
| same operator + shared location token 'ibaraki' | AESC Ibaraki Plant ⟷ Vehicle Energy Japan Ibaraki plant | aesc-japan-ltd-aesc-group-aesc-ibaraki-plant-japan, vehicle-energy-japan-vehicle-energy-japan-ibaraki-plant-japan |
| same operator + shared location token 'xiamen' | CATL Xiamen battery base (Xiamen Times New Energy) ⟷ CATL Xiamen Times high-performance lithium battery project (Tongxiang, Dongliao section) | catl-catl-xiamen-battery-base-xiamen-times-new-energy-china, catl-catl-xiamen-times-high-performance-lithium-battery-project-china |
| same operator + shared location token 'sunderland' | AESC Sunderland Plant 1 (original gigafactory) ⟷ Envision AESC Sunderland Gigafactory | envision-aesc-aesc-sunderland-plant-1-united-kingdom, envision-aesc-envision-aesc-sunderland-gigafactory-united-kingdom |
| same operator + shared location token 'zhongkai' | EVE Energy Huizhou plant (Zhongkai High-tech Zone production base) ⟷ EVE Energy Huizhou Zhongkai 60GWh energy storage (power) battery project | eve-energy-eve-energy-huizhou-plant-zhongkai-high-tech-zone-production-base-china, eve-energy-huizhou-tonghu-zhongkai-60gwh-china |
| same operator + shared location token 'jingmen' | EVE Energy Jingmen production base ⟷ EVE Power Jingmen (Shayang) 60GWh power and storage battery project | eve-energy-eve-energy-jingmen-production-base-china, eve-energy-jingmen-shayang-60gwh-power-storage-china |
| same operator + shared location token 'qidong' | EVE Energy Qidong plant (EVE-Linyang) ⟷ EVE Energy Qidong 50GWh storage (power) battery base | eve-energy-eve-energy-qidong-plant-eve-linyang-china, eve-energy-qidong-economic-development-zone-50gwh-china |
| same operator + shared location token '60gwh' | EVE Energy Huizhou Zhongkai 60GWh energy storage (power) battery project ⟷ EVE Power Jingmen (Shayang) 60GWh power and storage battery project | eve-energy-huizhou-tonghu-zhongkai-60gwh-china, eve-energy-jingmen-shayang-60gwh-power-storage-china |
| same operator + shared location token 'kulim' | EVE Energy Malaysia (Kulim, Kedah) ⟷ Highstar Malaysia Tabless Cell Base (Kulim) | eve-energy-malaysia-sdn-bhd-eve-energy-malaysia-kulim-kedah-malaysia, jiangsu-highstar-battery-manufacturing-co-ltd-highstar-malaysia-tabless-cell-base-kulim-malaysia |
| same operator + shared location token 'ganzhou' | Farasis Energy Ganzhou plant (30 GWh new energy battery project) ⟷ Farasis Energy Ganzhou original base (赣州基地) | farasis-energy-farasis-energy-ganzhou-plant-30-gwh-new-energy-battery-project-china, farasis-energy-ganzhou-original-base-china |
| same operator + shared location token 'xinyu' | Ganfeng LiEnergy Fenyi 10 GWh pouch cell and zero-carbon industrial base (Fenyi County, Xinyu) ⟷ Ganfeng LiEnergy Xinyu Plant (Jiangxi New-type Lithium Battery Technology Industrial Park) | ganfeng-lienergy-fenyi-10gwh-pouch-cell-zero-carbon-base-china, ganfeng-lienergy-ganfeng-lienergy-xinyu-plant-jiangxi-new-type-lithium-battery-technology-industrial-park-china |
| same operator + shared location token 'zhumadian' | Great Power Zhengyang (Zhumadian) 120Ah cell plant ⟷ Great Power Zhumadian plant (Zhumadian production base) | great-power-great-power-zhengyang-120ah-cell-plant-china, great-power-guangzhou-great-power-energy-technology-co-ltd-penghui-energy-great-power-zhumadian-plant-zhumadian-production-base-china |
| same operator + shared location token 'banner' | Guyi New Energy Tumd Left Banner 2.2 GWh high-safety solid-state battery project (Taigemu Town, Hohhot) ⟷ Jianheng Aoneng Dalate Banner sodium-ion battery base (Ordos supply-chain area) | guyi-new-energy-inner-mongolia-technology-guyi-tumd-left-banner-2-2gwh-solid-state-china, inner-mongolia-jianheng-aoneng-technology-jianheng-aoneng-dalate-sodium-ion-base-china |
| same operator + shared location token 'hohhot' | Guyi New Energy Tumd Left Banner 2.2 GWh high-safety solid-state battery project (Taigemu Town, Hohhot) ⟷ Hohhot 50 GWh sodium-ion battery and energy storage industrial park (Hohhot Economic and Technological Development Zone) | guyi-new-energy-inner-mongolia-technology-guyi-tumd-left-banner-2-2gwh-solid-state-china, inner-mongolia-juneng-zhengxin-energy-storage-technology-hohhot-50gwh-sodium-ion-park-china |
| same operator + shared location token 'banner' | Guyi New Energy Tumd Left Banner 2.2 GWh high-safety solid-state battery project (Taigemu Town, Hohhot) ⟷ Ordos Juungar Banner sodium-ion battery and energy storage industrial park (Juungar Economic Development Zone) | guyi-new-energy-inner-mongolia-technology-guyi-tumd-left-banner-2-2gwh-solid-state-china, inner-mongolia-xinjing-new-energy-technology-ordos-juungar-sodium-ion-park-china |
| same operator + shared location token 'xinzhan' | Gotion Hefei Xinzhan 20GWh power battery project (Hefei Gotion Green Energy) ⟷ Gotion Hefei plant (VW unified/standard cell base, Xinzhan district) | hefei-gotion-green-energy-co-ltd-gotion-hefei-xinzhan-20gwh-power-battery-project-hefei-gotion-green-energy-china, hefei-gotion-high-tech-power-energy-co-ltd-gotion-hefei-plant-vw-unified-standard-cell-base-xinzhan-district-china |
| same operator + shared location token '20gwh' | Gotion Hefei Xinzhan 20GWh power battery project (Hefei Gotion Green Energy) ⟷ Wuhu Gotion 20GWh New Energy Battery Base (Gotion Wuhu plant) | hefei-gotion-green-energy-co-ltd-gotion-hefei-xinzhan-20gwh-power-battery-project-hefei-gotion-green-energy-china, wuhu-gotion-power-technology-co-ltd-wuhu-gotion-20gwh-new-energy-battery-base-gotion-wuhu-plant-china |
| same operator + shared location token 'banner' | Jianheng Aoneng Dalate Banner sodium-ion battery base (Ordos supply-chain area) ⟷ Ordos Juungar Banner sodium-ion battery and energy storage industrial park (Juungar Economic Development Zone) | inner-mongolia-jianheng-aoneng-technology-jianheng-aoneng-dalate-sodium-ion-base-china, inner-mongolia-xinjing-new-energy-technology-ordos-juungar-sodium-ion-park-china |
| same operator + shared location token 'changshu' | Zenergy new 50 GWh battery base (Changshu High-tech Zone per Jiemian/STCN; English press says Xiangcheng, Suzhou) ⟷ Zenergy Changshu Plant | jiangsu-zenergy-suzhou-xiangcheng-plant-china, jiangsu-zenergy-zenergy-changshu-plant-china |

## 2. Capacity double-count / consistency flags (29 rows)

| plant | operator | region | nameplate GWh | flag |
|---|---|---|---:|---|
| CATL Ningde plant (Ningde manufacturing hub) | CATL | China | 500.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| DFD Nanning Plant (Guangxi Ningfu New Energy, 20GWh lithium battery project) | DFD New Energy (Guangxi Ningfu New Energy Technology Co., Ltd.) | China | 20.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Easton Sodium-ion Cell Plant Dongguan (Songshan Lake) | Easton (EAST Group) | China | 0.2 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Eni Storage Systems Gigafactory (Brindisi) | Eni Storage Systems | Europe | 8.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Envision AESC Yichang storage super factory | Envision AESC | China | 100.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| EVE Energy Jingmen production base | EVE Energy | China | 212.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Geely Tonglu power battery project (12 GWh, Tonglu Economic Development Zone; ENERGEE Tonglu base) | Geely Technology Group (吉利科技集团) - ENERGEE (吉曜通行) Tonglu base | China | 12.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Great Power Guangzhou (Panyu) plant | Great Power | China | 2.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Hengdian DMEGC Dongyang Lithium Cell Plant | Hengdian Group DMEGC Magnetics Co., Ltd. | China | 8.5 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Hithium Xiamen plant (Xiamen production base) | Hithium | China | 45.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Zenergy Changshu Plant | Jiangsu Zenergy | China | 70.5 | capacity may be a hub/company-wide aggregate (double-count risk) |
| LG Energy Solution Nanjing (LGESNJ; Plants 6 and 9, Jiangning) | LG Energy Solution (Nanjing) Co., Ltd. | China | 54.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Li-FUN Zhuzhou Plant | Li-FUN Technology | China | 2.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Narada Jiuquan storage cell base (Jiuquan Narada Smart Energy Storage Manufacturing Base) | Narada Power (Jiuquan Narada, wholly-owned subsidiary) | China | 4.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Phylion Suzhou Plant (Suzhou manufacturing base) | Phylion Battery (Xingheng Power Co., Ltd.) | China | 2.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| PowerCo Sagunto (Gigafactory Valencia) | PowerCo | Europe | 29.1 | capacity may be a hub/company-wide aggregate (double-count risk) |
| QingTao Energy Kunshan Semi-Solid Plant | QingTao (Kunshan) Energy | China | 10.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| StarPlus Energy Gigafactory (Kokomo, Indiana) | StarPlus Energy | USA | 33.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Sunwoda Zhuhai plant | Sunwoda (Sunwoda EVB / Sunwoda Power) | China | 30.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Sunwoda Nanjing power battery base (Lishui) | Sunwoda | China | 30.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| SVOLT Chengdu plant (Chengdu Eastern New Area base) | SVOLT Energy Technology (Honeycomb Energy / 蜂巢能源) | China | 31.5 | capacity may be a hub/company-wide aggregate (double-count risk) |
| SVOLT Shangrao Base | SVOLT Energy Technology | China | 24.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| SVOLT Ma'anshan plant | SVOLT (Svolt Energy Technology / 蜂巢能源) | China | 28.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Talent New Energy Chongqing Solid-State Plant | Talent New Energy | China | 2.2 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Lishen Chuzhou base (Quanjiao) | Tianjin Lishen Battery | China | 42.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Tianneng Changxing (South Taihu) Lithium Battery Base | Tianneng New Energy (Huzhou) Co., Ltd. (Zhejiang Tianneng Energy Storage Co.) | China | 10.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Waaree ESS Cell Plant (Rola) | Waaree ESS (Waaree Energy Storage Solutions) | India | 3.5 | capacity may be a hub/company-wide aggregate (double-count risk) |
| WeLion Haibo (Zibo) semi-solid-state / solid-state battery base | WeLion Haibo (Zibo) New Energy Technology Co., Ltd. (卫蓝海博（淄博）新能源科技有限公司) | China | 20.0 | capacity may be a hub/company-wide aggregate (double-count risk) |
| Yichun Gotion Battery plant | Yichun Gotion | China | 30.0 | capacity may be a hub/company-wide aggregate (double-count risk) |

### Live cell sites missing a nameplate figure (58)

Genuine cell plants (operational/under-construction) with no sourced capacity — capacity left null per the no-guessing rule.

| plant | operator | region | status |
|---|---|---|---|
| Saft/ACC Nersac Pilot Plant (Industrial Excellence Center) | ACC (Automotive Cells Company) | Europe | operational |
| APB Fukui Center Takefu Factory (Echizen Plant) | APB Corporation | Japan | operational |
| BAK Zhengzhou Plant | BAK Battery | China | operational |
| Blue Energy Fukuchiyama (Osadano) Plant | Blue Energy Co., Ltd. | Japan | operational |
| CATL Xiamen battery base (Xiamen Times New Energy) | CATL | China | under_construction |
| Cellforce Kirchentellinsfurt | Cellforce Group | Europe | under_construction |
| Chilwee Changxing Lithium Cell Plant | Chilwee (Chaowei Group) | China | operational |
| Customcells Itzehoe | Customcells | Europe | operational |
| Customcells Tübingen | CustomCells | Europe | operational |
| DFD Jiaozuo Plant (Do-Fluoride New Energy, Henan base) | Do-Fluoride New Energy Technology Co., Ltd. (DFD) | China | operational |
| E-One Moli Maple Ridge | E-One Moli Energy (Canada) Ltd. | Rest of World | under_construction |
| e-Zinc Mississauga Pilot Manufacturing Facility | e-Zinc | Rest of World | operational |
| Cheonan Plant | EIG (Energy Innovation Group Ltd.) | South Korea | operational |
| Kawasaki Plant | Eliiy Power | Japan | operational |
| EnerVenue Shelby County | EnerVenue | USA | under_construction |
| Enovix Fremont (Fab-1) | Enovix | USA | operational |
| Eos Energy Turtle Creek | Eos Energy Enterprises | USA | operational |
| ESS Inc Wilsonville | ESS Tech, Inc. (ESS Inc) | USA | operational |
| EVE Energy Huizhou plant (Zhongkai High-tech Zone production base) | EVE Energy | China | operational |
| EVE Energy Ningbo plant | EVE Energy | China | operational |
| Washizu Plant (Kosai) | FDK Energy Co., Ltd. (FDK Corporation) | Japan | operational |
| Gotion New Energy (Chuzhou) high-end manufacturing base | Gotion (Chuzhou Gotion New Energy Power Co., Ltd.) | China | operational |
| Gree Titan Zhuhai LTO Cell Plant | Gree Titan (Gree Titanium New Energy, formerly Yinlong New Energy) | China | operational |
| Coslight Harbin Plant (Harbin Coslight Power lithium battery base) | Harbin Coslight Power Co., Ltd. | China | operational |
| Highpower International Huizhou Plant (Longhu/Tonghu Industrial Park) | Huizhou Highpower Technology | China | operational |
| Sunwoda Huizhou plant (Huizhou Liwei New Energy) | Huizhou Liwei New Energy Technology Co., Ltd. (Sunwoda) | China | operational |
| Highstar Qidong Plant | Jiangsu Highstar Battery Manufacturing Co., Ltd. (Highstar Battery) | China | operational |
| Jiangsu Tafel New Energy Nanjing Plant | Jiangsu Tafel New Energy | China | operational |
| Tianpeng Power Zhangjiagang Cell Plant | Jiangsu Tianpeng Power Supply Co. (Tenpower) | China | operational |
| Daejeon flexible battery pilot | LiBEST | South Korea | operational |
| Lyten San Jose | Lyten | USA | operational |
| Ono Works | Maxell | Japan | operational |
| Murata Yasu Plant | Murata Manufacturing | Japan | operational |
| Nanotech Energy Chico 2 | Nanotech Energy | USA | operational |
| Nandu Power (Narada) Hangzhou/Fuyang Lithium Cell Base | Narada Power (Nandu Power) | China | operational |
| Natron Energy Holland | Natron Energy | USA | operational |
| ONE Circle | Our Next Energy | USA | operational |
| Panasonic Energy Kaizuka Factory | Panasonic Energy Kaizuka Co., Ltd. | Japan | operational |
| PPES Tokushima Plant | Prime Planet Energy & Solutions | Japan | operational |
| QuantumScape San Jose (Eagle Line / QS-0) | QuantumScape | USA | operational |
| Sakuu Silicon Valley | Sakuu | USA | operational |
| Salient Energy Dartmouth | Salient Energy | Rest of World | operational |
| Samsung SDI Cheonan Plant | Samsung SDI | South Korea | operational |
| Suwon S-Line all-solid-state pilot | Samsung SDI | South Korea | operational |
| Shenzhen BetterPower Shenzhen Plant (Longhua base) | Shenzhen BetterPower Battery Co., Ltd | China | operational |
| Zhuoneng Shenzhen Plant | Shenzhen Zhuoneng New Energy Co., Ltd | China | operational |
| Daejeon all-solid-state pilot line | SK On | South Korea | operational |
| Sodium Batteries Australia pilot manufacturing facility | Sodium Batteries Australia | Rest of World | operational |
| Solid Power Louisville EV Cell Pilot Line | Solid Power | USA | operational |
| Sunwoda Quzhou plant | Sunwoda | China | operational |
| TDS Lithium-Ion Battery Gujarat (Hansalpur) | TDS Lithium-Ion Battery Gujarat Pvt Ltd (TDSG) | India | operational |
| Toshiba Kashiwazaki Operations (SCiB) | Toshiba Infrastructure Systems & Solutions Corporation | Japan | operational |
| Toshiba Yokohama Plant (SCiB) | Toshiba Infrastructure Systems & Solutions Corporation | Japan | operational |
| Toyota Battery (PEVE) Kosai Plant | Toyota Battery Co., Ltd. (formerly Primearth EV Energy / PEVE) | Japan | operational |
| Toyota Battery (PEVE) Miyagi Plant | Toyota Battery Co., Ltd. (formerly Primearth EV Energy) | Japan | operational |
| UNIGRID San Diego | UNIGRID Battery | USA | under_construction |
| CosMX Zhuhai Plant (Zhuhai headquarters / polymer lithium-ion battery base) | Zhuhai CosMX Battery Co., Ltd. | China | operational |
| CosMX Chongqing Plant | Zhuhai CosMX Battery | China | operational |

## 3. Rows with confidence < 0.5 (253)

| plant | operator | country | conf | is_cell | note |
|---|---|---|---:|:---:|---|
| 3D (Shaanxi) Battery Zhangjiakou 1 GWh solid-state lithium battery project (Nanshan Automotive Industry Base) | 3D (Shaanxi) Battery Technology Co., Ltd. | China | 0.2 | N | [T042 2026-11-20] NEW (T042 sweep, Hebei). SMM item 2025-04-30: signing ceremony at the Na… |
| BAK Battery Changzhou large-cylindrical base | BAK Battery | China | 0.2 | N | [T009 2026-11-20] Announced Jan 2023 (strategic agreement with Changzhou): 30 GWh large-cy… |
| Chery Wuhu all-solid-state battery line (first 1.25 GWh line) | Chery Automobile | China | 0.2 | N | [T040 2026-11-20] NEW, small and weakly sourced. CarNewsChina 2024-11-19: Chery claims the… |
| Pingdingshan 60 GWh storage and power battery super-factory (Xinhua High-tech Park) | Pingdingshan 60 GWh consortium (China Pingmei Shenma lead) | China | 0.2 | N | [T040 2026-11-20] NEW (Henan). Five parties (China Pingmei Shenma Holding, Zhongyuan Yuzi … |
| Farasis Wuhu plant | Farasis Energy | China | 0.2 | Y | [T009 2026-11-20] Only source is the Aug/Sep 2021 agreement (24 GWh, two sub-projects of 1… |
| Pengcheng New Energy Jinchang 1 GWh lithium-ion cell project (Xugu New Energy Industrial Park) | Hangzhou Pengcheng New Energy Co., Ltd. (杭州鹏程新能源有限公司) | China | 0.2 | N | [T049 2026-11-20] NEW (T049 sweep, Gansu; not in DB). Weak, early-stage add: SMM 2025-03-1… |
| InoBat Ćuprija (Project Lion) | InoBat | Serbia | 0.2 | Y | [T015 2026-11-20] Stalled MoU-stage project; no news after Jan 2024 found (searched Englis… |
| JEVE (捷威动力) Changxing (Huzhou) 12 GWh battery base | JEVE (Tianjin Jiewei Power / 捷威动力) | China | 0.2 | N | [T046 2026-11-20] NEW but STALE. MarkLines teaser (page date 2021-08-02, 'JEVE 12GWh new-e… |
| Kexiang Sodium Energy Industrial Park, 8 GWh sodium-ion energy storage battery project (Daya Bay, Huizhou) | Kexiang Co., Ltd. (科翔股份) | China | 0.2 | N | [T064 2026-11-22] [T064 NEW, Guangdong/Huizhou sweep] CLS 2024-03-19 (S5): Kexiang (科翔股份, … |
| Liacon Itzehoe | Liacon | Germany | 0.2 | N | [T014 2026-11-20] status unconfirmed. No open source shows cell production at Itzehoe: the… |
| Lucas TVS Thervoy Kandigai Cell Plant | Lucas TVS (TVS Indeon Ltd) | India | 0.2 | Y | [T018 2026-11-20] Changed vs v1: under_construction -> announced; v1 start_year 2024 and c… |
| Narada Hangzhou Lin'an Plant | Narada Power (Zhejiang Narada Power Source Co., Ltd.) | China | 0.2 | Y | [T023 2026-11-20] status unconfirmed. Lin'an (Qingshan Lake) is the registered HQ address … |
| Baofeng Energy (宝丰能源) Ningdong lithium battery and energy-storage project (Ningdong Energy and Chemical Base / Su-Yin Industrial Park, Ningxia) | Ningxia Baofeng Group / Baofeng Energy (宁夏宝丰集团 / 宝丰能源) | China | 0.2 | N | [T049 2026-11-20] NEW (T049 sweep, Ningxia; not in DB; the only Ningxia lead found). Bundl… |
| Pingmei Shenma Group Xinxiang Lithium Power (phase II 2 GWh, Fengquan District) | Pingmei Shenma Group (Henan Shenma Group), Xinxiang Lithium Power | China | 0.2 | N | [T047 2026-11-20] NEW (T047 sweep, Henan/Xinxiang). SMM 2019-09-29: launch event for the s… |
| Deligreen Shanghai Cylindrical Cell Plant | Shanghai Deligreen Power | China | 0.2 | Y | [T023 2026-11-20] status unconfirmed. Entity identity (上海德朗能动力电池有限公司 / DLG, Fengxian) rest… |
| Shanxi Guanjia 10 GWh lithium battery production line project (Ying County, Shuozhou) | Shanxi Guanjia New Energy Development Co., Ltd. (山西冠佳新能源发展有限公司) | China | 0.2 | N | [T048 2026-11-20] NEW (T048 sweep, Shanxi). EnergyTrend (English print page; year taken fr… |
| Zhongna Yingdian Xinxiang 2 GWh sodium-ion battery annual production line (Xinxiang Power Supply Industry Development Zone) | Zhongna Yingdian (Shenzhen) New Energy Co., Ltd. | China | 0.2 | N | [T047 2026-11-20] NEW (T047 sweep, Henan/Xinxiang). SMM 2024-05-10: investment cooperation… |
| Bravo Motor Company gigafactory (Colossus Cluster) | Bravo Motor Company Brasil Energy | Brazil | 0.25 | Y | [T020 2026-11-20] Aug 2024 reports (S17, S18): protocol of intent with Bahia/Sao Sebastiao… |
| Banan 15 GWh electrochemical energy-storage full-chain manufacturing base (Chongqing Tegu Industrial Technology Group and two other firms) | Chongqing Tegu Industrial Technology Group Co., Ltd. (重庆特古工业科技集团有限公司) and two unnamed partners | China | 0.25 | N | [T067 2026-11-22] [T067] NEW (Chongqing sweep, Banan district). One article only (S3, Sina… |
| Coslight Harbin Plant (Harbin Coslight Power lithium battery base) | Harbin Coslight Power Co., Ltd. | China | 0.25 | Y | [T021 2026-11-20] status unconfirmed. The only source for v1's 6 GWh / operational claim i… |
| Siheung Plant | Kokam | South Korea | 0.25 | Y | [T019 2026-11-20] Status unconfirmed. Only v1 source was a supplier directory (not re-open… |
| Megamillion Energy gigafactory (Giga-Africa 1) | Megamillion Energy Group | South Africa | 0.25 | Y | [T020 2026-11-20] Giga-Africa 1: Feb 2025 JV announcement with Dr Henry Mao, start at 1 GW… |
| Pomega South Carolina LFP cell factory (Colleton Industrial Campus, near Walterboro) | Pomega Energy Storage Technologies | United States | 0.25 | N | [T044 2026-11-20] Discovery add (T044, USA sweep). Kontrolmatik's US subsidiary Pomega: LF… |
| Pylontech Shanghai LFP cell base | Pylontech (Pylon Technologies Co., Ltd.) | China | 0.25 | Y | [T023 2026-11-20] REVERSED after audit: restored as update (removal withdrawn; S5b only sa… |
| Zhuoneng Shenzhen Plant | Shenzhen Zhuoneng New Energy Co., Ltd | China | 0.25 | Y | [T023 2026-11-20] status unconfirmed. The only evidence is the company's 2016 NEEQ annual … |
| 24M Technologies Cambridge | 24M Technologies | United States | 0.3 | Y | [T016 2026-11-20] Status unconfirmed. v1 0.2 GWh (cited to a Businesswire page it could no… |
| Agricultural Development Holding (Beijing) Xining Nanchuan 6 GWh rare-earth lithium battery and PACK project | Agricultural Development Holding (Beijing) Co., Ltd. (农业发展控股（北京）有限公司) | China | 0.3 | N | [T049 2026-11-20] NEW (T049 sweep, Qinghai; not in DB; not the CATL/Qinghai Times or Zhaor… |
| Amperex Technology Sohna Cell Plant | Amperex Technology Limited (ATL India Technology Pvt Ltd) | India | 0.3 | Y | [T018 2026-11-20] Status unconfirmed. PIB release 2163723 (S39, 2025-09-04): minister inau… |
| AMTE Power Thurso | LionVolt | United Kingdom | 0.3 | Y | [T015 2026-11-20] Status unconfirmed. AMTE Power went into administration Dec 2023; Dutch … |
| Anneng Qisheng (安能旗胜) Linwu lithium battery and energy-storage battery project (Linwu County, Chenzhou) | Anneng Qisheng (安能旗胜) | China | 0.3 | N | [T065 2026-11-22] [T065] NEW (no Anneng/安能/Linwu/Chenzhou row in factories_export.csv or r… |
| BYD Baotou battery plant (包头比亚迪电池) | Baotou BYD Battery | China | 0.3 | N | [T003 2026-11-20] Entity on BYD's 2025 environmental-disclosure list (D-016, <=0.4); no ca… |
| Basquevolt Vitoria-Gasteiz | Basquevolt | Spain | 0.3 | Y | [T015 2026-11-20] Status unconfirmed; v1 'operational' + 10 GWh by 2027 not supported. Bas… |
| BenAn Energy Taicang sodium-ion plant | Benan Energy Technology (Jiangsu) Co., Ltd. | China | 0.3 | Y | [T021 2026-11-20] status unconfirmed. Only open evidence: Dec 2024 EIA-stage notice for a … |
| Beyonder Battery Center (Forus/Sandnes) | Beyonder AS | Norway | 0.3 | Y | [T015 2026-11-20] Status unconfirmed. Beyonder's own site (undated, fetched) says its 'inn… |
| BYD FinDreams (XCMG-FinDreams) Xuzhou Blade Battery Plant | BYD (FinDreams Battery) | China | 0.3 | Y | [T003 2026-11-20] Timeline: iFeng 2023-11-20 structures topped out, trial production plann… |
| CATL Shanghai Lingang battery base (Nanhui New City) | CATL | China | 0.3 | N | [T002 2026-11-20] cell production unconfirmed; module base per S22. is_cell_manufacturer=f… |
| Chilwee Changxing Lithium Cell Plant | Chilwee (Chaowei Group) | China | 0.3 | Y | [T021 2026-11-20] status unconfirmed. Only fetched evidence: company profile page says HQ … |
| Deyi Energy (Chery) Tongling Zongyang power battery project (Qiaogang Park) | Deyi Energy Technology (Tongling) Co., Ltd. | China | 0.3 | N | [T040 2026-11-20] NEW. Chery's own power-battery base: Qiaogang Park, Zongyang Economic De… |
| E-One Moli (Molicel) Kaohsiung plant | E-One Moli Energy Corp. (Molicel) | Taiwan | 0.3 | N | [T043 2026-11-20] NEW (T043, Taiwan sweep). GTAI 2026-06-17 (S8): fire at E-One Moli's pro… |
| Cheonan Plant | EIG (Energy Innovation Group Ltd.) | South Korea | 0.3 | Y | [T019 2026-11-20] Energy Innovation Group, Ltd. (registered office #70, 3-ro, 4-sandan, Ji… |
| BYD FinDreams Shenzhen plant (Kengzi/Pingshan base) | FinDreams Battery (BYD) | China | 0.3 | Y | [T003 2026-11-20] status unconfirmed (D-016). v1 50 GWh came from a Sina article that is n… |
| Gansu Yingao Energy Storage Baiyin 8 GWh LFP battery project (Baiyin District) | Gansu Yingao Energy Storage Technology Co., Ltd. (甘肃英奥储能科技有限公司) | China | 0.3 | N | [T049 2026-11-20] NEW (T049 sweep, Gansu; not in factories_export.csv or removed.csv: no m… |
| Geely Ganzhou power battery project (phase 1 12 GWh of a planned 42 GWh; ENERGEE Ganzhou base) | Geely Technology Group (吉利科技集团) - ENERGEE (吉曜通行) Ganzhou base | China | 0.3 | N | [T066 2026-11-22] [T066 NEW; ENERGEE completeness] ENERGEE names Ganzhou as one of its pro… |
| Geely Tonglu power battery project (12 GWh, Tonglu Economic Development Zone; ENERGEE Tonglu base) | Geely Technology Group (吉利科技集团) - ENERGEE (吉曜通行) Tonglu base | China | 0.3 | N | [T066 2026-11-22] [T066 NEW; ENERGEE completeness] ENERGEE lists Tonglu among its bases (S… |
| Godi Energy Hyderabad Gigafactory | Godi India | India | 0.3 | Y | [T018 2026-11-20] Only source: Jan 2024 Davos MoU with Telangana (S34): 12.5 GWh total = P… |
| Gotion Lujiang plant (Lujiang High-tech Zone base) | Gotion High-tech | China | 0.3 | Y | [T005 2026-11-20] is_cell_manufacturer kept true (D-015: not flipped to pass a check). Aut… |
| Great Power Ulanqab energy storage and semi-solid-state cell plant | Great Power | China | 0.3 | Y | [T008 2026-11-20] Announcement 2024-07-21 (S6, S7b): 10 GWh/yr storage cells + system inte… |
| Gree Titan Zhuhai LTO Cell Plant | Gree Titan (Gree Titanium New Energy, formerly Yinlong New Energy) | China | 0.3 | Y | [T021 2026-11-20] status unconfirmed at site level. Evidence is company-level only: Gree T… |
| Guoneng (国能电池) Jiangxi Fenyi (Xinyu) plant | 国能电池科技股份有限公司 (Guoneng Battery, Beijing) | China | 0.3 | N | [T095 2026-11-24] [T095] SURVIVORSHIP add, not in DB (data/reference/candidates/T074_miit_… |
| Hubei Wocheng New Energy Shiyan 20 GWh sodium-ion energy storage zero-carbon manufacturing base (Zhangwan District) | Hubei Wocheng New Energy Co., Ltd. | China | 0.3 | N | [T047 2026-11-20] NEW (T047 sweep, Hubei/Shiyan; also listed as a T025 candidate, not prev… |
| Jianheng Aoneng Dalate Banner sodium-ion battery base (Ordos supply-chain area) | Inner Mongolia Jianheng Aoneng Technology Co., Ltd. | China | 0.3 | N | [T067 2026-11-22] [T067] NEW (Inner Mongolia sweep, Ordos). SMM 2025-07-14 (S9): phase I (… |
| Hohhot 50 GWh sodium-ion battery and energy storage industrial park (Hohhot Economic and Technological Development Zone) | Inner Mongolia Juneng Zhengxin Energy Storage Technology Co., Ltd. (Chinese name unconfirmed) | China | 0.3 | N | [T067 2026-11-22] [T067] NEW (Inner Mongolia sweep). Launch ceremony 2024-07-28 (S4, S5): … |
| Ordos Juungar Banner sodium-ion battery and energy storage industrial park (Juungar Economic Development Zone) | Inner Mongolia Xinjing New Energy Technology Co. (name as transliterated by China Daily; Chinese name unconfirmed) | China | 0.3 | N | [T067 2026-11-22] [T067] NEW (Inner Mongolia sweep). China Daily 2025-09-04 (S7): investme… |
| International Battery Company Bengaluru Gigafactory | International Battery Company | India | 0.3 | Y | [T018 2026-11-20] Status: groundbreaking of the INR 390 crore 'Giga Factory Unit' in Benga… |
| JEVE (捷威动力) Yancheng base | JEVE (Tianjin Jiewei Power / 捷威动力) | China | 0.3 | N | [T095 2026-11-24] [T095] SURVIVORSHIP/coverage add. JEVE (Tianjin Jiewei Power) is a Tianj… |
| Jiangsu Ruien New Energy (Reliance Energy Tech) cell plant, Inđija | Jiangsu Ruien New Energy (reported in Serbian media as Jiangsu Reliance Energy Tech) | Serbia | 0.3 | N | [T052 2026-11-20] NEW (T052 sweep, Serbia; named in task prompt; not in DB or removed.csv … |
| Jiangsu Tafel New Energy Nanjing Plant | Jiangsu Tafel New Energy | China | 0.3 | Y | [T022 2026-11-20] CHANGED vs v1 (7.5 GWh -> null): the 4 GWh / 10 GWh figures below are CO… |
| Jiuxu Sodium (Alxa) 50 GWh sodium-battery full-chain project (Alxa High-tech Zone incubation park) | Jiuxu Sodium Battery (Alxa) New Energy Technology Co., Ltd. (九续钠电（阿拉善）新能源科技有限公司) | China | 0.3 | N | [T042 2026-11-20] NEW (T042 sweep, Inner Mongolia). Project 'landed' 27 May (2026, per art… |
| Jueshi New Energy Zhangye 5 GWh sodium-ion battery manufacturing project (Zhangye Economic and Technological Development Zone) | Jueshi New Energy (name as transliterated by SMM; Chinese name unconfirmed) | China | 0.3 | N | [T049 2026-11-20] NEW but weak (T049 sweep, Gansu; not in DB; distinct from the Easton Zha… |
| Liotech Novosibirsk lithium-ion cell plant (PNK-Tolmachevo) | Liotech | Russia | 0.3 | N | [T052 2026-11-20] NEW (T052 sweep, Russia; not in factories_export.csv or removed.csv: no … |
| Ritto Plant (Lithium Energy Japan) | Lithium Energy Japan (LEJ) | Japan | 0.3 | N | [T063 2026-11-22] [T063 2026-11-22] NEW (Japan sweep). LEJ's main cell plant at Ritto, Shi… |
| Nafang New Energy (钠方新能源, Li-FUN subsidiary) Yueyang sodium-ion cell base | Nafang New Energy (钠方新能源) | China | 0.3 | N | [T065 2026-11-22] [T065] NEW (Li-FUN's Zhuzhou plant is the existing row li-fun-technology… |
| FinDreams Ningbo battery plant (宁波弗迪电池) | Ningbo FinDreams Battery | China | 0.3 | N | [T003 2026-11-20] Entity on BYD's 2025 environmental-disclosure list (D-016, <=0.4); no ca… |
| Phylion Suzhou Plant (Suzhou manufacturing base) | Phylion Battery (Xingheng Power Co., Ltd.) | China | 0.3 | Y | [T023 2026-11-20] Status operational at <=0.4: only an undated company self-description (S… |
| PPES Kasai Plant | Prime Planet Energy & Solutions | Japan | 0.3 | N | [T043 2026-11-20] NEW (T043, Japan sweep; lead from T013.csv 'no_open_source'). PPES's own… |
| PPES Sumoto Plant | Prime Planet Energy & Solutions | Japan | 0.3 | N | [T043 2026-11-20] NEW (T043, Japan sweep; lead from data/reference/operator_sites/T013.csv… |
| Beijing BESK Technology (BEST) Changzhou battery plant (SK / BAIC JV) | Beijing BESK Technology (BEST) | China | 0.3 | N | [T011 2026-11-20] Same evidence standard as Samsung SDI Tianjin/Xi'an: SK Innovation's own… |
| Sodium Batteries Australia pilot manufacturing facility | Sodium Batteries Australia | Australia | 0.3 | Y | [T020 2026-11-20] Only evidence is the company's own homepage: a '1MW pilot Na Ion manufac… |
| Statevolt Ras Al Khaimah | Statevolt Emirates | United Arab Emirates | 0.3 | Y | [T020 2026-11-20] US$3.2bn, 60 ha RAKEZ site (Al Hamra per S10; Al Ghail per S9), up to 40… |
| Sunwoda Quzhou plant | Sunwoda | China | 0.3 | Y | [T007 2026-11-20] Restored (not removed). ESS News (Aug 2025, S37; Quzhou named in the art… |
| Sunwoda Shenzhen plant | Sunwoda | China | 0.3 | N | [T007 2026-11-20] Restored (not removed). Sunwoda's 2025 annual report construction-in-pro… |
| Lishen Tianjin plant (Tianjin Binhai New Energy Industry Base) | Tianjin Lishen Battery Joint-Stock Co., Ltd. | China | 0.3 | Y | [T009 2026-11-20] Row re-scoped to the new Binhai Hi-Tech base: 24 GWh EV power batteries … |
| Lishen Mianyang Southwest Production Base | Tianjin Lishen Battery | China | 0.3 | Y | [T009 2026-11-20] Restored (not removed). status unconfirmed: the only fetched page (escn,… |
| Lishen Tianjin HQ cell plant (Huayuan Industrial Park) | Tianjin Lishen Battery Joint-Stock Co., Ltd. | China | 0.3 | N | [T009 2026-11-20] Split from the Binhai new-base row: the operating Tianjin headquarters c… |
| Lishen Wuxi New Energy Industrial Base | Tianjin Lishen Battery | China | 0.3 | Y | [T009 2026-11-20] Groundbreaking 28 June 2022 (SMM 2022-06-30): production base in Ehu Tow… |
| Tianpu Technology Ordos lithium-ion battery and system intelligent manufacturing project (50 GWh) | Tianpu Technology | China | 0.3 | N | [T042 2026-11-20] NEW (T042 sweep, Inner Mongolia). REPORTED tier: only an SMM news item (… |
| Toyota Battery (PEVE) Miyagi Plant | Toyota Battery Co., Ltd. (formerly Primearth EV Energy) | Japan | 0.3 | Y | [T013 2026-11-20] Status unconfirmed (D-016): no current production evidence for this site… |
| Toyota Teiho Plant | Toyota Motor Corporation | Japan | 0.3 | Y | [T013 2026-11-20] Status unconfirmed (<=0.4). Toyota Times (2023-10-02): Teiho is Toyota's… |
| VFlowTech Tuas Facility | VFlowTech | Singapore | 0.3 | Y | [T019 2026-11-20] Status unconfirmed. The Feb 2023 Series A was to fund 'setting up a 200 … |
| BYD FinDreams Wenzhou battery base (Qiaotou, Yongjia) | Wenzhou FinDreams Battery Co., Ltd. | China | 0.3 | Y | [T003 2026-11-20] China Daily 2023-02-23: 29 Wenzhou projects (incl. BYD's new-energy batt… |
| Xingtai 12 GW high-performance lithium-ion ESS battery project, phase I | Xingtai (Hebei) Lithium Battery Technology Co., Ltd. | China | 0.3 | N | [T048 2026-11-20] NEW (T048 sweep, Hebei). SMM 2026-01-28: Xingtai Municipal Bureau of Eco… |
| Zeta Energy Houston | Zeta Energy | United States | 0.3 | Y | [T017 2026-11-20] Status unconfirmed. Zeta's 12,000+ sq ft West Houston site (Dec 2021 rel… |
| Zhongtian Energy Storage (ZTT) Nantong new-energy-storage low-carbon intelligent manufacturing project | Zhongtian Energy Storage Technology Co., Ltd. (中天储能科技有限公司) | China | 0.3 | N | [T070 2026-11-23] [T070 NEW; capacity null by D-026/cell-vs-system ambiguity] Not in DB (g… |
| Zoolnasm (Zhongna Energy) Guangde sodium-ion battery base | Zoolnasm (Zhongna Energy) | China | 0.3 | Y | [T024 2026-11-20] CHANGE vs v1 (operational/start 2024): no open page shows Guangde produc… |
| Afrivolt Atlantis gigafactory | Afrivolt | South Africa | 0.35 | Y | [T020 2026-11-20] Planned Atlantis SEZ (Cape Town) Li-ion cell plant: 1.5 GWh initial, 5 G… |
| ATL Dongguan cell plant | Amperex Technology Limited (ATL) | China | 0.35 | N | [T039 2026-11-20] status supported only by a secondary open page (Wikipedia: ATL 'has prod… |
| ATL Ningde cell plant | Amperex Technology Limited (ATL) | China | 0.35 | N | [T039 2026-11-20] Fujian, Ningde. Same evidence and caveats as the ATL Dongguan row (Wikip… |
| Anhui Yijiatong (EIKTO) Xuancheng cell plant | Anhui Yijiatong Battery Co., Ltd. (安徽益佳通电池有限公司, EIKTO) | China | 0.35 | N | [T070 2026-11-23] [T070 NEW; capacity null] Not in DB (grep yijiatong / 益佳通 / EIKTO / Xuan… |
| Zhaoqing Aoyou Power Battery (肇庆遨优动力电池) plant | 肇庆遨优动力电池有限公司 (Zhaoqing Aoyou Power Battery Co., Ltd.) | China | 0.35 | N | [T095 2026-11-24] [T095] SURVIVORSHIP add, not in DB (Grep Zhaoqing rows: none is Aoyou). … |
| APB Fukui Center Takefu Factory (Echizen Plant) | APB Corporation | Japan | 0.35 | Y | [T019 2026-11-20] APB (Echizen, Fukui) received a bankruptcy commencement order from Fukui… |
| BAK Zhengzhou Plant | BAK Battery | China | 0.35 | Y | [T009 2026-11-20] v1 had 30 GWh (2028) / 15 GWh (2026) / 2.5 GWh (2024) attributed to Zhen… |
| BAK Shenzhen Plant (BAK Industrial Park) | BAK Battery (Shenzhen BAK Power Battery) | China | 0.35 | Y | [T009 2026-11-20] v1 3.5 GWh (2018, Baidu Baike) not confirmed by any fetched page -> null… |
| BYD FinDreams Bengbu plant | BYD (FinDreams Battery) | China | 0.35 | Y | [T003 2026-11-20] Status unconfirmed beyond the entity: 蚌埠弗迪电池有限公司 is on BYD's 2025 enviro… |
| BYD FinDreams Huizhou plant | BYD FinDreams | China | 0.35 | Y | [T003 2026-11-20] 惠州比亚迪电池有限公司 (phase 1 and 2 parks) is on the 2025 environmental-disclosur… |
| Cubenergy Changzhou energy storage intelligent manufacturing base (15 GWh) | Cubenergy | China | 0.35 | N | [T046 2026-11-20] NEW but doubtful scope. EnergyTrend 2025-12-24: Cubenergy's energy stora… |
| Dragonfly Energy Reno | Dragonfly Energy | United States | 0.35 | Y | [T016 2026-11-20] Status unconfirmed (D-016 low-confidence null). FY2025 10-K (filed 2026-… |
| Elinor Batteries Gigafactory (Eiktyr Industrial Park, Orkland) | Elinor Batteries | Norway | 0.35 | Y | [T015 2026-11-20] Still announced/pre-FID; no groundbreaking or FID found. Investor page (… |
| Far East Battery Jiangxi (Yichun) cylindrical cell plant | Jiangxi Far East Battery / Far East Lithium (江西远东锂电) | China | 0.35 | N | [T070 2026-11-23] [T070 NEW; capacity null] Not in DB (grep as for the Yixing row). Far Ea… |
| Fuzhou FinDreams Battery Plant (Jiangxi) | FinDreams Battery | China | 0.35 | Y | [T003 2026-11-20] Coordinates nulled: v1 26.06N/119.31E is Fuzhou, FUJIAN; the plant is in… |
| Ganfeng LiEnergy Dongguan Base (赣锋锂电东莞科技 10GWh new-type lithium battery & ESS HQ base) | Ganfeng LiEnergy | China | 0.35 | N | [T009 2026-11-20] Restored (not removed): site exists and commenced operation 25 Feb 2026 … |
| Gelion Fairfield | Gelion | Australia | 0.35 | Y | [T020 2026-11-20] Pilot zinc-bromide (Endure) line at partner Battery Energy Power Solutio… |
| Great Power Guangde plant | Great Power | China | 0.35 | Y | [T008 2026-11-20] Company plan (board announcement 2024-11-19): 10 GWh storage cells + sys… |
| INESIS gigafactory, New Moscow (planned; possibly the second Krasnaya Pakhra plant) | Innovative Energy Systems (INESIS / ИНЭСИС) | Russia | 0.35 | N | [T052 2026-11-20] NEW (T052 sweep, Russia; not in DB or removed.csv: no match for INESIS/И… |
| Alxa 30 GWh cell and energy-storage equipment project (Zhilian Huitong) | Inner Mongolia Zhilian Huitong Logistics Co., Ltd. | China | 0.35 | N | [T023 2026-11-20] REVISED after audit: nameplate now cited to S19d (page wording: workshop… |
| Li-FUN Zhuzhou Plant | Li-FUN Technology | China | 0.35 | Y | [T022 2026-11-20] Status unconfirmed. Only open source fetched: 36Kr company profile - Hun… |
| Kusatsu Plant (Lithium Energy Japan) | Lithium Energy Japan (LEJ) | Japan | 0.35 | Y | [T019 2026-11-20] Kusatsu plant (Shiga) began shipping June 2009 with capacity ~110 MWh/yr… |
| Log9 Materials Bengaluru Cell Facility | Log9 Materials | India | 0.35 | Y | [T018 2026-11-20] pv magazine India 2023-04-24 (S41): Log9 'has launched the production' a… |
| Nandu Power (Narada) Hangzhou/Fuyang Lithium Cell Base | Narada Power (Nandu Power) | China | 0.35 | Y | [T023 2026-11-20] REVISED after audit (D-016): status operational at <=0.4. Narada's 2025 … |
| Panasonic Energy Kaizuka Factory | Panasonic Energy Kaizuka Co., Ltd. | Japan | 0.35 | Y | [T013 2026-11-20] Status unconfirmed (D-016): no open source shows current cell production… |
| Phylion Chuzhou Plant | Phylion Battery (Xingheng Power) | China | 0.35 | Y | [T023 2026-11-20] ESCALATE-type row (v1 nameplate 25 GWh, now null). Evidence: S3 (company… |
| PPES Dalian Plant | Prime Planet Energy Dalian Co., Ltd. | China | 0.35 | N | [T013 2026-11-20] Found while mining the PPES locations page (S22 lists 'Dalian, China - R… |
| Pylontech Yangzhou (Yizheng) plant (扬州派能) | Yangzhou Pylon Technologies (扬州派能) | China | 0.35 | N | [T023 2026-11-20] Added because Pylontech's 2025 annual report lists Yangzhou as one of it… |
| Recharge Industries Geelong (Avalon) Gigafactory | Recharge Industries | Australia | 0.35 | Y | [T020 2026-11-20] Announced Jan 2023: up to 30 GWh/yr, 2 GWh 2024 and 6 GWh 2026 targets (… |
| Samsung SDI-ARN (Xi'an) Power Battery plant, Changan District, Xi'an | Samsung SDI | China | 0.35 | N | [T011 2026-11-20] SAMSUNG SDI-ARN (Xi'an) Power Battery Co., Ltd., No. 2655 Biyuan 3rd Rd,… |
| Samsung SDI Tianjin plant (Tianjin Samsung SDI / Samsung SDI (Tianjin) Battery), Wuqing | Samsung SDI | China | 0.35 | N | [T011 2026-11-20] Samsung SDI's Global Network page lists two Tianjin battery entities (Ti… |
| Sanwei Battery Yugan solid-state battery project (Yugan High-Tech Zone) | Sanwei Battery (Shaanxi) | China | 0.35 | N | [T039 2026-11-20] Jiangxi, Yugan High-Tech Zone (Shangrao). Single press source (CarNewsCh… |
| Sany Redelephant (三一红象) Changsha lithium-ion power battery project (Changsha Economic and Technological Development Zone) | Sany Redelephant (三一红象) | China | 0.35 | N | [T065 2026-11-22] [T065] NEW (no Sany/三一/红象 row in factories_export.csv or removed.csv). C… |
| SES AI Woburn | SES AI | United States | 0.35 | N | [T017 2026-11-20] Woburn MA is SES AI's R&D site (Q3 2026 release dateline WOBURN; company… |
| Qingke Energy (Shaanxi Coal Research Institute) Xi'an Aerospace Base 3.5 GWh energy storage/power battery cell project | Qingke Energy Co. (陕煤研究院顷刻能源公司) | China | 0.35 | N | [T041 2026-11-20] NEW (not in DB; no match for Qingke/顷刻/Shaanxi Coal/Aerospace Base in ex… |
| Waterma (沃特玛) Shenzhen Pingshan base | Shenzhen Waterma Battery Co., Ltd. (深圳市沃特玛电池有限公司) | China | 0.35 | N | [T095 2026-11-24] [T095] SURVIVORSHIP add, not in DB or data/removed.csv (Grep zh+en). Wat… |
| SVOLT Wuhan plant (formerly Zhongxing Gaoneng / 中兴高能, Dongxihu) | 蜂巢能源（武汉）有限公司 (SVOLT Wuhan; formerly 中兴高能技术有限责任公司) | China | 0.35 | N | [T095 2026-11-24] [T095] SURVIVORSHIP add, not in DB (the DB has SVOLT Chengdu/Shangrao/Hu… |
| Times SAIC (时代上汽) power battery plant, Liyang | Times SAIC Power Battery Co., Ltd. (时代上汽动力电池有限公司) | China | 0.35 | N | [T038 2026-11-20] Discovery add (T038, Jiangsu), routed from T002 (operator_sites row 'Liy… |
| Trentar Sodium-Ion Cell Plant | Trentar Energy Solutions | India | 0.35 | Y | [T018 2026-11-20] KPIT release 2025-02-12 (S52): Trentar to commercialise KPIT's sodium-io… |
| UniverCell Flintbek (headquarters, electrode and first 21700 cell production) | UniverCell Holding GmbH | Germany | 0.35 | N | [T052 2026-11-20] NEW (T052 sweep, Germany). The Next Web 2026-03-05: the Flintbek factory… |
| Veken Ningbo sodium-ion plant | Veken Technology | China | 0.35 | Y | [T024 2026-11-20] status unconfirmed. v1 'operational since July 2024 batch sampling' came… |
| YİĞİT AKÜ-Ganfeng gigafactory | YİĞİT AKÜ-Ganfeng LiEnergy JV | Turkey | 0.35 | Y | [T009 2026-11-20] Announced Aug 2024 (5 GWh design capacity, USD 500m, JV with Yigit Aku).… |
| Yunnan Junhe Yuanxin Nanhua County (Chuxiong) cell line project, Phase 1 (Laogaoba Industrial Park) | Yunnan Junhe Yuanxin New Energy Co., Ltd. (云南君和远信新能源有限公司) | China | 0.35 | N | [T049 2026-11-20] NEW (T049 sweep, Yunnan; not in DB or removed.csv; distinct from the Jin… |
| Zhejiang Aoyou Power (浙江遨优动力) Huzhou / Nanxun bases | 浙江遨优动力系统有限公司 (Zhejiang Aoyou Power Systems Co., Ltd.) | China | 0.35 | N | [T095 2026-11-24] [T095] SURVIVORSHIP add, not in DB. Aoyou was 'once a star of China's po… |
| AESC Zama Plant | AESC | Japan | 0.4 | Y | [T012 2026-11-20] AESC's original plant at Nissan Zama (Kanagawa). Only open capacity figu… |
| Ambri Marlborough | Ambri | United States | 0.4 | Y | [T016 2026-11-20] Ambri (liquid-metal calcium-antimony cells for ESS) filed Chapter 11 May… |
| Anhui Volt Era (伏特时代) Jinzhai 10 GWh semi-solid / solid-state battery project | Anhui Volt Era New Energy Co., Ltd. | China | 0.4 | N | [T040 2026-11-20] NEW. Jinzhai County Economic Development Zone (Lu'an), Anhui. SMM 2025-0… |
| BE-VOLT gigafactory (Seneffe-Manage) | AVESTA Holding (BE-VOLT) | Belgium | 0.4 | N | [T069 2026-11-22] [T069] ADD at low confidence; cell-vs-pack scope UNRESOLVED, so nameplat… |
| WeLion New Energy Huzhou Semi-Solid Plant | Beijing WeLion New Energy | China | 0.4 | Y | [T021 2026-11-20] MAJOR CORRECTION vs v1: v1 gave 20 GWh operational with phase 1 complete… |
| Blue Solutions Quimper (Ergué-Gabéric / Odet mother plant) | Blue Solutions | France | 0.4 | Y | [T014 2026-11-20] Status unconfirmed beyond 2024: Blue Solutions (17 May 2024 release) say… |
| Wuwei FinDreams Battery plant (BYD New Energy Power Battery Yangtze River Delta Manufacturing Center) | BYD FinDreams Battery | China | 0.4 | Y | [T003 2026-11-20] Coordinates nulled: v1 37.93N/102.63E is Wuwei, Gansu; the plant is 无为 (… |
| CALB Zigong Base | CALB | China | 0.4 | N | [T004 2026-11-20] Construction started 2026-01, completion/production expected within 2026… |
| Camel Xiangyang New Energy Low-Carbon Industrial Park | Camel Group | China | 0.4 | Y | [T021 2026-11-20] REVISED after audit. Camel's 2025 annual report (cninfo) construction-in… |
| CATL Xiamen battery base (Xiamen Times New Energy) | CATL | China | 0.4 | Y | [T002 2026-11-20] ESCALATE (unresolved after 3 further Chinese searches and 2 opened pages… |
| CATL Xining plant (Qinghai Times New Energy Technology Co., Ltd.) | CATL | China | 0.4 | Y | [T002 2026-11-20] ESCALATE (capacity). Qinghai Times is named in CATL's 2025 annual report… |
| China Lithium Battery Technology (Luoyang) Co., Ltd. (中航锂电（洛阳）, 'Luoyang Company') cell plant, Luoyang | China Lithium Battery Technology (Luoyang) Co., Ltd. | China | 0.4 | N | [T057 2026-11-20] [T057] New row (lead from data/reference/operator_sites/T004.csv, exclud… |
| Chongqing Yaoning New Energy 30 GWh battery plant (Geely; sale to CATL approved 2026) | Chongqing Yaoning New Energy (重庆耀宁新能源) | China | 0.4 | N | [T066 2026-11-22] [T066 NEW; found while checking ENERGEE - outside the eight named base c… |
| Dejia Energy (Shanghai) Lingang Blue Bay solid-state line | Dejia Energy (Shanghai) Co., Ltd. (德嘉能源（上海）) | China | 0.4 | N | [T046 2026-11-20] NEW (no match on Dejia / 德嘉 in the DB). SMM 2026-03-02: Dejia Energy (Sh… |
| Docters (Tianjin) all-solid-state battery GWh line | Docters (Tianjin) New Energy Technology Co., Ltd. (道克特斯（天津）新能源科技有限公司) | China | 0.4 | N | [T048 2026-11-20] NEW (T048 sweep, Tianjin). S9: on 1 July 2026 the company announced its … |
| e-Zinc Mississauga Pilot Manufacturing Facility | e-Zinc | Canada | 0.4 | Y | [T020 2026-11-20] 42,000 sq ft pilot manufacturing facility at 7391 Pacific Circle, Missis… |
| EAS Batteries Nordhausen | EAS Batteries GmbH | Germany | 0.4 | N | [T071 2026-11-23] [T071] ADD (Part 2, Battery-News Oct-2025 residue 'Nordhausen 0.9 GWh').… |
| Easton (EAST Group) Zhangye sodium-ion cell plant (new energy-storage equipment demonstration project, Phase II) | Easton (EAST Group Co., Ltd., 易事特) | China | 0.4 | N | [T041 2026-11-20] NEW (not in DB as its own row). The existing Dongguan row (easton-east-g… |
| Chungju Plant | Enertech International | South Korea | 0.4 | Y | [T019 2026-11-20] Company site (factory: 223 Chungjusandan 7-ro, Chungju) states it produc… |
| AESC Sunderland Plant 1 (original gigafactory) | Envision AESC | United Kingdom | 0.4 | N | [T012 2026-11-20] Original AESC cell plant at the Nissan Sunderland site, producing since … |
| EVE Energy Ningbo plant | EVE Energy | China | 0.4 | Y | [T006 2026-11-20] CAVEAT: A1 lists 'Zhejiang' as a base - not site-specific (does not name… |
| Far East Yixing power battery plant (Far East First New Energy) | Far East First New Energy (远东首诺新能源), Yixing | China | 0.4 | N | [T070 2026-11-23] [T070 NEW] Not in DB: grepped factories_export.csv, data/removed.csv and… |
| AESC Smyrna (Tennessee) | Fixx Energy (formerly AESC / Envision AESC) | United States | 0.4 | Y | [T012 2026-11-20] 500 Battery Plant Rd, Smyrna TN. AESC/Nissan site since 2012 (S35); EV c… |
| Gigafactory Malaysia | Gigafactory Malaysia Sdn Bhd | Malaysia | 0.4 | Y | [T019 2026-11-20] NanoMalaysia subsidiary, 15,000 sq ft plant in Suria Industrial Park, Se… |
| Great Power Changzhou plant | Great Power | China | 0.4 | N | [T008 2026-11-20] Listed by the 2025 annual report among 9 stably operating bases (S1); su… |
| Great Power Foshan plant | Great Power | China | 0.4 | N | [T008 2026-11-20] Listed by the 2025 annual report among 9 stably operating bases (S1); ad… |
| Great Power Guangzhou (Panyu) plant | Great Power | China | 0.4 | Y | [T008 2026-11-20] 2025 annual report names Guangzhou as one of 9 stably operating producti… |
| Great Power Vietnam plant | Great Power | Vietnam | 0.4 | N | [T008 2026-11-20] 2025 annual report: Vietnam is one of 9 operating bases and 'the Vietnam… |
| Great Power Zhuhai plant | Great Power | China | 0.4 | N | [T008 2026-11-20] Listed by the 2025 annual report as one of 9 stably operating production… |
| GS Yuasa Ibaraki stationary storage plant | GS Yuasa Corporation | Japan | 0.4 | N | [T063 2026-11-22] [T063 2026-11-22] NEW (Japan sweep; lead from team/candidate_routing.csv… |
| FinDreams Guangxi-ASEAN battery plant (广西东盟弗迪电池) | Guangxi ASEAN FinDreams Battery | China | 0.4 | N | [T003 2026-11-20] Cailian 2022-09-13: 广西东盟弗迪电池 project of 10 GWh hybrid-vehicle battery + … |
| Guyi New Energy Tumd Left Banner 2.2 GWh high-safety solid-state battery project (Taigemu Town, Hohhot) | Guyi New Energy (Inner Mongolia) Technology Co., Ltd. | China | 0.4 | N | [T067 2026-11-22] [T067] NEW (Inner Mongolia sweep, Hohhot). Mysteel 2026-04-07 (S8): proj… |
| Foxconn Kaohsiung LFP battery plant | Foxconn (Hon Hai Precision Industry) | Taiwan | 0.4 | N | [T043 2026-11-20] NEW (T043, Taiwan sweep). GTAI 2026-06-17 (S5): Foxconn makes LFP 'Batte… |
| Sunwoda Huizhou plant (Huizhou Liwei New Energy) | Huizhou Liwei New Energy Technology Co., Ltd. (Sunwoda) | China | 0.4 | Y | [T007 2026-11-20] Status basis (D-016): the annual-report subsidiary table shows existence… |
| Highstar Qidong Plant | Jiangsu Highstar Battery Manufacturing Co., Ltd. (Highstar Battery) | China | 0.4 | Y | [T022 2026-11-20] CHANGED vs v1 (7.3 GWh -> null). v1 summed 1.3 GWh + a '6 GWh ESS projec… |
| Jiangsu Muxing Shidai 3 GWh energy storage battery plant (Nantong High-tech Zone) | Jiangsu Muxing Shidai Energy Storage Technology Co., Ltd. | China | 0.4 | N | [T038 2026-11-20] Discovery add (T038, Jiangsu). EnergyTrend roundup (Dec 2025, date from … |
| Zenergy Nanjing production base | Nanjing Zenergy Battery Technologies Co., Ltd. | China | 0.4 | N | [T009 2026-11-20] Zenergy's FY2025 annual report records an impairment of 'production line… |
| LG Energy Solution Ochang Energy Plant | LG Energy Solution | South Korea | 0.4 | Y | [T010 2026-11-20] CONFIDENCE 0.4 (D-015): the only capacity figure is an undated-outcome 2… |
| Liaoning Yuanxin 10 GWh drone solid-state battery and energy-storage equipment project (Chaoyang) | Liaoning Yuanxin Energy Storage Technology Co., Ltd. (辽宁远信储能技术有限公司) | China | 0.4 | N | [T048 2026-11-20] NEW (T048 sweep, Liaoning). Chaoyang Economic and Technological Developm… |
| Longbang (Fujian) Longyan 1 GWh three-dimensional solid-state lithium-ion battery project (Gaobei, Longyan High-tech Zone) | Longbang (Fujian) Machinery Co., Ltd. | China | 0.4 | N | [T064 2026-11-22] [T064 NEW, Fujian/Longyan sweep] Mysteel flash news 2025-11-17 (S1, open… |
| Lyten Reno Lithium-Sulfur Gigafactory | Lyten | United States | 0.4 | N | [T017 2026-11-20] Discovery candidate (T026 -> T017). Announced 2024-10-15: >$1bn plant ne… |
| Macsen Sodium-Ion Cell Pilot Line (Udaipur) | Macsen Labs | India | 0.4 | Y | [T018 2026-11-20] Only fetched source (S45, 2025-08-25, headline: sodium-ion cell pilot li… |
| Ono Works | Maxell | Japan | 0.4 | Y | [T019 2026-11-20] Maxell announced (2024-09-13) a ~JPY 5bn investment at the Ono Business … |
| Munoth Lithium Cell Plant (Tirupati) | Munoth Industries Limited | India | 0.4 | Y | [T018 2026-11-20] Phases (S46 EVreporter 2022-09-15, S47 Swarajya 2022-09-17): Phase I ins… |
| Murata Yasu Plant | Murata Manufacturing | Japan | 0.4 | Y | [T019 2026-11-20] Murata's all-solid-state (oxide, SMD chip) battery line is at the Yasu P… |
| FinDreams Nanning battery plant (南宁弗迪电池) | Nanning FinDreams Battery | China | 0.4 | N | [T003 2026-11-20] Entity on BYD's 2025 environmental-disclosure list (D-016, <=0.4). Possi… |
| Nanotech Energy Chico 2 | Nanotech Energy | United States | 0.4 | Y | [T017 2026-11-20] Chico 2 (50,000 sq ft, Chico CA): Dec 2023 press release says the 18650 … |
| ProLogium Taoyuan (Taoke) Gigafactory | ProLogium Technology | Taiwan | 0.4 | N | [T043 2026-11-20] NEW (T043, Taiwan sweep). No Taiwan row existed in the DB (only ProLogiu… |
| REPT Battero Foshan plant | REPT Battero | China | 0.4 | Y | [T007 2026-11-20] Foshan (Nanhai district) base: signed with Nanhai government 2021-03-31 … |
| Sakuu Silicon Valley | Sakuu | United States | 0.4 | Y | [T017 2026-11-20] Aug 2022: 79,000 sq ft San Jose engineering/printing hub; Sakuu 'recentl… |
| Samsung SDI Seremban Plant 2 | Samsung SDI | Malaysia | 0.4 | Y | [T011 2026-11-20] Status confirmed operational by a fresh source (Herald Business, 2026-10… |
| Samsung SDI Ulsan Plant | Samsung SDI | South Korea | 0.4 | Y | [T011 2026-11-20] Only one open capacity figure exists: DIGITIMES (2023-08-21, open teaser… |
| Shanghai Electric Gotion New Energy (Nantong) energy storage battery base | Shanghai Electric Gotion New Energy Technology (Nantong) Co., Ltd. | China | 0.4 | Y | [T005 2026-11-20] Reinstated as update. 灼见汽车 article on Stockstar (2026-09-18): '南通生产基地规划年… |
| Yangquan sodium-ion battery line (Huana Xinneng) | Shanxi Huana Xinneng Technology (Huayang) | China | 0.4 | Y | [T023 2026-11-20] CHANGE vs v1 (nameplate 5 -> 1 GWh, ramp JSON removed). Only the 1 GWh l… |
| Siro Gemlik | Siro | Turkey | 0.4 | Y | [T009 2026-11-20] Unresolved: Farasis' 2025 AR / Securities Times (2026-11-02) say Siro's … |
| SoftBank Sakai battery cell plant (former Sharp site) | SoftBank Corp. | Japan | 0.4 | N | [T043 2026-11-20] NEW (T043, Japan sweep). SoftBank press release 2026-05-11 (S9): cell an… |
| SVOLT Huzhou plant (South Taihu New Area) | SVOLT (Honeycomb Energy / 蜂巢能源) | China | 0.4 | Y | [T008 2026-11-20] SVOLT's STAR-market prospectus (draft, Nov 2022) describes the Huzhou 'l… |
| SVOLT Ma'anshan plant | SVOLT (Svolt Energy Technology / 蜂巢能源) | China | 0.4 | Y | [T008 2026-11-20] [ESCALATE: 28 GWh row at 0.5 - capacity is a 2021 plan, status evidence … |
| Tailan New Energy Qianjiang All-Solid-State Battery Base | Tailan New Energy (太蓝新能源) | China | 0.4 | N | [T021 2026-11-20] Candidate T025:30 verified only via an aggregator page (Chyxx/智研咨询, 2026… |
| Rongsheng Mengguli Tianjin Baodi manufacturing base | Tianjin Rongsheng Mengguli New Energy Technology Co., Ltd. (天津荣盛盟固利新能源科技有限公司) | China | 0.4 | N | [T066 2026-11-22] [T066 NEW; T062 missing lead] Rongsheng Mengguli (formerly CITIC Guoan M… |
| Tongke New Energy Heyuan plant | Tongke New Energy (通科新能源) | China | 0.4 | N | [T022 2026-11-20] Plan: 2 GWh/yr sodium/lithium-ion batteries in Heyuan, Guangdong; steel-… |
| Trina Storage Dafeng base (Yancheng) | Trina Storage | China | 0.4 | N | [T038 2026-11-20] Discovery add (T038, Jiangsu). TrinaStorage company release reposted by … |
| Vehicle Energy Japan Ibaraki plant | Vehicle Energy Japan | Japan | 0.4 | N | [T063 2026-11-22] [T063 2026-11-22] NEW (Japan sweep). Vehicle Energy Japan (ex-Hitachi Ve… |
| Volklec Coventry | Volklec | United Kingdom | 0.4 | Y | [T015 2026-11-20] Downgraded from v1 under_construction/0.6: no opened source confirms pro… |
| Yunshi Weilan solid-state lithium battery production base (Jiangning, Nanjing) | Yunshi Weilan | China | 0.4 | N | [T038 2026-11-20] Discovery add (T038, Jiangsu). Signed 10 Jan 2026 at the Jiangning Distr… |
| Zhejiang Dangzhuo Energy anode-free solid-state cell project (Nanhu, Jiaxing) | Zhejiang Dangzhuo Energy | China | 0.4 | N | [T038 2026-11-20] Discovery add (T038, Zhejiang). EnergyTrend roundup (2026-03-27, date fr… |
| Sunwoda Lanxi base (Zhejiang Liwei / Zhejiang Lixin consumer and cylindrical cells) | Zhejiang Liwei Energy Technology Co., Ltd. (浙江锂威能源科技有限公司) | China | 0.4 | N | [T038 2026-11-20] Discovery add (T038, Zhejiang), routed from T007 (operator_sites row 'Zh… |
| Weizhen / Fansheng / Liyuan 1 GWh MOFs solid-state battery base (South Taihu New Area) | Zhejiang Weizhen New Material Technology Co., Ltd. | China | 0.4 | N | [T046 2026-11-20] NEW. EnergyTrend 2025-12-24: on 19 Dec 2025 the 1 GWh MOFs solid-state b… |
| Zhongna Energy Storage Gansu Zhengning Sodium-ion/Li Cell Plant | Zhongna Energy Storage New Energy Technology (Gansu) Co., Ltd. (中钠储能) | China | 0.4 | N | [T021 2026-11-20] Candidate T025:22 verified from one page (EnergyTrend China 2026-08-25),… |
| Saft/ACC Nersac Pilot Plant (Industrial Excellence Center) | ACC (Automotive Cells Company) | France | 0.45 | Y | [T014 2026-11-20] ACC's own page: pilot line, production started end 2021, qualification/t… |
| Ampace Xiamen battery base (Phase I + Phase II, CATL-ATL JV) | Ampace (Xiamen Ampace Technology Limited, 新能安) | China | 0.45 | N | [T039 2026-11-20] Xiamen (Tongxiang High-tech City per CATL annual-report lead in operator… |
| Anhui Yichuang Energy Anqing 20 GWh power battery project (Anqing Economic and Technological Development Zone) | Anhui Yichuang Energy Technology Co., Ltd. | China | 0.45 | N | [T040 2026-11-20] NEW. Seetao (2026-01-08, English translation of a local report): groundb… |
| Baise Kunyu 6 GWh cell and energy-storage integration project (Baise High-tech Zone) | Baise Kunyu New Energy Co., Ltd. (百色昆宇新能源有限公司) | China | 0.45 | N | [T039 2026-11-20] Guangxi, Baise High-tech Zone. 14 Mar 2025 city-wide Q1 major-projects g… |
| Honda GS Yuasa New Battery Plant (Blue Energy BEV lithium-ion plant) | Blue Energy Co., Ltd. | Japan | 0.45 | Y | [T013 2026-11-20] ESCALATE (20 GWh, conf<0.6). Status: GS Yuasa Q&A of 2025-05-13 says con… |
| BYD FinDreams Xining plant (Qinghai FinDreams Battery Co., Ltd.) | BYD | China | 0.45 | Y | [T003 2026-11-20] Nameplate 24 GWh is a 2018 figure (CleanTechnica; plant opened June 2018… |
| Changhong Malaysia High-Rate Lithium Battery Base | Changhong Sanjie New Energy Co., Ltd. | Malaysia | 0.45 | N | [T019 2026-11-20] Discovery candidate (T027). Board approved on 2026-04-03; Mianyang SASAC… |
| BYD FinDreams Changsha plant (Ningxiang) | Changsha FinDreams Battery (FinDreams Battery) | China | 0.45 | Y | [T003 2026-11-20] Status: 长沙弗迪电池有限公司 on the 2025 environmental-disclosure list (D-016, <=0… |
| Chuanhong New Energy Southwest Battery Production Base (Longchang, Neijiang) | Chuanhong New Energy (川宏新能源) | China | 0.45 | N | [T021 2026-11-20] ESCALATE: 10 GWh at 0.45 - the 10 GWh is stated for 'battery cells and s… |
| DFD Jiaozuo Plant (Do-Fluoride New Energy, Henan base) | Do-Fluoride New Energy Technology Co., Ltd. (DFD) | China | 0.45 | Y | [T021 2026-11-20] MAJOR CORRECTION vs v1: the '10 GWh Jiaozuo' figure came from a 2017 BES… |
| ElevenES Subotica | ElevenEs | Serbia | 0.45 | Y | [T015 2026-11-20] Pilot/pre-series LFP line in Subotica opened Apr 2023, 'fully operationa… |
| Envision AESC Wuxi Plant (Jiangyin battery manufacturing base) | Envision AESC | China | 0.45 | Y | [T012 2026-11-20] Jiangyin (Wuxi), Jiangsu. Nameplate 20 GWh: electrive 2019 (S16) states … |
| EVE Energy Qidong plant (EVE-Linyang) | EVE Energy | China | 0.45 | Y | [T006 2026-11-20] CAVEAT: A1 lists 'Jiangsu' as a production base - not site-specific (doe… |
| EVE Energy Qujing plant (23GWh cylindrical LFP energy storage & power battery project) | EVE Energy | China | 0.45 | Y | [T006 2026-11-20] REVISED: ref year 2025 now rests on the 2025 annual report fund-use tabl… |
| Factorial Energy Methuen | Factorial Energy | United States | 0.45 | Y | [T016 2026-11-20] Pilot-scale. Facility opened Oct 2023; first phase = cathode coating lin… |
| BYD FinDreams Xi'an plant | FinDreams Battery (BYD) | China | 0.45 | Y | [T003 2026-11-20] status unconfirmed (D-016): 西安弗迪电池有限公司 appears only in the AR tax-rate l… |
| BYD FinDreams Chongqing (Bishan) Blade Battery Plant | FinDreams Battery Co., Ltd. | China | 0.45 | Y | [T003 2026-11-20] Nameplate 35 GWh = phases 1+2 at full output (MarkLines 2021-04-16 tease… |
| Ganfeng LiEnergy Nanchang energy-storage cell base (588Ah line) | Nanchang Ganfeng LiEnergy | China | 0.45 | N | [T009 2026-11-20] ESCALATE (10 GWh at 0.45; status and cell-vs-pack split rest on one 2026… |
| Qingdao Gotion Battery plant (Laixi) | Gotion High-tech | China | 0.45 | Y | [T005 2026-11-20] Confidence 0.45: installed 3 GWh dated 2024-02 (>18 months). installed b… |
| InoBat Šurany (GIB EnergyX Slovakia Gigafactory) | Gotion InoBat Batteries (GIB) EnergyX Slovakia | Slovakia | 0.45 | Y | [T005 2026-11-20] D-015 revision: nameplate 8.4 GWh = latest company statement (Gotion exc… |
| Jinzhai Gotion storage cell base (Lu'an, Anhui) | Jinzhai Gotion New Energy Co., Ltd. | China | 0.45 | N | [T005 2026-11-20] D-015 revision: installed set to 5 GWh (phase 1 only, design 5 GWh [S38]… |
| Great Power Zhumadian plant (Zhumadian production base) | Great Power (Guangzhou Great Power Energy & Technology Co., Ltd. / Penghui Energy) | China | 0.45 | Y | [T008 2026-11-20] Zhumadian (Henan Penghui, Yicheng district) is listed among 9 stably ope… |
| Guoke Energy Anqing base (phase 1 running, phase 2 5 GWh storage cell line) | Guoke Energy (国科能源) | China | 0.45 | N | [T040 2026-11-20] NEW. Ifeng Finance roundup (2026-04-05): Guoke Energy held the groundbre… |
| Hina Fuyang Plant | Hina Battery | China | 0.45 | Y | [T022 2026-11-20] Phase 1 (1 GWh, first product rolled off the line 29 Nov 2022 per CnEVPo… |
| HiNa Battery Wuhan Jiangxia 10 GWh sodium-ion production base | HiNa Battery Technology Co., Ltd. (中科海钠科技有限责任公司) | China | 0.45 | N | [T047 2026-11-20] NEW (T047 sweep, Hubei/Wuhan). Signing 14 Oct 2026 between HiNa and Jian… |
| Highpower International Huizhou Plant (Longhu/Tonghu Industrial Park) | Huizhou Highpower Technology | China | 0.45 | Y | [T022 2026-11-20] CHANGED vs v1: the 3 GWh is NOT existing ESS capacity. It is the ~RMB 44… |
| Inlyte Energy US factory (site not yet selected) | Inlyte Energy | United States | 0.45 | Y | [T016 2026-11-20] v1 'operational Hayward' is not supported: no source places an Inlyte ce… |
| Jinglan New Energy Chuxiong sodium-ion base | Jinglan New Energy (景蓝新能源) | China | 0.45 | N | [T022 2026-11-20] 'Annual 5 GWh consumer-grade sodium-ion battery project' broke ground in… |
| JSW Energy Cell Gigafactory | JSW Energy | India | 0.45 | Y | [T018 2026-11-20] Latest (1 Jun 2026, Business Standard via fuelprice.co.in rewrite; BS or… |
| Gijang Dream Factory (Busan) | Kumyang | South Korea | 0.45 | Y | [T019 2026-11-20] Plan: 3.7 GWh/yr of 2170(21700) cells + 12.6 GWh/yr of 4695 cells = 16.3… |
| Lanjun New Energy Jiashan Base | Lanjun New Energy | China | 0.45 | Y | [T009 2026-11-20] ESCALATE (77 GWh; installed figure is from June 2022, >18 months old; D-… |
| Leclanché Willstätt | Leclanché | Germany | 0.45 | Y | [T014 2026-11-20] Operating pouch-cell plant but small: pv magazine 2016 reports 'more tha… |
| LG Energy Solution Nanjing (LGESNJ; Plants 6 and 9, Jiangning) | LG Energy Solution (Nanjing) Co., Ltd. | China | 0.45 | N | [T010 2026-11-20] FLOOR: LGESNJ cylindrical only. CONFIDENCE 0.45: LGES ESG 2025 (S76) lis… |
| Lishen Qingdao plant (Lishen (Qingdao) New Energy; renamed China Auto New Energy (Qingdao) Battery Technology, "中汽新能", July 2025) | Lishen (Qingdao) New Energy Co., Ltd. (now China Auto New Energy (Qingdao) Battery Technology Co., Ltd.) | China | 0.45 | Y | [T009 2026-11-20] CONFLICT: Xinhua-Shandong via Solarbe (2023-10-17) says 'currently has 4… |
| Gotion Liuzhou power battery base | Liuzhou Gotion Battery Co., Ltd. (Gotion High-tech subsidiary) | China | 0.45 | Y | [T005 2026-11-20] D-015 revision: installed now 10 GWh (phase 1, in production since Sept … |
| Anhui Nandu Huatuo Jieshou lithium cell plant (安徽南都华拓) | Anhui Nandu Huatuo New Energy Technology Co., Ltd. (安徽南都华拓新能源科技有限公司) | China | 0.45 | N | [T023 2026-11-20] Added from the Narada annual report (S1: 华拓二期 4GWh 锂电池电芯产能 being pushed … |
| Naxion Sodium-Ion Cell Pilot Plant (Hyderabad) | Naxion Energy | India | 0.45 | N | [T018 2026-11-20] Discovery while removing the Coimbatore row (pack assembly, S48: 'annual… |
| Novo Energy Gothenburg (Torslanda) gigafactory (suspended) | Novo Energy AB | Sweden | 0.45 | N | [T052 2026-11-20] NEW (T052 sweep, Sweden; not in DB or removed.csv: no match for Novo Ene… |
| ONE Circle | Our Next Energy | United States | 0.45 | Y | [T017 2026-11-20] Pilot-line LFP cell production began Nov 2023 (Solar Power World, 2023-1… |
| Panasonic Energy Wakayama Factory | Panasonic Energy | Japan | 0.45 | Y | [T013 2026-11-20] ESCALATE (10 GWh, conf<0.6). 4680 mother-factory lines at Wakayama: two … |
| Pomega Gigafactory (Polatlı, Ankara) | Pomega Energy Storage Technologies | Turkey | 0.45 | Y | [T015 2026-11-20] Polatli (Ankara) LFP cell plant began operating Aug 2023 and 'seri ureti… |
| Salient Energy Dartmouth | Salient Energy | Canada | 0.45 | Y | [T020 2026-11-20] Pilot zinc-ion cell line at Dartmouth NS: ~100 batteries/month in 2022 (… |
| Shenzhen BetterPower Shenzhen Plant (Longhua base) | Shenzhen BetterPower Battery Co., Ltd | China | 0.45 | Y | [T023 2026-11-20] Shenzhen Special Zone Daily feature (2023-06-16, via Tencent, S13): Long… |
| StB Giga Factory | StB Giga Factory, Inc. | Philippines | 0.45 | N | [T019 2026-11-20] New Clark City plant: 'initially have a production capacity of 300 MWh a… |
| SVOLT Suining plant | SVOLT (Svolt Energy Technology) | China | 0.45 | Y | [T008 2026-11-20] Phase 1 started production the week of 2022-11-04, 'designed for an annu… |
| Talent New Energy Chongqing Solid-State Plant | Talent New Energy | China | 0.45 | Y | [T024 2026-11-20] Phase 1 0.2 GWh semi-solid line in Liangjiang New Area 'nearly at full c… |
| Gotion Tongcheng battery base (40 GWh power battery project) | Tongcheng Gotion High-Tech | China | 0.45 | Y | [T005 2026-11-20] Confidence 0.45 (D-015 cap: installed figure from 2022-08, >18 months). … |
| Toyota Battery (PEVE) Kosai Plant | Toyota Battery Co., Ltd. (formerly Primearth EV Energy / PEVE) | Japan | 0.45 | Y | [T013 2026-11-20] Toyota Battery Co. (ex-PEVE, HQ Kosai, Shizuoka; wholly-owned by Toyota … |
| UNIGRID San Diego | UNIGRID Battery | United States | 0.45 | Y | [T017 2026-11-20] 12,000 sq ft Sorrento Valley pilot/LRIP sodium-ion cell line funded by a… |
| Waaree ESS Cell Plant (Rola) | Waaree ESS (Waaree Energy Storage Solutions) | India | 0.45 | Y | [T018 2026-11-20] Changed vs v1: under_construction -> announced (no source says cell-line… |
| WeLion Haibo (Zibo) semi-solid-state / solid-state battery base | WeLion Haibo (Zibo) New Energy Technology Co., Ltd. (卫蓝海博（淄博）新能源科技有限公司) | China | 0.45 | N | [T048 2026-11-20] NEW (T048 sweep, Shandong/Zibo). The v1 Huzhou row's notes (T0xx correct… |
| Lingpao Sanming 4 GWh lithium-ion and sodium-ion battery line (Jikou Emerging Industrial Park) | Xiamen Lingpao Lithium Energy Technology Co., Ltd. (厦门领胞锂能科技有限公司) | China | 0.45 | N | [T039 2026-11-20] Fujian, Sanming Economic Development Zone, Jikou Emerging Industrial Par… |
| UniLiB La Plata | Y-TEC | Argentina | 0.45 | Y | [T020 2026-11-20] UniLiB pilot/development plant (Y-TEC + Universidad Nacional de La Plata… |
| FinDreams Yancheng (Sheyang) battery base | Yancheng FinDreams Battery | China | 0.45 | N | [T003 2026-11-20] Xueqiu aggregator post (demonstrably unreliable elsewhere; D-013): 'phas… |
| CosMX Zhuhai Plant (Zhuhai headquarters / polymer lithium-ion battery base) | Zhuhai CosMX Battery Co., Ltd. | China | 0.45 | Y | [T024 2026-11-20] Operator is Zhuhai CosMX (珠海冠宇, 688772); 2025 annual report (S31, p.12) … |
| CosMX Chongqing Plant | Zhuhai CosMX Battery | China | 0.45 | Y | [T024 2026-11-20] Chongqing COSMX Plant II officially put into operation 6 Jan 2020 per co… |

## Appendix — non-cell sites flagged by researchers (7)

Kept in the DB and tagged `is_cell_manufacturer = false`. Filter these out for a pure cell-manufacturing view; they are pack-assembly, material or corporate-HQ entries surfaced by the wide-net seed list.

| plant | operator | country | why flagged (note excerpt) |
|---|---|---|---|
| Amprius Colorado (Brighton) | Amprius Technologies | United States | [T016 2026-11-20] Cancelled. Amprius 10-Q (Q3 2026): lease for Brighton CO facility terminated 2026-01-30 for … |
| CATL Shanghai Lingang battery base (Nanhui New City) | CATL | China | [T002 2026-11-20] cell production unconfirmed; module base per S22. is_cell_manufacturer=false so it drops out… |
| Ganfeng LiEnergy Dongguan Base (赣锋锂电东莞科技 10GWh new-type lithium battery & ESS HQ base) | Ganfeng LiEnergy | China | [T009 2026-11-20] Restored (not removed): site exists and commenced operation 25 Feb 2026 (EnergyTrend 2026-02… |
| Liacon Itzehoe | Liacon | Germany | [T014 2026-11-20] status unconfirmed. No open source shows cell production at Itzehoe: the only company profil… |
| SES AI Woburn | SES AI | United States | [T017 2026-11-20] Woburn MA is SES AI's R&D site (Q3 2026 release dateline WOBURN; company says it is 'headqua… |
| StB Giga Factory | StB Giga Factory, Inc. | Philippines | [T019 2026-11-20] New Clark City plant: 'initially have a production capacity of 300 MWh annually' and product… |
| Sunwoda Shenzhen plant | Sunwoda | China | [T007 2026-11-20] Restored (not removed). Sunwoda's 2025 annual report construction-in-progress table lists tw… |
