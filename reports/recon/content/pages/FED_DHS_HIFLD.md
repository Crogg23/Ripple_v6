# FED_DHS_HIFLD

rows 500  columns 18  scan 2.4s

roles: audit 2, category 2, date 1, empty 9, other 2, who 2

## when

SOURCE_DATE
  2014       359  ##############################
  2015       107  #########
  2016         5  
  2017         9  #
  2018         3  
  2019        11  #
  2020         2  
  2021         4  

## who

LAYER_NAME by rows
       500  Electric Power Transmission Lines

_SRC_SHA256 by rows
       500  3e4f3fd3bc26aa1d974b56b6d4bbb4dd174bb5d1f274fc208c5706ae738ad18b

## who x when

LAYER_NAME by SOURCE_DATE
  Electric Power Transmission Lines         2014:359 2015:107 2016:5 2017:9 2018:3 2019:11 2020:2 2021:4

_SRC_SHA256 by SOURCE_DATE
  3e4f3fd3bc26aa1d974b56b6d4bbb4dd174bb5d1  2014:359 2015:107 2016:5 2017:9 2018:3 2019:11 2020:2 2021:4

## what

STATUS: NOT AVAILABLE 86%, IN SERVICE 14%

OWNER: PACIFICORP 27%, TRI-STATE G & T ASSN, INC 17%, PUBLIC SERVICE CO OF COLORADO 14%, IDAHO POWER CO 14%, WAPA-- WESTERN AREA POWER ADMI 9%, MIDWEST ENERGY INC 6%, BONNEVILLE POWER ADMINISTRATIO 3%, WHEAT BELT PUBLIC POWER DIST 3%, NOT AVAILABLE 2%, BLACK HILLS POWER, INC. 2%, DELTA MONTROSE ELECTRIC ASSN 1%, PIONEER ELECTRIC COOP, INC - ( 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 507 | 0 | 70273 3; 70272 3; 70271 3; 70270 3 |
| NAME | empty | 1 | 500 |  |
| ADDRESS | empty | 1 | 500 |  |
| CITY | empty | 1 | 500 |  |
| STATE | empty | 1 | 500 |  |
| ZIP | empty | 1 | 500 |  |
| COUNTY | empty | 1 | 500 |  |
| FIPS | empty | 1 | 500 |  |
| LATITUDE | empty | 1 | 500 |  |
| LONGITUDE | empty | 1 | 500 |  |
| NAICS_CODE | other | 1 | 0 | 221121 500 |
| LAYER_NAME | who | 1 | 0 | Electric Power Transmissi 500 |
| STATUS | category | 2 | 0 | NOT AVAILABLE 428; IN SERVICE 72 |
| OWNER | category | 17 | 0 | PACIFICORP 133; TRI-STATE G & T ASSN, INC 85; PUBLIC SERVICE CO OF COLO 70; IDAHO POWER CO 67 |
| SOURCE_DATE | date | 40 | 0 | 1404864000000 92; 1435536000000 82; 1404172800000 37; 1403481600000 37 |
| _INGESTED_AT | audit | 1 | 0 | 1783005852681013 500 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 2cc16353-0cbf-40ff-a5fe-d 500 |
| _SRC_SHA256 | who | 1 | 0 | 3e4f3fd3bc26aa1d974b56b6d 500 |
