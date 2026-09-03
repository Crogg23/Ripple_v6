# PORTAL_SOC_UTAH_OPEN_DATA_P_5A037856FE

rows 2.0K  columns 13  scan 3.2s

roles: audit 2, category 3, date 1, other 3, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

NAME by rows
        27  7-ELEVEN
        26  AMERICA FIRST CREDIT UNION
         6  ALLSTATE
         5  AMERICAN UNITED FCU
         5  AFTER HOURS MEDICAL COMPANY
         4  ACADEMY MORTGAGE CORPORATION
         4  24 HOUR FITNESS
         4  ABRA UTAH INC
         4  ALCATEL-LUCENT USA INC
         3  1-800 CONTACTS, INC.
         3  3M CO
         3  AEROPOSTALE
         3  AETNA LIFE INSURANCE CO
         3  AMERICAN PREPARATORY ACADEMY
         2  ADVANTAGE FINANCIAL SERVICES INC
         2  AMERICA'S BEST
         2  AMERICAN EAGLE OUTFITTER
         2  ALTA VIEW/HIDDEN VALLEY INT MED
         2  3M HEALTH INFORMATION SYSTEMS
         2  401K ADVISORS INTERMOUNTAIN, INC.

COUNTYNAME by rows
      2.0K  Salt Lake

NAICS by rows
        56  425120
        48  447110
        36  561320
        35  541511
        32  238221
        31  522130
        29  621111
        28  561730
        28  541611
        27  524210
        25  531210
        25  561720
        22  624120
        22  445120
        21  423450
        20  561110
        19  541512
        19  621610
        19  561330
        17  541330

LOCATION_2 by rows
      1.8K  nan
         9  {"human_address": "{\"address\": \"STE 200\", \"city\": \"\", \"state\
         7  {"human_address": "{\"address\": \"STE 100\", \"city\": \"\", \"state\
         5  {"human_address": "{\"address\": \"STE 150\", \"city\": \"\", \"state\
         5  {"human_address": "{\"address\": \"STE A\", \"city\": \"\", \"state\":
         4  {"human_address": "{\"address\": \"STE B\", \"city\": \"\", \"state\":
         4  {"human_address": "{\"address\": \"STE 105\", \"city\": \"\", \"state\
         4  {"human_address": "{\"address\": \"STE 3\", \"city\": \"\", \"state\":
         3  {"human_address": "{\"address\": \"SUITE 200\", \"city\": \"\", \"stat
         3  {"human_address": "{\"address\": \"STE 101\", \"city\": \"\", \"state\
         3  {"human_address": "{\"address\": \"STE C\", \"city\": \"\", \"state\":
         3  {"human_address": "{\"address\": \"STE 120\", \"city\": \"\", \"state\
         2  {"human_address": "{\"address\": \"STE F\", \"city\": \"\", \"state\":
         2  {"human_address": "{\"address\": \"STE 4\", \"city\": \"\", \"state\":
         2  {"human_address": "{\"address\": \"STE 5\", \"city\": \"\", \"state\":
         2  {"human_address": "{\"address\": \"STE 11\", \"city\": \"\", \"state\"
         2  {"human_address": "{\"address\": \"STE 6\", \"city\": \"\", \"state\":
         2  {"human_address": "{\"address\": \"STE 550\", \"city\": \"\", \"state\
         2  {"human_address": "{\"address\": \"STE 102\", \"city\": \"\", \"state\
         2  {"human_address": "{\"address\": \"STE 300\", \"city\": \"\", \"state\

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  1-800 CONTACTS, INC.                      2026:3
  24 HOUR FITNESS                           2026:4
  3M CO                                     2026:3
  3M HEALTH INFORMATION SYSTEMS             2026:2
  401K ADVISORS INTERMOUNTAIN, INC.         2026:2
  7-ELEVEN                                  2026:27
  ABRA UTAH INC                             2026:4
  ACADEMY MORTGAGE CORPORATION              2026:4
  ADVANTAGE FINANCIAL SERVICES INC          2026:2
  AEROPOSTALE                               2026:3
  AETNA LIFE INSURANCE CO                   2026:3
  AFTER HOURS MEDICAL COMPANY               2026:5
  ALCATEL-LUCENT USA INC                    2026:4
  ALLSTATE                                  2026:6
  ALTA VIEW/HIDDEN VALLEY INT MED           2026:2
  AMERICA FIRST CREDIT UNION                2026:26
  AMERICA'S BEST                            2026:2
  AMERICAN EAGLE OUTFITTER                  2026:2
  AMERICAN PREPARATORY ACADEMY              2026:3
  AMERICAN UNITED FCU                       2026:5

COUNTYNAME by INGESTED_AT  LOAD STAMP, not an event date
  Salt Lake                                 2026:2.0K

## what

EMPRANGE:  1-4 46%,  0 15%,  5-9 13%,  10-19 12%,  20-49 7%,  50-99 3%,  100-249 2%,  250-499 1%,  500-999 0%

EMPRANGECODE: B 46%, A 15%, C 13%, D 12%, E 7%, F 3%, G 2%, H 1%, I 0%

OWNERSHIP: Private 100%, Local 0%, State 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 1.9K | 0 | AMERICA FIRST CREDIT UNIO 34; 7-ELEVEN 27; AMERICAN UNITED FCU 14; ALLSTATE 13 |
| COUNTYCODE | other | 1 | 0 | 35 2.0K |
| COUNTYNAME | who | 1 | 0 | Salt Lake 2.0K |
| PHONE | other | 1.6K | 0 | nan 235; (314) 997-2100 23; (801) 232-8468 16; (801) 359-4699 16 |
| EMPRANGE | category | 9 | 0 |  1-4 922;  0 308;  5-9 269;  10-19 248 |
| EMPRANGECODE | category | 9 | 0 | B 922; A 308; C 269; D 248 |
| NAICS | who | 441 | 0 | 425120 56; 447110 48; 522130 36; 561320 36 |
| OWNERSHIP | category | 3 | 0 | Private 2.0K; Local 4; State 2 |
| LOCATION_1 | other | 1.3K | 0 | nan 596; {"latitude": "40.67689237 8; {"latitude": "40.72978084 8; {"latitude": "40.52795983 8 |
| LOCATION_2 | who | 105 | 0 | nan 1.8K; {"human_address": "{\"add 9; {"human_address": "{\"add 7; {"human_address": "{\"add 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:50:14.32314 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 88c7727f-3a6c-43c8-aad1-1 2.0K |
| SRC_SHA256 | who | 1 | 0 | e65bb36bb09553ceda384bbe2 2.0K |
