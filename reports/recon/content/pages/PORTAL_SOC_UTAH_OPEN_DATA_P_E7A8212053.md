# PORTAL_SOC_UTAH_OPEN_DATA_P_E7A8212053

rows 116  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 327.2K | 92.95M | 1.52B | 1.58B | 26.82B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.2K | 3.7K | 9.6K | 10.0K | 464.9K |

## who

SRC_SHA256 by rows
       116  4238e078a671add777e85381ef76b7be40d48aac74e6522aa359c86be03e81f1

SRC_SHA256 by dollars
      26.82B      116 rows  4238e078a671add777e85381ef76b7be40d48aac74e6522aa359c86be03e

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  4238e078a671add777e85381ef76b7be40d48aac  2026:26.82B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 42 2; 151279 2; 18999 2; 75034 2 |
| ESTABLISHMENTS | other | 109 | 0 | 36 3; 2340 2; 579 2; 12138 2 |
| PAYROLL | amount | 112 | 0 | 375370 2; 1221547586 2; 420342560 2; 1286025818 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 2979 2; 2692 2; 7375 2; 5713 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:45.09204 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | b7223090-b19e-4ea8-8a9e-b 116 |
| SRC_SHA256 | who | 1 | 0 | 4238e078a671add777e85381e 116 |
