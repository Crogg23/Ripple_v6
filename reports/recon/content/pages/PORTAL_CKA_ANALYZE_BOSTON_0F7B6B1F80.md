# PORTAL_CKA_ANALYZE_BOSTON_0F7B6B1F80

rows 26  columns 10  scan 3.7s

roles: amount 4, audit 2, category 2, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        26  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 26 | 15.64 | 723.37 | 4.4K | 4.7K | 31.3K |
| SQMILES | 26 | 0.02 | 1.13 | 6.84 | 7.29 | 48.91 |
| SHAPE_LENGTH | 26 | 0.01 | 0.12 | 0.38 | 0.39 | 3.52 |
| SHAPE_AREA | 26 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
        26  4d6b37c23410da1f784d9e53705182ced4eb12aa524d6a9e85cace008b7fdb46

SRC_SHA256 by dollars
       31.3K       26 rows  4d6b37c23410da1f784d9e53705182ced4eb12aa524d6a9e85cace008b7f

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  4d6b37c23410da1f784d9e53705182ced4eb12aa  2026:31.3K

## what

NAME: Harbor Islands 8%, Allston 8%, South Boston 8%, South Boston Waterfront 8%, Dorchester 8%, Mattapan 8%, Hyde Park 8%, West Roxbury 8%, Brighton 8%, Fenway 8%, Downtown 8%, Beacon Hill 8%

NEIGHBORHOOD_ID: 22 8%, 24 8%, 17 8%, 29 8%, 6 8%, 12 8%, 10 8%, 19 8%, 25 8%, 34 8%, 7 8%, 30 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | category | 26 | 0 | Harbor Islands 1; Allston 1; South Boston 1; South Boston Waterfront 1 |
| ACRES | amount | 26 | 0 | 824.888657940000030 1; 998.534478690000014 1; 1439.888807309999947 1; 621.843523730000015 1 |
| NEIGHBORHOOD_ID | category | 26 | 0 | 22 1; 24 1; 17 1; 29 1 |
| SQMILES | amount | 25 | 0 | 0.620000000000000 2; 1.290000000000000 1; 1.560000000000000 1; 2.250000000000000 1 |
| SHAPE_LENGTH | amount | 26 | 0 | 0.297930934951251 1; 0.122310950454451 1; 0.212398700706368 1; 0.125951270258673 1 |
| SHAPE_AREA | amount | 26 | 0 | 0.000364630871659 1; 0.000441599797148 1; 0.000636552305208 1; 0.000274956643860 1 |
| SHAPE_WKT | empty | 1 | 26 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:18:46.58111 26 |
| SOURCE_RUN_ID | audit | 1 | 0 | 24fe68f9-66b9-4e1b-b857-1 26 |
| SRC_SHA256 | who | 1 | 0 | 4d6b37c23410da1f784d9e537 26 |
