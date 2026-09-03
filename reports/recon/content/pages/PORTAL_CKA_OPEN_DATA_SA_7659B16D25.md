# PORTAL_CKA_OPEN_DATA_SA_7659B16D25

rows 7  columns 10  scan 4.1s

roles: amount 3, audit 2, category 3, date 2, who 1

## when

CREATED_DATE
  2025         7  ##############################

INGESTED_AT
  2026         7  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQMILES | 7 | 12.04 | 78.93 | 135.99 | 138.24 | 506.69 |
| SHAPE__AREA | 7 | 0 | 0.02 | 0.03 | 0.03 | 0.11 |
| SHAPE__LENGTH | 7 | 0.40 | 1.57 | 2.32 | 2.36 | 9.62 |

## who

SRC_SHA256 by rows
         7  610967ad2831752196884da0c6c30d603bd2ffba65e2a1b3d21c75c8455c2523

SRC_SHA256 by dollars
      506.69        7 rows  610967ad2831752196884da0c6c30d603bd2ffba65e2a1b3d21c75c8455c

## who x when

SRC_SHA256 by CREATED_DATE, dollars = SQMILES
  610967ad2831752196884da0c6c30d603bd2ffba  2025:506.69

## what

OBJECTID: 7 14%, 6 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

SUBSTN: WEST 14%, SOUTH 14%, PRUE 14%, NORTH 14%, EAST 14%, DOWNTOWN 14%, CENTRAL 14%

WEBSITE: https://www.sanantonio.gov/SAP 29%, https://www.sanantonio.gov/SAP 14%, https://www.sanantonio.gov/SAP 14%, https://www.sanantonio.gov/SAP 14%, https://www.sanantonio.gov/SAP 14%, https://www.sanantonio.gov/SAP 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 7 | 0 | 7 1; 6 1; 5 1; 4 1 |
| SUBSTN | category | 7 | 0 | WEST 1; SOUTH 1; PRUE 1; NORTH 1 |
| SQMILES | amount | 7 | 0 | 78.92759428 1; 138.24325741 1; 93.53653251 1; 100.72168851 1 |
| WEBSITE | category | 6 | 0 | https://www.sanantonio.go 2; https://www.sanantonio.go 1; https://www.sanantonio.go 1; https://www.sanantonio.go 1 |
| CREATED_DATE | date | 1 | 0 | 11/17/2025 8:24:27 PM 7 |
| SHAPE__AREA | amount | 7 | 0 | 0.0190202414939904 1; 0.0332622348896621 1; 0.0225594142282262 1; 0.02429613927643 1 |
| SHAPE__LENGTH | amount | 7 | 0 | 1.67582925213051 1; 2.36209408698292 1; 1.57013456763227 1; 1.50610511984663 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:31.85453 7 |
| SOURCE_RUN_ID | audit | 1 | 0 | 99bab2f8-5a26-452d-a463-a 7 |
| SRC_SHA256 | who | 1 | 0 | 610967ad2831752196884da0c 7 |
