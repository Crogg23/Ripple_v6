#!/usr/bin/env python3
"""Raise / restore the RIPPLE_BUDGET resource monitor for a backfill sprint.

PREVIEW by default (reads live state + prints the EXACT DDL it would run). Chris
runs --apply / --restore -- this is ACCOUNTADMIN and the auto-classifier blocks
agent monitor/grant writes, so the agent only ever PREVIEWS.

Stress-hardened (from the build-program stress-test):
  * ALTER, never CREATE OR REPLACE. CREATE OR REPLACE DROPS the monitor and its
    account/warehouse BINDING -> the sprint would run UNCAPPED. ALTER ... SET keeps it.
  * Read live USED / QUOTA / LEVEL FIRST and print them -- never assume.
  * SUSPEND triggers sit BELOW 100% so one long in-flight statement can't overshoot
    past the hard cap before SUSPEND_IMMEDIATE bites.

Chris's call (2026-06-27): sprint ceiling ~100 credits, restore to 15 after.

    python scripts/budget_sprint.py                 # PREVIEW: live state + the DDL
    python scripts/budget_sprint.py --apply          # raise quota to --quota (default 100)
    python scripts/budget_sprint.py --restore        # drop back to --restore-quota (default 15)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

MONITOR = "RIPPLE_BUDGET"


def _alter_sql(quota: int, suspend_pct: int = 90) -> str:
    """The exact ALTER statement. PURE -> unit-testable offline.

    ALTER (not CREATE OR REPLACE) preserves the account binding. Triggers: notify at
    50% and 75%, SUSPEND (let running queries finish) at ``suspend_pct``, and a hard
    SUSPEND_IMMEDIATE backstop at 100%. ``suspend_pct`` < 100 leaves overshoot
    headroom for one long statement.
    """
    quota = int(quota)
    suspend_pct = int(suspend_pct)
    if not 0 < suspend_pct < 100:
        raise ValueError("suspend_pct must be in (0, 100)")
    return (
        f"ALTER RESOURCE MONITOR {MONITOR} SET "
        f"CREDIT_QUOTA = {quota} "
        f"TRIGGERS ON 50 PERCENT DO NOTIFY "
        f"ON 75 PERCENT DO NOTIFY "
        f"ON {suspend_pct} PERCENT DO SUSPEND "
        f"ON 100 PERCENT DO SUSPEND_IMMEDIATE"
    )


def _query(conn, sql: str) -> list[dict]:
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def _print_state(conn) -> dict | None:
    rows = _query(conn, f"SHOW RESOURCE MONITORS LIKE '{MONITOR}'")
    if not rows:
        print(f"   [!] resource monitor {MONITOR} NOT FOUND — create it before a sprint.")
        return None
    m = rows[0]
    print(f"   {MONITOR}: quota={m.get('credit_quota')} used={m.get('used_credits')} "
          f"remaining={m.get('remaining_credits')} level={m.get('level')!r} "
          f"frequency={m.get('frequency')}")
    if str(m.get("level") or "").upper() != "ACCOUNT":
        print("   [!] monitor is NOT account-level — confirm the binding "
              "(ALTER ACCOUNT SET RESOURCE_MONITOR = RIPPLE_BUDGET) or the cap won't apply.")
    return m


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Raise/restore the RIPPLE_BUDGET monitor for a sprint")
    ap.add_argument("--apply", action="store_true", help="ALTER the monitor up to --quota")
    ap.add_argument("--restore", action="store_true", help="ALTER the monitor back to --restore-quota")
    ap.add_argument("--quota", type=int, default=100, help="sprint ceiling in credits (default 100)")
    ap.add_argument("--suspend", type=int, default=90, help="SUSPEND trigger %% (default 90)")
    ap.add_argument("--restore-quota", type=int, default=15, help="steady-state quota (default 15)")
    args = ap.parse_args(argv)

    if args.apply and args.restore:
        raise SystemExit("choose one of --apply / --restore, not both")

    target = args.restore_quota if args.restore else args.quota
    mode = "RESTORE" if args.restore else ("APPLY" if args.apply else "PREVIEW")
    sql = _alter_sql(target, args.suspend)
    print(f"== RIPPLE_BUDGET sprint [{mode}] ==")
    print(f"   DDL: {sql}")

    if mode == "PREVIEW":
        try:
            import snow
            conn = snow.connect()
            try:
                _print_state(conn)
            finally:
                conn.close()
        except Exception as e:  # offline / no creds -> still show the DDL
            print(f"   (no Snowflake connection — preview shows the DDL only: {str(e)[:90]})")
        print("   PREVIEW only. Re-run with --apply (raise) or --restore (drop back).")
        return 0

    import snow
    conn = snow.connect()
    try:
        print("   before:")
        _print_state(conn)
        snow.execute(conn, sql)
        print(f"   ✓ applied: CREDIT_QUOTA -> {target} credits")
        print("   after:")
        _print_state(conn)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
