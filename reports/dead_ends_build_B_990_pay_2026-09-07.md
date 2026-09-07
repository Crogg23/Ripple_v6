# Dead ends, build B: hospital Form 990 officer pay landed (2026-09-07)

Docket 124: "Wealthy nonprofit hospitals — how much do they pay their top executives?"
Scope report said: the pay sits inside each return's XML, Part VII Section A; nothing landed carries it. Pull the XML for the hospital slice, parse one row per person. This is that build.

## The short answer

| thing | number |
|---|---|
| hospital EINs in the slice (BMF NTEE E2x, full-form 990 in the index) | 3,987 |
| hospital returns in the slice | 32,963 |
| returns the IRS still hosts | 25,116 (object-id years 2019-2026) |
| returns landed | 23,810 |
| person rows landed | 526,374 |
| EINs covered | 3,918 of 3,987 (98.3%) |
| rows per return | 22 average |
| rows with any pay > 0 | 273,515 (52%) |
| rows flagged officer / key employee / highest paid | 262,171 |
| tax years | 2016 (17 returns) to 2025 (117), solid 2017-2024 |

**Bad news, up front.**
- **9,153 returns of the slice cannot be fetched.** 7,847 carry object ids 2016-2018: the IRS download page starts at 2019, the old `s3.amazonaws.com/irs-form-990` bucket answers 404, ProPublica's download-xml sits behind a bot wall. Another 1,306 carry 2022 object ids and are in no hosted zip (the 2022 folder is one file now, `2022_TEOS_XML_01A.zip`; it held 2,332 of the 3,662). Tax years before 2017 are essentially absent.
- **Ranking rows is not ranking people.** One executive appears on every affiliate's return: Skogsbergh 5 rows for 2024, Dean 3 rows a year, all the same dollars tagged "from related orgs". Group by person and year, take max, before naming anyone.
- **61 rows are group returns** ("Sanford Group Return", "BJC HEALTH SYS GROUP RETURN") where PERSON_NAME is the filer and the dollars are a whole system's officers on one line. The single biggest "person" row, $68.1M, is one of these. Filter `PERSON_NAME ilike '%group return%'`.

## What was found on irs.gov

`https://www.irs.gov/charities-non-profits/form-990-series-downloads` lists 68 zips at `https://apps.irs.gov/pub/epostcard/990/xml/<year>/`: 2019 and 2020 as 8 numbered parts plus a CT1 file, 2021 and 2022 as one file each (3.7 GB and 2.6 GB), 2023 on as one zip a month, some months split A-D. About 25 GB in all. No per-object URL exists any more.

Members are named `<OBJECT_ID>_public.xml`. `apps.irs.gov` honours HTTP Range (checked: `206 Partial Content`, `Accept-Ranges: bytes`). The loader reads each zip's central directory over Range, keeps the members whose object id is in the slice, and pulls those with one Range request each. 68 directory reads and 26,752 member reads instead of 25 GB.

## Landing

`scripts/irs_990_officer_pay_load.py`. Dry run default (parses 20, prints them, lands nothing), `--run` to land. CREATE TABLE IF NOT EXISTS, append via write_pandas. Resume: object ids already in the table are skipped; finished zips are in `logs/irs_990_officer_pay_checkpoint.json`. Progress line every 500 returns.

```
python scripts/irs_990_officer_pay_load.py --years 2024
  dry run: 20 returns parsed, 280 person rows, 0 empty, 0 errors, 1s

python scripts/irs_990_officer_pay_load.py --run
  hospital slice: 32,963 returns, 3,987 EINs, object-id years 2016..2026
  NOT HOSTED by the IRS: object-id years ['2016', '2017', '2018'], 7,847 returns.
  run: 23,922 returns parsed, 463,614 person rows, 2942 fetch/parse errors, 871s
  landed returns now in FED_IRS_990_OFFICER_PAY: 20,980 of 32,963 targets

python scripts/irs_990_officer_pay_load.py --run        # after the Deflate64 fix, resumed
  run: 2,830 returns parsed, 62,760 person rows, 0 errors, 286s
  landed returns now in FED_IRS_990_OFFICER_PAY: 23,810 of 32,963 targets
  [DQ OK] fed_irs_990_officer_pay/FED_IRS_990_OFFICER_PAY: 526,374 rows, density 0.4167
```

