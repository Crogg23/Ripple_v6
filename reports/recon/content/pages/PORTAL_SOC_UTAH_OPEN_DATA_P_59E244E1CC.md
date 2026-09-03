# PORTAL_SOC_UTAH_OPEN_DATA_P_59E244E1CC

rows 5.0K  columns 16  scan 3.6s

roles: audit 2, category 6, date 1, id 1, other 3, who 4

## when

INGESTED_AT
  2026      5.0K  ##############################

## who

NAME by rows
        74  AMERICA FIRST CREDIT UNION
        49  7-ELEVEN
        36  AUTOZONE
        26  ALCOHOLIC BEVERAGE CONTROL
        24  ARO
        21  ALTABANK
        18  ARBYS
        17  BANK OF UTAH
        16  ARBY'S
        15  1ST AMERICAN TITLE INSURANCE
        14  ARCTIC CIRCLE RESTAURANTS, INC.
        11  AT T MOBILITY SERVICES LLC
         9  ABRA INC
         8  ACADEMY MORTGAGE CORPORATION
         7  ARMY NATIONAL GUARD UNITS  TITLE 32
         7  AMERICAN NATIONAL RED CROSS
         7  AMERICAN EAGLE OUTFITTERS
         7  BACKMAN TITLE
         6  ALPINE CREDIT UNION
         6  7 PEAKS

NAICS by rows
       120  624120
       117  531210
       109  238221
        94  454390
        94  722513
        82  541611
        82  522130
        78  236115
        74  561730
        72  524210
        70  621210
        68  447110
        66  541511
        63  621111
        58  722511
        58  441310
        55  811111
        54  541330
        52  541613
        50  236118

CITY by rows
       332  OGDEN
       314  SAINT GEORGE
       263  OREM
       227  PROVO
       170  LOGAN
       164  PARK CITY
       160  LEHI
       150  LAYTON
       136  AMERICAN FORK
       113  BOUNTIFUL
       100  CEDAR CITY
        89  VERNAL
        87  SPANISH FORK
        75  PLEASANT GROVE
        73  NORTH SALT LAKE
        68  KAYSVILLE
        67  LINDON
        66  HEBER CITY
        66  WASHINGTON
        66  CLEARFIELD

SRC_SHA256 by rows
      5.0K  91b16c1f829eded9b7f85af4a1096e136eff7056bace5fee6e152abfe1727b89

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  1ST AMERICAN TITLE INSURANCE              2026:15
  7 PEAKS                                   2026:6
  7-ELEVEN                                  2026:49
  ABRA INC                                  2026:9
  ACADEMY MORTGAGE CORPORATION              2026:8
  ALCOHOLIC BEVERAGE CONTROL                2026:26
  ALPINE CREDIT UNION                       2026:6
  ALTABANK                                  2026:21
  AMERICA FIRST CREDIT UNION                2026:74
  AMERICAN EAGLE OUTFITTERS                 2026:7
  AMERICAN NATIONAL RED CROSS               2026:7
  ARBY'S                                    2026:16
  ARBYS                                     2026:18
  ARCTIC CIRCLE RESTAURANTS, INC.           2026:14
  ARMY NATIONAL GUARD UNITS  TITLE 32       2026:7
  ARO                                       2026:24
  AT T MOBILITY SERVICES LLC                2026:11
  AUTOZONE                                  2026:36
  BACKMAN TITLE                             2026:7
  BANK OF UTAH                              2026:17

NAICS by INGESTED_AT  LOAD STAMP, not an event date
  236115                                    2026:78
  236118                                    2026:50
  238221                                    2026:109
  441310                                    2026:58
  447110                                    2026:68
  454390                                    2026:94
  522130                                    2026:82
  524210                                    2026:72
  531210                                    2026:117
  541330                                    2026:54
  541511                                    2026:66
  541611                                    2026:82
  541613                                    2026:52
  561730                                    2026:74
  621111                                    2026:63
  621210                                    2026:70
  624120                                    2026:120
  722511                                    2026:58
  722513                                    2026:94
  811111                                    2026:55

## what

STATE: UT 100%

COUNTYCODE: 49 35%, 11 16%, 57 12%, 53 12%, 5 7%, 43 5%, 21 3%, 51 2%, 47 2%, 3 2%, 45 2%, 13 1%

COUNTYNAME: Utah 35%, Davis 16%, Weber 12%, Washington 12%, Cache 7%, Summit 5%, Iron 3%, Wasatch 2%, Uintah 2%, Box Elder 2%, Tooele 2%, Duchesne 1%

EMPRANGE: 1-4 45%, 5-9 17%, 0 14%, 10-19 12%, 20-49 8%, 50-99 2%, 100-249 1%, 250-499 0%, 500-999 0%, 1000-1999 0%, 2000-2999 0%, 10000-14999 0%

EMPRANGECODE: B 45%, C 17%, A 14%, D 12%, E 8%, F 2%, G 1%, H 0%, I 0%, J 0%, K 0%, P 0%

OWNERSHIP: Private 98%, Local 1%, State 1%, Federal 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 4.6K | 0 | AMERICA FIRST CREDIT UNIO 86; AUTOZONE 57; 7-ELEVEN 50; ARO 41 |
| ADDRESS1 | id | 4.1K | 742 | 300 S 200 W 23; 218 SOUTH UNIVERSITY AVE 22; 2301 N 750 W 22; 80 E 800 S 22 |
| CITY | who | 217 | 707 | OGDEN 332; SAINT GEORGE 314; OREM 263; PROVO 227 |
| STATE | category | 2 | 707 | UT 4.3K |
| ZIP | other | 2.7K | 707 | 84003 74; 84043 63; 84790 54; 84770 53 |
| COUNTYCODE | category | 27 | 0 | 49 1.6K; 11 772; 57 571; 53 541 |
| COUNTYNAME | category | 27 | 0 | Utah 1.6K; Davis 772; Weber 571; Washington 541 |
| PHONE | other | 3.8K | 756 | (801) 359-4699 61; (623) 792-6100 27; (435) 750-5566 25; (801) 616-1421 22 |
| EMPRANGE | category | 12 | 0 | 1-4 2.3K; 5-9 873; 0 675; 10-19 596 |
| EMPRANGECODE | category | 12 | 0 | B 2.3K; C 873; A 675; D 596 |
| NAICS | who | 585 | 0 | 624120 120; 531210 117; 238221 109; 722513 94 |
| OWNERSHIP | category | 4 | 0 | Private 4.9K; Local 55; State 28; Federal 15 |
| ADDRESS2 | other | 228 | 4.7K | STE B 7; STE 1 7; STE 100 6; STE 101 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:48:47.14360 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1a15505d-f4c2-4c35-9951-2 5.0K |
| SRC_SHA256 | who | 1 | 0 | 91b16c1f829eded9b7f85af4a 5.0K |
