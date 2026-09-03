# PORTAL_CKA_INDIANA_DATA_HUB_FE00D42ACC

rows 10.0K  columns 13  scan 3.9s

roles: audit 2, category 1, date 3, other 6, who 2

## when

DATE
  2020      1.4K  #####
  2021      8.6K  ##############################

CURRENT_AS_OF
  2023     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## who

COUNTY by rows
       111  Hamilton
       111  Out of State
       111  Allen
       111  Marion
       110  Madison
       110  La Porte
       110  Johnson
       110  Lake
       110  Howard
       110  Hendricks
       110  Boone
       110  Clark
       110  Harrison
       110  Jefferson
       109  Spencer
       109  Floyd
       109  Pike
       109  Vanderburgh
       109  Shelby
       109  Dearborn

SRC_SHA256 by rows
     10.0K  4e962348ff757dd4b3a27eb3c55b82ca19be22b72e1225c8a247da31faafe8ef

## who x when

COUNTY by DATE
  Allen                                     2020:18 2021:93
  Boone                                     2020:17 2021:93
  Clark                                     2020:17 2021:93
  Dearborn                                  2020:16 2021:93
  Floyd                                     2020:16 2021:93
  Hamilton                                  2020:18 2021:93
  Harrison                                  2020:17 2021:93
  Hendricks                                 2020:17 2021:93
  Howard                                    2020:17 2021:93
  Jefferson                                 2020:17 2021:93
  Johnson                                   2020:17 2021:93
  La Porte                                  2020:17 2021:93
  Lake                                      2020:17 2021:93
  Madison                                   2020:17 2021:93
  Marion                                    2020:18 2021:93
  Out of State                              2020:18 2021:93
  Pike                                      2020:16 2021:93
  Shelby                                    2020:16 2021:93
  Spencer                                   2020:16 2021:93
  Vanderburgh                               2020:17 2021:92

SRC_SHA256 by DATE
  4e962348ff757dd4b3a27eb3c55b82ca19be22b7  2020:1.4K 2021:8.6K

## what

REGION: 6 14%, 10 13%, 9 13%, 3 12%, 4 9%, 5 9%, 7 8%, 8 8%, 2 7%, 1 5%, Out of State 1%, Unknown 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATE | date | 112 | 0 | 2021-04-02T00:00:00 94; 2021-04-01T00:00:00 94; 2021-03-31T00:00:00 94; 2021-03-30T00:00:00 94 |
| COUNTY | who | 94 | 0 | Out of State 111; Marion 111; Hamilton 111; Allen 111 |
| REGION | category | 12 | 0 | 6 1.4K; 10 1.3K; 9 1.3K; 3 1.2K |
| FIPS | other | 94 | 0 | Out of State 111; 18097 111; 18057 111; 18003 111 |
| SINGLE_DOSE_ADMINISTERED | other | 239 | 0 | 0 7.4K; 1 433; 2 215; 3 170 |
| ALL_DOSES_ADMINISTERED | other | 1.5K | 0 | 1 231; 2 180; 3 151; 4 126 |
| FULLY_VACCINATED | other | 914 | 0 | 0 1.6K; 1 435; 2 257; 3 220 |
| BOOSTER_DOSE_ADMINISTERED | other | 1 | 0 | 0 10.0K |
| SECOND_BOOSTER_DOSE_ADMINISTERED | other | 1 | 0 | 0 10.0K |
| CURRENT_AS_OF | date | 1 | 0 | 2023-05-10T05:00:00 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:03:42.25167 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 13ab7f24-5f17-4bb6-b7ca-5 10.0K |
| SRC_SHA256 | who | 1 | 0 | 4e962348ff757dd4b3a27eb3c 10.0K |
