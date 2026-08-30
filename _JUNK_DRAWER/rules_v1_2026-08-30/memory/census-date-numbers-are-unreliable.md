---
name: census-date-numbers-are-unreliable
description: "2026-08-20 - the Aug-17 census grid's date_min/date_max/\"corrupt table\" counts are wrong twice over; use reports/time_index/ instead"
metadata: 
  node_type: memory
  type: project
  originSessionId: b7d61832-8c75-40e6-a228-a1702062f80b
  modified: 2026-08-20T16:37:12.142Z
---

**Do not trust the date columns in the 2026-08-12 census grid fill
(`reports/census_grid_2026-08-12/fill/fill_tables.csv`).** They are wrong in two
independent ways, and both were verified against the live warehouse on
2026-08-20.

**1. It only measured columns Snowflake already typed DATE or TIMESTAMP.**
Ripple's landing layer is all-VARCHAR by design, so nearly every real date is a
string that staging re-parses. The census's scanner filtered on `data_type in
('DATE','TIMESTAMP_NTZ',...)`, so it walked past the clock on 143 tables holding
~229M rows — including pharma payments to doctors, all federal grants and
contracts, all drug adverse-event reports, and 80 years of UN votes. Worse, on
tables whose *only* typed column was Ripple's own `_INGESTED_AT`, it measured
that and reported it as the table's date range.

**2. It reported min/max, which a single junk row destroys.** It flagged 89
tables as having corrupt date ranges. Counting how many rows are actually bad
shows most of those tables are healthy — one row at year 0001 or 9999 was
dragging the whole range. Real junk across the warehouse is ~6,000 rows in 1.2
billion, once our own two cast bugs and the publishers' null-markers are set
aside.

**How to apply:**
- For anything about dates, read `reports/time_index/` instead — `columns.csv`
  (per-column trusted window, grain, junk counts, value shape),
  `clock_index.csv` (what each column MEANS: happened / reported / decided /
  span / ingest / not-a-date), and `README.md` for the findings.
- Rebuild that index with `scripts/census/scan_time_index.py` (read-only,
  checkpointed, ~$3 for all 686 tables). It measures every time-shaped column
  regardless of type and shape-guards every parse.
- **A wild min/max is a hypothesis, not a verdict** — the same lesson as
  [[completeness-check-traps]]. Always count the bad ROWS before calling a table
  broken.
- Before nulling any date-shaped sentinel, run the isolated-spike test: count on
  the exact marker versus count in the surrounding years. On 2026-08-20 that test
  saved a bank established-date and UK incorporation dates that have thousands of
  genuine records around 1900.

Related: [[warehouse-data-traps]], [[value-shape-sniffer-2026-08-18]].
