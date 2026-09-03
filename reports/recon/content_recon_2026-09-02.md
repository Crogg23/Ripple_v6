# Content recon, mission one — 2026-09-02, elucidated 2026-09-03

Chris's ask, verbatim: "delta force level reconnaissance on what is even out there in the first place ...
we need to inspect the CONTENT of the warehouse." Then "1 and 2 - full send", then "go".

Every finding below walks its chain: what was checked, what a hit means, what a miss means.

## 1. What ran

| item | value | how we know |
|---|---|---|
| scope | 2,208 base tables in LIBRARY_RAW.LANDING, 1.34B rows, 96 GB, 79,007 columns | information_schema.tables and .columns |
| door | Python scripts, read-only | every statement is a SELECT; no DDL, no DML |
| pages | 2,208 json + 2,208 md | file count in reports/recon/content/json and /pages |
| query time | 2.85 hours | sum of per-table seconds in index.csv |
| cost | 5.47 credits on COMPUTE_WH in the first 5 hours ≈ $11 at the $2 default | warehouse_metering_history, queried in session; not re-checkable from the repo |
| estimate given | ~$7, ~3.5 hrs | over by ~$4: three classifier reruns plus idle billing between small queries |

Runs: one client-side hang on FDA MAUDE (no query reached the warehouse), one silent exit after one table,
three reruns after classifier fixes (397, 395, 287 tables). Resume-safe by json presence.

## 2. The atoms — chain for each

| atom | what was checked | a hit means | a miss means |
|---|---|---|---|
| scan | per column, one pass per table: approx distinct, blank count, top 12 values on first 200 chars | we hold the actual values | column is all blank |
| type | top values matched to date shapes, number shape, US state set; names only break ties | date / amount / state / who by content | free text, or the name lied |
| when | rows per year, year pulled by the detected format | the table's curve | dates unparseable, page shows raw values |
| how big | count, min, median, p99, max, sum via try_to_number | the spread | text junk is null, not zero |
| who | top 20 by rows; top 20 by dollars when an amount exists | the players | no name-like column |
| who x when | each top name, rows and dollars per year | a name's own curve | no parsed date; 851 pages fall back to the load stamp, now labelled |

Why content-first was forced: 78,074 of 79,007 landing columns are TEXT. TRANSACTION_DT held `09302024`.
INGESTED_AT held `1788291300090871`. Names cannot tell them apart; values can.

## 3. Cliffs — big tables whose curve stops years ago

| table | column | first | last | rows |
|---|---|---|---|---|
| FED_DEA_ARCOS_FULL | TRANSACTION_DATE | 2006 | 2012 | 178.6M |
| FED_FDA_FAERS_DEMO | FDA_DT | 2003 | 2014 | 5.8M |
| FED_FJC_IDB_CRIMINAL | C_UPDATE | 1993 | 2012 | 6.3M |
| FED_DOL_OFLC | CASE_SUBMITTED | 2012 | 2019 | 665K |
| FED_SENATE_LDA_FILINGS | TERMINATION_DATE | 2001 | 2021 | 831K |

- Checked: rows per year on the column; last year holding ≥5% of the peak year; table ≥10K rows.
- Hit: the load is an old vintage. ARCOS is the 2006 to 2012 public release, nothing newer was ever landed.
- Miss: the world did not stop. Skeptic caught FAERS: REPT_DT runs to 2016; only the FDA receipt date ends 2014. LDA has a stray 2030 row.
- Use: any chart on these five must state the vintage in the title.

## 4. Spikes — one year at 3x both neighbours

| table | column | year | rows | before | after | plain read |
|---|---|---|---|---|---|---|
| FED_FEMA_IA_HOUSING_REGISTRATIONS | APPLIEDDATE | 2005 | 3.08M | 265K | 184K | Katrina, real |
| FED_COURTLISTENER_OPINION_CLUSTERS | DATE_MODIFIED | 2024 | 7.42M | 107K | 334K | a bulk re-edit stamp, not new opinions |
| FED_FEC_INDEPENDENT_EXPENDITURES | EXP_DATE | 2024 | 44.5K | 3.2K | 2.3K | election year, real |
| FED_SAM_EXCLUSIONS_FULL_R2 | CREATION_DATE | 2012 | 88K | 93 | 4.4K | system migration stamped everything 2012 |
| FED_DOL_OFLC | PERIOD_OF_EMPLOYMENT_START_DATE | 2019 | 554K | 34K | 13K | last loaded year, see the cliff |

- Checked: a year with ≥10K rows and ≥3x both the year before and after.
- Hit: either an event in the world or an event in the system. The column name separates them: APPLIEDDATE and EXP_DATE are world; DATE_MODIFIED and CREATION_DATE are system.
- Miss: flat curves are boring by design and are not listed.

## 5. Largest sums — which are money and which are not

| table | column | sum | read |
|---|---|---|---|
| FED_USASPENDING_CONTRACTS_FULL_R2 | FEDERAL_ACTION_OBLIGATION | $11.4T | real, 2006 to 2026, 93M rows |
| FED_BLS_QCEW | TOTAL_ANNUAL_WAGES | $382T | not a total; county × industry × year rows also carry state and national rollups, the same wage lands many times |
| FED_SEC_13F_HOLDINGS | VALUE | $659T | not a total; quarterly snapshots, the same position every quarter |
| FED_SEC_13F_HOLDINGS | SSHPRNAMT | 1,853T | shares, not dollars |
| FED_FRACFOCUS_REGISTRY | MASSINGREDIENT | 21,392T | pounds, not dollars |
| FED_TREASURY_DEBT_TO_PENNY | TOT_PUB_DEBT_OUT_AMT | 124,951T | daily balance summed over 8,300 days; the real number is max $39.3T |

