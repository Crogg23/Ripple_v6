# PORTAL_ARC_LA_COUNTY_OPEN_D_90F6889981

rows 212  columns 17  scan 4.7s

roles: amount 2, audit 2, category 4, date 1, other 5, who 4

## when

INGESTED_AT
  2026       212  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 212 | 33.34 | 34.09 | 34.70 | 34.79 | 7.2K |
| LONGITUDE | 212 | -118.81 | -118.31 | -117.77 | -117.75 | -25.1K |

## who

CONAME by rows
         4  Harley-davidson
         4  Cycle Gear
         2  Thunderroad Motorcycles
         2  California Harley-davidson
         2  Safari Cycle
         2  Golf Cars La
         2  Heartland Usa
         1  Nationwide Cycle
         1  Axo America Inc
         1  F 4 K Team Inc
         1  Alloy Art
         1  Four Aces Cycle
         1  Wheels in Motion
         1  Rpm Motorsports
         1  Solar Electric Scooters Inc
         1  Mc Intosh Equipment
         1  Harleys & Hot Rods
         1  Vespa of Sherman Oaks
         1  West Valley Cycle Sales Inc
         1  Temple City Power Sports

CONAME by dollars
      137.16        4 rows  Cycle Gear
      136.89        4 rows  Harley-davidson
       68.36        2 rows  Golf Cars La
       68.18        2 rows  Thunderroad Motorcycles
       67.85        2 rows  Heartland Usa
       67.58        2 rows  California Harley-davidson
       67.56        2 rows  Safari Cycle
       34.79        1 rows  Classic British Spares
       34.70        1 rows  Baker Custom Inc
       34.70        1 rows  Mgs Racing
       34.69        1 rows  High Desert Performance
       34.68        1 rows  Flums Machine Factory
       34.68        1 rows  A V Honda Motorsports
       34.68        1 rows  Av Motoplex
       34.65        1 rows  Aces & Eights Scooters
       34.65        1 rows  Mc Intosh Equipment
       34.65        1 rows  Nationwide Cycle
       34.59        1 rows  Palmdale Supercycles
       34.49        1 rows  Starcycle Accessories Castaic
       34.45        1 rows  Santa Clarita Valley Golf Cars

STATE_NAME by rows
       212  California

STATE_NAME by dollars
        7.2K      212 rows  California

CITY by rows
        14  Los Angeles
        11  Lancaster
         9  Santa Clarita
         7  West Hollywood
         7  Chatsworth
         6  Torrance
         6  Van Nuys
         6  Marina Del Rey
         5  Glendale
         5  City of Industry
         5  Avalon
         5  Inglewood
         4  Pomona
         4  Santa Fe Springs
         4  Long Beach
         4  Canoga Park
         4  Pasadena
         4  Pico Rivera
         3  Harbor City
         3  Valencia

CITY by dollars
      476.73       14 rows  Los Angeles
      381.55       11 rows  Lancaster
      309.71        9 rows  Santa Clarita
      239.68        7 rows  Chatsworth
      238.60        7 rows  West Hollywood
      205.26        6 rows  Van Nuys
      203.93        6 rows  Marina Del Rey
      203.03        6 rows  Torrance
      170.70        5 rows  Glendale
      170.05        5 rows  City of Industry
      169.80        5 rows  Inglewood
      166.70        5 rows  Avalon
      136.83        4 rows  Canoga Park
      136.59        4 rows  Pasadena
      136.29        4 rows  Pomona
      135.97        4 rows  Pico Rivera
      135.78        4 rows  Santa Fe Springs
      135.16        4 rows  Long Beach
      103.31        3 rows  Valencia
      103.29        3 rows  Canyon Country

SRC_SHA256 by rows
       212  21fd6d5d8266bec603aec78d7732177dd011ef90dd07e3c74b1d1f4410b69c92

