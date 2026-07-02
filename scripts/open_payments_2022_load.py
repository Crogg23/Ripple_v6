#!/usr/bin/env python3
"""DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only.
Replaces/appends directly on the live table (a mid-run crash leaves a partial year).
For any new or repeat bulk load use scripts/bridge_fuel_load.py, which lands through
a staging table + atomic swap, density-gates, and guards the registry.

Backfill CMS Open Payments GENERAL payments detail for PROGRAM YEAR 2022
(discovery sweep #23: the FED_CMS_OPEN_PAYMENTS union currently spans only
2024 [unsuffixed table] + 2023 [_2023 table]. 2022 is the missing year -- adding
it turns the "is this normal?" snapshot into a real 3-year time series, which the
just-below-$125 meal-cap fingerprint / threshold detectors need to establish a
trend instead of a single before/after).

Lands to a NEW per-year table LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS_2022 that
MATCHES the 94-column schema of FED_CMS_OPEN_PAYMENTS_2023 exactly (same column
names, same ordinal positions, _INGESTED_AT as NUMBER), so the dbt union model
int_open_payments_all_years just needs one more `union all select * from ...2022`.

Source (resolved live via the OpenPayments metastore API, 2026-06-28):
  https://download.cms.gov/openpayments/PGYR2022_P01232026_01102026/OP_DTL_GNRL_PGYR2022_P01232026_01102026.csv
  ~7.43 GB uncompressed CSV, 91 source columns, ~12-13M rows. This is the latest
  CMS republication (P01232026 = published 2026-01-23). It's a direct CSV (not a
  zip). We DOWNLOAD it to a local temp file (iter_content, 1 MB blocks) then parse
  the file in row chunks and APPEND -- the whole 7.4 GB is NEVER held in memory, and
  decoupling the transfer from the parse avoids the EOF socket-close that mislogged
  the 2026-06-28 run (a complete load reported as error/0). Temp file is cleaned up.

Idempotent: snapshot-replace. The first chunk REPLACES the table (overwrite=True),
every later chunk APPENDS -- a full re-run rebuilds the year cleanly, no dupes.
RECORD_ID is CMS's globally-unique payment key (disjoint across years), so the
unioned table can't double-count.

    python3 scripts/open_payments_2022_load.py            # preview (size + plan, no load)
    ONBOARD_SKIP_IF_UNCHANGED=0 python3 scripts/open_payments_2022_load.py --run

BUDGET: one real ~12-13M-row append on RIPPLE_WH (X-Small). ~698 MB compressed in
Snowflake (cf. the 2023 sibling). Within the keyless-backfill budget. Stream is
bounded-memory; the spend is the storage + a single warehouse session.
"""
from __future__ import annotations

import argparse
import csv
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

TABLE = "FED_CMS_OPEN_PAYMENTS_2022"
TEMPLATE_TABLE = "FED_CMS_OPEN_PAYMENTS_2023"   # exact schema we mirror
SID = "fed_cms_open_payments_2022"
URL = ("https://download.cms.gov/openpayments/PGYR2022_P01232026_01102026/"
       "OP_DTL_GNRL_PGYR2022_P01232026_01102026.csv")
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
CHUNK = 250_000
SCRATCH = Path("c:/Code/Ripple_v6/.scratch/"
               "e8eac5fb-de36-4362-9440-da24a904b9b4/scratchpad")

