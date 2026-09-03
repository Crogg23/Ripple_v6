# PORTAL_CKA_INDIANA_DATA_HUB_0ED686ABD6

rows 10.0K  columns 13  scan 3.5s

roles: amount 2, audit 2, category 5, date 1, other 2, who 2

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| STUDENT_WAGE_CNT | 8.9K | 10 | 83 | 1.8K | 60.3K | 5.40M |
| MEDIAN_WAGE | 7.7K | 15.7K | 32.7K | 56.3K | 81.4K | 261.80M |

## who

CORPORATION_NAME by rows
        75  Central Noble Com School Corp
        75  Griffith Public Schools
        75  Center Grove Community School Corp
        75  Benton Community School Corp
        75  Crawfordsville Community Schools
        75  Culver Community Schools Corp
        75  Greater Jasper Consolidated Schs
        75  East Gibson School Corporation
        75  Delphi Community School Corp
        75  Attica Consolidated School Corp
        75  Bloomfield School District
        75  Columbus Christian School Inc
        75  Bethesda Christian School
        75  Bethany Christian School
        75  Fremont Community Schools
        75  21st Century Charter Sch of Gary
        75  Batesville Community School Corp
        75  Barr-Reeve Community Schools Inc
        75  Anderson Community School Corp
        75  Eastern Greene Schools

CORPORATION_NAME by dollars
       3.95M       75 rows  All School Corporations
      106.8K       75 rows  Fort Wayne Community Schools
       82.6K       75 rows  Charter Schools
       78.0K       75 rows  Evansville Vanderburgh School Corp
       65.1K       75 rows  Archdiocese of Indianapolis
       49.8K       75 rows  Carmel Clay Schools
       43.9K       75 rows  East Allen County Schools
       42.3K       75 rows  Bartholomew Con School Corp
       40.5K       75 rows  Elkhart Community Schools
       37.8K       75 rows  Diocese of Fort Wayne - South Bend
       35.7K       75 rows  Avon Community School Corp
       33.7K       75 rows  Greater Clark County Schools
       32.7K       75 rows  Franklin Township Com Sch Corp
       31.9K       75 rows  Crown Point Community School Corp
       31.0K       75 rows  Brownsburg Community School Corp
       29.9K       75 rows  Center Grove Community School Corp
       23.1K       75 rows  Duneland School Corporation
       22.6K       75 rows  Clark-Pleasant Community Sch Corp
       22.5K       75 rows  Anderson Community School Corp
       21.9K       75 rows  Goshen Community Schools

SRC_SHA256 by rows
     10.0K  41eabf2a6ac6de036f6e11e38509913c40d5fcd2bd84398195432ad164fca008

SRC_SHA256 by dollars
       5.40M    10.0K rows  41eabf2a6ac6de036f6e11e38509913c40d5fcd2bd84398195432ad164fc

## who x when

CORPORATION_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = STUDENT_WAGE_CNT
  21st Century Charter Sch of Gary          2026:1.6K
  All School Corporations                   2026:3.95M
  Anderson Community School Corp            2026:22.5K
  Archdiocese of Indianapolis               2026:65.1K
  Attica Consolidated School Corp           2026:3.5K
  Barr-Reeve Community Schools Inc          2026:3.0K
  Bartholomew Con School Corp               2026:42.3K
  Batesville Community School Corp          2026:8.6K
  Benton Community School Corp              2026:7.5K
  Bethany Christian School                  2026:1.6K
  Bethesda Christian School                 2026:1.2K
  Bloomfield School District                2026:3.7K
  Carmel Clay Schools                       2026:49.8K
  Center Grove Community School Corp        2026:29.9K
  Central Noble Com School Corp             2026:5.8K
  Charter Schools                           2026:82.6K
  Columbus Christian School Inc             2026:140
  Crawfordsville Community Schools          2026:9.0K
  Culver Community Schools Corp             2026:3.3K
  Delphi Community School Corp              2026:6.6K
  Diocese of Fort Wayne - South Bend        2026:37.8K
  East Allen County Schools                 2026:43.9K
  East Gibson School Corporation            2026:3.6K
  Eastern Greene Schools                    2026:5.1K
  Elkhart Community Schools                 2026:40.5K
  Evansville Vanderburgh School Corp        2026:78.0K
  Fort Wayne Community Schools              2026:106.8K
  Fremont Community Schools                 2026:4.7K
  Greater Jasper Consolidated Schs          2026:14.0K
  Griffith Public Schools                   2026:9.8K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = STUDENT_WAGE_CNT
  41eabf2a6ac6de036f6e11e38509913c40d5fcd2  2026:5.40M

