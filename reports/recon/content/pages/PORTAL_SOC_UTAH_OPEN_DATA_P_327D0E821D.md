# PORTAL_SOC_UTAH_OPEN_DATA_P_327D0E821D

rows 2.0K  columns 22  scan 3.0s

roles: audit 2, category 8, date 1, id 1, other 6, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

NAME by rows
         4  WALGREENS
         4  LAB CORP OF AMERICA
         3  GOWIRELESS, INC.
         3  DEPT OF TRANSPORTATON
         3  US BANK NATIONAL ASSOC
         3  7-ELEVEN
         3  MCDONALDS
         3  ZIONS 1ST NATIONAL BANK
         3  H & R BLOCK
         3  WELLS FARGO BANK N A
         3  ARCTIC CIRCLE RESTAURANTS, INC.
         2  XPO LOGISTICS INC
         2  BURGER KING
         2  TACO BELL
         2  STARBUCKS COFFEE
         2  SPRINT CORP
         2  SPRING COMMUNICATIONS HOLDING LLC
         2  US POSTAL SERVICE
         2  TARGET CORP
         2  AMERICA FIRST CREDIT UNION

COUNTYNAME by rows
      2.0K  Salt Lake

NAICS by rows
        65  722513
        52  531210
        44  541110
        44  624120
        39  621111
        34  541511
        33  524210
        32  722511
        31  541611
        28  621210
        24  238221
        22  561730
        21  541330
        20  425120
        20  561720
        20  236118
        19  531311
        19  236115
        18  812112
        17  561110

ADDRESS2 by rows
      1.8K  nan
        11  STE 200
         4  STE 100
         4  STE 101
         3  STE 110
         3  STE 230
         3  SUITE 100
         3  STE B
         3  STE C
         3  SUITE B
         2  SUITE 400
         2  STE 300
         2  STE D
         2  APT 4
         2  STE 2
         2  STE 150
         2  STE 250
         2  STE 120
         2  STE G
         2  SUITE 300

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  7-ELEVEN                                  2026:3
  AMERICA FIRST CREDIT UNION                2026:2
  ARCTIC CIRCLE RESTAURANTS, INC.           2026:3
  BURGER KING                               2026:2
  DEPT OF TRANSPORTATON                     2026:3
  GOWIRELESS, INC.                          2026:3
  H & R BLOCK                               2026:3
  LAB CORP OF AMERICA                       2026:4
  MCDONALDS                                 2026:3
  SPRING COMMUNICATIONS HOLDING LLC         2026:2
  SPRINT CORP                               2026:2
  STARBUCKS COFFEE                          2026:2
  TACO BELL                                 2026:2
  TARGET CORP                               2026:2
  US BANK NATIONAL ASSOC                    2026:3
  US POSTAL SERVICE                         2026:2
  WALGREENS                                 2026:4
  WELLS FARGO BANK N A                      2026:3
  XPO LOGISTICS INC                         2026:2
  ZIONS 1ST NATIONAL BANK                   2026:3

COUNTYNAME by INGESTED_AT  LOAD STAMP, not an event date
  Salt Lake                                 2026:2.0K

## what

CITY: SALT LAKE CITY 53%, SANDY 10%, SOUTH JORDAN 6%, WEST JORDAN 6%, DRAPER 6%, WEST VALLEY CITY 4%, MIDVALE 4%, RIVERTON 4%, MURRAY 3%, HERRIMAN 2%, TAYLORSVILLE 2%, BLUFFDALE 1%

EMPRANGE: 1-4 44%, 5-9 17%, 10-19 14%, 0 10%, 20-49 9%, 50-99 4%, 100-249 2%, 250-499 1%, 500-999 0%, 1000-1999 0%, 5000-6999 0%

EMPRANGECODE: B 44%, C 17%, D 14%, A 10%, E 9%, F 4%, G 2%, H 1%, I 0%, J 0%, N 0%

OWNERSHIP: Private 98%, Local 1%, State 1%, Federal 0%

COMPUTED_REGION_5D9V_6BUI: 26 98%, 5 1%, 22 1%, 8 0%, 19 0%, 7 0%, 16 0%, 6 0%, 11 0%

COMPUTED_REGION_QMWN_IMPY: 220 32%, 180 10%, nan 8%, 98 8%, 242 7%, 181 7%, 245 7%, 224 6%, 109 4%, 247 4%, 244 3%, 246 3%

COMPUTED_REGION_2FPW_SWV9: 42 16%, 24 12%, 21 12%, 34 9%, 38 9%, 27 8%, 30 7%, 28 6%, 26 6%, 23 6%, 32 5%, 29 5%

COMPUTED_REGION_MI24_NG5Q: 29 98%, 19 1%, 23 1%, 15 0%, 17 0%, 8 0%, 4 0%, 12 0%, 9 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 2.0K | 0 | ALDOUS & ASSOCIATES 10; NORTH AMERICAN INDUSTRIAL 10; KEVIN RYAN WORLDWIDE INC 10; MINDRAY DS USA, INC. 10 |
| CITY | category | 46 | 0 | SALT LAKE CITY 1.0K; SANDY 190; SOUTH JORDAN 122; WEST JORDAN 120 |
| STATE | other | 1 | 0 | UT 2.0K |
| ZIP | other | 1.3K | 0 | 84104 44; 84107 42; 84020 35; 84115 34 |
| COUNTYCODE | other | 1 | 0 | 35 2.0K |
| COUNTYNAME | who | 1 | 0 | Salt Lake 2.0K |
| EMPRANGE | category | 11 | 0 | 1-4 871; 5-9 334; 10-19 273; 0 200 |
| EMPRANGECODE | category | 11 | 0 | B 871; C 334; D 273; A 200 |
| NAICS | who | 445 | 0 | 722513 65; 531210 52; 541110 44; 624120 44 |
| OWNERSHIP | category | 4 | 0 | Private 2.0K; Local 19; State 14; Federal 4 |
| GEOCODED_COLUMN | other | 1.9K | 0 | {"type": "Point", "coordi 11; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| COMPUTED_REGION_5D9V_6BUI | category | 9 | 0 | 26 1.9K; 5 16; 22 11; 8 6 |
| COMPUTED_REGION_QMWN_IMPY | category | 41 | 0 | 220 575; 180 174; nan 144; 98 136 |
| COMPUTED_REGION_JDNU_JMST | other | 67 | 0 | 53 128; 51 107; 64 104; 72 99 |
| COMPUTED_REGION_2FPW_SWV9 | category | 44 | 0 | 42 229; 24 173; 21 167; 34 128 |
| COMPUTED_REGION_MI24_NG5Q | category | 9 | 0 | 29 1.9K; 19 16; 23 11; 15 6 |
| ADDRESS1 | id | 2.0K | 0 | nan 26; 4625 S 2300 E, STE 207 10; 3567 W DIRECTORS ROW 10; 11833 HIDDEN VALLEY RD 10 |
| PHONE | other | 1.5K | 0 | nan 374; (801) 359-4699 17; (801) 676-0945 12; (801) 676-0119 10 |
| ADDRESS2 | who | 121 | 0 | nan 1.8K; STE 200 11; STE 101 4; STE 100 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:50.75804 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c1ba3444-0be2-406d-a7ae-f 2.0K |
| SRC_SHA256 | who | 1 | 0 | ba710ccb49cc5e666fcd9e952 2.0K |
