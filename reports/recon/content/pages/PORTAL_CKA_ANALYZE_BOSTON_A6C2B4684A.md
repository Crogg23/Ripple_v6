# PORTAL_CKA_ANALYZE_BOSTON_A6C2B4684A

rows 18  columns 24  scan 3.6s

roles: amount 3, audit 2, category 18, date 1, who 1

## when

INGESTED_AT
  2026        18  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TEST | 17 | 0 | 0 | 0 | 0 | 0 |
| SHAPE_LENGTH | 18 | 0 | 0.02 | 1.11 | 1.27 | 1.90 |
| SHAPE_AREA | 18 | 0 | 0 | 0.01 | 0.01 | 0.01 |

## who

SRC_SHA256 by rows
        18  f54fca4de56bdb315e3228471b785110fd73e075a7621a96bad4f0a7493c1b60

SRC_SHA256 by dollars
        1.90       18 rows  f54fca4de56bdb315e3228471b785110fd73e075a7621a96bad4f0a7493c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  f54fca4de56bdb315e3228471b785110fd73e075  2026:1.90

## what

OBJECTID_1: 289 9%, 287 9%, 286 9%, 284 9%, 283 9%, 282 9%, 280 9%, 279 9%, 276 9%, 275 9%, 274 9%

TOWNS_ID: 277 9%, 275 9%, 274 9%, 272 9%, 271 9%, 270 9%, 268 9%, 267 9%, 264 9%, 263 9%, 262 9%

TOWN_ID: 35 100%

TOWN: BOSTON 100%

FIPS_STCO: 25025 100%

CCD_MCD: 440 100%

FIPS_PLACE: 07000 100%

POP1980: 570719 100%

POP1990: 574283 100%

POP2000: 588957 100%

POPCH80_90: 3564 100%

POPCH90_00: 14674 100%

FOURCOLOR: 1 100%

TYPE: C 100%

ISLAND: 1 100%

FIPS_MCD: 25025440 100%

FIPS_COUNT: 25 100%

SHAPE_WKT: MULTIPOLYGON (((-70.8903842879 20%, MULTIPOLYGON (((-70.8832617729 20%, MULTIPOLYGON (((-70.8942570149 20%, MULTIPOLYGON (((-70.8923094739 20%, MULTIPOLYGON (((-70.8693006859 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 18 | 1 | 289 1; 287 1; 286 1; 284 1 |
| TOWNS_ID | category | 18 | 1 | 277 1; 275 1; 274 1; 272 1 |
| TOWN_ID | category | 2 | 1 | 35 17 |
| TOWN | category | 2 | 1 | BOSTON 17 |
| FIPS_STCO | category | 2 | 1 | 25025 17 |
| CCD_MCD | category | 2 | 1 | 440 17 |
| FIPS_PLACE | category | 2 | 1 | 07000 17 |
| POP1980 | category | 2 | 1 | 570719 17 |
| POP1990 | category | 2 | 1 | 574283 17 |
| POP2000 | category | 2 | 1 | 588957 17 |
| POPCH80_90 | category | 2 | 1 | 3564 17 |
| POPCH90_00 | category | 2 | 1 | 14674 17 |
| FOURCOLOR | category | 2 | 1 | 1 17 |
| TYPE | category | 2 | 1 | C 17 |
| ISLAND | category | 2 | 1 | 1 17 |
| FIPS_MCD | category | 2 | 1 | 25025440 17 |
| FIPS_COUNT | category | 2 | 1 | 25 17 |
| TEST | amount | 2 | 1 | 0.000000000000000 17 |
| SHAPE_LENGTH | amount | 18 | 0 | 1.273311030611833 1; 0.021504611851078 1; 0.051687864619563 1; 0.016159663668967 1 |
| SHAPE_AREA | amount | 18 | 0 | 0.012191276580099 1; 0.000009568548446 1; 0.000075076632839 1; 0.000018241239977 1 |
| SHAPE_WKT | category | 6 | 13 | MULTIPOLYGON (((-70.89038 1; MULTIPOLYGON (((-70.88326 1; MULTIPOLYGON (((-70.89425 1; MULTIPOLYGON (((-70.89230 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:52.03810 18 |
| SOURCE_RUN_ID | audit | 1 | 0 | bd058a95-5207-4d83-85b2-8 18 |
| SRC_SHA256 | who | 1 | 0 | f54fca4de56bdb315e3228471 18 |
