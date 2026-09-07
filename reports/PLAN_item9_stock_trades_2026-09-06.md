# Item 9: congressional stock trades — the plan

Written 2026-09-06. Every number here was measured live today, not carried over
from the earlier plan. Where the earlier plan's number held, it says so.

## What is actually broken

| | |
|---|---|
| `FINANCE__FED_SENATE_STOCK_WATCHER` | 8,350 rows, 2012-06-14 to 2020-12-02 |
| House trade lines | none in the warehouse at all |
| Blocks | questions 35, 78, 91 |

The Senate table stops dead in December 2020. Whatever fed it was a scrape of a
third-party mirror that stopped publishing. Nothing since.

## What is reachable, verified live 2026-09-06

**Senate.** The four-step sequence still works, unchanged:

1. `GET efdsearch.senate.gov/search/home/` — sets a `csrftoken` cookie.
2. `POST` the same URL with `prohibition_agreement=1` and that token.
   Redirects to `/search/`. This is the "I agree" gate; without it every
   later call returns the agreement page instead of data.
3. `POST /search/report/data/` per year with `report_types=[11]`, which is
   Periodic Transaction Report. It is a DataTables endpoint: `start`,
   `length`, and a `recordsTotal` in the response.
4. `GET` each filing's link out of column 3 of the row.

Counted today, one call per year:

| year | PTR filings |
|---|---|
| 2021 | 145 |
| 2022 | 119 |
| 2023 | 115 |
| 2024 | 129 |
| 2025 | 167 |
| 2026 | 124 |
| **total** | **799** |

799 matches the earlier plan exactly. Nothing has drifted.

**House.** The Clerk publishes one index zip per year at
`disclosures-clerk.house.gov/public_disc/financial-pdfs/<year>FD.zip`, 57-96 KB,
holding a tab-delimited text file. Columns: Prefix, Last, First, Suffix,
FilingType, StateDst, Year, FilingDate, DocID.

`FilingType = 'P'` is the Periodic Transaction Report.

| year | all filings | PTRs |
|---|---|---|
| 2021 | 2,718 | 680 |
| 2022 | 2,747 | 624 |
| 2023 | 2,385 | 460 |
| 2024 | 2,291 | 451 |
| 2025 | 2,915 | 515 |
| 2026 | 1,594 | 375 |
| **total** | **14,650** | **3,105** |

3,105 also matches the earlier plan exactly.

The index gives a DocID; the document itself is a PDF at
`/public_disc/ptr-pdfs/<year>/<DocID>.pdf`. There is no structured feed. The
trade lines live inside the PDF.

## The plan, five stages

### 1. Senate index — half a day

Land `FED_SENATE_EFD_FILINGS`: one row per filing. Filer first, last, full name,
filing link, filing date, year, and the report type. 799 rows.

This is the cheap half and it is worth landing on its own, before any document
is fetched, because it is the list that every later stage checks itself against.

Fail loud if a year's `recordsTotal` disagrees with the rows actually paged.

### 2. Senate trade lines — one day

`GET` each of the 799 filings. Two shapes come back and they are NOT the same
job:

* **HTML filings**, about 699 of 799 by the earlier count. A real table, one row
  per trade. Parse it.
* **Scanned paper filings**, about 100. An image. There is no tesseract in this
  environment, so these CANNOT be read. Land one row per filing with the trade
  fields null and a `FILING_KIND = 'paper'` flag, so the gap is visible in the
  data rather than silently absent.

Land `FED_SENATE_EFD_PTR` with the old table's core columns —
TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, ASSET_TYPE, TYPE, AMOUNT,
COMMENT, SENATOR — plus FILING_ID, IS_AMENDMENT, FILING_KIND and LINE_NO.

Unknown until it runs: total line count, throttling behaviour, how long the
session cookie lives. Budget a retry loop and a per-filing checkpoint. A crash
at filing 700 of 799 must not restart at 1, which is the lesson from the donor
backfill that lost an hour today.

### 3. House index — half a day

Land `FED_HOUSE_FD_INDEX` from the six annual zips: 14,650 rows, all filing
types, not just PTRs. The other types are useful on their own and the zip is
already downloaded.

This one is easy and has no unknowns. Do it first if the Senate scrape stalls.

### 4. House trade lines — two days

3,105 PDFs. The earlier plan measured 2,633 as extractable text and 421 as
scans, with 51 untested filings on a 9-prefix DocID. Use pypdf and the regex the
earlier plan already tested. Keep `RAW_LINE` on every row, always — a parsed
trade line that cannot be traced back to its source text is not evidence.

The 421 scans get the same treatment as the Senate's paper filings: one row,
null trade fields, flagged.

### 5. Join and mart — half a day

The mart is a UNION: the old table for 2012 to 2020, the new tables for 2021 on.
They do not overlap, so nothing needs deduping across the seam.

Matching a filer to a member:

* Senate: last name plus term span. Roughly 100 senators at a time makes this
  tractable.
