# PORTAL_CKA_ANALYZE_BOSTON_BE87D5EA10

rows 10.0K  columns 15  scan 3.9s

roles: amount 5, audit 2, category 5, date 2, other 1, who 1

## when

ADDED
  2014         4  #######
  2019         3  #####
  2020        17  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GRND_ELEV_2010 | 10.0K | -2 | 34.82 | 167.06 | 187.90 | 479.7K |
| ROOF_ELEV_2010 | 10.0K | 10.80 | 68.05 | 193.14 | 694.06 | 810.8K |
| BLDG_HGT_2010 | 10.0K | 1.50 | 28.82 | 97.53 | 685 | 331.2K |
| SHAPE_LENGTH | 10.0K | 0 | 0 | 0 | 0.01 | 0.13 |
| SHAPE_AREA | 10.0K | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
     10.0K  75a0a9f7f16ea00134f119633261518e3170140e16e10cff5d21c97d6209e1b2

SRC_SHA256 by dollars
      479.7K    10.0K rows  75a0a9f7f16ea00134f119633261518e3170140e16e10cff5d21c97d6209

## who x when

SRC_SHA256 by ADDED, dollars = GRND_ELEV_2010
  75a0a9f7f16ea00134f119633261518e3170140e  2014:148.86 2019:60.23 2020:893

## what

PART_USE: R2 26%, R1 20%, CM 12%, R3 10%, A 8%, C 7%, E 7%, R4 5%, RC 4%, I 2%, RL 0%, EA 0%

PART_BRA_U: R2 24%, R1 19%, CM 11%, R3 9%, A 8%, C 7%, RC 5%, E 5%, R4 5%, G 3%, I 2%, XG 1%

IEL_TYPE: BLDG 93%, OUTBLDG 7%, MOBILE 0%

LAND_USE: R2 23%, R1 18%, CM 12%, R3 9%, A 9%, C 8%, G 7%, RC 5%, R4 4%, E 4%, I 1%, XG 1%

BRA_LAND_USE: R2 23%, R1 18%, CM 12%, R3 9%, A 9%, C 8%, G 7%, RC 5%, R4 4%, E 4%, I 1%, XG 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PART_USE | category | 16 | 27 | R2 2.6K; R1 2.0K; CM 1.2K; R3 953 |
| PART_BRA_U | category | 17 | 21 | R2 2.4K; R1 1.9K; CM 1.1K; R3 916 |
| GRND_ELEV_2010 | amount | 9.2K | 0 | 9.000000000000000 205; 10.000000000000000 163; 8.000000000000000 126; 11.000000000000000 88 |
| ROOF_ELEV_2010 | amount | 7.5K | 0 | 45.299999999999997 55; 92.750000000000000 54; 45.460000000000001 53; 45.649999999999999 53 |
| BLDG_HGT_2010 | amount | 9.8K | 0 | 19.709400930000001 55; 52.390598290000000 54; 20.102299649999999 53; 19.991699600000000 53 |
| IEL_TYPE | category | 3 | 0 | BLDG 9.3K; OUTBLDG 731; MOBILE 3 |
| LAND_USE | category | 15 | 0 | R2 2.3K; R1 1.8K; CM 1.2K; R3 892 |
| BRA_LAND_USE | category | 15 | 0 | R2 2.3K; R1 1.8K; CM 1.2K; R3 892 |
| ADDED | date | 13 | 10.0K | 4/3/2020 0:00:00 5; 3/30/2020 0:00:00 4; 10/11/2019 0:00:00 2; 3/26/2020 0:00:00 2 |
| SHAPE_LENGTH | amount | 9.9K | 0 | 0.000406457045229 50; 0.000407335172491 50; 0.000324582712574 50; 0.000352992384242 50 |
| SHAPE_AREA | amount | 9.9K | 0 | 0.000000007669255 50; 0.000000007988841 50; 0.000000006446670 50; 0.000000006952494 50 |
| SHAPE_WKT | other | 992 | 9.0K | MULTIPOLYGON ZM (((-71.06 6; MULTIPOLYGON ZM (((-71.06 6; MULTIPOLYGON ZM (((-71.07 6; MULTIPOLYGON ZM (((-71.07 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:04:51.64100 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 7e2d4e02-e2ce-4e1b-ad83-a 10.0K |
| SRC_SHA256 | who | 1 | 0 | 75a0a9f7f16ea00134f119633 10.0K |
