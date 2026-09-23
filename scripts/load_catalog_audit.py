"""Load the catalog audit's findings into LIBRARY_META.AUDIT.CATALOG_AUDIT.

One row per finding from audit/catalog_audit_<date>.tsv (scripts/audit_catalog.py
analyze): table, column, check, result, severity, proposed fix, plus the audit date.
Appends; a re-run for the same date first refuses if that date is already loaded,
so the table is a history of audits, never a silent double.

    python scripts/load_catalog_audit.py 2026-09-23
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

FQN = ("LIBRARY_META", "AUDIT", "CATALOG_AUDIT")


def main() -> int:
    day = sys.argv[1]
    df = pd.read_csv(REPO / "audit" / f"catalog_audit_{day}.tsv", sep="\t", dtype=str).fillna("")
    df.columns = [c.upper() for c in df.columns]
    df = df.rename(columns={"TABLE": "TABLE_NAME", "COLUMN": "COLUMN_NAME", "CHECK": "CHECK_NAME"})
    df["AUDIT_DATE"] = pd.to_datetime(day).date()
    df["SOURCE"] = "scripts/audit_catalog.py analyze"
    conn = db.connect()
    exists = db.rows(conn, """select count(*) from LIBRARY_META.information_schema.tables
        where table_schema='AUDIT' and table_name='CATALOG_AUDIT'""")[0][0]
    if exists and db.rows(conn, f"select count(*) from LIBRARY_META.AUDIT.CATALOG_AUDIT where audit_date='{day}'")[0][0]:
        print(f"STOP: {day} already loaded")
        return 1
    ok, _, n, _ = write_pandas(conn, df, FQN[2], database=FQN[0], schema=FQN[1],
                               auto_create_table=True, overwrite=False, use_logical_type=True)
    if not exists:
        db.rows(conn, "comment on table LIBRARY_META.AUDIT.CATALOG_AUDIT is "
                      "'Catalog audit findings, one row per finding: is the map of LIBRARY_MARTS telling the truth. "
                      "Written by scripts/load_catalog_audit.py from scripts/audit_catalog.py. Appends one audit date per run.'")
    print(f"loaded {n:,} rows, ok={ok}")
    print(db.rows(conn, f"select check_name, count(*) from LIBRARY_META.AUDIT.CATALOG_AUDIT where audit_date='{day}' group by 1 order by 2 desc"))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
