# PORTAL_CKA_WESTERN_PENNSYLV_BD609B0793

rows 10.0K  columns 6  scan 2.2s

roles: audit 2, category 1, date 2, other 1, who 1

## when

DATE
  2022      1.6K  ###################
  2023      2.4K  ##############################
  2024      2.4K  ##############################
  2025      2.3K  ############################
  2026      1.3K  ################

INGESTED_AT
  2026     10.0K  ##############################

## who

SRC_SHA256 by rows
     10.0K  4bacbc41ddb378e5f5ceb8461b8594b8ee02e2ef9ed090fe82df9a3191e4d55a

## who x when

SRC_SHA256 by DATE
  4bacbc41ddb378e5f5ceb8461b8594b8ee02e2ef  2022:1.6K 2023:2.4K 2024:2.4K 2025:2.3K 2026:1.3K

## what

CENTER_NAME: West Penn Community Center 12%, Magee Community Center 12%, Warrington Community Center 11%, Brookline Community Center 11%, Paulson Community Center 11%, Ormsby Community Center 10%, Phillips Community Center 10%, Arlington Community Center 9%, Ammon Community Center 8%, Jefferson Community Center 6%, Jefferson Recreation Center 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATE | date | 1.3K | 0 | 2022-04-19 55; 2022-04-21 55; 2022-04-25 55; 2022-04-26 55 |
| CENTER_NAME | category | 10 | 0 | West Penn Community Cente 1.2K; Magee Community Center 1.1K; Warrington Community Cent 1.1K; Brookline Community Cente 1.1K |
| ATTENDANCE_COUNT | other | 213 | 0 | 1 258; 11 236; 7 234; 12 231 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:46:55.27530 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | e8c695e7-f811-43cb-8e2e-6 10.0K |
| SRC_SHA256 | who | 1 | 0 | 4bacbc41ddb378e5f5ceb8461 10.0K |
