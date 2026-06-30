#!/usr/bin/env python3
"""Stream-load FEC itcont -- itemized individual contributions, the ~70M-row donor
firehose -- cycles 2024 + 2026. BOUNDED MEMORY: download the zip to disk, stream the
inner member line-by-line, parse + write in chunks (never the whole file in RAM, so
build_money_spine's whole-file OOM can't happen).

Lands to a STAGING table; atomic-swaps to live only on FULL success (loadkit.
atomic_load), so a crash leaves the live table untouched and nothing to clean up.
Parsing is fail-loud (loadkit.fec_parse): a row whose embedded pipe shifts the
columns is quarantined, never landed mis-shaped.

  python scripts/fec_itcont_load.py --max-rows 500000   # capped smoke
  python scripts/fec_itcont_load.py                      # full load (hours)
"""
from __future__ import annotations

import argparse
import hashlib
import io
import os
import sys
import tempfile
import uuid
import zipfile

import requests

sys.path.insert(0, r"c:\Code\Ripple_v6")
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")

from dotenv import load_dotenv  # noqa: E402

load_dotenv(r"c:\Code\Ripple_v6\library-onboarding\.env", override=True)

import ingest  # noqa: E402
import snow    # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

from loadkit import atomic_load, fec_parse  # noqa: E402

ITCONT_COLS = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM", "TRANSACTION_TP",
    "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE", "EMPLOYER", "OCCUPATION",
    "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID", "TRAN_ID", "FILE_NUM",
    "MEMO_CD", "MEMO_TEXT", "SUB_ID",
]
CYCLES = {"2024": "24", "2026": "26"}
SID = "fed_fec_indiv_contributions"
TABLE = SID.upper()
STG = atomic_load.staging_name(TABLE)
CHUNK = 500_000


def download(url: str, path: str) -> None:
    if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
        print(f"  reuse cached {path} ({os.path.getsize(path)/1e9:.2f} GB)", flush=True)
        return
    print(f"  downloading {url} ...", flush=True)
    with requests.get(url, stream=True, timeout=1200) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for ch in r.iter_content(1024 * 1024):
                f.write(ch)
    print(f"  downloaded {os.path.getsize(path)/1e9:.2f} GB", flush=True)


def stream_lines(zip_path: str):
    zf = zipfile.ZipFile(zip_path)
    name = [n for n in zf.namelist() if n.lower().endswith(".txt")][0]
    with zf.open(name) as raw:
        for line in io.TextIOWrapper(raw, encoding="latin-1"):
            yield line.rstrip("\n")


def write_chunk(conn, lines, run_id, started, first: bool) -> tuple[int, int]:
    res = fec_parse.parse_pipe("\n".join(lines), ITCONT_COLS).require_clean(0.005)
    out = ingest._stringify(res.good)
    out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    out[ingest.META_SOURCE_RUN_ID] = run_id
    out[ingest.META_SRC_SHA256] = hashlib.sha256("\n".join(lines).encode("latin-1")).hexdigest()
    out.columns = [ingest._sf_col(c) for c in out.columns]  # reserved-word guard
    ok, _c, _r, _ = write_pandas(
        conn, out, table_name=STG, database=settings.raw_database, schema=settings.raw_schema,
        auto_create_table=True, overwrite=first, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError("write_pandas failed on a chunk")
    return len(res.good), res.n_bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-rows", type=int, default=0, help="0 = full load")
    args = ap.parse_args(argv)

    run_id = str(uuid.uuid4())
    started = ingest._utcnow()
    conn = snow.connect()
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
    total, bad, first, zips = 0, 0, True, []
    print(f"=== FEC itcont stream-load (cycles {'+'.join(CYCLES)}; cap={args.max_rows or 'none'}) ===", flush=True)
    try:
        for cyc, yy in CYCLES.items():
            url = f"https://www.fec.gov/files/bulk-downloads/{cyc}/indiv{yy}.zip"
            zpath = os.path.join(tempfile.gettempdir(), f"indiv{yy}.zip")
            zips.append(zpath)
            download(url, zpath)
            print(f"  streaming indiv{yy} ...", flush=True)
            buf = []
            for line in stream_lines(zpath):
                if not line.strip():
                    continue
                buf.append(line)
                if len(buf) >= CHUNK:
                    n, b = write_chunk(conn, buf, run_id, started, first)
                    total += n; bad += b; first = False; buf = []
                    print(f"    landed {total:,} rows (quarantined {bad})", flush=True)
                    if args.max_rows and total >= args.max_rows:
                        break
            if buf and not (args.max_rows and total >= args.max_rows):
                n, b = write_chunk(conn, buf, run_id, started, first)
                total += n; bad += b; first = False
                print(f"    landed {total:,} rows (quarantined {bad})", flush=True)
            if args.max_rows and total >= args.max_rows:
                break

        atomic_load.execute_swap(conn, TABLE, database=settings.raw_database, schema=settings.raw_schema)
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", total, None, "",
                        "https://www.fec.gov/files/bulk-downloads/", started, ended,
                        f"itcont streamed {total:,} rows (quarantined {bad}); cycles {'+'.join(CYCLES)}.")
        print(f"\nDONE -> LIBRARY_RAW.LANDING.{TABLE}: {total:,} rows (quarantined {bad})", flush=True)
    finally:
        conn.close()
        if not args.max_rows:                      # keep the cached zips for a capped smoke; clean after a full run
            for z in zips:
                try:
                    os.remove(z)
                except OSError:
                    pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
