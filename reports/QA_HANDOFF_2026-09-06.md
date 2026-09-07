# QA/QC handoff: audit everything built 2026-09-06

You are auditing one session's work. Twenty-two commits, nine handoff items, ten
tables landed or rebuilt, thirteen marts touched. Assume nothing below is true.
Every number here is a CLAIM to be checked, not a fact to be repeated.

## How to work

**The Python door is the only one open.** dbt cannot authenticate on this
machine and the chat plug-in's token was rejected at session start. Connect with:

```python
import sys; sys.path.insert(0, "library-onboarding")
from dotenv import load_dotenv; load_dotenv("library-onboarding/.env", override=True)
import snow; conn = snow.connect()
```

**Read-only.** Do not write, drop, rename or rebuild anything. Every table
rebuilt today kept a rollback copy named `<TABLE>__PREV_20260906`; those are your
before-and-after, not garbage to clean up.

**Walk every chain.** A row count matching is not proof the rows are right. For
each claim, say what you checked, what a hit means, and what a miss means.

**Report the misses first.** Group findings as BLOCKER, REAL, MINOR. A number
that reproduces is worth one line; a number that does not is worth the space.

---

## 1. The loaders — did they land what they say?

| table | claimed rows | claimed shape |
|---|---|---|
| `LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS` | 283,771,819 | 14 cycles, 2000-2026, 11 quarantined |
| `FED_FEC_INDEPENDENT_EXPENDITURES` | 276,183 | 5 cycles, 2018-2026 |
| `FED_CONGRESS_COMMITTEE_MEMBERSHIP` | 26,971 | congresses 113-119 |
| `FED_CMS_HCRIS` | 80,077 | 13 years, 2011-2023 |
| `IRS527_SCHEDULE_A_CONTRIBUTIONS` | 9,701,952 | 8 ragged rows dropped |
| `IRS527_SCHEDULE_B_EXPENDITURES` | 8,191,177 | 17 ragged rows dropped |
| `FED_GOVINFO_BILLSTATUS` | 107,150 | 7 congresses, 113-119 |
| `FED_GOVINFO_BILL_COSPONSORS` | 1,268,519 | same 7 |
| `FED_SENATE_EFD_FILINGS` | 799 | 699 html, 100 paper |
| `FED_SENATE_EFD_PTR` | 6,855 | 6,755 trades, 100 paper |
| `FED_HOUSE_FD_INDEX` | 14,650 | all filing types |
| `FED_HOUSE_PTR` | 21,911 | 21,429 trades, 472 scans |
| `FED_SENATE_LDA_LOBBYIST_POSITIONS` | still growing | crawl was mid-2011 |

For each: count it, check its year or cycle spread, and check its stated key is
actually unique. The keys claimed are:

* FEC IE: `FILE_NUM` + `TRAN_ID`
* Committee roster: `CONGRESS` + `COMMITTEE_CODE` + `BIOGUIDE`
* HCRIS: `RPT_REC_NUM`
* Bills: `CONGRESS` + `BILL_TYPE` + `BILL_NUMBER`
* Donor: `SUB_ID`

**The most suspicious claim in this table** is that the donor loader's dedupe on
`SUB_ID` dropped exactly zero rows across fourteen cycles. Check whether SUB_ID
really is unique FEC-wide or whether the dedupe simply never ran.

## 2. The numbers that were reported to Chris

Reproduce each. A number that cannot be reproduced from the warehouse as it
stands now is a finding, even if it was true when written.

**FEC independent expenditures, clean totals** — filter
`IS_SUSPECT_FILING='False' AND IS_SUPERSEDED='False'`:

| cycle | claimed |
|---|---|
| 2018 | $1.30B |
| 2020 | $3.30B |
| 2022 | $2.26B |
| 2024 | $4.44B |
| 2026 | $1.05B |

Only 2024 was ever checked against an outside figure, the FEC's published ~$4.4B.
The other four are unverified. Say so if you cannot verify them either.

**The suspect flag** is `TRAN_ID LIKE 'WFT%' AND EXP_AMO > 20,000,000`, 35 rows
carrying $129.53B [CORRECTED 2026-09-07: written down everywhere as $91.0B,
which was off by $38.5B/42% low — resummed the 35 flagged rows fresh, see
QA_HANDOFF_AUDIT_2026-09-06.md]. Attack it: find a legitimate row it catches,
or a junk row it misses. It is known to miss Logan Keener at $20.0M in 2026,
Kurt Cobain at $12.4M in 2022 and Jason Kim at $10.0M in 2020.

**Question 84**, congress-matched, three committees, 2018-2026: $586.0M against
and $191.4M for, 157 candidates. An earlier version of this number was
$1,431.9M, a 5.7x roster fan-out. Check the current one has not fanned out too.

**Hospital finances:** 65 to 108 hospitals stop filing each year; 1,322 changed
ownership type at least once; the share losing money runs 33.4% in 2011 to 43.1%
in 2022, with a 24.4% dip in 2020.

**Bills:** enactment rate 2.8% in the 113th falling to 1.4% in the 118th.
Cross-party cosponsorship 24.2% in the 113th, 17.4% in the 117th, 21.6% in the
119th. NOTE the trap: `LAW_NUMBER` is an empty string, never NULL, on the 104,998
bills that never became law.

