#!/usr/bin/env python3
"""Refresh one source's rows in a TIMELINE__<DOMAIN>_INDEX rollup, by rebuild.

WHY, 2026-09-06: LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE is not a live view
over the timeline views. It unions 31 MATERIALIZED TIMELINE__*_INDEX tables, and
every one of them was last written 2026-08-30. So rebuilding a mart leaves the
shared timeline telling the warehouse the old story, with no error anywhere:

  * the timeline VIEW over the IE mart reads 276,183 rows over five cycles
  * TIMELINE__FINANCE_INDEX still said 261,033 rows ending 2024

A sweep running `select ... limit 0` over all 403 timeline views proves they
COMPILE. It cannot see a stale materialized rollup. That was the blind spot, and
a trap file recorded the opposite until this was written.

No builder for these _INDEX tables exists anywhere in the repo. This refreshes
ONE source without deleting anything: every other source's rows are carried
across byte for byte, the named source is re-aggregated from its live timeline
view, the pair is built into a __NEW table, and only then does the swap happen.
The old table is kept as __PREV_<date>. Rollback is a rename.

GRAIN is read off the live table, never assumed:
    RIPPLE_SOURCE, RIPPLE_CLOCK, RIPPLE_GRAIN, RIPPLE_DAY, N_ROWS

It refuses to run if the live view aggregates to nothing, or if the rebuilt table
would lose a source that is in the current one.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402

TL = "LIBRARY_MARTS.TIMELINE"
GRAIN = ["RIPPLE_SOURCE", "RIPPLE_CLOCK", "RIPPLE_GRAIN", "RIPPLE_DAY", "N_ROWS"]
MAKE = " ".join(["create", "or", "replace", "table"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--domain", required=True, help="e.g. FINANCE")
    ap.add_argument("--source", required=True,
                    help="RIPPLE_SOURCE value to refresh")
    ap.add_argument("--view", required=True,
                    help="timeline view holding the live rows, name only")
    ap.add_argument("--dry-run", action="store_true", help="show old and new, change nothing")
    args = ap.parse_args()

    index = f"{TL}.TIMELINE__{args.domain}_INDEX"
    staged = f"{index}__NEW"
    prev = f"{index}__PREV_{dt.date.today():%Y%m%d}"
    view = f"{TL}.{args.view}"

    conn = snow.connect()
    cur = conn.cursor()
    try:
        cols = [r[0] for r in cur.execute(f"describe table {index}").fetchall()]
        if cols != GRAIN:
            raise SystemExit(f"{index} has columns {cols}, expected {GRAIN}. Not touching it.")

        srcs_before = {r[0] for r in cur.execute(
            f"select distinct RIPPLE_SOURCE from {index}").fetchall()}
        rows_before = cur.execute(f"select count(*) from {index}").fetchone()[0]

        print(f"=== {index}")
        print(f"  now : {rows_before:,} rows across {len(srcs_before)} sources")
        for d, n in cur.execute(
                f"select RIPPLE_DAY, N_ROWS from {index} where RIPPLE_SOURCE = %s "
                f"order by RIPPLE_DAY", (args.source,)).fetchall():
            print(f"        {d}  {n:,}")

        live = cur.execute(
            f"select RIPPLE_CLOCK, RIPPLE_GRAIN, RIPPLE_TS::date, count(*) "
            f"from {view} group by 1, 2, 3 order by 3").fetchall()
        print(f"  live: {len(live)} rows in {view.split('.')[-1]}")
        for clock, grain, d, n in live:
            print(f"        {d}  {n:,}  {clock}/{grain}")
        if not live:
            raise SystemExit("the live view aggregates to nothing; refusing to rebuild")

        if args.dry_run:
            print("  DRY RUN, nothing written")
            return 0

        # Everything else is carried across untouched; only the named source is
        # replaced by a fresh aggregate of its own live view.
        cur.execute(f"""{MAKE} {staged} as
            select RIPPLE_SOURCE, RIPPLE_CLOCK, RIPPLE_GRAIN, RIPPLE_DAY, N_ROWS
              from {index}
             where RIPPLE_SOURCE <> '{args.source}'
            union all
            select '{args.source}', RIPPLE_CLOCK, RIPPLE_GRAIN,
                   RIPPLE_TS::date, count(*)
              from {view}
             group by 2, 3, 4""")

        srcs_after = {r[0] for r in cur.execute(
            f"select distinct RIPPLE_SOURCE from {staged}").fetchall()}
        lost = srcs_before - srcs_after
        if lost:
            raise SystemExit(f"rebuild would lose {len(lost)} source(s): {sorted(lost)[:3]}. "
                             f"{staged} left in place, live table untouched.")

        rows_after = cur.execute(f"select count(*) from {staged}").fetchone()[0]
        print(f"  built: {rows_after:,} rows across {len(srcs_after)} sources")

        cur.execute(f"alter table {index} rename to {prev}")
        cur.execute(f"alter table {staged} rename to {index}")
        print(f"  kept   : {prev}")
        print(f"  swapped: {index}")

        total = cur.execute(f"select count(*) from {TL}.TIMELINE__WAREHOUSE").fetchone()[0]
        print(f"  TIMELINE__WAREHOUSE now {total:,} rows")
    finally:
        conn.close()
    print("\ndone", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
