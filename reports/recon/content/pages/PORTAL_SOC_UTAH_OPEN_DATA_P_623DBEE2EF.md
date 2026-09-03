# PORTAL_SOC_UTAH_OPEN_DATA_P_623DBEE2EF

rows 118  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 254.8K | 70.12M | 946.72M | 1.23B | 19.64B |
| AVERAGE_MONTHLY_WAGE | 118 | 976 | 2.9K | 6.6K | 10.9K | 372.7K |

## who

SRC_SHA256 by rows
       118  1f76afe8c82725b53fdb470429c1bd81a6d8e0d22008c2c050e92c1b78352c56

SRC_SHA256 by dollars
      19.64B      118 rows  1f76afe8c82725b53fdb470429c1bd81a6d8e0d22008c2c050e92c1b7835

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  1f76afe8c82725b53fdb470429c1bd81a6d8e0d2  2026:19.64B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 474 2; 124313 2; 19367 2; 60824 2 |
| ESTABLISHMENTS | other | 112 | 0 | 211 2; 2005 2; 461 2; 9932 2 |
| PAYROLL | amount | 115 | 0 | 3634845 2; 946721804 2; 261960651 2; 753367369 2 |
| AVERAGE_MONTHLY_WAGE | amount | 114 | 0 | 2556 2; 2539 2; 4509 2; 4129 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:25.45599 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0e9806f7-57fb-47a1-ac5a-3 118 |
| SRC_SHA256 | who | 1 | 0 | 1f76afe8c82725b53fdb47042 118 |
