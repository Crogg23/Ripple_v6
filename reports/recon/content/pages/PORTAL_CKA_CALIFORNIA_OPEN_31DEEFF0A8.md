# PORTAL_CKA_CALIFORNIA_OPEN_31DEEFF0A8

rows 25  columns 16  scan 4.2s

roles: amount 2, audit 2, category 4, date 6, who 3

## when

EFFECTIVE
  1964         1  ##
  1986         1  ##
  2025         6  ###########
  2026        17  ##############################

RECEIVED
  2026        24  ##############################
  2027         1  #

ACKNOWLEDGED
  2026        23  ##############################

CREATED_DATE
  2026        25  ##############################

LAST_EDITED_DATE
  2026        25  ##############################

INGESTED_AT
  2026        25  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 25 | 643.90 | 161.1K | 32.87M | 43.03M | 48.72M |
| SHAPE__LENGTH | 25 | 106.70 | 1.7K | 24.4K | 30.2K | 83.2K |

## who

CREATED_USER by rows
        25  APRICE1

CREATED_USER by dollars
      48.72M       25 rows  APRICE1

LAST_EDITED_USER by rows
        25  APRICE1

LAST_EDITED_USER by dollars
      48.72M       25 rows  APRICE1

SRC_SHA256 by rows
        25  5ab1dbb6e003193f409e479eba3ea220d8bef751df5127419baa7dc53f75ec22

SRC_SHA256 by dollars
      48.72M       25 rows  5ab1dbb6e003193f409e479eba3ea220d8bef751df5127419baa7dc53f75

## who x when

CREATED_USER by EFFECTIVE, dollars = SHAPE__AREA
  APRICE1                                   1964:232.2K 1986:643.90 2025:956.0K 2026:47.53M

LAST_EDITED_USER by EFFECTIVE, dollars = SHAPE__AREA
  APRICE1                                   1964:232.2K 1986:643.90 2025:956.0K 2026:47.53M

## what

OBJECTID: 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

COFILE: 40-2027-001 15%, 50-2027-003 8%, 16-2027-000 8%, 16-2027-007 8%, 15-2027-006 8%, 56-2027-000 8%, 37-2027-009 8%, 49-2027-001 8%, 15-2027-004 8%, 10-2027-002 8%, 54-2027-003 8%, 54-2027-002 8%

CHANGE: Hanford 32%, Bakersfield 14%, Fresno 9%, Unincorporated 9%, Waterford 5%, Delano 5%, Thousand Oaks 5%, San Diego 5%, Petaluma 5%, Farmersville 5%, Porterville 5%, La Mesa 5%

NOTES: Correction per BOE file #113c 25%, Boundary correction 25%, Part 2 - Detached from city of 25%, Part 1 - Detached from city of 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 25 | 0 | 26 1; 25 1; 24 1; 23 1 |
| COFILE | category | 24 | 0 | 40-2027-001 2; 50-2027-003 1; 16-2027-000 1; 16-2027-007 1 |
| CHANGE | category | 15 | 0 | Hanford 7; Bakersfield 3; Fresno 2; Unincorporated 2 |
| EFFECTIVE | date | 20 | 0 | 1/20/2026 8:00:00 AM 5; 8/20/2025 7:00:00 AM 2; 5/26/2026 7:00:00 AM 1; 12/14/1964 8:00:00 AM 1 |
| RECEIVED | date | 16 | 0 | 2/2/2026 8:00:00 AM 4; 4/1/2026 7:00:00 AM 3; 6/2/2026 7:00:00 AM 2; 3/9/2026 7:00:00 AM 2 |
| ACKNOWLEDGED | date | 16 | 2 | 2/9/2026 8:00:00 AM 4; 4/1/2026 7:00:00 AM 3; 4/7/2026 7:00:00 AM 2; 3/3/2026 8:00:00 AM 2 |
| NOTES | category | 5 | 21 | Correction per BOE file # 1; Boundary correction 1; Part 2 - Detached from ci 1; Part 1 - Detached from ci 1 |
| CREATED_USER | who | 1 | 0 | APRICE1 25 |
| CREATED_DATE | date | 25 | 0 | 6/27/2026 2:08:25 AM 1; 6/18/2026 4:14:21 AM 1; 6/11/2026 10:54:12 PM 1; 6/11/2026 10:24:00 PM 1 |
| LAST_EDITED_USER | who | 1 | 0 | APRICE1 25 |
| LAST_EDITED_DATE | date | 25 | 0 | 6/27/2026 2:10:04 AM 1; 6/18/2026 4:16:15 AM 1; 6/11/2026 10:55:35 PM 1; 6/11/2026 10:25:07 PM 1 |
| SHAPE__AREA | amount | 25 | 0 | 279819.1640625 1; 232172.97265625 1; 585845.51171875 1; 50557.84765625 1 |
| SHAPE__LENGTH | amount | 25 | 0 | 2641.26547842685 1; 1928.94546678178 1; 3539.52022067895 1; 1451.34936114807 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:17:08.19271 25 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8e0863ad-aeca-41e6-830e-5 25 |
| SRC_SHA256 | who | 1 | 0 | 5ab1dbb6e003193f409e479eb 25 |
