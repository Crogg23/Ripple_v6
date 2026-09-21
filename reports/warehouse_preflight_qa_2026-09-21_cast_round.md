# Mart cast guard round — 2026-09-21

Chris said go on the skeptic's finding that live marts still read `source()` with bare casts.
File edits only. No dbt run or build, no warehouse write. Tool: `scripts/guard_mart_casts.py`, dry run by default.

## What counts as bare, tested live through the Python door

| Cast | Input | Came back | Verdict |
|---|---|---|---|
| try_to_double | 'nan' | NaN | bare, use stg_float |
| try_to_number, no scale | '1.5' | 2 | bare, use stg_int or stg_float |
| try_to_date, no format | '2015' | a day in 1970 | bare, use stg_date |
| try_to_date, 'MMDDYYYY' | '2015' | 0005-02-01 | bare, use stg_date with format |
| try_to_timestamp_tz, no format | '2015' | 1970-01-01 00:33:35 | bare, use stg_ts or stg_ts_tz |
| try_to_date with a separator format, 'YYYYMMDD', 'DDMONYYYY', 'YYMMDD', 14-digit wayback | '2015' | NULL | safe, left alone |
| try_to_decimal(x, 18, 2) | 'nan' | NULL | safe, left alone |
| try_to_date, 'YYYY' | '2015' | 2015-01-01 | see note below |

'YYYY' note: one use, `economics__fed_irs_990_efile_index.sql` line 34, last in a coalesce behind two real
formats, on purpose, for year-only SUB_DATE values. `try_to_date('12','YYYY')` reads year 12, so a junk
value would land there. Left as is; the file carries a 2026-08-18 review comment. Skeptic flagged it.

## What changed

223 casts in 26 enabled mart files: 213 by script, 10 by hand (4 assistance dates, 5 GLEIF timestamps,
1 debt-cliff year). A one-argument try_to_number became stg_float only where the live column holds a
fraction today (one column: Part D `Tot_30day_Fills`); every other one became stg_int.

The skeptic's earlier "41 marts" counted separator-format casts too. Those test safe above, which is why
26 files were edited and not 41. After: the script finds 0 bare casts. The looser audit detector still
lists 55 lines in 26 files; every one is a separator format, an explicit scale, or inside a regexp guard.

`dbt compile`: 208 of 208 nodes on the 26 models, then 38 of 38 on the 4 re-edited ones. The skeptic
re-ran the whole project: 9,727 of 9,727. A compile proves parsing only.

## Old cast vs new cast on live source rows

Numbers and dates, 195 casts, every row of each source table. Lost = old gave a value, new gives NULL.
Changed = both give a value and they differ.
- 0 lost and 0 changed on 22 files. ARCOS by hand: 0 lost on all 178,598,026 rows.
- USASpending contracts_full: 2,494,957 lost, every one the string 'NAN' that the old cast read as a
  float NaN (`cost_accounting_standards_clause` 2,494,954, two other columns 3). The guard working.
- Part D prescribers `Tot_30day_Fills`: 5,996,738 of 25,869,521 rows changed. The old cast rounded
  12.2 to 12 on the live mart. The new one keeps the fraction.
- Not compared: `money__debt_repayment_cliff`, 1 cast on an unpivot alias.

## Skeptic pass — DISAGREE, and it was right

The first comparison rendered `stg_ts` wrong in the checker and compared timestamps by instant. Snowflake
compares TIMESTAMP_TZ to TIMESTAMP_NTZ by instant, so a moved printed date reads as equal. Two misses:
- GLEIF: `stg_ts` moves an offset value to UTC. GLEIF writes local midnight, `2012-07-25T00:00:00+02:00`,
  so 1,070,259 of 3,382,301 creation dates printed one day earlier, and the column type went TZ to NTZ
  under a select-star public view.
- USGS water: dropping the outer convert_timezone changed 64,860 offset-less rows by 7 or 8 hours.

Fix: new macro `stg_ts_tz` in `macros/staging_casts.sql`. Same epoch guard, keeps the offset and the
TIMESTAMP_TZ type. Used in `economics__intl_gleif` (5), `economics__intl_gleif_relationships` (13), and
inside the original convert_timezone in `environment__fed_usgs_water` (1). A cast-guard round should not
move values; whether USGS offset-less rows SHOULD take the session zone is a separate question, untouched.

Re-check by PRINTED value, `to_char` old vs new, every row:

| Cast | Rows | Lost | Printed differs |
|---|---|---|---|
| GLEIF, 5 columns | 3,382,301 | 0 | 0 |
| GLEIF relationships, 6 columns | 485,285 | 0 | 0 |
| USGS water DATETIME | 6,694,816 | 0 | 0 |
| Wayback DOJ deep pages, listing; DOJ Epstein library | 2,542; 24,897; 777 | 0 | 0 |
| NOAA AIS basedatetime, in lead_queue | 58,106,517 | 0 | 0 |

