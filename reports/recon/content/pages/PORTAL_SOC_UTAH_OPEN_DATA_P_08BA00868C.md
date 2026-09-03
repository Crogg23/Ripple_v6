# PORTAL_SOC_UTAH_OPEN_DATA_P_08BA00868C

rows 118  columns 9  scan 2.6s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 185.2K | 71.02M | 980.04M | 1.23B | 20.13B |
| AVERAGE_MONTHLY_WAGE | 118 | 947 | 3.2K | 8.4K | 8.9K | 387.2K |

## who

SRC_SHA256 by rows
       118  bc0fbe3fdfe72de861bbff6b7c6857106c2beeb28d9a18037f25aa9857ae4a20

SRC_SHA256 by dollars
      20.13B      118 rows  bc0fbe3fdfe72de861bbff6b7c6857106c2beeb28d9a18037f25aa9857ae

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  bc0fbe3fdfe72de861bbff6b7c6857106c2beeb2  2026:20.13B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 243 2; 128469 2; 21144 2; 57598 2 |
| ESTABLISHMENTS | other | 114 | 0 | 167 2; 1927 2; 449 2; 9612 2 |
| PAYROLL | amount | 114 | 0 | 2318574 2; 883637549 2; 298271066 2; 834219741 2 |
| AVERAGE_MONTHLY_WAGE | amount | 112 | 0 | 3180 2; 2109 2; 2293 2; 4702 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:37:18.78918 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 670fc49e-9890-473c-b2fe-b 118 |
| SRC_SHA256 | who | 1 | 0 | bc0fbe3fdfe72de861bbff6b7 118 |
