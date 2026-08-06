"""FracFocus bulk CSV loader -- DisclosureList (wells) + FracFocusRegistry
(per-chemical disclosure rows, split across 15 files) from the bulk zip.

Zip already downloaded to outputs/_fracfocus.zip (fracfocusdata.org 403s
plain curl-style requests without a browser User-Agent; requests with a
UA header works fine -- noting as a new fetch trap).
"""
from __future__ import annotations
import datetime as dt
import hashlib
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import ingest  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

ZIP_PATH = _REPO / "outputs" / "_fracfocus.zip"


def load_csv_group(conn, zf, names: list[str], table: str, source_id: str, url: str):
    from snowflake.connector.pandas_tools import write_pandas
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    total = 0
    sha_all = hashlib.sha256()
    first = True
    for name in names:
        with zf.open(name) as f:
            data = f.read()
        sha_all.update(data)
        import io
        for chunk in pd.read_csv(io.BytesIO(data), dtype=str, chunksize=200_000,
                                  encoding_errors="replace", low_memory=False):
            chunk.columns = [ingest._sf_col(c) for c in chunk.columns]
            chunk["_INGESTED_AT"] = started.isoformat()
            chunk["_SOURCE_RUN_ID"] = run_id
            chunk["_SRC_FILE"] = name
            ok, _c, n, _ = write_pandas(
                conn, chunk, table_name=table,
                database="LIBRARY_RAW", schema="LANDING",
                auto_create_table=first, overwrite=first, quote_identifiers=False,
            )
            first = False
            total += n
        print(f"  {name}: cumulative {total:,}")

    sha = sha_all.hexdigest()
    cur = conn.cursor()
    cur.execute(f'SELECT COUNT(*) FROM LIBRARY_RAW.LANDING."{table}"')
    final_count = cur.fetchone()[0]
    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)

    # Quality gate (audit 2026-08-05/06 finding: none here at all -- this
    # chunked loader can't check density before writing since chunks stream in,
    # so it checks the live landed table right after, like assess_bulk_load's
    # other callers in this file's sibling module).
    passed, report = bulk.assess_bulk_load(conn, table)
    status = "success" if passed else "partial"
    if not passed:
        print(f"  QUALITY GATE FAILED for {table}: {report}")

    ingest._log_run(conn, source_id=source_id, run_id=run_id,
                     status=status, row_count=final_count, file_bytes=None,
                     sha=sha, url=url, started=started, ended=ended,
                     message=f"{len(names)} source files")
    print(f"{table}: FINAL {final_count:,} rows (status={status})")
    if not passed:
        raise RuntimeError(f"QUALITY GATE FAILED for {table}: {report}")
    return final_count


def main():
    conn = snow.connect()
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
        disclosure_files = sorted(n for n in names if n.startswith("DisclosureList"))
        registry_files = sorted(n for n in names if n.startswith("FracFocusRegistry"))
        water_files = sorted(n for n in names if n.startswith("WaterSource"))

        print("Loading DisclosureList (well-level)...")
        load_csv_group(conn, zf, disclosure_files, "FED_FRACFOCUS_DISCLOSURE_LIST",
                        "fed_fracfocus_disclosure_list",
                        "https://www.fracfocusdata.org/digitaldownload/fracfocuscsv.zip")

        print("Loading WaterSource...")
        load_csv_group(conn, zf, water_files, "FED_FRACFOCUS_WATER_SOURCE",
                        "fed_fracfocus_water_source",
                        "https://www.fracfocusdata.org/digitaldownload/fracfocuscsv.zip")

        print("Loading FracFocusRegistry (chemical-level, 15 files)...")
        load_csv_group(conn, zf, registry_files, "FED_FRACFOCUS_REGISTRY",
                        "fed_fracfocus_registry",
                        "https://www.fracfocusdata.org/digitaldownload/fracfocuscsv.zip")


if __name__ == "__main__":
    main()
