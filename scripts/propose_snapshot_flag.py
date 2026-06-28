#!/usr/bin/env python3
"""Preview (and optionally apply) a SNAPSHOT-vs-PANEL temporal-coverage flag on the
catalog (discovery sweep theme #3: 'looks like a panel, is a snapshot'). Several
landed sources are a single day / single quarter / single year / API-row-capped
pull, so a query that treats them as a longitudinal panel silently reads depth that
is not there. This stamps them so a 'panel' query knows.

Adds a TEMPORAL_COVERAGE column ('snapshot' | 'panel') + TEMPORAL_COVERAGE_NOTE to
SOURCE_REGISTRY (idempotent ADD COLUMN IF NOT EXISTS), then marks the known
single-cross-section sources 'snapshot'. preview by default, snapshot-rollback,
--apply gated (Chris runs --apply; the auto-classifier blocks agent catalog writes).

    python3 scripts/propose_snapshot_flag.py            # preview only
    python3 scripts/propose_snapshot_flag.py --apply    # Chris runs this

NB: TEMPORAL_COVERAGE is added to the base table; to surface it in the CATALOG view
add it to that view's SELECT (the view DDL lives only in Snowflake -- GET_DDL first).
"""
from __future__ import annotations

import argparse
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

REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_SNAPSHOTFLAG_20260628"

# (source_id, finding, reason) -- confirmed single-cross-section / capped pulls.
SNAPSHOT = [
    ("fed_noaa_ais",                  "#4",   "single 24h snapshot (2024-01-01 only); no second day to diff -- no behavior-over-time"),
    ("fed_cms_hcris",                 "#11",  "single most-recent cost-report cycle (99.9% FY2023-24), not a panel"),
    ("fed_cfpb_complaints",           "#26",  "two 250-row 'most-recent' API pulls (500 rows); dates are ingestion ts, not complaint dates"),
    ("fed_sec_edgar_financials",      "#42",  "single quarterly drop (100% filed 2024-Q4)"),
    ("fed_usgs_earthquakes",          "#46",  "30-day rolling snapshot (not seismic history)"),
    ("fed_federal_register_documents","#58",  "most-recent-5000 API-capped pull (~9.5-week window)"),
    ("fed_noaa_storm_events",         "#77",  "single-year snapshot (all rows 2025; NCEI goes back to 1950)"),
    ("fed_clinicaltrials",            "#98",  "500-row sample, not the full registry"),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Flag SNAPSHOT vs PANEL temporal coverage.")
    ap.add_argument("--apply", action="store_true", help="write the flag (default previews)")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        sids = [s[0] for s in SNAPSHOT]
        ph = ",".join(["%s"] * len(sids))
        cur.execute(f"SELECT source_id, COALESCE(volume,''), COALESCE(update_cadence,'') "
                    f"FROM {REGISTRY} WHERE source_id IN ({ph})", tuple(sids))
        cur_state = {r[0]: (r[1], r[2]) for r in cur.fetchall()}
        cur.close()

        mode = "APPLY" if args.apply else "PREVIEW (reads only)"
        print("=" * 78)
        print(f"SNAPSHOT-vs-PANEL temporal flag (theme #3)  --  {mode}")
        print("=" * 78)
        print(f"\nWould ADD COLUMN TEMPORAL_COVERAGE/_NOTE (if absent) and mark "
              f"{len(SNAPSHOT)} sources 'snapshot':\n")
        print(f"  {'SOURCE_ID':<34} {'FIND':>5}  REASON")
        print(f"  {'-'*34} {'-'*5}  {'-'*40}")
        for sid, finding, reason in SNAPSHOT:
            present = "" if sid in cur_state else "  [NOT IN REGISTRY -- skip]"
            print(f"  {sid:<34} {finding:>5}  {reason[:54]}{present}")

        if not args.apply:
            print("\nPREVIEW only. Re-run with --apply to write "
                  f"(snapshots first; rollback via {BACKUP}).")
            return 0

        cur = conn.cursor()
        cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
        print(f"\n  rollback snapshot -> {BACKUP}")
        cur.execute(f"ALTER TABLE {REGISTRY} ADD COLUMN IF NOT EXISTS TEMPORAL_COVERAGE VARCHAR")
        cur.execute(f"ALTER TABLE {REGISTRY} ADD COLUMN IF NOT EXISTS TEMPORAL_COVERAGE_NOTE VARCHAR")
        # default everything landed/modeled to 'panel', then override the snapshots
        cur.execute(f"UPDATE {REGISTRY} SET TEMPORAL_COVERAGE='panel' "
                    "WHERE TEMPORAL_COVERAGE IS NULL")
        n = 0
        for sid, finding, reason in SNAPSHOT:
            if sid not in cur_state:
                continue
            cur.execute(
                f"UPDATE {REGISTRY} SET TEMPORAL_COVERAGE='snapshot', "
                "TEMPORAL_COVERAGE_NOTE=%s WHERE source_id=%s",
                (f"{finding}: {reason}", sid))
            n += cur.rowcount or 0
        conn.commit()
        cur.close()
        print(f"  marked {n} source(s) 'snapshot' (rest default 'panel').")
        print("  NOTE: add TEMPORAL_COVERAGE to the CATALOG view SELECT to surface it.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
