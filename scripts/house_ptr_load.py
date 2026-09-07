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

A LINE CAN CARRY MANY TRADES, GLUED, NOT ONE. A busy filer's PDF often reads
the whole table onto one pypdf line with no separator between the end of one
trade and the owner code of the next:

    JTAlphabet Inc. - Class C CapitalStock (gOOg) [ST] P 06/24/2021 ...
    ...JTApple Inc. (AAPL) [ST] S 06/18/2021 ...

Searching once (re.search) finds only the first trade on that line and drops
every other one silently -- a fresh 20-filing audit caught one such filing
landing 3 of 21 real trades. The fix is finditer: every trade on the line, not
the first, each keeping only ITS OWN slice of the line (the text since the
previous trade found on that same line, or since the line start for the
first) as its asset text. A ticker or type bracket is searched for only
inside that slice, never the whole line -- searching the whole line lets a
mismatched or missing ticker on trade 1 fall through and steal trade 2's
ticker instead, which is exactly as wrong as it sounds and was landing in
the data.

THE OWNER CODE IS FOUND, NEVER ASSUMED TO LEAD THE BLOCK. Each trade's own
slice usually still has somebody else's leftovers glued to the front of it --
the previous trade's own "FILING STATUS / SUBHOLDING OF / DESCRIPTION" tail,
or (for the first trade on a page) the whole page header ending "...Amount
Cap. Gains >$200?". Both are stripped by finding the owner code itself (the
literal SP/DC/JT, never anchored to string start) and keeping only what comes
after the FIRST one found outside a (ticker) or [type] -- first, not last,
because the true asset name can itself spell out one of those letter pairs
later on ("FUNDCOMMON" contains "DC") without that making it an owner. A
candidate with no real owner code before it (the header text alone, when the
owner column is genuinely blank for a self-owned trade) is left as SELF, same
as before. When a page break orphans just the two-letter owner code onto the
tail of a form-furniture line by itself, the backward walk rescues that one
token before it stops there rather than discarding the whole line.

TICKER CASE IS NOT TRUSTWORTHY, AND "Ticker:" SOMETIMES PREFIXES IT. The same
small-caps rendering that turns "GOOG" into "gOOg" turns "AGCO" into "AgCO" --
an all-caps-only ticker regex simply fails on these and used to fall through
to the next ticker anywhere in the blob (see above). The fix matches any
case and normalizes with .upper(). Some assets print "(Ticker: CCLFX)"
instead of a bare "(CCLFX)"; the regex strips that label if present.

A BARE "No" MATCHES "note", "Nokia", "Nordstrom", ANYTHING STARTING THAT WAY,
if it is not word-bounded. The NOISE filter's Yes/No alternative (there to
catch the certification page's Yes/No checkbox line) needs \bNo\b, or an
asset description that legitimately starts "note ..." gets swallowed as if
it were that checkbox line and the row lands with everything blank.
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
STOP = re.compile(r"^(?:F\s|S\s+O|S\s+:|\*|I\s|L\s+:|C\s|D\s|Yes\b|No\b)", re.I)
# Case-insensitive, and tolerant of a "Ticker: " label glued inside the
# parenthetical ("(Ticker: CCLFX)") -- see the module docstring, bug 6.
TICKER = re.compile(r"\((?:Ticker:?\s*)?([A-Za-z][A-Za-z0-9.\-]{0,6})\)", re.I)
ASSET_TYPE = re.compile(r"\[([A-Z]{2,4})\]")
# \b after Yes/No, always -- a bare "No" with no boundary matches "note",
# "Nokia", "Nordstrom", "Northrop"... any asset name that starts that way.
# See the module docstring, bug 5.
NOISE = re.compile(r"^(?:ID|Owner|Asset|Type|Date|Amount|Cap\.|Gains|\$200\?|"
                   r"Notification|F\s|S\s|P\s+T\s+R|Clerk of the House|Name:|Status:|"
                   r"State/District|\*|I\s|C\s|Yes\b|No\b)", re.I)
TYPE_NAME = {"P": "Purchase", "S": "Sale", "E": "Exchange"}

# The three literal owner-column codes, never anchored -- see parse_pdf.
OWNER_TOKEN = re.compile(r"SP|DC|JT")
# A ticker parenthetical or an asset-type bracket. A hit inside either of
# these is a ticker/type character pair, never the owner column.
ENCLOSED = re.compile(r"\([^()]*\)|\[[^\[\]]*\]")
# The table header ("...ID Owner Asset Transaction Type Date Notification
# Date Amount Cap. Gains >$200?") ends in this exact literal every time, and
# it is often glued directly onto the front of the FIRST trade on a page --
# same line, no newline, so the backward line-walk never sees it as a
# separate line to stop on. Strip through the LAST copy of it (greedy .*
# backtracks to the rightmost match), whatever is glued in front of it is
# never part of an asset. See the module docstring, bug 4.
HEADER_JUNK = re.compile(r".*\$200\?", re.S)


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


