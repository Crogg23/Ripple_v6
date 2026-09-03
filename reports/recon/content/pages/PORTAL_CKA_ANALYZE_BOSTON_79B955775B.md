# PORTAL_CKA_ANALYZE_BOSTON_79B955775B

rows 15  columns 15  scan 3.3s

roles: amount 2, audit 2, category 8, date 1, empty 1, who 2

## when

INGESTED_AT
  2026        15  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 15 | 0 | 0.03 | 0.06 | 0.06 | 0.45 |
| SHAPE_AREA | 15 | 0 | 0 | 0 | 0 | 0 |

## who

STATUS by rows
        15  Designated & Activated

STATUS by dollars
        0.45       15 rows  Designated & Activated

SRC_SHA256 by rows
        15  ff545cd5532a7e84c3db892a293fdd1c531066ea0e02fd202a1bb74130da00cb

SRC_SHA256 by dollars
        0.45       15 rows  ff545cd5532a7e84c3db892a293fdd1c531066ea0e02fd202a1bb74130da

## who x when

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Designated & Activated                    2026:0.45

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  ff545cd5532a7e84c3db892a293fdd1c531066ea  2026:0.45

## what

SURVEYID: 0 20%, 30707 10%, 30009 10%, 24554 10%, 14242 10%, 25597 10%, 15380 10%, 13793 10%, 10560 10%

HIST_NAME: St. Botolph Area Architectural 8%, South End Protection Area 8%, South End Landmark District 8%, Mission Hill Triangle Architec 8%, Historic Beacon Hill District 8%, Highland Park Architectural Co 8%, Fort Point Seaport Blvd Prot.  8%, Fort Point Landmark District 8%, Fort Point A St Protection Are 8%, Eustis Street Protection Area 8%, Eustis Street Architectural Co 8%, Bay Village Historic District 8%

PLACE_NAME: Boston 20%, Roxbury 20%, South Boston 20%, Fenway 13%, South End 13%, Mission Hill 7%, Brighton 7%

YEAR: 1981 18%, 1983 18%, 1986 9%, 1955 9%, 2022 9%, 2009 9%, 1979 9%, 1966 9%, 2002 9%

USE_TYPE: Residential District 70%, Other Governmental or Civic 10%, Other 10%, Other Commercial 10%

TYPE: LHD 60%, PA 27%, Landmark District 7%, ACD 7%

URL: http://www.cityofboston.gov/la 20%, http://www.cityofboston.gov/la 13%, http://www.cityofboston.gov/la 13%, http://www.cityofboston.gov/la 7%, http://www.cityofboston.gov/la 7%, https://www.boston.gov/histori 7%, https://www.boston.gov/histori 7%, https://www.cityofboston.gov/l 7%, https://www.boston.gov/sites/d 7%, http://www.cityofboston.gov/la 7%, http://www.cityofboston.gov/la 7%

SHAPE_WKT: MULTIPOLYGON (((-71.0490454819 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SURVEYID | category | 10 | 5 | 0 2; 30707 1; 30009 1; 24554 1 |
| HIST_NAME | category | 15 | 0 | St. Botolph Area Architec 1; South End Protection Area 1; South End Landmark Distri 1; Mission Hill Triangle Arc 1 |
| PLACE_NAME | category | 7 | 0 | Boston 3; Roxbury 3; South Boston 3; Fenway 2 |
| YEAR | category | 10 | 4 | 1981 2; 1983 2; 1986 1; 1955 1 |
| STYLE | empty | 2 | 15 |  |
| USE_TYPE | category | 6 | 5 | Residential District 7; Other Governmental or Civ 1; Other 1; Other Commercial 1 |
| TYPE | category | 4 | 0 | LHD 9; PA 4; Landmark District 1; ACD 1 |
| STATUS | who | 1 | 0 | Designated & Activated 15 |
| URL | category | 11 | 0 | http://www.cityofboston.g 3; http://www.cityofboston.g 2; http://www.cityofboston.g 2; http://www.cityofboston.g 1 |
| SHAPE_LENGTH | amount | 15 | 0 | 0.015265845599761 1; 0.060822967357720 1; 0.061099258014674 1; 0.006425442343381 1 |
| SHAPE_AREA | amount | 15 | 0 | 0.000008139545865 1; 0.000072131957845 1; 0.000139486028212 1; 0.000001692916557 1 |
| SHAPE_WKT | category | 2 | 14 | MULTIPOLYGON (((-71.04904 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:16.61202 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | 39e766bb-0d8c-4093-82b5-6 15 |
| SRC_SHA256 | who | 1 | 0 | ff545cd5532a7e84c3db892a2 15 |
