#!/usr/bin/env python3
"""Restore site coordinates from the durable, in-repo data/coordinates.csv.

The DuckDB binary is gitignored, so coordinates.csv is the source of truth for
lat/long. Base rows (data/researched/*.json) carry the 33 verified coordinates;
the rest are city-centroid approximations produced by scripts/geocode_sites.py.
This loader re-applies all of them and, for approximate rows, re-appends the
`[GEO=city:...]` provenance note to research_notes if it is not already present.

Usage: python3 scripts/load_coordinates.py   (reads data/coordinates.csv)
"""
import csv
import sys

import duckdb

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/coordinates.csv"


def main():
    con = duckdb.connect("factories.db")
    applied = noted = missing = 0
    for r in csv.DictReader(open(SRC)):
        rid = r["id"]
        row = con.execute("SELECT research_notes FROM factories WHERE id=?", [rid]).fetchone()
        if not row:
            missing += 1
            continue
        con.execute("UPDATE factories SET latitude=?, longitude=? WHERE id=?",
                    [float(r["latitude"]), float(r["longitude"]), rid])
        applied += 1
        note = r.get("geo_note") or ""
        if note.startswith("[GEO="):
            notes = row[0] or ""
            if "[GEO=city:" not in notes:
                con.execute("UPDATE factories SET research_notes=? WHERE id=?",
                            [(notes + "\n\n" if notes else "") + note, rid])
                noted += 1
    print(f"applied {applied} coordinates ({noted} approximate notes re-appended, "
          f"{missing} ids not found)")
    con.close()


if __name__ == "__main__":
    main()
