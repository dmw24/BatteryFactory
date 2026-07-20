#!/usr/bin/env python3
"""Load capacity_timeline results into factories.db.

Usage: python scripts/load_timelines.py <source>
  <source> is either
    * a capacity-history workflow journal (.jsonl, one {"type":"result",...} per line), or
    * the committed data/timelines.json snapshot (a plain JSON array of
      {id, is_single_site, capacity_timeline}). This is the rebuild path: the
      DuckDB binary is gitignored, so data/timelines.json is the durable,
      in-repo source of truth for the real sourced capacity histories.

Validates that every datapoint carries a source_url + source_date (drops those
that don't), stores the timeline JSON and is_single_site on each row by id.
"""
import json
import sys
import duckdb


def _records(source):
    """Yield {id, timeline, is_single_physical_site} dicts from either format."""
    if source.endswith(".json"):
        arr = json.load(open(source))
        for r in arr if isinstance(arr, list) else []:
            if isinstance(r, dict):
                yield {"id": r.get("id"),
                       "timeline": r.get("capacity_timeline") or r.get("timeline"),
                       "is_single_physical_site": r.get("is_single_site",
                                                        r.get("is_single_physical_site", True))}
        return
    for line in open(source):
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if o.get("type") == "result" and isinstance(o.get("result"), dict):
            yield o["result"]


def main():
    journal = sys.argv[1]
    con = duckdb.connect("factories.db")
    cols = [c[1] for c in con.execute("PRAGMA table_info('factories')").fetchall()]
    if "is_single_site" not in cols:
        con.execute("ALTER TABLE factories ADD COLUMN is_single_site BOOLEAN")

    loaded = pts = bad = skipped = 0
    for r in _records(journal):
        if not isinstance(r, dict):
            continue
        rid, tl = r.get("id"), r.get("timeline")
        if not rid or not isinstance(tl, list):
            continue
        clean = []
        for p in tl:
            if not isinstance(p, dict):
                continue
            if not (p.get("source_url") and p.get("source_date")):
                bad += 1
                continue
            clean.append(p)
        if not con.execute("SELECT 1 FROM factories WHERE id=?", [rid]).fetchone():
            skipped += 1
            continue
        con.execute("UPDATE factories SET capacity_timeline=?, is_single_site=? WHERE id=?",
                    [json.dumps(clean, ensure_ascii=False),
                     bool(r.get("is_single_physical_site", True)), rid])
        loaded += 1
        pts += len(clean)
    print(f"loaded {loaded} timelines, {pts} sourced datapoints, "
          f"{bad} points dropped (no source), {skipped} ids not found")
    con.close()


if __name__ == "__main__":
    main()
