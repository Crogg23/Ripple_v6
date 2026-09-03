# FED_NOAA_WEATHER_API

rows 287  columns 35  scan 4.3s

roles: audit 2, category 7, date 5, empty 12, other 5, who 4

## when

SENT
  2026       287  ##############################

EFFECTIVE
  2026       287  ##############################

ONSET
  2026       286  ##############################

EXPIRES
  2026       287  ##############################

ENDS
  2026       240  ##############################

## who

SENDER_NAME by rows
        40  NWS Anchorage AK
        17  NWS Mount Holly NJ
        14  NWS La Crosse WI
        14  NWS Baltimore MD/Washington DC
        11  NWS Wakefield VA
         7  NWS Little Rock AR
         7  NWS St Louis MO
         7  NWS Gray ME
         7  NWS Denver CO
         7  NWS Upton NY
         6  NWS Lincoln IL
         6  NWS Boston/Norton MA
         6  NWS State College PA
         6  NWS Pueblo CO
         5  NWS Blacksburg VA
         5  NWS Birmingham AL
         5  NWS Peachtree City GA
         4  NWS Memphis TN
         4  NWS Tiyan GU
         4  NWS Phoenix AZ

INSTRUCTION by rows
        21  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
        21  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
        16  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
        12  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
        10  Inexperienced mariners, especially those operating smaller
vessels, sh
         9  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         6  A Red Flag Warning means that critical fire weather conditions
are eit
         6  Turn around, don't drown when encountering flooded roads. Most flood
d
         6  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         5  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         5  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         5  Turn around, don't drown when encountering flooded roads. Most flood
d
         4  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         4  Persons with interests along this river need to remain aware of the
la
         4  Motorists should not attempt to drive around barricades or drive cars

         3  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         3  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         3  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         3  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t
         2  Drink plenty of fluids, stay in an air-conditioned room, stay out of
t

TYPE by rows
       287  Feature

_SRC_SHA256 by rows
       287  88fc93cb93895d59694aa3359d0ef607f606d3698906c71fecf3488820db085d

## who x when

SENDER_NAME by EFFECTIVE
  NWS Anchorage AK                          2026:40
  NWS Baltimore MD/Washington DC            2026:14
  NWS Birmingham AL                         2026:5
  NWS Blacksburg VA                         2026:5
  NWS Boston/Norton MA                      2026:6
  NWS Denver CO                             2026:7
  NWS Gray ME                               2026:7
  NWS La Crosse WI                          2026:14
  NWS Lincoln IL                            2026:6
  NWS Little Rock AR                        2026:7
  NWS Memphis TN                            2026:4
  NWS Mount Holly NJ                        2026:17
  NWS Peachtree City GA                     2026:5
  NWS Phoenix AZ                            2026:4
  NWS Pueblo CO                             2026:6
  NWS St Louis MO                           2026:7
  NWS State College PA                      2026:6
  NWS Tiyan GU                              2026:4
  NWS Upton NY                              2026:7
  NWS Wakefield VA                          2026:11

INSTRUCTION by EFFECTIVE
  A Red Flag Warning means that critical f  2026:6
  Drink plenty of fluids, stay in an air-c  2026:3
  Drink plenty of fluids, stay in an air-c  2026:3
  Drink plenty of fluids, stay in an air-c  2026:16
  Drink plenty of fluids, stay in an air-c  2026:12
  Drink plenty of fluids, stay in an air-c  2026:21
  Drink plenty of fluids, stay in an air-c  2026:5
  Drink plenty of fluids, stay in an air-c  2026:6
  Drink plenty of fluids, stay in an air-c  2026:2
  Drink plenty of fluids, stay in an air-c  2026:9
  Drink plenty of fluids, stay in an air-c  2026:21
  Drink plenty of fluids, stay in an air-c  2026:3
  Drink plenty of fluids, stay in an air-c  2026:5
  Drink plenty of fluids, stay in an air-c  2026:3
  Drink plenty of fluids, stay in an air-c  2026:4
  Inexperienced mariners, especially those  2026:10
  Motorists should not attempt to drive ar  2026:4
  Persons with interests along this river   2026:4
  Turn around, don't drown when encounteri  2026:5
  Turn around, don't drown when encounteri  2026:6

## what

EVENT: Heat Advisory 26%, Extreme Heat Warning 23%, Small Craft Advisory 21%, Air Quality Alert 13%, Flood Warning 9%, Red Flag Warning 3%, Extreme Heat Watch 1%, Special Weather Statement 1%, Flood Advisory 1%, Severe Thunderstorm Warning 1%, Flood Watch 1%, Rip Current Statement 0%

STATUS: Actual 100%, Test 0%

MESSAGE_TYPE: Update 52%, Alert 48%

