#!/usr/bin/env python3
"""Preview (and optionally apply) SOURCE_REGISTRY.VOLUME updates for the sources the
2026-06-28 APPEND backfills deepened. Those loaders streamed new rows + logged the run
but did NOT re-register, so the catalog still advertises the old snapshot volume (e.g.
storm 'VOLUME=72,360 rows' while LANDING now holds 1.78M).

Scoped to an EXPLICIT backfill list on purpose -- the IRS BMF / Open Payments 2022
loaders self-registered with a correct volume, and the rest of the catalog's
descriptive volumes ('~8-9 million', '~1.1M rows/yr') are fine as estimates and out of
scope for this sync. Preview by default, rollback-snapshotted, --apply gated (the
catalog-write classifier blocks the agent; Chris runs --apply).

    python3 scripts/propose_registry_volume_sync.py            # preview
    python3 scripts/propose_registry_volume_sync.py --apply    # Chris runs this
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
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_VOLSYNC_20260628"

# Sources whose APPEND backfill (2026-06-28) deepened LANDING without re-registering.
# (fed_irs_bmf + fed_cms_open_payments_2022 self-registered, so they're excluded.)
BACKFILLED = [
    ("fed_noaa_ais",                 "single-day snapshot -> 8-day series (2024-01-01..08)"),
    ("fed_noaa_storm_events",        "single-year (2025) -> 30-year history (1996-2025)"),
    ("fed_usgs_earthquakes",         "30-day rolling -> 2010-2026 history (M2.5+)"),
    ("fed_federal_register_documents","most-recent-5000 cap -> 2023-2026 paginated"),
    ("fed_sec_edgar_financials",     "single quarter -> 8 quarters (2023q1-2024q4)"),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync backfilled sources' SOURCE_REGISTRY.VOLUME to live counts.")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        props = []
        for sid, why in BACKFILLED:
            cur.execute(f"SELECT COALESCE(volume,'(none)') FROM {REGISTRY} WHERE source_id=%s", (sid,))
            row = cur.fetchone()
            if not row:
                continue
            old = row[0]
            cur.execute(f"SELECT row_count FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
                        f"WHERE table_schema='LANDING' AND table_name=%s", (sid.upper(),))
            rc = cur.fetchone()
            live = rc[0] if rc else None
            if live is not None:
                props.append((sid, old, live, why))
        cur.close()

        mode = "APPLY" if args.apply else "PREVIEW (reads only)"
        print("=" * 86)
        print(f"REGISTRY VOLUME SYNC for 2026-06-28 backfills  --  {mode}")
        print("=" * 86)
        print(f"\n  {'SOURCE_ID':<32} {'CATALOG VOLUME (old)':>22} {'LIVE ROWS':>12}  BACKFILL")
        print(f"  {'-'*32} {'-'*22} {'-'*12}  {'-'*30}")
        for sid, old, live, why in props:
            print(f"  {sid:<32} {str(old)[:22]:>22} {live:>12,}  {why[:38]}")

        if not args.apply:
            print(f"\n{len(props)} VOLUME update(s). Re-run with --apply to write "
                  f"(snapshots first; rollback via {BACKUP}).")
            return 0

        cur = conn.cursor()
        cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
        print(f"\n  rollback snapshot -> {BACKUP}")
        for sid, _old, live, why in props:
            cur.execute(f"UPDATE {REGISTRY} SET volume = %s, "
                        "notes = LEFT(COALESCE(notes,'') || ' || [backfill 2026-06-28] ' || %s, 4000) "
                        "WHERE source_id = %s", (f"{live:,} rows", why, sid))
        conn.commit()
        cur.close()
        print(f"  applied {len(props)} VOLUME update(s).")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
