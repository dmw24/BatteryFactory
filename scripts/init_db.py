#!/usr/bin/env python3
"""Initialise the gigafactory database.

Creates `factories.db` (DuckDB) with the `factories` table and a companion
`sources` provenance table. Idempotent: safe to re-run — it will not drop
existing data unless --reset is passed.
"""
import argparse
import duckdb

DB_PATH = "factories.db"

# Column order is authoritative and mirrored by the schema in CLAUDE.md.
FACTORIES_DDL = """
CREATE TABLE IF NOT EXISTS factories (
    id                      VARCHAR PRIMARY KEY,   -- stable slug: <operator>-<plant>-<country>
    plant_name              VARCHAR NOT NULL,
    operator                VARCHAR,               -- entity running the site
    parent_company          VARCHAR,               -- ultimate owner / group
    country                 VARCHAR,
    region                  VARCHAR,               -- China|USA|Europe|South Korea|Japan|India|Southeast Asia|Rest of World
    latitude                DOUBLE,
    longitude               DOUBLE,
    status                  VARCHAR,               -- announced|under_construction|operational
    announced_year          INTEGER,
    start_year              INTEGER,               -- first production year
    nameplate_capacity_gwh  DOUBLE,                -- annual GWh/year at full nameplate
    capacity_by_year_json   VARCHAR,              -- JSON {"2024":10,"2025":20} phased ramp GWh/yr
    chemistry               VARCHAR,               -- e.g. LFP, NMC, NCA, sodium-ion, solid-state
    cell_format             VARCHAR,               -- prismatic|cylindrical|pouch|mixed
    end_market              VARCHAR,               -- EV|ESS|consumer|mixed
    jv_partners             VARCHAR,               -- comma-separated partner list if JV
    source_url              VARCHAR,
    source_date             VARCHAR,               -- ISO date the source was published/accessed
    confidence              DOUBLE,                -- 0-1; lower when values unconfirmed
    -- housekeeping
    capacity_ref_year       INTEGER,               -- year nameplate_capacity_gwh refers to
    is_cell_manufacturer    BOOLEAN,               -- false = pack/material/recycling only (kept, flagged)
    research_notes          VARCHAR,               -- researcher provenance / caveats
    capacity_timeline       VARCHAR,               -- JSON array of dated, sourced capacity observations (real data)
    inserted_at             TIMESTAMP DEFAULT now(),
    CHECK (status IN ('announced','under_construction','operational') OR status IS NULL),
    CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1))
);
"""

# Optional multi-source provenance (a plant may cite more than one source).
SOURCES_DDL = """
CREATE TABLE IF NOT EXISTS sources (
    factory_id   VARCHAR,
    source_url   VARCHAR,
    source_date  VARCHAR,
    note         VARCHAR
);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB_PATH)
    ap.add_argument("--reset", action="store_true", help="drop existing tables first")
    args = ap.parse_args()

    con = duckdb.connect(args.db)
    if args.reset:
        con.execute("DROP TABLE IF EXISTS factories;")
        con.execute("DROP TABLE IF EXISTS sources;")
        print("Dropped existing tables.")
    con.execute(FACTORIES_DDL)
    con.execute(SOURCES_DDL)
    cols = con.execute("PRAGMA table_info('factories')").fetchall()
    print(f"factories.db ready at {args.db}")
    print(f"factories table: {len(cols)} columns")
    for c in cols:
        print(f"  - {c[1]:24} {c[2]}")
    con.close()


if __name__ == "__main__":
    main()