# The 94 landing columns, in ordinal order, taken from FED_CMS_OPEN_PAYMENTS_2023.
# The 91 SOURCE columns map 1:1 BY POSITION to the first 91 of these (verified:
# UPPER(source header) == landing name for every position except pos 3
# Teaching_Hospital_CCN->CCN and pos 7 Covered_Recipient_NPI->NPI). We rename the
# CSV header to these landing names by position, which is robust to CMS casing drift.
DATA_COLS = [
    "CHANGE_TYPE", "COVERED_RECIPIENT_TYPE", "CCN", "TEACHING_HOSPITAL_ID",
    "TEACHING_HOSPITAL_NAME", "COVERED_RECIPIENT_PROFILE_ID", "NPI",
    "COVERED_RECIPIENT_FIRST_NAME", "COVERED_RECIPIENT_MIDDLE_NAME",
    "COVERED_RECIPIENT_LAST_NAME", "COVERED_RECIPIENT_NAME_SUFFIX",
    "RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE1",
    "RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE2", "RECIPIENT_CITY",
    "RECIPIENT_STATE", "RECIPIENT_ZIP_CODE", "RECIPIENT_COUNTRY", "RECIPIENT_PROVINCE",
    "RECIPIENT_POSTAL_CODE", "COVERED_RECIPIENT_PRIMARY_TYPE_1",
    "COVERED_RECIPIENT_PRIMARY_TYPE_2", "COVERED_RECIPIENT_PRIMARY_TYPE_3",
    "COVERED_RECIPIENT_PRIMARY_TYPE_4", "COVERED_RECIPIENT_PRIMARY_TYPE_5",
    "COVERED_RECIPIENT_PRIMARY_TYPE_6", "COVERED_RECIPIENT_SPECIALTY_1",
    "COVERED_RECIPIENT_SPECIALTY_2", "COVERED_RECIPIENT_SPECIALTY_3",
    "COVERED_RECIPIENT_SPECIALTY_4", "COVERED_RECIPIENT_SPECIALTY_5",
    "COVERED_RECIPIENT_SPECIALTY_6", "COVERED_RECIPIENT_LICENSE_STATE_CODE1",
    "COVERED_RECIPIENT_LICENSE_STATE_CODE2", "COVERED_RECIPIENT_LICENSE_STATE_CODE3",
    "COVERED_RECIPIENT_LICENSE_STATE_CODE4", "COVERED_RECIPIENT_LICENSE_STATE_CODE5",
    "SUBMITTING_APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_NAME",
    "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID",
    "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME",
    "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE",
    "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_COUNTRY",
    "TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS", "DATE_OF_PAYMENT",
    "NUMBER_OF_PAYMENTS_INCLUDED_IN_TOTAL_AMOUNT",
    "FORM_OF_PAYMENT_OR_TRANSFER_OF_VALUE", "NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE",
    "CITY_OF_TRAVEL", "STATE_OF_TRAVEL", "COUNTRY_OF_TRAVEL",
    "PHYSICIAN_OWNERSHIP_INDICATOR", "THIRD_PARTY_PAYMENT_RECIPIENT_INDICATOR",
    "NAME_OF_THIRD_PARTY_ENTITY_RECEIVING_PAYMENT_OR_TRANSFER_OF_VALUE",
    "CHARITY_INDICATOR", "THIRD_PARTY_EQUALS_COVERED_RECIPIENT_INDICATOR",
    "CONTEXTUAL_INFORMATION", "DELAY_IN_PUBLICATION_INDICATOR", "RECORD_ID",
    "DISPUTE_STATUS_FOR_PUBLICATION", "RELATED_PRODUCT_INDICATOR",
    "COVERED_OR_NONCOVERED_INDICATOR_1",
    "INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1",
    "PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_1",
    "NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1",
    "ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_1",
    "ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1",
    "COVERED_OR_NONCOVERED_INDICATOR_2",
    "INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_2",
    "PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_2",
    "NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_2",
    "ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_2",
    "ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_2",
    "COVERED_OR_NONCOVERED_INDICATOR_3",
    "INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_3",
    "PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_3",
    "NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_3",
    "ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_3",
    "ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_3",
    "COVERED_OR_NONCOVERED_INDICATOR_4",
    "INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_4",
    "PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_4",
    "NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_4",
    "ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_4",
    "ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_4",
    "COVERED_OR_NONCOVERED_INDICATOR_5",
    "INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_5",
    "PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_5",
    "NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_5",
    "ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_5",
    "ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_5", "PROGRAM_YEAR",
    "PAYMENT_PUBLICATION_DATE",
]  # 91 data cols
META_COLS = [ingest.META_INGESTED_AT, ingest.META_SOURCE_RUN_ID, ingest.META_SRC_SHA256]
TABLE_COLS = DATA_COLS + META_COLS  # 94, exact ordinal order of the 2023 table


def _preview() -> tuple[int, int]:
    """HEAD/Content-Length the CSV. Returns (bytes, source_col_count)."""
    with requests.get(URL, headers=UA, stream=True, timeout=120) as r:
        r.raise_for_status()
        nbytes = int(r.headers.get("Content-Length") or 0)
        raw = next(r.iter_lines())
        hdr = raw.decode("utf-8-sig")
        ncols = len(next(csv.reader(io.StringIO(hdr))))
    return nbytes, ncols


def _ensure_table(conn) -> None:
    """Create FED_CMS_OPEN_PAYMENTS_2022 with the EXACT schema of the 2023 sibling
    (CREATE TABLE LIKE clones column names/types/order, incl. _INGESTED_AT NUMBER)."""
    fq = f'"{settings.raw_database}"."{settings.raw_schema}"'
    snow.execute(conn,
                 f'CREATE TABLE IF NOT EXISTS {fq}."{TABLE}" '
                 f'LIKE {fq}."{TEMPLATE_TABLE}"')