SEVERITY: Severe 37%, Moderate 28%, Minor 21%, Unknown 14%

CERTAINTY: Likely 75%, Unknown 14%, Observed 10%, Possible 1%

URGENCY: Expected 75%, Unknown 14%, Immediate 8%, Future 3%, Past 0%

GEOMETRY: {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%, {"type": "Polygon", "coordinat 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 286 | 0 | https://api.weather.gov/a 2; https://api.weather.gov/a 2; https://api.weather.gov/a 2; https://api.weather.gov/a 2 |
| TYPE | who | 1 | 0 | Feature 287 |
| EVENT | category | 17 | 0 | Heat Advisory 74; Extreme Heat Warning 64; Small Craft Advisory 58; Air Quality Alert 38 |
| STATUS | category | 2 | 0 | Actual 286; Test 1 |
| MESSAGE_TYPE | category | 2 | 0 | Update 149; Alert 138 |
| SEVERITY | category | 4 | 0 | Severe 107; Moderate 79; Minor 61; Unknown 40 |
| CERTAINTY | category | 4 | 0 | Likely 216; Unknown 39; Observed 28; Possible 4 |
| URGENCY | category | 5 | 0 | Expected 215; Unknown 39; Immediate 24; Future 8 |
| AREA_DESC | other | 226 | 0 | Nikolski to Seguam Pacifi 3; Seguam to Adak Pacific Si 3; Cape Tolstoi to Unalga Pa 3; Sitkinak to Castle Cape f 3 |
| SENT | date | 114 | 0 | 2026-07-02T02:48:00-08:00 15; 2026-07-01T14:45:00-08:00 11; 2026-07-02T12:45:00-04:00 11; 2026-07-01T02:12:00-08:00 9 |
| EFFECTIVE | date | 113 | 0 | 2026-07-02T02:48:00-08:00 15; 2026-07-01T14:45:00-08:00 11; 2026-07-02T12:45:00-04:00 11; 2026-07-01T02:12:00-08:00 9 |
| ONSET | date | 127 | 1 | 2026-07-02T05:00:00-08:00 11; 2026-07-01T15:45:00-04:00 9; 2026-07-01T02:00:00-08:00 8; 2026-07-02T17:00:00-08:00 8 |
| EXPIRES | date | 90 | 0 | 2026-07-02T20:45:00-04:00 18; 2026-07-02T17:00:00-04:00 16; 2026-07-02T15:30:00-08:00 15; 2026-07-03T00:00:00-04:00 13 |
| ENDS | date | 65 | 47 | 2026-07-03T20:00:00-04:00 41; 2026-07-04T20:00:00-04:00 23; 2026-07-02T20:00:00-04:00 21; 2026-07-02T17:00:00-08:00 20 |
| HEADLINE | other | 184 | 1 | Small Craft Advisory issu 9; Air Quality Alert issued  9; Small Craft Advisory issu 7; Small Craft Advisory issu 7 |
| DESCRIPTION | other | 252 | 0 | Coastal Waters Forecast f 35; ...The Flood Warning is e 6; Coastal Waters Forecast f 5; * WHAT...For the first Ex 5 |
| INSTRUCTION | who | 63 | 87 | Drink plenty of fluids, s 50; Drink plenty of fluids, s 37; Drink plenty of fluids, s 16; Drink plenty of fluids, s 12 |
| SENDER_NAME | who | 74 | 0 | NWS Anchorage AK 40; NWS Mount Holly NJ 17; NWS Baltimore MD/Washingt 14; NWS La Crosse WI 14 |
| ZONE_UGC | other | 226 | 0 | https://api.weather.gov/z 3; https://api.weather.gov/z 3; https://api.weather.gov/z 3; https://api.weather.gov/z 3 |
| GEOMETRY | category | 32 | 256 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| STATION_ID | empty | 1 | 287 |  |
| TEMPERATURE | empty | 1 | 287 |  |
| WIND_SPEED | empty | 1 | 287 |  |
| WIND_DIRECTION | empty | 1 | 287 |  |
| TIMESTAMP | empty | 1 | 287 |  |
| FORECAST_OFFICE | empty | 1 | 287 |  |
| GRID_X | empty | 1 | 287 |  |
| GRID_Y | empty | 1 | 287 |  |
| LATITUDE | empty | 1 | 287 |  |
| LONGITUDE | empty | 1 | 287 |  |
| FIPS_CODE | empty | 1 | 287 |  |
| ZIP_CODE | empty | 1 | 287 |  |
| _INGESTED_AT | audit | 1 | 0 | 1783012955291511 287 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 9649aa6f-5451-4a76-9f2d-e 287 |
| _SRC_SHA256 | who | 1 | 0 | 88fc93cb93895d59694aa3359 287 |
