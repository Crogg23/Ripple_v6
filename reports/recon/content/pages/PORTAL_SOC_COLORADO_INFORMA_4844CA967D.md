# PORTAL_SOC_COLORADO_INFORMA_4844CA967D

rows 36  columns 10  scan 2.1s

roles: audit 2, category 6, date 1, other 1, who 1

## when

INGESTED_AT
  2026        36  ##############################

## who

SRC_SHA256 by rows
        36  31b90e7de34e3d6a2759938cff5869c05cdf676af2be82dec31c076c5d26aed2

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  31b90e7de34e3d6a2759938cff5869c05cdf676a  2026:36

## what

THE_GEOM: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

OBJECTID: 33679 8%, 32191 8%, 31584 8%, 33310 8%, 34913 8%, 34119 8%, 33140 8%, 33681 8%, 33247 8%, 33683 8%, 33318 8%, 31577 8%

CONAME: KROGER 19%, DOLLAR TREE STORES 15%, FAMILY DOLLAR STORES 15%, WAL-MART ASSOCIATES  INC 11%, SAFEWAY 11%, DOLLAR GENERAL 7%, CAROLS ORIENTAL FOODS INC 4%, NATURAL GROCERS 4%, SPROUTS FARMERS MARKET 4%, DOLLAR TREE 4%, EL TORITO CARNICERIA 4%, G J MART, LLC 4%

CITY: GRAND JUNCTION 81%, FRUITA 8%, CLIFTON 6%, PALISADE 6%

ZIP: 81505 25%, 81501 19%, 81503 19%, 81504 14%, 81521 8%, 81520 6%, 81526 6%, 81506 3%

NAICS: 445110 47%, 455219 33%, 455211 11%, 445240 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | category | 36 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| OBJECTID | category | 35 | 0 | 33679 1; 32191 1; 31584 1; 33310 1 |
| CONAME | category | 21 | 0 | KROGER 5; DOLLAR TREE STORES 4; FAMILY DOLLAR STORES 4; WAL-MART ASSOCIATES  INC 3 |
| CITY | category | 4 | 0 | GRAND JUNCTION 29; FRUITA 3; CLIFTON 2; PALISADE 2 |
| STATE | other | 1 | 0 | CO 36 |
| ZIP | category | 8 | 0 | 81505 9; 81501 7; 81503 7; 81504 5 |
| NAICS | category | 4 | 0 | 445110 17; 455219 12; 455211 4; 445240 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:21.44468 36 |
| SOURCE_RUN_ID | audit | 1 | 0 | e324c07b-2f28-45ba-b628-f 36 |
| SRC_SHA256 | who | 1 | 0 | 31b90e7de34e3d6a2759938cf 36 |
