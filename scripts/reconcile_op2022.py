#!/usr/bin/env python3
"""Reconcile the mislogged fed_cms_open_payments_2022 load (2026-07-01).

WHAT HAPPENED: the 2026-06-28 backfill streamed all 13,250,000 rows into
LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS_2022 (single run stamp 60f19a4a53054596,
every row PROGRAM_YEAR=2022) but threw 'I/O operation on closed file' at EOF *after*
the final write -- and the error path hardcoded row_count=0. So a COMPLETE load was
logged as error/0, the registry upsert never ran, and CATALOG shows the source as
'scouted' despite 13.25M rows physically present. (The loader has since been fixed to
download-to-disk-then-parse and to log the real count -- this can't recur.)

THIS SCRIPT (no re-download; the data is already landed):
  1. Snapshots the current INGEST_RUNS rows -> outputs/_rollback_op2022_reconcile_20260701.sql
  2. Corrects the winning run 60f19a4a53054596: error/0 -> success/13,250,000
  3. Upserts SOURCE_REGISTRY via the loader's own _register (idempotent MERGE)
  4. Verifies the ledger + registry + CATALOG lifecycle flip

    python scripts/reconcile_op2022.py            # PREVIEW (reads only, no writes)
    python scripts/reconcile_op2022.py --apply    # do the reconciliation

Run this yourself -- the agent's auto-mode classifier blocks it as a shared-state write.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "scripts"))

import snow  # noqa: E402

RUN_ID = "60f19a4a53054596"   # the run stamp on all 13.25M rows
ROWS = 13_250_000
ROLLBACK = _REPO / "outputs" / "_rollback_op2022_reconcile_20260701.sql"
NEW_MSG = ("Reconciled 2026-07-01: EOF socket-close mislogged a COMPLETE 13,250,000-row "
           "PY2022 load as error. Data verified present (single run stamp, all "
           "PROGRAM_YEAR=2022). No re-download.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Reconcile fed_cms_open_payments_2022 mislog.")
    ap.add_argument("--apply", action="store_true", help="perform the writes (else preview only)")
    args = ap.parse_args()

    conn = snow.connect()
    cur = conn.cursor()
    try:
        # verify the data really is there before touching anything
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT PROGRAM_YEAR) "
                    "FROM LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS_2022")
        n, yrs = cur.fetchone()
        print(f"landing rows: {n:,} | distinct PROGRAM_YEAR: {yrs}")
        if n != ROWS or yrs != 1:
            print(f"ABORT: expected {ROWS:,} rows in a single program year; got {n:,}/{yrs}. "
                  "Inspect before reconciling.")
            return 2

        cur.execute("""SELECT RUN_ID, STATUS, ROW_COUNT, LEFT(MESSAGE,60)
          FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
          WHERE SOURCE_ID='fed_cms_open_payments_2022' ORDER BY STARTED_AT""")
        before = cur.fetchall()
        print("INGEST_RUNS before:")
        for r in before:
            print("  ", r)

        if not args.apply:
            print("\nPREVIEW only. Re-run with --apply to:")
            print(f"  - set run {RUN_ID}: status success, row_count {ROWS:,}")
            print("  - upsert SOURCE_REGISTRY (via open_payments_2022_load._register)")
            return 0

        # 1. rollback snapshot
        ROLLBACK.parent.mkdir(parents=True, exist_ok=True)
        with open(ROLLBACK, "w", encoding="utf-8") as f:
            f.write("-- Rollback for fed_cms_open_payments_2022 reconciliation (2026-07-01)\n")
            f.write("-- INGEST_RUNS rows before the UPDATE:\n")
            for r in before:
                f.write(f"--   {r}\n")
            f.write("UPDATE LIBRARY_META.INGEST_LOGS.INGEST_RUNS SET STATUS='error', ROW_COUNT=0,\n")
            f.write("  MESSAGE='PY2022 load failed: ValueError: I/O operation on closed file.'\n")
            f.write(f"  WHERE SOURCE_ID='fed_cms_open_payments_2022' AND RUN_ID='{RUN_ID}';\n")
            f.write("-- To un-register:\n")
            f.write("-- DELETE FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE SOURCE_ID='fed_cms_open_payments_2022';\n")
        print("rollback snapshot ->", ROLLBACK)

        # 2. correct the ledger
        cur.execute("""UPDATE LIBRARY_META.INGEST_LOGS.INGEST_RUNS
          SET STATUS='success', ROW_COUNT=%s, MESSAGE=%s
          WHERE SOURCE_ID='fed_cms_open_payments_2022' AND RUN_ID=%s""",
                    (ROWS, NEW_MSG, RUN_ID))
        print("ledger UPDATE rows affected:", cur.rowcount)

        # 3. register the source (idempotent MERGE, reuses the loader's exact facets)
        import open_payments_2022_load as op
        op._register(conn, ROWS)

        # 4. verify
        cur.execute("""SELECT STATUS, ROW_COUNT FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
          WHERE SOURCE_ID='fed_cms_open_payments_2022' AND RUN_ID=%s""", (RUN_ID,))
        print("ledger after:", cur.fetchone())
        cur.execute("SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
                    "WHERE SOURCE_ID='fed_cms_open_payments_2022'")
        print("registry rows:", cur.fetchone()[0])
        cur.execute("SELECT lifecycle, trust_layer FROM LIBRARY_META.REGISTRY.CATALOG "
                    "WHERE source_id='fed_cms_open_payments_2022'")
        print("CATALOG now:", cur.fetchone())
        print("\nDONE.")
        return 0
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
