# PORTAL_CKA_INDIANA_DATA_HUB_517D2C08EB

rows 11  columns 7  scan 2.4s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        11  ##############################

## who

SRC_SHA256 by rows
        11  41849cd8a4591b81d4bbf7fd0f462218d4ccd40fd7b9401107d6b905cdbe2acc

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  41849cd8a4591b81d4bbf7fd0f462218d4ccd40f  2026:11

## what

FIELD_NAME: Transaction ID 9%, Transaction Date 9%, Transaction Amount 9%, Source 9%, Pcard or Tcard 9%, Merchant Name 9%, Merchant Category Code 9%, Last Updated 9%, Fiscal Year 9%, Agency Name 9%, Agency ID 9%

FIELD_TYPE: Varchar(40) 27%, Varchar(5) 18%, Varchar(24) 9%, Date 9%, Decimal(26,3) 9%, Varchar(25) 9%, TIMESTAMP 9%, Varchar(4) 9%

DESCRIPTION: Transaction identification num 9%, Date of transaction 9%, Transaction amount 9%, Data location 9%, Type of card 9%, Merchant name 9%, Merchant category code as assi 9%, Date of latest data extraction 9%, Fiscal year of transaction 9%, Name of agency 9%, Agency code, 5 digit number 9%

NOTES: Ex. PeopleSoft Financials, the 20%, The state utilizes separate pu 20%, The state operates on a fiscal 20%, References a state agency unde 20%, Ex. 00060; Business Unit repre 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 11 | 0 | Transaction ID 1; Transaction Date 1; Transaction Amount 1; Source 1 |
| FIELD_TYPE | category | 8 | 0 | Varchar(40) 3; Varchar(5) 2; Varchar(24) 1; Date 1 |
| DESCRIPTION | category | 11 | 0 | Transaction identificatio 1; Date of transaction 1; Transaction amount 1; Data location 1 |
| NOTES | category | 6 | 6 | Ex. PeopleSoft Financials 1; The state utilizes separa 1; The state operates on a f 1; References a state agency 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:16.18418 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | d844e549-9c14-4245-b4fb-5 11 |
| SRC_SHA256 | who | 1 | 0 | 41849cd8a4591b81d4bbf7fd0 11 |
