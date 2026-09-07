# Dead ends, scope B: four docket lines where data landed but is unusable

2026-09-07. Read-only pass through the Python door (`connect.db`). No writes.
Lines: docket 124, 143, 144, E75. Each one: what physically sits in the table, what code exists, the fix, the size.

## The short table

| id | line | what is physically wrong | fix | size | effort |
|---|---|---|---|---|---|
| 144 | Immigration judges | 12.63M rows, one column, 39 tab-separated fields each. It is `A_TblCase` only. Judge and decision live in `B_TblProceeding`, which never landed (zip largest-member trap). NUL bytes inside fields. | (1) warehouse SQL split of the existing column into 39 columns; (2) reload the FOIA zip keeping every member, at least `B_TblProceeding` | 12.6M rows now; proceedings file roughly the same order | small for (1), medium for (2) |
| 124 | Hospital exec pay | Index only. 5.54M rows of EIN + return id + XML object id. No dollar column anywhere. The 200-row `FED_IRS_990` has an `OFFICERCOMPENSATIONAMT` column that is blank on all 200 rows. | new load: IRS 990 XML zips, parse Part VII (person, title, comp) for hospital EINs picked by the index | 32,963 hospital 990 returns, 3,987 EINs; roughly 10-20 people each, so 300K-700K pay rows | large |
| 143 | Trial doctors vs drug money | 500 rows. One API page. ClinicalTrials.gov has about 550K studies. Investigator names are already in the rows (JSON in `LOCATIONS` and `RESPONSIBLE_PARTY`), 226 of 500 carry one. No NPI. | reload through the v2 API with paging (1,000 per page), then a warehouse FLATTEN of the `LOCATIONS` JSON for investigator name + facility; name-match to Open Payments | about 550K studies; a few million investigator-site rows after flatten | medium |
| E75 | Nursing home chains and COVID money | 45 rows. They are the website's navigation menu (`About TAGGS`, `Sitemap`, `Award Search`...). Every data column is blank, `RECIPIENT_EIN` included. Registry already retired it 2026-07-24. | new source: HRSA Provider Relief Fund public payment file (provider name, city, state, amount; no EIN). Match by facility name + city to `NURSINGHOME411`, roll up by `CHAIN_ID` | a few hundred thousand payment rows; 14,713 homes, 10,162 with a chain id | medium |

Bad news up front: none of the four is a one-line fix. Two need new downloads (124, E75), one needs a full API crawl (143), one can be half-fixed in SQL today (144).

---

## 144 — EOIR immigration court cases

**Docket says:** `IMMIGRATION__FED_EOIR_CASE_DATA`, 12,631,225 rows, "the case data isn't usable yet".

**Landed table:** `LIBRARY_RAW.LANDING.FED_EOIR_CASE_DATA`. Columns: `CASE_TYPE`, `_INGESTED_AT`, `_SOURCE_RUN_ID`, `_SRC_SHA256`. The mart view has one column, `CASE_TYPE`.

```sql
select regexp_count(CASE_TYPE, '\t') as tabs, count(*) from LIBRARY_RAW.LANDING.FED_EOIR_CASE_DATA group by 1 order by 2 desc
-- 38 tabs: 12,631,125   39: 96   40: 2   45: 1   46: 1
```
39 fields on 99.999% of rows. The 100 odd rows have a tab inside a free-text field.

**What the 39 fields are.** The sample row matches the EOIR FOIA file `A_TblCase` field for field:

```
3982131  EL PASO  TX  79925  ''  ''  MX  SP  D  ' '  2001-05-24  01  RMV  EPD  2001-06-08  0900  M ...  N/A
f1 IDNCASE  f2 ALIEN_CITY  f3 ALIEN_STATE  f4 ALIEN_ZIPCODE  f7 NAT  f8 LANG  f9 CUSTODY
f13 CASE_TYPE  f14 UPDATED_SITE (court code)  f15 LATEST_HEARING  f16 LATEST_TIME  f39 last flag
```

