#!/usr/bin/env python3
"""Standing check: flag DEGENERATE landed sources -- tables that landed rows but
whose columns collapse to <=1 distinct value (the dead-scrape signature: a loader
captured page chrome / nav / cookie banners instead of data).

This is the automatic catcher for the 2026-06-27 discovery sweep's "dead-scrape
pile" (13 sources) and a guardrail against the next one. It is READ-ONLY -- it
never writes; pair it with scripts/propose_dead_scrape_demote.py to act on the list.

    python3 scripts/degenerate_load_detector.py              # full report
    python3 scripts/degenerate_load_detector.py --sample 8000
    python3 scripts/degenerate_load_detector.py --json out.json
    python3 scripts/degenerate_load_detector.py --all        # include portal_* samples

Signal per source (sampled, cheap):
  data_cols       non-meta columns in the landing table
  degenerate_cols columns with <=1 distinct non-blank value in the sample
  degenerate_frac degenerate_cols / data_cols
A source is FLAGGED degenerate when degenerate_frac >= --threshold (default 0.85):
i.e. almost every column is constant or blank -- no real data varies.
"""
from __future__ import annotations

import argparse
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


def _landed_sources(conn, include_portal: bool):
    """(source_id, landing_table) for every landed/modeled catalog source."""
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT source_id, COALESCE(landing_fqn,'')
               FROM LIBRARY_META.REGISTRY.CATALOG
               WHERE lifecycle IN ('landed','modeled')
               ORDER BY source_id""")
        rows = cur.fetchall()
    except Exception:
        # Fallback: latest success run per source from INGEST_RUNS
        cur.execute(
            """SELECT DISTINCT source_id, '' FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS r
               WHERE status='success' ORDER BY source_id""")
        rows = cur.fetchall()
    finally:
        cur.close()
    out = []
    for sid, fqn in rows:
        if not include_portal and sid.lower().startswith("portal_"):
            continue
        out.append((sid, sid.upper()))
    return out


def _data_columns(conn, table: str):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
            "WHERE table_schema='LANDING' AND table_name=%s ORDER BY ordinal_position", (table,))
        cols = [c[0] for c in cur.fetchall()]
    finally:
        cur.close()
    return [c for c in cols if c.upper() not in META_COLS]


def _profile(conn, table: str, cols: list[str], sample: int):
    """One query: row count + COUNT(DISTINCT NULLIF(TRIM(col),'')) per column on a sample."""
    if not cols:
        return None
    sel = ["COUNT(*) AS _n"] + [
        f'COUNT(DISTINCT NULLIF(TRIM("{c}"),\'\')) AS "d_{i}"' for i, c in enumerate(cols)]
    sql = (f"SELECT {', '.join(sel)} FROM "
           f"(SELECT * FROM LIBRARY_RAW.LANDING.\"{table}\" LIMIT {int(sample)})")
    cur = conn.cursor()
    try:
        cur.execute(sql)
        row = cur.fetchone()
    except Exception as e:
        return {"error": str(e)[:120]}
    finally:
        cur.close()
    n = row[0]
    distincts = list(row[1:])
    return {"n": n, "distincts": dict(zip(cols, distincts))}


def main() -> int:
    ap = argparse.ArgumentParser(description="Flag degenerate (dead-scrape) landed sources.")
    ap.add_argument("--sample", type=int, default=5000, help="rows sampled per table (default 5000)")
    ap.add_argument("--threshold", type=float, default=0.85,
                    help="flag when degenerate_frac >= this (default 0.85)")
    ap.add_argument("--all", action="store_true", help="include portal_* samples")
    ap.add_argument("--json", type=str, default="", help="write full results to this path")
    args = ap.parse_args()

    conn = snow.connect()
    results = []
    try:
        sources = _landed_sources(conn, args.all)
        print(f"profiling {len(sources)} landed/modeled source(s) "
              f"(sample={args.sample}, flag>= {args.threshold:.0%} degenerate cols)...\n")
        for sid, table in sources:
            cols = _data_columns(conn, table)
            if not cols:
                continue
            prof = _profile(conn, table, cols, args.sample)
            if prof is None or "error" in (prof or {}):
                continue
            n = prof["n"]
            degen = [c for c, d in prof["distincts"].items() if (d or 0) <= 1]
            frac = len(degen) / len(cols)
            results.append({
                "source_id": sid, "rows_sampled": n, "data_cols": len(cols),
                "degenerate_cols": len(degen), "degenerate_frac": round(frac, 3),
                "flagged": frac >= args.threshold,
                "degenerate_col_names": degen if frac >= args.threshold else [],
            })

        flagged = sorted([r for r in results if r["flagged"]],
                         key=lambda r: (-r["degenerate_frac"], r["rows_sampled"]))
        print(f"{'='*78}\nDEGENERATE (dead-scrape) CANDIDATES: {len(flagged)} of {len(results)} sources\n{'='*78}")
        print(f"  {'SOURCE_ID':<40} {'ROWS':>7} {'COLS':>5} {'DEGEN':>6} {'FRAC':>6}")
        print(f"  {'-'*40} {'-'*7} {'-'*5} {'-'*6} {'-'*6}")
        for r in flagged:
            print(f"  {r['source_id']:<40} {r['rows_sampled']:>7} {r['data_cols']:>5} "
                  f"{r['degenerate_cols']:>6} {r['degenerate_frac']*100:5.0f}%")

        near = sorted([r for r in results if not r["flagged"] and r["degenerate_frac"] >= args.threshold - 0.15],
                      key=lambda r: -r["degenerate_frac"])
        if near:
            print(f"\n  -- near-threshold (review): --")
            for r in near[:12]:
                print(f"  {r['source_id']:<40} {r['rows_sampled']:>7} {r['data_cols']:>5} "
                      f"{r['degenerate_cols']:>6} {r['degenerate_frac']*100:5.0f}%")

        if args.json:
            Path(args.json).write_text(json.dumps(results, indent=2))
            print(f"\nfull results -> {args.json}")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
