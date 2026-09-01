"""Bulk-load DOL enforcement datasets (OSHA, MSHA, WHD).

Two sources that DON'T require API keys:
  1. MSHA Open Government Data (arlweb.msha.gov) -- direct ZIP downloads,
     pipe-delimited text files, updated weekly. High-value mine safety data.
  2. OSHA ITA data (osha.gov/itadata) -- injury tracking, severe injuries.

The DOL API (apiprod.dol.gov/v4) requires a free API key from
dataportal.dol.gov/api-keys. If DOL_API_KEY is set in env, this script
will also pull OSHA inspection/violation data from the API.

    python scripts/dol_enforce_bulk_load.py              # preview
    python scripts/dol_enforce_bulk_load.py --run        # load all
    python scripts/dol_enforce_bulk_load.py --run --limit 5
"""
from __future__ import annotations

import argparse
import io
import os
import sys
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO))
from loadkit.archive import pick_member  # noqa: E402
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

TABLE_PREFIX = "FED_DOL"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

ENTITY_KEYS = {
    "MINE_ID", "CONTROLLER_ID", "OPERATOR_ID", "VIOLATOR_ID",
    "EVENT_NO", "DOCUMENT_NO", "VIOLATION_NO", "ACTIVITY_NR",
}

# MSHA Open Government Data -- direct ZIPs (pipe-delimited, updated weekly)
# Source: https://arlweb.msha.gov/OpenGovernmentData/OGIMSHA.asp
OSHA_MANIFEST = [
    {
        "name": "OSHA_INSPECTION",
        "table": "FED_DOL_OSHA_INSPECTION",
        "url": "https://enforcedata.dol.gov/data_catalogs/osha/osha_inspection.csv.zip",
        "description": "All OSHA workplace inspections since 1972 (ACTIVITY_NR keyed)",
        "sep": ",",
    },
    {
        "name": "OSHA_VIOLATION",
        "table": "FED_DOL_OSHA_VIOLATION",
        "url": "https://enforcedata.dol.gov/data_catalogs/osha/osha_violation.csv.zip",
        "description": "Citations issued from OSHA inspections (violation-level)",
        "sep": ",",
    },
    {
        "name": "OSHA_ACCIDENT",
        "table": "FED_DOL_OSHA_ACCIDENT",
        "url": "https://enforcedata.dol.gov/data_catalogs/osha/osha_accident.csv.zip",
        "description": "OSHA accident investigation records",
        "sep": ",",
    },
]

MSHA_MANIFEST = [
    {
        "name": "MSHA_MINES",
        "table": "FED_DOL_MSHA_MINES",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/Mines.zip",
        "description": "All mines under MSHA jurisdiction since 1970 (MINE_ID keyed)",
    },
    {
        "name": "MSHA_VIOLATIONS",
        "table": "FED_DOL_MSHA_VIOLATIONS",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/Violations.zip",
        "description": "Violations from MSHA inspections since 2000",
    },
    {
        "name": "MSHA_ACCIDENTS",
        "table": "FED_DOL_MSHA_ACCIDENTS",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/Accidents.zip",
        "description": "All mine accidents, injuries, illnesses since 2000",
    },
    {
        "name": "MSHA_INSPECTIONS",
        "table": "FED_DOL_MSHA_INSPECTIONS",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/Inspections.zip",
        "description": "All mine inspections since 2000 (EVENT_NO keyed)",
    },
    {
        "name": "MSHA_ASSESSED_VIOLATIONS",
        "table": "FED_DOL_MSHA_ASSESSED_VIOLATIONS",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/AssessedViolations.zip",
        "description": "Violations with penalty assessments since 2000",
    },
    {
        "name": "MSHA_EMPLOYMENT_YEARLY",
        "table": "FED_DOL_MSHA_EMPLOYMENT_YEARLY",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/MinesProdYearly.zip",
        "description": "Annual mine employment and production data",
    },
    {
        "name": "MSHA_CONTROLLER_HISTORY",
        "table": "FED_DOL_MSHA_CONTROLLER_HISTORY",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/ControllerOperatorHistory.zip",
        "description": "Controller/operator history at mining operations",
    },
    {
        "name": "MSHA_ADDRESSES",
        "table": "FED_DOL_MSHA_ADDRESSES",
        "url": "https://arlweb.msha.gov/OpenGovernmentData/DataSets/AddressofRecord.zip",
        "description": "Mine addresses of record",
    },
]


