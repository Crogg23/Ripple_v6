# PORTAL_CKA_INDIANA_DATA_HUB_7F118FAE1C

rows 15  columns 7  scan 2.0s

roles: audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        15  ##############################

## who

SRC_SHA256 by rows
        15  9d4da584172ff0984c0da5222b152dc999bd0ab4df8fde90389154c9705926aa

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  9d4da584172ff0984c0da5222b152dc999bd0ab4  2026:15

## what

FIELD_NAME: Balance Date 8%, YTD Amount 8%, MTD Amount 8%, Legal Fund Name 8%, Legal Fund ID 8%, CF_ATTRIBUTE 8%, Fund Name 8%, Fund ID 8%, Account Name 8%, Account ID 8%, Accounting Period 8%, Fiscal Year 8%

FIELD_TYPE: VARCHAR(5000) 33%, DECIMAL(28,7) 13%, VARCHAR(5) 13%, DECIMAL(28,0) 13%, TIMESTAMP 7%, VARCHAR(60) 7%, VARCHAR(15) 7%, VARCHAR(10) 7%

DESCRIPTION: Date of latest period balance 8%, Fiscal Year to date accumulate 8%, Month to date accumulated Amou 8%, Legal Fund description 8%, Legal Fund code; 4 digits 8%, Charterfield Attribute Number 8%, Fund description 8%, Fund code, 5 digit number 8%, Account description 8%, Account code; 6 digits 8%, Accounting Period/Fiscal Year  8%, Fiscal Year of Transaction 8%

NOTES: Reference to classification of 17%, Ex. General Fund, State Highwa 8%, Ex. 1000; References money set 8%, Ex. Legal_Fund; Identifies the 8%, Ex. Access Indiana; References 8%, Ex. 46710; References operatin 8%, References the fiscal year per 8%, The state operates on a fiscal 8%, References the state's General 8%, References a state agency unde 8%, Ex. 00060; Business Unit repre 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELD_NAME | category | 15 | 0 | Balance Date 1; YTD Amount 1; MTD Amount 1; Legal Fund Name 1 |
| FIELD_TYPE | category | 8 | 0 | VARCHAR(5000) 5; DECIMAL(28,7) 2; VARCHAR(5) 2; DECIMAL(28,0) 2 |
| DESCRIPTION | category | 15 | 0 | Date of latest period bal 1; Fiscal Year to date accum 1; Month to date accumulated 1; Legal Fund description 1 |
| NOTES | category | 12 | 3 | Reference to classificati 2; Ex. General Fund, State H 1; Ex. 1000; References mone 1; Ex. Legal_Fund; Identifie 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:07:51.76616 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4a758a19-e83e-4105-8d3b-4 15 |
| SRC_SHA256 | who | 1 | 0 | 9d4da584172ff0984c0da5222 15 |
