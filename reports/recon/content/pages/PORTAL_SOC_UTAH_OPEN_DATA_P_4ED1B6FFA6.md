# PORTAL_SOC_UTAH_OPEN_DATA_P_4ED1B6FFA6

rows 116  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 250.3K | 72.86M | 1.02B | 1.38B | 21.26B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.0K | 3.2K | 7.7K | 9.0K | 390.5K |

## who

SRC_SHA256 by rows
       116  9d20592d92d87ae21b4ae6bd5360dfec4565a14baaaa417c1f0a1cc15271b514

SRC_SHA256 by dollars
      21.26B      116 rows  9d20592d92d87ae21b4ae6bd5360dfec4565a14baaaa417c1f0a1cc15271

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  9d20592d92d87ae21b4ae6bd5360dfec4565a14b  2026:21.26B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 128 2; 131689 2; 19887 2; 63437 2 |
| ESTABLISHMENTS | other | 107 | 0 | 113 2; 32 2; 163 2; 1990 2 |
| PAYROLL | amount | 113 | 0 | 1369149 2; 920699824 2; 325977962 2; 842269222 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3565 2; 1881 2; 2330 2; 5464 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:20.77090 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 611dee7c-e68c-46b5-afdc-8 116 |
| SRC_SHA256 | who | 1 | 0 | 9d20592d92d87ae21b4ae6bd5 116 |
