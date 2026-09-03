# PORTAL_CKA_OPEN_DATA_SA_C589D75D2F

rows 12  columns 8  scan 2.5s

roles: amount 2, audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        12  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 12 | 12.04M | 25.25M | 356.42M | 383.72M | 857.51M |
| SHAPE__LENGTH | 12 | 16.6K | 52.3K | 312.3K | 336.5K | 947.6K |

## who

SRC_SHA256 by rows
        12  fc1bbf4b1759c7d51794a1e100beeebbee529b73f60e162389510461cb08d72b

SRC_SHA256 by dollars
     857.51M       12 rows  fc1bbf4b1759c7d51794a1e100beeebbee529b73f60e162389510461cb08

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  fc1bbf4b1759c7d51794a1e100beeebbee529b73  2026:857.51M

## what

OBJECTID: 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%, 1 8%

NAME: Roosevelt 8%, Fredericksburg Rd  8%, N. St. Marys 8%, Broadway 8%, Nacogdoches Corridor 8%, Austin Highway Corridor 8%, Loop 410 Corridor 8%, Perrin Beitel Corridor 8%, Loop 1604 Corridor 8%, I 35 Corridor 8%, TX 151 Corridor 8%, I 10 West Corridor 8%

STATUS: Completed 50%, Potential 42%, Pending 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 12 | 0 | 12 1; 11 1; 10 1; 9 1 |
| NAME | category | 12 | 0 | Roosevelt 1; Fredericksburg Rd  1; N. St. Marys 1; Broadway 1 |
| STATUS | category | 3 | 0 | Completed 6; Potential 5; Pending 1 |
| SHAPE__AREA | amount | 12 | 0 | 17260323.0332031 1; 12373564.1542969 1; 12044390.4863281 1; 23653603.1328125 1 |
| SHAPE__LENGTH | amount | 12 | 0 | 61151.3250464904 1; 16643.006888576 1; 16761.85620552 1; 27570.7743061193 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:07.77876 12 |
| SOURCE_RUN_ID | audit | 1 | 0 | e92d009d-8ebd-48ff-b3c6-3 12 |
| SRC_SHA256 | who | 1 | 0 | fc1bbf4b1759c7d51794a1e10 12 |
