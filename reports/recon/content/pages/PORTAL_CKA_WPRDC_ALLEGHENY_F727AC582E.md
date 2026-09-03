# PORTAL_CKA_WPRDC_ALLEGHENY_F727AC582E

rows 563  columns 12  scan 2.8s

roles: audit 2, category 2, date 3, other 3, who 3

## when

FILING_DATE
  2021       138  ##############################
  2022        92  ####################
  2023        99  ######################
  2024        96  #####################
  2025        91  ####################
  2026        47  ##########

LAST_ACTIVITY
  2021         7  #
  2022        18  ##
  2023        37  ####
  2024        87  #########
  2025       131  ##############
  2026       283  ##############################

INGESTED_AT
  2026       563  ##############################

## who

PARTY_NAME by rows
       105  Rising Tide Partners
        24  East Liberty Development Incorporated
        23  Penn Pioneer Enterprises LLC
        19  CP Development
        15  Weapon X Inc.
        14  Pennsylvania Affordable Housing Corporation
        13  East Liberty Development Inc.
        11  IHHWT LLC
         9  Wholesale Properties LLC
         9  Pridewell LLC
         9  RK Conservation Corporation
         8  Erus Holdings LLC
         8  Macedonia Baptist Church
         7  Reaching for a Better Tomorrow Inc.
         7  Uptown Partners of Pittsburgh
         6  Hord Property LLC
         6  Rose Leon
         6  Marlex Properties LLC
         5  Baldwin Borough
         5  RE Servicing LLC

PARTY_TYPE by rows
       563  Petitioner

SRC_SHA256 by rows
       563  fbe3efd369e3e33fe578c447523171654696e0832ea5e086d567b7472de57712

## who x when

PARTY_NAME by FILING_DATE
  Baldwin Borough                           2021:3 2024:2
  CP Development                            2022:7 2023:12
  East Liberty Development Inc.             2021:8 2022:1 2025:2 2026:2
  East Liberty Development Incorporated     2021:16 2023:3 2024:5
  Erus Holdings LLC                         2021:2 2022:2 2025:1 2026:3
  Hord Property LLC                         2024:1 2025:3 2026:2
  IHHWT LLC                                 2021:2 2022:2 2023:2 2024:2 2025:3
  Macedonia Baptist Church                  2022:8
  Marlex Properties LLC                     2022:1 2024:2 2025:3
  Penn Pioneer Enterprises LLC              2021:13 2023:1 2024:2 2025:1 2026:6
  Pennsylvania Affordable Housing Corporat  2023:3 2024:11
  Pridewell LLC                             2021:1 2022:1 2024:7
  RE Servicing LLC                          2021:1 2025:4
  RK Conservation Corporation               2023:2 2024:4 2025:3
  Reaching for a Better Tomorrow Inc.       2025:6 2026:1
  Rising Tide Partners                      2021:49 2022:19 2023:24 2024:12 2025:1
  Rose Leon                                 2024:6
  Uptown Partners of Pittsburgh             2022:3 2023:2 2024:1 2026:1
  Weapon X Inc.                             2021:7 2023:1 2024:7
  Wholesale Properties LLC                  2021:6 2022:2 2024:1

PARTY_TYPE by FILING_DATE
  Petitioner                                2021:138 2022:92 2023:99 2024:96 2025:91 2026:47

## what

MUNICIPALITY: Pittsburgh 79%, Wilkinsburg Boro 11%, Penn Hills Township 3%, Sharpsburg Boro 1%, Moon Township 1%, Ross Township 1%, Baldwin Boro 1%, Sewickley Boro 1%, S. Fayette Township 1%, Churchill Boro 1%, Turtle Creek Boro 1%, Rankin Boro 0%

WARD: 13 22%, 12 20%, 11 10%, 5 9%, 15 8%, 10 7%, 25 6%, 24 5%, 26 5%, 14 5%, 32 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PIN | other | 515 | 0 | 0027A00047000000 4; 0027A00050000000 4; 0012F00108000000 4; 0026K00067000000 4 |
| BLOCK_LOT | other | 525 | 0 | 27A50 4; 12F108 4; 26K67 4; 61M224 4 |
| FILING_DATE | date | 304 | 0 | 2021-11-09 13; 2021-07-31 13; 2022-11-14 10; 2021-12-21 10 |
| CASE_ID | other | 482 | 0 | CS-21-000109 10; CS-25-000062 8; CS-22-000072 8; CS-25-000053 6 |
| MUNICIPALITY | category | 42 | 0 | Pittsburgh 415; Wilkinsburg Boro 59; Penn Hills Township 16; Sharpsburg Boro 7 |
| WARD | category | 33 | 146 | 13 65; 12 61; 11 29; 5 26 |
| PARTY_TYPE | who | 1 | 0 | Petitioner 563 |
| PARTY_NAME | who | 195 | 0 | Rising Tide Partners 105; East Liberty Development  24; Penn Pioneer Enterprises  23; CP Development 19 |
| LAST_ACTIVITY | date | 260 | 0 | 2026-04-25 37; 2026-06-23 27; 2026-06-15 22; 2026-06-30 12 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:21:37.75563 563 |
| SOURCE_RUN_ID | audit | 1 | 0 | 807beec4-7c28-45ea-825a-7 563 |
| SRC_SHA256 | who | 1 | 0 | fbe3efd369e3e33fe578c4475 563 |
