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
    # Cents are OPTIONAL but captured: 98 rows carry a real exact figure rather
    # than a range -- $669.27, $474.06, $224.00 -- and \$[\d,]+ alone stopped
    # dead at the decimal point and landed $669, silently losing the cents.
    r"(?P<amt>\$[\d,]+(?:\.\d{2})?(?:\s*-\s*(?:\$[\d,]+(?:\.\d{2})?)?)?\+?)")
STOP = re.compile(r"^(?:F\s|S\s+O|S\s+:|\*|I\s|L\s+:|C\s|D\s|Yes\b|No\b)", re.I)
# Case-insensitive, and tolerant of a "Ticker: " label glued inside the
# parenthetical ("(Ticker: CCLFX)") -- see the module docstring, bug 6.
#
# 2026-09-07: take the LAST parenthetical, not the first, and cap it at six
# characters. An asset often carries a qualifier in its own parentheses ahead
# of the ticker, and the first-match rule was landing that qualifier:
#     Anheuser-busch Inbev ... AdR (belgium) (bud)[CS]  ->  BELGIUM, not BUD
#     American Tower Corporation(REIT) (AMT) [CS]       ->  REIT,    not AMT
# The ticker is always the parenthetical nearest the [type] bracket. Six is
# the real ceiling -- CWEN.A and BAC.PL are the longest genuine ones seen.
TICKER = re.compile(r"\((?:Ticker:?\s*)?([A-Za-z][A-Za-z0-9.\-]{0,5})\)", re.I)
ASSET_TYPE = re.compile(r"\[([A-Z]{2,4})\]")
# \b after Yes/No, always -- a bare "No" with no boundary matches "note",
# "Nokia", "Nordstrom", "Northrop"... any asset name that starts that way.
# See the module docstring, bug 5.
NOISE = re.compile(r"^(?:ID|Owner|Asset|Type|Date|Amount|Cap\.|Gains|\$200\?|"
                   r"Notification|F\s|S\s|P\s+T\s+R|Clerk of the House|Name:|Status:|"
                   r"State/District|\*|I\s|C\s|Yes\b|No\b)", re.I)
TYPE_NAME = {"P": "Purchase", "S": "Sale", "E": "Exchange"}

# The form's fixed brackets. A filer picks one; there are no other ranges.
#
# 2026-09-07: 72 rows landed with a dangling "$15,001 -" and no upper bound.
# Widening the next-line rescue recovered exactly ONE of them, because the
# bound is not on a later line -- pypdf drops it from the extraction outright.
# The tail reads "$15,001 - g fedcFil...", footer glued straight onto the dash.
# But the lower bound names the bracket on its own, so the top can be filled
# from the form itself rather than from the text. This is the form's own
# ladder, not an inference about what the filer meant.
AMOUNT_LADDER = {
    "$1,001": "$15,000",
    "$15,001": "$50,000",
    "$50,001": "$100,000",
    "$100,001": "$250,000",
    "$250,001": "$500,000",
    "$500,001": "$1,000,000",
    "$1,000,001": "$5,000,000",
    "$5,000,001": "$25,000,000",
    "$25,000,001": "$50,000,000",
}

# The three literal owner-column codes, never anchored -- see parse_pdf.
#
# 2026-09-07: the bare r"SP|DC|JT" matched INSIDE words and ate company names.
# 107 rows landed with a chopped asset AND a wrong owner:
#
#   VOLVO AB UNSP/ADR (VLVLY)  -> OWNER=SP  ASSET='/ADR (VLVLY)'      47 rows
#   Golub Capital BDC, Inc.    -> OWNER=DC  ASSET=', Inc. (GBDC)'      6 rows
#   CRISPR Therapeutics        -> OWNER=SP  ASSET='R Therapeutics'     2 rows
#   SPDR S&P 500 (SPY)         -> OWNER=SP  ASSET='DR S&P 500 (SPY)'  39 rows
#   SPY... / SPX...            -> OWNER=SP  ASSET='Y ...' / 'X ...'   13 rows
#
# Still unanchored, because a real code genuinely does have text jammed in
# front of it: the previous row's tail runs straight into it, as in
# "...SuBHOLDINg OF: Neuberger Berman - Traditional IRASPAmphenol Corp".
# That is IRA + SP + Amphenol, and nothing in the character stream says so.
#
# Two lookbehind rules were tried against 96 refetched filings, 1,446 rows:
#     (?<![A-Za-z0-9])   false-rejected 179 real codes, 12.4%
#     (?<![A-Z0-9])      false-rejected  66 real codes,  4.6%
# Both die on the same shape -- furniture ending in a capital, "...IRA" + "SP".
# So position is not the signal. What IS safe is the character AFTER the code:
# no asset name on this form begins with a slash, comma, period, dash, close
# paren or apostrophe. That guard alone recovers "UNSP/ADR" and "BDC, Inc.",
# 53 of the 107 bad rows, and cannot reject a real code.
OWNER_TOKEN = re.compile(r"(?:SP|DC|JT)(?![/,.\-)'])")

