#!/usr/bin/env python3
"""Loader for the NTSB Aviation Accident/Incident Database (avall.mdb bulk export).

NTSB publishes the current rolling aviation database as a Microsoft Access
(.mdb) file at data.ntsb.gov/avdata. This loader downloads the zip, opens the
.mdb via the Windows "Microsoft Access Driver" ODBC driver (pyodbc), and lands
the two core tables:
  - events   (one row = one accident/incident, ev_id key)
  - aircraft (one row = one aircraft in that event, ev_id + Aircraft_Key key)

Older history (pre-2008, pre-1982) ships as separate zips on the same page --
not loaded here; this loader covers the current rolling database NTSB serves
as "the" bulk download.

    python scripts/ntsb_aviation_load.py          # preview (fetch + sample, no write)
    python scripts/ntsb_aviation_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import tempfile
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

URL = ("https://data.ntsb.gov/avdata/FileDirectory/DownloadFile"
       "?fileID=C%3A%5Cavdata%5Cavall.zip")

TABLES = {
    "events": "fed_ntsb_aviation_events",
    "aircraft": "fed_ntsb_aviation_aircraft",
}


def _register(conn, sid: str, table: str, rows: int, desc: str, unit: str) -> None:
    cfg = {
        "source_id": sid,
        "name": f"NTSB Aviation Accident Database -- {desc}",
        "publisher": "National Transportation Safety Board",
        "url": "https://www.ntsb.gov/Pages/AviationQueryV2.aspx",
        "description": f"NTSB's aviation accident/incident bulk database (avall.mdb), {desc} table. "
                       f"Current rolling window (older years ship as separate archived zips, not loaded here).",
        "jurisdiction": "federal", "category": "Transportation", "subcategory": "Aviation Safety",
        "unit_of_observation": unit,
        "geographic_scope": "US + some international (NTSB jurisdiction)", "access_method": "bulk_download",
        "format": "mdb (MS Access) -> extracted table", "auth": {"type": "none"}, "cost": "free",
        "update_cadence": "rolling, updated by NTSB periodically", "volume": f"{rows:,} rows",
        "license_terms": "U.S. Government work, public",
        "join_keys": "ev_id (events<->aircraft), ntsb_no",
        "accountability_relevance": "Aviation accidents/incidents -- who operated, what failed, who was hurt.",
        "priority_tier": "2", "landing_table": table.upper(),
        "notes": "Loaded by scripts/ntsb_aviation_load.py (LLM-free, mdb via pyodbc, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def _load_mdb_tables(mdb_path: Path) -> dict[str, pd.DataFrame]:
    import pyodbc
    conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                fr"DBQ={mdb_path};")
    cn = pyodbc.connect(conn_str)
    try:
        out = {}
        for t in TABLES:
            out[t] = pd.read_sql(f"SELECT * FROM [{t}]", cn)
        return out
    finally:
        cn.close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for NTSB aviation accident database")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== NTSB Aviation Accident Database ===", flush=True)
    r = requests.get(URL, timeout=180, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    content = r.content
    sha = hashlib.sha256(content).hexdigest()
    print(f"downloaded avall.zip: {len(content):,} bytes", flush=True)

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        zipfile.ZipFile(io.BytesIO(content)).extractall(tdp)
        mdb_path = tdp / "avall.mdb"
        if not mdb_path.exists():
            cands = list(tdp.glob("*.mdb"))
            if not cands:
                print("no .mdb file found in zip -- BLOCKED", flush=True)
                return 1
            mdb_path = cands[0]
        dfs = _load_mdb_tables(mdb_path)

        for t, df in dfs.items():
            print(f"  {t}: {len(df):,} rows, {len(df.columns)} cols", flush=True)

        if not args.run:
            ev = dfs["events"]
            print("\nSAMPLE events (first 3, key cols):")
            cols = [c for c in ["ev_id", "ntsb_no", "ev_date", "ev_city", "ev_state", "inj_tot_f"] if c in ev.columns]
            print(ev[cols].head(3).to_string() if cols else ev.head(3).to_string())
            print("\nPREVIEW only -- add --run to land.")
            return 0

        started = ingest._utcnow()
        conn = snow.connect()
        try:
            snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
            from snowflake.connector.pandas_tools import write_pandas
            for t, sid in TABLES.items():
                df = dfs[t]
                table = sid.upper()
                run_id = str(uuid.uuid4())
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
                ingest._log_run(conn, sid, run_id, status, len(df), None, sha, URL, started, ended,
                                f"NTSB avall.mdb / {t} table; {len(df):,} rows; density {dens.get('populated_fraction')}")
                unit = "one row = one accident/incident event" if t == "events" else "one row = one aircraft involved in an event"
                _register(conn, sid, table, len(df), t, unit)
                print(f"LOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{table} "
                      f"(status={status}); registered INCLUDE=Y", flush=True)

            n_ev = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_NTSB_AVIATION_EVENTS"')
            dk_ev = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT "EV_ID") FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_NTSB_AVIATION_EVENTS"')
            n_ac = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_NTSB_AVIATION_AIRCRAFT"')
            join_ok = snow.fetch_scalar(conn,
                f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."FED_NTSB_AVIATION_AIRCRAFT" a '
                f'JOIN "{settings.raw_database}"."{settings.raw_schema}"."FED_NTSB_AVIATION_EVENTS" e ON a."EV_ID" = e."EV_ID"')
            print(f"verify: events {n_ev:,} rows (DISTINCT EV_ID={dk_ev:,}); aircraft {n_ac:,} rows; "
                  f"aircraft->events join matches {join_ok:,}", flush=True)
        finally:
            conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