Checks that pin it:
```sql
select split_part(CASE_TYPE,'\t',13), count(*) ... -- RMV 10,883,997 | DEP 1,093,156 | CFR 209,364 | EXC 204,041 | DDC 129,329  (case types)
select split_part(CASE_TYPE,'\t',14), count(*) ... -- MIA 850,958 | NYC 812,576 | WLA 586,435 | CHI 500,642 | ORL 445,473  (court codes)
select split_part(CASE_TYPE,'\t',9),  count(*) ... -- N 8,197,201 | D 2,954,594 | R 1,348,821  (custody: never / detained / released)
select count(distinct split_part(CASE_TYPE,'\t',1)) ... -- 12,631,225 = row count. Field 1 is the unique case id.
select max(try_to_timestamp(split_part(CASE_TYPE,'\t',15))) ... -- 2040-05-09 (future hearing dates exist), min 1953-08-05
```
No header row survived: `where CASE_TYPE ilike '%IDNCASE%'` returns 0. The loader ate the header and named the whole line after its 13th field.

**Hazard:** NUL bytes. Field 10 holds `\x00` on 4,264,379 rows; field 20 on 622,565; fields 36-37 on about 22K. Any parser must strip `\x00` before trimming. Fields 36-37 (detention facility, about 24K non-blank: `TDCJ`, `Red Rock Correctional Center`, `Eloy Arizona`) are mostly empty; the case file's detention picture is the `CUSTODY` flag, not a named facility.

**What is missing for the question.** The docket asks "by judge". `A_TblCase` has no judge. The judge code (`IJ_CODE`), decision code, and hearing location sit in `B_TblProceeding` and `tbl_schedule` in the same FOIA zip. One `_SOURCE_RUN_ID`, one `_SRC_SHA256`, and only one EOIR table in LANDING: the zip loader kept its largest member and dropped the rest (traps.md 2026-08-31).

**Code:** nothing in `scripts/` or `connect/` touches EOIR. The dbt chain (`landing_clean__fed_eoir_case_data.sql`, `staging/fed_eoir_case_data/stg_fed_eoir_case_data__records.sql`, `marts/immigration/immigration__fed_eoir_case_data.sql`) passes the one column through untouched; the staging model says "GRAIN: NOT YET DETERMINED". The only prior split is a retired July chart card, `_JUNK_DRAWER/retired_2026-08-30/investigations/proof_growth_2026-07-03/q03_eoir_tab_split.py`, which did `SPLIT_PART(CASE_TYPE, CHAR(9), 3)` for the state map. Same mechanic as fix (1), never made it into a model. Registry row `fed_eoir_case_data` points at the FOIA library page, not the zip.

**Fix, two parts:**
1. Warehouse SQL, now: a view over the existing column, `split_part(replace(CASE_TYPE,'\x00',''), '\t', n)` for n in 1..39, named from the EOIR data dictionary. 12.6M rows. Small. Gives court, custody, case type, nationality, hearing date. No judge yet.
2. Reload the FOIA zip with a loader that keeps every member (or at least `B_TblProceeding`, `tbl_schedule`, `tblLookupBaseCity`, `tblLookup_Judge`), tab-delimited, with a real header. Python-side download, warehouse COPY. Proceedings file is the same order of size as cases. Medium. Gated: it is a reload into LANDING.

---

## 124 — Wealthy nonprofit hospitals, executive pay

**Docket says:** `ECONOMICS__FED_IRS_BMF` + `ECONOMICS__FED_IRS_990_EFILE_INDEX`, 7,519,456 rows, "the pay data isn't in a usable format yet".

**Landed tables:**
- `FED_IRS_990_EFILE_INDEX`, 5,544,626 rows. Columns: `RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, SUB_DATE_RAW, TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID`. That is the whole list. No money column of any kind.
- `FED_IRS_BMF`, 1,974,830 rows. Has `ASSET_AMT, INCOME_AMT, REVENUE_AMT` (org totals) and `NTEE_CODE`. No pay.
- `FED_IRS_990` (LANDING), 200 rows. This one has the right header: `OFFICERCOMPENSATIONAMT, TOTALREVENUEAMT, TOTALEXPENSESAMT ...` but:

