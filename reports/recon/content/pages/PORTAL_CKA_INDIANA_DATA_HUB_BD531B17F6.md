# PORTAL_CKA_INDIANA_DATA_HUB_BD531B17F6

rows 92  columns 15  scan 3.1s

roles: amount 4, audit 2, category 6, date 1, other 2, who 1

## when

INGESTED_AT
  2026        92  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POSITIVITY_RATE | 92 | 0 | 0.02 | 0.07 | 0.09 | 2.25 |
| COUNTY_SCORE | 92 | 0 | 0.50 | 1 | 1 | 35.50 |
| PREVIOUS_POSITIVITY | 92 | 0 | 0.03 | 0.08 | 0.08 | 2.94 |
| DIFFERENCE_IN_POSITIVITY | 92 | -0.06 | -0.01 | 0.03 | 0.05 | -0.72 |

## who

SRC_SHA256 by rows
        92  90de77b9a02828f92384d787796fe7c45173a7e3ce8e570eef0d5161818c57cc

SRC_SHA256 by dollars
        2.25       92 rows  90de77b9a02828f92384d787796fe7c45173a7e3ce8e570eef0d5161818c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = POSITIVITY_RATE
  90de77b9a02828f92384d787796fe7c45173a7e3  2026:2.25

## what

CASES: 2 21%, 3 20%, 8 8%, 5 8%, 1 8%, 4 8%, 6 7%, 7 7%, 12 5%, 9 5%, 10 3%

CASE_RATE: 14 15%, 8 10%, 10 10%, 17 10%, 19 10%, 20 8%, 9 8%, 6 8%, 15 6%, 16 6%, 13 6%

CASE_SCORE: 1 72%, 0 28%

POSITIVITY_SCORE: 0 95%, 1 5%

COUNTY_SCORE_COLOR: Blue (0 and 0.5) 95%, Yellow (1 and 1.5) 5%

ADVISORY_LEVEL: Blue 83%, Yellow 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTY | other | 92 | 0 | Whitley 1; White 1; Wells 1; Wayne 1 |
| FIPS | other | 92 | 0 | 18183 1; 18181 1; 18179 1; 18177 1 |
| CASES | category | 32 | 6 | 2 13; 3 12; 8 5; 5 5 |
| CASE_RATE | category | 34 | 6 | 14 7; 8 5; 10 5; 17 5 |
| CASE_SCORE | category | 2 | 0 | 1 66; 0 26 |
| POSITIVITY_RATE | amount | 80 | 0 | 0.0292 3; 0.0125 3; 0.0122 2; 0.0222 2 |
| POSITIVITY_SCORE | category | 2 | 0 | 0 87; 1 5 |
| COUNTY_SCORE | amount | 3 | 0 | 0.5 61; 0.0 26; 1.0 5 |
| COUNTY_SCORE_COLOR | category | 2 | 0 | Blue (0 and 0.5) 87; Yellow (1 and 1.5) 5 |
| ADVISORY_LEVEL | category | 2 | 0 | Blue 76; Yellow 16 |
| PREVIOUS_POSITIVITY | amount | 85 | 0 | 0.0 2; 0.0198 2; 0.0222 2; 0.0213 2 |
| DIFFERENCE_IN_POSITIVITY | amount | 85 | 0 | -0.009 2; 0.0122 2; -0.0093 2; 0.0053 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:31:25.30865 92 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4ba8dba0-6dca-47dc-9b8a-8 92 |
| SRC_SHA256 | who | 1 | 0 | 90de77b9a02828f92384d7877 92 |
