# PORTAL_SOC_UTAH_OPEN_DATA_P_B84814B0C6

rows 117  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 20.5K | 83.72M | 1.36B | 1.44B | 23.80B |
| AVERAGE_MONTHLY_WAGE | 117 | 1.1K | 3.4K | 7.1K | 7.2K | 417.7K |

## who

SRC_SHA256 by rows
       117  5aae2bfc0e05aacedac579b67870679f7be48ec683622a58d2dc35a6aae2004e

SRC_SHA256 by dollars
      23.80B      117 rows  5aae2bfc0e05aacedac579b67870679f7be48ec683622a58d2dc35a6aae2

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  5aae2bfc0e05aacedac579b67870679f7be48ec6  2026:23.80B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 40 2; 144369 2; 19222 2; 72033 2 |
| ESTABLISHMENTS | other | 112 | 0 | 33 2; 2283 2; 554 2; 11633 2 |
| PAYROLL | amount | 110 | 0 | 400578 2; 1216980653 2; 329309119 2; 1087012429 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 3338 2; 2810 2; 5711 2; 5030 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:44:46.79553 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | e5069a94-7067-487c-9aef-4 117 |
| SRC_SHA256 | who | 1 | 0 | 5aae2bfc0e05aacedac579b67 117 |
