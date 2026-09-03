# PORTAL_SOC_UTAH_OPEN_DATA_P_A8921E729F

rows 117  columns 9  scan 3.1s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 108.8K | 59.56M | 773.93M | 1.13B | 16.52B |
| AVERAGE_MONTHLY_WAGE | 117 | 844 | 2.8K | 5.6K | 6.3K | 337.6K |

## who

SRC_SHA256 by rows
       117  69d870dd352b2d97304287407f50ca463bf8f557dfb63ab545106eb71c29f4c5

SRC_SHA256 by dollars
      16.52B      117 rows  69d870dd352b2d97304287407f50ca463bf8f557dfb63ab545106eb71c29

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  69d870dd352b2d97304287407f50ca463bf8f557  2026:16.52B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 111 2; 120856 2; 21846 2; 49785 2 |
| ESTABLISHMENTS | other | 106 | 0 | 99 2; 1586 2; 415 2; 7239 2 |
| PAYROLL | amount | 114 | 0 | 1024009 2; 766844978 2; 298421713 2; 654481765 2 |
| AVERAGE_MONTHLY_WAGE | amount | 113 | 0 | 3075 2; 2115 2; 4553 2; 4382 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:24.81196 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7cbbd094-dae2-4245-9921-1 117 |
| SRC_SHA256 | who | 1 | 0 | 69d870dd352b2d97304287407 117 |
