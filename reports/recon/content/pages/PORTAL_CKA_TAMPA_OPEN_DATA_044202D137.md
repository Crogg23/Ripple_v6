# PORTAL_CKA_TAMPA_OPEN_DATA_044202D137

rows 42  columns 13  scan 3.4s

roles: amount 1, audit 2, category 2, date 2, empty 2, other 2, who 3

## when

DATE
  2022        12  ###############
  2023        24  ##############################
  2024         2  ##
  2025         2  ##
  2026         2  ##

INGESTED_AT
  2026        42  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 42 | 13 | 298.6K | 43.91M | 45.40M | 124.74M |

## who

CHARTNAME by rows
        42  Marketing and Communications

CHARTNAME by dollars
     124.74M       42 rows  Marketing and Communications

C_ORGANIZATION by rows
        42  Marketing & Communications (Marketing and Communications)

C_ORGANIZATION by dollars
     124.74M       42 rows  Marketing & Communications (Marketing and Communications)

SRC_SHA256 by rows
        42  27abbae60b1e15678fcd5a79c3f902d3133d8ad9ee87c244d26b48890b9ec7e4

SRC_SHA256 by dollars
     124.74M       42 rows  27abbae60b1e15678fcd5a79c3f902d3133d8ad9ee87c244d26b48890b9e

## who x when

CHARTNAME by DATE, dollars = VALUE
  Marketing and Communications              2022:12.72M 2023:23.64M 2024:46.01M 2025:42.37M 2026:341

C_ORGANIZATION by DATE, dollars = VALUE
  Marketing & Communications (Marketing an  2022:12.72M 2023:23.64M 2024:46.01M 2025:42.37M 2026:341

## what

ID: 18984 8%, 18983 8%, 18691 8%, 18688 8%, 18685 8%, 18681 8%, 10332 8%, 10329 8%, 10323 8%, 10322 8%, 10253 8%, 10252 8%

CATEGORY: Impressions 26%, Total Audience 26%, Videos Created 24%, Press Releases Sent 24%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 42 | 0 | 18984 1; 18983 1; 18691 1; 18688 1 |
| C_ORGANIZATION | who | 1 | 0 | Marketing & Communication 42 |
| CHARTNAME | who | 1 | 0 | Marketing and Communicati 42 |
| DESCRIPTION | empty | 1 | 42 |  |
| CATEGORY | category | 4 | 0 | Impressions 11; Total Audience 11; Videos Created 10; Press Releases Sent 10 |
| SUMMARY | other | 1 | 0 | Total 42 |
| TYPEDATA | other | 1 | 0 | Date 42 |
| DATE | date | 12 | 0 | 2023-06-30T00:00:00 4; 2023-01-31T00:00:00 4; 2023-05-31T00:00:00 4; 2023-02-28T00:00:00 4 |
| PERIOD | empty | 1 | 42 |  |
| VALUE | amount | 39 | 0 | 30 3; 25 2; 71 1; 270 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:11:52.99605 42 |
| SOURCE_RUN_ID | audit | 1 | 0 | c4fdb0f1-1551-43b0-b50b-f 42 |
| SRC_SHA256 | who | 1 | 0 | 27abbae60b1e15678fcd5a79c 42 |