## what

CORPORATION_TYPE: Public School Corporations 65%, Non-Public Schools 20%, Charter Schools 13%, Turn-around Corporation 2%, All School Types 1%

GRADUATION_SCHOOL_YR: 2012 12%, 2013 12%, 2011 12%, 2010 12%, 2014 11%, 2015 10%, 2016 9%, 2017 7%, 2018 6%, 2019 5%, 2020 3%, 2021 2%

GRADUATION_SCHOOL_YR_DESC: 2011-2012 12%, 2012-2013 12%, 2010-2011 12%, 2009-2010 12%, 2013-2014 11%, 2014-2015 10%, 2015-2016 9%, 2016-2017 7%, 2017-2018 6%, 2018-2019 5%, 2019-2020 3%, 2020-2021 2%

RELATIVE_YR: 1 17%, 2 15%, 3 14%, 4 12%, 5 11%, 6 9%, 7 8%, 8 6%, 9 5%, 10 4%

RELATIVE_YR_DESC: 1 Year After Expected Graduati 17%, 2 Years After Expected Graduat 15%, 3 Years After Expected Graduat 14%, 4 Years After Expected Graduat 12%, 5 Years After Expected Graduat 11%, 6 Years After Expected Graduat 9%, 7 Years After Expected Graduat 8%, 8 Years After Expected Graduat 6%, 9 Years After Expected Graduat 5%, 10 Years After Expected Gradua 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CORPORATION_NAME | who | 175 | 0 | Hamilton Community School 75; Griffith Public Schools 75; Greenwood Community Sch C 75; Greenwood Christian Acade 75 |
| CORPORATION_TYPE | category | 5 | 0 | Public School Corporation 6.5K; Non-Public Schools 2.0K; Charter Schools 1.3K; Turn-around Corporation 152 |
| GRADUATION_SCHOOL_YR | category | 12 | 0 | 2012 1.2K; 2013 1.2K; 2011 1.2K; 2010 1.2K |
| GRADUATION_SCHOOL_YR_DESC | category | 12 | 0 | 2011-2012 1.2K; 2012-2013 1.2K; 2010-2011 1.2K; 2009-2010 1.2K |
| RELATIVE_YR | category | 10 | 0 | 1 1.7K; 2 1.5K; 3 1.4K; 4 1.2K |
| RELATIVE_YR_DESC | category | 10 | 0 | 1 Year After Expected Gra 1.7K; 2 Years After Expected Gr 1.5K; 3 Years After Expected Gr 1.4K; 4 Years After Expected Gr 1.2K |
| GRADUATE_CNT | other | 494 | 0 | Suppressed 755; 56 114; 37 103; 11 96 |
| STUDENT_WAGE_CNT | amount | 945 | 0 | Suppressed 1.1K; 10 115; 11 104; 25 89 |
| STUDENT_3_QTR_NO_ENRL_FED_MIN_WAGE_CNT | other | 608 | 0 | Suppressed 2.3K; 10 147; 13 139; 14 139 |
| MEDIAN_WAGE | amount | 6.8K | 0 | Suppressed 2.3K; 40306 39; 30524 39; 33238 39 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:45:23.42269 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6de354d7-c786-428f-9e48-e 10.0K |
| SRC_SHA256 | who | 1 | 0 | 41eabf2a6ac6de036f6e11e38 10.0K |
