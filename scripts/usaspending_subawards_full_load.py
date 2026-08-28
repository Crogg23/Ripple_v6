"""Full pull of USASpending SUBAWARDS (sub-contracts + sub-grants), FY2008-present.

WHY: FED_USASPENDING_SUBAWARDS holds only a 5,000-row API slice. The full
subaward corpus is multi-million rows and is prime graph fuel: each row carries
both the PRIME recipient's UEI/DUNS and the SUB recipient's UEI/DUNS —
prime->sub money edges. This loader lands the whole thing into a NEW table
(FED_USASPENDING_SUBAWARDS_FULL); the old 5k slice is untouched.

Pattern: clone of scripts/usaspending_contracts_full_load.py — month-by-month
bulk-download jobs against POST /api/v2/bulk_download/awards/ with
sub_award_types, checkpointed to disk so a kill/crash resumes at the next
unfinished month. Months run NEWEST-FIRST so the freshest edges land first.

Differences from the contracts loader, on purpose:
- No hardcoded column list. Subaward CSVs have their own schema; guessing names
  is how phantom columns happen. The first successfully downloaded file's
  header (intersection across its CSVs, preserving order) is frozen into the
  checkpoint and the table is created from it — every data column VARCHAR.
  Later months reindex to the frozen set (missing cols -> empty string).
- date_type "action_date" filters subawards on sub-award action date.

Traps built around (all previously hit on this platform):
- write_pandas auto_create_table types columns off the first batch — we CREATE
  TABLE explicitly with every data column VARCHAR before the first write.
- pandas NaN -> the text 'nan' — reads use dtype=str + keep_default_na=False,
  and ingest._stringify handles the rest.
- "success"-logged truncation — per-month row counts print, and the quality
  gate floor is 3M rows (the corpus is known multi-million).

    python scripts/usaspending_subawards_full_load.py            # preview 1 month
    python scripts/usaspending_subawards_full_load.py --run      # full pull, resumable
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

SID = "fed_usaspending_subawards_full"
TABLE = "FED_USASPENDING_SUBAWARDS_FULL"
API = "https://api.usaspending.gov/api/v2/bulk_download/awards/"
UA = {"User-Agent": "Mozilla/5.0 (ripple-usaspending-loader)", "Content-Type": "application/json"}
CKPT = _REPO / "data" / "usaspending_subawards" / "checkpoint.json"

_READ = {"dtype": str, "keep_default_na": False, "na_values": [], "low_memory": False}

START, END = "2007-10-01", "2026-08-27"   # FY2008 .. today


def _months(start: str, end: str) -> list[tuple[str, str]]:
    sy, sm, sd = map(int, start.split("-"))
    ey, em, ed = map(int, end.split("-"))
    cur, last, out = date(sy, sm, sd), date(ey, em, ed), []
    while cur <= last:
        nxt = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)
        out.append((cur.isoformat(), min(nxt - timedelta(days=1), last).isoformat()))
        cur = nxt
    out.reverse()   # newest-first
    return out


def _load_ckpt() -> dict:
    if CKPT.exists():
        return json.loads(CKPT.read_text())
    return {"done_months": [], "total_loaded": 0, "table_created": False, "columns": None}


def _save_ckpt(ck: dict) -> None:
    CKPT.parent.mkdir(parents=True, exist_ok=True)
    CKPT.write_text(json.dumps(ck))


def _request_file(start: str, end: str) -> str:
    payload = {
        "filters": {
            "sub_award_types": ["procurement", "grant"],
            "date_type": "action_date",
            "date_range": {"start_date": start, "end_date": end},
        },
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
            print(f"    request retry {attempt + 1}/8 ({str(ex)[:120]}); wait {wait}s", flush=True)
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


def _discover_columns(zbytes: bytes) -> list[str]:
    """Union of headers across CSVs in the zip, first-file order preserved."""
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    cols: list[str] = []
    seen: set[str] = set()
    for m in [x for x in z.namelist() if x.lower().endswith(".csv")]:
        with z.open(m) as fh:
            head = pd.read_csv(fh, nrows=0, **_READ)
        for c in head.columns:
            if c not in seen:
                seen.add(c)
                cols.append(c)
    if not cols:
        raise RuntimeError("no CSV headers found in downloaded zip")
    return cols


def _create_table(conn, columns: list[str]) -> None:
    cols = ", ".join(f'"{bulk.sf_col(c)}" VARCHAR' for c in columns)
    meta = (f'"{ingest.META_INGESTED_AT}" TIMESTAMP_NTZ, '
            f'"{ingest.META_SOURCE_RUN_ID}" VARCHAR, "{ingest.META_SRC_SHA256}" VARCHAR')
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
    snow.execute(conn, f'CREATE TABLE IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"'
                       f'."{TABLE}" ({cols}, {meta})')


def _land_month(conn, zbytes: bytes, columns: list[str], run_id: str, started) -> int:
    from snowflake.connector.pandas_tools import write_pandas
    appended = 0
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    for m in [x for x in z.namelist() if x.lower().endswith(".csv")]:
        with z.open(m) as fh:
            for chunk in pd.read_csv(fh, chunksize=100_000, **_READ):
                if not len(chunk):
                    continue
                # frozen schema: keep only known columns, add missing as empty
                chunk = chunk.reindex(columns=columns, fill_value="")
                out = ingest._stringify(chunk)
                out.columns = [bulk.sf_col(c) for c in out.columns]
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
        "name": "USASpending — Federal Subawards (sub-contracts + sub-grants, FULL)",
        "publisher": "U.S. Treasury — USASpending.gov",
        "url": "https://www.usaspending.gov/download_center/custom_award_data",
        "description": "All subaward transactions (sub-contracts and sub-grants) FY2008-present, "
                       "full column set. Replaces the 5,000-row API slice in "
                       "FED_USASPENDING_SUBAWARDS. Prime->sub money edges with UEI/DUNS on both ends.",
        "jurisdiction": "US", "category": "Money", "subcategory": "Federal Subawards",
        "unit_of_observation": "one row = one subaward transaction",
        "geographic_scope": "United States", "access_method": "bulk", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily",
        "volume": f"{rows:,} rows", "license_terms": "Public domain (US Gov / Treasury)",
        "join_keys": "prime UEI/DUNS, sub UEI/DUNS, prime award key, NAICS",
        "accountability_relevance": "Who prime contractors/grantees pass federal money to "
                                    "(prime->sub edges, both ends keyed by UEI/DUNS).",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/usaspending_subawards_full_load.py "
                 "(checkpointed month-by-month, newest-first).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Checkpointed full USASpending subawards pull")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    months = _months(START, END)
    if not args.run:
        s, e = months[1]     # most recent full month
        url = _request_file(s, e)
        zbytes = _download(url)
        cols = _discover_columns(zbytes)
        z = zipfile.ZipFile(io.BytesIO(zbytes))
        names = [x for x in z.namelist() if x.lower().endswith(".csv")]
        total = 0
        for name in names:
            with z.open(name) as fh:
                total += sum(len(c) for c in pd.read_csv(fh, chunksize=200_000, usecols=[0], **_READ))
        print(f"PREVIEW {s}..{e}: zip {len(zbytes)/1e6:.1f} MB, {len(names)} csv(s), "
              f"{total:,} rows, {len(cols)} cols")
        print("COLUMNS:", ", ".join(cols))
        print("add --run to land")
        return 0

    ck = _load_ckpt()
    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = snow.connect()
    try:
        todo = [m for m in months if m[0] not in ck["done_months"]]
        print(f"=== USASpending SUBAWARDS full pull: {len(todo)}/{len(months)} months to go "
              f"(landed so far {ck['total_loaded']:,}) ===", flush=True)
        for s, e in todo:
            t0 = time.time()
            url = _request_file(s, e)
            zbytes = _download(url)
            if ck["columns"] is None:
                ck["columns"] = _discover_columns(zbytes)
                _save_ckpt(ck)
                print(f"  frozen schema: {len(ck['columns'])} cols", flush=True)
            if not ck["table_created"]:
                _create_table(conn, ck["columns"])
                ck["table_created"] = True
                _save_ckpt(ck)
            n = _land_month(conn, zbytes, ck["columns"], run_id, started)
            ck["done_months"].append(s)
            ck["total_loaded"] += n
            _save_ckpt(ck)
            print(f"  {s[:7]}: +{n:,} rows in {time.time()-t0:.0f}s "
                  f"(total {ck['total_loaded']:,})", flush=True)
        # per-FY coverage print — makes a silent partial pull visible.
        # Date column name comes from the frozen schema (never guessed).
        date_col = next((bulk.sf_col(c) for c in (ck["columns"] or [])
                         if "action_date" in c.lower()), None)
        if date_col:
            try:
                cur = conn.cursor()
                cur.execute(f'''select case when month(try_to_date("{date_col}")) >= 10
                                            then year(try_to_date("{date_col}")) + 1
                                            else year(try_to_date("{date_col}")) end fy,
                                       count(*), min("{date_col}"), max("{date_col}")
                                from "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"
                                group by 1 order by 1''')
                for row in cur.fetchall():
                    print(f"  FY{row[0]}: {row[1]:,} rows  {row[2]} .. {row[3]}", flush=True)
            except Exception as ex:  # noqa: BLE001
                print(f"  (coverage print skipped: {str(ex)[:120]})", flush=True)
        passed, report = bulk.run_quality_gate(
            conn, SID, TABLE, run_id, row_count=ck["total_loaded"],
            source_url=API, expected_min_rows=3_000_000)
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
