# PORTAL_CKA_OPEN_DATA_SA_9C302CA0AB

rows 3  columns 9  scan 3.3s

roles: amount 2, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026         3  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 3 | 70.27M | 6.77B | 7.43B | 7.44B | 14.29B |
| SHAPE__LENGTH | 3 | 37.6K | 1.32M | 1.40M | 1.40M | 2.76M |

## who

SRC_SHA256 by rows
         3  5ae608bf53c5a41f6fdf54eb5a9d3e9dd37ffbbe0d950cf64dcc0dced249b18e

SRC_SHA256 by dollars
      14.29B        3 rows  5ae608bf53c5a41f6fdf54eb5a9d3e9dd37ffbbe0d950cf64dcc0dced249

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  5ae608bf53c5a41f6fdf54eb5a9d3e9dd37ffbbe  2026:14.29B

## what

OBJECTID: 3 33%, 2 33%, 1 33%

ZONE: Zone 2 33%, Zone 3 33%, Zone 1 33%

CASEMGR: Christina Martinez 33%, Enrique Korrodi 33%, Brittni Williams 33%

GLOBALID: d0b3025c-493a-42e6-9f61-ded24e 33%, 00def3f7-ad5e-4acf-ae1c-086c70 33%, 80262a20-204c-4c31-908f-c46c4b 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 3 | 0 | 3 1; 2 1; 1 1 |
| ZONE | category | 3 | 0 | Zone 2 1; Zone 3 1; Zone 1 1 |
| CASEMGR | category | 3 | 0 | Christina Martinez 1; Enrique Korrodi 1; Brittni Williams 1 |
| GLOBALID | category | 3 | 0 | d0b3025c-493a-42e6-9f61-d 1; 00def3f7-ad5e-4acf-ae1c-0 1; 80262a20-204c-4c31-908f-c 1 |
| SHAPE__AREA | amount | 3 | 0 | 6774774130.34961 1; 7444279436.08398 1; 70266160.2792969 1 |
| SHAPE__LENGTH | amount | 3 | 0 | 1324541.52013455 1; 1396693.71551537 1; 37629.9484594044 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:06.38934 3 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6f3e6877-3f7d-405b-a9a9-a 3 |
| SRC_SHA256 | who | 1 | 0 | 5ae608bf53c5a41f6fdf54eb5 3 |
