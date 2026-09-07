"""Land the HHS/HRSA Provider Relief Fund payment file.

WHAT THE FILE IS
  One flat CSV, four columns: Provider Name, State, City, Payment.
  It is the public list of providers who attested to accepting a Provider
  Relief Fund (CARES Act / PPPHCEA / CRRSA / ARP Rural is a separate appropriation, not shown here) payment. HRSA does not
  host the file itself; hrsa.gov/provider-relief/payments-and-data points at
  the CDC open-data portal, dataset kh8y-3es6 ("HHS Provider Relief Fund").
  Measured 2026-09-07: 419,846 rows, $135.06B, last modified 2025-03-28.

  No EIN, no NPI, no CCN. The name is the payee, which for a nursing home is
  usually the operating LLC, not the sign on the building. Name + city +
  state is the only bridge, and it is done in dbt, not here.

  hrsa.gov itself answers 403 to a plain fetch (checked 2026-09-07), so the
  URL below is the CDC portal's CSV export and the HRSA page is documentation.

HOW IT LANDS
  LIBRARY_RAW.LANDING.FED_HRSA_PROVIDER_RELIEF_FUND, every column VARCHAR,
  plus _INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256, same stamps as
  senate_lda_load.py. CREATE TABLE IF NOT EXISTS then append; never overwrite,
  never drop. If the table already holds rows the loader stops and says so,
  because a second append would double every dollar. Staging reads the newest
  _SOURCE_RUN_ID only, so a deliberate reload with --append is still safe
  downstream.

    python scripts/hrsa_prf_load.py            # dry run: download, profile, load nothing
    python scripts/hrsa_prf_load.py --run      # land it
    python scripts/hrsa_prf_load.py --run --append   # land on top of existing rows
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import sys
import uuid
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

SOURCE_ID = "fed_hrsa_provider_relief_fund"
TABLE = "FED_HRSA_PROVIDER_RELIEF_FUND"
DOC_URL = "https://www.hrsa.gov/provider-relief/payments-and-data"
DATA_URL = "https://data.cdc.gov/api/views/kh8y-3es6/rows.csv?accessType=DOWNLOAD"
USER_AGENT = "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"


def download() -> bytes:
    r = requests.get(DATA_URL, headers={"User-Agent": USER_AGENT}, timeout=300)
    r.raise_for_status()
    return r.content


def to_frame(content: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(content), dtype=str, low_memory=False,
                     encoding_errors="replace")
    df.columns = [bulk.sf_col(c) for c in df.columns]
    return df


def profile(df: pd.DataFrame) -> dict:
    amt = pd.to_numeric(df["PAYMENT"].str.replace(r"[$,]", "", regex=True),
                        errors="coerce")
    return {
        "rows": len(df),
        "columns": df.columns.tolist(),
        "dollars": float(amt.sum()),
        "unparsed_payments": int(amt.isna().sum()),
        "states": int(df["STATE"].nunique()),
        "exact_dupe_rows": int(df.duplicated().sum()),
        "name_city_state_dupes": int(df.duplicated(["PROVIDER_NAME", "STATE", "CITY"]).sum()),
    }


def existing_rows(conn) -> int | None:
    try:
        return conn.cursor().execute(
            f'select count(*) from {bulk.LANDING_FQS}."{TABLE}"').fetchone()[0]
    except Exception:
        return None  # table does not exist


def land(conn, df: pd.DataFrame, sha: str, run_id: str) -> int:
    from snowflake.connector.pandas_tools import write_pandas
    df = df.copy()
    df[bulk.META_INGESTED_AT] = pd.Timestamp.utcnow().tz_localize(None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    cols_sql = ", ".join(f'"{c}" VARCHAR' for c in df.columns)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{TABLE}" ({cols_sql})')
    cur.close()
    df = df.astype(str).replace({"None": None, "nan": None, "NaT": None})
    ok, _c, nrows, _ = write_pandas(conn, df, TABLE, database=bulk.LANDING_DB,
                                    schema=bulk.LANDING_SCHEMA,
                                    quote_identifiers=False,
                                    auto_create_table=False)
    if not ok:
        raise RuntimeError("write_pandas reported failure")
    return nrows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land it; default is dry run")
    ap.add_argument("--append", action="store_true",
                    help="allow landing on top of rows already in the table")
    args = ap.parse_args()

    print(f"source page: {DOC_URL}")
    print(f"file:        {DATA_URL}")
    content = download()
    sha = hashlib.sha256(content).hexdigest()
    df = to_frame(content)
    p = profile(df)
    print(f"downloaded {len(content):,} bytes, sha256 {sha[:12]}")
    print(f"rows {p['rows']:,}  dollars {p['dollars']:,.0f}  states {p['states']}")
    print(f"columns {p['columns']}")
    print(f"unparsed payments {p['unparsed_payments']}  exact dupe rows {p['exact_dupe_rows']}  "
          f"name+city+state dupes {p['name_city_state_dupes']}")

    if not args.run:
        print("\n(dry run -- add --run to land)")
        return

    conn = snow.connect()
    have = existing_rows(conn)
    if have:
        print(f"{TABLE} already holds {have:,} rows.")
        if not args.append:
            print("Stopping: a second append would double the money. "
                  "Pass --append if that is what you want.")
            conn.close()
            sys.exit(2)
    run_id = str(uuid.uuid4())
    n = land(conn, df, sha, run_id)
    print(f"landed {n:,} rows into {bulk.LANDING_FQS}.{TABLE}  run {run_id}")

    passed, report = bulk.run_quality_gate(
        conn, SOURCE_ID, TABLE, run_id, sha256=sha, row_count=n,
        source_url=DATA_URL, file_bytes=len(content))
    conn.close()
    if not passed:
        print(f"QUALITY GATE FAILED: {report}")
        sys.exit(1)
    print("DONE")


if __name__ == "__main__":
    main()
