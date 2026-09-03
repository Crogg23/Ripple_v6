# PORTAL_SOC_UTAH_OPEN_DATA_P_A6AF8166D5

rows 116  columns 9  scan 2.5s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 387.4K | 79.98M | 1.09B | 1.38B | 21.82B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.1K | 6.1K | 6.1K | 378.9K |

## who

SRC_SHA256 by rows
       116  f9d25c8584266498fa43c876e7de6af7ee70ec17ff8ab8f3a1186f3664e1b7d2

SRC_SHA256 by dollars
      21.82B      116 rows  f9d25c8584266498fa43c876e7de6af7ee70ec17ff8ab8f3a1186f3664e1

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  f9d25c8584266498fa43c876e7de6af7ee70ec17  2026:21.82B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 188 2; 114639 2; 20627 2; 65299 2 |
| ESTABLISHMENTS | other | 106 | 0 | 122 2; 2031 2; 492 2; 10238 2 |
| PAYROLL | amount | 113 | 0 | 1734033 2; 868781692 2; 284826112 2; 881474902 2 |
| AVERAGE_MONTHLY_WAGE | amount | 106 | 0 | 3075 2; 3507 2; 2526 2; 4603 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:49:29.79607 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2f9936c3-6cd2-4918-8956-1 116 |
| SRC_SHA256 | who | 1 | 0 | f9d25c8584266498fa43c876e 116 |
