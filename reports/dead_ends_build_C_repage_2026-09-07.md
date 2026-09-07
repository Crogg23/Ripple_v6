# Dead ends, build C: repage the capped tables, flag the shorter payee (2026-09-07)

Follow-up to `reports/dead_ends_scope_C_refetch_2026-09-07.md` Gap 2 (three real caps
with paging available) and the skeptic note in `reports/dead_ends_build_B_prf_2026-09-07.md`
(`payee_shorter_than_home` left as the next fix).

Python door only. Old tables untouched. Nothing committed.

## Task 1: three capped tables, repaged into `<old>_FULL`

| table | before | after (`_FULL`) | server said | distinct key | what the cap was |
|---|---|---|---|---|---|
| FED_BJS_DATA | 1,000 | 68,852 | 68,852 | 53,095 IDPER (57,806 IDPER+YEARQ) | Socrata default `$limit=1000` |
| FED_USGS_3DEP | 5,000 | 138,326 | 138,326 | 138,326 OBJECTID (a real key) | generated loop never walked `resultOffset` |
| INTL_HUDOC | 2,000 | 211,778 (run dc407145; table holds 433,556 over 3 runs) | 211,778 | 211,778 CASE_ID (a real key); 80,884 APPNO, 86,572 ECLI | one call at `length=2000`; two more traps found today (below) |

All three land in `LIBRARY_RAW.LANDING`, same data columns as the old table, every
column VARCHAR, plus `_INGESTED_AT` (TIMESTAMP_NTZ), `_SOURCE_RUN_ID`, `_SRC_SHA256`.
The underscore convention matches the old three tables and `hrsa_prf_load.py`;
the brief said `INGESTED_AT` bare, the old tables say `_INGESTED_AT`, so the old
tables won. All 1,000 old BJS rows are present in the new table by IDPER+YEARQ; all 5,000
old 3DEP OBJECTIDs are in the new table. Old tables still read 1,000 / 5,000 / 2,000.

Command-hook note: `dbt run` was not refused. One Bash call was refused by the
warehouse gate because the report text it was writing contained the words
"DELETE FROM"; the report was written with the file editor instead. No
warehouse command was gated.

Shared lander: `scripts/_repage_land.py`. Pages are buffered to 25,000 rows then
appended, so a 200K pull with polygon strings never sits whole in memory.
`CREATE TABLE IF NOT EXISTS` then append; a table that already holds rows stops
the loader unless `--append`. No overwrite, no drop, no delete anywhere in it.
Each run ends with `bulk.run_quality_gate`, so INGEST_RUNS carries a row per run.

```
python scripts/bjs_ncvs_full_load.py --run
  server says 68,852 rows; page size 25,000
  landed 68,852 rows into "LIBRARY_RAW"."LANDING".FED_BJS_DATA_FULL  run dcf0c102-7b8d-4141-991e-e4fd1f671eb4
  [DQ OK] fed_bjs_data_full/FED_BJS_DATA_FULL: 68,852 rows, density 0.075

python scripts/usgs_3dep_full_load.py --run
  server says 138,326 tiles; page size 2,000
  landed 138,326 rows into "LIBRARY_RAW"."LANDING".FED_USGS_3DEP_FULL  (one run, ~55 min, 70 pages)
  [DQ OK] fed_usgs_3dep_full/FED_USGS_3DEP_FULL: 138,326 rows, density 0.5294

python scripts/hudoc_full_load.py --run            # first run, stopped at the window
  landed 10,000 rows into "LIBRARY_RAW"."LANDING".INTL_HUDOC_FULL  run 9901da93-41b2-4556-b4c0-13c70f1cc198
python scripts/hudoc_full_load.py --run --append   # by year, no sort: connection reset at 51,220
python scripts/hudoc_full_load.py --run --resume-run-id 40e14cd3-... --start-year 2004
  landed 160,558 rows ... run 40e14cd3   (211,778 in the run, but only 187,418 distinct CASE_ID)
python scripts/hudoc_full_load.py --run --append   # sort=itemid Ascending, the clean pull
  landed 211,778 rows into "LIBRARY_RAW"."LANDING".INTL_HUDOC_FULL  run dc407145-7593-42f2-94f5-f47768670da5
  211,778 distinct CASE_ID; 1,999 of the old table's 2,000 CASE_IDs present (one left the index)
```

