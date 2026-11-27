#!/usr/bin/env python3
"""Build the battery supply-chain asset database from sourced patches (team/SPEC_SUPPLY_CHAIN.md).

    python3 scripts/sc_build.py

data/supply_chain/patches/*.json (filename order) -> supply_chain.db (tables assets, field_evidence, removed,
units; view assets_active), sc_assets.csv, data/supply_chain/field_evidence.csv, data/supply_chain/removed.csv.
Normalised capacity/production (t LCE, t Ni, t Co, t Mn, ...) are derived with data/supply_chain/units.csv;
a researcher-given *_norm value (from a grade the source states) overrides the default factor.
"""
import glob
import json
import os
import re
import sys
import unicodedata

import duckdb
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "data/supply_chain")
DB = os.path.join(ROOT, "supply_chain.db")

COLUMNS = [
    "id", "asset_name", "step", "commodity", "product", "asset_type", "feedstock", "chemistry",
    "operator", "parent_company", "jv_partners", "ownership_json", "country", "region", "province_state",
    "latitude", "longitude", "geo_precision",
    "status", "project_state", "announced_year", "start_year",
    "capacity", "capacity_unit", "capacity_ref_year", "capacity_norm", "installed_capacity", "installed_as_of",
    "installed_norm", "capacity_by_year_json",
    "production", "production_unit", "production_year", "production_norm", "norm_unit", "production_norm_unit",
    "reserves_resources", "feeds", "offtakers", "end_market",
    "source_url", "source_date", "source_published_date", "confidence", "research_notes",
    "last_verified", "verified_by_task", "reported_fields", "evidence_tier",
]
STEPS = {"mining", "refining", "precursor", "cathode", "anode", "electrolyte", "separator", "foil", "recycling"}
STATUS = {"announced", "under_construction", "operational"}
STATES = {"active", "paused", "cancelled"}
REGIONS = {"China", "East Asia", "Southeast Asia", "South Asia", "Australia & Oceania", "North America",
           "South America", "Europe", "Africa", "Middle East", "Russia & Central Asia"}
NUMERIC = ["latitude", "longitude", "capacity", "capacity_norm", "installed_capacity", "installed_norm",
           "production", "production_norm", "confidence"]
INTS = ["announced_year", "start_year", "capacity_ref_year", "production_year"]


def slugify(*parts):
    s = "-".join(p for p in parts if p)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def units():
    u = pd.read_csv(os.path.join(SC, "units.csv"))
    return {r.capacity_unit: (r.norm_unit, (None if pd.isna(r.factor) else float(r.factor))) for r in u.itertuples()}


def apply_patches():
    df = pd.DataFrame({c: pd.Series(dtype=object) for c in COLUMNS}).set_index("id", drop=False)
    ev_rows, removed, log = [], [], []
    # two passes (D-106): every patch's "add" rows first, then update/fix/remove in filename order, so a
    # lower-numbered task can update an asset added by a higher-numbered one.
    patches = [(os.path.basename(f), json.load(open(f))) for f in sorted(glob.glob(os.path.join(SC, "patches/*.json")))]
    work = [(n, p, r) for n, p in patches for r in p["rows"] if r["action"] == "add"] + \
           [(n, p, r) for n, p in patches for r in p["rows"] if r["action"] != "add"]
    for name, p, r in work:
        task, vdate, sources = p["task"], p["verified_on"], p.get("sources", {})
        if True:
            action, rid, fields = r["action"], r.get("id"), dict(r.get("fields") or {})
            if action == "remove":
                if rid not in df.index:
                    sys.exit(f"ERROR {name}: remove of unknown id {rid}")
                row = df.loc[rid].to_dict()
                row.update(removed_by_task=task, removed_reason=r.get("reason"), removed_on=vdate)
                removed.append(row)
                df = df.drop(rid)
                continue
            if action == "add":
                rid = rid or slugify(fields.get("operator", ""), fields.get("asset_name", ""), fields.get("country", ""))
                fields.pop("id", None)
                if rid in df.index:
                    sys.exit(f"ERROR {name}: add of existing id {rid}; use update")
                new = {c: None for c in COLUMNS}
                new.update(id=rid, project_state="active")
                df.loc[rid] = pd.Series(new, dtype=object)
            elif action in ("update", "fix"):
                if rid not in df.index:
                    sys.exit(f"ERROR {name}: {action} of unknown id {rid}")
            else:
                sys.exit(f"ERROR {name}: unknown action {action}")
            for f, v in fields.items():
                if f not in COLUMNS or f == "id":
                    sys.exit(f"ERROR {name}: {rid} sets unknown field {f}")
                df.at[rid, f] = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
            if "confidence" in r:
                df.at[rid, "confidence"] = r["confidence"]
            if r.get("notes"):
                prev = df.at[rid, "research_notes"]
                tag = f"[{task}{' fix' if action == 'fix' else ''} {vdate}] {r['notes']}"
                df.at[rid, "research_notes"] = f"{prev} || {tag}" if isinstance(prev, str) and prev else tag
            if action != "fix":
                df.at[rid, "last_verified"], df.at[rid, "verified_by_task"] = vdate, task
            rep_now = []
            for f, sids in (r.get("evidence") or {}).items():
                tiers = []
                for sid in sids:
                    s = sources.get(sid)
                    if s is None:
                        sys.exit(f"ERROR {name}: {rid} cites unknown source {sid}")
                    t = "reported" if s.get("tier") == "reported" else "confirmed"
                    tiers.append(t)
                    ev_rows.append(dict(id=rid, field=f, task=task, source_id=f"{task}:{sid}", url=s.get("url"),
                                        publisher=s.get("publisher"), published=s.get("published"),
                                        accessed=s.get("accessed"), language=s.get("language"),
                                        quote=s.get("quote") or s.get("snippet"), tier=t))
                if tiers and all(t == "reported" for t in tiers):
                    rep_now.append(f)
            prev = df.at[rid, "reported_fields"]
            prev = json.loads(prev) if isinstance(prev, str) and prev else []
            new_rep = sorted((set(prev) - set((r.get("evidence") or {}).keys())) | set(rep_now))
            df.at[rid, "reported_fields"] = json.dumps(new_rep) if new_rep else None
            log.append(f"{task}: {action} {rid}")
    return df, pd.DataFrame(ev_rows), pd.DataFrame(removed), log


