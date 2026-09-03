# PORTAL_SOC_UTAH_OPEN_DATA_P_FA2123B348

rows 116  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 298.4K | 84.43M | 1.26B | 1.36B | 22.72B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.4K | 7.4K | 7.7K | 416.0K |

## who

SRC_SHA256 by rows
       116  0a520c7c12790c0bf56216de1659ece2cf38e1f85c642bdbaf189529291288d8

SRC_SHA256 by dollars
      22.72B      116 rows  0a520c7c12790c0bf56216de1659ece2cf38e1f85c642bdbaf1895292912

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  0a520c7c12790c0bf56216de1659ece2cf38e1f8  2026:22.72B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 108 | 0 | 79 2; 141243 2; 18646 2; 67971 2 |
| ESTABLISHMENTS | other | 107 | 0 | 70 3; 377 2; 2228 2; 518 2 |
| PAYROLL | amount | 110 | 0 | 1169182 2; 1203274632 2; 305872514 2; 992235672 2 |
| AVERAGE_MONTHLY_WAGE | amount | 108 | 0 | 4933 3; 2840 2; 5468 2; 4866 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:09.24693 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 58e4f8e5-1211-4685-bd1b-c 116 |
| SRC_SHA256 | who | 1 | 0 | 0a520c7c12790c0bf56216de1 116 |
