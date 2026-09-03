# PORTAL_SOC_UTAH_OPEN_DATA_P_36BE408253

rows 117  columns 9  scan 2.8s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 94.5K | 56.63M | 749.62M | 1.11B | 15.43B |
| AVERAGE_MONTHLY_WAGE | 117 | 839 | 2.5K | 5.1K | 5.2K | 311.1K |

## who

SRC_SHA256 by rows
       117  337b890c4d8fad924f7e0cc1c16821076421010c0a23629a47c1521972fa81fe

SRC_SHA256 by dollars
      15.43B      117 rows  337b890c4d8fad924f7e0cc1c16821076421010c0a23629a47c1521972fa

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  337b890c4d8fad924f7e0cc1c16821076421010c  2026:15.43B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 114 | 0 | 208 2; 115950 2; 22050 2; 51188 2 |
| ESTABLISHMENTS | other | 104 | 0 | 305 3; 136 2; 772 2; 1564 2 |
| PAYROLL | amount | 114 | 0 | 1688961 2; 749619885 2; 238903456 2; 566104260 2 |
| AVERAGE_MONTHLY_WAGE | amount | 110 | 0 | 2707 2; 2155 2; 3612 2; 3686 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:58.58631 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2aa4d48f-483a-4590-bb56-d 117 |
| SRC_SHA256 | who | 1 | 0 | 337b890c4d8fad924f7e0cc1c 117 |
