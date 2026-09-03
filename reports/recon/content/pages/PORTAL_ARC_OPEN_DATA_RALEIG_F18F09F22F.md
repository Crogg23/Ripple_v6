# PORTAL_ARC_OPEN_DATA_RALEIG_F18F09F22F

rows 2  columns 22  scan 2.2s

roles: audit 2, category 3, date 1, empty 14, other 2, who 1

## when

INGESTED_AT
  2026         2  ##############################

## who

SRC_SHA256 by rows
         2  ff6deaaf4a074ff9f1e2e5eecf08a1b27e20cac42ea52bd2805e63b165e6b52c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  ff6deaaf4a074ff9f1e2e5eecf08a1b27e20cac4  2026:2

## what

APPLICATION_DATE: Total 100%

ACCOUNT_NAME: 307 100%

FID: 2 50%, 1 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| APPLICATION_DATE | category | 2 | 1 | Total 1 |
| ACCOUNT_NAME | category | 2 | 1 | 307 1 |
| COMPANY_STRUCTURE | empty | 1 | 2 |  |
| PRIMARY_OWNER | empty | 1 | 2 |  |
| STAGE | empty | 1 | 2 |  |
| AMOUNT | other | 1 | 0 | 0 2 |
| SHIPPING_ADDRESS_LINE_1 | empty | 1 | 2 |  |
| SHIPPING_CITY | empty | 1 | 2 |  |
| SHIPPING_ZIP_POSTAL_CODE | empty | 1 | 2 |  |
| FULL_ADDRESS | empty | 1 | 2 |  |
| PRIMARY_OWNER_EMAIL | empty | 1 | 2 |  |
| PHONE | empty | 1 | 2 |  |
| PRIMARY_OWNER_RACE | empty | 1 | 2 |  |
| MINORITY_OWNED_FIRM | empty | 1 | 2 |  |
| WOMEN_OWNED_FIRM | empty | 1 | 2 |  |
| VETERAN_OWNED_FIRM | empty | 1 | 2 |  |
| NAICS_6_DIGIT_CODE | other | 1 | 0 | 0 2 |
| NAICS_6_DIGIT_DESCRIPTION | empty | 1 | 2 |  |
| FID | category | 2 | 0 | 2 1; 1 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:11:43.28156 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0fd88049-c5f1-4298-9338-8 2 |
| SRC_SHA256 | who | 1 | 0 | ff6deaaf4a074ff9f1e2e5eec 2 |
