# PORTAL_SOC_UTAH_OPEN_DATA_P_956795DA22

rows 5.0K  columns 12  scan 2.9s

roles: audit 2, category 4, date 1, other 2, who 4

## when

INGESTED_AT
  2026      5.0K  ##############################

## who

NAME by rows
         6  DEPT OF DEFENSE
         3  DIRECT MAIL
         2  KEYSTONE DENTAL, INC.
         2  DREAM WEAR, INC.
         2  HENRY ELLIOTT AND CO INC
         2  HEWLETT PACKARD CO
         2  ACENTIA, LLC
         2  LIVINGSTON INTERNATIONAL, INC.
         2  EMMEDIATE SUCCESS LLC
         2  3M CO
         2  FEDEX
         2  ALCATEL-LUCENT USA INC
         2  AMWINS GROUP, INC.
         2  AMERICAN TRAVELERS STAFFING PROFESS
         2  ASSET APPRAISAL SERVICES INC
         2  ALLSTATE
         1  A BEAM CONSULTING USA LTD
         1  ACTIFIO, INC.
         1  ACME CONCRETE PAVING, INC.
         1  ACE TOMATO COMPANY LLC

COUNTYNAME by rows
      5.0K  Salt Lake

NAICS by rows
       342  425120
       218  814110
       170  541511
       140  541611
       118  624120
        97  541519
        91  541512
        89  561320
        84  531210
        82  541613
        72  541990
        65  541330
        61  541690
        61  423450
        61  524210
        60  541110
        49  561110
        48  511210
        47  424210
        45  722511

SRC_SHA256 by rows
      5.0K  428e7f10ee1b60381edc36a74baaf66e15b090a20cd9127d9a687023800d9928

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  3M CO                                     2026:2
  A BEAM CONSULTING USA LTD                 2026:1
  ACE TOMATO COMPANY LLC                    2026:1
  ACENTIA, LLC                              2026:2
  ACME CONCRETE PAVING, INC.                2026:1
  ACTIFIO, INC.                             2026:1
  ALCATEL-LUCENT USA INC                    2026:2
  ALLSTATE                                  2026:2
  AMERICAN TRAVELERS STAFFING PROFESS       2026:2
  AMWINS GROUP, INC.                        2026:2
  ASSET APPRAISAL SERVICES INC              2026:2
  DEPT OF DEFENSE                           2026:6
  DIRECT MAIL                               2026:3
  DREAM WEAR, INC.                          2026:2
  EMMEDIATE SUCCESS LLC                     2026:2
  FEDEX                                     2026:2
  HENRY ELLIOTT AND CO INC                  2026:2
  HEWLETT PACKARD CO                        2026:2
  KEYSTONE DENTAL, INC.                     2026:2
  LIVINGSTON INTERNATIONAL, INC.            2026:2

COUNTYNAME by INGESTED_AT  LOAD STAMP, not an event date
  Salt Lake                                 2026:5.0K

## what

EMPRANGE:  1-4 63%, 0 23%,  5-9 7%,  10-19 4%,  20-49 2%,  50-99 0%,  100-249 0%,  250-499 0%,  500-999 0%

EMPRANGECODE: B 63%, A 23%, C 7%, D 4%, E 2%, F 0%, G 0%, H 0%, I 0%

OWNERSHIP: Private 100%, Federal 0%, State 0%, Local 0%

LOCATION_1: {"human_address": "{\"address\ 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 4.8K | 0 | LIVINGSTON INTERNATIONAL, 26; MAC WAREHOUSE LLC 25; MAC ONE CONSTRUCTION, LLC 25; MAC COSMETICS INC 25 |
| COUNTYCODE | other | 1 | 0 | 35 5.0K |
| COUNTYNAME | who | 1 | 0 | Salt Lake 5.0K |
| PHONE | other | 3.9K | 290 | (801) 359-4699 158; (314) 997-2100 94; (801) 561-3473 61; (888) 805-5142 24 |
| EMPRANGE | category | 9 | 0 |  1-4 3.1K; 0 1.2K;  5-9 362;  10-19 188 |
| EMPRANGECODE | category | 9 | 0 | B 3.1K; A 1.2K; C 362; D 188 |
| NAICS | who | 540 | 0 | 425120 342; 814110 218; 541511 170; 541611 140 |
| OWNERSHIP | category | 4 | 0 | Private 5.0K; Federal 8; State 2; Local 2 |
| LOCATION_1 | category | 2 | 5.0K | {"human_address": "{\"add 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:46:37.40025 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | cd25ba87-a00c-400f-b3dd-0 5.0K |
| SRC_SHA256 | who | 1 | 0 | 428e7f10ee1b60381edc36a74 5.0K |
