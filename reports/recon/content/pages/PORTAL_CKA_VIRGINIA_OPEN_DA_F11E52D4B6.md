# PORTAL_CKA_VIRGINIA_OPEN_DA_F11E52D4B6

rows 10.0K  columns 10  scan 2.7s

roles: audit 2, category 4, date 2, other 2, who 1

## when

REPORT_DATE
  2024     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## who

SRC_SHA256 by rows
     10.0K  a282df8a3c17dcf239a1dd4d4375344debe35861a641f6a71b4c779a1feef6bb

## who x when

SRC_SHA256 by REPORT_DATE
  a282df8a3c17dcf239a1dd4d4375344debe35861  2024:10.0K

## what

GEOGRAPHY_TYPE: Health District 99%, State 1%

GEOGRAPHY_NAME: Roanoke 9%, Loudoun 9%, Alleghany 8%, Mount Rogers 8%, Central Virginia 8%, Lord Fairfax 8%, Richmond 8%, Fairfax 8%, Chickahominy 8%, Hampton 8%, Blue Ridge 8%, Central Shenandoah 8%

FACILITYTYPEGROUP: All Outbreaks 12%, Healthcare Setting 11%, Other 11%, Correctional Facility 11%, Congregate Setting 11%, College / University 11%, K-12 11%, Long Term Care Facilities 11%, Child Care 11%

NUMBER_OF_OUTBREAK_ASSOCIATED_DEATHS: Not Provided at this time 99%, 76 0%, 155 0%, 164 0%, 165 0%, 45 0%, 128 0%, 75 0%, 166 0%, 122 0%, 131 0%, 50 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 85 | 0 | 2024-09-17T00:00:00 317; 2024-09-14T00:00:00 317; 2024-09-16T00:00:00 303; 2024-09-08T00:00:00 299 |
| GEOGRAPHY_TYPE | category | 2 | 0 | Health District 9.9K; State 56 |
| GEOGRAPHY_NAME | category | 35 | 0 | Roanoke 320; Loudoun 317; Alleghany 309; Mount Rogers 307 |
| FACILITYTYPEGROUP | category | 9 | 0 | All Outbreaks 1.2K; Healthcare Setting 1.1K; Other 1.1K; Correctional Facility 1.1K |
| NUMBER_OF_OUTBREAKS | other | 400 | 0 | 0 1.3K; 4 332; 7 303; 12 267 |
| NUMBER_OF_OUTBREAK_ASSOCIATED_CASES | other | 606 | 0 | Not Provided at this time 8.7K; 1937 32; 5341 19; 2047 16 |
| NUMBER_OF_OUTBREAK_ASSOCIATED_DEATHS | category | 12 | 0 | Not Provided at this time 9.9K; 76 22; 155 8; 164 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:49:05.05299 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f33f0761-ef43-4008-8a27-8 10.0K |
| SRC_SHA256 | who | 1 | 0 | a282df8a3c17dcf239a1dd4d4 10.0K |
