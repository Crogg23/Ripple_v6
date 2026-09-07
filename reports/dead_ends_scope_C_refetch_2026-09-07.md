# Dead ends, scope C: refetch — receipts (2026-09-07)

Read-only pass. Nothing loaded, nothing written to the warehouse. Python door only.

Two docket lines that died on a thin source (118, E74) plus the 14 round-number
tables in `reports/warehouse_gaps_2026-09-06.md` Gap 2.

## Docket 118 — FED_FDIC_ENFORCEMENT (14 rows)

**What was checked**
- `LIBRARY_RAW.LANDING.FED_FDIC_ENFORCEMENT`: 14 rows, columns `RAW_TEXT, ORDER_URL, _INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256`. One run, ingested 2026-06-17.
- The 14 rows: `ORDER_URL` values are `fdic.gov/about/`, `/resources/`, `/analysis/`, `/news/`, `/search/help.html`, `/doing-business-fdic`, `/household-survey`. `RAW_TEXT` is the site menu text ("About|The Federal Deposit Insurance Corporation (FDIC) is an independent agency...").
- Registry `URL` = `https://orders.fdic.gov/s/searchform`. Access method blank.
- Loader: no hand-written script anywhere in `scripts/` or `connect/`. It came through `library-onboarding/ingest.py`, which asks the LLM for a `fetch_data(context)` function per source (line 289) and runs it; the generated code is not saved to disk, only the run row. dbt already knew: `ripple_dbt/dbt_project.yml` disables `regulation__fed_fdic_enforcement` with "stub: 14 rows, failed scrape".

**Why it stopped at 14**
orders.fdic.gov is a Salesforce Lightning app; a plain GET returns a JS shell (WebFetch of `orders.fdic.gov/s/` today: "CSS Error", no content). The generated scraper fell back to, or was redirected to, fdic.gov, and landed the navigation menu as data: 7 nav links x 2 spellings = 14 rows. It is the "landing page scraped as data" fingerprint that `ingest._reject_html` now blocks (that guard post-dates this load).

**Real size**
- No FDIC API for orders. `api.fdic.gov/banks/docs` (BankFind) lists institutions, locations, failures, SOD, financials, demographics — no enforcement endpoint.
- Orders are published monthly since March 1990 on orders.fdic.gov (`/s/press-release-orders?prYear=&prMonth=`). January 2025: 12 orders + 1 decision. At roughly 10-25 orders a month over 35 years the corpus is in the low tens of thousands. **No hard total found today; treat "tens of thousands" as an estimate, not a count.**
- The site is JS-rendered; a full pull needs a browser (Playwright, which `ingest.py` line 829 already lazily supports) walking the monthly press-release-orders pages, or the underlying Salesforce Aura endpoint.

**Fix available:** yes, but it is a new scraper (browser-driven, monthly pages), not a rerun. Not a flat file, not an API.

## Docket E74 — home health agency ownership

**What was checked**
- LANDING tables LIKE `%HOME_HEALTH%`, `%HHA%`, `%OWNERSHIP%`, `%OWNER%`:
  - `FED_CMS_HOME_HEALTH` 12,392 rows (Care Compare, one row per CCN). Only ownership column: `TYPE_OF_OWNERSHIP` — PROPRIETARY 9,037 / '-' 2,037 / NON-PROFIT 1,068 / GOVERNMENT OPERATED 250. A category, not a name.
  - `FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS` 11,508 rows (PECOS enrollment: ENROLLMENT_ID, NPI, CCN, ASSOCIATE_ID, ORGANIZATION_NAME, DBA, INCORPORATION_DATE, PROPRIETARY_NONPROFIT, address). No owner columns.
  - Other `%OWNER%` hits are unrelated: `FED_EIA860_4_OWNER` (power plants), `FED_SEC_INSIDER_REPORTINGOWNER`.
- No HHA owners table anywhere in LANDING or MARTS.

**The source exists**
- CMS "Home Health Agency All Owners", data.cms.gov, quarterly (R/P3M), last modified 2026-08-19.
- API: `https://data.cms.gov/data-api/v1/dataset/fc009b2d-7846-44b1-b4a1-692f0c143879/data` — stats endpoint reports **total_rows 101,188**.
- CSV: `https://data.cms.gov/sites/default/files/2026-07/e3c50419-ff93-4b7a-964c-f8b1d622d817/HHA_All_Owners_2026.07.17.csv`. Historical versions back to 2023-04-01 on catalog.data.gov.
- Columns (38): ENROLLMENT ID, ASSOCIATE ID, ORGANIZATION NAME, ASSOCIATE ID - OWNER, TYPE - OWNER, ROLE CODE/TEXT - OWNER, ASSOCIATION DATE - OWNER, owner name fields, owner address, PERCENTAGE OWNERSHIP, and the flag set (CORPORATION, LLC, HOLDING COMPANY, INVESTMENT FIRM, PRIVATE EQUITY COMPANY, REIT, CHAIN HOME OFFICE, CREATED FOR ACQUISITION ...).
- It joins to `FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS` on ENROLLMENT_ID / ASSOCIATE_ID (same PECOS keys), then to CCN.
- ASSOCIATION DATE - OWNER answers "when did the new owner arrive"; the docket's "who is the new owner" question is answerable.

