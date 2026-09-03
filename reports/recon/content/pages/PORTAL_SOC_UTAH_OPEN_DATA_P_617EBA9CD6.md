# PORTAL_SOC_UTAH_OPEN_DATA_P_617EBA9CD6

rows 118  columns 9  scan 3.1s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       118  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 118 | 190.9K | 62.89M | 874.18M | 1.14B | 17.13B |
| AVERAGE_MONTHLY_WAGE | 118 | 877 | 3.0K | 6.9K | 7.8K | 355.9K |

## who

SRC_SHA256 by rows
       118  bc8030e2ff992e09d0698d8079b47df5a1a54e61f020107558dd8e1bfd2c7aa8

SRC_SHA256 by dollars
      17.13B      118 rows  bc8030e2ff992e09d0698d8079b47df5a1a54e61f020107558dd8e1bfd2c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  bc8030e2ff992e09d0698d8079b47df5a1a54e61  2026:17.13B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 118 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 118 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 115 | 0 | 113 2; 122577 2; 20945 2; 51529 2 |
| ESTABLISHMENTS | other | 106 | 0 | 104 3; 1708 2; 424 2; 7897 2 |
| PAYROLL | amount | 115 | 0 | 1258131 2; 793836893 2; 253413916 2; 699736387 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 3711 2; 2159 2; 3823 2; 4033 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:48:17.19795 118 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1a816467-be4e-44e4-af75-a 118 |
| SRC_SHA256 | who | 1 | 0 | bc8030e2ff992e09d0698d807 118 |
