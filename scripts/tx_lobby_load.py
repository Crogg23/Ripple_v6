#!/usr/bin/env python3
"""Deterministic loader for the Texas Ethics Commission Lobby Activities bulk data.

One ZIP of 10 flat CSVs (cover sheet + schedules A-G), no key required. Lands each
CSV as its own RAW table, all prefixed TX_LOBBY_, joined on filerIdent/reportInfoIdent.

Snapshot-replace (overwrite=True) per table -> idempotent; rerun never duplicates.

    python scripts/tx_lobby_load.py          # preview (fetch + sample, no write)
    python scripts/tx_lobby_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402

URL = "https://prd.tecprd.ethicsefile.com/public/lobby/public/TEC_LA_CSV.zip"
ZIP_PATH = _LIB / "raw_downloads" / "tx_lobby.zip"
EXTRACT_DIR = _LIB / "raw_downloads" / "tx_lobby"

# csv filename -> (source_id suffix, table suffix, description)
FILES = {
    "LaCvr.csv": ("tx_lobby_cover", "TX_LOBBY_COVER", "Form LA Cover Sheet totals (one row per lobby activity report filed)"),
    "LaSub.csv": ("tx_lobby_subject_matter", "TX_LOBBY_SUBJECT_MATTER", "Subject Matter - Schedule A"),
    "LaDock.csv": ("tx_lobby_dockets", "TX_LOBBY_DOCKETS", "Dockets - Schedule A"),
    "LaTran.csv": ("tx_lobby_transportation", "TX_LOBBY_TRANSPORTATION", "Transportation - Schedule B"),
    "LaFood.csv": ("tx_lobby_food_beverage", "TX_LOBBY_FOOD_BEVERAGE", "Food/Beverages - Schedule C"),
    "LaEnt.csv": ("tx_lobby_entertainment", "TX_LOBBY_ENTERTAINMENT", "Entertainment - Schedule D"),
    "LaGift.csv": ("tx_lobby_gifts", "TX_LOBBY_GIFTS", "Gifts - Schedule E"),
    "LaAwrd.csv": ("tx_lobby_awards", "TX_LOBBY_AWARDS", "Awards/Mementos - Schedule F"),
    "LaEvnt.csv": ("tx_lobby_events", "TX_LOBBY_EVENTS", "Events - Schedule G"),
    "LaI4E.csv": ("tx_lobby_individual_reporting", "TX_LOBBY_INDIVIDUAL_REPORTING", "Individual Reporting for Entity"),
}


def _register(conn, sid: str, table: str, desc: str, rows: int) -> None:
    cfg = {
        "source_id": sid,
        "name": f"Texas Ethics Commission Lobby Activities — {desc}",
        "publisher": "Texas Ethics Commission",
        "url": "https://www.ethics.state.tx.us/search/lobby/",
        "description": f"{desc}. Part of the TEC Lobby Activities Reports (LA) bulk CSV export, "
                       "electronic filings from 2005 forward plus paper-filing totals from 1993.",
        "jurisdiction": "state:TX", "category": "Politics", "subcategory": "Lobbying",
        "unit_of_observation": f"one row = one {desc.split(' - ')[0].lower()} record",
        "geographic_scope": "Texas", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "periodic",
        "volume": f"{rows:,} rows", "license_terms": "Public record (TEC)",
        "join_keys": "filerIdent, reportInfoIdent",
        "accountability_relevance": "Texas state lobbyist activity/spend disclosure.",
        "priority_tier": "2", "landing_table": table,
        "notes": "Loaded by scripts/tx_lobby_load.py (LLM-free, bulk CSV via TEC_LA_CSV.zip, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for TX Ethics Commission lobby activities bulk CSVs")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== Texas Ethics Commission Lobby Activities ===", flush=True)
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not ZIP_PATH.exists():
        r = requests.get(URL, timeout=180)
        r.raise_for_status()
        ZIP_PATH.write_bytes(r.content)
    if not EXTRACT_DIR.exists() or not any(EXTRACT_DIR.iterdir()):
        EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extractall(EXTRACT_DIR)

    dfs = {}
    for fname, (sid, table, desc) in FILES.items():
        p = EXTRACT_DIR / fname
        df = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8", on_bad_lines="warn")
        dfs[fname] = df
        print(f"  {fname:14} {len(df):>8,} rows  -> {table}", flush=True)

    if not args.run:
        print("\nSAMPLE (LaCvr.csv, first 3 rows, key cols):")
        cvr = dfs["LaCvr.csv"]
        for _, row in cvr.head(3).iterrows():
            print(f"  filerIdent={row['filerIdent']}  filerName={row['filerName']}  periodEndDt={row['periodEndDt']}")
        print(f"\ndistinct filerIdent in LaCvr: {cvr['filerIdent'].nunique():,} of {len(cvr):,} rows")
        print("\nPREVIEW only — add --run to land.")
        return 0

    conn = snow.connect()
    gate_failed = []
    try:
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        from snowflake.connector.pandas_tools import write_pandas
        for fname, (sid, table, desc) in FILES.items():
            df = dfs[fname]
            started = ingest._utcnow()
            run_id = str(uuid.uuid4())
            sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
            if settings.skip_if_unchanged:
                last_sha = ingest._latest_success_sha(conn, sid)
                if last_sha == sha:
                    print(f"skip {table} (sha unchanged)", flush=True)
                    continue
            out = ingest._stringify(df)
            out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = sha
            out.columns = [ingest._sf_col(c) for c in out.columns]
            ok, _c, nrows, _ = write_pandas(conn, out, table_name=table,
                                            database=settings.raw_database, schema=settings.raw_schema,
                                            auto_create_table=True, overwrite=True, quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write_pandas failed for {table}")
            ended = ingest._utcnow()
            dens = ingest.assess_density(df)
            status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
            if status != "success":
                print(f"  QUALITY GATE FAILED for {table}: {dens}")
                gate_failed.append(table)
            ingest._log_run(conn, sid, run_id, status, len(df), None, sha, URL, started, ended,
                            f"TX TEC Lobby {desc}; {len(df):,} rows; density {dens.get('populated_fraction')}")
            _register(conn, sid, table, desc, len(df))
            print(f"LOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{table} "
                  f"(status={status})", flush=True)
    finally:
        conn.close()
    if gate_failed:
        raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(gate_failed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