**Fix available:** yes. Flat CSV, no auth, one file, ~100K rows. Same shape as the hospice owners file CMS released the same day (April 2023).

## Gap 2 — the 14 round-number tables

Landing tables written by `library-onboarding/ingest.py` (LLM-generated `fetch_data`) carry `_INGESTED_AT`; tables from `scripts/recon_bulk_load_*` carry unprefixed `INGESTED_AT`. All 14 hold exactly one `_SOURCE_RUN_ID`.

| rows | table | loader | what stopped it | full set reachable |
|---|---|---|---|---|
| 50,000 | FED_USASPENDING_BULK | onboarding `fetch_data` (2026-07-02, generated code not saved) | generated code read a slice of one archive; `_INGESTED_AT` one run | **already done**: `FED_USASPENDING_CONTRACTS_FULL_R2` 93M rows via `scripts/usaspending_contracts_full_load.py` |
| 10,000 | FED_SAM_EXCLUSIONS | `scripts/sam_exclusions_load.py` (deprecated) | `PAGE_SIZE=1000`, `--flush-pages 10`: first flush = 10,000, then SAM throttle killed page 14 (2026-08-22). Also the API itself: "can return only the first 10,000 records" | **already done**: `FED_SAM_EXCLUSIONS_FULL_R2` 168,328 rows via `scripts/sam_exclusions_extract_load.py` (daily public extract ZIP, no key) |
| 5,000 | FED_USGS_3DEP | onboarding `fetch_data` | ArcGIS ImageServer query; 5,000 = a generated loop cap, no `resultOffset` walk | yes, page with resultOffset; low value (DEM tile index, not data) |
| 5,000 | FED_EPA_ENVIROFACTS | onboarding `fetch_data` | efservice `tri.tri_facility` rows 0-4999, one page | **already done**: `FED_EPA_TRI_FACILITY` full pull 64,990 rows (`recon_bulk_load_2026-08-07.py` line 182) |
| 5,000 | FED_USASPENDING_SUBAWARDS | onboarding `fetch_data` | one `RECORD` JSON column, API search slice of 5,000 | **already done**: `FED_USASPENDING_SUBAWARDS_FULL` 4,742,460 rows via `scripts/usaspending_subawards_full_load.py` |
| 5,000 | INTL_DE_GOVDATA | onboarding `fetch_data` | CKAN `package_search`, generated loop stopped at 5 pages x 1,000 | yes, keep paging `start=`; catalogue metadata only |
| 5,000 | INTL_GR_DATAGOV | onboarding `fetch_data` | same shape, 5,000 loop cap | yes; catalogue metadata only |
| 5,000 | INTL_CH_OPENDATASWISS | onboarding `fetch_data` | CKAN, same 5,000 loop cap | yes; catalogue metadata only |
| 2,000 | FED_DOL_OFCCP_CSAL | `recon_bulk_load_tier1_remaining_2026-08-07.py` `load_xlsx`, `max_rows` default 5,000,000 | **not a cap.** OFCCP's FY2025 CSAL Release 1 is 2,000 establishments by design (DOL announcement 2024-11-20). REVIEW_TYPE: ESTABLISHMENT 1,880 / CMCE 60 / FAAP 48 / UNIVERSITY 12 | complete as landed |
| 2,000 | FED_ATF_FFL_LOCATIONS | `recon_bulk_load_2026-08-07.py` json_api entry, single GET | ArcGIS FeatureServer `maxRecordCount = 2000`; the entry's own description says "needs a new loader that pages". 2,000 rows, 1,906 distinct LIC_SEQN | **already done**: `FED_ATF_FFL` 77,514 rows via `scripts/atf_ffl_load.py` (pages with resultOffset, PAGE_SIZE 2000) |
| 2,000 | INTL_HUDOC | onboarding `fetch_data` | HUDOC search API, generated loop cap of 2,000 | yes, `start=`/`length=` paging; ECHR case index is ~100K+ |
| 1,000 | FED_BJS_DATA | onboarding `fetch_data`, URL `api.ojp.gov/bjsdataset/v1/gcuy-rt5g.csv` | Socrata-style default `$limit=1000`; fetching the URL bare today returns exactly 1,000 rows, last one truncated | yes, `$limit`/`$offset`; NCVS person file |
| 1,000 | INTL_CL_DATOSGOB | onboarding `fetch_data` | CKAN `package_search` `rows` max 1,000, one call | yes; catalogue metadata only |
| 1,000 | INTL_ES_DATOSGOB | onboarding `fetch_data` | datos.gob.es `apidata` default page of 1,000 (`_pageSize`), one call | yes; catalogue metadata only |

