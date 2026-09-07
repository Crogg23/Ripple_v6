#!/usr/bin/env python3
"""Scrape Senate Periodic Transaction Reports from efdsearch, 2021 to now.

FINANCE__FED_SENATE_STOCK_WATCHER stops dead at 2020-12-02, 8,350 rows. It was
fed by a third-party mirror that stopped publishing. This goes to the source.

THE SEQUENCE, verified live 2026-09-06:

  1. GET  /search/home/                     sets a csrftoken cookie
  2. POST /search/home/  prohibition_agreement=1 + that token
                                            the "I agree" gate; skip it and
                                            every later call returns the
                                            agreement page instead of data
  3. POST /search/report/data/              DataTables, one call per year,
                                            report_types=[11] is the PTR
  4. GET  each filing link out of column 3

MEASURED, not assumed:

  799 PTR filings across 2021-2026, by paging every year: 145/119/115/129/167/124.

  699 of them are HTML at /search/view/ptr/<uuid>/ and 100 are scanned paper at
  /search/view/paper/<uuid>/. The link path itself says which, so nothing has to
  be fetched to find out.

  The fetch is FAST and unthrottled: 25 filings in 5 seconds, 0.21s each, so all
  799 is about three minutes. No filing paginated. The biggest of 25 sampled held
  24 trade rows, all on one page. An earlier plan budgeted a day for this.

  A paper filing is an image. There is no tesseract binary and no pytesseract in
  this environment, so it CANNOT be read. It lands as one row with null trade
  fields and FILING_KIND='paper', so the hole is visible in the data instead of
  being silently absent.

THE NAME MATCH IS THE HARD PART, not the scrape. A plain last-name join of the
62 distinct filers to POLITICS__MEMBER_CROSSWALK lands 26 clean, 29 ambiguous
and 7 missed: the crosswalk holds every member in history so 'Marshall' hits 18
people, and the filer's last name carries its suffix -- 'Perdue , Jr',
'Manchin, III', and 'Moran,' with a bare trailing comma. FILER_LAST_CLEAN is
landed here with the suffix and comma stripped; the join itself belongs in the
mart, restricted to people who actually held a Senate seat in the term.

CHECKPOINT per filing, in logs/senate_efd_checkpoint.json. A crash at filing 700
of 799 must not restart at 1.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_LIB))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_LIB / ".env", override=True)

from land_frame import land  # noqa: E402

BASE = "https://efdsearch.senate.gov"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
PTR_REPORT_TYPE = "[11]"
CHECKPOINT = _REPO / "logs" / "senate_efd_checkpoint.json"

SID_FILINGS = "fed_senate_efd_filings"
SID_PTR = "fed_senate_efd_ptr"

FIRST_YEAR, LAST_YEAR = 2021, 2026
PAUSE = 0.25  # polite, and still finishes 799 filings in about four minutes


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    s.get(f"{BASE}/search/home/", timeout=60)
    tok = s.cookies.get("csrftoken")
    r = s.post(f"{BASE}/search/home/", timeout=60,
               data={"prohibition_agreement": "1", "csrfmiddlewaretoken": tok},
               headers={"Referer": f"{BASE}/search/home/"})
    if not r.url.rstrip("/").endswith("/search"):
        raise SystemExit(f"agreement POST did not land on /search/, got {r.url}")
    return s


def index(s: requests.Session, years: list[int]) -> pd.DataFrame:
    rows = []
    for y in years:
        start, declared = 0, None
        while True:
            r = s.post(f"{BASE}/search/report/data/", timeout=120,
                       headers={"Referer": f"{BASE}/search/",
                                "X-Requested-With": "XMLHttpRequest"},
                       data={"start": str(start), "length": "100",
                             "report_types": PTR_REPORT_TYPE, "filer_types": "[]",
                             "submitted_start_date": f"01/01/{y} 00:00:00",
                             "submitted_end_date": f"12/31/{y} 23:59:59",
                             "candidate_state": "", "senator_state": "",
                             "office_id": "", "first_name": "", "last_name": "",
                             "csrfmiddlewaretoken": s.cookies.get("csrftoken")})
            r.raise_for_status()
            j = r.json()
            declared = j["recordsTotal"] if declared is None else declared
            for d in j["data"]:
                m = re.search(r'href="([^"]+)"[^>]*>(.*?)</a>', d[3], re.S)
                link = m.group(1) if m else None
                title = re.sub(r"<[^>]+>", "", m.group(2)).strip() if m else None
                kind = "paper" if link and "/paper/" in link else "ptr"
                rows.append({
                    "FILER_FIRST": d[0].strip(),
                    "FILER_LAST": d[1].strip(),
                    "FILER_LAST_CLEAN": clean_last(d[1]),
                    "FILER_FULL": d[2].strip(),
                    "REPORT_TITLE": title,
                    "FILING_LINK": link,
                    "FILING_ID": link.rstrip("/").split("/")[-1] if link else None,
                    "FILING_KIND": kind,
                    "IS_AMENDMENT": str(bool(title and "amendment" in title.lower())),
                    "FILED_DATE": d[4].strip(),
                    "FILING_YEAR": str(y),
                })
            start += 100
            if start >= j["recordsTotal"]:
                break
        got = sum(1 for x in rows if x["FILING_YEAR"] == str(y))
        if got != declared:
            raise SystemExit(f"{y}: paged {got} rows against a declared {declared}")
        print(f"  {y}: {got} PTR filings", flush=True)
    return pd.DataFrame(rows)


SUFFIX = re.compile(r"(?:,)?\s*(?:JR|SR|II|III|IV|V)\.?$", re.I)


def clean_last(x: str) -> str:
    """'Perdue , Jr' -> 'PERDUE'. 'Moran,' -> 'MORAN'.

    Without this the crosswalk join misses 7 of 62 filers outright."""
    return SUFFIX.sub("", (x or "").strip().rstrip(",").upper()).strip().rstrip(",")


CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)
ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)


def _cells(tr: str) -> list[str]:
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip() for c in CELL.findall(tr)]


def trades(s: requests.Session, rec: dict) -> list[dict]:
    """One row per trade line. A paper filing yields one flagged row instead."""
    base = {
        "FILING_ID": rec["FILING_ID"],
        "SENATOR": rec["FILER_FULL"],
        "FILER_LAST_CLEAN": rec["FILER_LAST_CLEAN"],
        "FILED_DATE": rec["FILED_DATE"],
        "FILING_YEAR": rec["FILING_YEAR"],
        "IS_AMENDMENT": rec["IS_AMENDMENT"],
        "FILING_KIND": rec["FILING_KIND"],
        "PTR_LINK": BASE + (rec["FILING_LINK"] or ""),
    }
    if rec["FILING_KIND"] == "paper":
        return [dict(base, LINE_NO=None, TRANSACTION_DATE=None, OWNER=None,
                     TICKER=None, ASSET_DESCRIPTION=None, ASSET_TYPE=None,
                     TYPE=None, AMOUNT=None, COMMENT=None)]

    r = s.get(BASE + rec["FILING_LINK"], timeout=90)
    r.raise_for_status()
    out = []
    for tr in ROW.findall(r.text):
        c = _cells(tr)
        # Header rows come back as 9 <th> cells; a trade row is 9 <td> cells
        # whose first is the line number.
        if len(c) != 9 or not c[0].isdigit():
            continue
        out.append(dict(base, LINE_NO=c[0], TRANSACTION_DATE=c[1], OWNER=c[2],
                        TICKER=c[3], ASSET_DESCRIPTION=c[4], ASSET_TYPE=c[5],
                        TYPE=c[6], AMOUNT=c[7], COMMENT=c[8]))
    if not out:
        # An HTML filing with no parseable line is a real signal, not a blank.
        out.append(dict(base, LINE_NO=None, TRANSACTION_DATE=None, OWNER=None,
                        TICKER=None, ASSET_DESCRIPTION=None, ASSET_TYPE=None,
                        TYPE=None, AMOUNT=None, COMMENT="NO PARSEABLE TRADE ROWS"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--years", default="")
    ap.add_argument("--index-only", action="store_true",
                    help="stage 1 only: land the filing list, fetch no documents")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="stop after N filings")
    args = ap.parse_args()
    years = ([int(y) for y in args.years.split(",") if y.strip()]
             if args.years else list(range(FIRST_YEAR, LAST_YEAR + 1)))

    print("=== Senate EFD Periodic Transaction Reports ===", flush=True)
    s = session()
    idx = index(s, years)
    print(f"\n  {len(idx):,} filings, "
          f"{(idx.FILING_KIND == 'ptr').sum()} html and "
          f"{(idx.FILING_KIND == 'paper').sum()} paper, "
          f"{idx.FILER_FULL.nunique()} distinct filers", flush=True)

    if not args.dry_run:
        res = land(idx, SID_FILINGS, f"{BASE}/search/",
                   "Senate EFD filing index, PTRs 2021 on; one row = one filing.")
        if res.get("status") != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {SID_FILINGS}: {res}")
        print(f"  landed -> LIBRARY_RAW.LANDING.{SID_FILINGS.upper()}", flush=True)

    if args.index_only:
        print("\nSTAGE 1 ONLY: no documents fetched", flush=True)
        return 0

    done = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else {}
    rows, t0 = [], time.time()
    recs = idx.to_dict("records")
    if args.limit:
        recs = recs[:args.limit]
    for i, rec in enumerate(recs, 1):
        rows.extend(trades(s, rec))
        done[rec["FILING_ID"]] = len(rows)
        if i % 100 == 0:
            CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
            CHECKPOINT.write_text(json.dumps(done))
            print(f"    {i}/{len(recs)} filings, {len(rows):,} rows, "
                  f"{time.time()-t0:.0f}s", flush=True)
        time.sleep(PAUSE)

    df = pd.DataFrame(rows)
    real = df[df.FILING_KIND == "ptr"]
    print(f"\n  {len(df):,} rows from {len(recs):,} filings in {time.time()-t0:.0f}s")
    print(f"  {len(real):,} real trade lines, "
          f"{(df.FILING_KIND == 'paper').sum()} unreadable paper filings", flush=True)

    if args.dry_run:
        print("DRY RUN: nothing landed", flush=True)
        return 0
    res = land(df, SID_PTR, f"{BASE}/search/",
               "Senate PTR trade lines, 2021 on; one row = one reported trade; "
               "FILING_KIND='paper' rows are scanned filings that cannot be read.")
    if res.get("status") != "success":
        raise RuntimeError(f"QUALITY GATE FAILED for {SID_PTR}: {res}")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID_PTR.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