The 2,942 errors on the first pass were all one thing: `unsupported compression 9`. The 2020 CT1 zip and every 2025 and 2026 monthly zip are Deflate64, which zlib cannot inflate. Fixed with `pip install inflate64` and a branch in `fetch_member`; the checkpoint for those 25 zips was cleared and the second pass picked up 2,830 of them. The other 112 were retried inside the first pass's own retry loop and had landed already (23,810 - 20,980 = 2,830).

Table: `LIBRARY_RAW.LANDING.FED_IRS_990_OFFICER_PAY`. All VARCHAR: EIN, TAX_YEAR, TAX_PERIOD_END, TAX_PERIOD, OBJECT_ID, RETURN_TYPE, FILER_NAME, PERSON_SEQ, PERSON_NAME, TITLE, AVG_HOURS_PER_WEEK, AVG_HOURS_PER_WEEK_RELATED_ORG, six IS_* checkboxes ('X' or null), REPORTABLE_COMP_FROM_ORG, REPORTABLE_COMP_FROM_RELATED_ORGS, OTHER_COMPENSATION, SCHEMA_VERSION, SOURCE_ZIP, then INGESTED_AT (no underscore, as asked) and _SOURCE_RUN_ID. Two run ids. Logged to INGEST_RUNS as `fed_irs_990_officer_pay`.

## ID columns, checked before trusting

| column | what was checked | result |
|---|---|---|
| index OBJECT_ID | count vs distinct on FED_IRS_990_EFILE_INDEX | 5,544,626 / 5,544,626. Unique. The join key. |
| index RETURN_ID | same | 5,544,626 / 4,601,737. **Not unique.** Never join on it. |
| landed OBJECT_ID + PERSON_SEQ | groups with count > 1 | 0. Grain holds. |
| landed EIN | distinct raw vs distinct lpad 9, min/max length | 3,918 / 3,918, all 9 chars. Rows with no BMF match: 0. |
| PERSON_NAME | nulls | 0 of 526,374 (TITLE null on 47). |
| REPORTABLE_COMP_FROM_ORG | non-null values that fail try_to_number | 0. |

## dbt

| model | where | grain | rows |
|---|---|---|---|
| `stg_fed_irs_990_officer_pay__people` | LIBRARY_STAGING view | one (object_id, person_seq), newest load per object_id | 526,374 |
| `health__hospital_officer_pay` | LIBRARY_MARTS.HEALTH table | same, left-joined to BMF for hospital name, city, state, NTEE, asset and revenue | 526,374 |

Source declared in `models/staging/fed_irs_990_officer_pay/schema.yml`. Tests in `models/marts/health/schema_dead_ends_990_pay.yml`.

```
dbt run  --select stg_fed_irs_990_officer_pay__people health__hospital_officer_pay   # 2 success, 18s
dbt test --select stg_fed_irs_990_officer_pay__people health__hospital_officer_pay   # 11 tests, 11 pass
```

Counts through the Python door on the mart: 526,374 rows, 3,918 distinct EINs, 23,810 distinct returns, 0 rows without a BMF city.

## Top 20 paid people, one row per person per year

`max(total_compensation)` grouped by upper(person_name) and tax year, group returns excluded. `returns` is how many affiliate returns list that person that year.

