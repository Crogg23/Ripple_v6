# Dead ends, build B — parsers. 2026-09-07

Follows `reports/dead_ends_scope_B_parsers_2026-09-07.md`, lines 144 and 143.
Chris greenlit `rebuild` this session. Nothing dropped. Old tables untouched.

---

## 144 — EOIR immigration court cases: the one-column table is now 39 columns

**What was wrong.** `LIBRARY_RAW.LANDING.FED_EOIR_CASE_DATA` holds 12,631,225 rows in ONE column named `CASE_TYPE`, each value a tab-separated line of 39 fields with NUL bytes inside. The loader ate the header.

**What was built.**

| thing | where | what |
|---|---|---|
| staging view | `LIBRARY_STAGING.STAGING.STG_FED_EOIR__CASES` | `replace(CASE_TYPE,'\x00','')` then `split_part(line,'\t',1..39)`, blanks to null, plus `field_count` |
| mart table | `LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASES` | 38 columns: 33 of the 39 fields typed, plus field_count, two meta columns and source_id. Six legacy fields stay in staging only: E_28_DATE, UP_BOND_DATE, UP_BOND_RSN, RELEASE_MONTH, RELEASE_YEAR, ZBOND_MRG_FLAG |
| model files | `library-onboarding/ripple_dbt/models/staging/fed_eoir_case_data/stg_fed_eoir__cases.sql`, `.../marts/immigration/immigration__fed_eoir_cases.sql`, `schema_fed_eoir_cases.yml` | |

The old one-column `immigration__fed_eoir_case_data` model is left as it was.

**Field names.** From the EOIR Case Data Code Key PDF, `https://www.justice.gov/eoir/page/file/eoir-case-data-code-key/download` (May 2019, 113 pages, pulled with `pypdf`). The Code Key lists `A_tblCase` fields but its numbering is not file position: it omits `UPDATED_ZIPCODE`/`UPDATED_CITY` at 5-6, `C_BIRTHDATE` at 26, `ADDRESS_CHANGEDON` at 29, `ZBOND_MRG_FLAG` at 30, and lists `FNLDISP`, which is not in the file. Those five names are the FOIA file's published header. 18 of 39 positions were checked against a 200K-row sample by value shape (13 below plus city, state, zip, LANG, SITE_TYPE); the other 21 rest on the Code Key order alone, because the file's own header no longer exists anywhere in the warehouse:

```
f1  IDNCASE           12,631,225 distinct = row count
f7  NAT               MX 3.08M, GT 1.30M, HO 1.20M, ES 946K, VE 814K
f9  CUSTODY           N 8,197,201  D 2,954,594  R 1,348,821  null 130,511
f13 CASE_TYPE         RMV 10,883,997  DEP 1,093,156  CFR 209,364  EXC 204,041  DDC 129,329
f14 UPDATE_SITE       MIA 850,958  NYC 812,576  WLA 586,435  CHI 500,642  ORL 445,473
f15 LATEST_HEARING    1953-08-05 to 2040-05-09, null on 2,351,663
f20 CORRECTIONAL_FAC  S / D / F / M, 2.2% filled
f25 C_ASY_TYPE        E / I / J
f26 C_BIRTHDATE       MM/YYYY, masked
f27 C_RELEASE_DATE    2099-12-31 sentinel, 0.8% filled
f31 GENDER            M 4,141,514  F 2,765,195  null 5,724,135
f34 LPR               0 / 1
f36 DETENTION_LOCATION  "ASP Red Rock Correctional Center", "TDCJ", 21 distinct in sample
f39 CASEPRIORITY_CODE   N/A 97%, UC, AWC/ATD, CR
```

**Proof the split worked.**

```
select count(*), count(distinct case_id), count_if(case_id is null)
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASES
-- 12,631,225 | 12,631,225 | 0

select field_count, count(*) ... group by 1
-- 39: 12,631,125   40: 96   41: 2   46: 1   47: 1

select custody, custody_label, count(*) ... group by 1,2 order by 3 desc
-- N never detained 8,197,201 | D detained 2,954,594 | R released 1,348,821 | null 130,511
-- then 98 rows of SP/ENG/UR/... = the 100 shifted rows, a language code sitting in the custody slot

select court_code, count(*) ... group by 1 order by 2 desc limit 10
-- MIA 850,958 | NYC 812,576 | WLA 586,435 | CHI 500,642 | ORL 445,473
-- SFR 443,767 | NEW 436,056 | DAL 435,772 | SNA 330,415 | ATL 313,562
```

Commands:
```
cd library-onboarding/ripple_dbt
dbt run  --select stg_fed_eoir__cases immigration__fed_eoir_cases   # 2 success, 50.6s
dbt test --select stg_fed_eoir__cases immigration__fed_eoir_cases   # 8 tests: 4 pass, 4 warn
```

Tests: `unique` and `not_null` on the case id pass on both layers. Four warn-severity tests warn as designed: custody accepted_values (the 100 shifted rows plus 130K blanks), `court_code` not_null, `case_type` not_null (blanks on a small share). None fail.