```sql
select count(*), count_if(nullif(trim(OFFICERCOMPENSATIONAMT),'') is not null), count_if(nullif(trim(TOTALREVENUEAMT),'') is not null) from LIBRARY_RAW.LANDING.FED_IRS_990
-- 200, 0, 0
```
All 200 rows are 2026 index entries with the financial columns blank. It is a 200-row test load of the index wearing a wider header (`scripts/sprint_a_specs.py` line 85 says as much: "replaces 200-row test load").

**Where the pay actually sits:** inside each return's XML, Form 990 Part VII Section A (`Form990PartVIISectionAGrp`: `PersonNm`, `TitleTxt`, `ReportableCompFromOrgAmt`, `ReportableCompFromRltdOrgAmt`, `OtherCompensationAmt`). Also Schedule J for the top earners. Nothing landed carries it. The registry row `fed_irs_990` says it: "the raw XML is required for granular financial line items."

**How big the hospital slice is:**
```sql
select count(distinct i.EIN) from ..._990_EFILE_INDEX i join ..._FED_IRS_BMF b on b.EIN=i.EIN where b.NTEE_CODE like 'E2%' and i.RETURN_TYPE='990'   -- 3,987 EINs
select count(*) ...same join...                                                                                                             -- 32,963 returns
select RETURN_TYPE, count(*), min(TAX_PERIOD), max(TAX_PERIOD) from ..._990_EFILE_INDEX group by 1
-- 990 2,620,469 (200108..202609) | 990EZ 1,503,577 | 990PF 904,261 | 990O 228,639 | 990EO 140,343 | 990T 117,252 | 990PR 30,085
```
NTEE `E2x` = hospitals. Full-form 990 only (EZ and PF do not file Part VII the same way).

**Code:** `scripts/irs_bulk_discover_load.py::_load_990_index` loads index CSVs for 2022-2023 into `FED_IRS_990_EFILER_INDEX_<year>` (a different table name; not what is in LANDING). `scripts/server_side_specs.py` line 349 holds the manifest of index CSVs 2017-2026. No XML parser anywhere in live code. Registry note: "Full XML parse is a separate build."

**Fix:** new source. Download the IRS annual 990 XML zips (irs.gov form-990-series-downloads; each year is several multi-GB zips), open only the files whose name matches an `OBJECT_ID` from the hospital slice, parse Part VII with an XML reader, write one row per person per return. Python-side parse, then COPY to a new LANDING table. The `OBJECT_ID` column is the join back to the index. Roughly 33K returns x 10-20 listed people = 300K-700K rows. Large: the download is the cost (tens of GB across years), the parse itself is a few hundred lines. No prior run in the query log, so no real number for the load cost.

Cheaper first cut, if wanted: ProPublica Nonprofit Explorer API returns per-filing `compnsatncurrofcr` (total officer comp) for an EIN. 3,987 calls, one small table. Gives "how much in total", not "who".

---

## 143 — Companies running trials paying the same doctors

**Docket says:** `HEALTH__FED_CLINICALTRIALS` + `HEALTH__FED_CMS_OPEN_PAYMENTS`, 15,385,547 rows, "the detailed trial data isn't loaded".

**Landed table:** `FED_CLINICALTRIALS`, 500 rows, one `_SOURCE_RUN_ID`, one `_INGESTED_AT`. ClinicalTrials.gov holds about 550K studies. 500 is one page from the v2 API (`pageSize` cap is 1,000).

```sql
select table_name, row_count from LIBRARY_RAW.information_schema.tables where table_schema='LANDING' and (table_name ilike '%CLINICAL%' or table_name ilike '%CTGOV%' or table_name ilike '%TRIAL%')
-- FED_CLINICALTRIALS 500. Nothing else. No AACT, no investigator or facility tables.
```

**What the 500 rows do carry.** 44 mart columns. The "detail" the docket wants is already inside the JSON text columns:
- `RESPONSIBLE_PARTY`: `{"type": "PRINCIPAL_INVESTIGATOR", "investigatorFullName": "Stephen LaConte", "investigatorAffiliation": "Virginia Polytechnic..."}`
- `LOCATIONS`: JSON array of sites, `facility, city, state, zip`, and where the sponsor filled it in, `contacts` / `investigators` with names.
- `LEAD_SPONSOR_NAME`, `LEAD_SPONSOR_CLASS` (`INDUSTRY` on 110 of 500), `INTERVENTIONS` (drug names as JSON), `NPI` (blank on every sample row; registry says self-reported and mostly empty).

