"""Bulk-load SEC DERA datasets and EDGAR bulk APIs.

Known-manifest loader: SEC data.json is thin (mostly metadata), so this targets
the actual bulk data sources directly:
  - DERA Financial Statement Data Sets (quarterly ZIPs with sub.txt/num.txt)
  - EDGAR Submissions bulk ZIP (company CIK/EIN/SIC roster)
  - DERA Form D, 13F, Insider Transactions

All keyed on CIK/EIN -- the core SEC<->corporate bridge.

SEC REQUIRES a descriptive User-Agent or returns 403.

    python scripts/sec_bulk_discover_load.py              # preview
    python scripts/sec_bulk_discover_load.py --run        # load all
    python scripts/sec_bulk_discover_load.py --run --limit 5
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
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

TABLE_PREFIX = "FED_SEC"
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

ENTITY_KEYS = {
    "CIK", "CUSIP", "EIN", "FILER_CIK", "COMPANY_CIK", "TICKER",
    "REGISTRANT_CIK", "OWNER_CIK", "ISSUER_CIK", "ACCESSION_NUMBER",
    "ADSH", "CENTRAL_INDEX_KEY", "SIC",
}

# ---------------------------------------------------------------------------
# DERA quarterly datasets: Financial Statements sub.txt (the submissions panel)
# URL pattern: https://www.sec.gov/files/dera/data/financial-statement-data-sets/{YYYY}q{N}.zip
# Each ZIP contains: sub.txt, num.txt, tag.txt, pre.txt (tab-separated)
# We load sub.txt (the submission metadata) which has CIK+EIN+SIC per filing.
# ---------------------------------------------------------------------------
DERA_QUARTERS = [
    "2026q1", "2025q4", "2025q3", "2025q2", "2025q1",
    "2024q4", "2024q3", "2024q2", "2024q1",
]

# Other DERA datasets at known URLs
SEC_MANIFEST = [
    {
        "name": "EDGAR_COMPANY_TICKERS",
        "url": "https://www.sec.gov/files/company_tickers.json",
        "kind": "json",
        "description": "All SEC-registered entities: CIK, ticker, company name",
    },
    {
        "name": "EDGAR_COMPANY_TICKERS_EXCHANGE",
        "url": "https://www.sec.gov/files/company_tickers_exchange.json",
        "kind": "json",
        "description": "CIK + ticker + exchange mapping",
    },
    {
        "name": "DERA_FORM_D_2026Q1",
        "url": "https://www.sec.gov/files/structureddata/data/form-d-data-sets/2026q1_d.zip",
        "kind": "zip",
        "description": "Regulation D private placements Q1 2026 (issuer CIK/EIN)",
    },
    {
        "name": "DERA_FORM_D_2025Q4",
        "url": "https://www.sec.gov/files/structureddata/data/form-d-data-sets/2025q4_d.zip",
        "kind": "zip",
        "description": "Regulation D private placements Q4 2025 (issuer CIK/EIN)",
    },
    {
        "name": "DERA_13F_SEP_NOV_2025",
        "url": "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/01sep2025-30nov2025_form13f.zip",
        "kind": "zip",
        "description": "Form 13F institutional holdings Sep-Nov 2025 (manager CIK, CUSIP)",
    },
    {
        "name": "DERA_13F_JUN_AUG_2025",
        "url": "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/01jun2025-31aug2025_form13f.zip",
        "kind": "zip",
        "description": "Form 13F institutional holdings Jun-Aug 2025 (manager CIK, CUSIP)",
    },
]


def _load_dera_quarter(conn, quarter: str, max_rows: int) -> int:
    """Download one DERA Financial Statement quarter ZIP and load sub.txt."""
    url = f"https://www.sec.gov/files/dera/data/financial-statement-data-sets/{quarter}.zip"
    tbl = f"FED_SEC_DERA_SUB_{quarter.upper()}"
    print(f"  Fetching {quarter}...")
    try:
        resp = requests.get(url, timeout=300, headers=USER_AGENT)
        resp.raise_for_status()
    except Exception as e:
        print(f"    FAILED download {quarter}: {str(e)[:80]}")
        return 0

    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            # Load sub.txt (tab-separated submission metadata)
            if "sub.txt" not in zf.namelist():
                print(f"    No sub.txt in {quarter}.zip")
                return 0
            with zf.open("sub.txt") as f:
                content = f.read()
        # sub.txt is tab-delimited
        df = pd.read_csv(io.BytesIO(content), sep="\t", dtype=str,
                         nrows=max_rows + 1, low_memory=False, encoding_errors="replace")
        if len(df) > max_rows:
            raise RuntimeError(
                f"{quarter}: source has more than max_rows={max_rows:,} rows -- "
                f"refusing to silently truncate. Pass a higher max_rows explicitly.")
        if df.empty:
            return 0
        df.columns = [bulk.sf_col(c) for c in df.columns]
        # Add provenance and load
        import datetime as dt, hashlib, uuid
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
        # Quality gate (audit 2026-08-05/06 finding: none here at all -- this DERA
        # quarter loader writes directly instead of going through
        # bulk._load_bytes/fast_load, so it never got their internal density gate).
        passed, report = bulk.assess_bulk_load(conn, tbl)
        if not passed:
            raise RuntimeError(f"QUALITY GATE FAILED for {tbl}: {report}")
        print(f"    -> {tbl}: {len(df):,} rows")
        return len(df)
    except Exception as e:
        print(f"    FAILED load {quarter}: {str(e)[:100]}")
        return 0


def _load_json_dataset(conn, entry: dict, max_rows: int) -> int:
    """Load a SEC JSON dataset (company tickers etc.)."""
    tbl = f"{TABLE_PREFIX}_{entry['name']}"
    print(f"  Loading {tbl}...")
    try:
        resp = requests.get(entry["url"], timeout=120, headers=USER_AGENT)
        resp.raise_for_status()
        data = resp.json()
        # Handle different JSON structures
        if isinstance(data, dict):
            # company_tickers.json: {"0": {cik, ticker, title}, ...}
            records = list(data.values()) if all(isinstance(v, dict) for v in data.values()) else [data]
        elif isinstance(data, list):
            records = data
        else:
            print(f"    Unexpected JSON structure for {entry['name']}")
            return 0
        df = pd.DataFrame(records[:max_rows]).astype(str)
        if df.empty:
            return 0
        n = bulk._load_bytes(conn, df.to_csv(index=False).encode("utf-8"), tbl, max_rows=max_rows)
        print(f"    -> {tbl}: {n:,} rows")
        return n
    except Exception as e:
        print(f"    FAILED {entry['name']}: {str(e)[:100]}")
        return 0


def _load_zip_dataset(conn, entry: dict, max_rows: int) -> int:
    """Load a SEC ZIP dataset (Form D, 13F)."""
    tbl_prefix = f"{TABLE_PREFIX}_{entry['name']}"
    print(f"  Loading {tbl_prefix}...")
    try:
        results = bulk.load_zip_csvs(
            conn, entry["url"], tbl_prefix, ENTITY_KEYS,
            user_agent=USER_AGENT, max_rows=max_rows, timeout=600,
        )
        total = sum(r[1] for r in results) if results else 0
        if not results:
            # Try loading the whole ZIP regardless of key matching
            resp = requests.get(entry["url"], timeout=600, headers=USER_AGENT)
            resp.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
                for name in zf.namelist():
                    if not name.lower().endswith(('.csv', '.txt', '.tsv')):
                        continue
                    tbl = bulk.table_name(tbl_prefix, Path(name).stem)
                    with zf.open(name) as f:
                        content = f.read()
                    n = bulk._load_bytes(conn, content, tbl, max_rows=max_rows)
                    if n > 0:
                        total += n
                        print(f"    -> {tbl}: {n:,} rows")
        return total
    except Exception as e:
        print(f"    FAILED {entry['name']}: {str(e)[:100]}")
        return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="SEC DERA + EDGAR bulk loader")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--max-rows", type=int, default=5_000_000)
    args = ap.parse_args()

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING")

    # Build task list
    all_tasks = []

    # DERA quarterly submissions
    for q in DERA_QUARTERS:
        tbl = f"FED_SEC_DERA_SUB_{q.upper()}"
        if tbl in loaded:
            print(f"  SKIP {tbl} (already loaded)")
        else:
            all_tasks.append({"kind": "dera_quarter", "quarter": q, "table": tbl})

    # Other SEC datasets
    for entry in SEC_MANIFEST:
        tbl = f"{TABLE_PREFIX}_{entry['name']}"
        # Check if any table with this prefix exists
        if tbl in loaded or any(t.startswith(tbl) for t in loaded):
            print(f"  SKIP {entry['name']} (already loaded)")
        else:
            all_tasks.append({"kind": entry["kind"], "entry": entry, "table": tbl})

    to_load = all_tasks[:args.limit]
    print(f"\n{len(to_load)} SEC datasets to load")

    if not args.run:
        print("\n(preview only -- add --run to load)")
        for i, t in enumerate(to_load, 1):
            if t["kind"] == "dera_quarter":
                print(f"  {i:2d}. {t['table']:50s} (DERA submissions {t['quarter']})")
            else:
                desc = t["entry"].get("description", "")[:50]
                print(f"  {i:2d}. {t['table']:50s} ({desc})")
        return 0

    # Load
    total_rows = 0
    ok = 0
    failed = []
    for t in to_load:
        try:
            if t["kind"] == "dera_quarter":
                n = _load_dera_quarter(conn, t["quarter"], args.max_rows)
            elif t["kind"] == "json":
                n = _load_json_dataset(conn, t["entry"], args.max_rows)
            elif t["kind"] == "zip":
                n = _load_zip_dataset(conn, t["entry"], args.max_rows)
            else:
                n = 0
            if n > 0:
                ok += 1
                total_rows += n
            else:
                failed.append(t["table"])
        except Exception as e:
            print(f"  FAILED: {str(e)[:120]}")
            failed.append(t["table"])

    print(f"\nDone: {ok}/{len(to_load)} datasets loaded, {total_rows:,} total rows")
    conn.close()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