def _load_dol_zip(conn, entry: dict, max_rows: int) -> int:
    """Load a DOL enforcement ZIP (pipe-delimited MSHA or comma-delimited OSHA)."""
    tbl = entry["table"]
    sep = entry.get("sep", "|")
    print(f"  Downloading {entry['name']}...")
    try:
        resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
        resp.raise_for_status()
    except Exception as e:
        print(f"    FAILED download: {str(e)[:100]}")
        return 0

    import zipfile, hashlib, datetime as dt, uuid
    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            # ONE data member or an explicit entry["member"] pattern -- never
            # largest-wins (the EIA-860 multi-file truncation trap).
            # 'definition' files excluded via the pattern default below.
            target = pick_member(
                zf,
                pattern=entry.get("member", r"^(?!.*definition)"),
                suffixes=(".txt", ".csv"),
            )
            with zf.open(target) as f:
                content = f.read()

        df = pd.read_csv(io.BytesIO(content), sep=sep, dtype=str,
                         nrows=max_rows + 1, low_memory=False, encoding_errors="replace")
        if len(df) > max_rows:
            raise RuntimeError(
                f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
                f"refusing to silently truncate. Pass a higher max_rows explicitly.")
        if df.empty:
            return 0

        # Clean columns
        df.columns = [bulk.sf_col(c) for c in df.columns]

        # Provenance
        sha = hashlib.sha256(content).hexdigest()
        run_id = str(uuid.uuid4())
        started = dt.datetime.now(dt.timezone.utc)
        df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
        df[bulk.META_SOURCE_RUN_ID] = run_id
        df[bulk.META_SRC_SHA256] = sha

        from snowflake.connector.pandas_tools import write_pandas
        ok, _c, _n, _ = write_pandas(
            conn, df, table_name=tbl,
            database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
            auto_create_table=True, overwrite=True, quote_identifiers=False,
        )
        if not ok:
            raise RuntimeError("write_pandas failed")
        print(f"    -> {tbl}: {len(df):,} rows")
        return len(df)
    except Exception as e:
        print(f"    FAILED load: {str(e)[:120]}")
        return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="DOL enforcement bulk loader (MSHA + OSHA)")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--limit", type=int, default=len(OSHA_MANIFEST) + len(MSHA_MANIFEST))
    ap.add_argument("--max-rows", type=int, default=None)
    ap.add_argument("--force", action="store_true", help="Reload even if table exists (for re-pours)")
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING")

    # Combine manifests
    all_entries = OSHA_MANIFEST + MSHA_MANIFEST

    # Filter to not-yet-loaded (or --force to reload broken tables)
    to_load = []
    for entry in all_entries[:args.limit]:
        if entry["table"] in loaded and not args.force:
            print(f"  SKIP {entry['table']} (already loaded)")
        else:
            to_load.append(entry)

    print(f"\n{len(to_load)} DOL datasets to load")

    if not args.run:
        print("\n(preview only -- add --run to load)")
        for i, e in enumerate(to_load, 1):
            print(f"  {i}. {e['table']:45s} — {e['description']}")
        return 0

    # Parallel load (4 workers -- MSHA ZIPs can be large)
    print(f"\nLoading {len(to_load)} datasets (parallel, 4 workers)...")

    tasks = []
    for entry in to_load:
        tasks.append({
            "fn": _load_dol_zip,
            "args": (conn, entry, args.max_rows),
            "name": entry["table"],
        })

    results = bulk.parallel_load(tasks, max_workers=4, label="DOL")
    ok = sum(1 for r in results if "result" in r and r["result"])
    total_rows = sum(r.get("result", 0) for r in results if "result" in r)

    # Run quality gate on each successfully loaded table
    import uuid as _uuid
    run_id = str(_uuid.uuid4())
    dq_failures = 0
    for r in results:
        if "result" in r and r["result"]:
            tbl = r["name"]
            passed, _ = bulk.run_quality_gate(conn, f"fed_dol_{tbl.lower()}", tbl, run_id)
            if not passed:
                dq_failures += 1

    print(f"\nDone: {ok}/{len(to_load)} datasets loaded, {total_rows:,} total rows"
          + (f", {dq_failures} DQ failures" if dq_failures else ""))
    conn.close()
    return 1 if dq_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
