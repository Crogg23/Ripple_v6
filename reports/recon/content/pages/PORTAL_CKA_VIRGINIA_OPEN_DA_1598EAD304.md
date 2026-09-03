# PORTAL_CKA_VIRGINIA_OPEN_DA_1598EAD304

rows 10.0K  columns 19  scan 3.5s

roles: amount 3, audit 2, category 4, date 2, empty 1, other 6, who 2

## when

WEEK_ENDING_DATE
  2020      1.5K  #############################
  2021      1.6K  ##############################
  2022      1.6K  ##############################
  2023      1.6K  ##############################
  2024      1.5K  #############################
  2025      1.5K  ############################
  2026       723  ##############

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERCENT_OF_ED_VISITS_INFLUENZA | 9.9K | 0 | 0.30 | 15.06 | 33.50 | 16.7K |
| PERCENT_OF_ED_VISITS_RSV | 9.9K | 0 | 0 | 1.50 | 3.60 | 1.2K |
| PERCENT_OF_ED_VISITS_COMBINED | 9.9K | 0 | 2.80 | 20.00 | 39.30 | 41.4K |

## who

REPORT_DATE by rows
     10.0K  Jun 23 2026  9:00AM

REPORT_DATE by dollars
       16.7K    10.0K rows  Jun 23 2026  9:00AM

SRC_SHA256 by rows
     10.0K  3098037ce9c55983f9d0aecd7c0672096066a12fbac2f8182f91f09d3fe58a90

SRC_SHA256 by dollars
       16.7K    10.0K rows  3098037ce9c55983f9d0aecd7c0672096066a12fbac2f8182f91f09d3fe5

## who x when

REPORT_DATE by WEEK_ENDING_DATE, dollars = PERCENT_OF_ED_VISITS_INFLUENZA
  Jun 23 2026  9:00AM                       2020:2.4K 2021:337.40 2022:2.9K 2023:1.6K 2024:2.5K 2025:4.5K 2026:2.5K

SRC_SHA256 by WEEK_ENDING_DATE, dollars = PERCENT_OF_ED_VISITS_INFLUENZA
  3098037ce9c55983f9d0aecd7c0672096066a12f  2020:2.4K 2021:337.40 2022:2.9K 2023:1.6K 2024:2.5K 2025:4.5K 2026:2.5K

## what

HEALTH_REGION: Eastern Region 24%, Central Region 23%, Southwest Region 22%, Northern Region 14%, Northwest Region 14%, Out of State 2%

HEALTH_DISTRICT: Chesapeake 11%, Chickahominy 10%, Loudoun 10%, Northern Region 8%, Central Region 8%, Crater 8%, Lenowisco 8%, Chesterfield 8%, New River 8%, Rappahannock 7%, Lord Fairfax 7%, Fairfax 7%

FACILITY_TYPE: Emergency Department 51%, Urgent Care 49%

YEAR: 2023 16%, 2021 16%, 2020 16%, 2022 16%, 2024 15%, 2025 15%, 2026 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | who | 1 | 0 | Jun 23 2026  9:00AM 10.0K |
| WEEK_ENDING_DATE | date | 335 | 0 | 2022-05-14 53; 2020-11-28 52; 2022-10-08 52; 2021-10-02 52 |
| HEALTH_REGION | category | 6 | 0 | Eastern Region 2.4K; Central Region 2.3K; Southwest Region 2.2K; Northern Region 1.4K |
| HEALTH_DISTRICT | category | 40 | 0 | Chesapeake 452; Chickahominy 418; Loudoun 395; Northern Region 331 |
| FACILITY_TYPE | category | 2 | 0 | Emergency Department 5.1K; Urgent Care 4.9K |
| COUNTY_FIPS | empty | 1 | 10.0K |  |
| YEAR | category | 7 | 0 | 2023 1.6K; 2021 1.6K; 2020 1.6K; 2022 1.6K |
| WEEK | other | 53 | 0 | 20 230; 8 228; 13 226; 24 223 |
| PERCENT_OF_ED_VISITS_COVID | other | 204 | 0 | 0.0 862; 0.5 393; 0.4 374; 0.3 348 |
| PERCENT_OF_ED_VISITS_INFLUENZA | amount | 208 | 0 | 0.0 2.5K; 0.1 1.2K; 0.2 735; 0.3 583 |
| PERCENT_OF_ED_VISITS_RSV | amount | 34 | 0 | 0.0 6.7K; 0.1 1.2K; 0.2 521; 0.3 349 |
| PERCENT_OF_ED_VISITS_COMBINED | amount | 272 | 0 | 0.0 352; 0.5 245; 0.9 227; 0.7 223 |
| DIAGNOSED_COVID_COUNT | other | 577 | 0 | * 1.2K; 0 960; 5 278; 7 268 |
| DIAGNOSED_INFLUENZA_COUNT | other | 545 | 0 | * 2.5K; 0 2.3K; 5 290; 6 265 |
| DIAGNOSED_RSV_COUNT | other | 129 | 0 | 0 6.1K; * 2.2K; 5 190; 7 145 |
| COMBINED_RESPIRATORY_VIRUSES_COUNT | other | 797 | 0 | * 738; 0 456; 7 185; 9 183 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:48:47.42534 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 74abcbcf-ff07-4e3c-be73-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | 3098037ce9c55983f9d0aecd7 10.0K |
