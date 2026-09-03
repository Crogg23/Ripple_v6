# PORTAL_SOC_UTAH_OPEN_DATA_P_8196274D0D

rows 117  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 232.2K | 79.01M | 1.16B | 1.44B | 22.46B |
| AVERAGE_MONTHLY_WAGE | 117 | 1.1K | 3.4K | 6.4K | 6.5K | 394.4K |

## who

SRC_SHA256 by rows
       117  742a236205fe13933708703445415aab95481bde327fd51011eb62d792c96aaa

SRC_SHA256 by dollars
      22.46B      117 rows  742a236205fe13933708703445415aab95481bde327fd51011eb62d792c9

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  742a236205fe13933708703445415aab95481bde  2026:22.46B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 97 2; 118211 2; 20532 2; 68893 2 |
| ESTABLISHMENTS | other | 106 | 0 | 103 2; 630 2; 2094 2; 491 2 |
| PAYROLL | amount | 112 | 0 | 1154477 2; 929293066 2; 306159140 2; 965834774 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 3967 2; 3669 2; 2620 2; 4970 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:58.50168 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 010e2a69-58f0-4ecc-a59c-1 117 |
| SRC_SHA256 | who | 1 | 0 | 742a236205fe1393370870344 117 |
