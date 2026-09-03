# PORTAL_CKA_SAN_JOSE_OPEN_DA_9F5FD1969E

rows 6  columns 14  scan 5.3s

roles: amount 2, audit 2, category 7, date 1, empty 1, who 2

## when

INGESTED_AT
  2026         6  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 6 | 110.6K | 203.2K | 278.0K | 278.4K | 1.24M |
| SHAPE_AREA | 6 | 277.48M | 1.01B | 2.64B | 2.66B | 7.81B |

## who

CREATIONDATE by rows
         6  1900/01/01 00:00:00+00

CREATIONDATE by dollars
       1.24M        6 rows  1900/01/01 00:00:00+00

SRC_SHA256 by rows
         6  61ce479eee9ffe515265d0ef3011455e31f192f9ef5e47beaba561670977d070

SRC_SHA256 by dollars
       1.24M        6 rows  61ce479eee9ffe515265d0ef3011455e31f192f9ef5e47beaba561670977

## who x when

CREATIONDATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  1900/01/01 00:00:00+00                    2026:1.24M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  61ce479eee9ffe515265d0ef3011455e31f192f9  2026:1.24M

## what

OBJECTID: 6 17%, 5 17%, 4 17%, 3 17%, 2 17%, 1 17%

FACILITYID: 202 17%, 128 17%, 135 17%, 127 17%, 137 17%, 136 17%

ZONE: 4 17%, 6 17%, 1 17%, 3 17%, 2 17%, 5 17%

NAME: Victor Lopez 17%, Antonio Lopez 17%, Jason Pratico 17%, Carl Dinga 17%, Jose Alcazar 17%, William Anton 17%

LASTUPDATE: 2023/11/15 16:28:42+00 17%, 2023/11/15 16:29:05+00 17%, 2023/11/15 16:27:38+00 17%, 2021/10/07 15:21:35+00 17%, 2023/11/15 16:27:50+00 17%, 2023/11/15 16:29:01+00 17%

NOTES: Central 17%, West 17%, North West 17%, South 17%, East 17%, South East 17%

INTID: 202 17%, 128 17%, 135 17%, 127 17%, 137 17%, 136 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 6 | 0 | 6 1; 5 1; 4 1; 3 1 |
| FACILITYID | category | 6 | 0 | 202 1; 128 1; 135 1; 127 1 |
| ZONE | category | 6 | 0 | 4 1; 6 1; 1 1; 3 1 |
| NAME | category | 6 | 0 | Victor Lopez 1; Antonio Lopez 1; Jason Pratico 1; Carl Dinga 1 |
| SECONDARYNAME | empty | 1 | 6 |  |
| LASTUPDATE | category | 6 | 0 | 2023/11/15 16:28:42+00 1; 2023/11/15 16:29:05+00 1; 2023/11/15 16:27:38+00 1; 2021/10/07 15:21:35+00 1 |
| NOTES | category | 6 | 0 | Central 1; West 1; North West 1; South 1 |
| SHAPE_LENGTH | amount | 6 | 0 | 110611.91756312 1; 207113.822917066 1; 199270.560893751 1; 270778.668019454 1 |
| SHAPE_AREA | amount | 6 | 0 | 277479127.395668 1; 512733360.383353 1; 909383893.636624 1; 2346845051.28752 1 |
| INTID | category | 6 | 0 | 202 1; 128 1; 135 1; 127 1 |
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:10:35.27964 6 |
| SOURCE_RUN_ID | audit | 1 | 0 | 92cc1ff1-558d-4d8a-9be2-7 6 |
| SRC_SHA256 | who | 1 | 0 | 61ce479eee9ffe515265d0ef3 6 |