def _download_to_disk(dest: Path) -> int:
    """Stream the CSV to a LOCAL temp file with iter_content (bounded memory, 1 MB
    blocks). Returns bytes written. This DECOUPLES the network transfer from the
    parse -- the fec_itcont-proven idiom. Reading requests' r.raw live during a
    multi-GB parse is fragile: urllib3 auto-closes the socket at content-length EOF,
    so pandas' final read raised 'I/O operation on closed file' *after* every row was
    already written (the 2026-06-28 mislog: a complete 13.25M-row load logged as
    error/0). Parsing a finished local file cannot hit that."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    nbytes = 0
    with requests.get(URL, headers=UA, stream=True, timeout=900) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for block in r.iter_content(1024 * 1024):
                if block:
                    f.write(block)
                    nbytes += len(block)
    return nbytes


def _stream_load(conn, run_id: str, csv_path: Path, progress: dict) -> tuple[int, int, str]:
    """Parse the LOCAL CSV in row chunks and append to Snowflake, bounded memory.
    Returns (rows, file_bytes, manifest_sha). ``progress['rows']`` is updated after
    every chunk so the caller's error path logs the REAL landed count, not a
    hardcoded 0 (the other half of the 2026-06-28 mislog)."""
    started = ingest._utcnow()
    ingested_at = started.replace(tzinfo=None)
    appended = 0
    file_bytes = csv_path.stat().st_size
    chunk_shas: list[str] = []
    n = 0

    reader = pd.read_csv(
        csv_path, dtype=str, keep_default_na=False, na_filter=False,
        chunksize=CHUNK, low_memory=False, header=0,
    )
    for chunk in reader:
        if chunk.shape[1] != len(DATA_COLS):
            raise RuntimeError(
                f"chunk has {chunk.shape[1]} cols, expected {len(DATA_COLS)} "
                f"-- CMS header drift; aborting before a misaligned write.")
        # Rename BY POSITION to the landing column names (drift-proof).
        chunk.columns = DATA_COLS
        csv_bytes = chunk.to_csv(index=False).encode("utf-8")
        chunk_sha = hashlib.sha256(csv_bytes).hexdigest()
        chunk_shas.append(chunk_sha)

        out = chunk.copy()
        out[ingest.META_INGESTED_AT] = ingested_at
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = chunk_sha
        out = out[TABLE_COLS]
        overwrite = (n == 0)  # snapshot-replace: first chunk wipes, rest append
        ok, _c, _nrows, _ = write_pandas(
            conn, out, table_name=TABLE,
            database=settings.raw_database, schema=settings.raw_schema,
            auto_create_table=False, overwrite=overwrite, quote_identifiers=False,
        )
        if not ok:
            raise RuntimeError(f"write_pandas failed on chunk {n + 1} "
                               f"(after {appended:,} rows)")
        appended += len(out)
        progress["rows"] = appended
        n += 1
        print(f"  chunk {n}: +{len(out):,} rows (total {appended:,})", flush=True)

    if appended == 0:
        raise RuntimeError("parsed 0 rows -- bad file / parse / empty file")
    manifest_sha = hashlib.sha256("".join(chunk_shas).encode("utf-8")).hexdigest()
    return appended, file_bytes, manifest_sha


def _register(conn, rows: int) -> None:
    """Best-effort registry upsert for the new per-year source. Non-fatal."""
    config = {
        "source_id": SID,
        "name": "CMS Open Payments - General Payments Detail (PY2022)",
        "url": URL,
        "publisher": "Centers for Medicare & Medicaid Services (CMS)",
        "jurisdiction": "fed",
        "category": "health",
        "subcategory": "industry_payments",
        "unit_of_observation": "one row = one general (non-research) payment / transfer of value to a covered recipient, program year 2022",
        "access_method": "bulk_csv",
        "format": "csv",
        "auth": {"type": "none"},
        "cost": "free",
        "update_cadence": "annual",
        "volume": str(rows),
        "license_terms": "Public domain (US federal government work)",
        "url_temporal_coverage": "2022",
        "temporal_coverage": "2022",
        "join_keys": "NPI,CCN,RECORD_ID,NDC",
        "priority_tier": "1",
        "join_keys_std": ["NPI", "CCN", "RECORD_ID", "NDC"],
        "join_key_tier": "STEEL",
        "join_key_tier_provisional": True,
        "landing_table": TABLE,
    }
    enrichment = {
        "accountability_relevance": "high",
        "epstein_relevant": False,
        "domain_primary": "health_medicine",
        "entity_types": ["physician", "teaching_hospital", "manufacturer", "gpo"],
        "themes": ["industry_payments", "conflicts_of_interest", "pharma"],
        "domain_confidence": "high",
        "notes": ("Program-year-2022 sibling of FED_CMS_OPEN_PAYMENTS (2024) and "
                  "FED_CMS_OPEN_PAYMENTS_2023. Identical 94-col schema; extends the "
                  "dbt union int_open_payments_all_years to 3 years. RECORD_ID is "
                  "globally unique across years (disjoint) -> UNION ALL is dup-safe. "
                  "Source = latest CMS republication P01232026 (published 2026-01-23)."),
    }
    try:
        row = register._build_row(config, enrichment)
        sql, params = register._merge_sql(row)
        snow.execute(conn, sql, params)
        print(f"  registry: upserted {SID}")
    except Exception as ex:  # noqa: BLE001
        print(f"  registry upsert skipped ({type(ex).__name__}: {str(ex)[:140]})")


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill CMS Open Payments PY2022 (chunked stream).")
    ap.add_argument("--run", action="store_true", help="actually stream + load (else preview)")
    args = ap.parse_args()

    nbytes, ncols = _preview()
    gb = nbytes / 1e9
    est_rows = "~12-13M (cf. 2023: 14.7M / 698MB compressed)"
    print(f"SOURCE : {URL}")
    print(f"SIZE   : {nbytes:,} bytes (~{gb:.2f} GB uncompressed CSV)")
    print(f"COLUMNS: {ncols} source cols -> {len(TABLE_COLS)}-col landing (94, matches {TEMPLATE_TABLE})")
    print(f"EST ROW: {est_rows}")
    print(f"BOUND  : full PY2022, single year only (no 2020/2021). Streamed in {CHUNK:,}-row chunks.")
    if not args.run:
        print("\nPREVIEW only. Add --run to stream + load (snapshot-replace).")
        return 0

    if gb > 12 or nbytes == 0:
        # Hard safety: 2022 should be ~7.4 GB. If it balloons past 12 GB something
        # changed upstream -- stop rather than blow the budget.
        raise SystemExit(f"ABORT: file is {gb:.1f} GB (expected ~7.4) -- refusing to load blind.")

    conn = snow.connect()
    csv_path = SCRATCH / "OP_DTL_GNRL_PGYR2022.csv"
    progress = {"rows": 0}
    try:
        _ensure_table(conn)
        run_id = uuid.uuid4().hex[:16]
        started = ingest._utcnow()
        try:
            print("Downloading to local temp file (bounded memory; decouples net from parse) ...", flush=True)
            dl_bytes = _download_to_disk(csv_path)
            print(f"  downloaded {dl_bytes/1e9:.2f} GB -> {csv_path}", flush=True)
            rows, file_bytes, sha = _stream_load(conn, run_id, csv_path, progress)
        except Exception as ex:
            ended = ingest._utcnow()
            ingest._log_run(conn, SID, run_id, "error", progress["rows"], 0, "", URL,
                            started, ended,
                            f"PY2022 load failed after {progress['rows']:,} rows: "
                            f"{type(ex).__name__}: {str(ex)[:140]}")
            raise
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", rows, file_bytes, sha, URL,
                        started, ended,
                        f"CMS Open Payments PY2022 general-detail: snapshot-replace "
                        f"load of {rows:,} rows into LIBRARY_RAW.LANDING.{TABLE}.")
        _register(conn, rows)

        # Confirm the unlock: PROGRAM_YEAR distribution in the new table.
        cur = conn.cursor()
        cur.execute(f"SELECT PROGRAM_YEAR, COUNT(*) FROM LIBRARY_RAW.LANDING.{TABLE} "
                    f"GROUP BY 1 ORDER BY 1")
        dist = cur.fetchall(); cur.close()
        print(f"\nDONE: {rows:,} rows landed in {TABLE}.")
        print("PROGRAM_YEAR distribution:")
        for yr, c in dist:
            print(f"  {yr}: {c:,}")
        return 0
    finally:
        try:
            if csv_path.exists():
                csv_path.unlink()  # remove the ~7.4 GB temp regardless of outcome
        except Exception:
            pass
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
