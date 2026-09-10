# Phase 5 probes, 2026-09-10

Step 1 of the depth plan, phase 5: find the real file, read its head, name the key. Nothing landed yet.
All probes ran through the Python door. Chat plug-in was 401 at boot, not used.

## A. SAM entity registration

Premise in the brief: "lands as FED_SAM_ENTITY_REGISTRATION, UEI, EIN, parent UEI".

| check | result |
|---|---|
| `LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC` | exists, 895,429 rows, 146 cols, landed 2026-08-30 from the 20260802 extract |
| INGEST_RUNS | `fed_sam_entity_public` success, 895,429 rows |
| source | `api.sam.gov/data-services/v1/extracts?fileType=ENTITY&sensitivity=PUBLIC&frequency=MONTHLY` with SAM_API_KEY, redirects to S3 |
| this month's file | `SAM_PUBLIC_MONTHLY_V2_20260906.ZIP`, 146 MB, one .dat member, BOF header says 895,932 records |
| layout | 142 pipe fields, no header row, record ends `!end`, latin-1 |
| EIN | not in the public V2 layout, ever |
| parent UEI | not in the public V2 layout |
| distinct UEI | 887,310 of 895,429 rows |
| dupes | USPS UEI GD73T619EZJ3 has 82 rows, one per CAGE code; whole-row distinct = 895,429, so no double-append |

Key is UEI_SAM + CAGE_CODE, not UEI alone.
Parent UEI lives on USAspending contracts as RECIPIENT_PARENT_UEI, not in SAM public.
EIN is never published by SAM. The contracts-to-nonprofits bridge stays name+ZIP.

What a refresh would do: swap the August extract for September, +503 rows, same columns.

## B. CMS SNF ownership

Source: data.cms.gov data.json, title "Skilled Nursing Facility All Owners", 46 quarterly CSV vintages back to 2015.
Newest: `https://data.cms.gov/sites/default/files/2026-08/1d804c1b-cefd-4438-852d-a267890bb144/SNF_All_Owners_2026.07.31.csv`, 6.28 MB.

| check | result |
|---|---|
| rows | 295,083 data rows, 40 cols, zero bad widths |
| encoding | not UTF-8; byte 0xBF at 4,456,218; reads clean as cp1252 |
| CCN | absent. Key is ENROLLMENT ID, joins 1:1 to FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS which holds CCN |
| distinct ENROLLMENT ID | 14,410 of 14,425 enrollments |
| distinct owner ASSOCIATE ID | 89,543 |
| distinct enrollment+owner | 198,299; grain is enrollment x owner x role |
| PERCENTAGE OWNERSHIP filled | 96,823 rows |
| top roles | ADP OF THE SNF 93,015; OPERATIONAL/MANAGERIAL CONTROL 57,582; 5%+ INDIRECT 28,096 |

Key: ENROLLMENT ID + ASSOCIATE ID - OWNER + ROLE CODE - OWNER.
Sibling already landed the same way: FED_CMS_HOME_HEALTH_OWNERS, 101,188 rows, via scripts/cms_hha_owners_load.py.
Under 5M rows: bridge_fuel_load.

## C. EOIR immigration court

Source: `https://fileshare.eoir.justice.gov/EOIR Case Data.zip`, 4.56 GB, dated 2026-09-01. The old FOIA-TRAC-Report.zip 404s.
No file named tblDecision exists. Decision fields ride on B_TblProceeding: IJ_CODE, DEC_TYPE, DEC_CODE, COMP_DATE, ABSENTIA.

| member | rows per Count.txt | uncompressed | key |
|---|---|---|---|
| B_TblProceeding.csv | 16,817,336 | 3.5 GB, 38 cols | IDNPROCEEDING, IDNCASE, IJ_CODE |
| Lookup/tblLookupJudge.csv | 1,786 | 170 KB, 18 cols | JUDGE_CODE, JUDGE_NAME |
| Lookup/tblLookupJudgeBaseCity.csv | 12,566 | 1.6 MB | JUDGE_CODE x BASE_CITY_CODE |
| A_TblCase.csv | 12,821,531 | 1.9 GB, 39 cols | IDNCASE, already landed as FED_EOIR_CASE_DATA |

Files are tab-delimited with a header, .csv extension, per the Readme.
Ranged reads work: central directory at the tail, local header at the member offset, inflate the member alone. No need to pull 4.56 GB for two members.
B_TblProceeding over 5M rows: fast loader, with a tab delimiter. tblLookupJudge: bridge_fuel.

## D. DOL WHD enforcement

enforcedata.dol.gov and enfxfr.dol.gov both redirect every path to data.dol.gov. The flat-file catalog is gone.
Dataset lives at `apiprod.dol.gov/v4/get/whd/enforcement/csv`, name "Enforcement", table WHD_enforcement, quarterly, published 2026-06-04.
Every call answers 401 without an X-API-KEY. DOL_API_KEY in library-onboarding/.env is empty.
A key is free: sign in at data.dol.gov, Profile, API key.
Row count and columns unknown until a key answers.

