#!/usr/bin/env python3
"""Reload every portal table that stopped at a page limit.

197 tables hold exactly 2,000 rows. 126 hold exactly 10,000. That is not what
those datasets contain; it is where the fetcher stopped asking. The pager was
fixed on 2026-09-05 and proved on Oklahoma, where 32 tables went from 320,000
rows to 7,396,758. Every portal loaded before that fix is still capped.

This finds the capped tables, matches each back to its row in the portal index,
and reloads it with the fixed pager.

    python scripts/reload_capped_portals.py            # list what it would do
    python scripts/reload_capped_portals.py --run      # reload them
    python scripts/reload_capped_portals.py --run --limit 20
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from connect import db  # noqa: E402
from connect import portal_loader as P  # noqa: E402

# A load that lands on one of these did not stop because the data ran out.
PAGE_CAPS = {1000, 2000, 5000, 10000, 20000, 25000, 50000}
MAX_ROWS = 2_000_000


def capped(conn) -> dict[str, int]:
    cur = conn.cursor()
    cur.execute("""SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
                   WHERE TABLE_SCHEMA = 'LANDING' AND TABLE_TYPE = 'BASE TABLE'
                     AND TABLE_NAME LIKE 'PORTAL_%'""")
    out = {t: int(n or 0) for t, n in cur.fetchall() if int(n or 0) in PAGE_CAPS}
    cur.close()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true", help="actually reload")
    ap.add_argument("--limit", type=int, default=0, help="stop after this many")
    args = ap.parse_args()

    conn = db.connect()
    try:
        stuck = capped(conn)
        index = {P.source_id_for(r).upper(): r for r in db.dicts(
            conn, f"""SELECT platform, portal_name, dataset_id, dataset_title,
                             source_url, row_count, top_tier, join_keys
                      FROM {P.INDEX}""")}
        work = [(t, n, index[t]) for t, n in sorted(stuck.items()) if t in index]
        print(f"{len(stuck)} capped tables, {len(work)} matched to the portal index")
        print(f"they hold {sum(n for _, n, _ in work):,} rows today")
        if not args.run:
            print("\nlist only. Add --run to reload.")
            for t, n, r in work[:20]:
                print(f"  {n:>7,}  {r['PLATFORM']:<8} {str(r['DATASET_TITLE'])[:52]}")
            return 0

        if args.limit:
            work = work[:args.limit]
        grew = same = failed = 0
        gained = 0
        for i, (t, before, rec) in enumerate(work, 1):
            try:
                res = P.load_one(conn, rec, max_rows=MAX_ROWS, force=True)
            except Exception as exc:
                print(f"[{i}/{len(work)}] {t[:46]}: {str(exc).splitlines()[-1][:60]}",
                      flush=True)
                failed += 1
                continue
            after = int(res.get("rows") or 0)
            if after > before:
                grew += 1
                gained += after - before
                print(f"[{i}/{len(work)}] {t[:44]}  {before:,} -> {after:,}", flush=True)
            elif res.get("status") != "loaded":
                failed += 1
                print(f"[{i}/{len(work)}] {t[:44]}  {res.get('status')}", flush=True)
            else:
                same += 1
        print(f"\ngrew {grew}, unchanged {same}, failed {failed}")
        print(f"rows gained: {gained:,}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
