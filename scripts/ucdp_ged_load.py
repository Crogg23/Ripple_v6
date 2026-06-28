#!/usr/bin/env python3
"""Deterministic loader for the UCDP Georeferenced Event Dataset (GED) Global.

The keyless, CC-BY-4.0 conflict backbone: every geo-coded, dated event of
organized violence worldwide since 1989, with best/low/high fatality estimates
split by side. Onboardable proxy for issues #1 (Ukraine), #2 (Gaza), #3 (Sudan),
#5/#7/#8 (Myanmar/Sahel), #39 (extremism), #43 (Ethiopia/Horn). Chosen OVER ACLED
because ACLED forbids redistributing raw rows; UCDP GED does not.

One bulk ZIP -> one CSV -> snapshot-replace (idempotent).

    python scripts/ucdp_ged_load.py          # preview
    python scripts/ucdp_ged_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
import io
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

SID = "intl_ucdp_ged"
TABLE = SID.upper()
# UCDP GED Global v25.1 (most recent annual; bump the stem when v26 lands)
URL = "https://ucdp.uu.se/downloads/ged/ged251-csv.zip"
URL_FALLBACKS = [
    "https://ucdp.uu.se/downloads/ged/ged261-csv.zip",
    "https://ucdp.uu.se/downloads/ged/ged241-csv.zip",
]


def _fetch_zip_csv():
    """Try the primary + fallback stems; return (df, url, version)."""
    last = None
    for url in [URL] + URL_FALLBACKS:
        try:
            r = requests.get(url, timeout=300)
            if r.status_code != 200:
                last = f"{url} -> HTTP {r.status_code}"
                continue
            zf = zipfile.ZipFile(io.BytesIO(r.content))
            csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
            with zf.open(csv_name) as fh:
                df = pd.read_csv(fh, dtype=str, keep_default_na=False, low_memory=False)
            ver = "".join(c for c in url.split("/")[-1] if c.isdigit())
            return df, url, ver
        except Exception as ex:  # noqa: BLE001
            last = f"{url} -> {str(ex)[:80]}"
            continue
    raise SystemExit(f"All UCDP GED URLs failed. Last: {last}")


def _register(conn, rows: int, url: str, ver: str) -> None:
    cfg = {
        "source_id": SID,
        "name": "UCDP Georeferenced Event Dataset (GED) Global",
        "publisher": "Uppsala Conflict Data Program, Uppsala University",
        "url": "https://ucdp.uu.se/downloads/",
        "description": "Geo-coded, dated events of organized violence worldwide (1989-present) with "
                       "best/low/high fatality estimates by side. Keyless, openly licensed conflict "
                       f"backbone. GED Global v{ver}.",
        "jurisdiction": "international", "category": "Conflict", "subcategory": "Political Violence",
        "unit_of_observation": "one row = one geo-coded event of organized violence",
        "geographic_scope": "Global", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "annual (+ monthly candidate)",
        "volume": f"{rows:,} rows", "license_terms": "CC BY 4.0 (cite UCDP)",
        "join_keys": "LATLON, COUNTRY, NAME",
        "accountability_relevance": "Canonical open conflict-event/fatality data; the redistributable "
                                    "proxy for war casualties across issues #1/#2/#3/#5/#7/#8/#39/#43.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/ucdp_ged_load.py (LLM-free, bulk ZIP-CSV, snapshot-replace). "
                 "Prefer over ACLED for public output (ACLED forbids raw redistribution).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for UCDP GED Global")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== UCDP GED Global ===", flush=True)
    df, url, ver = _fetch_zip_csv()
    print(f"v{ver} from {url}: {len(df):,} events, {len(df.columns)} cols", flush=True)

    if not args.run:
        cols = list(df.columns)
        print("cols:", ", ".join(cols[:18]), "...")
        if "country" in df.columns and "year" in df.columns:
            ukr = df[df["country"] == "Ukraine"]
            print(f"Ukraine events: {len(ukr):,}")
        dens = ingest.assess_density(df)
        print(f"density: {dens.get('populated_fraction')}, empty={dens.get('empty')}")
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    sha = hashlib.sha256(pd.util.hash_pandas_object(df, index=False).values.tobytes()).hexdigest()
    conn = snow.connect()
    try:
        from snowflake.connector.pandas_tools import write_pandas
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        out = ingest._stringify(df)
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        out.columns = [ingest._sf_col(c) for c in out.columns]
        ok, _c, _n, _ = write_pandas(conn, out, table_name=TABLE,
                                     database=settings.raw_database, schema=settings.raw_schema,
                                     auto_create_table=True, overwrite=True, quote_identifiers=False)
        if not ok:
            raise RuntimeError("write_pandas failed")
        ended = ingest._utcnow()
        dens = ingest.assess_density(df)
        status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, url, started, ended,
                        f"UCDP GED Global v{ver}; {len(df):,} events; density {dens.get('populated_fraction')}")
        _register(conn, len(df), url, ver)
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y; verify count={n:,}", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
