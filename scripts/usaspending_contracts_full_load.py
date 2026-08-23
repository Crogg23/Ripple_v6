"""Full re-pull of USASpending prime contract transactions, FY2007-FY2026.

WHY: FED_USASPENDING_CONTRACTS_FULL (20M rows) is a truncated sample — exactly
1,000,000 rows per FY and each FY's action_date spans only ~2-3 months. No
loader for it exists in the repo. This is that loader, done right: month-by-month
bulk-download jobs (a full-FY request is too big for the API to generate),
checkpointed to disk so a kill/crash resumes at the next unfinished month, and
landing appended into a NEW table (FED_USASPENDING_CONTRACTS_FULL_R2) so the old
sample stays untouched until the re-pull is verified and staging is repointed.

Traps built around (all previously hit on this platform):
- write_pandas auto_create_table types columns off the first batch — we CREATE
  TABLE explicitly with every data column VARCHAR before the first write.
- pandas NaN -> the text 'nan' — reads use dtype=str + keep_default_na=False,
  and ingest._stringify handles the rest.
- "success"-logged truncation — the quality gate floor is 50M rows (real
  transaction volume 2007-2026 is far above the old 20M sample), and the loader
  prints per-FY date-coverage so a partial pull is visible, not silent.

    python scripts/usaspending_contracts_full_load.py            # preview 1 month
    python scripts/usaspending_contracts_full_load.py --run      # full pull, resumable
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import time
import uuid
import zipfile
from datetime import date, timedelta
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
except Exception:
    pass

import ingest  # noqa: E402
import register  # noqa: E402
import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402
from config import settings  # noqa: E402

SID = "fed_usaspending_contracts_full_r2"
TABLE = "FED_USASPENDING_CONTRACTS_FULL_R2"
API = "https://api.usaspending.gov/api/v2/bulk_download/awards/"
UA = {"User-Agent": "Mozilla/5.0 (ripple-usaspending-loader)", "Content-Type": "application/json"}
CKPT = _REPO / "data" / "usaspending_full" / "checkpoint.json"

# Same curated 36-col investigative subset the wired contracts table uses.
COLUMNS = [
    "contract_award_unique_key", "award_id_piid", "action_date",
    "period_of_performance_start_date", "period_of_performance_current_end_date",
    "federal_action_obligation", "total_dollars_obligated", "current_total_value_of_award",
    "awarding_agency_name", "awarding_sub_agency_name", "funding_agency_name",
    "recipient_uei", "recipient_duns", "cage_code", "recipient_name",
    "recipient_doing_business_as_name", "recipient_parent_uei", "recipient_parent_name",
    "recipient_city_name", "recipient_state_code", "recipient_zip_4_code", "recipient_country_name",
    "primary_place_of_performance_state_code", "primary_place_of_performance_city_name",
    "award_type", "naics_code", "naics_description", "product_or_service_code_description",
    "transaction_description",
    "highly_compensated_officer_1_name", "highly_compensated_officer_1_amount",
    "highly_compensated_officer_2_name", "highly_compensated_officer_2_amount",
    "foreign_owned", "usaspending_permalink", "last_modified_date",
]
_READ = {"dtype": str, "keep_default_na": False, "na_values": [], "low_memory": False}

START, END = "2006-10-01", "2026-08-22"   # FY2007 .. today (FY2026 partial by nature)


def _months(start: str, end: str) -> list[tuple[str, str]]:
    sy, sm, sd = map(int, start.split("-"))
    ey, em, ed = map(int, end.split("-"))
    cur, last, out = date(sy, sm, sd), date(ey, em, ed), []
    while cur <= last:
        nxt = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)
        out.append((cur.isoformat(), min(nxt - timedelta(days=1), last).isoformat()))
        cur = nxt
    return out


def _load_ckpt() -> dict:
    if CKPT.exists():
        return json.loads(CKPT.read_text())
    return {"done_months": [], "total_loaded": 0, "table_created": False}


def _save_ckpt(ck: dict) -> None:
    CKPT.parent.mkdir(parents=True, exist_ok=True)
    CKPT.write_text(json.dumps(ck))


def _request_file(start: str, end: str) -> str:
    payload = {
        "filters": {
            "prime_award_types": ["A", "B", "C", "D"],
            "date_type": "action_date",
            "date_range": {"start_date": start, "end_date": end},
        },
        "columns": COLUMNS,
        "file_format": "csv",
    }
    for attempt in range(8):
        try:
            r = requests.post(API, json=payload, headers=UA, timeout=90)
            r.raise_for_status()
            j = r.json()
            status_url, file_url = j.get("status_url"), j.get("file_url")
            if not status_url:
                raise RuntimeError(f"no status_url: {str(j)[:200]}")
            for _ in range(240):                      # up to ~40 min server-side gen
                s = requests.get(status_url, timeout=60).json()
                st = s.get("status")
                if st == "finished":
                    return s.get("file_url") or file_url
                if st == "failed":
                    raise RuntimeError(f"gen job failed: {s.get('message')}")
                time.sleep(10)
            raise RuntimeError("gen job timed out")
        except Exception as ex:  # noqa: BLE001
            wait = min(600, 30 * (attempt + 1))
            print(f"    request retry {attempt + 1}/8 ({str(ex)[:80]}); wait {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"month {start} unrecoverable")


def _download(url: str) -> bytes:
    for attempt in range(8):
        try:
            r = requests.get(url, timeout=1200)
            r.raise_for_status()
            return r.content
        except Exception as ex:  # noqa: BLE001
            wait = min(300, 20 * (attempt + 1))
            print(f"    download retry {attempt + 1}/8 ({str(ex)[:80]}); wait {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("download unrecoverable")


def _create_table(conn) -> None:
    cols = ", ".join(f'"{c.upper()}" VARCHAR' for c in COLUMNS)
    meta = (f'"{ingest.META_INGESTED_AT}" TIMESTAMP_NTZ, '
            f'"{ingest.META_SOURCE_RUN_ID}" VARCHAR, "{ingest.META_SRC_SHA256}" VARCHAR')
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
    snow.execute(conn, f'CREATE TABLE IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"'
                       f'."{TABLE}" ({cols}, {meta})')


def _land_month(conn, zbytes: bytes, run_id: str, started) -> int:
    from snowflake.connector.pandas_tools import write_pandas
    appended = 0
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    for m in [x for x in z.namelist() if x.lower().endswith(".csv")]:
        with z.open(m) as fh:
            for chunk in pd.read_csv(fh, chunksize=100_000, **_READ):
                chunk = chunk.loc[:, [c for c in COLUMNS if c in chunk.columns]]
                if not len(chunk):
                    continue
                out = ingest._stringify(chunk)
                out.columns = [c.upper() for c in out.columns]
                out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
                out[ingest.META_SOURCE_RUN_ID] = run_id
                out[ingest.META_SRC_SHA256] = hashlib.sha256(
                    chunk.to_csv(index=False).encode("utf-8")).hexdigest()
                ok, _c, _r, _ = write_pandas(conn, out, table_name=TABLE,
                                             database=settings.raw_database,
                                             schema=settings.raw_schema,
                                             auto_create_table=False, overwrite=False,
                                             quote_identifiers=False)
                if not ok:
                    raise RuntimeError("write_pandas failed")
                appended += len(chunk)
    return appended


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "USASpending — Federal Prime Contract Awards (FULL re-pull)",
        "publisher": "U.S. Treasury — USASpending.gov",
        "url": "https://www.usaspending.gov/download_center/award_data_archive",
        "description": "Prime contract award transactions FY2007-FY2026, curated 36-col subset. "
                       "Replaces the truncated FED_USASPENDING_CONTRACTS_FULL (1M/FY sample).",
        "jurisdiction": "US", "category": "Money", "subcategory": "Federal Contracts",
        "unit_of_observation": "one row = one prime contract award transaction",
        "geographic_scope": "United States", "access_method": "bulk", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily",
        "volume": f"{rows:,} rows", "license_terms": "Public domain (US Gov / Treasury)",
        "join_keys": "UEI, DUNS, CAGE, NAICS, FIPS",
        "accountability_relevance": "Who received federal contract money (by UEI), full history.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/usaspending_contracts_full_load.py (checkpointed month-by-month).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Checkpointed full USASpending contracts re-pull")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    months = _months(START, END)
    if not args.run:
        s, e = months[-2]
        url = _request_file(s, e)
        zbytes = _download(url)
        z = zipfile.ZipFile(io.BytesIO(zbytes))
        name = [x for x in z.namelist() if x.lower().endswith(".csv")][0]
        with z.open(name) as fh:
            head = pd.read_csv(fh, nrows=5, **_READ)
        print(f"PREVIEW {s}..{e}: zip {len(zbytes)/1e6:.1f} MB, {len(head.columns)} cols")
        print("add --run to land")
        return 0

    ck = _load_ckpt()
    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = snow.connect()
    try:
        if not ck["table_created"]:
            _create_table(conn)
            ck["table_created"] = True
            _save_ckpt(ck)
        todo = [m for m in months if m[0] not in ck["done_months"]]
        print(f"=== USASpending FULL re-pull: {len(todo)}/{len(months)} months to go "
              f"(landed so far {ck['total_loaded']:,}) ===", flush=True)
        for s, e in todo:
            t0 = time.time()
            url = _request_file(s, e)
            zbytes = _download(url)
            n = _land_month(conn, zbytes, run_id, started)
            ck["done_months"].append(s)
            ck["total_loaded"] += n
            _save_ckpt(ck)
            print(f"  {s[:7]}: +{n:,} rows in {time.time()-t0:.0f}s "
                  f"(total {ck['total_loaded']:,})", flush=True)
        # per-FY coverage print — makes a silent partial pull visible
        cur = conn.cursor()
        cur.execute(f'''select case when month(try_to_date(ACTION_DATE)) >= 10
                                    then year(try_to_date(ACTION_DATE)) + 1
                                    else year(try_to_date(ACTION_DATE)) end fy,
                               count(*), min(ACTION_DATE), max(ACTION_DATE)
                        from "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"
                        group by 1 order by 1''')
        for row in cur.fetchall():
            print(f"  FY{row[0]}: {row[1]:,} rows  {row[2]} .. {row[3]}", flush=True)
        passed, report = bulk.run_quality_gate(
            conn, SID, TABLE, run_id, row_count=ck["total_loaded"],
            source_url=API, expected_min_rows=50_000_000)
        if not passed:
            print(f"QUALITY GATE FAILED {TABLE}: {report}")
            return 1
        _register(conn, ck["total_loaded"])
        print(f"\nLOADED {ck['total_loaded']:,} rows -> LIBRARY_RAW.LANDING.{TABLE}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
