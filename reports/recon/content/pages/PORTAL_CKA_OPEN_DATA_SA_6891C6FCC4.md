# PORTAL_CKA_OPEN_DATA_SA_6891C6FCC4

rows 12  columns 9  scan 2.8s

roles: amount 3, audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BONDAREA | 12 | 20.27 | 175.85 | 841.85 | 863.35 | 3.2K |
| SHAPE__AREA | 12 | 882.7K | 7.66M | 36.67M | 37.61M | 137.89M |
| SHAPE__LENGTH | 12 | 9.6K | 20.7K | 95.0K | 96.6K | 425.1K |

## who

SRC_SHA256 by rows
        12  9345702de20135f108042f79cfaa09541aed05e1bcbf6024dd5aa6ffdf8d5db9

SRC_SHA256 by dollars
        3.2K       12 rows  9345702de20135f108042f79cfaa09541aed05e1bcbf6024dd5aa6ffdf8d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = BONDAREA
  9345702de20135f108042f79cfaa09541aed05e1  2026:3.2K

## what

OBJECTID: 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%, 1 8%

NAME: Roosevelt-Mission Reach 8%, Edgewood 8%, Culebra at Callahan 8%, South Park 8%, Near East 8%, Wurzbach 8%, East Southcross 8%, Pearsall 8%, Southeast 8%, Lincoln Park - Arena District 8%, Westside 8%, Near West Five Points 8%

GLOBALID: f3700ddb-bb07-4108-bb0a-14e67b 8%, 538baf19-b20a-43f5-a3cc-c8bc7c 8%, 9ba2d3f5-98d5-4345-b502-01fdcb 8%, d78e472c-b497-44c9-ba61-fe088d 8%, b7c171f5-aa19-479b-a3d5-92a798 8%, 3ce76d35-8354-48ea-a439-7b7018 8%, 410056ba-38e3-4a50-a39a-21621d 8%, 0a8e6676-4265-4ad7-84a7-cc93bd 8%, 5762c9d9-fb24-4af5-b583-dac678 8%, 47d00846-7cca-4a9c-8c90-bab7dd 8%, adaaad13-092f-4fe2-aa3a-73fbea 8%, 785d2c7c-04a7-4fbd-ac09-836897 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 12 | 0 | 12 1; 11 1; 10 1; 9 1 |
| NAME | category | 12 | 0 | Roosevelt-Mission Reach 1; Edgewood 1; Culebra at Callahan 1; South Park 1 |
| BONDAREA | amount | 12 | 0 | 65.907 1; 41.441 1; 39.922 1; 103.127 1 |
| GLOBALID | category | 12 | 0 | f3700ddb-bb07-4108-bb0a-1 1; 538baf19-b20a-43f5-a3cc-c 1; 9ba2d3f5-98d5-4345-b502-0 1; d78e472c-b497-44c9-ba61-f 1 |
| SHAPE__AREA | amount | 12 | 0 | 2870880.92773438 1; 1805177.1171875 1; 1738985.50976563 1; 4492202.28515625 1 |
| SHAPE__LENGTH | amount | 12 | 0 | 15124.0205886235 1; 13821.5031615337 1; 9607.23653820757 1; 13278.2954394515 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:50.97181 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2c0fc890-e776-48fc-9294-9 12 |
| SRC_SHA256 | who | 1 | 0 | 9345702de20135f108042f79c 12 |
