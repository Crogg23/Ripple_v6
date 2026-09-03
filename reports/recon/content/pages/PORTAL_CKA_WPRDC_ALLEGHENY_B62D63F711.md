# PORTAL_CKA_WPRDC_ALLEGHENY_B62D63F711

rows 585  columns 26  scan 3.6s

roles: amount 1, audit 2, category 16, date 1, other 4, who 3

## when

INGESTED_AT
  2026       585  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MILEAGE | 585 | 0 | 0.10 | 4.31 | 9.41 | 216.19 |

## who

TRAIL_NAME by rows
         9  Green
         9  Red
         7  Blue
         7  Corrigan Drive Trail
         6  Yellow
         6  Purple
         6  White
         6  Orange
         3  Yellow Access
         2  Orange with White Dot
         2  Irwin Rd Trail
         2  Blue Loop
         2  White with Black Dot
         2  Blue Loop Access
         2  White with Red Dot
         1  Yellow Loop West
         1  Paved Access to Paved Trail
         1  Red Loop Trail
         1  Park Office Service Road
         1  Picnic Loop Road Trail Cross Loop Connector

TRAIL_NAME by dollars
       30.12        9 rows  Red
       14.56        9 rows  Green
       12.31        6 rows  White
       10.99        7 rows  Blue
       10.86        6 rows  Yellow
       10.56        6 rows  Orange
        8.95        1 rows  Rachel Carson Trail
        7.13        6 rows  Purple
        4.97        1 rows  Lake Loop
        3.17        2 rows  Blue Loop
        2.43        2 rows  White with Red Dot
        2.32        7 rows  Corrigan Drive Trail
        2.24        1 rows  Orange Trail - South
        2.22        1 rows  Montour Trail Connector 
        2.21        1 rows  Picnic Loop Paved Trail
        1.73        1 rows  Red Loop Trail
        1.68        1 rows  Gazebo Paved Trail Network - Corrigan Spur
        1.60        1 rows  Blue with Red Dot
        1.58        2 rows  Irwin Rd Trail
        1.24        1 rows  Blue with Yellow Dot

TRAIL_STATUS by rows
       585  Active

TRAIL_STATUS by dollars
      216.19      585 rows  Active

SRC_SHA256 by rows
       585  28e1e458dc0ff59645c5abc5668c21883e356439ca57cdbeb4ef2b8ccbdab566

SRC_SHA256 by dollars
      216.19      585 rows  28e1e458dc0ff59645c5abc5668c21883e356439ca57cdbeb4ef2b8ccbda

## who x when

TRAIL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = MILEAGE
  Blue                                      2026:10.99
  Blue Loop                                 2026:3.17
  Blue Loop Access                          2026:0.12
  Blue with Red Dot                         2026:1.60
  Blue with Yellow Dot                      2026:1.24
  Corrigan Drive Trail                      2026:2.32
  Gazebo Paved Trail Network - Corrigan Sp  2026:1.68
  Green                                     2026:14.56
  Irwin Rd Trail                            2026:1.58
  Lake Loop                                 2026:4.97
  Montour Trail Connector                   2026:2.22
  Orange                                    2026:10.56
  Orange Trail - South                      2026:2.24
  Orange with White Dot                     2026:0.54
  Park Office Service Road                  2026:0.56
  Paved Access to Paved Trail               2026:0.09
  Picnic Loop Paved Trail                   2026:2.21
  Picnic Loop Road Trail Cross Loop Connec  2026:0.17
  Purple                                    2026:7.13
  Rachel Carson Trail                       2026:8.95
  Red                                       2026:30.12
  Red Loop Trail                            2026:1.73
  White                                     2026:12.31
  White with Black Dot                      2026:0.78
  White with Red Dot                        2026:2.43
  Yellow                                    2026:10.86
  Yellow Access                             2026:0.35
  Yellow Loop West                          2026:1

TRAIL_STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = MILEAGE
  Active                                    2026:216.19

## what

BASE_COLOR: Gray 37%, Blue 13%, Red 10%, Orange 9%, Green 9%, White 9%, Yellow 8%, Purple 5%, Pink 1%

BLAZE_COLOR_FULL: Gravel or Paved Trail/Road 37%, <Null> 19%, Blue 8%, Red 7%, Green 6%, Yellow 6%, Orange 6%, Purple 4%, White 4%, Gray 3%, White with Black Dot 1%

BLAZE_COLOR_SHORT: GY 39%, <Null> 17%, BL 8%, YL 7%, RD 7%, GN 6%, OR 6%, PL 4%, WT 4%, WT/BK Dot 1%, WT/RD Dot 1%

CAP_COLOR: Red 23%, Blue 23%, White 15%, Green 15%, Yellow 15%, Orange 8%

CONFIGURATION: <Null> 56%, Connector Trail 12%, Point to Point 10%, Complete Loop 10%, Access Trail 10%, Service Road 1%

DASH_COLOR: Black 33%, White 33%, Purple 33%

