#!/usr/bin/env python3
"""DOL EBSA Form 5500 -- FULL filing history (2009-2024), main form file.

Fixes the ~80x truncation in FED_DOL_FORM5500 (33,484 rows vs ~250k main-form
filings/yr published). Lands into a NEW table FED_DOL_FORM5500_FULL -- the old
table is left untouched (write_pandas overwrite keeps old schema; never reuse
a truncated table's shell).

Source: https://www.dol.gov/agencies/ebsa/researchers/data/health-and-welfare/form-5500-datasets
Files:  https://askebsa.dol.gov/FOIA%20Files/{year}/Latest/F_5500_{year}_Latest.zip
        ("Latest" = the latest filing per plan-year; "All" adds superseded/amended
        duplicates. Schedules + Form 5500-SF are follow-ons, not loaded here.)

Traps honored:
  - every column lands as text via ingest._stringify (nulls never land as 'nan')
  - year columns stay text -- nothing is cast to date
  - append per year with column-drift handling (ALTER ADD for new columns);
    write_pandas COPY matches by column name so older/narrower years are fine
  - checkpoint per year (logs/dol_form5500_full_checkpoint.json) -> resumable
  - connection health-checked before every upload (multi-hour-run token expiry)

    python scripts/dol_form5500_full_load.py           # preview (probe 2024)
    python scripts/dol_form5500_full_load.py --run     # load 2024 -> 2009
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import uuid
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

import ingest  # noqa: E402
import register  # noqa: E402
import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

SID = "fed_dol_form5500_full"
TABLE = "FED_DOL_FORM5500_FULL"
URL_TMPL = "https://askebsa.dol.gov/FOIA%20Files/{year}/Latest/F_5500_{year}_Latest.zip"
UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
YEARS = list(range(2024, 2008, -1))  # newest first per authorization
CHECKPOINT_FILE = _REPO / "logs" / "dol_form5500_full_checkpoint.json"

REGISTER_CFG = {
    "source_id": SID,
    "name": "DOL EBSA Form 5500 annual filings (full history, main form)",
    "publisher": "U.S. Department of Labor, Employee Benefits Security Administration (EBSA)",
    "url": "https://www.dol.gov/agencies/ebsa/researchers/data/health-and-welfare/form-5500-datasets",
    "description": "Annual Form 5500 filings (main form, 'Latest' file per plan-year) for "
                   "employee benefit plans, 2009-2024. One row = the latest filing for a "
                   "plan-year: sponsor name/EIN, plan number, plan type, participant counts, "
                   "assets, administrator and preparer fields. Full-history replacement for "
                   "the truncated FED_DOL_FORM5500 (33k rows).",
    "jurisdiction": "federal", "category": "Labor", "subcategory": "Employee Benefits",
    "unit_of_observation": "one row = latest Form 5500 filing for one plan-year",
    "geographic_scope": "United States", "access_method": "bulk_download", "format": "csv",
    "auth": {"type": "none"}, "cost": "free",
    "update_cadence": "annual files, updated monthly by EBSA",
    "license_terms": "U.S. Government work, public domain",
    "join_keys": "SPONS_DFE_EIN, SPONS_DFE_PN (EIN+PN = plan key, joins PBGC trusteed plans), SPONS_DFE_MAIL_US_ZIP",
    "accountability_relevance": "The census of who runs employee benefit plans and how much "
                                "money sits in them. EIN+PN joins to PBGC trusteed/failed "
                                "plans; EIN joins across the whole warehouse spine.",
    "priority_tier": "1", "landing_table": TABLE,
    "notes": "Loaded by scripts/dol_form5500_full_load.py (per-year append, checkpointed). "
             "Schedules (SB/MB/H/I/C) and Form 5500-SF are follow-on loads.",
}


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------
def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {}


def save_checkpoint(cp: dict):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(json.dumps(cp, indent=2))


# ---------------------------------------------------------------------------
# Connection (health-checked; multi-hour runs outlive auth tokens)
# ---------------------------------------------------------------------------
_conn = None


def get_conn():
    global _conn
    if _conn is not None:
        try:
            _conn.cursor().execute("select 1")
            return _conn
        except Exception:
            try:
                _conn.close()
            except Exception:
                pass
            _conn = None
            print("  (snowflake session expired -- reconnecting)", flush=True)
    _conn = snow.connect()
    return _conn


# ---------------------------------------------------------------------------
# Download + parse one year
# ---------------------------------------------------------------------------
def fetch_year(year: int) -> tuple[pd.DataFrame, str, int]:
    """Returns (df, sha256, file_bytes). Retries transient network errors."""
    url = URL_TMPL.format(year=year)
    last = None
    for attempt in range(5):
        try:
            r = requests.get(url, headers=UA, timeout=900)
            r.raise_for_status()
            break
        except Exception as exc:
            last = exc
            print(f"    download error ({str(exc)[:80]}), retry {attempt + 1}/5...",
                  flush=True)
            import time
            time.sleep(min(120, 20 * (attempt + 1)))
    else:
        raise RuntimeError(f"download failed for {year}: {last}")
    sha = hashlib.sha256(r.content).hexdigest()
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(csvs) != 1:
            raise RuntimeError(f"{year}: expected 1 csv in zip, got {csvs}")
        with zf.open(csvs[0]) as f:
            df = pd.read_csv(f, dtype=str, low_memory=False, encoding_errors="replace")
    return df, sha, len(r.content)


# ---------------------------------------------------------------------------
# Land one year (append, column-drift-safe)
# ---------------------------------------------------------------------------
def table_columns(conn) -> list[str]:
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
            f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME=%s "
            "ORDER BY ORDINAL_POSITION", (TABLE,))
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()


def land_year(year: int, df: pd.DataFrame, sha: str, run_id: str) -> int:
    from snowflake.connector.pandas_tools import write_pandas

    out = ingest._stringify(df)  # all-text, null-safe (never the string 'nan')
    out.columns = [bulk.sf_col(c) for c in out.columns]
    # collapse any post-sanitize duplicate column names (keep first)
    out = out.loc[:, ~out.columns.duplicated()]
    started = dt.datetime.now(dt.timezone.utc)
    out["SRC_YEAR"] = str(year)
    out[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    out[bulk.META_SOURCE_RUN_ID] = run_id
    out[bulk.META_SRC_SHA256] = sha

    conn = get_conn()
    existing = table_columns(conn)
    if not existing:
        ok, _c, nrows, _ = write_pandas(
            conn, out, table_name=TABLE,
            database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
            auto_create_table=True, overwrite=False, quote_identifiers=False)
    else:
        new_cols = [c for c in out.columns if c not in existing]
        if new_cols:
            cur = conn.cursor()
            try:
                adds = ", ".join(f'"{c}" VARCHAR' for c in new_cols)
                cur.execute(f'ALTER TABLE {bulk.LANDING_FQS}."{TABLE}" ADD COLUMN {adds}')
            finally:
                cur.close()
            print(f"    (+{len(new_cols)} new columns: {new_cols[:6]}"
                  f"{'...' if len(new_cols) > 6 else ''})", flush=True)
        ok, _c, nrows, _ = write_pandas(
            conn, out, table_name=TABLE,
            database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
            auto_create_table=False, overwrite=False, quote_identifiers=False)
    if not ok:
        raise RuntimeError(f"write_pandas failed for {year}")
    return len(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--years", type=str, default="",
                    help="comma-separated year list (default: 2024 back to 2009)")
    args = ap.parse_args(argv)

    years = [int(y) for y in args.years.split(",") if y.strip()] or YEARS

    print(f"=== DOL Form 5500 full history -> {TABLE} ===", flush=True)
    if not args.run:
        url = URL_TMPL.format(year=years[0])
        r = requests.head(url, headers=UA, timeout=60, allow_redirects=True)
        print(f"probe {years[0]}: HTTP {r.status_code}, "
              f"{int(r.headers.get('Content-Length', 0)):,} bytes zip")
        print("PREVIEW only -- add --run to land.")
        return 0

    cp = load_checkpoint()
    run_id = str(uuid.uuid4())
    get_conn()  # fail fast on credentials
    failures = []

    for year in years:
        key = str(year)
        if cp.get(key, {}).get("status") == "done":
            print(f"[{year}] already loaded ({cp[key]['rows']:,} rows) -- skip", flush=True)
            continue
        print(f"[{year}] downloading...", flush=True)
        try:
            df, sha, nbytes = fetch_year(year)
            file_rows = len(df)
            print(f"[{year}] {file_rows:,} rows x {len(df.columns)} cols "
                  f"({nbytes / 1e6:.0f}MB zip), landing...", flush=True)
            landed = land_year(year, df, sha, run_id)
            if landed != file_rows:
                raise RuntimeError(f"row mismatch: file {file_rows:,} vs landed {landed:,}")
            bulk.bulk_log_run(get_conn(), SID, run_id, sha256=sha, row_count=landed,
                              status="success", source_url=URL_TMPL.format(year=year),
                              file_bytes=nbytes,
                              message=f"{SID} year {year}; {landed:,} rows appended")
            cp[key] = {"status": "done", "rows": landed, "sha": sha}
            save_checkpoint(cp)
            print(f"[{year}] LANDED {landed:,} rows (file rows match)", flush=True)
        except Exception as e:
            print(f"[{year}] FAILED: {str(e)[:200]}", flush=True)
            failures.append(year)
            cp[key] = {"status": "failed", "error": str(e)[:300]}
            save_checkpoint(cp)

    # ---- final verification + registration ----
    conn = get_conn()
    total = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM {bulk.LANDING_FQS}."{TABLE}"')
    cur = conn.cursor()
    cur.execute(
        f'SELECT COUNT(SPONS_DFE_EIN), APPROX_COUNT_DISTINCT(NULLIF(TRIM(SPONS_DFE_EIN),\'\')), '
        f'COUNT(SPONS_DFE_PN), APPROX_COUNT_DISTINCT(NULLIF(TRIM(SPONS_DFE_PN),\'\')), '
        f'APPROX_COUNT_DISTINCT(NULLIF(TRIM(SPONS_DFE_EIN),\'\') || \'-\' || NULLIF(TRIM(SPONS_DFE_PN),\'\')) '
        f'FROM {bulk.LANDING_FQS}."{TABLE}"')
    ein_n, ein_d, pn_n, pn_d, einpn_d = cur.fetchone()
    cur.close()
    print(f"\nTOTAL {total:,} rows in {TABLE}")
    print(f"EIN: {ein_n:,} populated, ~{ein_d:,} distinct")
    print(f"PN:  {pn_n:,} populated, ~{pn_d:,} distinct")
    print(f"EIN+PN plan key: ~{einpn_d:,} distinct plans")

    done_years = sum(1 for v in cp.values() if isinstance(v, dict) and v.get("status") == "done")
    if done_years == len(years) and not failures:
        passed, report = bulk.run_quality_gate(conn, SID, TABLE, run_id,
                                               row_count=total, source_url=REGISTER_CFG["url"])
        cfg = dict(REGISTER_CFG)
        cfg["volume"] = f"{total:,} rows (2009-2024)"
        snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))
        print("registered INCLUDE=Y")
        if not passed:
            print(f"QUALITY GATE FAILED: {report}")
            return 1
    else:
        print(f"partial: {done_years}/{len(years)} years done, failures={failures} -- "
              "re-run to resume from checkpoint (registration deferred to complete run)")
        return 1 if failures else 0
    print("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