```sql
select count(*) from HEALTH__FED_CLINICALTRIALS where LOCATIONS ilike '%investigator%' or RESPONSIBLE_PARTY ilike '%investigatorFullName%'   -- 226 of 500
```

**Other side of the join:** `HEALTH__FED_CMS_OPEN_PAYMENTS`, 15,385,047 rows, has `NPI`, `COVERED_RECIPIENT_FIRST_NAME`, `COVERED_RECIPIENT_LAST_NAME`, `SUBMITTING_APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_NAME`. So the bridge is investigator name + sponsor name, not NPI. Open Payments also publishes a research-payment file with principal-investigator columns; that file is the cleaner bridge and is not in this table's column list. Worth its own check.

**Code:** nothing in `scripts/` or `connect/` calls clinicaltrials.gov. `scripts/freshness_mapping.json` lists `fed_clinicaltrials` as daily on `LAST_UPDATE_POSTED_DATE`; `reports/stale_sources_2026-09-06.md` marks it 82x stale. Registry row `fed_clinicaltrials` names the v2 API and AACT.

**Fix:** reload, then parse.
1. Python-side crawl of `https://clinicaltrials.gov/api/v2/studies?pageSize=1000&pageToken=...`, about 550 pages, same 44-column shape as now. Or the AACT Postgres dump (bigger, already relational, schema drifts). About 550K rows.
2. Warehouse SQL: `lateral flatten(parse_json(LOCATIONS))` to one row per study-site-investigator; same for `INTERVENTIONS` to get drug names. A few million rows.
3. Name-match investigator to Open Payments covered recipient, sponsor to manufacturer. Multi-word rule (traps: single-word name matches are 8% real).
Medium. Part 1 is the time (550 HTTP calls); parts 2-3 are SQL.

---

## E75 — Nursing home chains and COVID relief money

**Docket says:** `LIBRARY_RAW.LANDING.FED_HHS_TAGGS` + `HEALTH__FED_NURSINGHOME411`, 14,758 rows, "the relief fund records aren't usable this way".

**Landed table:** `FED_HHS_TAGGS`, 45 rows, 22 columns, one `_SRC_SHA256`. The columns are right (`AWARD_NUMBER, OPDIV, RECIPIENT_NAME, RECIPIENT_EIN, AWARD_AMOUNT, ASSISTANCE_LISTING_NUMBER ...`). The rows are not data:

```sql
select PROJECT_DESCRIPTION, AWARD_NUMBER from LIBRARY_RAW.LANDING.FED_HHS_TAGGS
-- 'close about menu' | 'About TAGGS' | 'Data Dictionary' | 'Sitemap' | 'Search' | 'Award Search' | 'Recipient Search' | 'HHS COVID-19 Funding' | 'Grants by OPDIV' ... 45 rows, every other column ''
```
It is the taggs.hhs.gov navigation menu, scraped from the HTML and dropped into a grants header. `RECIPIENT_EIN`, the column that would identify the recipient, is blank on all 45. The registry row `fed_hhs_taggs` already says: "[2026-07-24] Retired: source still broken (< 50 rows after re-ingest attempt). Mart disabled." `dbt_project.yml` line 165 still lists `economics__fed_hhs_taggs`.

**Is the money anywhere else in the warehouse?**
```sql
select count(*), sum(try_to_number("federal_action_obligation")) from LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FULL where "cfda_number" like '93.498%'
-- 2,662 rows, sum -7,962,159,126 (net de-obligations)
select count(*) from ... where "cfda_number" like '93.498%' and "recipient_name" ilike '%NURSING%'   -- 0
```
93.498 is the Provider Relief Fund listing. USAspending has 2,662 rows of it, none naming a nursing home, and that table is capped at 1M rows per year (memory trap), so it is a floor, not the fund. No table named `%RELIEF%`, `%PRF%`, `%COVID%`, `%CARES%` in LANDING. `FED_SBA_PPP_LOANS_150K_PLUS` (968,524 rows) is a different program.