**Traps found.**
- About 100 rows carry a stray tab in a free-text field (city name) and every field right of it shifts by one. `field_count` on the mart marks them; filter `field_count = 39` for a clean cut.
- `GENDER` is blank on 45% of cases, and two rows carry a timestamp in the gender slot (shifted rows).
- `LATEST_HEARING` runs to 2040: scheduled future hearings, not typos.
- `_INGESTED_AT` on the landing table is TIMESTAMP, carried through as `_loaded_at`.

**Still missing.** The docket asks "by judge". `A_tblCase` has no judge and no decision. `IJ_CODE` and the outcome live in `B_TblProceeding` in the same FOIA zip, which the zip loader never kept (largest-member trap). Not attempted this session; it is a reload into LANDING and needs its own greenlight. Zip URL for whoever picks it up: `https://fileshare.eoir.justice.gov/EOIR Case Data.zip`.

---

## 143 — ClinicalTrials.gov: every study, into a new table

**What was wrong.** `FED_CLINICALTRIALS` holds 500 rows, one API page. ClinicalTrials.gov holds 601,694 studies.

**Column count.** The ask said 44 columns. The landing table has 38: 35 data plus 3 meta. The 44 is the mart's column count, not the landing table's. The new table matches the landing table, byte for byte on name and order.

**What was built.** `scripts/clinicaltrials_load.py`, after the `senate_lda_load.py` pattern: stream pages, flush a buffer every 10 pages, checkpoint the `pageToken` in `logs/clinicaltrials_checkpoint.json`, reconnect if the Snowflake token expires. Dry run shows the first page and the total; `--run` lands it, one progress line every 50 pages.

Target: `LIBRARY_RAW.LANDING.FED_CLINICALTRIALS_FULL`, a NEW table. The old 500-row table and its mart are untouched.

Shape: the same 35 data columns as the old table, same order, all VARCHAR, JSON blocks landed as JSON text the same way (`PHASE` as `["NA"]`, `LOCATIONS` as an array of site objects, booleans as `True`/`False`). Three meta columns: `_INGESTED_AT` as ISO text, not the epoch-micros NUMBER the old table carries; `_SOURCE_RUN_ID`; `_SRC_SHA256`, the sha256 of the API page body the row came from.

```
python scripts/clinicaltrials_load.py          # dry run
-- totalCount=601,694  pageSize=1000  ~602 pages; first page 1000 studies; 23 of 35 columns filled on study 1

python scripts/clinicaltrials_load.py --run    # log in logs/clinicaltrials_run.log
-- done: 602 pages, 601,694 rows landed this run, FED_CLINICALTRIALS_FULL now holds 601,694 rows, 44.1 min
```

Counts through the Python door:
```
select count(*), count(distinct NCT_ID), count_if(NCT_ID is null)
  from LIBRARY_RAW.LANDING.FED_CLINICALTRIALS_FULL
-- 601,694 | 601,694 | 0
-- 38 columns (35 data + 3 meta). All 500 NCT ids of the old table are in the new one.
-- LEAD_SPONSOR_CLASS: OTHER 430,377 | INDUSTRY 132,164 | OTHER_GOV 15,992 | NIH 11,573 | null 986
-- rows naming an investigator (LOCATIONS or RESPONSIBLE_PARTY): 279,874
-- LOCATIONS filled 541,210; INTERVENTIONS filled 540,752; START_DATE 596,330
-- FIRST_POSTED_DATE min 1999-09-20; LAST_UPDATE_POSTED_DATE max 2026-09-04
-- 602 distinct _SRC_SHA256 = one per page; one _SOURCE_RUN_ID; _INGESTED_AT 22:16 to 23:00 UTC
```

**Resume, honestly.** The checkpoint is written after each flush. A crash between a COPY committing and the checkpoint write re-lands up to 10,000 rows on resume, and the auth-expiry retry re-sends a whole batch. No uniqueness is enforced on NCT_ID. This run needed no resume and no retry, and rows = distinct = the API's totalCount, so it is clean. After any resumed run, re-count distinct NCT_ID before trusting the table.

**Completeness.** 601,694 is the API's own totalCount at crawl start. Studies added during the 44 minutes behind the cursor are not in the table. It is every study the cursor walked past.

**Pace.** 44.1 minutes for 602 pages, about 4.4 seconds a page, most of it the API. No 429, no retry, no reconnect in the log.

**Next for the question.** Not done here. `lateral flatten(parse_json(LOCATIONS))` to one row per study-site, pull `contacts`/`investigators` names, then name-match to Open Payments covered recipients with the multi-word rule. The staging model `stg_fed_clinicaltrials__clinical_trials` still reads the 500-row table; re-pointing it is a one-line source change once Chris says which table the mart should read.

---

## Docket

Rows 143 and 144 in `docket/docket.csv` moved from "missing a piece" to "part done", with `needs` naming the next hole (143: flatten and name-match; 144: `B_TblProceeding`). `docket_open.csv` and `DOCKET.md` regenerated with `scripts/build_docket.py`.

## Blocked

Nothing blocked. Two doors used: dbt (key-pair, this box) and the Python scripts door. The chat plug-in was down all session (401) and was not used.