## Live build, 2026-09-21 — Chris gave `greenlight rebuild` after a price

Price shown first, from the query log: ARCOS mart 3.7 min typical and 13.5 max, $0.12 typical and $0.45 max;
any other mart under a minute. X-Small, $2 a credit is the script default, not the contract rate.

`dbt build` on 28 marts, log in `outputs/cast_round_build_2026-09-21.log`:
224 nodes, 209 success, 3 warn, 5 error, 7 skipped, 5m 48s. ARCOS took 4m 36s.
- 2 of the 5 errors: `politics__fed_doj_epstein_library` and `politics__member_voting_record`, refused by
  `guard_politics_mirror`. By design. Their cast edits are moot at the served layer. The 7 skips are their tests.
- 3 of the 5 errors: mart-level `not_null` on HUDOC `appno` 57, `ecli` 2,334, `country` 4. Same cause as
  the staging copies of these tests fixed 2026-09-20: written against the 2,000-row sample, now facing
  real source nulls in 211,778 rows. Set to `severity: warn` with the count on each.

Served tables, read live after the build:

| Check | Before | After |
|---|---|---|
| BJS mart rows | 1,000 | 68,852 |
| HUDOC mart rows | 2,000 | 211,778 |
| USASpending contracts_full, NaN in `cost_accounting_standards_clause` | 2,494,954 | 0 |
| Part D `total_30day_fills` rows keeping a fraction | 0, all rounded | 5,996,738 of 25,869,521 |
| ARCOS rows | 178,598,026 | 178,598,026; dates 2006 to 2012; 5 null dates, same 5 as the old cast |
| GLEIF creation date type | TIMESTAMP_TZ | TIMESTAMP_TZ |

The build broke two views, found by the shelf probe, not by dbt: public `JUSTICE.ECHR_COURT_CASES` and
timeline `CRIMINAL_JUSTICE__FED_BJS_DATA` would not fetch. Cause: `_INGESTED_AT` on `INTL_HUDOC_FULL` and
`FED_BJS_DATA_FULL` is a TIMESTAMP that swallowed epoch micros as seconds, year 56 million. The capped
sample tables never had it. Same bug and same fix as the USAspending R2 clock on 2026-09-20:
`landing_parse_audit_epoch('date_part(epoch_second, _INGESTED_AT)')` in both staging models.
Second build, 5 models: 33 nodes, 21 success, 12 warn, 0 error. After: HUDOC stamps 2026-09-07 23:43 to 23:47,
BJS 2026-09-07 23:17, 0 null. Public shelf 254 of 254 and timeline shelf 405 of 405 open with a real fetch.
The landing loader that writes that stamp wrong is still unfixed; the next `_FULL` reload will do it again.

### Skeptic pass on the live build — AGREE on 7 claims, DISAGREE on one, fixed

Held, re-run by the skeptic: BJS 68,852 and HUDOC 211,778 match landing, HUDOC count equals distinct
CASE_ID; 0 NaN left; Part D 5,996,738 of 25,869,521 exact; ARCOS 178,598,026 rows, 2006 to 2012, 5 null
dates, sum of total_mme 955,923,726,992.69; GLEIF still TIMESTAMP_TZ; both repaired views fetch;
no filled column went NULL in QCEW, NPDB, ECHO or PPP. Its own full 659-view sweep did not finish.

Broken: the HUDOC warn notes said 57, 2,334 and 4 missing. Those were true NULLs only. `not_null` cannot
see an empty string and staging passed the three columns straight through. Blank or null is 184, 54,529
and 11; a quarter of the table has no ECLI. Fixed: `null_junk()` on APPNO, ECLI, COUNTRY in the staging
model, counts corrected in `schema.yml`, staging and mart built again. Live after: mart nulls read
184, 54,529, 11, and 0 blank ECLI left. The public view still fetches.

Also from the skeptic:
- `ENVIRONMENT__EPA_PENALTY_GAP` is a table that reads the ECHO mart and was not in the 28. Built again, 93,808 rows.
- OPEN: Snowflake froze column types in the catalog for two public views. `COMPANIES.INTL_GLEIF` lists 5 date
  columns as TEXT and `JUSTICE.ECHR_COURT_CASES` lists `_INGESTED_AT` as NUMBER. Queries return the right
  types. Anything that reads the catalog, such as the schema generation tool, gets the wrong ones until
  the two views are recreated.
- Blind spots named: a one-row fetch cannot see a type change or an all-NULL column, and neither probe
  touches the 36 base tables in the TIMELINE schema.

### Stale catalog types on the public shelf — closed, Chris said go

