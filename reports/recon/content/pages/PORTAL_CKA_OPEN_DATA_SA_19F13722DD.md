# PORTAL_CKA_OPEN_DATA_SA_19F13722DD

rows 801  columns 7  scan 2.5s

roles: amount 2, audit 2, date 1, other 2, who 1

## when

INGESTED_AT
  2026       801  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 801 | 0.06 | 250.6K | 45.26M | 138.62M | 2.52B |
| SHAPE__LENGTH | 801 | 6.34 | 2.6K | 52.6K | 109.2K | 5.48M |

## who

SRC_SHA256 by rows
       801  078518e4ddac98eb289d308bea00110875dbdd506358a01f8271e09fcc7d2977

SRC_SHA256 by dollars
       2.52B      801 rows  078518e4ddac98eb289d308bea00110875dbdd506358a01f8271e09fcc7d

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  078518e4ddac98eb289d308bea00110875dbdd50  2026:2.52B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 785 | 0 | 801 5; 800 4; 799 4; 798 4 |
| ORDINANCE | other | 497 | 0 | 202311300889 137; 39443 20; 201611100881 15; 202012100911 13 |
| SHAPE__AREA | amount | 775 | 0 | 9.31640625 5; 274336.8515625 4; 231198.29296875 4; 891752.71875 4 |
| SHAPE__LENGTH | amount | 799 | 0 | 2648.87862759163 5; 2551.17252193098 4; 3791.04418392912 4; 2393.19370399468 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:47:16.86795 801 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9239da31-41a8-4d57-b502-8 801 |
| SRC_SHA256 | who | 1 | 0 | 078518e4ddac98eb289d308be 801 |
