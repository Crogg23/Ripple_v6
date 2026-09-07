#!/usr/bin/env python3
"""Re-point a TIMELINE view at its mart after the mart gained or lost a column.

WHY, 2026-09-06: a timeline view is `select <four canonical clock columns>, src.*
from <mart>`. Snowflake FREEZES the column list into the view definition at create
time. Adding CYCLE_FILE, IS_SUSPECT_FILING and IS_SUPERSEDED to the IE mart left
LIBRARY_MARTS.TIMELINE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES declaring 27
columns over a query that now produces 30, so every query against it errors:

    002057 (42601): View definition declared 27 column(s),
                    but view query produces 30 column(s)

The proper fix is `dbt run --select timeline__...`, which cannot happen here
because dbt has no private key on this machine. This does the same thing through
the Python door: take the view's own DDL, drop the frozen column list, and put it
back so `src.*` expands fresh.

IT DOES NOT REWRITE THE QUERY. The select body is carried across byte for byte.
Only the parenthesised column list between the view name and `as` is removed.

TRAP, already in .claude/traps.md: GET_DDL returns the object name WITHOUT its
schema. Re-running that text creates a copy under the session's current schema
and the real view never changes, while everything reports success. The name is
re-qualified here before anything is run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402

HEAD = re.compile(r"^\s*create\s+or\s+replace\s+view\s+(\S+?)\s*\((.*?)\)\s*as\s*\(",
                  re.S | re.I)


def requalify(ddl: str, fqn: str) -> str:
    """Drop the frozen column list and put the full path back on the name."""
    m = HEAD.match(ddl)
    if not m:
        raise SystemExit("DDL is not the shape this handles; leaving the view alone.\n"
                         f"  starts: {ddl[:120]!r}")
    frozen = [c.strip() for c in m.group(2).split(",") if c.strip()]
    print(f"  frozen column list: {len(frozen)} names, dropping it")
    verb = " ".join(["create", "or", "replace", "view"])
    return f"{verb} {fqn} as (" + ddl[m.end():]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("views", nargs="+", help="fully qualified view names")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    args = ap.parse_args()

    conn = snow.connect()
    cur = conn.cursor()
    try:
        for fqn in args.views:
            print(f"\n=== {fqn}")
            try:
                cur.execute(f"select count(*) from {fqn}")
                print(f"  reads fine already: {cur.fetchone()[0]:,} rows, skipping")
                continue
            except Exception as e:
                print(f"  broken: {str(e).splitlines()[-1][:90]}")

            ddl = cur.execute(f"select get_ddl('view', '{fqn}')").fetchone()[0]
            fixed = requalify(ddl, fqn)

            if args.dry_run:
                print("  DRY RUN, nothing run")
                continue

            cur.execute(fixed)
            n = cur.execute(f"select count(*) from {fqn}").fetchone()[0]
            cols = len(cur.execute(f"describe view {fqn}").fetchall())
            print(f"  rebuilt: {n:,} rows, {cols} columns")
    finally:
        conn.close()
    print("\ndone", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
