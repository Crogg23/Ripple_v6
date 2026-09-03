# PORTAL_ARC_OPEN_DATA_DC_D74755206A

rows 1.1K  columns 6  scan 2.1s

roles: audit 2, date 1, id 3, who 1

## when

INGESTED_AT
  2026      1.1K  ##############################

## who

SRC_SHA256 by rows
      1.1K  3c8920a2b1ef553b8ea560e1b59615e9ffa37b06e8862ad20bbf324f964544f2

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  3c8920a2b1ef553b8ea560e1b59615e9ffa37b06  2026:1.1K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| F2017_NAICS_CODE | id | 1.0K | 0 | 621210.0 6; 621112.0 6; 621111.0 6; 611710.0 6 |
| F2017_NAICS_TITLE | id | 1.1K | 0 | Offices of Dentists  6; Offices of Physicians, Me 6; Offices of Physicians (ex 6; Educational Support Servi 6 |
| OBJECTID | id | 1.1K | 0 | 1058 6; 1057 6; 1056 6; 1055 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:30:12.31401 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 560c58f8-cbf4-4982-b6f9-5 1.1K |
| SRC_SHA256 | who | 1 | 0 | 3c8920a2b1ef553b8ea560e1b 1.1K |