---

# Phases 2 to 4, step 1 probes, 2026-09-10 afternoon

## HMDA LAR 2018-2024

Source: ffiec.cfpb.gov data-browser API, nationwide csv per year, Range honoured, 99 columns, header row.
`https://ffiec.cfpb.gov/v2/data-browser-api/view/nationwide/csv?years=YYYY`

| year | rows, from the aggregations endpoint | csv bytes |
|---|---|---|
| 2018 | 15,138,510 | 5.88 GB |
| 2019 | 17,573,963 | |
| 2020 | 25,699,043 | |
| 2021 | 26,269,980 | |
| 2022 | 16,125,975 | |
| 2023 | 11,564,178 | |
| 2024 | 12,259,199 | 4.64 GB |
| total | 124,630,848 | ~34 GB |

No row key in the public LAR. LEI repeats. Join on LEI, STATE_CODE+COUNTY_CODE, CENSUS_TRACT.
State-by-year is the same rows with STATE_CODE filled; nationwide is 7 pulls instead of 364.
Specs: scripts/sprint_phase2_specs.py, FED_CFPB_HMDA_LAR_2018..2024, fast loader via phase5_load url_csv.
Existing: FED_CFPB_HMDA_HISTORIC 44,992,667 rows 2007-2017, old layout. FED_CFPB_HMDA 28,301 and _LAR 17,474 are samples.

## FEMA disaster declarations

`https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv`, gzip on the wire, 70,402 rows, 29 cols.
Key `id` is unique, 70,402 distinct. `disasterNumber` repeats, 5,264 distinct: one row per disaster x designated area.
API count endpoint agrees: 70,402. fipsStateCode + fipsCountyCode give county FIPS. bridge_fuel.

## NPPES monthly deactivations

`https://download.cms.gov/nppes/NPPES_Deactivated_NPI_Report_081026_V2.zip`, 2.6 MB, one xlsx member.
Sheet DeactivatedNPIs: 351,914 rows including a title row and a header row. Two columns: NPI, NPPES Deactivation Date.
Monthly file name rotates, MMDDYY. Needs an xlsx reader; bridge_fuel does csv and zip_csv only.

## EIA-860 prior years

`https://www.eia.gov/electricity/data/eia860/archive/xls/eia860YYYY.zip`, 2019 18.8 MB, 2022 20.6 MB, 2023 21.2 MB. 2024 at the non-archive path, 22.1 MB.
Each zip: Utility, Plant, Generator, Wind, Solar, Storage, Multifuel, Owner, EnviroAssoc, EnviroEquip xlsx, plus form, instructions, layout.
Existing FED_EIA860_* tables are one vintage. Multi-sheet xlsx per member; needs the xlsx path.

## eGRID 2019-2023

xlsx per year on epa.gov, 11.6 MB 2019, 14.1 MB 2021, 21.2 MB 2023 rev1. Existing ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 is one year.

## Contracts R2 reload with county FIPS

scripts/usaspending_contracts_full_load.py pulls 36 curated columns through 238 monthly bulk-download jobs, write_pandas chunks. 93M rows landed as FED_USASPENDING_CONTRACTS_FULL_R2.
Columns the ledger wants, real bulk names: prime_award_transaction_place_of_performance_county_fips_code, awarding_agency_code, awarding_sub_agency_code, domestic_or_foreign_entity_code, plus the tax-exempt entity flags.
A reload is 238 server-side jobs again, many hours, and the transport should move to the fast path. Its own session.

## Contracts, done as new year tables from the archive, not an R2 reload

Chris 2026-09-10: "do it". USAspending publishes a monthly award-data archive: one zip per fiscal year, every column, csv members of 1M rows.
`https://files.usaspending.gov/award_data_archive/FY{y}_All_Contracts_Full_20260806.zip`, FY2007 to FY2026, 0.9 to 2.1 GB each, ~30 GB total.

| check, FY2024 | result |
|---|---|
| members | 7 csv, 14.78 GB raw |
| rows | 6,692,568 by the csv module, headers equal across members, zero bad widths |
| columns | 297 |
| key | contract_transaction_unique_key, 6,692,568 distinct, 0 null |
| county FIPS | prime_award_transaction_place_of_performance_county_fips_code filled on 6,208,254 rows |
| also present | awarding_agency_code, funding_agency_code, domestic_or_foreign_entity_code, tax-exempt entity flags |

Host behaviour: about 25 rapid requests at 12:50 got the address banned on files.usaspending.gov and api.usaspending.gov for roughly an hour, TLS closed before any response. www.usaspending.gov kept answering. Loads run one year at a time with a 60 s gap.
Tables: FED_USASPENDING_CONTRACTS_FY2007..FY2026. FED_USASPENDING_CONTRACTS_FULL_R2 untouched.
