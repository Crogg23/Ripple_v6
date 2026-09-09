# Dead columns in LIBRARY_MARTS — found, fixed, verified

2026-09-08. Started from `reports/THE_CATALOG.csv`, which had no measurements in it.

## What was measured

Every column of every base table in `LIBRARY_MARTS`, through the Python door
(`connect/db.py`) on an X-Small warehouse.

| | |
|---|---|
| tables | 704 |
| columns | 20,640 |
| per column | row_count, non_null, distinct, min, max, blank_string, top_5_values |
| output | `reports/catalog_profile_2026-09-08.csv` |

A column counts as dead when `non_null_pct` is 0, or when more than 99% of its
values are the empty string. That found 2,197.

## Why each dead column is dead

Each one was checked against the same-named column in the `LIBRARY_RAW` table
the dbt manifest says the mart descends from.

| verdict | columns | what it means |
|---|---|---|
| `raw_also_empty` | 829 | the source never published it |
| `SOURCE_THIN` | 681 | the mart carries every value raw has |
| `derived_in_model` | 399 | no raw parent column, built in SQL. **not value-checked** |
| `no_single_raw_parent` | 149 | mart joins several raw tables. **not value-checked** |
| `MODEL_LOST_IT` | 127 | raw holds values, a cast ate them |
| `ROW_SUBSET` | 9 | the mart holds fewer rows, and that explains it |
| `SENTINEL_SCRUBBED` | 3 | raw held placeholder junk, the model nulled it on purpose |

The 548 in the two "not value-checked" rows were classified from the model
graph, not from data. They are unverified, not proven dead.

## The 127 real losses, by mechanic

| count | bug | what raw actually holds |
|---|---|---|
| 52 | `try_to_date` with no format mask | `01-JUL-12`, `09-30-2003`, `8/2/2025 15:30` |
| 45 | numeric cast on a text column | `Yes`, `COALFLAG`, `F1`, `COST_S_1` |
| 14 | cast lives in a staging model, not the mart | `LOCAL_DATETIME` |
| 11 | `try_to_number` on a code | `IN`, `CA`, `US`, `HK` |
| 5 | `_source_run_id` hardcoded to null | a real uuid in raw |

Every format mask was tested against the real raw values before anything was
written. All 30 parse 100% of non-blank values.

## Result

| | |
|---|---|
| dbt model files edited | 47 |
| cast expressions rewritten | 122 |
| models rebuilt | 55 |
| columns now carrying values | 122, verified live |
| still empty | 5 |

### The 5 still empty, and why

| table | column | reason |
|---|---|---|
| `POLITICS__FED_CONGRESS_LEGISLATORS` | `LEGISLATOR_SET` | build blocked by the politics mirror guard |
| `HEALTH__FED_VA_SUICIDE_STATE` | `GENERAL_POPULATION_SUICIDES` | mart filters to one sheet, by design |
| `CORPORATE_REGISTRY__INTL_ES_BORME` | `PROVINCE` | mart holds 3 rows of 25 |
| `CORPORATE_REGISTRY__INTL_ES_BORME` | `ACT_DESCRIPTION` | same |
| `CORPORATE_REGISTRY__INTL_ES_BORME` | `PDF_URL` | same |

`LEGISLATOR_SET` is fixed in the model file. Running it is blocked by
`macros/guard_politics_mirror.sql`, standing policy `no_selectorless_dbt_build`.
That guard exists so a dbt run cannot overwrite audited OpenFEC/GovTrack
numbers. Overriding needs `--vars '{"allow_politics_rebuild": true}'` and a
deliberate decision.

## Column-name collisions

`FILING_DATE` is broken in PCAOB and correct in SEC 13F. A fix keyed on column
name alone would have broken the working one. Every fix is scoped to its own
model file through `scripts/dead_column_fix_scope.json`, built by walking the
dbt manifest.

## Two traps confirmed

- **NPPES `EIN`** reads 1,937,362 non-blank in raw. Every one is the literal
  text `<UNAVAIL>`. The staging model nulls it deliberately. The saved trap
  holds.
- **`distinct_ratio` in the profile can exceed 1.0.** It uses
  `approx_count_distinct`. NPPES `NPI` reads 9,631,613 distinct on 9,606,683
  rows, a 0.26% HLL overshoot. Do not use that ratio as an ID test without an
  exact count.

## Files

| file | what |
|---|---|
| `reports/catalog_profile_2026-09-08.csv` | every column, seven measures |
| `reports/dead_columns_2026-09-08.csv` | every dead column, verdict, raw values |
| `reports/dead_columns_recheck_2026-09-08.csv` | the 867 re-checked with exact counts |
| `reports/dead_column_fix_verified_2026-09-08.csv` | proof the 118 came back |
| `scripts/catalog_profile.py` | the profiler |
| `scripts/dead_column_diagnose.py` | mart against raw |
| `scripts/dead_column_values.py` | real raw values |
| `scripts/dead_column_recheck_38.py` | exact-count re-check, no sampling |
| `scripts/fix_dead_column_casts.py` | the fixer, scoped per file |
| `scripts/verify_dead_column_fix.py` | the proof |

## Known gaps

- 548 columns classified from the graph, never value-checked.
- The dead set is a floor. A column 98% null and 2% blank is invisible to the
  99% threshold.
- `PROCUREMENT__FED_USASPENDING_BULK` raw is exactly 50,000 rows. A round
  number on one table looks like the portal 10K-cap trap's bigger cousin, not a
  real landing. Not chased.
