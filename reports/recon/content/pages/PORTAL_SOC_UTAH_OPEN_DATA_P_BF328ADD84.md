# PORTAL_SOC_UTAH_OPEN_DATA_P_BF328ADD84

rows 116  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 272.2K | 84.53M | 1.36B | 1.44B | 23.47B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.7K | 7.6K | 9.3K | 440.4K |

## who

SRC_SHA256 by rows
       116  ee9fe6604931d87a94ed5bfcde152dae9f5d601c5c869c7c2b8305563f83d13f

SRC_SHA256 by dollars
      23.47B      116 rows  ee9fe6604931d87a94ed5bfcde152dae9f5d601c5c869c7c2b8305563f83

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  ee9fe6604931d87a94ed5bfcde152dae9f5d601c  2026:23.47B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 81 2; 139883 2; 19401 2; 65187 2 |
| ESTABLISHMENTS | other | 107 | 0 | 65 2; 316 2; 2170 2; 500 2 |
| PAYROLL | amount | 112 | 0 | 1717091 2; 1105071442 2; 340898928 2; 1074446817 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 7066 2; 4173 2; 2633 2; 5857 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:40:03.50536 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4c5a55e9-e629-4b14-8952-4 116 |
| SRC_SHA256 | who | 1 | 0 | ee9fe6604931d87a94ed5bfcd 116 |
