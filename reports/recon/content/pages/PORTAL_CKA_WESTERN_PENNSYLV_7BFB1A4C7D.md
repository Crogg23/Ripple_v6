# PORTAL_CKA_WESTERN_PENNSYLV_7BFB1A4C7D

rows 70  columns 15  scan 4.3s

roles: amount 2, audit 2, category 4, date 1, empty 1, other 3, who 3

## when

INGESTED_AT
  2026        70  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 70 | 40.23 | 40.45 | 40.66 | 40.67 | 2.8K |
| LONGITUDE | 70 | -80.23 | -79.95 | -79.71 | -79.71 | -5.6K |

## who

MARKET_NAME by rows
         1  Farmers Market on the Mount
         1  Plum Borough Farmers Market
         1  Olde World Produce
         1  Farmers Market Cooperative of East Liberty
         1  BEDNERS FARM MARKET
         1  Sturges Orchards
         1  East End Farmers Market
         1  Pittsburgh Urban Garden Project
         1  Pittsburgh Market Square
         1  Verona Farmers Market
         1  Duda's Farm Market
         1  Blackberry Meadows Farm
         1  Kaelin Farms Market
         1  Mt Lebanon Farmers Market
         1  Homewood Farmers Market
         1  Merritt Farmers Market
         1  Farmers Market at The Block
         1  Bethel Park Farmers Market
         1  Dillner Family Farm
         1  Bloomfield Farmers Market

MARKET_NAME by dollars
       40.67        1 rows  Dillner Family Farm
       40.66        1 rows  Pine Community Park Farmers Market
       40.66        1 rows  Blackberry Meadows Farm
       40.65        1 rows  Harvest Valley Farm Market & Bakery
       40.65        1 rows  Wexford Farms
       40.64        1 rows  Bachman's Farm Market
       40.63        1 rows  Shenot Farm Market
       40.63        1 rows  Janoski's Farm
       40.62        1 rows  Dillner Family Farm Market
       40.62        1 rows  Soergel Orchards
       40.61        1 rows  Eichner's Farm Market & Greenhouses
       40.61        1 rows  Kaelin Farms Market
       40.60        1 rows  Tarentum
       40.58        1 rows  Hampton Farmers Market
       40.55        1 rows  Farmers Market at The Block
       40.54        1 rows  Sewickley Farmers Market
       40.53        1 rows  Ross Township Farmers Market
       40.53        1 rows  Mazur's Farm Stand
       40.52        1 rows  Northside Farmers Market
       40.52        1 rows  Oakmont Farmers Market

COUNTY by rows
        70  Allegheny

COUNTY by dollars
        2.8K       70 rows  Allegheny

SRC_SHA256 by rows
        70  944fb0cf5d8f4658ef4a1dfb136519ea21a462b39094eae069549aecdd47001c

SRC_SHA256 by dollars
        2.8K       70 rows  944fb0cf5d8f4658ef4a1dfb136519ea21a462b39094eae069549aecdd47

## who x when

MARKET_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  BEDNERS FARM MARKET                       2026:40.36
  Bachman's Farm Market                     2026:40.64
  Bethel Park Farmers Market                2026:40.32
  Blackberry Meadows Farm                   2026:40.66
  Bloomfield Farmers Market                 2026:40.46
  Dillner Family Farm                       2026:40.67
  Dillner Family Farm Market                2026:40.62
  Duda's Farm Market                        2026:40.36
  East End Farmers Market                   2026:40.46
  Eichner's Farm Market & Greenhouses       2026:40.61
  Farmers Market Cooperative of East Liber  2026:40.46
  Farmers Market at The Block               2026:40.55
  Farmers Market on the Mount               2026:40.43
  Harvest Valley Farm Market & Bakery       2026:40.65
  Homewood Farmers Market                   2026:40.45
  Janoski's Farm                            2026:40.63
  Kaelin Farms Market                       2026:40.61
  Merritt Farmers Market                    2026:40.23
  Mt Lebanon Farmers Market                 2026:40.37
  Olde World Produce                        2026:40.31
  Pine Community Park Farmers Market        2026:40.66
  Pittsburgh Market Square                  2026:40.44
  Pittsburgh Urban Garden Project           2026:40.44
  Plum Borough Farmers Market               2026:40.48
  Shenot Farm Market                        2026:40.63
  Soergel Orchards                          2026:40.62
  Sturges Orchards                          2026:40.45
  Tarentum                                  2026:40.60
  Verona Farmers Market                     2026:40.51
  Wexford Farms                             2026:40.65

COUNTY by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Allegheny                                 2026:2.8K

## what

MARKET_TYPE: Farm Market 66%, Farm Stand 34%

CITY: Pittsburgh 50%, Wexford 14%, Elizabeth 7%, Gibsonia 5%, Natrona Heights 5%, PITTSBURGH 5%, Oakdale 2%, McDonald 2%, Monroeville 2%, Moon Township 2%, Clinton 2%, Monongahela 2%

ZIP_CODE: 15090 20%, 15222 10%, 15037 10%, 15237 7%, 15220 7%, 15206 7%, 15212 7%, 15203 7%, 15221 7%, 15228 7%, 15044 7%, 15224 7%

PHONE: 7248993438 14%, 7243391709 14%, 7244446594 14%, 4122218768 7%, 7245388621 7%, 7249352131 7%, 4122552539 7%, 4122621700 7%, 7242583557 7%, 7247528920 7%, 7249351743 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| MARKET_ID | other | 71 | 0 | 21 1; 4296 1; 4240 1; 4208 1 |
| MARKET_TYPE | category | 2 | 0 | Farm Market 46; Farm Stand 24 |
| MARKET_NAME | who | 70 | 0 | Beccari's Farm Market 1; Mazur's Farm Stand 1; Strip District Terminal 1; Pine Community Park Farme 1 |
| ADDRESS1 | other | 71 | 0 | 5095 Thomas Run Road 1; 3333 Babcock Blvd 1; Smallman St 1; 200 Pine Park Dr 1 |
| CITY | category | 40 | 0 | Pittsburgh 21; Wexford 6; Elizabeth 3; Gibsonia 2 |
| STATE | other | 1 | 0 | PA 70 |
| ZIP_CODE | category | 47 | 0 | 15090 6; 15222 3; 15037 3; 15237 2 |
| LATITUDE | amount | 70 | 0 | 40.3753878 1; 40.5336062 1; 40.4519411 1; 40.6617072 1 |
| LONGITUDE | amount | 70 | 0 | -80.1353771 1; -80.0192544 1; -79.9844127 1; -80.0346603 1 |
| PHONE | category | 21 | 47 | 7248993438 2; 7243391709 2; 7244446594 2; 4122218768 1 |
| PHONE_EXT | empty | 1 | 70 |  |
| COUNTY | who | 1 | 0 | Allegheny 70 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:23.81056 70 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7e7f1b33-057c-4223-a47e-5 70 |
| SRC_SHA256 | who | 1 | 0 | 944fb0cf5d8f4658ef4a1dfb1 70 |
