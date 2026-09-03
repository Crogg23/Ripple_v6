# PORTAL_CKA_OPEN_DATA_SA_3B9CCBCFD0

rows 15  columns 9  scan 2.9s

roles: amount 2, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        15  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 15 | 1.63M | 4.76M | 17.31M | 17.83M | 97.95M |
| SHAPE__LENGTH | 15 | 5.8K | 12.4K | 18.2K | 18.2K | 171.6K |

## who

SRC_SHA256 by rows
        15  578d065af83e725db992d86c226b1b24916b27f30e23a6bfba4b1b2040cccd79

SRC_SHA256 by dollars
      97.95M       15 rows  578d065af83e725db992d86c226b1b24916b27f30e23a6bfba4b1b2040cc

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  578d065af83e725db992d86c226b1b24916b27f3  2026:97.95M

## what

OBJECTID: 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%

LANDUSE: Mixed Use 47%, Residential 27%, Government/ Educational 13%, Commercial 7%, Government 7%

DISTRICT: M 15%, O 8%, F 8%, N 8%, A 8%, J 8%, Q 8%, L 8%, T 8%, G 8%, S 8%, P 8%

LANDUSECODE: 2200 33%, 1111 27%, 4100 20%, 2203 13%, 2000 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 15 | 0 | 15 1; 14 1; 13 1; 12 1 |
| LANDUSE | category | 5 | 0 | Mixed Use 7; Residential 4; Government/ Educational 2; Commercial 1 |
| DISTRICT | category | 14 | 0 | M 2; O 1; F 1; N 1 |
| LANDUSECODE | category | 5 | 0 | 2200 5; 1111 4; 4100 3; 2203 2 |
| SHAPE__AREA | amount | 15 | 0 | 4096724.93164063 1; 1721281.59375 1; 3068864.30273438 1; 17832691.9667969 1 |
| SHAPE__LENGTH | amount | 15 | 0 | 8553.78178515684 1; 5825.43395601393 1; 8088.65000425821 1; 18222.6203015519 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:03.57743 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2d55051b-b69c-4c7c-b83b-9 15 |
| SRC_SHA256 | who | 1 | 0 | 578d065af83e725db992d86c2 15 |