Snowflake stores a select-star view with its column list and types frozen at creation. When the mart under
it changes a column's type, queries return the new type but `information_schema.columns` keeps the old one.
What was checked: every THE_LIBRARY view whose body is a plain `select * from LIBRARY_MARTS.x.y`, 95 of 254,
catalog type per column against the mart's. A hit means a catalog reader gets the wrong type. A miss means
the two agree; it says nothing about the other 159 views, which are typed projections or read landing.

Found 11: the skeptic's 2 (COMPANIES.INTL_GLEIF, JUSTICE.ECHR_COURT_CASES) plus 9 from the 2026-09-20 cast
rebuilds: SANCTIONED_PARTIES, TREASURY_INTEREST_RATES, BANNED_HEALTHCARE_PROVIDERS, CLINICAL_TRIALS,
FOREIGN_AGENT_REGISTRATIONS, FOREIGN_AGENTS, AG_MULTISTATE_SETTLEMENTS, INTRA_AMERICAN_SLAVE_VOYAGES,
HEALTHCARE_PROVIDERS. All 11 recreated with `scripts/repair_library_views.py`'s own planner: same body,
comment kept, COPY GRANTS, column count unchanged on every one, grants identical before and after, each
fetches a real row. Rollback DDL: `outputs/library_view_rollback_catalog_types_2026-09-21.sql`, names
unqualified. Sweep re-run after: 0 of 95 stale.

OPEN, found by the same sweep:
- Three ID columns are FLOAT in their marts since the 2026-09-20 cast wave: `JUSTICE__FED_OFAC_SDN.ENT_NUM`,
  `FOREIGN_INFLUENCE__FED_FARA_BULK.REGISTRATION_NUMBER`, `FINANCE__FED_FARA.REGISTRATION_NUMBER`.
  The project ruling of 2026-09-19 says an ID stays TEXT via `stg_id_text`.
- The ECHR_COURT_CASES catalog comment still says "sample of European human-rights cases (2,000 rows)" and
  "Thin sample". The view now serves 211,778 rows. Comment, FRIENDLY_LAYER row and names file all carry it.

### IDs stored as FLOAT — closed live, Chris said go

Correction to the note above: these casts are `ripple_num`, a bare try_to_double, dated 2026-08-22 by git.
They did not come from the 2026-09-20 cast wave.

What was checked: every `ripple_num` call in a mart whose column name looks like an ID, 13 columns, profiled on
landing: filled, distinct, not-whole values, leading zeros, digits past 15. A FLOAT drops a leading zero and
cannot hold more than about 15 digits. 11 of the 13 are IDs and moved to `stg_id_text`, TEXT, in 7 marts:
TRI 2023 parent D&B numbers x2 and document control number; FEC committee-to-candidate IMAGE_NUM, FILE_NUM;
FEC independent expenditures IMAGE_NUM, FILE_NUM, PREV_FILE_NUM; FARA bulk registration_number; HCRIS
rpt_rec_num; FAERS drug NDA_NUM; OFAC ent_num. Left alone: Senate eFD `LINE_NO`, a line counter 1 to 99.

Damage measured in the served marts BEFORE the build:
- FEC committee-to-candidate IMAGE_NUM is 18 digits. 472,813 distinct image numbers in landing had collapsed
  to 60,751 in the mart; 839,829 of 866,730 rows printed a different number than the source.
- FEC independent expenditures IMAGE_NUM: 143,486 distinct in landing, 30,929 in the mart.

Build, 7 marts plus `finance__fed_fara`, log `outputs/id_text_build_2026-09-21.log`: 41 nodes, 39 success,
2 warn, 0 error, 19.7s. AFTER, read live: c2c IMAGE_NUM 472,813 distinct and 0 rows missing from landing;
independent expenditures 143,486; TRI parent D&B leading zeros 31,729 of 31,729 kept; FAERS NDA_NUM
leading zeros 3,713,099 of 3,713,099 kept, 5,453,859 filled both sides; OFAC 19,114 rows and 19,114 distinct;
HCRIS 80,077 and 80,077. Public shelf 254 of 254, timeline shelf 405 of 405, real fetch. The type change made
5 more select-star public views stale in the catalog; recreated the same way, grants identical, all fetch.

Still FLOAT: `FINANCE__FED_FARA.REGISTRATION_NUMBER`, a 30-row table where the landing column is blank on
every row, and two `__PREV_20260906` backup tables, which nothing serves.

## Not in scope

The 13 politics marts stay blocked by
`guard_politics_mirror`, so the `politics__member_voting_record` edit is moot at the served layer.
Skeptic also counted 78 same-shape casts in marts that read `ref()`, not `source()`, for example
`immigration__fed_eoir_cases.sql` lines 24 to 47. Whether the staging view under each is guarded was not checked.