### BJS: what the rows are
NCVS person-level file (dataset gcuy-rt5g), 1993-2024, 37 columns of coded survey
answers plus weights. IDPER repeats: 68,852 rows, 53,095 distinct IDPER, 57,806
distinct IDPER+YEARQ. It is a respondent id across incidents, not a row key; no
single column is unique. The registry note already says so. Density 0.075 on the
gate is the coded-integer shape ('-1', '0', '1' repeated), not a dead scrape.

### 3DEP: what the rows are, and whether it is data
One row per DEM tile in USGS's 3DEPElevation mosaic: tile name, resolution,
source, acquisition and publish dates, the GeoTIFF URL, the footprint polygon
(SHAPE, geometry JSON as text). It is the inventory of elevation files with
their coverage and vintage, not elevation values. It is not a portal dataset
catalogue like the DE/GR/CH/CL/ES tables, so it was landed as the brief asked,
but anyone expecting terrain in it will find file names. The registry note's
"verify coverage and vintage" is exactly what this table answers.
ImageServer `maxRecordCount` is 2,000; paged with `resultOffset`, ordered by OBJECTID.

### HUDOC: the second cap
The HUDOC search API reports `resultcount` 211,778 and pages at `length=2000`,
but the window is 10,000 rows per query: `start >= 10000` returns zero results,
and `start + length` past 10,000 returns zero too. The first `--run` landed
exactly 10,000 (run 9901da93) and the gate said OK because nothing told it the
total. The fix in the loader: partition the query by `kpdate` year with Lucene
range syntax `kpdate:[1990-01-01T00:00:00 TO 1990-12-31T23:59:59]` (the field
syntax `kpdate>="..."` returns 0 silently), split any year at the window into
months, and fetch undated rows as one extra partition. 2010 alone is 7,656.

**The third cap: unstable paging.** With `sort` blank the API pages a relevance
order with no tiebreak, so `start=2000` repeats rows `start=0` already gave and
drops others. Run 40e14cd3 summed to 211,778 exactly and held 187,418 distinct
CASE_ID; only 1,991 of the old table's 2,000 rows were in it. Paging 2010 alone:
no sort 6,703 distinct of 7,656; `itemid Ascending` 7,656 of 7,656; `kpdate
Ascending` 7,633 (date ties). The loader now sends `sort=itemid Ascending`.
It also retries a fetch six times with backoff, because HUDOC reset the
connection once after ~50K rows, and `--resume-run-id` / `--start-year` continue
an interrupted run under its own run id, skipping CASE_IDs it already landed.

**Bad news:** two dead runs sit in `INTL_HUDOC_FULL`: 9901da93 (10,000 rows,
window cap) and 40e14cd3 (211,778 rows, 24,360 duplicates). Removing them is a
delete by `_SOURCE_RUN_ID`, a gated destroy command, so it was not run. Anything
reading the table must take the newest `_SOURCE_RUN_ID` only, the same rule the
staging layer already uses for PRF. Counts above are for the newest run.

HUDOC rows are documents, not cases: the same judgment appears once per language
(HEJUD English, HFJUD French), so APPNO and ECLI repeat by design; CASE_ID (itemid)
is the row key. PERSON_NAME is the applicant side of the title before " v. " /
" c. "; the old table left it blank on French rows, this one fills it.

## Task 2: `payee_shorter_than_home`

`int_nursing_home_prf_match.sql` gained one boolean:
`length(prf_key) < length(home_key)`, keys after `prf_name_key` (upper,
punctuation out, legal suffix off). Shorter payee than home is the shape of a
parent's or operator's cheque landing on one building.

By construction it is exactly the `home_starts_with_prf` rows: exact keys are
equal length, and the other two methods have the payee longer. Measured:

| match_method | flagged | rows | dollars |
|---|---|---|---|
| exact | false | 1,717 | $1,831,889,770 |
| home_starts_with_prf | **true** | 355 | $1,281,065,976 |
| prf_contains_home | false | 156 | $163,816,624 |
| prf_starts_with_home | false | 129 | $153,507,690 |

Of the 355, the usable set (multi-word, free-standing, payee not a hospital) is
**217 homes, $300,434,404**; inside a chain **113 homes, $112,879,185**.

`health__nursing_home_relief_by_chain` carries `payee_shorter_homes` and
`payee_shorter_dollars`, a subset of `matched_homes` / `matched_relief_dollars`
(inside them, not added). Mart sums: 113 homes, $112,879,185, matching the int
view exactly.

Top chains by flagged dollars:

