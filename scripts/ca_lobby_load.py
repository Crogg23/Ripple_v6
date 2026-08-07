#!/usr/bin/env python3
"""Deterministic loader for California CAL-ACCESS lobbying disclosure bulk data.

CAL-ACCESS publishes its entire campaign-finance + lobbying database as one big
ZIP of pipe-... actually tab-separated .TSV files (dbwebexport.zip, ~1.5GB,
130 tables total). This loader pulls only the lobbying-family tables (12 distinct
tables; the export ships each as 1-3 byte-identical numbered duplicates -- we load
one copy of each) rather than the full campaign-finance database, which is out of
scope for this source.

    python scripts/ca_lobby_load.py          # preview (extract + sample, no write)
    python scripts/ca_lobby_load.py --run     # land it
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

URL = "https://campaignfinance.cdn.sos.ca.gov/dbwebexport.zip"
ZIP_PATH = _LIB / "raw_downloads" / "ca_dbwebexport.zip"
EXTRACT_DIR = _LIB / "raw_downloads" / "ca_lobby"

# tsv filename inside the zip (picking one copy of each duplicated numbered set) ->
# (source_id, table, description)
FILES = {
    "CVR_LOBBY_DISCLOSURE_CD.TSV": ("ca_lobby_cover", "CA_LOBBY_COVER", "Lobbying disclosure cover page (Form 615/625/635/645)"),
    "CVR2_LOBBY_DISCLOSURE_CD.TSV": ("ca_lobby_cover2", "CA_LOBBY_COVER2", "Lobbying disclosure cover page 2 (additional filer info)"),
    "LOBBYING_CHG_LOG_CD.TSV": ("ca_lobby_chg_log", "CA_LOBBY_CHG_LOG", "Lobbying registration change log"),
    "LOBBY_AMENDMENTS_CD.TSV": ("ca_lobby_amendments", "CA_LOBBY_AMENDMENTS", "Lobbying amendments"),
    "LOBBYIST_CONTRIBUTIONS1_CD.TSV": ("ca_lobby_contributions", "CA_LOBBY_CONTRIBUTIONS", "Lobbyist campaign contributions"),
    "LOBBYIST_EMPLOYER1_CD.TSV": ("ca_lobby_employer", "CA_LOBBY_EMPLOYER", "Lobbyist employers"),
    "LOBBYIST_EMPLOYER_FIRMS1_CD.TSV": ("ca_lobby_employer_firms", "CA_LOBBY_EMPLOYER_FIRMS", "Lobbyist employer <-> firm relationships"),
    "LOBBYIST_EMP_LOBBYIST1_CD.TSV": ("ca_lobby_emp_lobbyist", "CA_LOBBY_EMP_LOBBYIST", "Lobbyist employer <-> individual lobbyist relationships"),
    "LOBBYIST_FIRM1_CD.TSV": ("ca_lobby_firm", "CA_LOBBY_FIRM", "Lobbying firms"),
    "LOBBYIST_FIRM_EMPLOYER1_CD.TSV": ("ca_lobby_firm_employer", "CA_LOBBY_FIRM_EMPLOYER", "Lobbying firm <-> employer relationships"),
    "LOBBYIST_FIRM_LOBBYIST1_CD.TSV": ("ca_lobby_firm_lobbyist", "CA_LOBBY_FIRM_LOBBYIST", "Lobbying firm <-> individual lobbyist relationships"),
}
# LOBBYIST_EMPLOYER_HISTORY_CD.TSV and LOBBYIST_FIRM_HISTORY_CD.TSV are 0 bytes
# in this snapshot -- excluded, not a bug.


def _register(conn, sid: str, table: str, desc: str, rows: int) -> None:
    cfg = {
        "source_id": sid,
        "name": f"California CAL-ACCESS Lobbying — {desc}",
        "publisher": "California Secretary of State",
        "url": "https://www.sos.ca.gov/campaign-lobbying/cal-access-resources/raw-data-campaign-finance-and-lobbying-activity",
        "description": f"{desc}. Part of the CAL-ACCESS bulk database export (dbwebexport.zip), "
                       "lobbying-family tables only (campaign finance tables in the same export are out of scope for this source).",
        "jurisdiction": "state:CA", "category": "Politics", "subcategory": "Lobbying",
        "unit_of_observation": f"one row = one {desc.lower()} record",
        "geographic_scope": "California", "access_method": "bulk_download", "format": "tsv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "periodic",
        "volume": f"{rows:,} rows", "license_terms": "Public record (CA SOS)",
        "join_keys": "FILER_ID, FIRM_ID, EMPLOYER_ID",
        "accountability_relevance": "California state lobbyist/firm/employer registration and activity disclosure.",
        "priority_tier": "2", "landing_table": table,
        "notes": "Loaded by scripts/ca_lobby_load.py (LLM-free, lobbying subset of CAL-ACCESS dbwebexport.zip, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for CA CAL-ACCESS lobbying bulk TSVs")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== California CAL-ACCESS Lobbying ===", flush=True)
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not ZIP_PATH.exists():
        with requests.get(URL, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(ZIP_PATH, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)

    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH) as z:
        inner = {n.split("/")[-1]: n for n in z.namelist()}
        for fname in FILES:
            out = EXTRACT_DIR / fname
            if not out.exists():
                out.write_bytes(z.read(inner[fname]))

    dfs = {}
    for fname, (sid, table, desc) in FILES.items():
        p = EXTRACT_DIR / fname
        df = pd.read_csv(p, sep="\t", dtype=str, keep_default_na=False, encoding="latin-1", on_bad_lines="warn")
        dfs[fname] = df
        print(f"  {fname:32} {len(df):>8,} rows  -> {table}", flush=True)

    if not args.run:
        cvr = dfs["CVR_LOBBY_DISCLOSURE_CD.TSV"]
        print("\nSAMPLE (CVR_LOBBY_DISCLOSURE_CD.TSV, first 3 rows, key cols):")
        for _, row in cvr.head(3).iterrows():
            print(f"  FILER_ID={row.get('FILER_ID','')}  FILER_NAML={row.get('FILER_NAML','')}  RPT_DATE={row.get('RPT_DATE','')}")
        print(f"\ndistinct FILER_ID in cover: {cvr['FILER_ID'].nunique():,} of {len(cvr):,} rows")
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
                            f"CA CAL-ACCESS {desc}; {len(df):,} rows; density {dens.get('populated_fraction')}")
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
