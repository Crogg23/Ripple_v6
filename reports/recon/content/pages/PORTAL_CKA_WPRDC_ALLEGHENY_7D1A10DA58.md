# PORTAL_CKA_WPRDC_ALLEGHENY_7D1A10DA58

rows 692  columns 10  scan 4.9s

roles: amount 3, audit 2, category 1, date 1, other 2, who 2

## when

INGESTED_AT
  2026       692  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 692 | 1.5K | 68.5K | 5.89M | 12.25M | 260.77M |
| SHAPE_LENGTH | 692 | 158.19 | 1.6K | 30.1K | 129.2K | 2.40M |
| SQFT | 692 | 9.1K | 426.8K | 36.68M | 76.36M | 1.62B |

## who

DATA_YEAR by rows
       692  1967 map

DATA_YEAR by dollars
     260.77M      692 rows  1967 map

SRC_SHA256 by rows
       692  1598ae966db50f2b81c4284ab3292cbb677aa60b5f3d62421fc8959eeffd11cb

SRC_SHA256 by dollars
     260.77M      692 rows  1598ae966db50f2b81c4284ab3292cbb677aa60b5f3d62421fc8959eeffd

## who x when

DATA_YEAR by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  1967 map                                  2026:260.77M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  1598ae966db50f2b81c4284ab3292cbb677aa60b  2026:260.77M

## what

ZONING_DISTRICT: C3 16%, S 16%, R2 12%, C1 11%, R3 8%, R1 8%, R4 8%, M2 6%, M1 6%, M3 5%, RP 2%, R5 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATA_YEAR | who | 1 | 0 | 1967 map 692 |
| OBJECTID | other | 679 | 0 | 692 4; 691 4; 690 4; 689 4 |
| SHAPE_AREA | amount | 699 | 0 | 467781.04629450914 4; 20618.936417956986 4; 63712.54523609904 4; 21919.10772066862 4 |
| SHAPE_LENGTH | amount | 686 | 0 | 3639.3035372945947 4; 577.2362008155773 4; 2304.7657307320765 4; 625.5251980131566 4 |
| SQFT | amount | 690 | 0 | 2916176.6701477747 4; 128429.26294926429 4; 397173.08770363225 4; 136637.40614370597 4 |
| ZONING_DISTRICT | category | 26 | 0 | C3 102; S 102; R2 73; C1 67 |
| GEOMETRY | other | 691 | 0 | POLYGON ((587542.66037750 4; POLYGON ((586076.58996624 4; POLYGON ((588380.04091121 4; POLYGON ((586934.59078371 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:45:43.08051 692 |
| SOURCE_RUN_ID | audit | 1 | 0 | ef6296d1-577b-4d31-96e1-0 692 |
| SRC_SHA256 | who | 1 | 0 | 1598ae966db50f2b81c4284ab 692 |
