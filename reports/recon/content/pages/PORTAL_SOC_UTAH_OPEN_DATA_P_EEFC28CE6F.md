# PORTAL_SOC_UTAH_OPEN_DATA_P_EEFC28CE6F

rows 118  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 170.3K | 64.24M | 814.95M | 1.09B | 16.84B |
| AVERAGE_MONTHLY_WAGE | 118 | 895 | 2.8K | 7.0K | 7.4K | 353.3K |

## who

SRC_SHA256 by rows
       118  f3bd7ae5fa3f749a9219f54e1e4ebcd4d14fdd4b2221c2f0c2d7da6b6136d8b0

SRC_SHA256 by dollars
      16.84B      118 rows  f3bd7ae5fa3f749a9219f54e1e4ebcd4d14fdd4b2221c2f0c2d7da6b6136

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  f3bd7ae5fa3f749a9219f54e1e4ebcd4d14fdd4b  2026:16.84B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 151 2; 127348 2; 20772 2; 53236 2 |
| ESTABLISHMENTS | other | 106 | 0 | 124 4; 47 3; 1859 2; 441 2 |
| PAYROLL | amount | 112 | 0 | 1634135 2; 814946677 2; 264711934 2; 615896704 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 3607 2; 2952 2; 1904 2; 2133 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:39.72921 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | c918b726-333a-4fe5-bb75-a 118 |
| SRC_SHA256 | who | 1 | 0 | f3bd7ae5fa3f749a9219f54e1 118 |