COUNTRY_ALIASES = {"DRC": "Democratic Republic of the Congo", "Congo (Kinshasa)": "Democratic Republic of the Congo",
                   "USA": "United States", "US": "United States", "Korea": "South Korea",
                   "Korea, Republic of": "South Korea", "Czechia": "Czech Republic", "UK": "United Kingdom"}


def normalise(df):
    df["country"] = df["country"].map(lambda c: COUNTRY_ALIASES.get(c, c))
    u = units()
    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for i, r in df.iterrows():
        nu, fac = u.get(r.capacity_unit, (None, None)) if isinstance(r.capacity_unit, str) else (None, None)
        pu, pfac = u.get(r.production_unit, (None, None)) if isinstance(r.production_unit, str) else (None, None)
        df.at[i, "norm_unit"] = r.norm_unit if isinstance(r.norm_unit, str) and r.norm_unit else (nu or pu)
        if pd.isna(r.capacity_norm) and fac is not None and pd.notna(r.capacity):
            df.at[i, "capacity_norm"] = round(r.capacity * fac, 1)
        if pd.isna(r.installed_norm) and fac is not None and pd.notna(r.installed_capacity):
            df.at[i, "installed_norm"] = round(r.installed_capacity * fac, 1)
        if pd.isna(r.production_norm) and pfac is not None and pd.notna(r.production):
            df.at[i, "production_norm"] = round(r.production * pfac, 1)
        if pd.notna(df.at[i, "production_norm"]):
            # researcher-given production_norm is in the row's norm_unit; otherwise the unit's own norm unit
            df.at[i, "production_norm_unit"] = pu if (pd.isna(r.production_norm) and pu) else df.at[i, "norm_unit"]
    return df


def main():
    df, ev, removed, log = apply_patches()
    df = normalise(df)

    def _tier(rf):
        fl = json.loads(rf) if isinstance(rf, str) and rf else []
        return "reported" if set(fl) & {"status", "capacity", "installed_capacity", "production"} else "confirmed"
    df["evidence_tier"] = df["reported_fields"].map(_tier)
    for c in INTS:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    df = df[COLUMNS].reset_index(drop=True).sort_values(["step", "commodity", "id"]).reset_index(drop=True)
    df.to_csv(os.path.join(ROOT, "sc_assets.csv"), index=False)
    ev_cols = ["id", "field", "task", "source_id", "url", "publisher", "published", "accessed", "language", "quote", "tier"]
    ev = ev if len(ev) else pd.DataFrame(columns=ev_cols)
    ev.to_csv(os.path.join(SC, "field_evidence.csv"), index=False)
    removed.to_csv(os.path.join(SC, "removed.csv"), index=False)
    if os.path.exists(DB):
        os.remove(DB)
    con = duckdb.connect(DB)
    con.register("df", df)
    con.execute("CREATE TABLE assets AS SELECT * FROM df")
    con.execute("CREATE VIEW assets_active AS SELECT * FROM assets WHERE coalesce(project_state,'active')='active'")
    con.register("ev", ev.astype(str))
    con.execute("CREATE TABLE field_evidence AS SELECT * FROM ev")
    con.register("un", pd.read_csv(os.path.join(SC, "units.csv")))
    con.execute("CREATE TABLE units AS SELECT * FROM un")
    con.close()
    print(f"sc_build OK: {len(df)} assets, {len(ev)} evidence links, {len(removed)} removed, "
          f"{len(set(l.split(':')[0] for l in log))} patch files")
    if len(df):
        print(df.groupby(["step", "status"]).size().unstack(fill_value=0).to_string())


if __name__ == "__main__":
    main()
