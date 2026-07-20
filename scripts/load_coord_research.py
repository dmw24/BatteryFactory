#!/usr/bin/env python3
"""Apply researched site coordinates (from a coord-research workflow journal) and
rebuild the durable data/coordinates.csv from the DB.

For each result with found=true and non-null lat/long, sets factories lat/long and
appends a `[GEO=site:...]` / `[GEO=town:...]` provenance note (with source) to
research_notes — unless the row already carries a `[GEO=` marker (idempotent).
found=false rows (speculative / cancelled / no located site) are left null.

Then rewrites data/coordinates.csv from the DB so it captures verified + city-centroid
+ research-found coordinates in one durable, in-repo store.

Usage: python3 scripts/load_coord_research.py <workflow-journal.jsonl>
"""
import csv
import json
import re
import sys

import duckdb

OUT = "data/coordinates.csv"


def results(journal):
    for line in open(journal):
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if o.get("type") == "result" and isinstance(o.get("result"), dict):
            yield o["result"]


def geo_note_of(notes):
    """Extract the [GEO=...] marker line from research_notes, if any."""
    if not notes:
        return None
    m = re.search(r"\[GEO=[^\n]*", notes)
    return m.group(0).strip() if m else None


def main():
    journal = sys.argv[1]
    con = duckdb.connect("factories.db")
    applied = skipped = unfound = 0
    for r in results(journal):
        rid = r.get("id")
        if not rid:
            continue
        if not (r.get("found") and r.get("latitude") is not None and r.get("longitude") is not None):
            unfound += 1
            continue
        row = con.execute("SELECT research_notes FROM factories WHERE id=?", [rid]).fetchone()
        if not row:
            continue
        lat, lon = float(r["latitude"]), float(r["longitude"])
        con.execute("UPDATE factories SET latitude=?, longitude=? WHERE id=?",
                    [round(lat, 5), round(lon, 5), rid])
        notes = row[0] or ""
        if "[GEO=" not in notes:
            prec = r.get("precision", "site")
            src = r.get("source_url") or "research"
            date = r.get("source_date") or ""
            extra = (" " + r["note"]) if r.get("note") else ""
            note = (f"[GEO={prec}:research] Coordinates via web research ({date}); {src}."
                    f" precision={prec}.{extra}")
            con.execute("UPDATE factories SET research_notes=? WHERE id=?",
                        [(notes + "\n\n" if notes else "") + note, rid])
        applied += 1

    # rebuild the durable store from the DB
    rows = con.execute("""SELECT id, latitude, longitude, research_notes FROM factories
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL ORDER BY id""").fetchall()
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "latitude", "longitude", "geo_note"])
        for rid, la, lo, notes in rows:
            w.writerow([rid, la, lo, geo_note_of(notes) or "verified (from researcher / prior source)"])

    have = len(rows)
    print(f"applied {applied} researched coords ({unfound} not found/left null). "
          f"Coverage now {have}/378. Wrote {OUT} ({have} rows).")
    con.close()


if __name__ == "__main__":
    main()
