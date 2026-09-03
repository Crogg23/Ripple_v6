# PORTAL_CKA_ANALYZE_BOSTON_C36F95122C

rows 20  columns 11  scan 3.4s

roles: amount 2, audit 2, category 2, date 1, empty 4, who 1

## when

INGESTED_AT
  2026        20  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 20 | 0.01 | 0.04 | 0.10 | 0.10 | 1.01 |
| SHAPE_AREA | 20 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
        20  38467d2c69d6aa3a35a543bcb8e9178b4f954432127b0e88cdc2befc370d293b

SRC_SHA256 by dollars
        1.01       20 rows  38467d2c69d6aa3a35a543bcb8e9178b4f954432127b0e88cdc2befc370d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  38467d2c69d6aa3a35a543bcb8e9178b4f954432  2026:1.01

## what

NAME: MISSION HILL 8%, MATTAPAN 8%, ROSLINDALE VILLAGE 8%, WEST ROXBURY 8%, HYDE PARK 8%, ST MARKS 8%, FIELDS CORNER 8%, UPHAMS CORNER 8%, BOWDOIN/GENEVA 8%, FOUR CORNERS 8%, GREATER GROVE HALL 8%, EGLESTON SQUARE 8%

DIST_NAME: Mission Hill 8%, Mattapan 8%, Roslindale Village 8%, West Roxbury 8%, Hyde Park 8%, St Mark's 8%, Fields Corner 8%, Uphams Corner 8%, Bowdoin/Geneva 8%, Four Corners 8%, Grove Hall 8%, Egleston Square 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ROW_ID | empty | 1 | 20 |  |
| NAME | category | 20 | 0 | MISSION HILL 1; MATTAPAN 1; ROSLINDALE VILLAGE 1; WEST ROXBURY 1 |
| DIST_NAME | category | 20 | 0 | Mission Hill 1; Mattapan 1; Roslindale Village 1; West Roxbury 1 |
| AREA | empty | 1 | 20 |  |
| LEN | empty | 1 | 20 |  |
| SHAPE_LENGTH | amount | 20 | 0 | 0.078681581658594 1; 0.027466254074521 1; 0.017796020394126 1; 0.103705195698502 1 |
| SHAPE_AREA | amount | 20 | 0 | 0.000039962995271 1; 0.000009910429166 1; 0.000007219458323 1; 0.000053942730032 1 |
| SHAPE_WKT | empty | 1 | 20 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:18.77946 20 |
| SOURCE_RUN_ID | audit | 1 | 0 | f7948e50-b99e-488b-b6f9-d 20 |
| SRC_SHA256 | who | 1 | 0 | 38467d2c69d6aa3a35a543bcb 20 |
