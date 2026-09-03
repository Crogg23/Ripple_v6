# PORTAL_CKA_CALIFORNIA_OPEN_B98053323B

rows 4  columns 6  scan 2.2s

roles: audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026         4  ##############################

## who

SRC_SHA256 by rows
         4  00912c5fc26fd967e35e0acfaa51d3d6013f0ee63905ab7deae83f093940708f

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  00912c5fc26fd967e35e0acfaa51d3d6013f0ee6  2026:4

## what

FIELDNAME: YearlyNetChange 25%, TotalReleases 25%, TotalAdmissions 25%, Date 25%

DATATYPE: Num 75%, Char 25%

DESCRIPTION: Provides the sum of the differ 25%, Shows the total number of rele 25%, Shows the total number of admi 25%, Identifies the end of the list 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIELDNAME | category | 4 | 0 | YearlyNetChange 1; TotalReleases 1; TotalAdmissions 1; Date 1 |
| DATATYPE | category | 2 | 0 | Num 3; Char 1 |
| DESCRIPTION | category | 4 | 0 | Provides the sum of the d 1; Shows the total number of 1; Shows the total number of 1; Identifies the end of the 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:06:05.68984 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6f995bd3-6823-4c36-ae61-9 4 |
| SRC_SHA256 | who | 1 | 0 | 00912c5fc26fd967e35e0acfa 4 |
