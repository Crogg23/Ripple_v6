"""Bulk-load GHGRP, RCRAInfo handlers, and National Response Center incidents.

Phase 2 continuation (EPA facility family + NRC). Three independent sources,
one script for convenience.

  GHGRP    -- EPA Envirofacts efservice REST API (data.epa.gov/efservice).
              PUB_DIM_FACILITY (facility dimension, has FRS_ID) +
              PUB_FACTS_SECTOR_GHG_EMISSION (facility_id, year, gas, co2e).
  RCRA     -- EPA ECHO known-manifest ZIP (rcra_downloads.zip), same house
              style as scripts/epa_echo_bulk_load.py.
  NRC      -- USCG National Response Center yearly incident files
              (nrc.uscg.mil/FOIAFiles/CYxx.xlsx), 1990-2026, concatenated.

    python scripts/epa_ghgrp_rcra_nrc_bulk_load.py --run --source ghgrp
    python scripts/epa_ghgrp_rcra_nrc_bulk_load.py --run --source rcra
    python scripts/epa_ghgrp_rcra_nrc_bulk_load.py --run --source nrc
    python scripts/epa_ghgrp_rcra_nrc_bulk_load.py --run --source all
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import sys
import uuid
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import pandas as pd
import requests

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


def _load_df(conn, df: pd.DataFrame, tbl: str, sha: str, run_id: str) -> int:
    """Land an already-built dataframe with provenance stamps (mirrors _bulk_load_utils._load_bytes)."""
    from snowflake.connector.pandas_tools import write_pandas

    if df.empty:
        return 0
    df = df.copy()
    df.columns = [bulk.sf_col(c) for c in df.columns]
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    df[bulk.META_INGESTED_AT] = started
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    df = df.astype(str).where(df.notna(), None)

    ok, _c, n, _ = write_pandas(
        conn, df, table_name=tbl,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    return len(df)


# ---------------------------------------------------------------------------
# GHGRP -- Envirofacts efservice
# ---------------------------------------------------------------------------
GHGRP_TABLES = {
    "FED_EPA_GHGRP_FACILITY": "PUB_DIM_FACILITY",
    "FED_EPA_GHGRP_EMISSION": "PUB_FACTS_SECTOR_GHG_EMISSION",
}


def load_ghgrp(conn, max_rows: int) -> None:
    run_id = str(uuid.uuid4())
    for tbl, ef_table in GHGRP_TABLES.items():
        count_url = f"https://data.epa.gov/efservice/{ef_table}/COUNT/CSV"
        r = requests.get(count_url, headers=USER_AGENT, timeout=60)
        r.raise_for_status()
        total = int(r.text.strip().splitlines()[-1])
        print(f"  {ef_table}: {total:,} rows claimed")
        if total > max_rows:
            raise RuntimeError(
                f"{tbl}: envirofacts reports {total:,} rows > max_rows={max_rows:,} -- "
                f"refusing to silently truncate.")

        rows_url = f"https://data.epa.gov/efservice/{ef_table}/rows/0:{total}/CSV"
        resp = requests.get(rows_url, headers=USER_AGENT, timeout=600)
        resp.raise_for_status()
        sha = hashlib.sha256(resp.content).hexdigest()
        df = pd.read_csv(io.BytesIO(resp.content), dtype=str, low_memory=False,
                          encoding_errors="replace")
        n = _load_df(conn, df, tbl, sha, run_id)
        passed, report = bulk.run_quality_gate(
            conn, f"fed_epa_ghgrp_{tbl.lower()}", tbl, run_id,
            sha256=sha, row_count=n, source_url=rows_url,
            file_bytes=len(resp.content))
        print(f"  -> {tbl}: {n:,} rows landed (claimed {total:,}), DQ passed={passed}")


# ---------------------------------------------------------------------------
# RCRA -- EPA ECHO known-manifest ZIP
# ---------------------------------------------------------------------------
RCRA_ENTITY_KEYS = {
    "REGISTRY_ID", "FRS_ID", "HANDLER_ID", "RCRA_ID", "EPA_ID_NUMBER", "ID_NUMBER",
}
RCRA_ZIP = "https://echo.epa.gov/files/echodownloads/rcra_downloads.zip"


def load_rcra(conn, max_rows: int) -> None:
    run_id = str(uuid.uuid4())
    results = bulk.load_zip_csvs(
        conn, RCRA_ZIP, "FED_EPA_RCRA", RCRA_ENTITY_KEYS,
        user_agent=USER_AGENT, max_rows=max_rows, timeout=900)
    if not results:
        raise RuntimeError("RCRA: no CSVs with recognized entity keys found in ZIP")
    for tbl, n, keys in results:
        passed, report = bulk.run_quality_gate(
            conn, f"fed_epa_rcra_{tbl.lower()}", tbl, run_id,
            row_count=n, source_url=RCRA_ZIP)
        print(f"  -> {tbl}: {n:,} rows landed (keys: {keys}), DQ passed={passed}")


# ---------------------------------------------------------------------------
# NRC -- USCG National Response Center yearly incident files
# ---------------------------------------------------------------------------
NRC_TABLE = "FED_USCG_NRC_INCIDENTS"
NRC_YEARS = list(range(1990, 2027))  # CY90..CY26


def load_nrc(conn, max_rows: int) -> None:
    run_id = str(uuid.uuid4())
    frames = []
    total_bytes = 0
    for y in NRC_YEARS:
        suffix = f"{y % 100:02d}"
        url = f"https://nrc.uscg.mil/FOIAFiles/CY{suffix}.xlsx"
        try:
            r = requests.get(url, timeout=120)
        except Exception as e:
            print(f"  CY{suffix}: fetch failed ({str(e)[:80]}) -- skipping")
            continue
        if r.status_code != 200 or len(r.content) < 5000:
            print(f"  CY{suffix}: status={r.status_code} size={len(r.content)} -- skipping")
            continue
        try:
            df = pd.read_excel(io.BytesIO(r.content))
        except Exception as e:
            print(f"  CY{suffix}: read_excel failed ({str(e)[:80]}) -- skipping")
            continue
        if df.empty:
            print(f"  CY{suffix}: empty -- skipping")
            continue
        df["_SRC_YEAR"] = y
        frames.append(df)
        total_bytes += len(r.content)
        print(f"  CY{suffix}: {len(df):,} rows")

    if not frames:
        raise RuntimeError("NRC: no yearly files loaded")

    full = pd.concat(frames, ignore_index=True, sort=False)
    if len(full) > max_rows:
        raise RuntimeError(
            f"NRC: combined {len(full):,} rows > max_rows={max_rows:,} -- "
            f"refusing to silently truncate.")

    sha = hashlib.sha256(pd.util.hash_pandas_object(full, index=False).values.tobytes()).hexdigest()
    n = _load_df(conn, full, NRC_TABLE, sha, run_id)
    passed, report = bulk.run_quality_gate(
        conn, f"fed_uscg_nrc_{NRC_TABLE.lower()}", NRC_TABLE, run_id,
        sha256=sha, row_count=n, source_url="https://nrc.uscg.mil/FOIAFiles/",
        file_bytes=total_bytes)
    print(f"\n  -> {NRC_TABLE}: {n:,} rows landed across {len(frames)} years, DQ passed={passed}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--source", choices=["ghgrp", "rcra", "nrc", "all"], default="all")
    ap.add_argument("--max-rows", type=int, default=5_000_000)
    args = ap.parse_args()

    if not args.run:
        print("(preview only -- add --run to load)")
        print("Sources: ghgrp (envirofacts efservice), rcra (ECHO zip), nrc (yearly xlsx)")
        return 0

    conn = snow.connect()
    try:
        if args.source in ("ghgrp", "all"):
            print("\n=== GHGRP ===")
            load_ghgrp(conn, args.max_rows)
        if args.source in ("rcra", "all"):
            print("\n=== RCRA ===")
            load_rcra(conn, args.max_rows)
        if args.source in ("nrc", "all"):
            print("\n=== NRC ===")
            load_nrc(conn, args.max_rows)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
