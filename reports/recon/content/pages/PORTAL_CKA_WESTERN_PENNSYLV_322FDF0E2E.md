# PORTAL_CKA_WESTERN_PENNSYLV_322FDF0E2E

rows 828  columns 12  scan 3.6s

roles: amount 4, audit 2, category 3, date 2, who 2

## when

DATETIME
  2026       828  ##############################

INGESTED_AT
  2026       828  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE_STR | 828 | 39.50 | 40.88 | 42.25 | 42.25 | 33.8K |
| LONGITUDE_STR | 828 | -81.25 | -77.81 | -74.38 | -74.38 | -64.4K |
| TEMP_DIFF | 828 | 0 | 0 | 3.17 | 3.72 | 346.30 |
| HEIGHT | 828 | 0 | 0 | 342.01 | 474.90 | 73.7K |

## who

FORECAST_VERSION by rows
       828  2026-07-02_00

FORECAST_VERSION by dollars
       33.8K      828 rows  2026-07-02_00

SRC_SHA256 by rows
       828  c0eece3e0da187a959794e41f18cbe16ff60003899e4b4155b8f6beb969b267a

SRC_SHA256 by dollars
       33.8K      828 rows  c0eece3e0da187a959794e41f18cbe16ff60003899e4b4155b8f6beb969b

## who x when

FORECAST_VERSION by DATETIME, dollars = LATITUDE_STR
  2026-07-02_00                             2026:33.8K

SRC_SHA256 by DATETIME, dollars = LATITUDE_STR
  c0eece3e0da187a959794e41f18cbe16ff600038  2026:33.8K

## what

PLACE: Saltsburg 11%, Monroeville 11%, Pittsburgh 11%, Pittsburgh International Airpo 11%, Idlewild 11%, New Stanton 11%, Bethel Park 11%, Canonsburg 11%, Philadelphia 11%

INVERSION: 0 67%, 1 33%

STRENGTH: 0 67%, 2 17%, 1 15%, 3 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATETIME | date | 3 | 0 | 2026-07-03T12:00:00 276; 2026-07-07T12:00:00 276; 2026-07-05T12:00:00 276 |
| LATITUDE_STR | amount | 12 | 0 | 42.25 69; 42.0 69; 41.75 69; 41.5 69 |
| LONGITUDE_STR | amount | 22 | 0 | -74.375 36; -74.6875 36; -75.0 36; -75.3125 36 |
| PLACE | category | 10 | 801 | Saltsburg 3; Monroeville 3; Pittsburgh 3; Pittsburgh International  3 |
| INVERSION | category | 2 | 0 | 0 556; 1 272 |
| TEMP_DIFF | amount | 182 | 0 | 0.0 556; 1.9059199999999805 5; 0.43520999999998367 5; 1.0934199999999805 4 |
| HEIGHT | amount | 126 | 0 | 0.0 556; 198.22327499999994 12; 198.97327499999994 10; 334.54169 9 |
| STRENGTH | category | 4 | 0 | 0 556; 2 138; 1 123; 3 11 |
| FORECAST_VERSION | who | 1 | 0 | 2026-07-02_00 828 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:47:34.89121 828 |
| SOURCE_RUN_ID | audit | 1 | 0 | dc03b958-0d4e-4d02-9944-7 828 |
| SRC_SHA256 | who | 1 | 0 | c0eece3e0da187a959794e41f 828 |
