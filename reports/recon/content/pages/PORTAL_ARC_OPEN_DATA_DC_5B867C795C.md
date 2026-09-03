# PORTAL_ARC_OPEN_DATA_DC_5B867C795C

rows 133  columns 10  scan 2.6s

roles: amount 2, audit 2, category 1, date 2, other 3, who 1

## when

DATE
  2011        27  ##############################
  2012        18  ####################
  2013        27  ##############################
  2014        24  ###########################
  2015        26  #############################
  2016        11  ############

INGESTED_AT
  2026       133  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| Y | 133 | 0 | 38.89 | 38.96 | 38.96 | 4.9K |
| X | 133 | -77.10 | -76.99 | 0 | 0 | -9.8K |

## who

SRC_SHA256 by rows
       133  ad799af09cf50638d8d060e5a32d02521be5e0df0cbbce6a7ddc8be737ca81a3

SRC_SHA256 by dollars
        4.9K      133 rows  ad799af09cf50638d8d060e5a32d02521be5e0df0cbbce6a7ddc8be737ca

## who x when

SRC_SHA256 by DATE, dollars = Y
  ad799af09cf50638d8d060e5a32d02521be5e0df  2011:1.0K 2012:700.30 2013:894.55 2014:933.45 2015:1.0K 2016:388.87

## what

FATALITIES: 1 93%, 2 6%, 3 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | other | 132 | 0 | 133 1; 132 1; 131 1; 130 1 |
| CCN_REV | other | 126 | 2 | USPP 4; 13109655 2; 13065538 2; 16105271 1 |
| DATE | date | 129 | 0 | 1433980800000 3; 1368662400000 2; 1340409600000 2; 1317254400000 2 |
| FATALITIES | category | 3 | 0 | 1 124; 2 8; 3 1 |
| Y | amount | 119 | 0 | 0.0 6; 38.862524 3; 38.836173 2; 38.866486 2 |
| X | amount | 118 | 0 | 0.0 6; -76.997684 3; -76.985022 2; -76.982203 2 |
| GEOMETRY | other | 119 | 0 | nan 6; {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:32:36.07584 133 |
| SOURCE_RUN_ID | audit | 1 | 0 | d2844dc3-c5bb-4f97-8fd2-d 133 |
| SRC_SHA256 | who | 1 | 0 | ad799af09cf50638d8d060e5a 133 |
