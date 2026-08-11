"""Remove exact-duplicate rows from landing tables poisoned by runaway pagers.

WHY (2026-08-11 verification): two Lane-A sources were loaded by a generated
pager that re-fetched the same content in a loop -- the mortgage database
landed 19,054,246 rows of which 11,648 are real (x1,636 inflation), and
foreign-aid spending landed 3,967,456 rows of which 95,658 are real (97.6%
duplicates). The generating code was exec()'d and never persisted, so the
loader cannot be fixed; the honest repair is to keep exactly one copy of every
distinct DATA row (metadata columns excluded from the identity, earliest
ingest timestamp kept) and swap it in atomically.

Safety rails, in the spirit of repair_nan_text.py and the demote tool:
  * DRY RUN by default -- prints total vs distinct and the would-be action.
  * REFUSES to touch a table whose exact-duplicate rate is below --min-dup-rate
    (default 50%): this tool is for pathological inflation, not for shaving
    a few legitimate-looking repeats off a healthy table.
  * The swap is atomic (CREATE new + SWAP WITH); the inflated rows survive in
    the swapped-out side table until it is dropped, so nothing is destroyed
    outright. The drop of that side table is left to a human.

    python scripts/dedupe_landing_exact.py --dry-run
    python scripts/dedupe_landing_exact.py --table FED_FHFA_NMDB --run
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

# Metadata columns are excluded from row identity: duplicates written minutes
# apart differ in _INGESTED_AT but are the same fact.
META_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"}

# Tables the 2026-08-11 verification proved pathologically inflated.
SUSPECT = [
    "FED_FHFA_NMDB",
    "FED_FOREIGNASSISTANCE",
]


def data_columns(cur, table):
    cur.execute(
        "SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS"
        " WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION",
        (table,))
    cols = [r[0] for r in cur.fetchall()]
    return [c for c in cols if c not in META_COLS]


def survey(cur, table, cols):
    ident = ", ".join(f'"{c}"' for c in cols)
    cur.execute(
        f"SELECT COUNT(*), COUNT(DISTINCT HASH({ident}))"
        f" FROM LIBRARY_RAW.LANDING.{table}")
    return cur.fetchone()


def dedupe_sql(table, cols):
    """The three statements that perform the repair, returned for review."""
    ident = ", ".join(f'"{c}"' for c in cols)
    side = f"{table}__PREDEDUP"
    return [
        f"CREATE TABLE LIBRARY_RAW.LANDING.{table}__DEDUP AS"
        f" SELECT * FROM LIBRARY_RAW.LANDING.{table}"
        f" QUALIFY ROW_NUMBER() OVER (PARTITION BY {ident} ORDER BY _INGESTED_AT) = 1",
        f"ALTER TABLE LIBRARY_RAW.LANDING.{table} SWAP WITH LIBRARY_RAW.LANDING.{table}__DEDUP",
        f"ALTER TABLE LIBRARY_RAW.LANDING.{table}__DEDUP RENAME TO LIBRARY_RAW.LANDING.{side}",
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--table", action="append", help="repeatable; defaults to the suspect list")
    ap.add_argument("--min-dup-rate", type=float, default=0.5,
                    help="refuse tables whose exact-dup rate is below this fraction")
    args = ap.parse_args()
    if not args.run:
        args.dry_run = True
    tables = args.table or SUSPECT

    import snow
    cur = snow.connect().cursor()
    failures = 0
    for table in tables:
        cols = data_columns(cur, table)
        if not cols:
            print(f"{table}: no columns found (table missing?) -- skipped")
            continue
        total, distinct = survey(cur, table, cols)
        rate = 0.0 if not total else 1.0 - distinct / total
        print(f"{table}: {total:,} rows, {distinct:,} distinct data rows "
              f"({rate:.1%} exact duplicates)")
        if rate < args.min_dup_rate:
            print(f"{table}: dup rate below --min-dup-rate={args.min_dup_rate:.0%}"
                  " -- REFUSING (this tool is for pathological inflation only)")
            failures += 1
            continue
        stmts = dedupe_sql(table, cols)
        if args.dry_run:
            print(f"{table}: DRY RUN -- would execute:")
            for s in stmts:
                print(f"    {s};")
            continue
        for s in stmts:
            cur.execute(s)
        total2, distinct2 = survey(cur, table, cols)
        ok = total2 == distinct2 == distinct
        print(f"{table}: now {total2:,} rows, {distinct2:,} distinct -- "
              f"{'VERIFIED' if ok else 'MISMATCH (investigate before dropping the side table)'}")
        print(f"{table}: inflated rows preserved in LANDING.{table}__PREDEDUP"
              " (human-only drop when satisfied)")
        if not ok:
            failures += 1
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