- Checked: sum over the column with try_to_number.
- Hit: a real dollar total only when one row is one event. Contracts obligations pass that test.
- Miss: snapshot tables, rollup tables, and non-dollar quantities all produce huge meaningless sums. The digest section is now titled "largest numeric sums" for this reason.

## 6. Weird max — one row breaks the column

| table | column | max | p99 | ratio | read |
|---|---|---|---|---|---|
| FED_SEC_INSIDER_DERIV_TRANS | CONV_EXERCISE_PRICE | 400B | 343 | 1.2Bx | one row; pull it |
| FED_FRACFOCUS_REGISTRY | MASSINGREDIENT | 18,792T | 105.6M | 178Mx | one row, unit slip |
| FED_FJC_IDB_BANKRUPTCY | SECURED, REALPROP, UNSECPR, PERSPROP | 999,999,999,999.99 | ~1M | ~1Mx | four columns share the field's max value; a bracket ceiling, not money. TOTASSTS 2T and TOTLBLTS 3T are derived from them |
| FED_USASPENDING_CONTRACTS_FULL_R2 | HIGHLY_COMPENSATED_OFFICER_1_AMOUNT | 33.2T | 8.7M | 3.8Mx | a typo or cents-as-dollars |
| FED_FDA_FAERS_DRUG | DOSE_AMT | 5.7B | 2,000 | 2.9Mx | unit confusion, mg vs µg |
| FED_FEC_INDIV_CONTRIBUTIONS | TRANSACTION_AMT | 100M | 3,000 | 34Kx | real or a slip; pull the row |

- Checked: max divided by the 99th percentile on the same column, n ≥ 1,000.
- Hit: ≥1000x means one row, not a distribution. Four identical maxes across sibling columns means a field ceiling.
- Miss: a column whose max is under 1000x p99 has a fat tail, not a broken row, and is not listed.
- Skeptic corrected the FJC figure from "exactly 1000B" to 999,999,999,999.99.

## 7. Names that cross rooms — gen 3 emerging from gen 1

| name | tables | rooms |
|---|---|---|
| TENNESSEE VALLEY AUTHORITY | 12 | every EIA 860 and 861 form |
| WALMART STORES EAST LP | 10 | ATF gun licenses, CMS provider rolls, OSHA injuries |
| AMERICAN LEGION | 8 | IRS charities, revocations, Pub 78 |
| SELF EMPLOYED | 8 | FEC and NYC campaign finance; an employer placeholder, not an entity |
| SHELL OIL CO | 6 | EPA ECHO, FRS, RCRA, corporate crosswalk |

- Checked: each page's top-20 names, upper-cased, punctuation stripped, ≥2 words; same string in ≥3 non-portal tables.
- Hit: one entity holds a file at several agencies. Walmart sells guns, bills Medicare, reports injuries.
- Miss: absence means the agencies spell it differently, the Utah trap at warehouse scale. Counts are floors: exact string match only, no variant folding.
- Residue: place strings like UNITED STATES and address strings like 4TH FLOOR still slip in.

## 8. Traps found, saved to .claude/traps.md and memory

| trap | checked | hit means |
|---|---|---|
| PORTAL_ tables cap at 10,000 rows; 169 of 1,563 sit exactly there | information_schema row_count | those 169 are samples; any count is a floor |
| _INGESTED_AT reads year ~56,660,000 on 11 tables | year() threw on them | epoch microseconds stamped as seconds; never use it as a date unguarded |
| ArcGIS portal dates are epoch milliseconds with a trailing .0 | top values like 1555977600000.0 | a bare sum reads as trillions; divide by 1000, dateadd from 1970 |
| Open Payments ..._MAKING_PAYMENT_ID is a 12-digit id | top values 100000000xxx | the name says PAYMENT; the content says id |

## 9. Known holes, not fixed

- Caps of 6 dates, 6 amounts, 4 whos per table: ~11.8K classified columns were never queried. "12 unreadable" means 12 of the columns we queried.
- 9.2% of who picks are city, state, or street columns; the exclusion list only sorts, never filters.
- Subtotal and memo traps are not applied: House sums include TOTALS rows, FEC itoth sums include 15J memos. Pages show raw.
- Three tables have zero rows; their pages exist and are empty.
- Cost figure not re-checkable from the repo.

## 10. Skeptic verdict, 2026-09-03 — DISAGREE, resolved

| claim | verdict | fix |
|---|---|---|
| FAERS ends 2014 | wrong as stated; only FDA_DT | corrected in section 3 |
| FJC "exactly 1000B" | wrong; 999,999,999,999.99 | corrected in section 6 |
| gen 2 curves | 851 of 1,950 ran on the load stamp unlabelled | pages now say LOAD STAMP, not an event date |
| money section | ~13 of 40 rows not dollars | retitled, epoch columns dropped, section 5 says which |
| "12 unreadable" | survivorship | restated in section 9 |
| spikes, names, portal cap, TEXT count | exact | none |

Both verdicts stand; Chris decides.

## 11. Not done
Gens 3, 4, 5. Nothing committed; new files: scripts/content_recon.py, scripts/content_recon_digest.py, reports/recon/content/, this file, four trap lines.
