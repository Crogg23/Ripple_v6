# PORTAL_SOC_UTAH_OPEN_DATA_P_F9EFC33574

rows 116  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 221.2K | 81.92M | 1.21B | 1.36B | 22.13B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.4K | 9.7K | 11.1K | 427.1K |

## who

SRC_SHA256 by rows
       116  a1ded21fe2a11e018288463e3434ac5680921709c4af885445b3ed843c011e2d

SRC_SHA256 by dollars
      22.13B      116 rows  a1ded21fe2a11e018288463e3434ac5680921709c4af885445b3ed843c01

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  a1ded21fe2a11e018288463e3434ac5680921709  2026:22.13B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 110 | 0 | 76 2; 145082 2; 18422 2; 66936 2 |
| ESTABLISHMENTS | other | 112 | 0 | 70 2; 2219 2; 512 2; 10803 2 |
| PAYROLL | amount | 112 | 0 | 954325 2; 1104536274 2; 360048272 2; 968163810 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 4186 2; 2538 2; 6515 2; 4821 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:47:14.47074 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | 50d9193b-c3a7-4f5a-b358-d 116 |
| SRC_SHA256 | who | 1 | 0 | a1ded21fe2a11e018288463e3 116 |