# The other 54 rows need a named list, and here is why no rule replaces it.
# pypdf glues a real owner code straight onto the asset with no space, and the
# asset is very often ALL CAPS: 2,080 owner-coded rows start that way --
# SPNVIDIA Corporation, SPAT&T Inc., SPJP Morgan Chase, SPTJX Companies. Every
# shape test that rejects "SPDR S&P 500" also rejects those. Measured on the
# live table 2026-09-07:
#     (?=[A-Z][a-z])                    false-rejects 2,080 good rows
#     (?:SP|DC|JT)(?=[A-Z]{1,3}[ (\[])  false-rejects AT&T, JP Morgan, TJX
#
# These are matched by CONTAINMENT, not by prefix: the code sits at index 3 of
# CRISPR, so "does the text start with this word here" would miss it. A hit
# anywhere inside one of these words is part of the word, never a column.
# Extend the list when a new collision turns up; do not reach for a cleverer
# regex, and lean on OWNER_RAW to find the next one.
GLUED_WORDS = ("SPDR", "SPX", "SPY", "SPGI", "SPWR", "CRISPR", "UNSP", "SPAC")
# What a company name looks like when it starts right after an owner code.
# Capital then lowercase. Every GLUED_WORDS brand carries on in capitals
# instead, which is what separates "SP"+"Xylem" from "SPDR".
ASSET_WORD_START = re.compile(r"[A-Z][a-z]")
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

# The per-row footer the form prints under every trade, run together with the
# next trade by pypdf. Case is mangled beyond recognition in these PDFs --
# "FIlINg STATuS", "FILINg STATUS", "SuBHOLDINg OF", "S UbHOLDINg OF" -- so
# every marker here is matched case-insensitively and tolerates stray spaces.
#
# Why this exists (2026-09-07): it used to be cleaned by accident. A bogus
# owner-code hit inside "SPDR" or "UNSP" chopped the block, and the footer
# happened to sit in front of the chop. Fixing the owner regex removed that
# accident and left the footer glued to the asset name. Strip it on purpose.
#
# Greedy, so it cuts through the LAST marker on the block. Anything before a
# footer marker belongs to the previous trade, never to this one.
#
# The status value is spelled out, never \w+. "STATUS: NewAmeresco, Inc." has
# no space after New, so a greedy \w+ eats the first word of the company and
# lands ", Inc." as the asset -- the exact class of bug this file is fixing.
#
# Do NOT anchor on the leading F of FILING. The backward line-walk stops on a
# line beginning "F ", so the block often starts mid-word at "IlINg STATuS:
# New..." with the F already gone -- 14 rows landed that way. "STATUS:" plus a
# known value is unambiguous furniture on its own. Deleted is a real value too;
# leaving it out of the alternation is what stranded two Zuora rows.
FURNITURE = re.compile(
    r".*(?:STATUS\s*:\s*(?:New|Amended|Deleted)|"
    r"S\s*U\s*B\s*HOLDING\s+OF\s*:|DESCRIPTION\s*:|\bg\s+fedcb?)", re.I | re.S)
# NOT DONE, and this is the record of why. "SUBHOLDING OF:" and "DESCRIPTION:"
# are followed by free text with no delimiter before the asset name --
# "...DPJ & KAJ joint accountSPDR S&P 500 (SPY)". Roughly 6 rows in 96 filings
# keep that account name on the front of the asset.
#
# The obvious seam is a lowercase-to-uppercase step, bounded by the first "("
# so it cannot reach the ticker. Tried it 2026-09-07. It cut 34 real company
# names on the same sample, because plenty of them contain that step:
#     PayPal Holdings        -> Pal Holdings
#     SiteOne Landscape      -> One Landscape
#     AdaptHealth Corp       -> Health Corp
#     Taiwan Semiconductor Manufacturing -> Manufacturing
# Six visibly-ugly rows beat 34 silently-wrong ones, so the account name stays
# on. It is obvious on sight and OWNER_RAW carries the original head anyway.


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
        if any(s <= mm.start() < e for s, e in spans):
            continue
        # A code sitting INSIDE a brand name is not a code. Checked by
        # containment, not prefix -- CRISPR carries its SP at index 3. See
        # GLUED_WORDS for why this is a list and not a rule.
        # A real code followed by a Capital-then-lowercase word beats the deny
        # list. Added 2026-09-07 after the list ate two real owner codes:
        # "Ameriprise SEP IRA" + "SP" + "Xylem Inc." glues into "...IRASPXylem",
        # whose "SPX" is spelled BY the seam, not by either side. Every brand in
        # GLUED_WORDS continues in caps -- SPDR, SPX Corporation, SPY, CRISPR --
        # so "SP" then "Xy" is a code and "SP" then "DR" is not. Checked against
        # all 59 rows the deny list touches: flips the 2 Xylem rows, leaves the
        # other 57 brand rows alone.
        if not ASSET_WORD_START.match(text, mm.end()) and any(
                any(s2 <= mm.start() < s2 + len(g) for s2 in _spans_of(text, g))
                for g in GLUED_WORDS):
            continue
        return mm
    return None


