#!/usr/bin/env python3
"""Stream-load FEC itoth -- committee-to-committee transactions -- cycles
2024 + 2026. Found missing 2026-09-01: itcont and itpas2 landed, itoth landed
nowhere (proven by transaction-type census: no 16C/16F/18G/18J/24A/24E codes
in the account).

WHAT THE TABLE ACTUALLY HOLDS (skeptic census, 2026-09-01): 93% is 15J --
individual earmark MEMO rows flowing through conduits (ActBlue/WinRed),
MEMO_CD='X' = FEC's own "already counted elsewhere" flag. The true PAC-to-PAC
transfer layer is the ~1.9M non-15J rows (24K/18K/24E/18G/16C...), where
OTHER_ID is 99.95% populated. NEVER sum this table with itcont without
filtering MEMO_CD <> 'X' -- the same earmarked dollar appears in both, with
different CMTE_IDs and different SUB_IDs, so no dedup will catch it.

Same 21-column pipe layout as itcont; same bounded-memory stream shape as
scripts/fec_itcont_load.py: zip to disk, stream line-by-line, chunked
write_pandas into __STAGING, atomic swap only on full success, never-shrink
floor before the swap, fail-loud parse with quarantine.

  python scripts/fec_itoth_load.py --max-rows 200000   # capped smoke (NO swap)
  python scripts/fec_itoth_load.py                      # full load
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

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import ingest  # noqa: E402
import snow    # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

from loadkit import atomic_load, fec_parse  # noqa: E402

# Identical layout to itcont (fec.gov "Any transaction from one committee to
# another" file description) -- NAME here is the contributor committee's name.
ITOTH_COLS = [
    "CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM", "TRANSACTION_TP",
    "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE", "EMPLOYER", "OCCUPATION",
    "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID", "TRAN_ID", "FILE_NUM",
    "MEMO_CD", "MEMO_TEXT", "SUB_ID",
]
CYCLES = {"2024": "24", "2026": "26"}
SID = "fed_fec_committee_to_committee"
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
    txts = [n for n in zf.namelist() if n.lower().endswith(".txt")]
    if len(txts) != 1:
        # one-member rule (zip largest-member trap, 2026-08 review): refuse to
        # guess which member is the data rather than silently pick one.
        raise RuntimeError(f"expected exactly one .txt in {zip_path}, got {txts}")
    with zf.open(txts[0]) as raw:
        for line in io.TextIOWrapper(raw, encoding="latin-1"):
            yield line.rstrip("\n")


def write_chunk(conn, lines, run_id, started, first: bool) -> tuple[int, int]:
    res = fec_parse.parse_pipe("\n".join(lines), ITOTH_COLS).require_clean(0.005)
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
    print(f"=== FEC itoth stream-load (cycles {'+'.join(CYCLES)}; cap={args.max_rows or 'none'}) ===", flush=True)
    try:
        for cyc, yy in CYCLES.items():
            url = f"https://www.fec.gov/files/bulk-downloads/{cyc}/oth{yy}.zip"
            zpath = os.path.join(tempfile.gettempdir(), f"oth{yy}.zip")
            zips.append(zpath)
            download(url, zpath)
            print(f"  streaming oth{yy} ...", flush=True)
            buf = []
            for line in stream_lines(zpath):
                if not line.strip():
                    continue
                buf.append(line)
                # honor the cap exactly: trim the buffer so a smoke run lands
                # at most --max-rows, not the next full CHUNK (2.5x overshoot
                # caught by skeptic 2026-09-01)
                if args.max_rows and total + len(buf) >= args.max_rows:
                    buf = buf[: args.max_rows - total]
                    n, b = write_chunk(conn, buf, run_id, started, first)
                    total += n; bad += b; first = False; buf = []
                    print(f"    landed {total:,} rows (quarantined {bad})", flush=True)
                    break
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

        ended = ingest._utcnow()
        if args.max_rows:
            # SMOKE RUN: capped stream = partial staging table; never swap it
            # over live. Logged status='smoke' so INGEST_RUNS 'success'
            # consumers never mistake it for a real load.
            ingest._log_run(conn, SID, run_id, "smoke", total, None, "",
                            "https://www.fec.gov/files/bulk-downloads/", started, ended,
                            f"--max-rows={args.max_rows} smoke: {total:,} rows landed in "
                            f"LIBRARY_RAW.LANDING.{STG} (quarantined {bad}); live {TABLE} "
                            "untouched, NO swap performed.")
            print(f"\nSMOKE -> {total:,} rows in LIBRARY_RAW.LANDING.{STG}; "
                  f"live {TABLE} untouched (no swap on a capped run)", flush=True)
            return 0

        # Never-shrink floor -- same guard as itcont: a near-empty stream must
        # not swap over a previously healthy table.
        prev = ingest._latest_success_rows(conn, SID)
        if prev and total < prev * 0.5:
            ended = ingest._utcnow()
            ingest._log_run(conn, SID, run_id, "partial", total, None, "",
                            "https://www.fec.gov/files/bulk-downloads/", started, ended,
                            f"PARTIAL -- {total:,} rows is below the never-shrink floor "
                            f"({prev:,} last success x 0.5 = {int(prev*0.5):,}). Live {TABLE} "
                            f"LEFT UNTOUCHED (staging {STG} kept for inspection, quarantined {bad}).")
            print(f"\nREFUSED SWAP -> {total:,} rows < floor {int(prev*0.5):,} (prev success {prev:,}) "
                  f"-- live {TABLE} untouched, staging kept", flush=True)
            return 1

        atomic_load.execute_swap(conn, TABLE, database=settings.raw_database, schema=settings.raw_schema)
        ingest._log_run(conn, SID, run_id, "success", total, None, "",
                        "https://www.fec.gov/files/bulk-downloads/", started, ended,
                        f"itoth streamed {total:,} rows (quarantined {bad}); cycles {'+'.join(CYCLES)}.")
        print(f"\nDONE -> LIBRARY_RAW.LANDING.{TABLE}: {total:,} rows (quarantined {bad})", flush=True)
    except Exception as exc:
        # A crashed run must leave an INGEST_RUNS trace; live is safe either way
        # (only __STAGING is ever written), so log 'failed' and re-raise.
        try:
            ingest._log_run(conn, SID, run_id, "failed", total, None, "",
                            "https://www.fec.gov/files/bulk-downloads/", started, ingest._utcnow(),
                            f"itoth load FAILED after {total:,} rows (staging only, live "
                            f"{TABLE} untouched): {str(exc)[:500]}")
        except Exception:
            pass  # logging must never mask the original error
        raise
    finally:
        conn.close()
        if not args.max_rows:
            for z in zips:
                try:
                    os.remove(z)
                except OSError:
                    pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
