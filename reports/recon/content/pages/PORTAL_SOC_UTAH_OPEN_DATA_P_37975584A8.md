# PORTAL_SOC_UTAH_OPEN_DATA_P_37975584A8

rows 116  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 262.3K | 77.68M | 1.11B | 1.46B | 22.33B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.4K | 7.9K | 9.2K | 404.0K |

## who

SRC_SHA256 by rows
       116  0953dadf4dca6b46cf154bb50bc82c3e04ce4a1f3466b22b61b105dd2864fa2c

SRC_SHA256 by dollars
      22.33B      116 rows  0953dadf4dca6b46cf154bb50bc82c3e04ce4a1f3466b22b61b105dd2864

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  0953dadf4dca6b46cf154bb50bc82c3e04ce4a1f  2026:22.33B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 80 2; 134835 2; 20407 2; 67394 2 |
| ESTABLISHMENTS | other | 109 | 0 | 497 3; 331 3; 109 2; 2042 2 |
| PAYROLL | amount | 113 | 0 | 1168294 2; 999543963 2; 347608857 2; 917596332 2 |
| AVERAGE_MONTHLY_WAGE | amount | 113 | 0 | 4868 2; 2471 2; 5678 2; 4538 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:52:09.46323 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5457dd01-d2f8-4d25-9019-e 116 |
| SRC_SHA256 | who | 1 | 0 | 0953dadf4dca6b46cf154bb50 116 |
