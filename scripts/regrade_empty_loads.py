#!/usr/bin/env python3
"""Re-grade historical INGEST_RUNS using the load-time DENSITY gate (P0-1).

THE PROBLEM THIS UNDOES
-----------------------
Before the density gate, a load that landed rows but carried NO real data still
logged STATUS='success' -- so FED_FJC_IDB (4.1M rows, 100% EMPTY across every
column, a parse failure) rode into the catalog as a 'modeled' source. The gate now
stamps such loads STATUS='empty' at load time. This one-shot applies the SAME gate,
retroactively, to runs that already logged 'success', so the historical record stops
lying too.

WHAT IT DOES
------------
For every INGEST_RUNS row with STATUS='success' (latest per source by default):
  1. Re-sample its landing table LIBRARY_RAW.LANDING.<UPPER(source_id)> (cheap LIMIT).
  2. Run ingest.assess_density() -- the EXACT function the live loader uses.
  3. If the gate says 'empty', that run would re-grade success -> empty.

SAFE BY DEFAULT -- preview only. No warehouse writes unless --apply is passed.

  python3 scripts/regrade_empty_loads.py                 # preview (READS only)
  python3 scripts/regrade_empty_loads.py --all-runs       # consider every success run, not just latest
  python3 scripts/regrade_empty_loads.py --sample 5000    # rows sampled per table (default 2000)
  python3 scripts/regrade_empty_loads.py --apply          # re-grade (ACCOUNTADMIN; row UPDATEs only)

GUARDRAILS
----------
* --apply only mutates EXISTING INGEST_RUNS ROWS (sets STATUS='empty' and annotates
  MESSAGE with the measured density). It does NOT alter the INGEST_RUNS schema, does
  NOT touch LANDING/REGISTRY/CATALOG, and NEVER re-grades a run the gate calls healthy.
* The catalog's LIFECYCLE is DERIVED downstream from STATUS, so fixing STATUS here is
  enough -- no catalog write needed.
* This is a one-shot reconciliation. New loads are gated at load time by ingest.py.
"""
from __future__ import annotations

import argparse
import sys
import warnings

warnings.filterwarnings("ignore")

REPO = "c:/Code/Ripple_v6"
sys.path.insert(0, f"{REPO}/library-onboarding")

import pandas as pd  # noqa: E402

import snow  # noqa: E402  (shared connection + helpers)
from config import settings  # noqa: E402
from ingest import assess_density  # noqa: E402  (the SAME gate the loader uses)


def _landing_fqn(source_id: str) -> str:
    table = source_id.upper()
    return f'"{settings.raw_database}"."{settings.raw_schema}"."{table}"'


def _sample_frame(conn, source_id: str, sample_rows: int):
    """Pull a cheap leading-row sample of a landing table as a DataFrame.

    Returns None if the table doesn't exist / can't be read. The gate excludes the
    _INGESTED_AT/_SOURCE_RUN_ID/_SRC_SHA256 meta columns itself, so we select * and
    let assess_density ignore them -- identical to the load-time path.
    """
    fqn = _landing_fqn(source_id)
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {fqn} LIMIT {int(sample_rows)}")
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return pd.DataFrame(rows, columns=cols)
    except Exception:
        return None
    finally:
        cur.close()