Five of the 14 are already superseded by a `_FULL`/`_R2`/full-pull sibling. One (OFCCP) is complete. Eight are real caps with paging available, and six of those eight are portal catalogues (dataset lists, not data).

### FED_SAM_EXCLUSIONS, the one that matters

- `FED_SAM_EXCLUSIONS` 10,000 rows, all `RECORD_STATUS = Active`, one run 2026-08-22. Stopped by the first `--flush-pages 10` x `PAGE_SIZE 1000` durable flush before the throttle killed the run at page 14 (documented in the loader's own header and in `sam_exclusions_extract_load.py`).
- The Entity API is also hard-capped: "It can return only the first 10,000 records" (open.gsa.gov/api/exclusions-api). Paging past 10,000 was never possible on that door.
- `FED_SAM_EXCLUSIONS_FULL_R2` 168,328 rows, all Active, from the daily public extract `SAM_Exclusions_Public_Extract_V2_{yyjjj}.ZIP` (`sam.gov/api/prod/fileextractservices/v1/api/download/Exclusions/Public%20V2/...`). The extract is active-only by definition ("All records in the extract are Active", GSA layout doc), so purged past bans are invisible — same floor already recorded in traps 2026-09-05.
- Outside check: OpenSanctions pulls the same file list daily and reports 267,578 entities / 105,640 searchable targets as of 2026-09-07 07:55 (entities include addresses and identifiers split out, so it does not compare 1:1 to rows). The warehouse's 168,328 rows is the right order of magnitude for the daily V2 file; no published row count from GSA itself.
- `PROCUREMENT__FED_SAM_EXCLUSIONS` mart and the spine (`entity_index_specs.py`) already read `_FULL_R2`. The bare 10,000-row table is dead weight, not a gap.

## Price (`scripts/price_it.py`, last 90 days)

| pattern | runs | p50 | max | note |
|---|---|---|---|---|
| `%FED_SAM_EXCLUSIONS%` | 500 (cap) | 0.0 min / $0.00 | 16.2 min / 0.270 cr / $0.54 | max is an ENTITY_GOLDEN spine CTAS that names the table, not a load |
| `%FED_FDIC_ENFORCEMENT%` | 500 (cap) | 0.0 min / $0.00 | 0.1 min / 0.002 cr / $0.00 | catalog reads only; no load in the window |

Both patterns hit the cap; the cost is the spine rebuild mentioning the table, not any loader. The extract load itself (a 12 MB zip through write_pandas) leaves no priced statement above noise. A tighter statement-level check tripped the warehouse gate hook (the SQL text carried swap/create words) and was not run.

## Summary line per source

| source | stopping mechanic | real size | fix available |
|---|---|---|---|
| FED_FDIC_ENFORCEMENT (118) | JS site; scraper landed fdic.gov nav menu | monthly since 1990, ~12/month in 2025; no total found | yes, new browser scraper; no file/API |
| HHA ownership (E74) | never fetched; only a TYPE_OF_OWNERSHIP category landed | 101,188 rows, 38 cols, quarterly CSV/API | yes, flat CSV |
| FED_SAM_EXCLUSIONS | flush at 10 pages x 1,000, then throttle; API caps at 10,000 anyway | 168,328 active in daily V2 extract | already landed as _FULL_R2 |
| USASPENDING_BULK / SUBAWARDS / ENVIROFACTS / ATF_FFL_LOCATIONS | generated one-shot fetch or single ArcGIS page | 93M / 4.7M / 65K / 77.5K | already landed as siblings |
| OFCCP_CSAL | none; the list is 2,000 | 2,000 | complete |
| 3DEP, HUDOC, BJS, DE/GR/CH/CL/ES portals | default page or loop cap in generated code | paging available | yes; six are catalogues, low value |

parked: the onboarding pipeline throws away the generated `fetch_data` code, so for eight of these the stopping line can only be inferred from the API's default page size, never read.
