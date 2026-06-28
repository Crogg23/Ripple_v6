#!/usr/bin/env python3
"""Quarterly backfill for SEC EDGAR Financial Statement Data Sets -- submissions
(discovery sweep Phase 3 #42: FED_SEC_EDGAR_FINANCIALS is ONE quarter's sub.txt --
6,491 rows == 2024q4 exactly. "Looks like a panel, is a snapshot." Each extra
quarter turns the single-quarter submissions snapshot into a real filing time
series (distinct fiscal periods + filing dates across multiple quarters), which is
what lets the SEC <-> CIK/EIN bridge see how filers and financials move over time.

Source: SEC DERA Financial Statement Data Sets
  https://www.sec.gov/files/dera/data/financial-statement-data-sets/<YYYY>q<N>.zip
Each zip holds sub.txt / num.txt / tag.txt / pre.txt. The landing table mirrors
sub.txt (the 36 submission columns adsh..aciks), so this extracts ONLY sub.txt,
ignoring the big num.txt (527 MB) we don't land. sub.txt is tiny (~2 MB / ~6-7K
rows per quarter), so the whole 8-quarter window is ~50K rows -- a cheap load --
but we still STREAM each zip to disk and read sub.txt in CHUNKS to match the
template pattern and stay memory-safe.

BOUNDED to the last 8 quarters: 2023q1 .. 2024q4.

Idempotency: a SOURCE_FILE column (the quarter id, e.g. "2024q4") is added to the
table; any quarter already present in SOURCE_FILE is skipped. The pre-existing
6,491-row run (no SOURCE_FILE) is the 2024q4 snapshot -- it is tagged "2024q4" once
on first run so it is neither duplicated nor lost.

    python3 scripts/sec_edgar_financials_backfill.py                       # preview all 8
    python3 scripts/sec_edgar_financials_backfill.py --quarters 2023q1 2023q2
    python3 scripts/sec_edgar_financials_backfill.py --run                 # land the window

SEC requires a descriptive User-Agent or it 403s.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
import zipfile
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

TABLE = "FED_SEC_EDGAR_FINANCIALS"
SID = "fed_sec_edgar_financials"
UA = {"User-Agent": "Ripple-Library w.rogers9999@gmail.com"}
CHUNK = 250_000
SCRATCH = Path("/private/tmp/claude-501/-Users-chrisr--Documents-GitHub-Ripple-v6/"
               "e8eac5fb-de36-4362-9440-da24a904b9b4/scratchpad")

# the 36 sub.txt columns, in file order == landing column order (UPPER).
SUB_COLS = [
    "ADSH", "CIK", "NAME", "SIC", "COUNTRYBA", "STPRBA", "CITYBA", "ZIPBA",
    "BAS1", "BAS2", "BAPH", "COUNTRYMA", "STPRMA", "CITYMA", "ZIPMA", "MAS1",
    "MAS2", "COUNTRYINC", "STPRINC", "EIN", "FORMER", "CHANGED", "AFS", "WKSI",
    "FYE", "FORM", "PERIOD", "FY", "FP", "FILED", "ACCEPTED", "PREVRPT",
    "DETAIL", "INSTANCE", "NCIKS", "ACIKS",
]
TABLE_COLS = SUB_COLS + ["SOURCE_FILE",
                         "_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"]

# the bounded window: last 8 quarters
DEFAULT_QUARTERS = ["2023q1", "2023q2", "2023q3", "2023q4",
                    "2024q1", "2024q2", "2024q3", "2024q4"]


def _url(q: str) -> str:
    return f"https://www.sec.gov/files/dera/data/financial-statement-data-sets/{q}.zip"


def _ensure_source_file_col(conn) -> None:
    """Add SOURCE_FILE (idempotency key) if absent, and tag the legacy 2024q4
    snapshot rows (NULL SOURCE_FILE) so they are not re-loaded."""
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME=%s AND COLUMN_NAME='SOURCE_FILE'",
            (TABLE,),
        )
        has_col = cur.fetchone()[0] > 0
        if not has_col:
            cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{TABLE} ADD COLUMN SOURCE_FILE VARCHAR")
            # the pre-existing 6,491 rows are the 2024q4 sub.txt snapshot -> tag them
            cur.execute(
                f"UPDATE LIBRARY_RAW.LANDING.{TABLE} SET SOURCE_FILE='2024q4' "
                f"WHERE SOURCE_FILE IS NULL"
            )
            print("  + added SOURCE_FILE column; tagged legacy snapshot rows as '2024q4'")
    finally:
        cur.close()


def _already_loaded(conn) -> set[str]:
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT DISTINCT SOURCE_FILE FROM LIBRARY_RAW.LANDING.{TABLE}")
        return {r[0] for r in cur.fetchall() if r[0]}
    finally:
        cur.close()


def _load_quarter(conn, q: str, run_id: str) -> tuple[bool, str]:
    url = _url(q)
    tmp = SCRATCH / f"sec_{q}.zip"
    try:
        # stream the whole zip to disk (avoid holding 120MB in memory)
        with requests.get(url, headers=UA, timeout=600, stream=True) as r:
            if r.status_code != 200:
                return False, f"HTTP {r.status_code}"
            with open(tmp, "wb") as fh:
                for c in r.iter_content(1 << 20):
                    fh.write(c)
        sha = hashlib.sha256(tmp.read_bytes()).hexdigest()
        started = ingest._utcnow()
        appended = 0
        zf = zipfile.ZipFile(tmp)
        if "sub.txt" not in zf.namelist():
            return False, "no sub.txt in zip"
        with zf.open("sub.txt") as fh:
            # sub.txt is tab-separated; read as TEXT in chunks (memory-safe template)
            for chunk in pd.read_csv(fh, sep="\t", dtype=str, keep_default_na=False,
                                     low_memory=False, chunksize=CHUNK,
                                     quoting=3, on_bad_lines="warn"):
                # normalize headers to UPPER landing names
                chunk.columns = [str(c).upper() for c in chunk.columns]
                for c in SUB_COLS:
                    if c not in chunk.columns:
                        chunk[c] = ""
                out = chunk[SUB_COLS].copy()
                out["SOURCE_FILE"] = q
                out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
                out[ingest.META_SOURCE_RUN_ID] = run_id
                out[ingest.META_SRC_SHA256] = sha
                out = out[TABLE_COLS]
                ok, _c, n, _ = write_pandas(
                    conn, out, table_name=TABLE,
                    database=settings.raw_database, schema=settings.raw_schema,
                    auto_create_table=False, overwrite=False, quote_identifiers=False)
                if not ok:
                    return False, f"write_pandas failed after {appended:,}"
                appended += len(out)
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", appended, tmp.stat().st_size, sha, url,
                        started, ended, f"SEC EDGAR sub.txt backfill {q}: appended {appended:,} rows")
        return True, f"appended {appended:,} rows"
    except Exception as ex:  # noqa: BLE001
        return False, f"{type(ex).__name__}: {str(ex)[:160]}"
    finally:
        try:
            tmp.unlink()
        except Exception:
            pass


def _reregister(conn) -> None:
    """Refresh the registry row -- best effort, never fatal."""
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT SOURCE_FILE) FROM LIBRARY_RAW.LANDING.{TABLE}")
        n, nq = cur.fetchone()
        cur.close()
        config = {
            "source_id": SID,
            "name": "SEC EDGAR Financial Statement Data Sets (submissions)",
            "url": "https://www.sec.gov/dera/data/financial-statement-data-sets",
            "publisher": "U.S. Securities and Exchange Commission (DERA)",
            "jurisdiction": "US-Federal",
            "category": "money_finance",
            "access_method": "bulk_zip",
            "format": "tsv",
            "auth": {"type": "none"},
            "cost": "free",
            "update_cadence": "quarterly",
            "join_keys": "CIK,EIN,SIC,ADSH",
            "notes": f"sub.txt (submission index) per quarter. Backfilled to {nq} quarters / "
                     f"{n:,} rows (2023q1..2024q4). num/tag/pre.txt not landed.",
        }
        row = register._build_row(config, {})
        sql = register._merge_sql(row)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        print("  + registry row refreshed")
    except Exception as ex:  # noqa: BLE001
        print(f"  ! registry refresh skipped: {type(ex).__name__}: {str(ex)[:120]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Quarterly SEC EDGAR sub.txt backfill (append).")
    ap.add_argument("--quarters", nargs="*", help="explicit YYYYqN quarters (default: last 8)")
    ap.add_argument("--run", action="store_true", help="download + append (else preview)")
    args = ap.parse_args()
    quarters = args.quarters or DEFAULT_QUARTERS

    conn = snow.connect()
    try:
        _ensure_source_file_col(conn)
        loaded = _already_loaded(conn)
        todo = [q for q in quarters if q not in loaded]
        skip = [q for q in quarters if q in loaded]
        print(f"SEC EDGAR backfill: {len(quarters)} quarter(s) requested; "
              f"{len(skip)} already loaded; {len(todo)} to load.")
        for q in skip:
            print(f"  - {q}  already in table (SOURCE_FILE present) -- skip")
        if not args.run:
            for q in todo:
                print(f"  + {q}  {_url(q)}")
            print(f"\nPREVIEW only. sub.txt is ~6-7K rows/quarter (~2 MB inner file; "
                  f"zip ~115-125 MB). Add --run to load {len(todo)} quarter(s).")
            return 0
        run_id = uuid.uuid4().hex[:16]
        ok = fail = 0
        for q in todo:
            good, msg = _load_quarter(conn, q, run_id)
            print(f"  {'OK' if good else 'XX'} {q}  {msg}", flush=True)
            ok += good
            fail += (not good)
        cur = conn.cursor()
        cur.execute(
            f"SELECT COUNT(*), COUNT(DISTINCT SOURCE_FILE), "
            f"COUNT(DISTINCT FY||'-'||FP) FROM LIBRARY_RAW.LANDING.{TABLE}")
        n, nq, nfyfp = cur.fetchone()
        cur.close()
        _reregister(conn)
        print(f"\nDONE: {ok} quarter(s) loaded, {fail} failed. {TABLE} now holds {n:,} rows "
              f"across {nq} source quarter(s) / {nfyfp} distinct FY-FP combos.")
        return 0 if fail == 0 else 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
