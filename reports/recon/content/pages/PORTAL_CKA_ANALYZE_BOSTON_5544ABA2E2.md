# PORTAL_CKA_ANALYZE_BOSTON_5544ABA2E2

rows 391  columns 20  scan 3.6s

roles: amount 13, audit 2, category 3, date 2, who 1

## when

SCORE_CALCULATED_TS
  2026       391  ##############################

INGESTED_AT
  2026       391  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TARGET | 289 | 0.80 | 0.80 | 6 | 6 | 438.60 |
| DAY_SCORE | 145 | 0 | 1.25 | 1.87 | 1.97 | 156.43 |
| DAY_NUMERATOR | 243 | 0 | 6 | 21.1K | 23.5K | 109.3K |
| DAY_DENOMINATOR | 158 | 1 | 18 | 12.0K | 12.1K | 219.6K |
| WEEK_SCORE | 310 | 0.10 | 1.09 | 2.55 | 4.33 | 334.84 |
| WEEK_NUMERATOR | 323 | 0.04 | 39 | 21.5K | 21.5K | 491.6K |

## who

SRC_SHA256 by rows
       391  3801dfe8b9f8658e5e497ec7054868f484a871f2e0a726c9a13a28b3c248e4b4

SRC_SHA256 by dollars
      491.6K      391 rows  3801dfe8b9f8658e5e497ec7054868f484a871f2e0a726c9a13a28b3c248

## who x when

SRC_SHA256 by SCORE_CALCULATED_TS, dollars = WEEK_NUMERATOR
  3801dfe8b9f8658e5e497ec7054868f484a871f2  2026:491.6K

## what

METRIC_NAME: CITY SERVICES SATISFACTION SUR 8%, ON-TIME PERMIT REVIEWS 8%, CODE ENFORCEMENT TRASH COLLECT 8%, CODE ENFORCEMENT ON-TIME % 8%, TREE MAINTENANCE ON-TIME % 8%, PARKS MAINTENANCE ON-TIME % 8%, SIGN INSTALLATION ON-TIME % 8%, SIGNAL REPAIR ON-TIME % 8%, STREETLIGHT ON-TIME % 8%, MISSED TRASH ON-TIME % 8%, POTHOLE ON-TIME % 8%, GRAFFITI ON-TIME % 8%

METRIC_LOGIC: sum(numerator_value)/sum(denom 65%, historical_average / current_a 22%, current_average / historical_a 4%, target / median 4%, average(sum(numerator_value)/s 4%

LATEST_SCORE_FLAG: 0 94%, 1 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| METRIC_NAME | category | 23 | 0 | CITY SERVICES SATISFACTIO 17; ON-TIME PERMIT REVIEWS 17; CODE ENFORCEMENT TRASH CO 17; CODE ENFORCEMENT ON-TIME  17 |
| SCORE_CALCULATED_TS | date | 125 | 0 | 2026-06-18T09:13:14 7; 2026-06-18T09:13:13 7; 2026-06-11T08:40:45 7; 2026-04-10T10:58:09 7 |
| TARGET | amount | 7 | 102 | 0.8 170; 4.0 34; 0.95 34; 1.0 17 |
| METRIC_LOGIC | category | 5 | 0 | sum(numerator_value)/sum( 255; historical_average / curr 85; current_average / histori 17; target / median 17 |
| DAY_SCORE | amount | 65 | 246 | 1.25 73; 0.75 5; 0.833333333333333 3; 0.416666666666667 3 |
| DAY_NUMERATOR | amount | 95 | 148 | 6.0 22; 5.0 13; 1.0 13; 4.0 9 |
| DAY_DENOMINATOR | amount | 73 | 233 | 1.0 21; 3.0 11; 5.0 9; 4.0 7 |
| WEEK_SCORE | amount | 146 | 81 | 1.25 36; 1.21794871794872 7; 1.125 7; 1.22619047619048 6 |
| WEEK_NUMERATOR | amount | 122 | 68 | 6.0 19; 18.0 11; 23.0 9; 0.119047619047619 8 |
| WEEK_DENOMINATOR | amount | 133 | 81 | 4.0 12; 2.0 9; 78.0 7; 46.0 7 |
| MONTH_SCORE | amount | 95 | 69 | 0.793859649122807 12; 1.22743682310469 12; 1.24326923076923 12; 0.226683937823834 12 |
| MONTH_NUMERATOR | amount | 77 | 68 | 6.0 17; 181.0 12; 1360.0 12; 1293.0 12 |
| MONTH_DENOMINATOR | amount | 93 | 69 | 57.0 12; 1385.0 12; 1300.0 12; 386.0 12 |
| QUARTER_SCORE | amount | 99 | 68 | 0.800955414012739 12; 1.19003572339883 12; 1.22339803554724 12; 0.218275488069414 12 |
| QUARTER_NUMERATOR | amount | 79 | 68 | 6.0 17; 503.0 12; 3731.0 12; 4185.0 12 |
| QUARTER_DENOMINATOR | amount | 97 | 68 | 157.0 12; 3919.0 12; 4276.0 12; 922.0 12 |
| LATEST_SCORE_FLAG | category | 2 | 0 | 0 368; 1 23 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:20:04.79202 391 |
| SOURCE_RUN_ID | audit | 1 | 0 | a33281c9-85ca-4b77-8640-a 391 |
| SRC_SHA256 | who | 1 | 0 | 3801dfe8b9f8658e5e497ec70 391 |