| person | year | total comp | returns | hospital paying from org | title |
|---|---|---|---|---|---|
| KELBY KRABBENHOFT | 2020 | $44,353,819 | 4 | Sanford Health (SD) | PRESIDENT & CEO (THRU 11/20) |
| ROBERT I GROSSMAN MD | 2023 | $36,023,136 | 1 | NYU Langone Hospitals | EX-OFFICIO, DEAN & CEO |
| LLOYD H DEAN | 2021 | $35,462,873 | 3 | Dignity Health / CommonSpirit | CHIEF EXECUTIVE OFFICER |
| JAMES SKOGSBERGH | 2024 | $30,862,679 | 5 | Advocate Health Inc | CO-CHIEF EXECUTIVE OFFICER |
| LLOYD H DEAN | 2022 | $27,954,468 | 3 | Dignity Health | CEO THRU 7/31/22 |
| STEVEN J CORWIN | 2024 | $26,271,976 | 1 | New York-Presbyterian Hospital | PRESIDENT & CEO/TRUSTEE |
| EUGENE WOODS | 2024 | $25,781,275 | 1 | Advocate Health Inc | CHIEF EXECUTIVE OFFICER |
| MARNA BORGSTROM | 2022 | $23,675,898 | 2 | Yale New Haven Hospital | FORMER (VESTED DEFERRED) |
| ROBERT I GROSSMAN MD | 2022 | $22,767,598 | 1 | NYU Langone Hospitals | EX-OFFICIO, DEAN & CEO |
| JAVON BEA | 2023 | $22,757,779 | 1 | Mercy Crystal Lake Hospital | PRESIDENT/CEO |
| JAVON R BEA | 2023 | $22,757,779 | 4 | Mercy Health System Corp | PRESIDENT/CEO |
| LLOYD H DEAN | 2023 | $21,187,786 | 3 | Dignity Health | CHIEF EXECUTIVE EMERITUS |
| BLOM DAVID P | 2019 | $19,197,155 | 2 | OhioHealth Corporation | FRM CEO |
| ROBERT I GROSSMAN MD | 2021 | $19,104,692 | 1 | NYU Langone Hospitals | EX-OFFICIO, DEAN & CEO |
| EUGENE WOODS | 2023 | $18,576,902 | 1 | Advocate Health Inc | CO-CHIEF EXECUTIVE OFFICER |
| ERNIE SADAU | 2023 | $17,977,833 | 1 | Christus Health | PRESIDENT & CEO |
| ERNIE SADAU | 2021 | $17,916,470 | 1 | Christus Health | PRESIDENT & CEO |
| BERNARD TYSON | 2018 | $17,883,633 | 2 | Kaiser Foundation Health Plan of WA | Chairman & CEO |
| JAMES SKOGSBERGH | 2023 | $17,416,946 | 5 | Advocate Health Inc | CO-CHIEF EXECUTIVE OFFICER |
| KEVIN LOFTON FACHE | 2020 | $17,365,246 | 1 | CommonSpirit Health | FORMER CEO (THROUGH 6/30/20) |

Same person, two spellings: JAVON BEA and JAVON R BEA are one CEO on five returns. Name-keying is not done; the mart carries names as typed.

The biggest numbers are mostly departure years: Krabbenhoft left Sanford in Nov 2020, Dean stepped down mid-2022, Borgstrom is marked FORMER with vested deferred pay. A one-year max reads severance and deferred-comp payouts as salary. Look at the same person over three years before calling anything a pay rate.

## Traps found, all written to .claude/traps.md

- RETURN_ID in the 990 index is not unique (4.60M distinct on 5.54M rows); OBJECT_ID is.
- The IRS no longer hosts 2016-2018 XML; the 2022 folder is one zip holding 64% of the year's hospital returns.
- 2020 CT1 and all 2025-2026 zips are Deflate64 (method 9); zlib fails on every member.
- An executive repeats on every affiliate's return; group by person and year before ranking.
- Group returns put a system's whole officer pay on one PERSON_NAME line.

## Cost

Two loader passes, 871 s and 286 s, all outbound HTTP; the warehouse saw 22 write_pandas flushes and about 15 read-only count queries. dbt logged 18 s of build. No real number from the query log was pulled; call it "no real number for this" until priced.

No hook refused anything.

## Skeptic pass, 2026-09-07

Verdict DISAGREE on two numbers, build itself confirmed to the dollar. Fixed:

| finding | fix |
|---|---|
| headline $44.4M is a Schedule J pointer line, seq 14 "SEE SCH J, PART III"; the pay line, seq 13, reads $5.1M; 239 person-returns carry a pointer | mart gains `is_schedule_j_pointer`; rank with it false; trap written |
| group returns are 61, not 95, by the report's own filter | corrected here and in the docket; mart gains `is_group_return` |
| "three traps" was four lines | noted |
| docket time window said 2017-2024; table holds 2016 and 2025 thinly | docket row corrected |

Blind spot the tests cannot see: `person_seq` is minted by the parser, so the uniqueness test can never fail. No test compares a parsed dollar to anything outside the parser.
