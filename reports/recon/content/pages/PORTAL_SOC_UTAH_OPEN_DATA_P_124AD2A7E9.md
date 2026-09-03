# PORTAL_SOC_UTAH_OPEN_DATA_P_124AD2A7E9

rows 5.0K  columns 16  scan 3.6s

roles: audit 2, category 4, date 1, id 1, other 4, who 5

## when

INGESTED_AT
  2026      5.0K  ##############################

## who

NAME by rows
        53  7-ELEVEN
        33  AMERICA FIRST CREDIT UNION
        22  AUTOZONE
        22  ALCOHOLIC BEVERAGE CONTROL
        16  ARBYS
        16  ARO
        16  ARCTIC CIRCLE RESTAURANTS, INC.
        12  AT T MOBILITY SERVICES LLC
        10  1ST AMERICAN TITLE INSURANCE
        10  ARS - FRESNO LLC.
         7  APOLLO BURGER
         7  BARBACOA MEXICAN GRILL
         7  BATH   BODY WORKS  LLC
         7  BARNES & NOBLE BOOKSELLERS
         7  AIRGAS USA LLC
         6  ALTABANK
         5  BANK OF THE WEST
         5  AMERICAN NATIONAL RED CROSS
         5  ARBY'S
         5  24 HOUR FITNESS

COUNTYNAME by rows
      5.0K  Salt Lake

NAICS by rows
       123  541511
       118  624120
       107  541611
        89  722513
        82  561320
        78  425120
        71  541330
        70  447110
        70  524210
        63  531210
        63  541990
        59  238221
        59  541512
        52  541613
        51  561730
        48  621210
        47  561720
        46  561110
        46  541110
        45  238211

CITY by rows
      1.7K  SALT LAKE CITY
       395  SANDY
       197  WEST JORDAN
       190  DRAPER
       162  SOUTH JORDAN
       138  MIDVALE
       133  MURRAY
       124  WEST VALLEY CITY
       100  RIVERTON
        61  TAYLORSVILLE
        51  HERRIMAN
        30  COTTONWOOD HEIGHTS
        25  MAGNA
        24  BLUFFDALE
        22  HOLLADAY
        16  KEARNS
        14  SOUTH SALT LAKE
        10  LEHI
         8  MILLCREEK
         7  OGDEN

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  1ST AMERICAN TITLE INSURANCE              2026:10
  24 HOUR FITNESS                           2026:5
  7-ELEVEN                                  2026:53
  AIRGAS USA LLC                            2026:7
  ALCOHOLIC BEVERAGE CONTROL                2026:22
  ALTABANK                                  2026:6
  AMERICA FIRST CREDIT UNION                2026:33
  AMERICAN NATIONAL RED CROSS               2026:5
  APOLLO BURGER                             2026:7
  ARBY'S                                    2026:5
  ARBYS                                     2026:16
  ARCTIC CIRCLE RESTAURANTS, INC.           2026:16
  ARO                                       2026:16
  ARS - FRESNO LLC.                         2026:10
  AT T MOBILITY SERVICES LLC                2026:12
  AUTOZONE                                  2026:22
  BANK OF THE WEST                          2026:5
  BARBACOA MEXICAN GRILL                    2026:7
  BARNES & NOBLE BOOKSELLERS                2026:7
  BATH   BODY WORKS  LLC                    2026:7

COUNTYNAME by INGESTED_AT  LOAD STAMP, not an event date
  Salt Lake                                 2026:5.0K

## what

STATE: UT 100%

EMPRANGE: 1-4 48%, 0 15%, 5-9 14%, 10-19 11%, 20-49 7%, 50-99 3%, 100-249 1%, 250-499 0%, 500-999 0%, 2000-2999 0%

EMPRANGECODE: B 48%, A 15%, C 14%, D 11%, E 7%, F 3%, G 1%, H 0%, I 0%, K 0%

OWNERSHIP: Private 99%, State 1%, Local 0%, Federal 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 4.6K | 0 | 7-ELEVEN 54; AMERICA FIRST CREDIT UNIO 45; AUTOZONE 42; ARO 33 |
| ADDRESS1 | id | 3.3K | 1.5K | 12733 S 2360 W 19; 136 E SOUTH TEMPLE STE 21 19; 1047 S 100 W 18; 14641 S 2200 W 18 |
| CITY | who | 60 | 1.5K | SALT LAKE CITY 1.7K; SANDY 395; WEST JORDAN 197; DRAPER 190 |
| STATE | category | 2 | 1.5K | UT 3.5K |
| ZIP | other | 2.1K | 1.5K | 84020 85; 84070 80; 84115 77; 84107 70 |
| COUNTYCODE | other | 1 | 0 | 35 5.0K |
| COUNTYNAME | who | 1 | 0 | Salt Lake 5.0K |
| PHONE | other | 3.8K | 773 | (801) 359-4699 72; (715) 651-2414 23; (763) 450-3781 23; (801) 957-1400 22 |
| EMPRANGE | category | 10 | 0 | 1-4 2.4K; 0 757; 5-9 715; 10-19 526 |
| EMPRANGECODE | category | 10 | 0 | B 2.4K; A 757; C 715; D 526 |
| NAICS | who | 578 | 0 | 541511 123; 624120 118; 541611 107; 722513 89 |
| OWNERSHIP | category | 4 | 0 | Private 5.0K; State 26; Local 11; Federal 7 |
| ADDRESS2 | other | 238 | 4.7K | STE A 11; STE 200 10; STE B 7; SUITE 200 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:45:41.28549 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3d84e435-a841-4663-8028-9 5.0K |
| SRC_SHA256 | who | 1 | 0 | 24239ba798ba87cc84b384f92 5.0K |
