#!/usr/bin/env python3
"""Deterministic loader for USASpending prime contract awards (the 'who got federal
money' side of the money layer).

USASpending's bulk-download API (free, no key) returns transaction-level prime
award data with ~297 columns. We request only a lean+investigative subset
(company IDs, parent, geography, what-for, exec comp, permalink) so the landed
table is small but rich. The job is async: POST -> poll status -> download zip
(possibly multiple CSV members) -> chunk-load through the shared ingest pipeline
(TEXT mirror, provenance stamps, INGEST_RUNS log, SOURCE_REGISTRY upsert).

    python scripts/usaspending_load.py --start 2025-09-29 --end 2025-09-30          # preview
    python scripts/usaspending_load.py --start 2024-10-01 --end 2025-09-30 --run    # land FY2025
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import time
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

SID = "fed_usaspending_contracts"
TABLE = SID.upper()
API = "https://api.usaspending.gov/api/v2/bulk_download/awards/"
UA = {"User-Agent": "Mozilla/5.0 (ripple-usaspending-loader)", "Content-Type": "application/json"}

# Lean core + "potential" investigative hooks (exact USASpending column names).
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


def _request_file(start: str, end: str) -> str:
    payload = {
        "filters": {
            "prime_award_types": ["A", "B", "C", "D"],   # definitive + IDV-issued contracts
            "date_type": "action_date",
            "date_range": {"start_date": start, "end_date": end},
        },
        "columns": COLUMNS,
        "file_format": "csv",
    }
    r = requests.post(API, json=payload, headers=UA, timeout=90)
    r.raise_for_status()
    j = r.json()
    status_url, file_url = j.get("status_url"), j.get("file_url")
    if not status_url:
        raise RuntimeError(f"no status_url in response: {str(j)[:300]}")
    print(f"    job queued: {j.get('file_name')}")
    for i in range(180):                              # up to ~30 min server-side gen
        s = requests.get(status_url, timeout=60).json()
        st = s.get("status")
        if i % 4 == 0:
            print(f"    gen {i}: {st}  rows={s.get('total_rows')} size={s.get('total_size')}")
        if st == "finished":
            return s.get("file_url") or file_url
        if st == "failed":
            raise RuntimeError(f"download job failed: {s.get('message')}")
        time.sleep(10)
    raise RuntimeError("download job did not finish in time")


def _csv_members(zbytes: bytes):
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    for m in z.namelist():
        if m.lower().endswith(".csv"):
            yield m, z


def _months(start: str, end: str) -> list[tuple[str, str]]:
    """Split [start,end] into calendar-month (start,end) pairs — a full-year request
    is too big for the download API to generate in time, so we pull month by month."""
    from datetime import date, timedelta
    sy, sm, sd = map(int, start.split("-"))
    ey, em, ed = map(int, end.split("-"))
    cur, last, out = date(sy, sm, sd), date(ey, em, ed), []
    while cur <= last:
        nxt = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)  # first of next month
        out.append((cur.isoformat(), min(nxt - timedelta(days=1), last).isoformat()))
        cur = nxt
    return out


def _chunk_load(conn, zbytes: bytes, run_id: str, started, overwrite_first: bool) -> tuple[int, list[str]]:
    """Chunk-load one month's zip (possibly several CSV members). overwrite_first
    replaces the table on its first chunk (month 0); every other write appends."""
    from snowflake.connector.pandas_tools import write_pandas
    database, schema = settings.raw_database, settings.raw_schema
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{database}"."{schema}"')
    appended, n, shas = 0, 0, []
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    for m in [x for x in z.namelist() if x.lower().endswith(".csv")]:
        with z.open(m) as fh:
            for chunk in pd.read_csv(fh, chunksize=100_000, **_READ):
                chunk = chunk.loc[:, [c for c in COLUMNS if c in chunk.columns]]
                if not len(chunk):
                    continue
                csha = hashlib.sha256(chunk.to_csv(index=False).encode("utf-8")).hexdigest()
                shas.append(csha)
                out = ingest._stringify(chunk)
                out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
                out[ingest.META_SOURCE_RUN_ID] = run_id
                out[ingest.META_SRC_SHA256] = csha
                ok, _c, _r, _ = write_pandas(conn, out, table_name=TABLE, database=database,
                                             schema=schema, auto_create_table=True,
                                             overwrite=(overwrite_first and n == 0),
                                             quote_identifiers=False)
                if not ok:
                    raise RuntimeError("write_pandas failed")
                appended += len(chunk)
                n += 1
                print(f"      chunk {n}: +{len(chunk):,}", flush=True)
    return appended, shas


def _register(conn, start: str, end: str, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "USASpending — Federal Prime Contract Awards",
        "publisher": "U.S. Treasury — USASpending.gov",
        "url": "https://www.usaspending.gov/download_center/award_data_archive",
        "description": f"Prime contract award transactions ({start}..{end}), curated columns "
                       "(company IDs UEI/DUNS/CAGE, parent, geography, NAICS, exec comp, permalink).",
        "jurisdiction": "US", "category": "Money", "subcategory": "Federal Contracts",
        "unit_of_observation": "one row = one prime contract award transaction",
        "geographic_scope": "United States", "access_method": "bulk", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "daily",
        "volume": f"{rows:,} rows", "license_terms": "Public domain (US Gov / Treasury)",
        "join_keys": "UEI, DUNS, CAGE, NAICS, FIPS",
        "accountability_relevance": "Who received federal contract money (by UEI). Intersect with "
                                    "SAM exclusions for 'debarred-but-funded'; with OFAC for sanctioned recipients.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/usaspending_load.py (LLM-free, curated 36-col subset of 297).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for USASpending prime contracts")
    ap.add_argument("--start", default="2025-09-29")
    ap.add_argument("--end", default="2025-09-30")
    ap.add_argument("--run", action="store_true", help="actually land (default previews)")
    args = ap.parse_args(argv)

    months = _months(args.start, args.end)
    print(f"=== USASpending prime contracts {args.start}..{args.end}  ({len(months)} monthly job(s)) ===")

    if not args.run:
        s, e = months[0]
        zbytes = requests.get(_request_file(s, e), timeout=600).content
        for m, z in _csv_members(zbytes):
            with z.open(m) as fh:
                head = pd.read_csv(fh, nrows=5, **_READ)
            print(f"    PREVIEW {m}: {len(head.columns)} cols -> {', '.join(head.columns)}")
            break
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = snow.connect()
    total, allshas = 0, []
    try:
        for i, (s, e) in enumerate(months):
            print(f"\n-- month {i + 1}/{len(months)}: {s}..{e} --", flush=True)
            zbytes = requests.get(_request_file(s, e), timeout=600).content
            print(f"    zip: {len(zbytes) / 1e6:.1f} MB", flush=True)
            appended, shas = _chunk_load(conn, zbytes, run_id, started, overwrite_first=(i == 0))
            total += appended
            allshas += shas
            print(f"    month {s[:7]}: {appended:,} rows  (grand total {total:,})", flush=True)
        manifest = hashlib.sha256("".join(allshas).encode()).hexdigest()
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", total, None, manifest, API, started, ended,
                        f"USASpending prime contracts {args.start}..{args.end} (monthly). {total:,} rows.")
        _register(conn, args.start, args.end, total)
        print(f"\nLOADED {total:,} rows -> LIBRARY_RAW.LANDING.{TABLE}; registered INCLUDE=Y")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