def _first_owner_outside_enclosures(text: str) -> re.Match | None:
    """The leftmost SP/DC/JT that is not sitting inside a (ticker) or [type].

    Never anchored -- the real owner code is glued directly onto its own
    trade's asset name with nothing between them, so it can land anywhere in
    a block that also carries the previous trade's tail text or page
    furniture in front of it (HEADER_JUNK strips the one place that tail
    text reliably hides a false hit -- "Washington, DC" in the page header).
    Take the FIRST real hit, not the last: the true owner code always leads
    its own asset name, and the asset name itself can coincidentally spell
    out one of these three letter pairs later on (an all-caps "FUNDCOMMON"
    contains "DC") without that making it an owner column.
    """
    spans = [(mm.start(), mm.end()) for mm in ENCLOSED.finditer(text)]
    for mm in OWNER_TOKEN.finditer(text):
        if not any(s <= mm.start() < e for s, e in spans):
            return mm
    return None


def parse_pdf(raw: bytes, rec: dict) -> list[dict]:
    text = "".join((pg.extract_text() or "") for pg in PdfReader(io.BytesIO(raw)).pages)
    # NUL, not space. See the docstring: without this the form's own label lines
    # never match anything and end up inside the asset name.
    text = text.replace("\x00", " ")
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in text.split("\n") if l.strip()]
    out = []
    for i, line in enumerate(lines):
        # ALL of them, never just the first. Several trades can run together
        # on one pypdf line with no separator between the end of one and the
        # owner code of the next. See the module docstring, bug 1.
        matches = list(TRADE.finditer(line))
        if not matches:
            continue
        prev_end = 0
        for k, m in enumerate(matches):
            amt = re.sub(r"\s+", " ", m.group("amt")).strip()
            # "$50,001 -" is a range whose upper bound is on the NEXT line.
            # Only checked for the last trade on the line -- an amount ahead
            # of another trade on the SAME line was never cut off.
            if amt.endswith("-") and k == len(matches) - 1 and i + 1 < len(lines):
                nxt = re.match(r"\$[\d,]+", lines[i + 1])
                if nxt:
                    amt = f"{amt} {nxt.group(0)}"

            # This trade's own slice of the current line: from the end of the
            # PREVIOUS trade found on this line (or the line start, for the
            # first), up to this trade's own P/S/E. For a second-or-later
            # trade on a glued line this is the whole story; it never needs
            # anything from an earlier physical line.
            same_line = line[prev_end:m.start()]
            prev_end = m.end()

            block = []
            if same_line.strip():
                block.append(same_line)
            if k == 0:
                # Walk BACK to collect the whole asset block. It is one to
                # three lines and it carries the owner code at its front --
                # except when a page break has orphaned that owner code onto
                # the tail of the header/furniture line right above; rescue
                # just that trailing code before stopping there.
                for back in range(1, 5):
                    j = i - back
                    if j < 0:
                        break
                    cand = lines[j]
                    if TRADE.search(cand):
                        break
                    if NOISE.match(cand) or STOP.match(cand):
                        orphan = re.search(r"(SP|DC|JT)\s*$", cand)
                        if orphan:
                            block.append(orphan.group(1))
                        break
                    block.append(cand)
            block.reverse()
            asset_raw = " ".join(block)
            # Strip the table-header boilerplate glued onto the front of the
            # first trade on a page. See HEADER_JUNK and the module
            # docstring, bug 4.
            asset_raw = HEADER_JUNK.sub("", asset_raw, count=1)

            owner_hit = _first_owner_outside_enclosures(asset_raw)
            if owner_hit:
                owner = owner_hit.group(0)
                asset_local = asset_raw[owner_hit.end():]
            else:
                owner = m.group("owner") or "SELF"
                asset_local = asset_raw

            asset = clean_asset(asset_local)
            # Ticker/type are searched in THIS trade's own isolated text only
            # -- never the whole raw line -- so a mismatched ticker case or a
            # missing ticker never falls through to a different trade's
            # ticker further down the same blob. See the module docstring,
            # bugs 1, 2 and 3.
            tick = TICKER.search(asset_local)
            atype = ASSET_TYPE.search(asset_local)
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
                "TICKER": tick.group(1).upper() if tick else None,
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
