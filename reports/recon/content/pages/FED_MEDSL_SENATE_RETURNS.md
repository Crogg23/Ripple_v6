# FED_MEDSL_SENATE_RETURNS

rows 3.9K  columns 22  scan 3.0s

roles: amount 2, audit 2, category 11, state 1, who 6

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| STATE_CEN | 3.9K | 11 | 54 | 95 | 95 | 210.4K |
| TOTALVOTES | 3.9K | 1 | 1.58M | 10.77M | 15.35M | 9.01B |

## who

PARTY_DETAILED by rows
       871  REPUBLICAN
       840  DEMOCRAT
       393  LIBERTARIAN
       301  INDEPENDENT
        98  GREEN
        65  SOCIALIST WORKERS
        55  OTHER
        47  NATURAL LAW
        42  CONSTITUTION
        36  REFORM
        27  NONE
        26  CONSERVATIVE
        24  AMERICAN
        23  DEMOCRATIC
        16  WORKING FAMILIES
        16  INDEPENDENCE
        16  INDEPENDENT AMERICAN
        13  NO PARTY AFFILIATION
        13  UNAFFILIATED
        13  AMERICAN INDEPENDENT

PARTY_DETAILED by dollars
       1.75B      871 rows  REPUBLICAN
       1.71B      840 rows  DEMOCRAT
     928.55M      393 rows  LIBERTARIAN
     518.29M      301 rows  INDEPENDENT
     311.99M       98 rows  GREEN
     186.02M       65 rows  SOCIALIST WORKERS
     137.28M       55 rows  OTHER
     123.84M       47 rows  NATURAL LAW
     116.60M       26 rows  CONSERVATIVE
     109.75M       12 rows  PEACE AND FREEDOM
     108.80M       27 rows  NONE
     101.25M       13 rows  AMERICAN INDEPENDENT
      89.71M       42 rows  CONSTITUTION
      85.86M       36 rows  REFORM
      73.59M       23 rows  DEMOCRATIC
      72.96M       13 rows  NO PARTY AFFILIATION
      63.91M       16 rows  INDEPENDENCE
      59.97M       16 rows  WORKING FAMILIES
      52.53M        9 rows  LIBERAL
      45.87M        8 rows  RIGHT TO LIFE

OFFICE by rows
      3.9K  US SENATE

OFFICE by dollars
       9.01B     3.9K rows  US SENATE

DISTRICT by rows
      3.9K  statewide

DISTRICT by dollars
       9.01B     3.9K rows  statewide

CANDIDATEVOTES by rows
        16  1.0
        13  7.0
        11  10.0
        11  5.0
        10  12.0
         9  4.0
         8  18.0
         8  9.0
         7  2.0
         7  6.0
         7  14.0
         7  13.0
         6  15.0
         6  21.0
         6  23.0
         6  42.0
         6  19.0
         5  8.0
         5  3.0
         5  17.0

CANDIDATEVOTES by dollars
      39.58M       13 rows  7.0
      37.04M       11 rows  10.0
      34.32M        7 rows  2.0
      34.19M       11 rows  5.0
      31.00M       16 rows  1.0
      30.14M        9 rows  4.0
      29.68M       10 rows  12.0
      29.48M        8 rows  18.0
      26.70M        7 rows  13.0
      25.59M        8 rows  9.0
      23.39M        6 rows  42.0
      23.15M        7 rows  6.0
      21.51M        6 rows  19.0
      17.61M        6 rows  23.0
      17.47M        4 rows  16.0
      17.18M        3 rows  56.0
      16.35M        3 rows  11.0
      16.29M        3 rows  53.0
      15.35M        1 rows  6312594.0
      15.35M        1 rows  9036252.0

## where

STATE_PO: NY 161, TN 144, NJ 129, MN 120, VT 119, LA 116, MI 110, AZ 107, IL 104, FL 102, CO 102, CA 96

## what

