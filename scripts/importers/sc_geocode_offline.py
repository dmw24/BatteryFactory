import sys,re,json
sys.path.insert(0,'/tmp/claude-0/-home-user-BatteryFactory/cf603490-000c-57a0-a1e1-fea4fe5d2c58/scratchpad')
from cand import *
d=pd.read_csv('/home/user/BatteryFactory/sc_assets.csv').set_index('id')
MINE_OK={'zijin-musonoi-kolwezi-drc','cmoc-tenke-fungurume-tfm-drc','kobold-manono-roche-dure-drc','zijin-manono-northeast-mine-drc','yichun-tantalum-niobium-mine-414-china','critical-metals-wolfsberg-austria'}
# alias strings that are region/state/company/common words, never localities
DROP={'anda','zhonghe','beisu','boa sorte','mulia','deli','toyo','annex','green','asia','salto','centenario','carlton','pest','quebec','baden','brandenburg','bahia','mozambique','sungai raya','singapore','abu dhabi','holguin','el jadida','opole','tokushima','osaka','esztergom','tianzhuang','hengshan'}
SKIP={
 'lg-chem-cheongju-cathode-south-korea':'multi-site (Cheongju + Iksan)',
 'enchem-poland-lower-silesia-poland':'near-only reference (near Wroclaw)',
 'gem-china-battery-recycling-aggregate-china':'aggregate of plants in several cities',
 'sumitomo-metal-mining-toyo-niihama-japan':'two distant sites (Saijo + Niihama)',
 'shangtai-beisu-phase-2-wuji-china':'named locality (Wuji) not in gazetteer; gazetteer hit was a company-name coincidence',
 'titan-lithium-kezad-abu-dhabi-lithium-plant-united-arab-emirates':'KEZAD zone not in gazetteer; only emirate-level match',
 'nextsource-battery-anode-facility-abu-dhabi-united-arab-emirates':'emirate-level only',
 'tes-tes-b-lithium-ion-recycling-singapore':'city-state (would be country centroid)',
 'sinoma-lithium-film-tengzhou-china':'gazetteer alias Tengzhou->Chengtangcun not an unambiguous city match',
 'tinci-jorf-lasfar-integrated-morocco':'Jorf Lasfar port not in gazetteer; El Jadida is the province',
 'cngr-morocco-pcam-morocco':'El Jadida region only',
 'lg-toray-hungary-battery-separator-nyergesujfalu-hungary':'Nyergesujfalu not in gazetteer; only county-level match',
 'huayou-arcadia-sulphate-plant-zimbabwe':'near-only reference (near Harare)',
 'polar-lithium-kolmozerskoye-chemical-plant-russia':'oblast-level only; site not named',
 'sinomine-bikita-sulphate-plant-zimbabwe':'province-level only (Masvingo); plant is at Bikita',
 'smm-taganito-hpal-nickel-philippines':'province-level only (Surigao); plant is at Taganito/Claver',
 'librec-biberist-switzerland':'canton-level only (Solothurn); Biberist not in gazetteer',
 'sln-doniambo-ferronickel-new-caledonia':'row combines smelter and mines in several places',
 'toray-industries-hungary-nyergesujfalu-hungary':'Nyergesujfalu not in gazetteer; only county-level match',
}
FORCE={
 'ruitai-huarong-ningde-400kt-electrolyte-china':'fuding','ruitai-huarong-ningde-80kt-electrolyte-china':'fuding',
 'qingdao-haida-ruiyuan-pingdu-china':'qingdao','ionway-nysa-cathode-poland':'nysa','umicore-nysa-cathode-poland':'nysa',
 'nichia-anan-cathode-japan':'anan','enchem-hungary-komarom-hungary':'komarom','ube-maxell-sakai-japan':'sakai',
 'li-cycle-rochester-hub-new-york-usa':'rochester','li-cycle-rochester-spoke-new-york-usa':'rochester',
 'umicore-hoboken-battery-recycling-belgium':'hoboken','nornickel-kola-mmc-cobalt-russia':'monchegorsk',
 'weiling-guixi-lingneng-lithium-carbonate-china':'guixi','asahi-kasei-hyuga-japan':'hyuga','asahi-kasei-moriyama-japan':'moriyama',
 'volta-energy-solutions-granby-canada':'granby','sungeel-hungary-szigetszentmiklos-hungary':'szigetszentmiklos',
 'cnbm-heilongjiang-graphite-jixi-purification-china':'jixi','graphite-one-ohio-anode-plant-united-states':'warren','tinci-yichang-30wt-fepo4-china':'yichang',
 'ecopro-bm-ochang-south-korea':'cheongju','solus-advanced-materials-tatabanya-plant-1-hungary':'tatabanya',
 'solus-advanced-materials-tatabanya-plant-2-hungary':'tatabanya','btr-dali-xiangyun-anode-china':'xiangyun',
 'china-minmetals-graphite-yunshan-china':'hegang','citic-guoan-mengguli-beijing-changping-china':'changping',
 'zhongke-hunan-xingcheng-ningxiang-china':'ningxiang','sungeel-hitech-saemangeum-no3-south-korea':'gunsan',
 'capchem-nantong-electrolyte-china':'nantong','kokkola':None,
}
FORCE={k:v for k,v in FORCE.items() if v}
NOTES_OK={
 'wanrun-anhui-china':('anqing','notes: Anhui base is Anqing Derun New Energy Materials (annual report)'),
 'hunan-yuneng-sichuan-yuning-china':('suining','notes: entity located in Suining (annual report)'),
 'hunan-yuneng-sichuan-yuneng-china':('suining','notes: main operating place Suining (annual report)'),
 'hunan-yuneng-yunnan-yuneng-china':('anning','notes: main operating place Anning (annual report)'),
 'hunan-yuneng-circular-xiangxiang-lithium-carbonate-china':('xiangxiang','notes: main operating place Xiangxiang (subsidiary filing)'),
 'anda-kaiyang-450kt-lfp-precursor-china':('guiyang','notes: planned in Kaiyang, Guiyang'),
 'jinchuan-ruashi-drc':('lubumbashi','notes: Ruashi mine 5 km east of Lubumbashi (Jinchuan page)'),
}
def spread(hs):
    return max((hav(a,b) for a in hs for b in hs),default=0)
