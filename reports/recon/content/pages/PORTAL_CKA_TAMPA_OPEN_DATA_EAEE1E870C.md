# PORTAL_CKA_TAMPA_OPEN_DATA_EAEE1E870C

rows 82  columns 26  scan 4.3s

roles: amount 1, audit 2, category 6, date 8, empty 4, other 4, who 2

## when

DATE
  2021         6  #########
  2022        20  ##############################
  2023        18  ###########################
  2024        20  ##############################
  2025        12  ##################
  2026         6  #########

CUSTOM_DATE_1
  2026        82  ##############################

CUSTOM_DATE_2
  2026        82  ##############################

CUSTOM_DATE_3
  2026        82  ##############################

LAST_UPDATE
  2021         3  ####
  2022        15  ###################
  2023        24  ##############################
  2024        21  ##########################
  2025        12  ###############
  2026         7  #########

LAST_UPDATE_COT
  2026        82  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 82 | 0 | 99.00 | 100 | 100 | 6.2K |

## who

AUTOMATION by rows
        82  Manual

AUTOMATION by dollars
        6.2K       82 rows  Manual

SRC_SHA256 by rows
        82  6510acccc166b462967729f4890737fd8e821d8b5134040dd53e1fbd3bc986f4

SRC_SHA256 by dollars
        6.2K       82 rows  6510acccc166b462967729f4890737fd8e821d8b5134040dd53e1fbd3bc9

## who x when

AUTOMATION by DATE, dollars = VALUE
  Manual                                    2021:215 2022:1.4K 2023:1.4K 2024:1.4K 2025:1.2K 2026:578.53

SRC_SHA256 by DATE, dollars = VALUE
  6510acccc166b462967729f4890737fd8e821d8b  2021:215 2022:1.4K 2023:1.4K 2024:1.4K 2025:1.2K 2026:578.53

## what

ORGANZIATION: Logistics & Asset Management ( 68%, Neighborhood Empowerment 17%, Neighborhood Empowerment (Neig 15%

CHARTNAME: Percent of Vehicles Available  68%, Total Number of Organized Neig 17%, Total Number of Neighborhoods 15%

DESCRIPTION: Neighborhood Engagement; Total 54%, Neighborhood Engagement 46%

CATEGORY: Percent of Vehicles 68%, In Process 9%, Inactive 9%, Active 9%, Deed Restricted 6%

SUMMARY: Percent 68%, Total 32%

DATA_TYPE: Integer 78%, Decimal 22%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 83 | 0 | 21295 1; 21110 1; 20508 1; 19695 1 |
| ORGANZIATION | category | 3 | 0 | Logistics & Asset Managem 56; Neighborhood Empowerment 14; Neighborhood Empowerment  12 |
| CHARTNAME | category | 3 | 0 | Percent of Vehicles Avail 56; Total Number of Organized 14; Total Number of Neighborh 12 |
| DESCRIPTION | category | 3 | 56 | Neighborhood Engagement;  14; Neighborhood Engagement 12 |
| CATEGORY | category | 5 | 0 | Percent of Vehicles 56; In Process 7; Inactive 7; Active 7 |
| SUMMARY | category | 2 | 0 | Percent 56; Total 26 |
| PERIOD | empty | 1 | 82 |  |
| DATE | date | 61 | 0 | 11/01/2023 00:00:00 7; 07/07/2022 00:00:00 6; 11/21/2024 00:00:00 4; 02/07/2024 00:00:00 4 |
| DATA_TYPE | category | 2 | 0 | Integer 64; Decimal 18 |
| VALUE | amount | 32 | 0 | 100.00 37; 7.00 4; 78.00 4; 15.00 3 |
| AUTOMATION | who | 1 | 0 | Manual 82 |
| CUSTOM_TEXT_1 | empty | 1 | 82 |  |
| CUSTOM_TEXT_2 | empty | 1 | 82 |  |
| CUSTOM_TEXT_3 | empty | 1 | 82 |  |
| CUSTOM_NUMBER_1 | other | 1 | 0 | 0 82 |
| CUSTOM_NUMBER_2 | other | 1 | 0 | 0 82 |
| CUSTOM_NUMBER_3 | other | 1 | 0 | 0 82 |
| CUSTOM_DATE_1 | date | 1 | 0 | 07/02/2026 12:30:33 82 |
| CUSTOM_DATE_2 | date | 1 | 0 | 07/02/2026 12:30:33 82 |
| CUSTOM_DATE_3 | date | 1 | 0 | 07/02/2026 12:30:33 82 |
| LAST_UPDATE | date | 68 | 0 | 07/01/2022 15:30:00 5; 01/04/2023 20:40:00 4; 11/21/2024 11:43:00 3; 01/04/2023 20:39:00 3 |
| LAST_UPDATE_COT | date | 1 | 0 | 07/02/2026 12:30:33 82 |
| LAST_UPDATE_OGI | date | 1 | 0 | 07/02/2026 12:30:33 82 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:14:19.90068 82 |
| SOURCE_RUN_ID | audit | 1 | 0 | f0c0d420-86fa-46ab-bef7-1 82 |
| SRC_SHA256 | who | 1 | 0 | 6510acccc166b462967729f48 82 |
