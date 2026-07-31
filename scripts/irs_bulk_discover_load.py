"""Targeted bulk-load of IRS datasets NOT already covered by irs_bmf_load.py.

Known-manifest loader: IRS publishes bulk files at fixed URLs (no DCAT catalog).
Targets: automatic revocations, Pub78 eligible donees, 990 e-filer index, and
SOI exempt org statistics. All EIN-keyed.

    python scripts/irs_bulk_discover_load.py              # preview
    python scripts/irs_bulk_discover_load.py --run        # load all
    python scripts/irs_bulk_discover_load.py --run --limit 2
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

TABLE_PREFIX = "FED_IRS"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

ENTITY_KEYS = {"EIN", "OBJECT_ID", "TAXPAYER_NAME"}


def _load_pipe_zip(conn, url: str, tbl: str, col_names: list[str], max_rows: int) -> int:
    """Load a pipe-delimited txt file inside a ZIP (IRS format: no header, | separator)."""
    import zipfile, hashlib, datetime as dt, uuid
    resp = requests.get(url, timeout=300, headers=USER_AGENT)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        txt_files = [n for n in zf.namelist() if n.lower().endswith('.txt')]
        if not txt_files:
            return 0
        with zf.open(txt_files[0]) as f:
            content = f.read()
    df = pd.read_csv(io.BytesIO(content), sep="|", dtype=str, header=None,
                     names=col_names, nrows=max_rows + 1, on_bad_lines="skip",
                     encoding_errors="replace")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df.columns = [bulk.sf_col(c) for c in df.columns]
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
        raise RuntimeError(f"write_pandas failed for {tbl}")
    print(f"    -> {tbl}: {len(df):,} rows")
    return len(df)


def _load_revocations(conn, max_rows: int) -> int:
    """IRS automatic revocations -- orgs that lost exempt status. Pipe-delimited, no header."""
    url = "https://apps.irs.gov/pub/epostcard/data-download-revocation.zip"
    tbl = "FED_IRS_AUTO_REVOCATIONS"
    cols = ["EIN", "LEGAL_NAME", "DOING_BUSINESS_AS", "ORGANIZATION_ADDRESS",
            "CITY", "STATE", "ZIP_CODE", "COUNTRY", "EXEMPTION_TYPE",
            "REVOCATION_DATE", "REVOCATION_POSTING_DATE", "REINSTATEMENT_DATE"]
    print(f"  Loading {tbl}...")
    return _load_pipe_zip(conn, url, tbl, cols, max_rows)


def _load_pub78(conn, max_rows: int) -> int:
    """IRS Publication 78 -- eligible donee organizations. Pipe-delimited, no header."""
    url = "https://apps.irs.gov/pub/epostcard/data-download-pub78.zip"
    tbl = "FED_IRS_PUB78_ELIGIBLE_DONEES"
    cols = ["EIN", "LEGAL_NAME", "CITY", "STATE", "COUNTRY", "DEDUCTIBILITY_STATUS"]
    print(f"  Loading {tbl}...")
    return _load_pipe_zip(conn, url, tbl, cols, max_rows)


def _load_990_index(conn, max_rows: int) -> int:
    """IRS 990 e-filer index (CSV from IRS TEOS site)."""
    tbl = "FED_IRS_990_EFILER_INDEX"
    total = 0
    for year in (2023, 2022):
        url = f"https://apps.irs.gov/pub/epostcard/990/xml/{year}/index_{year}.csv"
        print(f"  Loading 990 index {year}...")
        try:
            n = bulk.fast_load(conn, url, f"{tbl}_{year}",
                              user_agent=USER_AGENT, max_rows=max_rows)
            total += n
            print(f"    -> {tbl}_{year}: {n:,} rows")
        except Exception as e:
            print(f"    FAILED {year}: {str(e)[:100]}")
    return total


def _load_soi_exempt(conn, max_rows: int) -> int:
    """IRS SOI Exempt Organizations -- charitable org statistics."""
    tbl = "FED_IRS_SOI_CHARITIES"
    # SOI publishes several CSV extracts; try the main ones
    urls = [
        "https://www.irs.gov/pub/irs-soi/eo_xx.csv",
        "https://www.irs.gov/pub/irs-soi/19eofinextractEZ.csv",
    ]
    print(f"  Loading {tbl}...")
    for url in urls:
        try:
            n = bulk.fast_load(conn, url, tbl, user_agent=USER_AGENT, max_rows=max_rows)
            if n > 0:
                return n
        except Exception:
            continue
    print(f"    FAILED: no working SOI URL found")
    return 0


# Manifest for preview/selection
IRS_MANIFEST = [
    {"name": "AUTO_REVOCATIONS", "fn": _load_revocations,
     "description": "Organizations that lost tax-exempt status (EIN-keyed)"},
    {"name": "PUB78_ELIGIBLE_DONEES", "fn": _load_pub78,
     "description": "Eligible donee organizations per IRS Publication 78 (EIN-keyed)"},
    {"name": "990_EFILER_INDEX", "fn": _load_990_index,
     "description": "990/990-EZ/990-PF e-filer index from AWS (EIN + ObjectId)"},
    {"name": "SOI_EXEMPT_ORGS", "fn": _load_soi_exempt,
     "description": "SOI Exempt Organizations statistics (EIN-keyed)"},
]


def main() -> int:
    ap = argparse.ArgumentParser(description="IRS targeted bulk loader")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--limit", type=int, default=len(IRS_MANIFEST))
    ap.add_argument("--max-rows", type=int, default=500000)
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING")

    # Filter to not-yet-loaded
    to_load = []
    for entry in IRS_MANIFEST[:args.limit]:
        tbl_prefix = f"FED_IRS_{entry['name']}"
        if any(t.startswith(tbl_prefix) for t in loaded):
            print(f"  SKIP {entry['name']} (already loaded)")
        else:
            to_load.append(entry)

    print(f"\n{len(to_load)} IRS datasets to load")

    if not args.run:
        print("\n(preview only -- add --run to load)")
        for i, e in enumerate(to_load, 1):
            print(f"  {i}. {e['name']:30s} — {e['description']}")
        return 0

    # Load sequentially (IRS sources are few and some need custom handling)
    total_rows = 0
    ok = 0
    for entry in to_load:
        try:
            n = entry["fn"](conn, args.max_rows)
            if n > 0:
                ok += 1
                total_rows += n
        except Exception as e:
            print(f"  FAILED {entry['name']}: {str(e)[:120]}")

    print(f"\nDone: {ok}/{len(to_load)} datasets loaded, {total_rows:,} total rows")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
