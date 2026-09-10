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
