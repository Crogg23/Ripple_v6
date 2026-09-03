# PORTAL_CKA_SAN_JOSE_OPEN_DA_4B62EE3E47

rows 312  columns 12  scan 3.5s

roles: amount 1, audit 2, category 3, date 1, other 3, who 3

## when

INGESTED_AT
  2026       312  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 312 | 4.75 | 472.39 | 39.2K | 63.4K | 748.0K |

## who

STATUS by rows
       312  Active

STATUS by dollars
      748.0K      312 rows  Active

CREATIONDATE by rows
       312  1900/01/01 00:00:00+00

CREATIONDATE by dollars
      748.0K      312 rows  1900/01/01 00:00:00+00

SRC_SHA256 by rows
       312  f8dd86497b98ed5d2bb4f1ae906d491cf7ed2d35eb14e56424d276ecb6954205

SRC_SHA256 by dollars
      748.0K      312 rows  f8dd86497b98ed5d2bb4f1ae906d491cf7ed2d35eb14e56424d276ecb695

## who x when

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Active                                    2026:748.0K

CREATIONDATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  1900/01/01 00:00:00+00                    2026:748.0K

## what

NAME: Light Rail 54%, Union Pacific 35%, Caltrain 8%, BART 3%

RAILTYPE: Lightrail 54%, Rail 46%

LASTUPDATE: 2019/09/04 00:43:05+00 99%, 2019/11/16 00:18:14+00 1%, 2019/10/02 22:46:15+00 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 308 | 0 | 745 2; 744 2; 743 2; 742 2 |
| RAILID | other | 307 | 0 | 449 2; 448 2; 447 2; 446 2 |
| INTID | other | 307 | 0 | 449 2; 448 2; 447 2; 446 2 |
| NAME | category | 4 | 0 | Light Rail 170; Union Pacific 108; Caltrain 25; BART 9 |
| RAILTYPE | category | 2 | 0 | Lightrail 170; Rail 142 |
| STATUS | who | 1 | 0 | Active 312 |
| LASTUPDATE | category | 3 | 0 | 2019/09/04 00:43:05+00 309; 2019/11/16 00:18:14+00 2; 2019/10/02 22:46:15+00 1 |
| SHAPE_LENGTH | amount | 306 | 0 | 1582.91931414975 2; 1215.41738112794 2; 25374.5622525034 2; 21777.0806099493 2 |
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 312 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:39:31.92209 312 |
| SOURCE_RUN_ID | audit | 1 | 0 | a703fa08-e6ad-4b9c-8cb8-b 312 |
| SRC_SHA256 | who | 1 | 0 | f8dd86497b98ed5d2bb4f1ae9 312 |
