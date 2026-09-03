# PORTAL_SOC_UTAH_OPEN_DATA_P_0F31165E86

rows 2.0K  columns 13  scan 3.2s

roles: audit 2, category 3, date 1, other 2, who 6

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

NAME by rows
        12  AMERICA FIRST CREDIT UNION
        12  7-ELEVEN
         6  AUTOZONE
         5  ARBYS
         4  AT T MOBILITY SERVICES LLC
         4  ASSOCIATED FRESH MARKETS, INC.
         3  ALCATEL-LUCENT USA INC
         3  AMERICAN UNITED FCU
         3  ALLSTATE
         2  AT T SERVICES  INC
         2  KINDER CARE LEARNING CTRS
         2  AMERICAN PREPARATORY ACADEMY
         2  ANN TAYLOR RETAIL INC
         2  AMERICAN TRAVELERS STAFFING PROFESS
         2  3M CO
         2  ASSET APPRAISAL SERVICES INC
         2  AM ACCESS FLOORS
         2  AFTER HOURS MEDICAL COMPANY
         2  APPLE CONTACT LENS CENTER INC
         2  ABIGAIL LEYVA

COUNTYNAME by rows
      2.0K  Salt Lake

LOCATION_1 by rows
       909  nan
         4  {"latitude": "40.769332920000465", "longitude": "-111.88707028799968",
         2  {"latitude": "40.56162613100048", "longitude": "-111.92480437999967", 
         2  {"latitude": "40.6361647920005", "longitude": "-111.8892152299997", "h
         2  {"latitude": "40.68704076400047", "longitude": "-111.85675983399972", 
         2  {"latitude": "40.68702773400048", "longitude": "-111.89270033599968", 
         1  {"latitude": "40.62497274900045", "longitude": "-111.84239286399969", 
         1  {"latitude": "40.715375019000476", "longitude": "-111.90259497999972",
         1  {"latitude": "40.6998929610005", "longitude": "-111.89931212899967", "
         1  {"latitude": "40.48698841200047", "longitude": "-111.91339348699967", 
         1  {"latitude": "40.6286542900005", "longitude": "-111.85195565199967", "
         1  {"latitude": "40.6855707470005", "longitude": "-111.86555348199971", "
         1  {"latitude": "40.71268789800047", "longitude": "-111.87668016199967", 
         1  {"latitude": "40.71064259700046", "longitude": "-111.83044024599968", 
         1  {"latitude": "40.51666306700048", "longitude": "-111.89168922999971", 
         1  {"latitude": "40.77164785400049", "longitude": "-111.9289119449997", "
         1  {"latitude": "40.550284959000464", "longitude": "-111.89084149699971",
         1  {"latitude": "40.765047584000456", "longitude": "-111.88367105699967",
         1  {"latitude": "40.71097099800045", "longitude": "-111.9771971619997", "
         1  {"latitude": "40.72138071100045", "longitude": "-111.85368637899967", 

NAICS by rows
        87  425120
        57  541511
        50  541611
        36  561320
        32  624120
        31  814110
        31  524210
        29  531210
        27  541330
        27  541110
        25  561730
        24  447110
        24  722513
        23  541519
        22  621111
        22  423450
        20  238221
        20  541512
        17  561330
        17  541690

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  3M CO                                     2026:2
  7-ELEVEN                                  2026:12
  ABIGAIL LEYVA                             2026:2
  AFTER HOURS MEDICAL COMPANY               2026:2
  ALCATEL-LUCENT USA INC                    2026:3
  ALLSTATE                                  2026:3
  AM ACCESS FLOORS                          2026:2
  AMERICA FIRST CREDIT UNION                2026:12
  AMERICAN PREPARATORY ACADEMY              2026:2
  AMERICAN TRAVELERS STAFFING PROFESS       2026:2
  AMERICAN UNITED FCU                       2026:3
  ANN TAYLOR RETAIL INC                     2026:2
  APPLE CONTACT LENS CENTER INC             2026:2
  ARBYS                                     2026:5
  ASSET APPRAISAL SERVICES INC              2026:2
  ASSOCIATED FRESH MARKETS, INC.            2026:4
  AT T MOBILITY SERVICES LLC                2026:4
  AT T SERVICES  INC                        2026:2
  AUTOZONE                                  2026:6
  KINDER CARE LEARNING CTRS                 2026:2

COUNTYNAME by INGESTED_AT  LOAD STAMP, not an event date
  Salt Lake                                 2026:2.0K

## what

EMPRANGE:  1-4 51%, 0 17%,  5-9 12%,  10-19 10%,  20-49 7%,  50-99 2%,  100-249 1%,  250-499 0%,  2000-2999 0%,  1000-1999 0%,  500-999 0%

EMPRANGECODE: B 51%, A 17%, C 12%, D 10%, E 7%, F 2%, G 1%, H 0%, K 0%, J 0%, I 0%

OWNERSHIP: Private 100%, Local 0%, State 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 1.9K | 0 | AMERICA FIRST CREDIT UNIO 17; AUTOZONE 15; AT T MOBILITY SERVICES LL 12; ASSOCIATED FRESH MARKETS, 12 |
| COUNTYCODE | other | 1 | 0 | 35 2.0K |
| COUNTYNAME | who | 1 | 0 | Salt Lake 2.0K |
| PHONE | other | 1.6K | 0 | nan 201; (801) 359-4699 29; (314) 997-2100 26; (801) 852-2673 10 |
| EMPRANGE | category | 11 | 0 |  1-4 1.0K; 0 340;  5-9 235;  10-19 191 |
| EMPRANGECODE | category | 11 | 0 | B 1.0K; A 340; C 235; D 191 |
| NAICS | who | 441 | 0 | 425120 87; 541511 57; 541611 50; 561320 36 |
| OWNERSHIP | category | 3 | 0 | Private 2.0K; Local 6; State 1 |
| LOCATION_1 | who | 1.1K | 0 | nan 909; {"latitude": "40.64922089 6; {"latitude": "40.47896942 6; {"latitude": "40.68314339 6 |
| LOCATION_2 | who | 102 | 0 | nan 1.9K; {"human_address": "{\"add 7; {"human_address": "{\"add 6; {"human_address": "{\"add 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:38.03533 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | fbad9977-fcec-46a0-abf3-6 2.0K |
| SRC_SHA256 | who | 1 | 0 | 5681bb7ea95ddbc15ba8080ad 2.0K |
