"""Metadata-only sweep of the whole Ripple warehouse for the Laboratory map.

Pulls INFORMATION_SCHEMA.TABLES + .COLUMNS across all five databases plus the
LIBRARY_META wiring tables. No data SELECTs, no profiling. Writes CSVs under
reports/lab_map/.
"""
import csv
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts._snowflake_conn import connect

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "lab_map")
os.makedirs(OUT, exist_ok=True)

DBS = ["LIBRARY_RAW", "LIBRARY_STAGING", "LIBRARY_MARTS", "LIBRARY_META",
       "LIBRARY_TOOLS"]


def dump(cur, sql, path, header):
    t0 = time.time()
    cur.execute(sql)
    rows = cur.fetchall()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"{os.path.basename(path)}: {len(rows)} rows in {time.time()-t0:.1f}s",
          flush=True)
    return rows


def main():
    conn = connect()
    cur = conn.cursor()

    all_tables = []
    all_cols = []
    for db in DBS:
        t = dump(cur, f"""
            select '{db}' as db, table_schema, table_name, table_type,
                   row_count, bytes, created, last_altered, comment
            from {db}.information_schema.tables
            where table_schema not in ('INFORMATION_SCHEMA')
            order by table_schema, table_name
        """, os.path.join(OUT, f"tables_{db}.csv"),
            ["db", "schema", "table", "type", "row_count", "bytes", "created",
             "last_altered", "comment"])
        all_tables += t

        c = dump(cur, f"""
            select '{db}' as db, table_schema, table_name, column_name,
                   ordinal_position, data_type, character_maximum_length,
                   numeric_precision, numeric_scale, is_nullable, comment
            from {db}.information_schema.columns
            where table_schema not in ('INFORMATION_SCHEMA')
            order by table_schema, table_name, ordinal_position
        """, os.path.join(OUT, f"columns_{db}.csv"),
            ["db", "schema", "table", "column", "ordinal", "dtype", "charlen",
             "numprec", "numscale", "nullable", "comment"])
        all_cols += c

    with open(os.path.join(OUT, "ALL_TABLES.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["db", "schema", "table", "type", "row_count", "bytes",
                    "created", "last_altered", "comment"])
        w.writerows(all_tables)
    with open(os.path.join(OUT, "ALL_COLUMNS.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["db", "schema", "table", "column", "ordinal", "dtype",
                    "charlen", "numprec", "numscale", "nullable", "comment"])
        w.writerows(all_cols)
    print(f"TOTAL tables={len(all_tables)} columns={len(all_cols)}", flush=True)

    conn.close()


if __name__ == "__main__":
    main()