def _candidate_runs(conn, all_runs: bool):
    """Return (run_id, source_id, row_count, started_at) for success runs to check.

    Default: the LATEST success run per source (the one that decides current state).
    --all-runs: every success run.
    """
    fqn = (f'"{settings.meta_database}"."{settings.ingest_log_schema}".'
           f'"{settings.ingest_log_table}"')
    cur = conn.cursor()
    try:
        if all_runs:
            cur.execute(
                f"SELECT RUN_ID, SOURCE_ID, ROW_COUNT, STARTED_AT FROM {fqn} "
                "WHERE STATUS='success' ORDER BY SOURCE_ID, STARTED_AT DESC")
        else:
            cur.execute(
                f"SELECT RUN_ID, SOURCE_ID, ROW_COUNT, STARTED_AT FROM {fqn} r "
                "WHERE STATUS='success' AND STARTED_AT = ("
                f"  SELECT MAX(STARTED_AT) FROM {fqn} s "
                "  WHERE s.SOURCE_ID = r.SOURCE_ID AND s.STATUS='success') "
                "ORDER BY ROW_COUNT DESC NULLS LAST")
        return cur.fetchall()
    finally:
        cur.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-grade empty INGEST_RUNS via the density gate.")
    ap.add_argument("--apply", action="store_true",
                    help="WRITE: set STATUS='empty' on runs the gate demotes (ACCOUNTADMIN).")
    ap.add_argument("--all-runs", action="store_true",
                    help="Check every success run, not just the latest per source.")
    ap.add_argument("--sample", type=int, default=2000,
                    help="Rows sampled per landing table (default 2000).")
    args = ap.parse_args()

    mode = "APPLY" if args.apply else "PREVIEW (reads only, no writes)"
    print("=" * 72)
    print(f"REGRADE EMPTY LOADS via density gate  --  {mode}")
    print(f"  floor = {__import__('ingest').DENSITY_MIN_POPULATED_FRACTION:.0%} populated cells"
          f"  |  sample = {args.sample} rows/table"
          f"  |  scope = {'all success runs' if args.all_runs else 'latest success per source'}")
    print("=" * 72)

    conn = snow.connect()
    try:
        runs = _candidate_runs(conn, args.all_runs)
        print(f"\nchecking {len(runs)} success run(s)...\n")

        demote = []   # (run_id, source_id, row_count, density_dict)
        skipped = 0   # tables we couldn't read (missing / permission) -> left alone
        for run_id, source_id, row_count, started in runs:
            df = _sample_frame(conn, source_id, args.sample)
            if df is None or len(df) == 0:
                skipped += 1
                continue
            d = assess_density(df)
            if d["empty"]:
                demote.append((run_id, source_id, row_count, d))

        if not demote:
            print("No success runs demote -- every checked load carries real data. Nothing to do.")
            print(f"({skipped} table(s) unreadable / empty-on-read, left untouched.)")
            return 0

        print(f"WOULD RE-GRADE {len(demote)} run(s) success -> empty "
              f"(headline: the FED_FJC_IDB class of parse-failure load):\n")
        print(f"  {'SOURCE_ID':<34} {'LANDED':>10}  {'DENSITY':>8}  REASON")
        print(f"  {'-'*34} {'-'*10}  {'-'*8}  {'-'*30}")
        for _run_id, source_id, row_count, d in demote:
            rc = f"{row_count:,}" if isinstance(row_count, int) else str(row_count)
            print(f"  {source_id:<34} {rc:>10}  {d['populated_fraction']*100:7.2f}%  {d['reason']}")

        if not args.apply:
            print(f"\n({skipped} table(s) unreadable / empty-on-read, left untouched.)")
            print("\nPREVIEW only -- re-run with --apply to write STATUS='empty' on these runs.")
            return 0

        # ---- APPLY: row UPDATEs on INGEST_RUNS only (no schema change) ----
        fqn = (f'"{settings.meta_database}"."{settings.ingest_log_schema}".'
               f'"{settings.ingest_log_table}"')
        cur = conn.cursor()
        n = 0
        try:
            for run_id, source_id, _rc, d in demote:
                note = (f"[regraded {pd.Timestamp.utcnow():%Y-%m-%d}] DENSITY GATE: "
                        f"{d['reason']}; populated={d['populated_fraction']:.2%}, "
                        f"source_cols={d['source_cols']}, all_blank_cols={d['all_blank_cols']}. "
                        "Was STATUS='success' but carries no real data -- demoted to 'empty'.")
                cur.execute(
                    f"UPDATE {fqn} SET STATUS='empty', "
                    "MESSAGE = LEFT(COALESCE(MESSAGE,'') || ' || ' || %s, 4000) "
                    "WHERE RUN_ID = %s AND STATUS='success'",
                    (note, run_id))
                n += cur.rowcount or 0
            conn.commit()
        finally:
            cur.close()
        print(f"\nAPPLIED: re-graded {n} run(s) to STATUS='empty'. "
              "Catalog LIFECYCLE will follow on its next derive.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
