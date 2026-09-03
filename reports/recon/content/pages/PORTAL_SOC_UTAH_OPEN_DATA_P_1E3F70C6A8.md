# PORTAL_SOC_UTAH_OPEN_DATA_P_1E3F70C6A8

rows 116  columns 9  scan 3.0s

roles: amount 2, audit 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       116  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLL | 116 | 339.5K | 77.69M | 1.09B | 1.42B | 22.55B |
| AVERAGE_MONTHLY_WAGE | 116 | 1.1K | 3.2K | 6.7K | 6.8K | 388.1K |

## who

SRC_SHA256 by rows
       116  6a0b76e0697d708d61aa55bb1edcb5fdc15a47862903067cdaac5f9416ef1484

SRC_SHA256 by dollars
      22.55B      116 rows  6a0b76e0697d708d61aa55bb1edcb5fdc15a47862903067cdaac5f9416ef

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLL
  6a0b76e0697d708d61aa55bb1edcb5fdc15a4786  2026:22.55B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDUSTRY_SECTOR | other | 116 | 0 | Management of Companies a 2; Utilities 2; Unclassified 1; Unclassified establishmen 1 |
| NAICS_SECTOR | other | 116 | 0 | 999 1; 99 1; 926 1; 925 1 |
| AVERAGE_EMPLOYMENT | other | 113 | 0 | 92 2; 129938 2; 20378 2; 68263 2 |
| ESTABLISHMENTS | other | 106 | 0 | 110 2; 2060 2; 500 2; 10517 2 |
| PAYROLL | amount | 107 | 0 | 1279009 2; 1079970162 2; 297335691 2; 1012524050 2 |
| AVERAGE_MONTHLY_WAGE | amount | 109 | 0 | 4634 2; 2770 2; 4864 2; 4944 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:04.79565 116 |
| SOURCE_RUN_ID | audit | 1 | 0 | e95c2f85-46fd-4da5-a1f5-5 116 |
| SRC_SHA256 | who | 1 | 0 | 6a0b76e0697d708d61aa55bb1 116 |
