#!/usr/bin/env python3
"""Import the CGS (Univ. of Maryland) Nickel Smelter Dataset V1 (CC BY 4.0, doi:10.5281/zenodo.17701177) as a patch.

Writes team/evidence/open_datasets/cgs_nickel_smelters_key.csv (key columns, committed, attribution kept) and
data/supply_chain/patches/SCN_cgs_nickel.json: updates for smelters already in the database (manual id map below),
adds for the rest, removes for duplicate rows created by overlapping first passes. Quotes are full CSV lines of the
key-column file, which verify_quotes reads locally (team/evidence/open_datasets/LOCAL.csv).
"""
import csv, json, os, re, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sc_build import slugify  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "team/evidence/open_datasets/CGS_Nickel_Smelter_Dataset_V1.xlsx")
KEY = os.path.join(ROOT, "team/evidence/open_datasets/cgs_nickel_smelters_key.csv")
URL = "https://zenodo.org/records/17701177/files/CGS_Nickel_Smelter_Dataset_V1.xlsx"
MAP = {  # CGS row index -> existing asset id (checked by hand, 2026-11-27)
    1: "pt-aneka-tambang-pomalaa-ferronickel-indonesia", 4: "nickel-industries-angel-nickel-indonesia",
    19: "excelsior-nickel-cobalt-enc-hpal-indonesia", 22: "pt-gunbuster-nickel-industry-npi-indonesia",
    23: "pt-halmahera-persada-lygend-hpal-indonesia", 25: "nickel-industries-hengjaya-nickel-indonesia",
    27: "huayou-huake-rkef-indonesia", 28: "huayue-nickel-cobalt-hnc-hpal-indonesia",
    33: "huayou-pomalaa-hpal-indonesia", 38: "pt-obsidian-stainless-steel-oss-npi-indonesia",
    39: "gem-qmb-hpal-indonesia", 40: "nickel-industries-ranger-nickel-indonesia",
    48: "pt-vale-indonesia-sorowako-matte-indonesia", 49: "pt-virtue-dragon-nickel-industry-npi-indonesia",
    55: "shengtun-mining-youshan-nickel-indonesia", 56: "huayou-huafei-nickel-cobalt-hpal-indonesia",
    58: "pt-vale-huayou-sorowako-hpal-indonesia", 73: "pt-obi-nickel-cobalt-hpal-indonesia",
    75: "pt-halmahera-jaya-feronikel-rkef-indonesia", 77: "pt-karunia-permai-sentosa-rkef-indonesia",
    80: "merdeka-battery-materials-nickel-matte-converter-indonesia", 81: "pt-esg-new-energy-material-hpal-indonesia",
    82: "nickel-industries-oracle-nickel-indonesia", 100: "cngr-nadesico-low-matte-indonesia",
    101: "cngr-debonair-low-matte-indonesia", 103: "cngr-ding-xing-refined-nickel-indonesia",
}
SKIP = {8: "Bahodopi: CGS lists HPAL/MHP, company sources describe the Vale-Tisco-Xinhai RKEF; conflict kept in notes of "
            "pt-vale-indonesia-bahodopi-rkef-indonesia, not imported",
        11: "MBMA RKEF (Bukit) is inside the MBMA RKEF aggregate row", 13: "MBMA RKEF (Cahaya) inside aggregate",
        34: "MBMA RKEF (Lestari) inside aggregate", 71: "MBMA RKEF (Zhao Hui) inside aggregate"}
REMOVE = {  # duplicate rows from overlapping first passes -> kept id
    "huayou-huake-nickel-indonesia-pyro-indonesia": "huayou-huake-rkef-indonesia",
    "huayou-huayue-hpal-indonesia": "huayue-nickel-cobalt-hnc-hpal-indonesia",
    "huayou-huafei-hpal-indonesia": "huayou-huafei-nickel-cobalt-hpal-indonesia",
    "huayou-sorowako-hpal-indonesia": "pt-vale-huayou-sorowako-hpal-indonesia",
    "pt-kni-pomalaa-hpal-indonesia": "huayou-pomalaa-hpal-indonesia",
    "huayou-huaxing-pyro-indonesia": "huayou-huaxing-rkef-indonesia",
    "huayou-qingtian-pyro-indonesia": "huayou-qingtian-rkef-indonesia",
    "gem-vale-danantara-igip-indonesia": "gem-igip-nickel-hpal-indonesia",
    "pt-qmb-new-energy-materials-hpal-indonesia": "gem-qmb-hpal-indonesia",
}
UNIT = {"NPI": "t NPI Ni", "FeNi": "t NPI Ni", "Ni Matte": "t Ni in matte", "MHP": "t Ni in MHP", "MSP": "t Ni in MHP",
        "Ni Sulfate": "t Ni", "Electrolytic Ni": "t Ni"}
STATUS = {"Operating": ("operational", "active", 0.6), "Construction": ("under_construction", "active", 0.55),
          "Planned": ("announced", "active", 0.45), "Stalled": ("announced", "paused", 0.35),
          "Unclear": ("announced", "paused", 0.3), "No longer operational": ("operational", "paused", 0.45)}
