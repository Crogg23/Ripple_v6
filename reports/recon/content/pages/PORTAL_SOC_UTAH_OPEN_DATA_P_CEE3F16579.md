# PORTAL_SOC_UTAH_OPEN_DATA_P_CEE3F16579

rows 116  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 353.4K | 86.24M | 1.42B | 1.50B | 25.12B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.2K | 3.5K | 7.9K | 10.4K | 433.7K |

## who

SRC_SHA256 by rows
       116  f8fea0116504043867dd8926e7c4b49bfe8d634d2062e48f4632beeee17bbb26

SRC_SHA256 by dollars
      25.12B      116 rows  f8fea0116504043867dd8926e7c4b49bfe8d634d2062e48f4632beeee17b

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  f8fea0116504043867dd8926e7c4b49bfe8d634d  2026:25.12B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 36 2; 147495 2; 19086 2; 78693 2 |
| ESTABLISHMENTS | other | 110 | 0 | 35 2; 220 2; 2343 2; 636 2 |
| PAYROLL | amount | 113 | 0 | 362664 2; 1244675586 2; 350623902 2; 1174316170 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3358 2; 2813 2; 2514 2; 6124 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:50:38.67296 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8fe755fe-66cc-4784-9d1e-2 116 |
| SRC_SHA256 | who | 1 | 0 | f8fea0116504043867dd8926e 116 |