def _spans_of(text: str, word: str) -> list[int]:
    """Every start index of `word` in `text`. Cheap: the lists are tiny."""
    out, at = [], text.find(word)
    while at != -1:
        out.append(at)
        at = text.find(word, at + 1)
    return out


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
            # "$50,001 -" is a range whose upper bound is on a LATER line.
            # Only checked for the last trade on the line -- an amount ahead
            # of another trade on the SAME line was never cut off.
            #
            # 2026-09-07: this used to look at exactly one line ahead and only
            # at its very first character, which left 72 rows carrying a
            # dangling "$15,001 -" with no upper bound at all. The House form
            # offers only fixed ranges, so an open top is always a lost value,
            # never a filer's choice. Walk up to three lines and allow the
            # bound to sit after leading furniture, but stop at the next trade
            # so a later trade's amount can never be borrowed as this one's top.
            if amt.endswith("-") and k == len(matches) - 1:
                for ahead in range(1, 4):
                    j = i + ahead
                    if j >= len(lines):
                        break
                    if TRADE.search(lines[j]):
                        break
                    nxt = re.match(r"[^$]{0,12}?(\$[\d,]+(?:\.\d{2})?)", lines[j])
                    if nxt:
                        amt = f"{amt} {nxt.group(1)}"
                        break
            # Still open? pypdf lost the bound entirely. Fill it from the
            # form's own ladder, keyed on the lower bound. See AMOUNT_LADDER.
            if amt.endswith("-"):
                low = amt[:-1].strip()
                top = AMOUNT_LADDER.get(low)
                if top:
                    amt = f"{low} - {top}"

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
            # Then the per-row footer glued in front of this trade's asset,
            # and the free-text value trailing the footer's last marker.
            asset_raw = FURNITURE.sub("", asset_raw, count=1)

            owner_hit = _first_owner_outside_enclosures(asset_raw)
            if owner_hit:
                owner = owner_hit.group(0)
                asset_local = asset_raw[owner_hit.end():]
            else:
                owner = m.group("owner") or "SELF"
                asset_local = asset_raw

            asset = clean_asset(asset_local)
            # The untouched head of the block, before any owner code was cut
            # off it. Added 2026-09-07 after the OWNER_TOKEN bug ate 107 company
            # names: with this column a bad split is a query away from being
            # spotted and undone, instead of needing all 2,633 PDFs refetched.
            # Keep it even when the split looks clean -- it costs 24 characters
            # a row and it is the only evidence of what the cut removed.
            owner_raw = re.sub(r"\s+", " ", asset_raw)[:24].strip() or None
            # Ticker/type are searched in THIS trade's own isolated text only
            # -- never the whole raw line -- so a mismatched ticker case or a
            # missing ticker never falls through to a different trade's
            # ticker further down the same blob. See the module docstring,
            # bugs 1, 2 and 3.
            # LAST parenthetical, not the first. See the TICKER comment: a
            # qualifier in its own brackets sits ahead of the real ticker often
            # enough that first-match landed BELGIUM and REIT as symbols.
            ticks = TICKER.findall(asset_local)
            tick = ticks[-1] if ticks else None
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
                "OWNER_RAW": owner_raw,
                "TRANSACTION_TYPE": TYPE_NAME.get(m.group("tp"), m.group("tp")),
                "IS_PARTIAL": str(bool(m.group("part"))),
                "TRANSACTION_DATE": m.group("d1"),
                "NOTIFICATION_DATE": m.group("d2"),
                "AMOUNT_RANGE": amt,
                "TICKER": tick.upper() if tick else None,
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
            "OWNER_RAW": None,
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