YEAR: 2010 11%, 2016 10%, 2020 9%, 2012 9%, 2014 9%, 2000 8%, 2022 8%, 2004 8%, 1992 8%, 2006 7%, 1994 7%, 1996 7%

STATE: NEW YORK 11%, TENNESSEE 10%, NEW JERSEY 9%, MINNESOTA 9%, VERMONT 8%, LOUISIANA 8%, MICHIGAN 8%, ARIZONA 8%, ILLINOIS 7%, FLORIDA 7%, COLORADO 7%, CALIFORNIA 7%

STATE_FIPS: 36 11%, 47 10%, 34 9%, 27 9%, 50 8%, 22 8%, 26 8%, 4 8%, 17 7%, 12 7%, 8 7%, 6 7%

STATE_IC: 13 11%, 54 10%, 12 9%, 33 9%, 6 8%, 45 8%, 23 8%, 61 8%, 21 7%, 43 7%, 62 7%, 71 7%

STAGE: gen 92%, GEN 8%, pre 0%, runoff 0%, GEN RUNOFF 0%

SPECIAL: False 96%, True 4%

WRITEIN: False 88%, True 12%

MODE: total 92%, TOTAL 8%

UNOFFICIAL: False 99%, True 1%

VERSION: 20210114 92%, 20230920 4%, 11/20/25 4%, 20241212 0%

PARTY_SIMPLIFIED: OTHER 46%, DEMOCRAT 22%, REPUBLICAN 22%, LIBERTARIAN 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 26 | 0 | 2010 242; 2016 221; 2020 204; 2012 190 |
| STATE | category | 50 | 0 | NEW YORK 161; TENNESSEE 144; NEW JERSEY 129; MINNESOTA 120 |
| STATE_PO | state | 50 | 0 | NY 161; TN 144; NJ 129; MN 120 |
| STATE_FIPS | category | 50 | 0 | 36 161; 47 144; 34 129; 27 120 |
| STATE_CEN | amount | 48 | 0 | 21.0 161; 62.0 144; 22.0 129; 41.0 120 |
| STATE_IC | category | 49 | 0 | 13 161; 54 144; 12 129; 33 120 |
| OFFICE | who | 1 | 0 | US SENATE 3.9K |
| DISTRICT | who | 1 | 0 | statewide 3.9K |
| STAGE | category | 5 | 0 | gen 3.6K; GEN 314; pre 9; runoff 4 |
| SPECIAL | category | 2 | 0 | False 3.8K; True 157 |
| CANDIDATE | who | 2.5K | 423 | OTHER 92; SCATTER 26; BLANK VOTE/SCATTERING 24; UNDERVOTES 21 |
| PARTY_DETAILED | who | 198 | 627 | REPUBLICAN 871; DEMOCRAT 840; LIBERTARIAN 393; INDEPENDENT 301 |
| WRITEIN | category | 2 | 0 | False 3.5K; True 472 |
| MODE | category | 2 | 0 | total 3.6K; TOTAL 316 |
| CANDIDATEVOTES | who | 3.7K | 0 | 7.0 23; 5.0 21; 1.0 21; 6860.0 20 |
| TOTALVOTES | amount | 868 | 0 | 1997218.0 36; 4914361.0 34; 3355307.0 33; 2321477.0 30 |
| UNOFFICIAL | category | 2 | 0 | False 3.9K; True 21 |
| VERSION | category | 4 | 0 | 20210114 3.6K; 20230920 168; 11/20/25 144; 20241212 4 |
| PARTY_SIMPLIFIED | category | 5 | 2 | OTHER 1.8K; DEMOCRAT 878; REPUBLICAN 875; LIBERTARIAN 394 |
| _INGESTED_AT | audit | 1 | 0 | 1782860760239423 3.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 2fc18271-ca46-4a9f-b7f4-e 3.9K |
| _SRC_SHA256 | who | 1 | 0 | 9ffe9ea7258e1d23f8eddd5a8 3.9K |
