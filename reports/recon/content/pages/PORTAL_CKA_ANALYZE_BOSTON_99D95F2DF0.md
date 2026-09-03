# PORTAL_CKA_ANALYZE_BOSTON_99D95F2DF0

rows 207  columns 18  scan 3.8s

roles: amount 6, audit 2, date 1, empty 1, other 7, who 2

## when

INGESTED_AT
  2026       207  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NAME20 | 207 | 1.01 | 803 | 9.8K | 9.8K | 275.4K |
| ALAND20 | 207 | 43.4K | 376.9K | 2.88M | 6.99M | 126.83M |
| AWATER20 | 207 | 0 | 0 | 1.32M | 5.39M | 18.65M |
| INTPTLON20 | 207 | -71.18 | -71.08 | -71.00 | -70.94 | -14.7K |
| SHAPE_LENGTH | 207 | 0.01 | 0.03 | 0.17 | 0.37 | 8.93 |
| SHAPE_AREA | 207 | 0 | 0 | 0 | 0 | 0 |

## who

NAMELSAD20 by rows
       207  Census Tract

NAMELSAD20 by dollars
      275.4K      207 rows  Census Tract

SRC_SHA256 by rows
       207  5ac315fe47d4f1da70dae6fe18ed20020bb16f3443563c7857beae8b5df76191

SRC_SHA256 by dollars
      275.4K      207 rows  5ac315fe47d4f1da70dae6fe18ed20020bb16f3443563c7857beae8b5df7

## who x when

NAMELSAD20 by INGESTED_AT  LOAD STAMP, not an event date, dollars = NAME20
  Census Tract                              2026:275.4K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = NAME20
  5ac315fe47d4f1da70dae6fe18ed20020bb16f34  2026:275.4K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATEFP20 | other | 1 | 0 | 25 207 |
| COUNTYFP20 | other | 1 | 0 | 025 207 |
| TRACTCE20 | other | 205 | 0 | 981501 2; 070901 2; 060601 2; 070801 2 |
| GEOID20 | other | 210 | 0 | 25025981501 2; 25025070901 2; 25025060601 2; 25025070801 2 |
| NAME20 | amount | 204 | 0 | 9815.01 2; 709.01 2; 606.01 2; 708.01 2 |
| NAMELSAD20 | who | 1 | 0 | Census Tract 207 |
| MTFCC20 | other | 1 | 0 | G5020 207 |
| FUNCSTAT20 | other | 1 | 0 | S 207 |
| ALAND20 | amount | 209 | 0 | 897746.000000000000000 2; 57691.000000000000000 2; 140332.000000000000000 2; 61235.000000000000000 2 |
| AWATER20 | amount | 65 | 0 | 0.000000000000000 144; 1203439.000000000000000 1; 4897.000000000000000 1; 629367.000000000000000 1 |
| INTPTLAT20 | other | 208 | 0 | +42.3524288 2; +42.3377169 2; +42.3392514 2; +42.3399771 2 |
| INTPTLON20 | amount | 207 | 0 | -071.0878101 2; -071.0795662 2; -071.0489604 2; -071.0825322 2 |
| SHAPE_LENGTH | amount | 208 | 0 | 0.264966468851378 2; 0.012518439640377 2; 0.016806852141929 2; 0.010827258606449 2 |
| SHAPE_AREA | amount | 210 | 0 | 0.000229610414458 2; 0.000006302014173 2; 0.000015330142139 2; 0.000006689452013 2 |
| SHAPE_WKT | empty | 1 | 207 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:36:46.13333 207 |
| SOURCE_RUN_ID | audit | 1 | 0 | c832a2de-79b8-4679-8085-9 207 |
| SRC_SHA256 | who | 1 | 0 | 5ac315fe47d4f1da70dae6fe1 207 |
