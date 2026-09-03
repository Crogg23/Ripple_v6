# PORTAL_CKA_OPEN_DATA_SA_33003C2E61

rows 48  columns 8  scan 2.6s

roles: amount 1, audit 2, category 2, date 1, other 2, who 1

## when

INGESTED_AT
  2026        48  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYROLLEDBUSINESSLOCATIONS | 48 | 46.1K | 103.2K | 211.9K | 212.1K | 5.36M |

## who

SRC_SHA256 by rows
        48  53fb95351883f9a7b70e588ce31062290d504caa565e0db2c19fb1c114bfb1a8

SRC_SHA256 by dollars
       5.36M       48 rows  53fb95351883f9a7b70e588ce31062290d504caa565e0db2c19fb1c114bf

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYROLLEDBUSINESSLOCATIONS
  53fb95351883f9a7b70e588ce31062290d504caa  2026:5.36M

## what

CITY: Austin 12%, Dallas 12%, Jacksonville 12%, Houston 12%, Charlotte 12%, Phoenix 12%, San Diego 12%, San Antonio 12%

YEAR: 2024 17%, 2023 17%, 2022 17%, 2021 17%, 2020 17%, 2019 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CITY | category | 8 | 0 | Austin 6; Dallas 6; Jacksonville 6; Houston 6 |
| YEAR | category | 6 | 0 | 2024 8; 2023 8; 2022 8; 2021 8 |
| NAICS | other | 1 | 0 | ALL 48 |
| DESCRIPTION | other | 1 | 0 | Total 48 |
| PAYROLLEDBUSINESSLOCATIONS | amount | 48 | 0 | 76679.000000000 1; 211701.000000000 1; 55685.000000000 1; 177389.000000000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:01:14.51566 48 |
| SOURCE_RUN_ID | audit | 1 | 0 | 97cd8672-1621-4672-9e2b-4 48 |
| SRC_SHA256 | who | 1 | 0 | 53fb95351883f9a7b70e588ce 48 |
