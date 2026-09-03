# PORTAL_SOC_UTAH_OPEN_DATA_P_AC57352C67

rows 116  columns 9  scan 3.1s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 397.4K | 87.27M | 1.32B | 1.46B | 23.49B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.2K | 3.7K | 7.4K | 7.8K | 430.5K |

## who

SRC_SHA256 by rows
       116  d640ca4f138000c94c5bd6aec2224772c040f851b49c5381370d3ce36881f7ad

SRC_SHA256 by dollars
      23.49B      116 rows  d640ca4f138000c94c5bd6aec2224772c040f851b49c5381370d3ce36881

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  d640ca4f138000c94c5bd6aec2224772c040f851  2026:23.49B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 109 | 0 | 74 2; 10925 2; 128246 2; 18723 2 |
| ESTABLISHMENTS | other | 108 | 0 | 65 2; 2247 2; 527 2; 11217 2 |
| PAYROLL | amount | 110 | 0 | 1158856 2; 1055572276 2; 307769089 2; 1017864020 2 |
| AVERAGE_MONTHLY_WAGE | amount | 108 | 0 | 5220 2; 2744 2; 5479 2; 4978 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:44:35.44157 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 436ad2ba-63ca-4d66-a897-3 116 |
| SRC_SHA256 | who | 1 | 0 | d640ca4f138000c94c5bd6aec 116 |
