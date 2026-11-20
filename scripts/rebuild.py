#!/usr/bin/env python3
"""Rebuild the database from durable repo files: baseline snapshot + sourced patches.

    python3 scripts/rebuild.py            # writes factories.db, factories_export.csv,
                                          # data/field_evidence.csv, data/removed.csv

Inputs
  data/baseline/factories_v1.csv   frozen v1 export (378 rows, pre-team state)
  data/patches/*.json              one file per task, applied in filename order

Patch file format (see team/CONVENTIONS.md for the full contract):
  {"task": "T003", "verified_on": "2026-11-20",
   "sources": {"S1": {"url": ..., "publisher": ..., "published": "YYYY-MM-DD"|null,
                      "accessed": "YYYY-MM-DD", "language": "en", "quote": "verbatim"}},
   "rows": [{"id": ..., "action": "update"|"add"|"remove",
             "fields": {...}, "evidence": {"field": ["S1", ...]},
             "confidence": 0.8, "notes": "...", "reason": "..."}]}

`update` and `add` stamp last_verified = verified_on. Fields not named keep their
previous value. `remove` moves the row to data/removed.csv with its reason; rows are
never silently dropped.
"""
import glob
import json
import os
import re
import sys

import duckdb
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "data/baseline/factories_v1.csv")
PATCH_GLOB = os.path.join(ROOT, "data/patches/*.json")
DB = os.path.join(ROOT, "factories.db")

V1_COLUMNS = list(pd.read_csv(BASELINE, nrows=0).columns)
NEW_COLUMNS = [
    "project_state",            # active | paused | cancelled
    "installed_capacity_gwh",   # GWh/yr actually installed (commissioned) as of installed_as_of
    "installed_as_of",          # YYYY-MM-DD or YYYY
    "site_type",                # single_site | hub (aggregate of adjacent plants in one city)
    "geo_precision",            # site | town | city | none
    "source_published_date",    # publication date of source_url (source_date = accessed/legacy)
    "last_verified",            # date of the team re-verification (null = v1, unverified)
    "verified_by_task",
    "reported_fields",          # JSON list: fields whose value is REPORTED (v1 or snippet), not confirmed by a v2 quote
    "evidence_tier",            # confirmed | reported (reported if status/capacity rests on a reported value)
]
COLUMNS = V1_COLUMNS + NEW_COLUMNS


def slugify(*parts):
    s = "-".join(p for p in parts if p)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return re.sub(r"-+", "-", s).strip("-")


def geo_precision(row):
    note = str(row.get("research_notes") or "")
    if pd.isna(row.get("latitude")):
        return "none"
    for tier in ("site", "town", "city"):
        if f"[GEO={tier}:" in note:
            return tier
    return "site_unflagged"  # v1 researcher-supplied coordinates, precision not recorded


def load_baseline():
    df = pd.read_csv(BASELINE)
    for c in NEW_COLUMNS:
        df[c] = None
    df["project_state"] = "active"
    df["site_type"] = df["is_single_site"].map({True: "single_site", False: "hub"})
    df["geo_precision"] = df.apply(geo_precision, axis=1)
    return df.set_index("id", drop=False)


