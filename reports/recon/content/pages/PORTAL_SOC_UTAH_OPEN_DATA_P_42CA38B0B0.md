# PORTAL_SOC_UTAH_OPEN_DATA_P_42CA38B0B0

rows 116  columns 9  scan 3.7s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 275.9K | 86.76M | 1.35B | 1.53B | 25.13B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.2K | 3.6K | 10.5K | 11.0K | 457.7K |

## who

SRC_SHA256 by rows
       116  21963b9e53e612212d13ff6a3b69732cb4bc8d0eac27565a70a4b88b5fc06063

SRC_SHA256 by dollars
      25.13B      116 rows  21963b9e53e612212d13ff6a3b69732cb4bc8d0eac27565a70a4b88b5fc0

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  21963b9e53e612212d13ff6a3b69732cb4bc8d0e  2026:25.13B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 29 2; 151593 2; 19081 2; 76427 2 |
| ESTABLISHMENTS | other | 106 | 0 | 35 2; 686 2; 2333 2; 615 2 |
| PAYROLL | amount | 112 | 0 | 287778 2; 1172444943 2; 424991055 2; 1146136119 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3308 2; 2578 2; 7424 2; 4999 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:36.12554 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 770fc819-0477-4ceb-b890-b 116 |
| SRC_SHA256 | who | 1 | 0 | 21963b9e53e612212d13ff6a3 116 |
