# Handoff: close the data gaps blocking the docket

Written 2026-09-06 at the end of a long session. Everything here is measured, not
assumed. The docket is `docket/docket.csv`, 150 questions, 86 open, 11 of them
blocked by missing data. This handoff is about those 11 and nothing else.

## State at handoff

| | |
|---|---|
| docket questions | 150 |
| open | 86 |
| runnable today | 75 |
| blocked on data | 11 |
| warehouse | 2,893 tables, 2.33 billion rows |
| spend today | about 4 credits, $8 |

Running when this was written: `scripts/fec_itcont_load.py`, the donor backfill,
cycle 2016 of 14, 38.9M rows landed to staging. It swaps at the end. Check
`LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS` for about 285 million rows.

## The nine must-dos, in the order I would take them

### 1. Donor records 2000 to 2022 — RUNNING, restarted once
Unblocks 4 questions: 32, 87, 89, 94.
`scripts/fec_itcont_load.py` was extended today from 2 cycles to 14, gained a
`--cycles` flag and a `CYCLE_FILE` column, and now deletes each zip as its cycle
finishes. Verify the swap happened and the cycle column is populated for all 14.

It crashed once, on cycle 2020, after 63.6 million rows had staged. One donor
memo field is larger than Python's 128 KB csv default, which kills the whole
parse rather than one row. Fixed in `loadkit/fec_parse.py`.

**Add per-cycle resume before running it again.** There is none. A crash at cycle
12 of 14 throws away every row and restarts at 2000, which is an hour of rework
for nothing. The pieces already exist:

  * `loadkit/checkpoint.py` is the house checkpoint helper.
  * The loader already writes a `CYCLE_FILE` column, so a completed cycle is
    identifiable in the staging table.
  * `--cycles` already lets you name the subset to run.

The smallest version: after each cycle, write the cycle id to a checkpoint file;
on start, skip any cycle already there unless `--force`. The staging table is
appended to across cycles, so a resumed run continues rather than overwrites.
Careful with the `first` flag, which drives `overwrite=True` on the very first
chunk. A resume must NOT set it, or it wipes what earlier cycles staged.

### 2. Committee roster by year — 1 hour
Unblocks 2 questions: 36, 78, 84.
`scripts/congress_committee_membership_load.py` runs again as of today. It loads
the CURRENT snapshot only. The historical file is
`committees-historical.yaml` in the unitedstates/congress-legislators repo. Add
it, keyed by congress number.
WARNING: this loader has no argparse. `--help` runs the full load.

### 3. Campaign spending miscount — 1 hour
Unblocks 1 question: 84.
`scripts/fec_independent_expenditure_load.py` runs again as of today. The mart
double counts amended filings. Dedupe on the latest amendment per FILE_NUM plus
TRAN_ID. Cross-check the 2024 total against the FEC's own $4.4 billion.

### 4. Hospital finances, all years — half a day
Unblocks 4 questions: E43, E47, E48, 11.
CMS HCRIS publishes one file per fiscal year, 2011 to 2023, about 60 MB each. The
warehouse holds one vintage. Loop the years, stamp a SOURCE_FILE_YEAR before
concatenating, keep landing's column naming.
NOTE: the mart grain moves from one row per hospital to one per hospital-year.
Its unique tests will need updating, and findings E43, E47 and E48 change shape.

### 5. Lobbying 2011 to 2019 — half a day
Unblocks 1 question: 83.
`scripts/senate_lda_load.py` has the API key set in `library-onboarding/.env`,
verified working today. It was killed after 90 minutes with nothing landed. It
holds a whole year of nested JSON in memory before uploading, and a year is tens
of thousands of filings. Rewrite it to upload in pages, not per year, and print
with flush. Missing years: 2011-2019 and 2022-2026. It appends, so existing years
are safe. It checkpoints per year to `logs/senate_lda_checkpoint.json`.

### 6. Political group donations — half a day
Unblocks 1 question: 88.
`scripts/irs527_load.py` runs. Add record types A and B from the same zip already
used for forms 8871 and 8872. 17.9 million rows. Do it chunked, not all in RAM.

### 7. Bills before 2023 — 1 day
Unblocks 1 question: 91.
No loader exists. GovInfo publishes BILLSTATUS in bulk by congress. Congresses
113 to 117 are missing. The old loader is in `_JUNK_DRAWER` and CLAUDE.md forbids
building from there, so write it fresh. About 50,000 bills and 400,000 cosponsors.

### 8. Revolving door names — unknown, decide first
Blocks 1 question: 90.
`GOVERNANCE__FED_REVOLVINGDOOR_PROJECT` has 406 rows and PERSON_NAME is the
string 'nan' on 405 of them. There is no person and no date. Either find a real
source or retire question 90.

### 9. Senate and house stock trades — 5 days, two scrapers
Blocks 3 questions: 35, 78, 91.
Senate trades stop 2020-12. House trade details sit in PDFs. Both need scrapers.
The full sequence for the Senate site was tested live and is written up in
`reports/politics_probe_2026-09-05/PLAN_data_holes.md` under Phase 4.
This is the biggest single item and the least leverage. Consider deferring.

## Rules that bit me today, so they do not bite you

1. Several loaders have no argparse. `python3 <loader>.py --help` runs the FULL
   load and replaces a live table. Check for argparse before smoke testing.
2. `ingest.assess_density` returns a key named `empty`, never `ok`. Reading it as
   `.get("ok", True)` turns the density gate into a rubber stamp.
3. `GET_DDL` on a Snowflake procedure returns the name WITHOUT its schema.
   Re-running that text creates a copy in the session's current schema.
4. Snowflake's `REGEXP_LIKE` matches the WHOLE string, not a prefix.
5. The Federal Register API rate limits. Backoff was added today.
6. The warehouse gate hook reads your command text. It blocks any command
   containing a destroy word, including a price command that mentions one.
7. `python3 <script>.py | grep ...` hides progress. grep buffers.

## How to verify each one landed

Every backfill ends the same way:

    python scripts/coverage_probe.py measure --table <FQN> --col <DATE COL> --write
    python scripts/coverage_probe.py overlap <TABLE A> <TABLE B>

The overlap check is the point. Six questions died last week because two tables
shared no years, and nobody knew until the join returned nothing. Then rebuild
the docket's data view:

    python scripts/docket_data_check.py

## What NOT to do

Do not touch the 280 capped portal tables, the 14 capped named sources, the 51
stale sources, or the 1,998 tables with no measured years. All of that is real,
written up in `reports/warehouse_gaps_2026-09-06.md`, and blocks zero docket
questions. Chris wants to analyse, not to keep loading.