def resolve_homonyms(hs, other_admins):
    if spread(hs)<=50: return max(hs,key=lambda r:r['population']),None
    f=[h for h in hs if h['admin1code'] in other_admins]
    if f and spread(f)<=50: return max(f,key=lambda r:r['population']),None
    return None,'homonym places >50 km apart'
out=[];skipped=[]
m=d[d.latitude.isna()]
for i,r in m.iterrows():
    iso=cbn.get(norm(r.country)); nm=r.asset_name; pr=r.province_state if isinstance(r.province_state,str) else ''
    if i in SKIP: skipped.append((i,'locality ambiguous/unsuitable',SKIP[i])); continue
    if r.step=='mining' and i not in MINE_OK:
        skipped.append((i,'mine/deposit (locality is a region, not the mine site)','')); continue
    if iso not in idx: skipped.append((i,'no gazetteer for country','')); continue
    src='name'
    pv=provs(nm+' || '+pr,iso)
    cn=[c for c in find(nm,iso,pv) if c[0] not in DROP]
    cp=[c for c in find(pr,iso,pv) if c[0] not in DROP]
    cands=cn or cp
    if cn: src='asset_name'
    elif cp: src='province_state'
    if i in NOTES_OK:
        a,why=NOTES_OK[i]; cands=[c for c in find(r.research_notes,iso,provs(r.research_notes,iso)) if c[0]==a][:1]; src=why
    if not cands:
        skipped.append((i,'no locality named / not in gazetteer (<15k pop or not matched)','')); continue
    # force
    if i in FORCE:
        cands=[c for c in cands+cp+cn if c[0]==FORCE[i]][:1]
        if not cands: print('FORCE FAIL',i); continue
    admins={c[1]['admin1code'] for c in cands}
    places=[]
    for a,h,sp,amb,hs in cands:
        hh,why=resolve_homonyms(hs,admins-{None}) if len(hs)>1 else (hs[0],None)
        if hh is None: continue
        if (a,hh['geonameid'] if 'geonameid' in hh else hh['name']) not in [(x[0],x[2]['geonameid'] if 'geonameid' in x[2] else x[2]['name']) for x in places]:
            places.append((a,why,hh))
    if not places: skipped.append((i,'locality ambiguous',' homonyms')); continue
    uniq={(round(p[2]['latitude'],2),round(p[2]['longitude'],2)):p for p in places}
    pl=list(uniq.values())
    if len(pl)>1:
        hs=[p[2] for p in pl]
        if spread(hs)>60: skipped.append((i,'locality ambiguous',' / '.join(p[2]['name'] for p in pl))); continue
        pick=min(pl,key=lambda p:p[2]['population'])
    else: pick=pl[0]
    a,_,h=pick
    prec='town' if h['population']<100000 else 'city'
    out.append(dict(id=i,alias=a,name=h['name'],lat=round(h['latitude'],4),lon=round(h['longitude'],4),prec=prec,src=src,pop=h['population'],admin=h['admin1code'],cc=iso,text=(nm+' || '+pr)[:110]))
json.dump(out,open('/tmp/claude-0/-home-user-BatteryFactory/cf603490-000c-57a0-a1e1-fea4fe5d2c58/scratchpad/out.json','w'),ensure_ascii=False)
json.dump(skipped,open('/tmp/claude-0/-home-user-BatteryFactory/cf603490-000c-57a0-a1e1-fea4fe5d2c58/scratchpad/skipped.json','w'),ensure_ascii=False)
print(len(out),len(skipped))
for o in out: print(o['id'][:48],'|',o['alias'],'->',o['name'],o['admin'],o['prec'],o['lat'],o['lon'],'|',o['src'][:10])
