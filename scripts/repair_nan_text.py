"""Repair landing tables that hold the literal text 'nan' where a NULL belongs.

WHY (2026-08-11): the bulk loaders stringified values with
`None if v is None else str(v)`. pandas turns a JSON null into float NaN rather
than None, so that test missed it and str(NaN) wrote the three characters 'nan'
into the warehouse. The loaders are fixed (see _as_text in each of them), but
tables loaded BEFORE the fix still carry the sentinel.

This matters most for identifier columns: 'nan' reads as populated and, worse,
joins to 'nan'. FDIC's LEI came back 6,260 "populated" of which 4,008 were the
sentinel.

Only ever turns the exact lowercase string 'nan' into NULL, and only in text
columns. A genuine source value of "nan" would be destroyed by this, so the
--dry-run output shows counts per column before anything is written.

    python scripts/repair_nan_text.py --dry-run
    python scripts/repair_nan_text.py --table FED_FDIC_SOD_BRANCH_DEPOSITS
"""
from __future__ import annotations

import argparse
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_REPO, "library-onboarding", ".env"), override=True)
except Exception:
    pass

import snow  # noqa: E402

# Tables known to have been loaded by an affected loader before the fix.
SUSPECT = [
    "FED_FDIC_SOD_BRANCH_DEPOSITS",
    "FED_FEMA_IA_HOUSING_REGISTRATIONS",
]


def text_columns(cur, table):
    cur.execute(
        "SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS"
        " WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s AND DATA_TYPE='TEXT'"
        " AND LEFT(COLUMN_NAME,1)<>'_' ORDER BY ORDINAL_POSITION", (table,))
    return [r[0] for r in cur.fetchall()]


def survey(cur, table, cols):
    """Per-column count of the sentinel, in ONE pass over the table."""
    expr = ", ".join(f"""SUM(IFF("{c}"='nan',1,0))""" for c in cols)
    cur.execute(f"SELECT COUNT(*), {expr} FROM LIBRARY_RAW.LANDING.{table}")
    row = cur.fetchone()
    return row[0], {c: (row[i + 1] or 0) for i, c in enumerate(cols)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--table", action="append", help="repeatable; defaults to the suspect list")
    args = ap.parse_args()
    tables = args.table or SUSPECT

    cur = snow.connect().cursor()
    for table in tables:
        cols = text_columns(cur, table)
        if not cols:
            print(f"{table}: no text columns (or table missing) -- skipped")
            continue
        n, per_col = survey(cur, table, cols)
        hits = {c: v for c, v in per_col.items() if v}
        total = sum(hits.values())
        print(f"\n{table}: {n:,} rows, {len(cols)} text columns, "
              f"{total:,} sentinel cell(s) in {len(hits)} column(s)")
        for c, v in sorted(hits.items(), key=lambda kv: -kv[1])[:15]:
            print(f"    {c:40s} {v:>12,}")
        if not hits or args.dry_run:
            continue
        # One UPDATE for the whole table -- Snowflake rewrites the micro-partitions
        # once, rather than once per column.
        sets = ", ".join(f'''"{c}" = NULLIF("{c}", 'nan')''' for c in hits)
        where = " OR ".join(f"""\"{c}\"='nan'""" for c in hits)
        cur.execute(f"UPDATE LIBRARY_RAW.LANDING.{table} SET {sets} WHERE {where}")
        print(f"    -> repaired ({cur.rowcount:,} rows touched)")


if __name__ == "__main__":
    main()