* House: surname plus state plus district, from `StateDst`, plus term span.

Both go through `POLITICS__MEMBER_CROSSWALK` on bioguide. Watch the fan-out trap
recorded today: the committee roster is one row per congress, so `select
distinct` before joining money or trades to it.

## What this does not do

* **No OCR.** 472 House filings and 100 Senate paper filings are images, 572 in
  all, 14.6% of everything. Verified: pypdf returns zero characters on a
  prefix-8 or prefix-9 House PDF, no tesseract binary and no pytesseract in this
  environment. They stay unread and flagged. Adding OCR is a separate decision.
* **No amendments resolution.** `IS_AMENDMENT` is landed but nothing supersedes
  an original with its amendment. That is the FEC lesson from today, and the
  same fix applies later.
* **No dollar amounts.** Both chambers report a RANGE, never a number.
  "$1,001 - $15,000" is the finest resolution that exists. Any total is a
  bounded estimate and must be reported as one.

## STRESS TEST, run 2026-09-06 after the plan was written

The plan survived, but three of its estimates were wrong and one risk was
pointed at the wrong stage.

### The Senate scrape is minutes, not a day

25 filings fetched in 5 seconds. No throttling, no rate limit hit, no cookie
expiry, and NOT ONE filing paginated. The biggest of the 25 held 24 trade rows,
all on one page.

    0.21 s per filing  ->  799 filings in about 3 minutes

Stage 2 was budgeted at one day. The fetching is three minutes. What is left is
parsing and landing, which is half a day at most.

### The House text-versus-scan split is knowable without downloading anything

The DocID's FIRST DIGIT predicts the format, perfectly, across all six years:

| prefix | filings | what comes back |
|---|---|---|
| 2 | 2,633 | real text, extractable |
| 8 | 421 | scan, pypdf returns 0 chars |
| 9 | 51 | scan, pypdf returns 0 chars |

15.2% of House PTRs are images. The earlier plan listed the 51 nine-prefix
filings as "untested" -- they are scans, same as the eights. So the scan list
can be built from the index alone and those PDFs never need fetching.

Per year the scan share is falling: 16.9% in 2021 down to 11.5% in 2026.

### The House text has no delimiters, and that IS the work

pypdf extracts, but the table structure is gone. A real trade line comes back as:

    P 10/09/202511/01/2025 $1,001 - $15,000

Transaction date, notification date and amount are run together with no
separator. The asset name and ticker sit on the one or two lines ABOVE it:

    Brown & Brown, Inc. Common Stock
    (BRO) [ST]
    P 10/09/202511/01/2025 $1,001 - $15,000

It is parseable -- the dates are fixed-width and the amount starts with a dollar
sign -- but it is a line-state machine, not a table read. Keep RAW_LINE.

### THE REAL RISK IS THE NAME MATCH, not the scrape

Stage 5 was written as half a day of joining. Measured on the 62 distinct Senate
filers of 2021-2026, a plain last-name join to `POLITICS__MEMBER_CROSSWALK`:

| | filers |
|---|---|
| clean single match | 26 |
| ambiguous last name | 29 |
| no match at all | 7 |

Only 26 of 62. The crosswalk holds every member in history, so "Marshall" hits
18 people and "Graham" hits 14. And the filer's last name carries its suffix:
`Perdue , Jr`, `McConnell, Jr.`, `Manchin, III`, and `Moran,` with a bare
trailing comma.

Two fixes, both tested:

1. Strip a trailing suffix and comma from the filer's last name.
2. Restrict the crosswalk to people who actually held a SENATE committee seat in
   the relevant congresses, using the roster landed today.

| | filers |
|---|---|
| clean match | 60 |
| ambiguous | 0 |
| unmatched | 2 |

The two left over are Perdue and Roberts, who both left the Senate in January
2021 and so appear in no 117th-congress roster. Adding the 116th to the
candidate set closes them.

### What did not change

799 Senate PTRs and 3,105 House PTRs, both re-counted by paging every year.
699 HTML and 100 paper on the Senate side, counted by classifying all 799 links
rather than trusting the earlier figure.

## Cost and order

Revised after the stress test:

| stage | was | now | unblocks |
|---|---|---|---|
| 1 Senate index | half a day | 2 hours | nothing on its own |
| 2 Senate lines | one day | half a day | 35, 78 |
| 3 House index | half a day | 2 hours | nothing on its own |
| 4 House lines | two days | two days | 91 |
| 5 join and mart | half a day | ONE day | all three |

About three and a half days, not five. The Senate half shrank because the
fetching is three minutes. Stage 5 grew because the name match is the real
problem and the plan had it as an afterthought.

**If only one stage gets done, do 1 and 2.** The Senate half unblocks two of the
three questions and its parse is a table rather than a PDF. The House half is
where the two days go and it buys one question.

## The check that proves it

Twenty filings hand-checked against the source document, ten Senate and ten
House, before anything is called done. Line count, ticker, date and amount range
on each. That is the skeptic gate the earlier plan already set, and it stands.