**527 money:** RGA $2,209.0M, DGA $1,137.8M, ActBlue Non-Federal $1,062.6M across
5,050,398 contributions [CORRECTED 2026-09-07: written down as 4,508,587,
which is just ActBlue's own row count — RGA (257,621 rows) and DGA (284,190
rows) were excluded from the combined total. See QA_HANDOFF_AUDIT_2026-09-06.md].

**Senate trades:** 59 distinct filers today, not 62 — no counting method tried
reaches 62 [CORRECTED 2026-09-07: written down as "62 distinct filers, all 62
matching the crosswalk with no fan-out." There IS an unresolved collision: last
name "Scott" matches both Tim Scott and Rick Scott, both sitting senators on a
relevant committee across congresses 116-119. See QA_HANDOFF_AUDIT_2026-09-06.md].
Senators off Banking, Finance and Commerce average 193 trades each;
those on one average 85. That second pair was reported as a FIRST NUMBER and
explicitly not an answer to question 78.

## 3. The parsers — this is where to spend your time

Three loaders parse text that has no schema. Each had defects the first pass
missed. Assume more remain.

### House PTR PDFs, `scripts/house_ptr_load.py`

Three defects were already found and fixed:

1. The regex was anchored at `^` and missed every filing that puts the asset and
   the trade on one line. 20 of 35 matched anchored, 35 of 35 searching.
2. The amount's upper bound is on the NEXT line. `P 04/09/202405/09/2024$50,001 -`
   then `$100,000` is one $50,001-$100,000 purchase. The first pass landed
   `$50,001`, which reads like a number.
3. **pypdf emits NUL BYTES, not spaces.** `F      S     : New` is really
   `F\x00\x00\x00\x00\x00 S\x00\x00\x00\x00\x00: New`, and `\s` does not match
   `\x00`, so the stop patterns silently failed and form labels landed as asset
   descriptions.

**Your job:** pull 20 filings at random, open the PDFs, and check the parsed rows
against them line by line. Look specifically for:

* trades dropped entirely, which a row count cannot show
* an asset description that is really two assets run together
* `TICKER` picking up a CUSIP or a footnote instead of a symbol
* `OWNER` defaulting to SELF when the filing says SP, DC or JT
* amounts still landing as a single bound

`RAW_LINE` is on every row. Use it.

### Senate PTR HTML, `scripts/senate_efd_ptr_load.py`

Simpler, a real table. Check the row count per filing against the document, and
check that `LINE_NO` runs 1..n with no gaps. 1,030 of 6,855 rows sit on amended
filings and NOTHING supersedes an original with its amendment. Quantify the
double count.

### IRS 527 Schedule A and B, `scripts/irs527_schedule_ab_load.py`

The field layout was measured, not read off a doc, because the IRS layout file is
legacy binary. The claim is that both records are 18 fields and diverge at
position 15: A has the year-to-date aggregate there and the date at 16; B has the
date at 15 and the purpose at 16. **Verify that independently.** If it is
backwards, 17.9M rows have their dates in the wrong column and nobody would see
it, because both columns hold plausible-looking text.

## 4. The things built to work around a broken door

Three scripts exist only because dbt cannot log in. They bypass real safety
rails and that was known when they were written.

`scripts/build_marts_python_door.py` renders a dbt model and builds it without
dbt. It does NOT read `dbt_project.yml`, so it ignores `+enabled: false` and the
`guard_politics_mirror()` pre-hook whose entire purpose is to stop anything but
the hand-reconciled loaders from overwriting a POLITICS mart. It also creates
non-transient tables where dbt-snowflake creates transient ones.

**Check:** does the SQL it produced actually match what dbt would produce? Are
the marts it built consistent with their siblings on transience, ownership and
grants? Did it silently build anything that dbt would have refused?

`scripts/refresh_timeline_index.py` writes to the `TIMELINE__*_INDEX` rollup
tables. No builder for those exists anywhere in the repo, so this one invented
its own. Check the FINANCE, POLITICS and HEALTH indexes against their live
timeline views, and check no source was lost.

`scripts/fix_timeline_view_columns.py` recreates a timeline view from its own
DDL with the frozen column list dropped. Check the recreated views still carry
the same four canonical columns in the same order.

## 5. The traps file

Twenty-two entries were appended to `.claude/traps.md` today. One of them was
already WRONG and corrected the same day: it claimed `TIMELINE__WAREHOUSE` does
not include the IE timeline view. It does.

**Read every entry written 2026-09-06 and try to falsify it.** A trap file that
lies is worse than no trap file, because the next session trusts it.

## 6. Things stated plainly as not done

Confirm each is genuinely still open, and look for anything that should be on
this list and is not.

* No OCR. 472 House scans and 100 Senate paper filings unread, flagged.
* No amendment supersession on either chamber's trades.
* `--cycles` on the FEC IE loader cannot run: `land()` refuses any subset as a
  95% shrink.
* No ticker-to-sector map exists, so question 78's real question is unanswerable.
* The LDA backfill was still crawling 2011 of 14 years at session end.
* `POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS` is behind its landing table and
  needs a rebuild once the crawl finishes.

## 7. What a good audit produces

A report file with, in this order:

1. Every claim that did NOT reproduce, with the number you got instead.
2. Every parser defect you found, with the filing and the line.
3. Every trap entry you could falsify.
4. Everything that reproduced, one line each.
5. A plain verdict: is this work trustworthy, and where is it not.

Chris's rules apply to your report. Plain words, short lines, tables for
comparable things, receipts in the file and the answer in chat. Say "looks done,
not verified" rather than "done" unless you ran the thing that could disprove it.
