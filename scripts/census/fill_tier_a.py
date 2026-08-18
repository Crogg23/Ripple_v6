"""Tier A of the census-grid fill: catalog-level metadata, near-zero compute.

Pulls, from the warehouse's own information_schema (no table scans):
  - every table in the marts and raw databases: row count, bytes, column count
  - full column lists (name, type) for the mart layer -- this also recovers the
    12 models whose columns could not be reconstructed from SQL at grid-build time

Writes reports/census_grid_2026-08-12/fill/tier_a_tables.csv and
tier_a_columns.csv. Read-only; aggregate catalog views only.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from _snowflake_conn import connect  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(REPO, "reports", "census_grid_2026-08-12", "fill")
os.makedirs(OUT_DIR, exist_ok=True)

DATABASES = ["LIBRARY_MARTS", "LIBRARY_RAW", "LIBRARY_STAGING"]


def main():
    conn = connect()
    cur = conn.cursor()
    cur.execute("show databases")
    have = {r[1].upper() for r in cur.fetchall()}
    dbs = [d for d in DATABASES if d in have]
    print("databases present:", dbs, flush=True)

    with open(os.path.join(OUT_DIR, "tier_a_tables.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["database", "schema", "table", "table_type", "row_count", "bytes", "created", "last_altered"])
        for db in dbs:
            cur.execute(
                f"select table_catalog, table_schema, table_name, table_type, row_count, bytes, "
                f"to_varchar(created), to_varchar(last_altered) "
                f"from {db}.INFORMATION_SCHEMA.TABLES where table_schema <> 'INFORMATION_SCHEMA' "
                f"order by table_schema, table_name"
            )
            rows = cur.fetchall()
            w.writerows(rows)
            print(f"{db}: {len(rows)} tables", flush=True)

    with open(os.path.join(OUT_DIR, "tier_a_columns.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["database", "schema", "table", "column", "ordinal", "data_type"])
        for db in dbs:
            cur.execute(
                f"select table_catalog, table_schema, table_name, column_name, ordinal_position, data_type "
                f"from {db}.INFORMATION_SCHEMA.COLUMNS where table_schema <> 'INFORMATION_SCHEMA' "
                f"order by table_schema, table_name, ordinal_position"
            )
            rows = cur.fetchall()
            w.writerows(rows)
            print(f"{db}: {len(rows)} columns", flush=True)
    conn.close()
    print("TIER A DONE", flush=True)


if __name__ == "__main__":
    main()
