# PORTAL_CKA_INDIANA_DATA_HUB_4F4EC0066B

rows 306  columns 13  scan 3.4s

roles: amount 3, audit 2, category 2, date 1, other 4, who 2

## when

INGESTED_AT
  2026       306  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| COVID_TEST_PCT | 306 | 0.36 | 38.35 | 78.39 | 84.01 | 10.2K |
| COVID_COUNT_PCT | 306 | 0.44 | 21.64 | 87.80 | 90.87 | 10.2K |
| COVID_DEATHS_PCT | 306 | 0 | 24.27 | 91.74 | 92.22 | 10.2K |

## who

COUNTY_NAME by rows
         3  Vanderburgh
         3  Carroll
         3  Porter
         3  Wells
         3  Vigo
         3  Brown
         3  Clinton
         3  Jennings
         3  Fulton
         3  Knox
         3  Ohio
         3  Miami
         3  Hamilton
         3  Shelby
         3  Decatur
         3  Adams
         3  Noble
         3  Montgomery
         3  Gibson
         3  Franklin

COUNTY_NAME by dollars
      100.01        3 rows  Noble
      100.01        3 rows  Orange
      100.01        3 rows  Randolph
      100.01        3 rows  Jackson
      100.01        3 rows  Shelby
      100.01        3 rows  Monroe
      100.01        3 rows  Scott
      100.01        3 rows  Benton
      100.01        3 rows  Hendricks
      100.01        3 rows  Jefferson
         100        3 rows  Fayette
         100        3 rows  Marion
         100        3 rows  Porter
         100        3 rows  Cass
         100        3 rows  Allen
         100        3 rows  Howard
         100        3 rows  Brown
         100        3 rows  Dearborn
         100        3 rows  Lake
         100        3 rows  Adams

SRC_SHA256 by rows
       306  1166a946e77bb28decc76125e94fa16248cdb0ad566ea3d4d34acb6d53e4728f

SRC_SHA256 by dollars
       10.2K      306 rows  1166a946e77bb28decc76125e94fa16248cdb0ad566ea3d4d34acb6d53e4

## who x when

COUNTY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = COVID_TEST_PCT
  Adams                                     2026:100
  Benton                                    2026:100.01
  Brown                                     2026:100
  Carroll                                   2026:100
  Clinton                                   2026:100
  Decatur                                   2026:100
  Fayette                                   2026:100
  Franklin                                  2026:100
  Fulton                                    2026:99.99
  Gibson                                    2026:100
  Hamilton                                  2026:99.99
  Hendricks                                 2026:100.01
  Jackson                                   2026:100.01
  Jefferson                                 2026:100.01
  Jennings                                  2026:100
  Knox                                      2026:100
  Marion                                    2026:100
  Miami                                     2026:100
  Monroe                                    2026:100.01
  Montgomery                                2026:99.99
  Noble                                     2026:100.01
  Ohio                                      2026:100
  Orange                                    2026:100.01
  Porter                                    2026:100
  Randolph                                  2026:100.01
  Scott                                     2026:100.01
  Shelby                                    2026:100.01
  Vanderburgh                               2026:100
  Vigo                                      2026:100
  Wells                                     2026:99.99

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = COVID_TEST_PCT
  1166a946e77bb28decc76125e94fa16248cdb0ad  2026:10.2K

## what

LOCATION_LEVEL: c 90%, d 10%

ETHNICITY: Unknown 33%, Not Hispanic or Latino 33%, Hispanic or Latino 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_LEVEL | category | 2 | 0 | c 276; d 30 |
| LOCATION_ID | other | 102 | 0 | 9 3; 8 3; 7 3; 6 3 |
| ETHNICITY | category | 3 | 0 | Unknown 102; Not Hispanic or Latino 102; Hispanic or Latino 102 |
| COVID_TEST | other | 300 | 0 | 523 3; 146198 2; 209485 2; 7232 2 |
| COVID_COUNT | other | 294 | 0 | 19 3; 33897 2; 114889 2; 3555 2 |
| COVID_DEATHS | other | 157 | 0 | 0 29; 1 17; 2 17; 6 7 |
| COVID_TEST_PCT | amount | 294 | 0 | 1.01 4; 2.02 3; 40.28 2; 57.72 2 |
| COVID_COUNT_PCT | amount | 296 | 0 | 1.43 3; 22.25 2; 75.42 2; 2.33 2 |
| COVID_DEATHS_PCT | amount | 263 | 0 | 0.0 29; 24.8 3; 1.19 3; 24.99 2 |
| COUNTY_NAME | who | 93 | 30 | Whitley 3; White 3; Wells 3; Wayne 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:18:35.23032 306 |
| SOURCE_RUN_ID | audit | 1 | 0 | bc2dbac8-3c02-4c1b-a4e7-d 306 |
| SRC_SHA256 | who | 1 | 0 | 1166a946e77bb28decc76125e 306 |
