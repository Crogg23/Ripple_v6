"""
price_it — what did this cost last time?

Reads the warehouse's own query log so a price tag is real history, not a guess.
Per-query warehouse credits are not stored by Snowflake; they are derived here from
actual past runtime x warehouse size, which is how Snowflake bills. That derivation
is labeled in the output.

The log holds SQL text, not shell commands — match on a table or statement the job runs:
  python scripts/price_it.py --like "%ENTITY_INDEX%"          # a table the spine writes
  python scripts/price_it.py --like "%create or replace table%MARTS.%"
  python scripts/price_it.py --tag  spine_rebuild             # QUERY_TAG, if the job sets one (none do yet)
  python scripts/price_it.py --days 60 --like "%HMDA%"        # look-back window

Prints: runs found (capped at 500 — a cap means "many small statements", not one job),
p50 / max runtime, p50 / max credits, dollars at RIPPLE_CREDIT_USD. If the env var is unset the
$/credit is a DEFAULT and is labeled as such. Zero runs -> says so.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connect import db  # noqa: E402  (plumbing, not the spine)

CREDITS_PER_HOUR = {  # Snowflake standard warehouse sizes
    "X-Small": 1, "Small": 2, "Medium": 4, "Large": 8, "X-Large": 16,
    "2X-Large": 32, "3X-Large": 64, "4X-Large": 128,
}


def _mark_priced() -> None:
    """Greenlights require a price shown in the last hour (.claude/hooks/chris-words.sh)."""
    import time
    state = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".claude", "state")
    os.makedirs(state, exist_ok=True)
    with open(os.path.join(state, "last_priced"), "w") as fh:
        fh.write(str(int(time.time())))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--like", help="SQL LIKE pattern against query text")
    g.add_argument("--tag", help="exact QUERY_TAG")
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()

    usd_env = os.environ.get("RIPPLE_CREDIT_USD")
    usd = float(usd_env) if usd_env else 2.00
    usd_label = f"${usd:.2f}/credit (RIPPLE_CREDIT_USD)" if usd_env else f"${usd:.2f}/credit (DEFAULT, not your contract rate — set RIPPLE_CREDIT_USD)"
    where = "query_text ILIKE %s" if args.like else "query_tag = %s"
    param = args.like or args.tag

    sql = f"""
      select warehouse_size,
             total_elapsed_time/1000.0 as secs,
             bytes_scanned,
             start_time,
             execution_status
      from snowflake.account_usage.query_history
      where {where}
        and start_time >= dateadd(day, -%s, current_timestamp())
        and warehouse_size is not null
        and query_text not ilike '%%price_it%%'
      order by start_time desc
      limit 500
    """
    conn = db.connect()
    rows = db.dicts(conn, sql, (param, args.days))
    _mark_priced()  # showing "no real number" is still showing the price honestly
    if not rows:
        print(f"no real number for this — zero runs matching {param!r} in the last {args.days} days")
        return 1

    for r in rows:
        r["SECS"] = float(r["SECS"] or 0)

    def credits(r):
        return r["SECS"] / 3600.0 * CREDITS_PER_HOUR.get(r["WAREHOUSE_SIZE"], 1)

    secs = sorted(r["SECS"] for r in rows)
    creds = sorted(credits(r) for r in rows)
    p50 = lambda xs: xs[len(xs) // 2]  # noqa: E731
    ok = sum(1 for r in rows if r["EXECUTION_STATUS"] == "SUCCESS")

    cap = "  (CAPPED at 500 — many small statements, not one job; tighten the pattern)" if len(rows) == 500 else ""
    print(f"runs found:      {len(rows)}  ({ok} succeeded)  last {args.days} days  match {param!r}{cap}")
    print(f"warehouse sizes: {sorted({r['WAREHOUSE_SIZE'] for r in rows})}")
    print(f"runtime:         p50 {p50(secs)/60:.1f} min   max {secs[-1]/60:.1f} min")
    print(f"credits:         p50 {p50(creds):.3f}   max {creds[-1]:.3f}   (runtime x size — how Snowflake bills)")
    print(f"dollars:         p50 ${p50(creds)*usd:.2f}   max ${creds[-1]*usd:.2f}   at {usd_label}")
    print(f"most recent:     {rows[0]['START_TIME']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
