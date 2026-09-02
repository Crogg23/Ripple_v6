#!/usr/bin/env python3
"""Load House Statement of Disbursements -- every quarterly DETAIL grid CSV.

One row = one expenditure transaction by a House office (member, committee,
leadership, officer). Vendor name, amount, dates, budget object code. The
House spending on itself -- salaries, travel, catering, consultants.

Source: house.gov SOD pages. The current page holds the latest quarter; the
archive page holds every prior quarter's grid CSV the site still links
(2016 onward as of 2026-09; older quarters exist only as PDF volumes there).
house.gov 403s non-browser agents, so requests carry a browser User-Agent.

Shape: scrape both pages for *DETAIL*GRID*.csv links, download each to temp,
read headers, compute the column union, then stream quarter-by-quarter into
__STAGING (one quarter in memory at a time), atomic swap on full success,
never-shrink floor, INGEST_RUNS logging, registry MERGE. Same guard stack as
scripts/fec_itoth_load.py.

    python scripts/house_disbursements_load.py --max-quarters 2   # smoke (NO swap)
    python scripts/house_disbursements_load.py                     # full load
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import tempfile
import uuid
from html import unescape
from urllib.parse import unquote
from pathlib import Path as _RepoPath

import pandas as pd
import requests

_REPO = _RepoPath(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import ingest    # noqa: E402
import register  # noqa: E402
import snow      # noqa: E402
from config import settings  # noqa: E402
from snowflake.connector.pandas_tools import write_pandas  # noqa: E402

from loadkit import atomic_load  # noqa: E402

SID = "fed_house_disbursements"
TABLE = SID.upper()
STG = atomic_load.staging_name(TABLE)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126"}
PAGES = [
    "https://www.house.gov/the-house-explained/open-government/statement-of-disbursements",
    "https://www.house.gov/the-house-explained/open-government/statement-of-disbursements/archive",
]


def discover_detail_urls() -> list[str]:
    """Every DETAIL grid CSV link on the SOD pages, absolute, deduped, in page order."""
    urls: list[str] = []
    for page in PAGES:
        r = requests.get(page, headers=UA, timeout=120)
        r.raise_for_status()
        for href in re.findall(r'href="([^"]+)"', r.text):
            h = unescape(href)
            # match on the DECODED name (%20 spaces), download the raw href
            if re.search(r"DETAIL[ _-]?GRID[^/]*\.csv$", unquote(h), re.IGNORECASE):
                if h.startswith("/"):
                    h = "https://www.house.gov" + h
                if not h.startswith("http"):
                    raise RuntimeError(f"unexpected relative SOD link shape: {h}")
                if h not in urls:
                    urls.append(h)
    # 42 grids known 2026-09 (2016q1..2026q2); fewer means the pages shrank
    # or the regex went blind -- refuse to quietly land a subset.
    if len(urls) < 40:
        raise RuntimeError(f"only {len(urls)} DETAIL grid links found (expected >=40)")
    return urls


def quarter_label(url: str) -> str:
    """Human quarter tag from the filename, e.g. 'APRIL-JUNE 2026'."""
    name = unquote(unescape(os.path.basename(url)))
    # some filenames lack 'SOD' ('OCT-DEC 2016 DETAIL GRID.csv') -- strip
    # from SOD or DETAIL or SUMM, whichever comes first
    return re.sub(r"[ _-]*(SOD|DETAIL|SUMM).*$", "", name, flags=re.IGNORECASE).strip()


def read_quarter(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, encoding="latin-1", low_memory=False,
                     on_bad_lines="error")
    cols = [re.sub(r"\W+", "_", c.strip().upper()).strip("_") for c in df.columns]
    # trailing-whitespace dirt seen in the live AMOUNT header padding means
    # normalization can COLLIDE two headers ('AMOUNT', 'AMOUNT ') -- reindex
    # on duplicates hard-crashes, so de-dupe with numbered suffixes here.
    seen: dict[str, int] = {}
    uniq = []
    for c in cols:
        seen[c] = seen.get(c, 0) + 1
        uniq.append(c if seen[c] == 1 else f"{c}_{seen[c]}")
    df.columns = uniq
    # trailing commas in some grids create phantom 'Unnamed: N' columns
    return df.drop(columns=[c for c in df.columns if c.startswith("UNNAMED_")])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-quarters", type=int, default=0, help="0 = all quarters")
    args = ap.parse_args(argv)

    urls = discover_detail_urls()
    if args.max_quarters:
        urls = urls[: args.max_quarters]
    print(f"=== House SOD detail load: {len(urls)} quarter files ===", flush=True)

    tmpdir = tempfile.mkdtemp(prefix="sod_")
    paths: list[tuple[str, str]] = []
    for u in urls:
        p = os.path.join(tmpdir, hashlib.sha256(u.encode()).hexdigest()[:16] + ".csv")
        with requests.get(u, headers=UA, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(p, "wb") as f:
                for ch in r.iter_content(1024 * 1024):
                    f.write(ch)
        print(f"  got {quarter_label(u)}: {os.path.getsize(p)/1e6:.1f} MB", flush=True)
        paths.append((u, p))

    # column union first, so every chunk writes the same shape
    union: list[str] = []
    for _u, p in paths:
        for c in read_quarter(p).head(0).columns:
            if c not in union:
                union.append(c)
    union += ["SOD_QUARTER", "SOD_SOURCE_URL"]
    print(f"  column union: {len(union)} cols", flush=True)

    run_id = str(uuid.uuid4())
    started = ingest._utcnow()
    conn = snow.connect()
    total, first = 0, True
    try:
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        for u, p in paths:
            df = read_quarter(p)
            df["SOD_QUARTER"] = quarter_label(u)
            df["SOD_SOURCE_URL"] = u
            df = df.reindex(columns=union)
            out = ingest._stringify(df)
            out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = hashlib.sha256(open(p, "rb").read()).hexdigest()
            out.columns = [ingest._sf_col(c) for c in out.columns]
            ok, _c, _r, _ = write_pandas(
                conn, out, table_name=STG, database=settings.raw_database,
                schema=settings.raw_schema, auto_create_table=True,
                overwrite=first, quote_identifiers=False,
            )
            if not ok:
                raise RuntimeError(f"write_pandas failed on {u}")
            total += len(df)
            first = False
            print(f"  landed {quarter_label(u)}: {len(df):,} rows (total {total:,})", flush=True)

        ended = ingest._utcnow()
        if args.max_quarters:
            ingest._log_run(conn, SID, run_id, "smoke", total, None, "", PAGES[0], started, ended,
                            f"--max-quarters={args.max_quarters} smoke: {total:,} rows in "
                            f"LIBRARY_RAW.LANDING.{STG}; live {TABLE} untouched, NO swap.")
            print(f"\nSMOKE -> {total:,} rows in staging; live untouched (no swap)", flush=True)
            return 0

        prev = ingest._latest_success_rows(conn, SID)
        if prev and total < prev * 0.98:
            ingest._log_run(conn, SID, run_id, "partial", total, None, "", PAGES[0], started, ended,
                            f"PARTIAL -- {total:,} < never-shrink floor {int(prev*0.98):,} "
                            f"(prev {prev:,}). Live {TABLE} LEFT UNTOUCHED.")
            print(f"\nREFUSED SWAP -> {total:,} < floor {int(prev*0.98):,}", flush=True)
            return 1

        atomic_load.execute_swap(conn, TABLE, database=settings.raw_database, schema=settings.raw_schema)
        ingest._log_run(conn, SID, run_id, "success", total, None, "", PAGES[0], started, ended,
                        f"SOD detail grids, {len(paths)} quarters, {total:,} rows.")
        cfg = {
            "source_id": SID,
            "name": "House Statement of Disbursements (detail)",
            "publisher": "U.S. House of Representatives, Chief Administrative Officer",
            "url": PAGES[0],
            "description": "Quarterly line-item spending by every House office -- members, "
                           "committees, leadership, officers. Vendor, amount, dates, budget "
                           "object code. Every grid CSV the site links (2016 onward; "
                           "older quarters are PDF-only there).",
            "jurisdiction": "federal", "category": "Government spending",
            "subcategory": "Legislative branch expenditures",
            "unit_of_observation": "one row = one expenditure transaction",
            "geographic_scope": "US", "access_method": "bulk_download", "format": "csv",
            "auth": {"type": "none"}, "cost": "free", "update_cadence": "quarterly",
            "volume": "roughly 100-140K transactions per quarter, ~10 years of quarters",
            "license_terms": "public domain",
            "join_keys": "candidates only, unverified: VENDOR_NAME, ORGANIZATION",
            "accountability_relevance": "Congress's own spending: consultants, travel, "
                                        "vendors paid by member offices.",
            "priority_tier": "2", "landing_table": TABLE,
            "notes": "Loaded by scripts/house_disbursements_load.py (all-quarters "
                     "snapshot-replace, atomic swap, never-shrink).",
        }
        snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))
        print(f"\nDONE -> LIBRARY_RAW.LANDING.{TABLE}: {total:,} rows, "
              f"{len(paths)} quarters; registered INCLUDE=Y", flush=True)
    except Exception as exc:
        try:
            ingest._log_run(conn, SID, run_id, "failed", total, None, "", PAGES[0],
                            started, ingest._utcnow(),
                            f"SOD load FAILED after {total:,} rows (staging only): {str(exc)[:500]}")
        except Exception:
            pass
        raise
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
