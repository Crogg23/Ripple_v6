# PORTAL_SOC_UTAH_OPEN_DATA_P_5D4CAAD7FB

rows 116  columns 9  scan 3.7s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 350.5K | 90.26M | 1.56B | 1.60B | 27.41B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.2K | 3.7K | 9.5K | 10.5K | 466.6K |

## who

SRC_SHA256 by rows
       116  3badbbc618633ff5fb8c020d02e6723c8c8f3f40b6ba3c03f09ada7685135048

SRC_SHA256 by dollars
      27.41B      116 rows  3badbbc618633ff5fb8c020d02e6723c8c8f3f40b6ba3c03f09ada768513

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  3badbbc618633ff5fb8c020d02e6723c8c8f3f40  2026:27.41B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 92 2; 156517 2; 19694 2; 80919 2 |
| ESTABLISHMENTS | other | 105 | 0 | 64 3; 525 2; 81 2; 564 2 |
| PAYROLL | amount | 112 | 0 | 1020661 2; 1274403376 2; 381580339 2; 1389102506 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 2714 3; 3698 2; 6458 2; 5722 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:47.64703 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | a79157fd-25aa-4ea8-b188-f 116 |
| SRC_SHA256 | who | 1 | 0 | 3badbbc618633ff5fb8c020d0 116 |
