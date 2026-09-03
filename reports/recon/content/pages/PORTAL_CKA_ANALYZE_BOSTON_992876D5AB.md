# PORTAL_CKA_ANALYZE_BOSTON_992876D5AB

rows 275  columns 16  scan 3.3s

roles: amount 4, audit 2, category 5, date 1, empty 1, other 3, who 1

## when

INGESTED_AT
  2026       275  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CONGRESS_2 | 275 | 7 | 7 | 8 | 8 | 2.0K |
| SHAPE_LENG | 275 | 1.1K | 4.0K | 14.5K | 84.3K | 1.31M |
| SHAPE_LENGTH | 275 | 0.01 | 0.03 | 0.12 | 0.70 | 10.29 |
| SHAPE_AREA | 275 | 0 | 0 | 0 | 0.01 | 0.01 |

## who

SRC_SHA256 by rows
       275  049f1914a93f2fc070f965e0573ce3559390a7b5b5abc9c7de4682c82779a66f

SRC_SHA256 by dollars
        2.0K      275 rows  049f1914a93f2fc070f965e0573ce3559390a7b5b5abc9c7de4682c82779

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CONGRESS_2
  049f1914a93f2fc070f965e0573ce3559390a7b5  2026:2.0K

## what

WARD1: 18 12%, 20 11%, 03 9%, 21 9%, 05 8%, 01 8%, 17 8%, 14 8%, 22 7%, 19 7%, 16 6%, 06 6%

PRECINCT1: 06 9%, 05 9%, 04 9%, 03 9%, 02 9%, 01 9%, 07 9%, 08 9%, 09 8%, 10 7%, 12 6%, 11 6%

GOV_COUN_2: 4th 71%, 6th 16%, 3rd 13%

REP_2022: 10th 10%, 6th 9%, 4th 9%, 14th 9%, 15th 9%, 13th 9%, 5th 9%, 8th 8%, 7th 8%, 9th 8%, 12th 7%, 3rd 7%

SENATE_202: 1st 30%, 2nd 27%, N & S 14%, 3rd 13%, S & M 13%, M & S 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DISTRICT | other | 276 | 0 | 22-13 2; 22-12 2; 22-11 2; 22-10 2 |
| WDPCT | other | 274 | 0 | 2213 2; 2212 2; 2211 2; 2210 2 |
| WARD1 | category | 22 | 0 | 18 23; 20 21; 03 17; 21 16 |
| PRECINCT1 | category | 23 | 0 | 06 22; 05 22; 04 22; 03 22 |
| STATE_WDPC | other | 262 | 16 | 22-13 2; 22-12 2; 22-11 2; 22-10 2 |
| GOV_COUN_2 | category | 3 | 0 | 4th 195; 6th 45; 3rd 35 |
| REP_2022 | category | 16 | 0 | 10th 22; 6th 20; 4th 20; 14th 19 |
| SENATE_202 | category | 6 | 0 | 1st 83; 2nd 73; N & S 39; 3rd 37 |
| CONGRESS_2 | amount | 2 | 0 | 7.000000000000000 189; 8.000000000000000 86 |
| SHAPE_LENG | amount | 274 | 0 | 2956.116114479999851 2; 6748.660295030000270 2; 5275.352237050000440 2; 4868.586904339999819 2 |
| SHAPE_LENGTH | amount | 277 | 0 | 0.022779650317153 2; 0.054318688785447 2; 0.043164494970648 2; 0.037677301809330 2 |
| SHAPE_AREA | amount | 280 | 0 | 0.000028493714128 2; 0.000070362184173 2; 0.000052565203010 2; 0.000044595472288 2 |
| SHAPE_WKT | empty | 1 | 275 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:11.60658 275 |
| SOURCE_RUN_ID | audit | 1 | 0 | 221ff646-0ee0-4749-b9e3-b 275 |
| SRC_SHA256 | who | 1 | 0 | 049f1914a93f2fc070f965e05 275 |