def apply_patches(df):
    evidence_rows, removed_rows, log = [], [], []
    skip = set(filter(None, os.environ.get("REBUILD_EXCLUDE", "").split(",")))
    for path in sorted(glob.glob(PATCH_GLOB)):
        if os.path.basename(path) in skip:
            continue
        p = json.load(open(path))
        task, vdate, sources = p["task"], p["verified_on"], p.get("sources", {})
        for r in p["rows"]:
            action = r["action"]
            rid = r.get("id")
            fields = dict(r.get("fields") or {})
            if action == "fix":
                # lead-only integration fix: change fields without stamping re-verification
                if rid not in df.index:
                    sys.exit(f"ERROR {os.path.basename(path)}: fix of unknown id {rid}")
                for f, v in fields.items():
                    if f not in COLUMNS or f == "id":
                        sys.exit(f"ERROR {os.path.basename(path)}: {rid} fixes unknown field {f}")
                    df.at[rid, f] = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                for f, url in (r.get("reported_evidence") or {}).items():
                    evidence_rows.append(dict(id=rid, field=f, task=task, source_id=f"{task}:reported", url=url,
                                              publisher="v1 source (not re-confirmed in v2)", published=None,
                                              accessed=None, language=None, quote=None, tier="reported"))
                if r.get("notes"):
                    prev = df.at[rid, "research_notes"]
                    df.at[rid, "research_notes"] = f"{prev} [{task} fix {vdate}] {r['notes']}" if isinstance(prev, str) else f"[{task} fix {vdate}] {r['notes']}"
                log.append(f"{task}: fix {rid} ({len(fields)} fields)")
                continue
            if action == "remove":
                if rid not in df.index:
                    sys.exit(f"ERROR {os.path.basename(path)}: remove of unknown id {rid}")
                row = df.loc[rid].to_dict()
                row.update(removed_by_task=task, removed_reason=r.get("reason"), removed_on=vdate,
                           removal_sources=";".join(r.get("evidence", {}).get("_remove", [])))
                removed_rows.append(row)
                df = df.drop(rid)
                log.append(f"{task}: remove {rid} ({r.get('reason')})")
                continue
            if action == "add":
                rid = rid or fields.pop("id", None)
                fields.pop("id", None)
                if not rid:
                    rid = slugify(fields.get("operator", ""), fields.get("plant_name", ""), fields.get("country", ""))
                if rid in df.index:
                    sys.exit(f"ERROR {os.path.basename(path)}: add of existing id {rid}; use update")
                new = {c: None for c in COLUMNS}
                new.update(id=rid, project_state="active")
                df.loc[rid] = pd.Series(new)
            elif action == "update":
                if rid not in df.index:
                    sys.exit(f"ERROR {os.path.basename(path)}: update of unknown id {rid}")
            else:
                sys.exit(f"ERROR {os.path.basename(path)}: unknown action {action}")
            for f, v in fields.items():
                if f not in COLUMNS or f == "id":
                    sys.exit(f"ERROR {os.path.basename(path)}: {rid} sets unknown field {f}")
                if isinstance(v, (dict, list)):
                    v = json.dumps(v, ensure_ascii=False)
                df.at[rid, f] = v
            if "confidence" in r:
                df.at[rid, "confidence"] = r["confidence"]
            if r.get("notes"):
                df.at[rid, "research_notes"] = f"[{task} {vdate}] {r['notes']}"
            df.at[rid, "last_verified"] = vdate
            df.at[rid, "verified_by_task"] = task
            rep_now = []
            for f, sids in (r.get("evidence") or {}).items():
                tiers = []
                for sid in sids:
                    s = sources.get(sid, {})
                    t = "reported" if s.get("tier") == "reported" else "confirmed"
                    tiers.append(t)
                    evidence_rows.append(dict(id=rid, field=f, task=task, source_id=f"{task}:{sid}",
                                              url=s.get("url"), publisher=s.get("publisher"),
                                              published=s.get("published"), accessed=s.get("accessed"),
                                              language=s.get("language"), quote=s.get("quote") or s.get("snippet"),
                                              tier=t))
                if tiers and all(t == "reported" for t in tiers):
                    rep_now.append(f)
            # a field re-evidenced in this patch takes the tier of its new evidence
            prev = df.at[rid, "reported_fields"] if "reported_fields" in df.columns else None
            prev = json.loads(prev) if isinstance(prev, str) else []
            new_rep = sorted((set(prev) - set((r.get("evidence") or {}).keys())) | set(rep_now))
            df.at[rid, "reported_fields"] = json.dumps(new_rep) if new_rep else None
            log.append(f"{task}: {action} {rid} ({len(fields)} fields)")
    return df, pd.DataFrame(evidence_rows), pd.DataFrame(removed_rows), log


def main():
    df, ev, removed, log = apply_patches(load_baseline())
    def _tier(rf):
        try:
            fl = json.loads(rf) if isinstance(rf, str) else []
        except json.JSONDecodeError:
            fl = []
        return "reported" if set(fl) & {"status", "nameplate_capacity_gwh", "installed_capacity_gwh"} else "confirmed"
    df["evidence_tier"] = df["reported_fields"].map(_tier)
    df = df[COLUMNS].reset_index(drop=True).sort_values("id").reset_index(drop=True)
    for c in ["latitude", "longitude", "nameplate_capacity_gwh", "installed_capacity_gwh", "confidence"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["announced_year", "start_year", "capacity_ref_year"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    df.to_csv(os.path.join(ROOT, "factories_export.csv"), index=False)
    ev_cols = ["id", "field", "task", "source_id", "url", "publisher", "published", "accessed", "language", "quote", "tier"]
    (ev if len(ev) else pd.DataFrame(columns=ev_cols)).to_csv(os.path.join(ROOT, "data/field_evidence.csv"), index=False)
    removed.to_csv(os.path.join(ROOT, "data/removed.csv"), index=False)
    if os.path.exists(DB):
        os.remove(DB)
    con = duckdb.connect(DB)
    con.register("df", df)
    con.execute("CREATE TABLE factories AS SELECT * FROM df")
    con.execute("ALTER TABLE factories ADD PRIMARY KEY (id)")
    # Active, comparable cell plants: what every capacity aggregate should use (D-003, D-018, D-019)
    nc = os.path.join(ROOT, "data/reference/non_comparable.csv")
    nc_ids = list(pd.read_csv(nc).id) if os.path.exists(nc) else []
    con.register("nc", pd.DataFrame({"id": nc_ids or ["__none__"]}))
    con.execute("CREATE TABLE non_comparable AS SELECT * FROM nc")
    con.execute("""CREATE VIEW factories_active AS SELECT * FROM factories
                   WHERE coalesce(is_cell_manufacturer, true) AND coalesce(project_state, 'active') = 'active'
                     AND id NOT IN (SELECT id FROM non_comparable)""")
    if len(ev):
        con.register("ev", ev)
        con.execute("CREATE TABLE field_evidence AS SELECT * FROM ev")
    if len(removed):
        con.register("rm", removed.astype(str))
        con.execute("CREATE TABLE removed AS SELECT * FROM rm")
    con.close()
    print(f"rebuild OK: {len(df)} rows, {len(ev)} evidence links, {len(removed)} removed, "
          f"{len(set(l.split(':')[0] for l in log))} patch files")


if __name__ == "__main__":
    main()
