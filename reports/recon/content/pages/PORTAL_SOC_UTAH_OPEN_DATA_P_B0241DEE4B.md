# PORTAL_SOC_UTAH_OPEN_DATA_P_B0241DEE4B

rows 116  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 252.5K | 79.03M | 1.17B | 1.35B | 21.62B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.3K | 7.9K | 9.3K | 398.6K |

## who

SRC_SHA256 by rows
       116  ac3986f5aaa5a3694e6aa591a03253f1f5c92ddfa8d6934ccc4a2dd373d73c7c

SRC_SHA256 by dollars
      21.62B      116 rows  ac3986f5aaa5a3694e6aa591a03253f1f5c92ddfa8d6934ccc4a2dd373d7

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  ac3986f5aaa5a3694e6aa591a03253f1f5c92ddf  2026:21.62B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 28 2; 137994 2; 19688 2; 67141 2 |
| ESTABLISHMENTS | other | 107 | 0 | 41 3; 416 2; 2106 2; 480 2 |
| PAYROLL | amount | 110 | 0 | 333098 2; 1057964368 2; 333176384 2; 944990313 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3965 2; 2556 2; 5641 2; 4692 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:45:03.36953 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2544e1ac-f496-4bfb-9c98-0 116 |
| SRC_SHA256 | who | 1 | 0 | ac3986f5aaa5a3694e6aa591a 116 |
