#!/usr/bin/env python3
"""Load House Periodic Transaction Reports: the index, then the trade lines.

The warehouse has no House trade data at all. This is stages 3 and 4 of the
item 9 plan and it unblocks the House half of docket question 91.

TWO SOURCES, both keyless:

  the index   disclosures-clerk.house.gov/public_disc/financial-pdfs/<year>FD.zip
              57-96 KB, one tab-delimited file per year. Columns: Prefix, Last,
              First, Suffix, FilingType, StateDst, Year, FilingDate, DocID.
              FilingType 'P' is the Periodic Transaction Report.
              14,650 filings 2021-2026, 3,105 of them PTRs.

  the filing  /public_disc/ptr-pdfs/<year>/<DocID>.pdf

THE DOCID'S FIRST DIGIT TELLS YOU THE FORMAT, and it is right every time across
all six years:

    prefix 2   2,633 filings   a real text PDF, pypdf extracts it
    prefix 8     421 filings   a scan, pypdf returns zero characters
    prefix 9      51 filings   a scan, same

So the scan list comes out of the index and those 472 PDFs are never fetched.
There is no tesseract binary and no pytesseract here, so a scan CANNOT be read.
Each lands as one row with null trade fields and IS_SCAN='True', which keeps the
hole visible in the data instead of silently absent.

THE PARSE IS A SEARCH, NEVER AN ANCHOR. pypdf keeps the words and throws away
the table, and the layout is not consistent between filings. Both of these are
real lines from 2024:

    P 10/09/202511/01/2025 $1,001 - $15,000
    Duke Energy Corporation (DUK) [ST]P 11/01/202411/04/2024$1,001 - $15,000

In the first the asset sits on the lines ABOVE. In the second it shares the line
with the trade and there is not even a space before the type letter. An anchored
^ regex matched 20 of 35 trades on an eight-filing sample and missed every
same-line one. Searching anywhere in the line matched 35 of 35.

THE AMOUNT WRAPS AND THE ASSET SPANS TWO LINES. A real filing looks like this,
Rep. Allen's 2024 PTR, doc 20025031:

    SP Ameriprise Financial, Inc. Common     <- asset, line 1, owner code first
    Stock (AMP) [ST]                         <- asset, line 2, ticker and type
    P 04/09/202405/09/2024$50,001 -          <- trade, amount cut off
    $100,000                                 <- the rest of the amount

So the owner code sits at the START OF THE ASSET BLOCK, not on the trade line.
The asset is TWO lines, not one. And the upper bound of the range is on the line
AFTER the trade. Take any of those three for granted and the row lands wrong:
a first pass reported "$50,001" as the amount and "Stock (AMP) [ST]" as the
asset name, both silently and both wrong.

The block is walked BACKWARD from the trade line, collecting lines until it hits
form furniture, another trade, or a "Filing Status" / "Subholding Of" line.

THE GAPS IN THE FORM LABELS ARE NUL BYTES, NOT SPACES. pypdf emits U+0000 where
the form draws its small-caps labels, so the line that LOOKS like

    F      S     : New

is really 'F\x00\x00\x00\x00\x00 S\x00\x00\x00\x00\x00: New'. Python's \s does not match
\x00, so every pattern written against the visible text silently fails to match
and those label lines get swallowed into the asset name. A first pass landed
"F S : New S O : R.W. Allen & Associates" as an asset description because of
exactly this. Every NUL is turned into a space before anything is matched.

RAW_LINE is landed on every row, always. A parsed trade that cannot be traced
back to its source text is not evidence.

AMOUNTS ARE RANGES, never numbers. "$1,001 - $15,000" is the finest resolution
the form has. Any total is a bounded estimate and must be reported as one.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests
from pypdf import PdfReader

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_LIB))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_LIB / ".env", override=True)

from land_frame import land  # noqa: E402

INDEX_URL = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
PDF_URL = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc}.pdf"
UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

SID_INDEX = "fed_house_fd_index"
SID_PTR = "fed_house_ptr"
FIRST_YEAR, LAST_YEAR = 2021, 2026
SCAN_PREFIXES = ("8", "9")

# Search anywhere in the line. See the module docstring for why anchoring fails.
TRADE = re.compile(
    r"(?P<owner>\b(?:SP|DC|JT)\b)?\s*(?P<tp>[PSE])\s*(?P<part>\(partial\))?\s*"
    r"(?P<d1>\d{2}/\d{2}/\d{4})\s*(?P<d2>\d{2}/\d{2}/\d{4})\s*"
    # The trailing dash is INSIDE the capture so a cut-off range is detectable.
    r"(?P<amt>\$[\d,]+(?:\s*-\s*(?:\$[\d,]+)?)?\+?)")
OWNER_LEAD = re.compile(r"^(SP|DC|JT)\b\s*")
STOP = re.compile(r"^(?:F\s|S\s+O|S\s+:|\*|I\s|L\s+:|C\s|D\s|Yes\b|No\b)", re.I)
TICKER = re.compile(r"\(([A-Z][A-Z0-9.\-]{0,6})\)")
ASSET_TYPE = re.compile(r"\[([A-Z]{2,4})\]")
NOISE = re.compile(r"^(?:ID|Owner|Asset|Type|Date|Amount|Cap\.|Gains|\$200\?|"
                   r"Notification|F\s|S\s|P\s+T\s+R|Clerk of the House|Name:|Status:|"
                   r"State/District|\*|I\s|C\s|Yes|No)", re.I)
TYPE_NAME = {"P": "Purchase", "S": "Sale", "E": "Exchange"}


def index_year(year: int) -> list[dict]:
    r = requests.get(INDEX_URL.format(year=year), headers=UA, timeout=300)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    name = [n for n in z.namelist() if n.lower().endswith(".txt")][0]
    text = z.read(name).decode("utf-8-sig", "replace")
    rows = []
    for x in csv.DictReader(io.StringIO(text), delimiter="\t"):
        doc = (x.get("DocID") or "").strip()
        rows.append({
            "DOC_ID": doc,
            "FILING_TYPE": (x.get("FilingType") or "").strip(),
            "PREFIX": (x.get("Prefix") or "").strip(),
            "FILER_LAST": (x.get("Last") or "").strip(),
            "FILER_FIRST": (x.get("First") or "").strip(),
            "FILER_SUFFIX": (x.get("Suffix") or "").strip(),
            "STATE_DISTRICT": (x.get("StateDst") or "").strip(),
            "FILING_YEAR": (x.get("Year") or "").strip(),
            "FILING_DATE": (x.get("FilingDate") or "").strip(),
            "INDEX_YEAR": str(year),
            # Read off the DocID, never off a download. See the docstring.
            "IS_SCAN": str(doc[:1] in SCAN_PREFIXES),
        })
    return rows


def clean_asset(s: str) -> str | None:
    s = re.sub(r"\s+", " ", s).strip(" .-•")
    return s or None


def parse_pdf(raw: bytes, rec: dict) -> list[dict]:
    text = "".join((pg.extract_text() or "") for pg in PdfReader(io.BytesIO(raw)).pages)
    # NUL, not space. See the docstring: without this the form's own label lines
    # never match anything and end up inside the asset name.
    text = text.replace("\x00", " ")
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in text.split("\n") if l.strip()]
    out = []
    for i, line in enumerate(lines):
        m = TRADE.search(line)
        if not m:
            continue
        amt = re.sub(r"\s+", " ", m.group("amt")).strip()
        # "$50,001 -" is a range whose upper bound is on the NEXT line. Without
        # this the row lands as a bare "$50,001", which reads like a number.
        if amt.endswith("-") and i + 1 < len(lines):
            nxt = re.match(r"\$[\d,]+", lines[i + 1])
            if nxt:
                amt = f"{amt} {nxt.group(0)}"
        # Walk BACK to collect the whole asset block. It is one to three lines
        # and it carries the owner code at its front.
        block = []
        before = line[:m.start()].strip()
        if before:
            block.append(before)
        for back in range(1, 5):
            j = i - back
            if j < 0:
                break
            cand = lines[j]
            if TRADE.search(cand) or NOISE.match(cand) or STOP.match(cand):
                break
            block.append(cand)
        block.reverse()
        asset_raw = " ".join(block)
        lead = OWNER_LEAD.match(asset_raw)
        owner = m.group("owner") or (lead.group(1) if lead else "SELF")
        asset = clean_asset(OWNER_LEAD.sub("", asset_raw))
        blob = f"{asset or ''} {line}"
        tick = TICKER.search(blob)
        atype = ASSET_TYPE.search(blob)
        out.append({
            "DOC_ID": rec["DOC_ID"],
            "FILER_LAST": rec["FILER_LAST"],
            "FILER_FIRST": rec["FILER_FIRST"],
            "STATE_DISTRICT": rec["STATE_DISTRICT"],
            "FILING_YEAR": rec["FILING_YEAR"],
            "FILING_DATE": rec["FILING_DATE"],
            "IS_SCAN": "False",
            "LINE_NO": str(len(out) + 1),
            "OWNER": owner,
            "TRANSACTION_TYPE": TYPE_NAME.get(m.group("tp"), m.group("tp")),
            "IS_PARTIAL": str(bool(m.group("part"))),
            "TRANSACTION_DATE": m.group("d1"),
            "NOTIFICATION_DATE": m.group("d2"),
            "AMOUNT_RANGE": amt,
            "TICKER": tick.group(1) if tick else None,
            "ASSET_TYPE": atype.group(1) if atype else None,
            "ASSET_DESCRIPTION": asset,
            # Always. A parsed trade with no traceable source line is not evidence.
            "RAW_LINE": line[:2000],
        })
    return out


def blank_row(rec: dict, why: str) -> dict:
    return {"DOC_ID": rec["DOC_ID"], "FILER_LAST": rec["FILER_LAST"],
            "FILER_FIRST": rec["FILER_FIRST"], "STATE_DISTRICT": rec["STATE_DISTRICT"],
            "FILING_YEAR": rec["FILING_YEAR"], "FILING_DATE": rec["FILING_DATE"],
            "IS_SCAN": rec["IS_SCAN"], "LINE_NO": None, "OWNER": None,
            "TRANSACTION_TYPE": None, "IS_PARTIAL": None, "TRANSACTION_DATE": None,
            "NOTIFICATION_DATE": None, "AMOUNT_RANGE": None, "TICKER": None,
            "ASSET_TYPE": None, "ASSET_DESCRIPTION": None, "RAW_LINE": why}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--years", default="")
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    years = ([int(y) for y in args.years.split(",") if y.strip()]
             if args.years else list(range(FIRST_YEAR, LAST_YEAR + 1)))

    print("=== House financial disclosures ===", flush=True)
    idx = []
    for y in years:
        rows = index_year(y)
        idx += rows
        p = sum(1 for x in rows if x["FILING_TYPE"] == "P")
        sc = sum(1 for x in rows if x["FILING_TYPE"] == "P" and x["IS_SCAN"] == "True")
        print(f"  {y}: {len(rows):,} filings, {p} PTRs, {sc} of those scans", flush=True)
    df_idx = pd.DataFrame(idx)
    print(f"\n  index total {len(df_idx):,} filings", flush=True)

    if not args.dry_run:
        res = land(df_idx, SID_INDEX,
                   "https://disclosures-clerk.house.gov/public_disc/",
                   "House financial disclosure index, all filing types 2021 on; "
                   "IS_SCAN is read off the DocID prefix, not off a download.")
        if res.get("status") != "success":
            raise RuntimeError(f"QUALITY GATE FAILED for {SID_INDEX}: {res}")
        print(f"  landed -> LIBRARY_RAW.LANDING.{SID_INDEX.upper()}", flush=True)

    if args.index_only:
        print("\nSTAGE 3 ONLY: no PDFs fetched", flush=True)
        return 0

    ptrs = [x for x in idx if x["FILING_TYPE"] == "P"]
    if args.limit:
        ptrs = ptrs[:args.limit]
    rows, n_scan, n_empty = [], 0, 0
    for i, rec in enumerate(ptrs, 1):
        if rec["IS_SCAN"] == "True":
            rows.append(blank_row(rec, "SCANNED FILING, NOT MACHINE READABLE"))
            n_scan += 1
            continue
        r = requests.get(PDF_URL.format(year=rec["FILING_YEAR"], doc=rec["DOC_ID"]),
                         headers=UA, timeout=300)
        if r.status_code != 200:
            rows.append(blank_row(rec, f"HTTP {r.status_code}"))
            continue
        try:
            got = parse_pdf(r.content, rec)
        except Exception as e:
            rows.append(blank_row(rec, f"PARSE ERROR {type(e).__name__}"))
            continue
        if not got:
            rows.append(blank_row(rec, "NO PARSEABLE TRADE LINES"))
            n_empty += 1
        else:
            rows += got
        if i % 200 == 0:
            print(f"    {i}/{len(ptrs)} filings, {len(rows):,} rows", flush=True)

    df = pd.DataFrame(rows)
    real = df[df.TRANSACTION_DATE.notna()]
    print(f"\n  {len(df):,} rows from {len(ptrs):,} PTRs")
    print(f"  {len(real):,} real trade lines")
    print(f"  {n_scan:,} scans, {n_empty:,} text filings with no parseable line",
          flush=True)

    if args.dry_run:
        print("DRY RUN: nothing landed", flush=True)
        return 0
    res = land(df, SID_PTR, "https://disclosures-clerk.house.gov/public_disc/",
               "House PTR trade lines 2021 on; one row = one reported trade; "
               "IS_SCAN rows are unreadable images; AMOUNT_RANGE is a range, "
               "never a number.")
    if res.get("status") != "success":
        raise RuntimeError(f"QUALITY GATE FAILED for {SID_PTR}: {res}")
    print(f"\nDONE -> LIBRARY_RAW.LANDING.{SID_PTR.upper()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
