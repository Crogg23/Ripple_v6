# PORTAL_SOC_UTAH_OPEN_DATA_P_79CFD825BF

rows 116  columns 9  scan 2.6s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 424.0K | 87.47M | 1.44B | 1.49B | 25.42B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.2K | 3.6K | 7.8K | 8.1K | 432.3K |

## who

SRC_SHA256 by rows
       116  6fc13330f905a9d5300a441a2576a4a90c317f735f0528d1b119684970981a4f

SRC_SHA256 by dollars
      25.42B      116 rows  6fc13330f905a9d5300a441a2576a4a90c317f735f0528d1b11968497098

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  6fc13330f905a9d5300a441a2576a4a90c317f73  2026:25.42B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 56 2; 133401 2; 19236 2; 78489 2 |
| ESTABLISHMENTS | other | 106 | 0 | 45 2; 156 2; 696 2; 2369 2 |
| PAYROLL | amount | 108 | 0 | 459013 2; 1144816873 2; 332340111 2; 1184708626 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 2732 2; 2861 2; 5759 2; 5031 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:37:12.30722 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | b4d7e2b1-f155-4bd6-93dc-e 116 |
| SRC_SHA256 | who | 1 | 0 | 6fc13330f905a9d5300a441a2 116 |