SRC_SHA256 by dollars
        7.2K      212 rows  21fd6d5d8266bec603aec78d7732177dd011ef90dd07e3c74b1d1f4410b6

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  A V Honda Motorsports                     2026:34.68
  Aces & Eights Scooters                    2026:34.65
  Alloy Art                                 2026:34.13
  Av Motoplex                               2026:34.68
  Axo America Inc                           2026:34.41
  Baker Custom Inc                          2026:34.70
  California Harley-davidson                2026:67.58
  Classic British Spares                    2026:34.79
  Cycle Gear                                2026:137.16
  F 4 K Team Inc                            2026:34.01
  Flums Machine Factory                     2026:34.68
  Four Aces Cycle                           2026:34.24
  Golf Cars La                              2026:68.36
  Harley-davidson                           2026:136.89
  Harleys & Hot Rods                        2026:33.97
  Heartland Usa                             2026:67.85
  High Desert Performance                   2026:34.69
  Mc Intosh Equipment                       2026:34.65
  Mgs Racing                                2026:34.70
  Nationwide Cycle                          2026:34.65
  Palmdale Supercycles                      2026:34.59
  Rpm Motorsports                           2026:34.23
  Safari Cycle                              2026:67.56
  Solar Electric Scooters Inc               2026:34.21
  Starcycle Accessories Castaic             2026:34.49
  Temple City Power Sports                  2026:34.10
  Thunderroad Motorcycles                   2026:68.18
  Vespa of Sherman Oaks                     2026:34.15
  West Valley Cycle Sales Inc               2026:34.21
  Wheels in Motion                          2026:34.24

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  California                                2026:7.2K

## what

NAICS: 44122808 56%, 44122809 22%, 44122807 11%, 44122804 7%, 44122801 2%, 44122810 1%, 44122811 0%

SIC: 557106 56%, 557103 22%, 557105 11%, 557102 7%, 557101 2%, 557109 1%, 557111 0%

EMPNUM: 3 41%, 2 18%, 1 11%, 5 6%, 4 5%, 20 4%, 6 4%, 9 4%, 7 3%, 10 3%, 8 2%, 12 1%

SALESVOL: 1094000 40%, 729000 17%, 365000 11%, 1823000 6%, 1458000 5%, 7289000 4%, 2187000 4%, 3280000 4%, 0 3%, 2551000 3%, 3645000 3%, 2916000 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 211 | 0 | 212 2; 211 2; 210 2; 209 2 |
| CONAME | who | 201 | 0 | Harley-davidson 4; Cycle Gear 4; Island Rentals 2; Safari Cycle 2 |
| ADDR | other | 163 | 2 | Ventura Blvd 5; Sierra Hwy 5; Pacific Coast Hwy 4; S La Cienega Blvd 4 |
| CITY | who | 80 | 0 | Los Angeles 14; Lancaster 11; Santa Clarita 9; West Hollywood 7 |
| STATE_NAME | who | 1 | 0 | California 212 |
| ZIP | other | 118 | 0 | 93534 9; 91350 8; 91311 7; 90292 6 |
| NAICS | category | 7 | 0 | 44122808 119; 44122809 46; 44122807 24; 44122804 14 |
| SIC | category | 7 | 0 | 557106 119; 557103 46; 557105 24; 557102 14 |
| EMPNUM | category | 25 | 0 | 3 79; 2 34; 1 21; 5 12 |
| SALESVOL | category | 26 | 0 | 1094000 76; 729000 32; 365000 21; 1823000 12 |
| DESC | other | 209 | 0 | Island Rentals, Avalon, C 2; Catalina Yamaha Golf Cars 2; Catalina Auto & Bike Rent 2; Cartopia Golf Cart Rental 2 |
| LATITUDE | amount | 199 | 0 | 33.9602000000254 3; 34.1677999996683 3; 33.9579999997085 2; 33.7895000002081 2 |
| LONGITUDE | amount | 195 | 0 | -118.370400000035 3; -118.534299999666 3; -118.303500000341 2; -117.926299999687 2 |
| GEOMETRY | other | 205 | 0 | {"type": "Point", "coordi 3; {"type": "Point", "coordi 3; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:21:06.47918 212 |
| SOURCE_RUN_ID | audit | 1 | 0 | d63f559c-2e5a-418e-9471-b 212 |
| SRC_SHA256 | who | 1 | 0 | 21fd6d5d8266bec603aec78d7 212 |
