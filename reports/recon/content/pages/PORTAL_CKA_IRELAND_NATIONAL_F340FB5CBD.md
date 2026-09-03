# PORTAL_CKA_IRELAND_NATIONAL_F340FB5CBD

rows 6.1K  columns 8  scan 2.7s

roles: amount 1, audit 2, category 2, date 2, other 1, who 1

## when

DATE
  2018       780  #####################
  2019      1.1K  ##############################
  2020      1.1K  ##############################
  2021       406  ###########
  2022       396  ###########
  2023       728  ####################
  2024       730  ####################
  2025       730  ####################
  2026       178  #####

INGESTED_AT
  2026      6.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 6.1K | 0 | 1.86M | 3.50M | 26.20M | 9.31B |

## who

SRC_SHA256 by rows
      6.1K  fcd143d2279a04d583a7f78839a986fc561f4c7c17ac834792e1665974b8e708

SRC_SHA256 by dollars
       9.31B     6.1K rows  fcd143d2279a04d583a7f78839a986fc561f4c7c17ac834792e1665974b8

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  fcd143d2279a04d583a7f78839a986fc561f4c7c  2018:1.06B 2019:1.76B 2020:1.63B 2021:999.46M 2022:951.72M 2023:870.19M 2024:873.29M 2025:925.05M 2026:240.67M

## what

NAME: Total Shrinkage Gas Purchased 47%, Total Shrinkage Gas Sold 20%, Gas Purchased via Services Con 16%, Gas Purchased via Trading Plat 16%

LOCATION: Total Shrinkage Gas Purchased 47%, Total Shrinkage Gas Sold 20%, Gas Purchased via Services Con 16%, Gas Purchased via Trading Plat 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | category | 4 | 0 | Total Shrinkage Gas Purch 2.9K; Total Shrinkage Gas Sold 1.2K; Gas Purchased via Service 1.0K; Gas Purchased via Trading 1.0K |
| LOCATION | category | 4 | 0 | Total Shrinkage Gas Purch 2.9K; Total Shrinkage Gas Sold 1.2K; Gas Purchased via Service 1.0K; Gas Purchased via Trading 1.0K |
| DATE | date | 2.9K | 0 | 2026-03-30T00:00:00 31; 2026-03-29T00:00:00 31; 2026-03-28T00:00:00 31; 2026-03-27T00:00:00 31 |
| VALUE | amount | 149 | 0 | 0 2.2K; 1758426 306; 2051497 209; 2227340 124 |
| UNIT | other | 1 | 0 | kWh 6.1K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:35:34.14838 6.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | cb92175c-db93-486b-9e1f-6 6.1K |
| SRC_SHA256 | who | 1 | 0 | fcd143d2279a04d583a7f7883 6.1K |
