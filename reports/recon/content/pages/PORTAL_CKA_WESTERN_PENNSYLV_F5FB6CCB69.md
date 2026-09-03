# PORTAL_CKA_WESTERN_PENNSYLV_F5FB6CCB69

rows 6  columns 16  scan 2.6s

roles: audit 2, category 8, date 2, other 3, who 2

## when

DATE_TIME
  2024         6  ##############################

INGESTED_AT
  2026         6  ##############################

## who

EXTERNAL_ATTR by rows
         6  2175008768

SRC_SHA256 by rows
         6  3305b18abe3d2cf374e31db19388fc2963897c9664051a06c38d4d086b6b29a7

## who x when

EXTERNAL_ATTR by DATE_TIME
  2175008768                                2024:6

SRC_SHA256 by DATE_TIME
  3305b18abe3d2cf374e31db19388fc2963897c96  2024:6

## what

FILENAME: EMS_Station.cpg 17%, EMS_Station.prj 17%, EMS_Station.shp 17%, EMS_Station.shx 17%, EMS_Station.dbf 17%, EMS_Station.xml 17%

COMPRESSED_SIZE: 5 17%, 336 17%, 300 17%, 93 17%, 993 17%, 966 17%

FILE_SIZE: 5 17%, 559 17%, 492 17%, 212 17%, 2660 17%, 3857 17%

COMPRESSION_RATIO: 100.00% 17%, 60.11% 17%, 60.98% 17%, 43.87% 17%, 37.33% 17%, 25.05% 17%

EXTRACT_VERSION: 20 83%, 10 17%

INTERNAL_ATTR: 1 50%, 0 50%

CRC: 243350608 17%, 2752819223 17%, 588931768 17%, 1736402519 17%, 877682697 17%, 3895500936 17%

COMPRESS_TYPE: 8 83%, 0 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FILENAME | category | 6 | 0 | EMS_Station.cpg 1; EMS_Station.prj 1; EMS_Station.shp 1; EMS_Station.shx 1 |
| COMPRESSED_SIZE | category | 6 | 0 | 5 1; 336 1; 300 1; 93 1 |
| FILE_SIZE | category | 6 | 0 | 5 1; 559 1; 492 1; 212 1 |
| COMPRESSION_RATIO | category | 6 | 0 | 100.00% 1; 60.11% 1; 60.98% 1; 43.87% 1 |
| DATE_TIME | date | 2 | 0 | 2024-12-04T05:19:04 5; 2024-12-04T05:19:06 1 |
| CREATE_SYSTEM | other | 1 | 0 | 3 6 |
| CREATE_VERSION | other | 1 | 0 | 30 6 |
| EXTRACT_VERSION | category | 2 | 0 | 20 5; 10 1 |
| FLAG_BITS | other | 1 | 0 | 0 6 |
| INTERNAL_ATTR | category | 2 | 0 | 1 3; 0 3 |
| EXTERNAL_ATTR | who | 1 | 0 | 2175008768 6 |
| CRC | category | 6 | 0 | 243350608 1; 2752819223 1; 588931768 1; 1736402519 1 |
| COMPRESS_TYPE | category | 2 | 0 | 8 5; 0 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:53.89643 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0b8d9f34-4549-424d-b065-d 6 |
| SRC_SHA256 | who | 1 | 0 | 3305b18abe3d2cf374e31db19 6 |