**The other side is ready:** `HEALTH__FED_NURSINGHOME411`, 14,713 rows, `CHAIN_NAME`, `CHAIN_ID` (10,162 homes carry one), `NUMBER_OF_FACILITIES_IN_CHAIN`, ratings, fines, `SPECIAL_FOCUS_STATUS`, `ABUSE_ICON`. The "worst chains" half of the question is answerable today.

**Code:** no loader for TAGGS in `scripts/` or `connect/`. The dbt staging model `staging/fed_hhs_taggs/stg_fed_hhs_taggs__grant_awards.sql` already trims and casts the right columns (EIN, award date, amount with `$` and `,` stripped); it is reusable the day real TAGGS rows land, but the fix below does not go through TAGGS. `connect/entity_index_specs.py` line 1575 already lists the table as "45 rows of page chrome".

**Fix:** new source, not a TAGGS retry. TAGGS is an HTML search portal; its award CSV export is per query. The Provider Relief Fund payments were published by HRSA as one flat public file (provider name, state, city, payment amount; a few hundred thousand rows; no EIN, no CCN). Land that flat file (Python download, COPY), then:
- match `provider name + city + state` to `NURSINGHOME411.PROVIDER_NAME, CITY_TOWN, STATE` (PRF names the payee, which for a home is usually the facility's operating entity; check a sample before trusting it, see the Utah owner-vs-facility trap),
- roll up to `CHAIN_ID`, set beside chain ratings and fines.
Medium. Name matching is the work; the load is small. If the PRF file's current URL has moved, the fallback is the TAGGS "HHS COVID-19 Funding" report export, which carries `RECIPIENT_EIN` and would need an EIN-to-CCN bridge that does not exist (traps: NPPES EIN is empty).

---

## Receipts, all four

| check | query | result |
|---|---|---|
| LANDING names | `table_name ilike '%CLINICAL%' or '%CTGOV%' or '%TRIAL%' or '%EOIR%' or '%990%' or '%TAGGS%'` | FED_CLINICALTRIALS 500, FED_EOIR_CASE_DATA 12,631,225, FED_HHS_TAGGS 45, FED_IRS_990 200, FED_IRS_990_EFILE_INDEX 5,544,626 |
| EOIR shape | `regexp_count(CASE_TYPE,'\t')` | 38 tabs on 12,631,125 rows |
| EOIR unique id | `count(distinct split_part(...,1))` | 12,631,225 |
| EOIR NULs | `split_part(...,10)` | `\x00` on 4,264,379 rows |
| 990 pay column | `count_if(OFFICERCOMPENSATIONAMT non-blank)` on FED_IRS_990 | 0 of 200 |
| hospital 990s | index join BMF NTEE `E2%`, RETURN_TYPE 990 | 3,987 EINs, 32,963 returns |
| trials with a named investigator | `LOCATIONS ilike '%investigator%' or RESPONSIBLE_PARTY ilike '%investigatorFullName%'` | 226 of 500 |
| industry-sponsored trials | `LEAD_SPONSOR_CLASS='INDUSTRY'` | 110 of 500 |
| Open Payments join columns | information_schema | NPI, first/last name, manufacturer name; 15,385,047 rows |
| TAGGS content | `select PROJECT_DESCRIPTION` | 45 menu labels, all data columns blank |
| PRF in USAspending | `cfda_number like '93.498%'` | 2,662 rows, net -7.96B, 0 with NURSING in name |
| homes with chain id | `CHAIN_ID<>''` on NURSINGHOME411 | 10,162 of 14,713 |

Code search (live tree, `_JUNK_DRAWER` and `reports` excluded): no `.py` loader or parser references EOIR, clinicaltrials.gov, or TAGGS. IRS 990 has the index loader only (`scripts/irs_bulk_discover_load.py`, `scripts/server_side_specs.py`, `scripts/sprint_a_specs.py`).

parked: the EOIR zip is one download; fixing the largest-member-only zip path fixes the other 17 zip specs at the same time.