DIFFICULTY: Easy 36%, Easy-Moderate 33%, Moderate 22%, Moderate-Difficult 7%, Difficult 1%

DOT_COLOR: Red 29%, Black 24%, White 19%, Yellow 14%, Green 10%, Purple 5%

IMAGE_LINK: https://apps.alleghenycounty.u 40%, <Null> 16%, https://apps.alleghenycounty.u 8%, https://apps.alleghenycounty.u 7%, https://apps.alleghenycounty.u 7%, https://apps.alleghenycounty.u 6%, https://apps.alleghenycounty.u 6%, https://apps.alleghenycounty.u 4%, https://apps.alleghenycounty.u 4%, https://apps.alleghenycounty.u 1%, https://apps.alleghenycounty.u 1%

PARK_NAME: North Park 26%, Boyce 19%, South Park 16%, Hartwood Acres 14%, Deer Lakes 11%, Harrison Hills 4%, White Oak 4%, Settlers Cabin 3%, Round Hill 3%

PARK_NAME_FULL: North Park 26%, Boyce Park 19%, South Park 16%, Hartwood Acres 14%, Deer Lakes 11%, Harrison Hills 4%, White Oak Park 4%, Settlers Cabin 3%, Round Hill 3%

PARK_NAME_SHORT: NP 26%, BP 19%, SP 16%, HA 14%, DL 11%, HH 4%, WO 4%, SC 3%, RH 3%

SERVICE_ROAD: No 91%, Yes 9%

SURFACE: Dirt 63%, Asphalt 21%, Grass 6%, Concrete 5%, Crushed Limestone 3%, Reclaimed Asphalt 2%

TRACK: Single 63%, Double 32%, double 3%, single 3%

TRACK_NUM: 1 63%, 2 34%, 11 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BASE_COLOR | category | 10 | 411 | Gray 65; Blue 22; Red 17; Orange 16 |
| BLAZE_COLOR_FULL | category | 45 | 372 | Gravel or Paved Trail/Roa 66; <Null> 33; Blue 14; Red 12 |
| BLAZE_COLOR_SHORT | category | 40 | 375 | GY 71; <Null> 30; BL 14; YL 13 |
| CAP_COLOR | category | 8 | 572 | Red 3; Blue 3; White 2; Green 2 |
| CONFIGURATION | category | 7 | 36 | <Null> 306; Connector Trail 67; Point to Point 57; Complete Loop 56 |
| DASH_COLOR | category | 5 | 582 | Black 1; White 1; Purple 1 |
| DIFFICULTY | category | 6 | 300 | Easy 104; Easy-Moderate 94; Moderate 64; Moderate-Difficult 19 |
| DOT_COLOR | category | 8 | 564 | Red 6; Black 5; White 4; Yellow 3 |
| GLOBALID | other | 587 | 0 | 2f825b34-3c90-47b8-930c-7 3; fbf39ffd-d338-46ee-add5-3 3; 07037a88-7bf0-4cdc-9cae-2 3; 0ceacbb3-5ce6-46b0-a1f6-9 3 |
| IMAGE_LINK | category | 42 | 376 | https://apps.alleghenycou 71; <Null> 29; https://apps.alleghenycou 14; https://apps.alleghenycou 13 |
| MILEAGE | amount | 591 | 0 | 1.38025072 3; 3.1718615 3; 2.439799 3; 1.57133552 3 |
| OBJECTID | other | 585 | 0 | 28797 3; 27871 3; 27863 3; 27642 3 |
| PARK_NAME | category | 9 | 0 | North Park 150; Boyce 113; South Park 92; Hartwood Acres 83 |
| PARK_NAME_FULL | category | 9 | 0 | North Park 150; Boyce Park 113; South Park 92; Hartwood Acres 83 |
| PARK_NAME_SHORT | category | 9 | 0 | NP 150; BP 113; SP 92; HA 83 |
| SERVICE_ROAD | category | 3 | 378 | No 189; Yes 18 |
| SURFACE | category | 7 | 356 | Dirt 144; Asphalt 48; Grass 13; Concrete 12 |
| TRACK | category | 5 | 547 | Single 24; Double 12; double 1; single 1 |
| TRACK_NUM | category | 4 | 547 | 1 24; 2 13; 11 1 |
| TRAIL_ID | other | 586 | 0 | DL68049 3; HH25186 3; SP51971 3; WO45405 3 |
| TRAIL_NAME | who | 125 | 406 | Red 9; Green 9; Corrigan Drive Trail 7; Blue 7 |
| TRAIL_STATUS | who | 1 | 0 | Active 585 |
| GEOMETRY | other | 594 | 0 | LINESTRING (599648.031302 3; MULTILINESTRING ((609296. 3; LINESTRING (584851.361516 3; LINESTRING (603191.108495 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:43:53.59292 585 |
| SOURCE_RUN_ID | audit | 1 | 0 | 54b1688e-312f-46a4-ab80-4 585 |
| SRC_SHA256 | who | 1 | 0 | 28e1e458dc0ff59645c5abc56 585 |
