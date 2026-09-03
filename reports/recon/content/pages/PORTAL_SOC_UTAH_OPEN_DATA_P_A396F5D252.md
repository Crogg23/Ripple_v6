# PORTAL_SOC_UTAH_OPEN_DATA_P_A396F5D252

rows 116  columns 9  scan 2.5s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 325.5K | 75.93M | 1.01B | 1.36B | 21.88B |
| AVERAGE_MONTHLY_WAGE | 116 | 990 | 3.2K | 7.1K | 9.7K | 385.5K |

## who

SRC_SHA256 by rows
       116  5a7fb97afeeae14a2afecc714f58af034b5c03677615e8292a6da47ba5177b2b

SRC_SHA256 by dollars
      21.88B      116 rows  5a7fb97afeeae14a2afecc714f58af034b5c03677615e8292a6da47ba517

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  5a7fb97afeeae14a2afecc714f58af034b5c0367  2026:21.88B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 129 3; 126502 2; 20206 2; 64842 2 |
| ESTABLISHMENTS | other | 107 | 0 | 115 2; 2019 2; 482 2; 10043 2 |
| PAYROLL | amount | 110 | 0 | 1677241 2; 987899422 2; 288974519 2; 865263476 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 4334 2; 2804 2; 2603 2; 4767 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:28.60408 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | a06a2190-3a0f-413f-b512-7 116 |
| SRC_SHA256 | who | 1 | 0 | 5a7fb97afeeae14a2afecc714 116 |
