# PORTAL_CKA_OPEN_DATA_SA_68BCB9DDA1

rows 20  columns 11  scan 2.8s

roles: amount 2, audit 2, category 6, date 1, who 1

## when

INGESTED_AT
  2026        20  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 20 | 1.83M | 16.60M | 126.33M | 134.10M | 615.78M |
| SHAPE__LENGTH | 20 | 11.5K | 58.3K | 151.0K | 158.9K | 1.10M |

## who

SRC_SHA256 by rows
        20  a101a407105091100083d72a72968623de8550007849b75c8b87181f685efa61

SRC_SHA256 by dollars
     615.78M       20 rows  a101a407105091100083d72a72968623de8550007849b75c8b87181f685e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  a101a407105091100083d72a72968623de855000  2026:615.78M

## what

OBJECTID: 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%

NAME: NEMetroCorridorOverlayDistrict 8%, Camp Bullis Rd 8%, Main Ave. 8%, IH-10 W 8%, North St. Mary's St 8%, San Pedro 8%, Fredericksburg Road 8%, McCullough Ave. 8%, Broadway 8%, Babcock Rd 8%, Loop N 1604 W 8%, Austin Highway 8%

STATUS: Adopted 95%, Proposed 5%

OVERLAYCODE: UC-1 24%, UC-5 12%, GC-1 12%, MC-4 6%, UC-4 6%, UC-6 6%, UC-3 6%, UC-2 6%, MC-3 6%, GC-3 6%, MC-2 6%, PC-1 6%

ORDINANCE: 2025-10-02-0691 11%, 2012-03-15-0200 11%, 2016-12-01-0902 11%, 2011-05-19-0426 11%, 2010-06-17-0576 11%, 2009-10-01-0798 11%, 2004-05-24-99358 11%, 2005-04-28-100774 11%, 2003-05-22-97656 11%

OVERLAYTYPE: 5 50%, 3 20%, 1 20%, 4 5%, 2 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 20 | 0 | 20 1; 19 1; 18 1; 17 1 |
| NAME | category | 20 | 0 | NEMetroCorridorOverlayDis 1; Camp Bullis Rd 1; Main Ave. 1; IH-10 W 1 |
| STATUS | category | 2 | 0 | Adopted 19; Proposed 1 |
| OVERLAYCODE | category | 15 | 0 | UC-1 4; UC-5 2; GC-1 2; MC-4 1 |
| ORDINANCE | category | 10 | 11 | 2025-10-02-0691 1; 2012-03-15-0200 1; 2016-12-01-0902 1; 2011-05-19-0426 1 |
| OVERLAYTYPE | category | 5 | 0 | 5 10; 3 4; 1 4; 4 1 |
| SHAPE__AREA | amount | 20 | 0 | 23797131.4746094 1; 4239670.91601563 1; 1825454.9765625 1; 75734433.7636719 1 |
| SHAPE__LENGTH | amount | 20 | 0 | 158910.718914603 1; 18503.2275669347 1; 14780.0604710295 1; 113229.235038225 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:24.07732 20 |
| SOURCE_RUN_ID | audit | 1 | 0 | a3e9e5af-3afe-4dd9-8935-7 20 |
| SRC_SHA256 | who | 1 | 0 | a101a407105091100083d72a7 20 |
