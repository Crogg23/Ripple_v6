# The Census Grid — FILLED — 2026-08-17

*The fill phase of the census grid: measured reality attached to every mart-layer
model. Sources: warehouse catalog metadata (Tier A, pennies), the 2026-08-11
verification scan reused for 562 tables ($0 new), and 27 fresh table scans
(Tier B, the new court tables + the mart views over large raw tables).
All queries read-only aggregates. Builders: `scripts/census/fill_tier_a.py`,
`fill_tier_b.py`, `staging_raw_crosswalk.py`, `merge_fill.py`.*

## The one-screen picture

- **All 589 mart-layer models measured. Zero unscanned. 1,227,375,627 total rows.**
- **349 models carry a real date range**; **306 are fresh into 2026**; 12 are
  stale (nothing after 2024-01-01) — list below.
- **1,170 of 1,172 staging models** now carry a measured row count via a parsed
  staging→raw reference crosswalk (`staging_to_raw.csv`) — the first hard key in
  the source-bookkeeping reconciliation. **2 staging views are broken**: their
  raw tables no longer exist (college-scorecard institutions, OSHA inspections
  — check whether re-pulls landed under new table names, the known spine-spec
  drift pattern).
- The pension tax-ID check is **PASSED**: 5,176 rows, 100% filled, 4,431
  distinct employers, zero sentinel masking, real sponsor names on sample.
  **Join trap:** values run 4–9 digits — leading zeros stripped; always join on
  a 9-digit zero-padded cast.

## What the fill found (the data-trap census, now with numbers)

These are hypotheses ranked by measured size, not verdicts — each needs a look
before repair (completeness-check trap rule).

**Duplicate-heavy tables (>5% identical full rows):** 11 models. Worst:
immigration USCIS data 94.5% dup, DHS OHSS 77.2%, **FAERS drug reactions 76.2%
dup of 20.6M rows** (if real, the adverse-event reaction table is ~4× smaller
than it looks), FEC committees 23.1%, FEC candidates 19.1%.

**Epoch-1970 date poisoning (>1k rows):** 20 models. Worst: **federal contracts
— all 20M rows carry at least one 1970 date column**, the 990 e-file index 3.2M,
FAA registry 1.2M, union filings 589k. Same TRY_TO_DATE epoch trap as the FAA
find on 2026-08-11.

**Far-future dates (>100 rows):** 23 models. Worst: consumer-product injuries
(NEISS) 9.8M rows, ICIJ offshore-leaks relationship dates 3.3M, NIH grants 2.1M,
ICE detainers 610k.

**Garbage year-zero dates:** two SEC fund tables whose newest "date" is year
0095/0099 — date parsing broken outright.

**Degenerate keys (≤1 distinct value):** 19 models whose best ID-shaped column
is a constant — 10 are aggregate tables whose only "ID" is the loader's run ID
(fine), but foreign-assistance's EIN column has exactly ONE distinct value
across 95k+ rows (a sentinel posing as a key — the NPPES pattern again).

**Sentinel-heavy keys (>1% masked):** 38 models, incl. 9.6M masked license
numbers in the provider registry and 334k literal-text VINs in vehicle
complaints.

**Stale tables (newest date before 2024):** the 990 e-file index stops
2020-01-28 (5.5M rows); Senate lobbying stops 2021 (the known 9% load);
OpenSanctions stops 2022-06; FAA registry's max date is 1970 (epoch);
judge financial-disclosure tables stop 2023-08 (likely source-side lag).

**The new court tables are join-ready internally:** docket IDs ~unique at 71.7M
rows, 7.8M distinct opinion clusters under 18.1M citations, 9.9M dockets
referenced by opinion clusters — high-cardinality real keys, still zero edges
to the entity map (registration remains the unlock).

## Files

| file | what it holds |
|---|---|
| `fill_tables.csv` | one row per mart model: rows, bytes, dup ratio, date range, epoch/future counts, best key + fill/distinct/sentinels, provenance |
| `tier_a_tables.csv` | catalog metadata, all 4,276 tables across marts/raw/staging |
| `tier_a_columns.csv` | full column inventory (142k columns) — recovers the 12 models whose columns weren't reconstructable from SQL |
| `tier_b_new_scans.jsonl` | the 27 fresh scans, same schema as the 2026-08-11 scan |
| `staging_to_raw.csv` | staging model → raw landing table crosswalk with raw row counts |