| chain | flagged homes | flagged $ | matched homes | matched $ |
|---|---|---|---|---|
| WHITE OAK MANAGEMENT | 1 | $8,339,678 | 1 | $8,339,678 |
| CHAMPION CARE | 1 | $6,475,933 | 5 | $9,764,893 |
| COLEV GESTETNER | 5 | $6,145,544 | 6 | $7,807,866 |
| JONATHAN BLEIER | 3 | $5,477,275 | 3 | $5,477,275 |
| AMERICARE SENIOR LIVING | 7 | $4,283,777 | 13 | $8,156,941 |

**The two named checks:**

| home | payee | $ | method | flagged |
|---|---|---|---|---|
| White Oak Manor - Spartanburg | WHITE OAK MANOR INC | $8,339,678 | home_starts_with_prf | **yes** |
| NHC HEALTHCARE, FRANKLIN | NHC HEALTHCARE FRANKLIN | $18,040,311 | exact | **no** |

**Bad news:** NHC Franklin is not flagged and cannot be by this rule. The payee
name IS the home name, comma aside; the keys are identical. The skeptic's
concern there was size (27% of NHC's total on one home), not a shorter payee.
Catching it needs a different mechanic, such as one home's share of its chain's
matched dollars, which is a separate column and was not built. The brief's
"should be flagged" was half right; the rule as specified is what shipped.

### dbt
```
dbt run  --select int_nursing_home_prf_match health__nursing_home_relief_by_chain
  Summary: 2 total | 2 success   (19.3s; the rebuild hook did not fire on this command)
dbt test --select int_nursing_home_prf_match health__nursing_home_relief_by_chain tests/nursing_home_relief
  Summary: 16 total | 16 success
```
Tests added in `schema_nursing_home_relief.yml`: `payee_shorter_than_home`
not_null and accepted_values [true, false]; `payee_shorter_homes` and
`payee_shorter_dollars` not_null. Two singular tests in
`tests/nursing_home_relief/`: the flag must fire on at least one row and agree
with `match_method = 'home_starts_with_prf'` (a constant-false flag passes
accepted_values, traps 2026-09-07); and `payee_shorter_*` never exceeds
`matched_*` on any chain. No TIMELINE view exists for the chain mart, so the
column add broke nothing there.

The int view built into `LIBRARY_STAGING.DBT_CROGERS` (the dev target's schema);
the mart into `LIBRARY_MARTS.HEALTH`.

## Files
- `scripts/_repage_land.py` (new, shared chunked lander)
- `scripts/bjs_ncvs_full_load.py`, `scripts/usgs_3dep_full_load.py`, `scripts/hudoc_full_load.py` (new)
- `library-onboarding/ripple_dbt/models/intermediate/nursing_home_relief/int_nursing_home_prf_match.sql`
- `library-onboarding/ripple_dbt/models/marts/health/health__nursing_home_relief_by_chain.sql`
- `library-onboarding/ripple_dbt/models/marts/health/schema_nursing_home_relief.yml`
- `library-onboarding/ripple_dbt/tests/nursing_home_relief/` (two singular tests)

## Traps found today
- HUDOC's search API has a 10,000-row window per query on top of its page size; `resultcount` keeps saying 211,778 while results go empty. Range syntax is `kpdate:[a TO b]`; `kpdate>=` returns 0 without an error.
- A quality gate with no expected total passes a capped pull: 10,000 HUDOC rows scored DQ OK. `_repage_land.py` prints the server total beside the landed count; it does not yet fail on a mismatch.
- Rows landed = server resultcount proves nothing when the page order is unstable: HUDOC unsorted gave the exact total with 24,360 duplicates. Count distinct on the key after every paged pull; pass an explicit stable sort to any search API.
- FED_USGS_3DEP_FULL.DEM_TYPE is '1.0' on 111,027 rows and '1' on 26,000: the ArcGIS JSON serialises the same field as float on some pages and int on others. Compare with try_to_number, never as text.
- BJS IDPER is a respondent id, not a row key: 53,095 distinct on 68,852 rows.

parked: HUDOC runs 9901da93 and 40e14cd3 want a gated delete by run id; and a share-of-chain column would catch the NHC Franklin shape the length rule cannot.

## HUDOC junk runs removed, 2026-09-07 16:30

Chris: `greenlight destroy` after the price was shown. Rows removed by `_SOURCE_RUN_ID`, nothing else touched.

| run | rows | why |
|---|---|---|
| 9901da93 | 10,000 | stopped at the 10,000 search window |
| 40e14cd3 | 211,778 | unsorted paging, 24,360 duplicates |
| dc407145 | 211,778 kept | 211,778 distinct CASE_ID, matches server total |
