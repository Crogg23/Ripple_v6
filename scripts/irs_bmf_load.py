#!/usr/bin/env python3
"""Loader for the IRS Exempt Organizations Business Master File (EO BMF) -- the
full roster of ~1.5M US tax-exempt organizations, keyed on a 9-digit EIN. Lands the
IRS side of the EIN bridge (discovery sweep #50: SEC EDGAR <-> IRS on EIN) and
complements the already-landed IRS automatic-revocation list.

Source: 4 regional CSV extracts the IRS publishes (eo1-4.csv); together they cover
all US states + territories. One row = one exempt org (EIN, NAME, NTEE, subsection,
asset/income/revenue codes, status, ...). Snapshot-replace -> idempotent.

    python3 scripts/irs_bmf_load.py          # preview (fetch headers, no write)
    python3 scripts/irs_bmf_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
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
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

SID = "fed_irs_bmf"
TABLE = SID.upper()
URLS = [f"https://www.irs.gov/pub/irs-soi/eo{n}.csv" for n in (1, 2, 3, 4)]
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}


def _fetch_concat() -> tuple[pd.DataFrame, str]:
    frames, hasher = [], hashlib.sha256()
    for u in URLS:
        r = requests.get(u, headers=UA, timeout=300)
        r.raise_for_status()
        hasher.update(r.content)
        frames.append(pd.read_csv(io.BytesIO(r.content), dtype=str,
                                  keep_default_na=False, low_memory=False, encoding_errors="replace"))
        print(f"  {u.split('/')[-1]}: {len(frames[-1]):,} rows", flush=True)
    df = pd.concat(frames, ignore_index=True)
    return df, hasher.hexdigest()


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID, "name": "IRS Exempt Organizations Business Master File (EO BMF)",
        "publisher": "Internal Revenue Service (IRS)",
        "url": "https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf",
        "description": "Full roster of US tax-exempt organizations -- EIN, name, NTEE code, "
                       "subsection, foundation/status codes, asset/income/revenue. The IRS side of "
                       "the EIN bridge (#50). Concatenated from the 4 regional eo1-4.csv extracts.",
        "jurisdiction": "federal", "category": "Corporate / Nonprofit", "subcategory": "Tax-exempt orgs",
        "unit_of_observation": "one row = one exempt organization (EIN)",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "monthly",
        "volume": f"{rows:,} rows", "license_terms": "Public domain (US Gov work)",
        "join_keys": "EIN, NTEE, FIPS (via STATE/ZIP)",
        "accountability_relevance": "The exempt-org backbone -- bridges nonprofits to SEC filers, "
                                    "contractors, and grant recipients on EIN. Issue #50.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/irs_bmf_load.py (4 regional EO BMF extracts, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Loader for the IRS EO BMF")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== IRS EO BMF ===", flush=True)
    df, sha = _fetch_concat()
    df.columns = [str(c).strip() for c in df.columns]
    print(f"total: {len(df):,} rows x {len(df.columns)} cols", flush=True)
    if not args.run:
        print("cols:", ", ".join(df.columns[:12]), "...")
        print("\nPREVIEW only -- add --run to land.")
        return 0

    started = ingest._utcnow(); run_id = str(uuid.uuid4())
    conn = snow.connect()
    try:
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
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, URLS[0], started, ended,
                        f"IRS EO BMF; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        eins = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT EIN) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"LOADED {n:,} rows -> {TABLE} (status={status}); {eins:,} distinct EINs", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
