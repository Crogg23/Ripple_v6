# PORTAL_CKA_OPEN_DATA_SA_1E2348F9B1

rows 10.0K  columns 10  scan 2.4s

roles: amount 2, audit 2, category 3, date 1, id 2, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 10.0K | 0 | 105.2K | 11.07M | 1.39B | 10.47B |
| SHAPE__LENGTH | 10.0K | 0.08 | 1.7K | 28.4K | 675.1K | 30.30M |

## who

SRC_SHA256 by rows
     10.0K  9b8572f88f70a639069d723656ace9ce2de06feee4f90198ff3186a8560edba5

SRC_SHA256 by dollars
      10.47B    10.0K rows  9b8572f88f70a639069d723656ace9ce2de06feee4f90198ff3186a8560e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  9b8572f88f70a639069d723656ace9ce2de06fee  2026:10.47B

## what

PLANNAME: San Antonio International Airp 22%, Near Northwest 12%, Greater Dellview Area 10%, South Central 10%, I-10 East Corridor 9%, North Central 8%, Northwest 8%, Eastern Triangle 6%, Northeast Inner Loop 6%, Kelly/South San PUEBLO 5%, Stinson Airport Vicinity 3%

LANDUSE: Low Density Residential 58%, Urban Low Density Residential 12%, Parks Open Space 6%, Neighborhood Commercial 6%, Community Commercial 5%, Medium Density Residential 3%, Mixed Use 3%, Public Institutional 2%, Low Density Mixed Use 2%, Residential Estate 1%, High Density Residential 1%

CENTERTIERS: Suburban Tier 75%, Natural Tier 12%, Rural Estate Tier 3%, General Urban Tier 2%, Civic Center 2%, Mixed Use Center 2%, Regional Center 1%, Specialized Center 1%, Country Tier 1%, Agribusiness Tier 1%, Military Center 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| PLANNAME | category | 35 | 584 | San Antonio International 1.7K; Near Northwest 959; Greater Dellview Area 838; South Central 772 |
| LANDUSE | category | 39 | 106 | Low Density Residential 5.5K; Urban Low Density Residen 1.2K; Parks Open Space 586; Neighborhood Commercial 584 |
| CENTERTIERS | category | 14 | 7.2K | Suburban Tier 2.1K; Natural Tier 340; Rural Estate Tier 84; General Urban Tier 62 |
| GLOBALID | id | 9.9K | 0 | 3d8e2ef3-f534-4a79-8f11-d 50; 74668940-0329-4b74-a91d-9 50; f876203e-f35a-4756-b075-2 50; a12b4a67-ede2-4081-aacd-2 50 |
| SHAPE__AREA | amount | 9.9K | 0 | 0.00390625 52; 39620.349609375 50; 156322.474609375 50; 170006.671875 50 |
| SHAPE__LENGTH | amount | 10.2K | 0 | 4.05337126331397 51; 867.803546074611 50; 1780.02772677876 50; 1982.01562136621 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:04:38.22762 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8f50ba61-c7c9-4472-9902-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | 9b8572f88f70a639069d72365 10.0K |
