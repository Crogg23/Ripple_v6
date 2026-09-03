# PORTAL_CKA_TAMPA_OPEN_DATA_39C5B89D70

rows 29  columns 13  scan 3.2s

roles: amount 1, audit 2, category 5, date 2, empty 1, other 2, who 1

## when

DATE
  2017         1  ###
  2018         1  ###
  2019         5  ###############
  2020        10  ##############################
  2021         9  ###########################
  2026         3  #########

INGESTED_AT
  2026        29  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 29 | 0 | 10 | 883.28 | 1.2K | 1.9K |

## who

SRC_SHA256 by rows
        29  4afeccc1a0cd680d7c4ff39ae55e45b9b0ccee51d527e18f74ad4ccd62f842f8

SRC_SHA256 by dollars
        1.9K       29 rows  4afeccc1a0cd680d7c4ff39ae55e45b9b0ccee51d527e18f74ad4ccd62f8

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  4afeccc1a0cd680d7c4ff39ae55e45b9b0ccee51  2017:9 2018:8 2019:1.3K 2020:470 2021:114 2026:10

## what

ID: 3423 8%, 3422 8%, 3421 8%, 3420 8%, 3419 8%, 3418 8%, 3417 8%, 3416 8%, 3415 8%, 3414 8%, 3413 8%, 3412 8%

C_ORGANIZATION: Office of the Mayor (Mayor) 90%, City of Tampa 10%

CHARTNAME: Sustainability 90%, Mayor's Strategic Initiatives  10%

DESCRIPTION: Initiatives completed 100%

CATEGORY: Number of Trees Planted 45%, Projects by Fiscal Year 14%, Initiatives completed 10%, Solar Energy 10%, Electric Vehicles 10%, Started 3%, Not Started 3%, Completed 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 29 | 0 | 3423 1; 3422 1; 3421 1; 3420 1 |
| C_ORGANIZATION | category | 2 | 0 | Office of the Mayor (Mayo 26; City of Tampa 3 |
| CHARTNAME | category | 2 | 0 | Sustainability 26; Mayor's Strategic Initiat 3 |
| DESCRIPTION | category | 2 | 3 | Initiatives completed 26 |
| CATEGORY | category | 8 | 0 | Number of Trees Planted 13; Projects by Fiscal Year 4; Initiatives completed 3; Solar Energy 3 |
| SUMMARY | other | 1 | 0 | Total 29 |
| TYPEDATA | other | 1 | 0 | Date 29 |
| DATE | date | 21 | 0 | 04/01/2021 00:00:00 3; 02/01/2021 00:00:00 3; 07/02/2026 12:30:57 3; 01/01/2020 00:00:00 2 |
| PERIOD | empty | 1 | 29 |  |
| VALUE | amount | 17 | 0 | 0.000 9; 3.000 3; 35.000 3; 18.000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:10:39.93013 29 |
| SOURCE_RUN_ID | audit | 1 | 0 | ba29d7b8-0e8b-4804-b386-8 29 |
| SRC_SHA256 | who | 1 | 0 | 4afeccc1a0cd680d7c4ff39ae 29 |
