# PORTAL_CKA_WESTERN_PENNSYLV_010A1B6275

rows 10.0K  columns 13  scan 3.2s

roles: amount 5, audit 2, category 1, date 1, id 3, other 1, who 1

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREA | 10.0K | 0.54 | 82.3K | 9.47M | 49.25M | 5.62B |
| ACRES | 10.0K | 0 | 1.89 | 217.38 | 1.1K | 128.9K |
| PERIMETER | 10.0K | 6 | 1.8K | 37.5K | 134.4K | 39.96M |
| SHAPE_AREA | 10.0K | 0.54 | 82.3K | 9.47M | 49.25M | 5.62B |
| SHAPE_LENG | 10.0K | 6 | 1.8K | 37.5K | 134.4K | 39.96M |

## who

SRC_SHA256 by rows
     10.0K  ae499ba3f7306d1cbd65b2864533da96836422e3d8a382ef13bd625a8c0b51fd

SRC_SHA256 by dollars
       5.62B    10.0K rows  ae499ba3f7306d1cbd65b2864533da96836422e3d8a382ef13bd625a8c0b

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREA
  ae499ba3f7306d1cbd65b2864533da96836422e3  2026:5.62B

## what

NATURE_COD: 310 85%, 0 15%, 350 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA | amount | 10.2K | 0 | 33387.4716375 50; 3937.9380785 50; 20146.909069 50; 583039.653405 50 |
| ACRES | amount | 10.0K | 0 | 0.766474354521 50; 0.0904029303683 50; 0.462511463249 50; 13.3848028008 50 |
| FID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| NATURE_COD | category | 3 | 0 | 310 8.5K; 0 1.5K; 350 1 |
| PERIMETER | amount | 10.1K | 0 | 1027.48575412 50; 281.67006192 50; 605.808027586 50; 7616.55369047 50 |
| SHAPE_AREA | amount | 9.9K | 0 | 33387.4893326 50; 3937.93589505 50; 20146.9187512 50; 583039.677838 50 |
| SHAPE_LENG | amount | 9.9K | 0 | 1027.48582662 50; 281.669988613 50; 605.80810396 50; 7616.55381676 50 |
| WOODLAND | id | 10.0K | 0 | 9641 50; 9640 50; 9639 50; 9638 50 |
| WOODLAND_I | other | 3.5K | 0 | 0 1.2K; 2115 46; 1383 46; 57 45 |
| GEOMETRY | id | 10.2K | 0 | POLYGON ((575060.50982418 50; POLYGON ((606552.07133045 50; POLYGON ((599333.44871041 50; POLYGON ((561953.23332256 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:31:37.08457 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3a414a67-9acd-4b6a-8d19-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | ae499ba3f7306d1cbd65b2864 10.0K |