GEO = {"Exact": "site", "Approximate within a group of smelters": "town", "Construction": "town"}  # audit: construction-site points are approximate


def main():
    d = pd.read_excel(SRC, "Nickel_smelters")
    d.columns = [c.strip() for c in d.columns]
    keep = ["Smelter Name", "Industrial Park Name", "Operating Owner", "Province", "Regency", "Latitude", "Longitude",
            "Location Status", "Process", "Output Product", "Output Capacity (Tonnes)", "Ni metal equivalent (tonnes)",
            "Status 2025"]
    k = d[keep].copy()
    k.insert(0, "row", range(len(k)))
    k.to_csv(KEY, index=False)
    lines = open(KEY, encoding="utf-8").read().splitlines()[1:]
    src, rows = {}, []
    for i, r in d.iterrows():
        if i in SKIP:
            continue
        st = str(r["Status 2025"]).strip()
        status, state, conf = STATUS.get(st, ("announced", "paused", 0.3))
        sid = f"C{i}"
        q = lines[i]
        if len(q) > 300:
            q = q[:297].rsplit(",", 1)[0]
        src[sid] = {"url": URL, "publisher": f"CGS Nickel Smelter Dataset V1 (Univ. of Maryland, CC BY 4.0), row {i}; local key "
                    "columns team/evidence/open_datasets/cgs_nickel_smelters_key.csv", "published": "2025-01-04",
                    "accessed": "2026-11-27", "language": "en", "quote": q}
        prod = str(r["Output Product"]).strip()
        unit = UNIT.get(prod)
        nieq = r["Ni metal equivalent (tonnes)"]
        f = {"status": status, "project_state": state}
        ev = {"status": [sid]}
        if unit and pd.notna(nieq):
            f.update(capacity=float(nieq), capacity_unit=unit, capacity_ref_year=2025)
            ev["capacity"] = [sid]
        ls = str(r["Location Status"]).strip()
        if ls in GEO and pd.notna(r["Latitude"]) and pd.notna(r["Longitude"]):
            f.update(latitude=round(float(r["Latitude"]), 5), longitude=round(float(r["Longitude"]), 5), geo_precision=GEO[ls])
        note = (f"CGS dataset: {r['Process']} → {prod}, gross output {r['Output Capacity (Tonnes)']} t, Ni-equivalent {nieq} t; "
                f"status 2025 '{st}'; park {r['Industrial Park Name']}; location status '{ls}'.")
        if i in MAP:
            # updates: add coordinates always; capacity/status only where the row has none (company sources keep priority)
            upd = {k2: v for k2, v in f.items() if k2 in ("latitude", "longitude", "geo_precision")}
            rows.append({"action": "update", "id": MAP[i], "fields": upd, "evidence": {},
                         "notes": note + " Coordinates from CGS; status/capacity kept from company sources (CGS values in this note)."})
            rows[-1]["_cgs"] = {"f": f, "ev": ev}
            continue
        name = str(r["Smelter Name"]).strip()
        f.update(asset_name=name, step="refining", commodity="nickel", product=prod if prod != "nan" else None,
                 asset_type=f"{r['Process']} smelter", operator=str(r["Operating Owner"]).strip(), country="Indonesia",
                 region="Southeast Asia", province_state=None if pd.isna(r["Province"]) else str(r["Province"]).strip(),
                 source_url=URL, source_date="2026-11-27", source_published_date="2025-01-04")
        rows.append({"action": "add", "id": slugify(name, "indonesia"), "fields": f, "evidence": ev,
                     "confidence": conf if unit else min(conf, 0.5), "notes": note})
    # for updated rows, fill capacity/status only when missing in the current DB
    a = pd.read_csv(os.path.join(ROOT, "sc_assets.csv")).set_index("id")
    for r in rows:
        c = r.pop("_cgs", None)
        if not c:
            continue
        cur = a.loc[r["id"]]
        if pd.isna(cur.capacity) and "capacity" in c["f"]:
            r["fields"].update({k2: c["f"][k2] for k2 in ("capacity", "capacity_unit", "capacity_ref_year")})
            r["evidence"]["capacity"] = c["ev"]["capacity"]
        if pd.isna(cur.latitude) is False:
            for k2 in ("latitude", "longitude", "geo_precision"):
                r["fields"].pop(k2, None)
    for rid, kept in REMOVE.items():
        rows.append({"action": "remove", "id": rid, "reason": f"duplicate of {kept} (overlapping first passes; CGS dataset check)"})
    patch = {"task": "SCN_cgs_nickel", "verified_on": "2026-11-27", "sources": src, "rows": rows}
    json.dump(patch, open(os.path.join(ROOT, "data/supply_chain/patches/SCN_cgs_nickel.json"), "w"), ensure_ascii=False, indent=1)
    print(len([r for r in rows if r["action"] == "add"]), "adds,", len([r for r in rows if r["action"] == "update"]), "updates,",
          len(REMOVE), "removes")


if __name__ == "__main__":
    main()
