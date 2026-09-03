# PORTAL_SOC_UTAH_OPEN_DATA_P_1C0C156DA7

rows 117  columns 9  scan 2.9s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 270.3K | 87.25M | 1.22B | 1.53B | 24.04B |
| AVERAGE_MONTHLY_WAGE | 117 | 1.1K | 3.6K | 7.8K | 9.2K | 427.8K |

## who

SRC_SHA256 by rows
       117  3ce8e7abd33ea3d4aae44f70a7c19e1415069c3566a75b0b7c4581d5e4ed4987

SRC_SHA256 by dollars
      24.04B      117 rows  3ce8e7abd33ea3d4aae44f70a7c19e1415069c3566a75b0b7c4581d5e4ed

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  3ce8e7abd33ea3d4aae44f70a7c19e1415069c35  2026:24.04B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 106 2; 137598 2; 20479 2; 68936 2 |
| ESTABLISHMENTS | other | 107 | 0 | 107 3; 333 3; 2109 2; 506 2 |
| PAYROLL | amount | 112 | 0 | 1259590 2; 1082961316 2; 327154488 2; 1104028427 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 3961 2; 2412 2; 2623 2; 5325 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:48:53.17916 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | d95e7ee5-ad03-4c81-9db3-0 117 |
| SRC_SHA256 | who | 1 | 0 | 3ce8e7abd33ea3d4aae44f70a 117 |
