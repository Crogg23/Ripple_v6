# PORTAL_SOC_UTAH_OPEN_DATA_P_CAEBCFEEAF

rows 117  columns 9  scan 2.6s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       117  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 117 | 141.9K | 58.41M | 700.02M | 1.11B | 15.30B |
| AVERAGE_MONTHLY_WAGE | 117 | 833 | 2.6K | 7.1K | 7.2K | 329.2K |

## who

SRC_SHA256 by rows
       117  b5cdf5f6387c60e06ede9ecbfa3e617bddc6ddbc2795f4cf17d03ca3ae46d44d

SRC_SHA256 by dollars
      15.30B      117 rows  b5cdf5f6387c60e06ede9ecbfa3e617bddc6ddbc2795f4cf17d03ca3ae46

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  b5cdf5f6387c60e06ede9ecbfa3e617bddc6ddbc  2026:15.30B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 117 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 117 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 112 | 0 | 182 2; 118866 2; 22007 2; 51266 2 |
| ESTABLISHMENTS | other | 108 | 0 | 420 3; 136 2; 1545 2; 6801 2 |
| PAYROLL | amount | 112 | 0 | 1996532 2; 700015524 2; 254123562 2; 565688547 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 3657 2; 1963 2; 3849 2; 3678 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:45:31.24978 117 |
| SOURCE_RUN_ID | audit | 1 | 0 | c9935506-d2d6-4a5d-ae7d-0 117 |
| SRC_SHA256 | who | 1 | 0 | b5cdf5f6387c60e06ede9ecbf 117 |
