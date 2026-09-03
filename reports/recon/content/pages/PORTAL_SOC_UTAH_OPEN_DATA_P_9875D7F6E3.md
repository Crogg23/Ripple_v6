# PORTAL_SOC_UTAH_OPEN_DATA_P_9875D7F6E3

rows 118  columns 9  scan 3.4s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 158.5K | 66.24M | 808.00M | 1.09B | 16.78B |
| AVERAGE_MONTHLY_WAGE | 118 | 890 | 2.8K | 5.8K | 6.4K | 341.3K |

## who

SRC_SHA256 by rows
       118  785a14e9e37ff8bdca46cfee2c38931b0066f88bd73688a648b6081ccf1859c3

SRC_SHA256 by dollars
      16.78B      118 rows  785a14e9e37ff8bdca46cfee2c38931b0066f88bd73688a648b6081ccf18

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  785a14e9e37ff8bdca46cfee2c38931b0066f88b  2026:16.78B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 155 2; 107821 2; 20865 2; 51184 2 |
| ESTABLISHMENTS | other | 107 | 0 | 115 2; 81 2; 1827 2; 429 2 |
| PAYROLL | amount | 113 | 0 | 1275866 2; 729402051 2; 231849194 2; 617404248 2 |
| AVERAGE_MONTHLY_WAGE | amount | 114 | 0 | 2744 2; 2255 2; 3704 2; 4021 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:50:02.29098 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | d9fb3b47-cfd4-4872-baf5-b 118 |
| SRC_SHA256 | who | 1 | 0 | 785a14e9e37ff8bdca46cfee2 118 |
