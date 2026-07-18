#!/usr/bin/env python3
"""Orchestrator loader for Step 3.

The *live* orchestration (fanning researcher sub-agents out over candidates.csv)
is driven by the main Claude session. This script is the deterministic backend
it calls: it validates each researcher JSON object against the schema and the
CLAUDE.md rules, then loads valid rows into factories.db. Invalid rows are
written to failures.csv with a reason.

Usage:
  # validate + load every JSON in data/researched/ into factories.db
  python scripts/orchestrator.py --load data/researched

  # validate a single file without loading (dry run)
  python scripts/orchestrator.py --validate data/researched/foo.json

  # show current candidate stats
  python scripts/orchestrator.py --stats-candidates candidates.csv
"""
import argparse
import csv
import glob
import json
import os
import re
import sys

import duckdb

DB_PATH = "factories.db"
FAILURES_CSV = "failures.csv"

VALID_STATUS = {"announced", "under_construction", "operational"}
VALID_REGIONS = {
    "China", "USA", "Europe", "South Korea", "Japan",
    "India", "Southeast Asia", "Rest of World",
}

# Every column the loader will write, in insert order.
COLUMNS = [
    "id", "plant_name", "operator", "parent_company", "country", "region",
    "latitude", "longitude", "status", "announced_year", "start_year",
    "nameplate_capacity_gwh", "capacity_ref_year", "capacity_by_year_json",
    "chemistry", "cell_format", "end_market", "jv_partners",
    "source_url", "source_date", "confidence",
]

INT_FIELDS = {"announced_year", "start_year", "capacity_ref_year"}
FLOAT_FIELDS = {"latitude", "longitude", "nameplate_capacity_gwh", "confidence"}


def slugify(*parts):
    s = "-".join(p for p in parts if p)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unknown"


def coerce(obj):
    """Normalise types; return (clean_dict, errors)."""
    errors = []
    out = {c: obj.get(c) for c in COLUMNS}

    # id fallback
    if not out.get("id"):
        out["id"] = slugify(out.get("operator"), out.get("plant_name"), out.get("country"))

    for f in INT_FIELDS:
        v = out.get(f)
        if v in ("", None):
            out[f] = None
        else:
            try:
                out[f] = int(float(v))
            except (ValueError, TypeError):
                errors.append(f"{f} not an int: {v!r}")
                out[f] = None

    for f in FLOAT_FIELDS:
        v = out.get(f)
        if v in ("", None):
            out[f] = None
        else:
            try:
                out[f] = float(v)
            except (ValueError, TypeError):
                errors.append(f"{f} not a number: {v!r}")
                out[f] = None

    # capacity_by_year_json must be a JSON string
    cby = out.get("capacity_by_year_json")
    if isinstance(cby, (dict, list)):
        out["capacity_by_year_json"] = json.dumps(cby)
    elif isinstance(cby, str) and cby.strip():
        try:
            json.loads(cby)
        except json.JSONDecodeError:
            errors.append("capacity_by_year_json not valid JSON")
            out["capacity_by_year_json"] = None
    else:
        out["capacity_by_year_json"] = None

    return out, errors


def validate(obj):
    """Return list of hard errors (empty == valid)."""
    errors = []
    clean, coerce_errors = coerce(obj)
    errors.extend(coerce_errors)

    if not clean.get("plant_name"):
        errors.append("missing plant_name")

    status = clean.get("status")
    if status and status not in VALID_STATUS:
        errors.append(f"invalid status: {status!r}")

    region = clean.get("region")
    if region and region not in VALID_REGIONS:
        errors.append(f"invalid region: {region!r}")

    conf = clean.get("confidence")
    if conf is not None and not (0 <= conf <= 1):
        errors.append(f"confidence out of range: {conf}")

    # Rule 5: any non-null capacity/coords must be backed by a source.
    has_source = bool(clean.get("source_url")) and bool(clean.get("source_date"))
    substantive = any(
        clean.get(f) is not None
        for f in ("nameplate_capacity_gwh", "latitude", "longitude", "status")
    )
    if substantive and not has_source:
        errors.append("substantive values present but no source_url/source_date")

    # Rule 2: capacity present but no reference year -> soft fail (warn via error)
    if clean.get("nameplate_capacity_gwh") is not None and clean.get("capacity_ref_year") is None:
        errors.append("nameplate_capacity_gwh set but capacity_ref_year missing")

    return clean, errors


def load(paths, db=DB_PATH):
    con = duckdb.connect(db)
    loaded, failed = 0, 0
    fail_rows = []
    seen_ids = set(r[0] for r in con.execute("SELECT id FROM factories").fetchall())

    files = []
    for p in paths:
        if os.path.isdir(p):
            files.extend(sorted(glob.glob(os.path.join(p, "*.json"))))
        else:
            files.append(p)

    for fp in files:
        try:
            with open(fp) as fh:
                raw = json.load(fh)
        except (json.JSONDecodeError, OSError) as e:
            fail_rows.append({"file": fp, "id": "", "plant_name": "", "reason": f"unreadable: {e}"})
            failed += 1
            continue

        objs = raw if isinstance(raw, list) else [raw]
        for obj in objs:
            clean, errors = validate(obj)
            if errors:
                fail_rows.append({
                    "file": fp, "id": clean.get("id", ""),
                    "plant_name": clean.get("plant_name", ""),
                    "reason": "; ".join(errors),
                })
                failed += 1
                continue
            if clean["id"] in seen_ids:
                # upsert: replace existing row for this site (no duplicates)
                con.execute("DELETE FROM factories WHERE id = ?", [clean["id"]])
            seen_ids.add(clean["id"])
            vals = [clean[c] for c in COLUMNS]
            placeholders = ", ".join(["?"] * len(COLUMNS))
            con.execute(
                f"INSERT INTO factories ({', '.join(COLUMNS)}) VALUES ({placeholders})",
                vals,
            )
            loaded += 1

    con.close()

    if fail_rows:
        write_failures(fail_rows)
    print(f"Loaded {loaded} rows; {failed} failures.")
    if fail_rows:
        print(f"See {FAILURES_CSV}")
    return loaded, failed


def write_failures(rows):
    exists = os.path.exists(FAILURES_CSV)
    with open(FAILURES_CSV, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "id", "plant_name", "reason"])
        if not exists:
            w.writeheader()
        w.writerows(rows)


def stats_candidates(path):
    with open(path) as fh:
        rows = list(csv.DictReader(fh))
    print(f"Total candidates: {len(rows)}")
    by_region = {}
    for r in rows:
        by_region[r.get("region", "?")] = by_region.get(r.get("region", "?"), 0) + 1
    for reg, n in sorted(by_region.items(), key=lambda x: -x[1]):
        print(f"  {reg:16} {n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--load", nargs="+", metavar="PATH", help="dir(s)/file(s) of researcher JSON to validate + load")
    ap.add_argument("--validate", metavar="FILE", help="validate one JSON file, no load")
    ap.add_argument("--stats-candidates", metavar="CSV")
    ap.add_argument("--db", default=DB_PATH)
    args = ap.parse_args()

    if args.stats_candidates:
        stats_candidates(args.stats_candidates)
    elif args.validate:
        with open(args.validate) as fh:
            obj = json.load(fh)
        clean, errors = validate(obj)
        if errors:
            print("INVALID:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("VALID")
        print(json.dumps(clean, indent=2, default=str))
    elif args.load:
        load(args.load, db=args.db)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
