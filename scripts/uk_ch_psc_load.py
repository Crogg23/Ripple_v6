#!/usr/bin/env python3
"""Deterministic loader for UK Companies House PSC (Persons with Significant Control) snapshot.

Distinct product from the existing basic company-data extract (int_uk_companies_house /
corporate_registry__intl_uk_companies_house) -- this is the beneficial-ownership layer.
Published as a chunked snapshot at download.companieshouse.gov.uk (see en_pscdata.html),
one JSON-lines .txt per chunk inside a per-chunk zip, ~32 chunks, ~10M PSC records total.

Given the size, this loader supports --chunks N to bound how many of the 32 chunks it
pulls in one run (checkpointed: each chunk downloads, flattens, and APPENDS to the RAW
table before moving to the next, so a partial run leaves a valid partial table rather
than nothing). Rerun with a higher --chunks (or --start-chunk) to keep going; this script
does NOT dedupe on rerun (append-only) -- track completed chunk numbers in the printed
receipt and don't reload a chunk twice in one "session" of building the full table.

    python scripts/uk_ch_psc_load.py --list                      # show available chunk URLs
    python scripts/uk_ch_psc_load.py --chunks 1 --run             # land chunk 1 only (preview if no --run)
    python scripts/uk_ch_psc_load.py --start-chunk 2 --chunks 5 --run   # land chunks 2-6
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
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

SID = "corporate_registry_uk_companies_house_psc"
TABLE = "UK_COMPANIES_HOUSE_PSC"
LIST_URL = "http://download.companieshouse.gov.uk/en_pscdata.html"
DOWNLOAD_DIR = _LIB / "ch_psc"


def _list_chunk_urls() -> list[str]:
    r = requests.get(LIST_URL, timeout=30)
    r.raise_for_status()
    files = re.findall(r'href="(psc-snapshot-[^"]+\.zip)"', r.text)
    # keep numeric order 1of32, 2of32, ...
    def key(f):
        m = re.search(r"_(\d+)of(\d+)\.zip", f)
        return int(m.group(1)) if m else 0
    files = sorted(set(files), key=key)
    return [f"https://download.companieshouse.gov.uk/{f}" for f in files]


def _flatten(rec: dict) -> dict:
    d = rec.get("data", {}) or {}
    addr = d.get("address", {}) or {}
    dob = d.get("date_of_birth", {}) or {}
    return {
        "COMPANY_NUMBER": rec.get("company_number", ""),
        "PSC_KIND": d.get("kind", ""),
        "PSC_NAME": d.get("name", ""),
        "PSC_LINK": (d.get("links", {}) or {}).get("self", ""),
        "NATURES_OF_CONTROL": "; ".join(d.get("natures_of_control", []) or []),
        "NOTIFIED_ON": d.get("notified_on", ""),
        "CEASED_ON": d.get("ceased_on", ""),
        "NATIONALITY": d.get("nationality", ""),
        "COUNTRY_OF_RESIDENCE": d.get("country_of_residence", ""),
        "DOB_MONTH": dob.get("month", ""),
        "DOB_YEAR": dob.get("year", ""),
        "ADDRESS_PREMISES": addr.get("premises", ""),
        "ADDRESS_LINE_1": addr.get("address_line_1", ""),
        "ADDRESS_LOCALITY": addr.get("locality", ""),
        "ADDRESS_POSTAL_CODE": addr.get("postal_code", ""),
        "ADDRESS_COUNTRY": addr.get("country", ""),
        "REG_COUNTRY": (d.get("identification", {}) or {}).get("country_registered", ""),
        "REG_NUMBER": (d.get("identification", {}) or {}).get("registration_number", ""),
        "REG_LEGAL_FORM": (d.get("identification", {}) or {}).get("legal_form", ""),
        "ETAG": d.get("etag", ""),
    }


def _register(conn, rows: int, chunks_done: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "UK Companies House PSC (Persons with Significant Control) Snapshot",
        "publisher": "UK Companies House",
        "url": "http://download.companieshouse.gov.uk/en_pscdata.html",
        "description": "Beneficial-ownership layer for UK companies -- who actually controls each "
                       "company (25%+ shares/votes, or other significant control), separate from the "
                       "basic company-data extract already landed. One row per PSC-per-company. "
                       f"{chunks_done} of 32 published chunks loaded so far.",
        "jurisdiction": "UK", "category": "Corporate/Offshore", "subcategory": "Beneficial Ownership",
        "unit_of_observation": "one row = one person/entity with significant control of one company",
        "geographic_scope": "United Kingdom", "access_method": "bulk_download", "format": "json (chunked zips)",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "monthly snapshot",
        "volume": f"{rows:,} rows (partial: {chunks_done}/32 chunks)" if chunks_done < 32 else f"{rows:,} rows",
        "license_terms": "Open Government Licence v3.0",
        "join_keys": "COMPANY_NUMBER (joins to basic Companies House extract), PSC_NAME",
        "accountability_relevance": "Entity spine block (Phase 5): the actual beneficial-ownership "
                                    "layer for UK companies -- separate product from the basic extract.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": f"Loaded by scripts/uk_ch_psc_load.py; chunked snapshot, {chunks_done}/32 chunks "
                 "landed as of this run. Distinct from int_uk_companies_house (basic extract, no PSC data).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for UK Companies House PSC snapshot")
    ap.add_argument("--list", action="store_true", help="print chunk URLs and exit")
    ap.add_argument("--start-chunk", type=int, default=1)
    ap.add_argument("--chunks", type=int, default=1, help="how many chunks to process this run")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    urls = _list_chunk_urls()
    print(f"=== UK Companies House PSC snapshot: {len(urls)} chunks available ===", flush=True)
    if args.list:
        for u in urls:
            print(u)
        return 0

    DOWNLOAD_DIR.mkdir(exist_ok=True)
    sel = urls[args.start_chunk - 1: args.start_chunk - 1 + args.chunks]
    conn = snow.connect() if args.run else None
    total_landed = 0
    try:
        for i, url in enumerate(sel, start=args.start_chunk):
            print(f"\n-- chunk {i}/{len(urls)}: {url} --", flush=True)
            zpath = DOWNLOAD_DIR / f"chunk{i}.zip"
            if not zpath.exists():
                r = requests.get(url, timeout=600)
                r.raise_for_status()
                zpath.write_bytes(r.content)
            with zipfile.ZipFile(zpath) as z:
                inner_name = z.namelist()[0]
                txt_path = DOWNLOAD_DIR / inner_name
                if not txt_path.exists():
                    z.extractall(DOWNLOAD_DIR)

            rows = []
            with open(txt_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rows.append(_flatten(json.loads(line)))
                    except json.JSONDecodeError:
                        continue
            df = pd.DataFrame(rows)
            print(f"chunk {i}: {len(df):,} PSC records, distinct COMPANY_NUMBER={df['COMPANY_NUMBER'].nunique():,}", flush=True)

            if not args.run:
                print(df.head(3).to_string())
                continue

            started = ingest._utcnow()
            run_id = str(uuid.uuid4())
            sha = hashlib.sha256(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()
            from snowflake.connector.pandas_tools import write_pandas
            snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
            out = ingest._stringify(df)
            out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = sha
            out.columns = [ingest._sf_col(c) for c in out.columns]
            # first chunk overall creates/replaces; subsequent chunks in this run append
            overwrite = (i == 1) and not snow.fetch_scalar(
                conn, f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{settings.raw_schema.upper()}' AND TABLE_NAME='{TABLE}'")
            ok, _c, nrows, _ = write_pandas(conn, out, table_name=TABLE,
                                            database=settings.raw_database, schema=settings.raw_schema,
                                            auto_create_table=True, overwrite=bool(overwrite), quote_identifiers=False)
            if not ok:
                raise RuntimeError("write_pandas failed")
            ended = ingest._utcnow()
            dens = ingest.assess_density(df)
            status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
            ingest._log_run(conn, SID, run_id, status, len(df), None, sha, url, started, ended,
                            f"CH PSC chunk {i}/{len(urls)}; {len(df):,} rows")
            total_landed += len(df)
            print(f"LOADED chunk {i}: {len(df):,} rows (status={status})", flush=True)
    finally:
        if conn:
            n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
            d = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT COMPANY_NUMBER) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
            print(f"\nTABLE TOTAL: {n:,} rows, distinct COMPANY_NUMBER={d:,}", flush=True)
            _register(conn, n, args.start_chunk - 1 + len(sel))
            conn.close()

    if not args.run:
        print("\nPREVIEW only -- add --run to land.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
