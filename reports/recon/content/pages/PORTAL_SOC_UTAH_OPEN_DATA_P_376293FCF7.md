# PORTAL_SOC_UTAH_OPEN_DATA_P_376293FCF7

rows 118  columns 9  scan 2.4s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 183.7K | 74.16M | 915.62M | 1.19B | 18.65B |
| AVERAGE_MONTHLY_WAGE | 118 | 962 | 3.1K | 6.5K | 6.6K | 365.6K |

## who

SRC_SHA256 by rows
       118  7d49a229b483d4d4371fbf9b95368916f5659a21a48d5e666beab3d05e58d8c2

SRC_SHA256 by dollars
      18.65B      118 rows  7d49a229b483d4d4371fbf9b95368916f5659a21a48d5e666beab3d05e58

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  7d49a229b483d4d4371fbf9b95368916f5659a21  2026:18.65B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 259 3; 110542 2; 20999 2; 55542 2 |
| ESTABLISHMENTS | other | 108 | 0 | 313 3; 168 2; 32 2; 1912 2 |
| PAYROLL | amount | 112 | 0 | 2415194 2; 782951549 2; 268464848 2; 707053205 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 3108 2; 1663 2; 3414 2; 2361 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:39.56331 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 873a8a5c-7a5a-4c0e-bbb3-0 118 |
| SRC_SHA256 | who | 1 | 0 | 7d49a229b483d4d4371fbf9b9 118 |
