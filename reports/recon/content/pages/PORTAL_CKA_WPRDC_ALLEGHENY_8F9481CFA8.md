# PORTAL_CKA_WPRDC_ALLEGHENY_8F9481CFA8

rows 2.2K  columns 17  scan 5.5s

roles: amount 5, audit 2, category 6, date 4, who 1

## when

DATETIME_UTC
  2026      2.2K  ##############################

DATETIME_ET
  2026      2.2K  ##############################

DATE_OF_PREDICTION
  2026      2.2K  ##############################

INGESTED_AT
  2026      2.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2.2K | 40 | 40.50 | 41 | 41 | 87.5K |
| LONGITUDE | 2.2K | -80.50 | -79.88 | -79.25 | -79.25 | -172.5K |
| VALUE | 2.2K | 0.09 | 1.48 | 9.27 | 14.50 | 4.5K |
| LATITUDE_STR | 2.2K | 40 | 40.50 | 41 | 41 | 87.5K |
| LONGITUDE_STR | 2.2K | -80.50 | -79.88 | -79.25 | -79.25 | -172.5K |

## who

SRC_SHA256 by rows
      2.2K  6a8eefd9ea8d5d0dfde92c15c1fabc714f5563d276749c026594cd3e76699afb

SRC_SHA256 by dollars
        4.5K     2.2K rows  6a8eefd9ea8d5d0dfde92c15c1fabc714f5563d276749c026594cd3e7669

## who x when

SRC_SHA256 by DATETIME_UTC, dollars = VALUE
  6a8eefd9ea8d5d0dfde92c15c1fabc714f5563d2  2026:4.5K

## what

PARAMETER: PM25_RH35 33%, NO2 33%, CO 33%

UNITS: ug m-3 33%, ppb 33%, ppm 33%

AQI: 1 69%, 2 21%, 3 5%, 4 2%, 0 0%, 5 0%, 19 0%, 26 0%, 22 0%, 32 0%, 15 0%

AQI_DESCRIPTOR: Good 100%

AQI_TYPE: 1-hour 57%, rolling 8-hour 40%, rolling 24-hour 2%

PLACE: Slippery Rock 9%, New Castle 9%, Elderton 9%, Kittanning 9%, Saxonburg 9%, Butler 9%, Beaver Falls 9%, Ohioville 9%, Blairsville 9%, Saltsburg 9%, Penn Hills 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATETIME_UTC | date | 24 | 0 | 2026-06-01T08:30:00 90; 2026-06-01T07:30:00 90; 2026-06-01T06:30:00 90; 2026-06-01T05:30:00 90 |
| DATETIME_ET | date | 24 | 0 | 2026-06-01T04:30:00 90; 2026-06-01T03:30:00 90; 2026-06-01T02:30:00 90; 2026-06-01T01:30:00 90 |
| LATITUDE | amount | 5 | 0 | 41.0 432; 40.75 432; 40.5 432; 40.25 432 |
| LONGITUDE | amount | 6 | 0 | -79.25 360; -79.5 360; -79.75 360; -80.0 360 |
| PARAMETER | category | 3 | 0 | PM25_RH35 720; NO2 720; CO 720 |
| VALUE | amount | 1.2K | 0 | 0.10058283805847168 26; 0.10337680578231812 22; 0.10244548320770264 21; 0.10523945093154907 17 |
| UNITS | category | 3 | 0 | ug m-3 720; ppb 720; ppm 720 |
| AQI | category | 25 | 900 | 1 858; 2 267; 3 67; 4 26 |
| AQI_DESCRIPTOR | category | 2 | 900 | Good 1.3K |
| AQI_TYPE | category | 4 | 900 | 1-hour 720; rolling 8-hour 510; rolling 24-hour 30 |
| PLACE | category | 27 | 288 | Slippery Rock 72; New Castle 72; Elderton 72; Kittanning 72 |
| LATITUDE_STR | amount | 5 | 0 | 41.0 432; 40.75 432; 40.5 432; 40.25 432 |
| LONGITUDE_STR | amount | 6 | 0 | -79.25 360; -79.5 360; -79.75 360; -80.0 360 |
| DATE_OF_PREDICTION | date | 1 | 0 | 2026-05-31 2.2K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:03:15.99260 2.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | cc69477e-7205-4d60-9fa9-9 2.2K |
| SRC_SHA256 | who | 1 | 0 | 6a8eefd9ea8d5d0dfde92c15c 2.2K |
