# PORTAL_SOC_UTAH_OPEN_DATA_P_4DA2A1E62F

rows 118  columns 9  scan 2.9s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 174.1K | 75.59M | 1.08B | 1.36B | 22.30B |
| AVERAGE_MONTHLY_WAGE | 118 | 1.0K | 3.4K | 7.5K | 8.3K | 407.7K |

## who

SRC_SHA256 by rows
       118  fef2c04737a21fee361ae2c0fe9b613817794a8ec8bd89a893a840a477f06cd2

SRC_SHA256 by dollars
      22.30B      118 rows  fef2c04737a21fee361ae2c0fe9b613817794a8ec8bd89a893a840a477f0

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  fef2c04737a21fee361ae2c0fe9b613817794a8e  2026:22.30B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 120 2; 131077 2; 19571 2; 63215 2 |
| ESTABLISHMENTS | other | 108 | 0 | 150 2; 2065 2; 483 2; 10389 2 |
| PAYROLL | amount | 113 | 0 | 1517256 2; 942195712 2; 340626486 2; 942259215 2 |
| AVERAGE_MONTHLY_WAGE | amount | 108 | 0 | 4215 2; 2396 2; 5802 2; 4969 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:40:23.48574 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 91c5e259-27ae-4ac5-910c-b 118 |
| SRC_SHA256 | who | 1 | 0 | fef2c04737a21fee361ae2c0f 118 |
