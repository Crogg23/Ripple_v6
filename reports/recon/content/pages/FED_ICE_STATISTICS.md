# FED_ICE_STATISTICS

rows 221  columns 13  scan 2.4s

roles: audit 3, category 3, date 1, empty 4, other 2, who 1

## when

SNAPSHOT_DATE
  2026       221  ##############################

## who

_SRC_SHA256 by rows
       221  ceab3e53d196a9fa860f3d8992d0a124f92aa7771695f62e7a264f6ab3331000

## who x when

_SRC_SHA256 by SNAPSHOT_DATE  LOAD STAMP, not an event date
  ceab3e53d196a9fa860f3d8992d0a124f92aa777  2026:221

## what

METRIC_TYPE: removals 92%, unknown 8%

CRIMINAL_HISTORY_CATEGORY: Total Arrests 25%, No Known Criminal Charges or C 25%, Pending Criminal Charges 25%, Criminal Convictions 25%

COUNT: 100% 17%, 240255 17%, 100.0% 17%, 10.8% 17%, 15.5% 17%, 73.7% 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | other | 100 | 24 | 1 16; 10 9; 2 7; 3 7 |
| FISCAL_QUARTER | empty | 1 | 221 |  |
| METRIC_TYPE | category | 2 | 0 | removals 203; unknown 18 |
| COUNTRY_OF_CITIZENSHIP | other | 200 | 24 | Total 1; Seychelles 1; Montserrat 1; Macau 1 |
| CRIMINAL_HISTORY_CATEGORY | category | 5 | 217 | Total Arrests 1; No Known Criminal Charges 1; Pending Criminal Charges 1; Criminal Convictions 1 |
| AOR | empty | 1 | 221 |  |
| COUNT | category | 7 | 215 | 100% 1; 240255 1; 100.0% 1; 10.8% 1 |
| REMOVAL_AUTHORITY | empty | 1 | 221 |  |
| ATD_MONITORING_TYPE | empty | 1 | 221 |  |
| SNAPSHOT_DATE | audit date | 1 | 0 | 2026-07-02 221 |
| _INGESTED_AT | audit | 1 | 0 | 1783009876478005 221 |
| _SOURCE_RUN_ID | audit | 1 | 0 | cf699030-063e-4098-a1fd-9 221 |
| _SRC_SHA256 | who | 1 | 0 | ceab3e53d196a9fa860f3d899 221 |
