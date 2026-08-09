#!/usr/bin/env python3
"""Chunked degenerate-column profiler for ULTRA-WIDE landing tables (1,000+ cols).

degenerate_load_detector.py profiles every column in ONE query -- that explodes
(compile time / 2MB statement cap) on tables like the 3,300-col College Scorecard
copies. This tool does the same COUNT(DISTINCT NULLIF(TRIM(col),'')) signal but
in column batches, so any width is safe. READ-ONLY.

    python3 scripts/wide_table_profiler.py TABLE_A TABLE_B --sample 3000
    python3 scripts/wide_table_profiler.py TABLE_A --batch 150 --json out.json

Per table it reports: rows, data cols, degenerate cols (<=1 distinct non-blank),
degenerate fraction, and a content fingerprint (row count + per-batch distinct
vector hash) so two tables can be compared for duplicate content cheaply.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402

META_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"}
BLOB_TYPES = {"VARIANT", "OBJECT", "ARRAY"}


def data_columns(conn, table: str) -> list[str]:
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT column_name, data_type FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
            "WHERE table_schema='LANDING' AND table_name=%s ORDER BY ordinal_position",
            (table,))
        rows = cur.fetchall()
    finally:
        cur.close()
    return [c for c, t in rows if c.upper() not in META_COLS and t.upper() not in BLOB_TYPES]


def profile_table(conn, table: str, cols: list[str], sample: int, batch: int) -> dict:
    """Batched COUNT(DISTINCT) profile. Returns per-column distincts + fingerprint."""
    distincts: dict[str, int] = {}
    n_rows = None
    fp = hashlib.sha256()
    for i in range(0, len(cols), batch):
        chunk = cols[i:i + batch]
        sel = ["COUNT(*)"] + [
            f'COUNT(DISTINCT NULLIF(TRIM("{c}"),\'\'))' for c in chunk]
        # Deterministic sample (ORDER BY first col of table would cost more; SAMPLE
        # is non-deterministic across queries, so for fingerprint comparability we
        # scan full table when small, sample only when big.)
        src = (f'LIBRARY_RAW.LANDING."{table}"' if sample <= 0 else
               f'(SELECT * FROM LIBRARY_RAW.LANDING."{table}" SAMPLE ({int(sample)} ROWS))')
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT {', '.join(sel)} FROM {src}")
            row = cur.fetchone()
        finally:
            cur.close()
        n_rows = row[0]
        for c, d in zip(chunk, row[1:]):
            distincts[c] = d or 0
        fp.update(",".join(f"{c}={d or 0}" for c, d in zip(chunk, row[1:])).encode())
    degen = [c for c, d in distincts.items() if d <= 1]
    return {
        "table": table, "rows": n_rows, "data_cols": len(cols),
        "degenerate_cols": len(degen),
        "degenerate_frac": round(len(degen) / len(cols), 3) if cols else None,
        "fingerprint": fp.hexdigest()[:16],
        "sample_degen_names": degen[:15],
        "distincts": distincts,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Chunked profiler for ultra-wide landing tables.")
    ap.add_argument("tables", nargs="+", help="LANDING table names")
    ap.add_argument("--sample", type=int, default=0,
                    help="rows sampled per query (0 = full table; fine for small-row wide tables)")
    ap.add_argument("--batch", type=int, default=200, help="columns per query (default 200)")
    ap.add_argument("--json", type=str, default="", help="write full results to this path")
    args = ap.parse_args()

    conn = snow.connect()
    conn.cursor().execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 120")
    out = []
    try:
        for t in args.tables:
            t = t.upper()
            cols = data_columns(conn, t)
            if not cols:
                print(f"{t}: no profilable columns (blob-only or missing)")
                continue
            r = profile_table(conn, t, cols, args.sample, args.batch)
            out.append(r)
            print(f"{t}: rows={r['rows']:,} cols={r['data_cols']:,} "
                  f"degenerate={r['degenerate_cols']:,} ({r['degenerate_frac']:.0%}) "
                  f"fingerprint={r['fingerprint']}")
        if len(out) > 1:
            fps = {r["fingerprint"] for r in out}
            print("\nDUPLICATE CHECK: " + (
                "all tables have IDENTICAL content fingerprints" if len(fps) == 1
                else f"{len(fps)} distinct fingerprints -- contents differ"))
        if args.json:
            slim = [{k: v for k, v in r.items() if k != "distincts"} for r in out]
            Path(args.json).write_text(json.dumps({"results": slim}, indent=2))
            print(f"full results -> {args.json}")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
