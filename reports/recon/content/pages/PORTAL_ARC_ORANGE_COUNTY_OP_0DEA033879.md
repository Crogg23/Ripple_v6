# PORTAL_ARC_ORANGE_COUNTY_OP_0DEA033879

rows 54  columns 22  scan 4.5s

roles: amount 2, audit 2, category 12, date 1, other 4, who 2

## when

INGESTED_AT
  2026        54  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITIUDE | 54 | 33.46 | 33.56 | 33.69 | 33.69 | 1.8K |
| LONGITUDE | 54 | -117.81 | -117.63 | -117.53 | -117.51 | -6.4K |

## who

BUSINESS_NAME by rows
         1  Mobil Service Station (Circle K)
         1  Las Flores Chevron
         1  Oso Grande Park
         1  Creighton Plunge
         1  Cinnabar Equestrian Operations / Coto de Caza Equestrian Center
         1  Cypress Point Park
         1  Lazy W Ranch Camp
         1  Quest Diagnostics / Nichols Institute (And Cafeteria) 
         1  Town Green
         1  Lapeyre Industrial Sands Inc./P.W. Gillibrand Co
         1  Eton Park
         1  Tree of Life Nursery
         1  Dana Point Shipyard (Industrial)
         1  Wagsdale Park
         1  Canterra Plunge
         1  Las Flores Hand Wash
         1  Avendale Village Club
         1  Township Plunge
         1  Ewles Materials- San Juan Capistrano
         1  Cherry Plunge

BUSINESS_NAME by dollars
       33.69        1 rows  Santiago Ranch Stables (Lease)
       33.69        1 rows  Rancho Las Lomas Wedding Center and Zoo
       33.66        1 rows  TY Nursery
       33.66        1 rows  Sakaida Nursery
       33.63        1 rows  Coto Sports & Recreation Park
       33.62        1 rows  Coto Valley Community/Sports Club
       33.62        1 rows  Cinnabar Equestrian Operations / Coto de Caza Equestrian Cen
       33.60        1 rows  Cypress Point Park
       33.60        1 rows  Lazy W Ranch Camp
       33.60        1 rows  Coto de Caza Country / Golf & Racquet Club (Includes Restaur
       33.59        1 rows  Ronald G. Wells Park 
       33.59        1 rows  Oak Tree Park and Pool
       33.59        1 rows  Starlight Ridge Park
       33.58        1 rows  Las Flores Hand Wash
       33.58        1 rows  Wagon Wheel Sports Park (Santa Margarita Water District)
       33.58        1 rows  Las Flores Chevron
       33.57        1 rows  Oak Knoll Village Club
       33.57        1 rows  Gene's Park
       33.57        1 rows  Cox Sportspark
       33.56        1 rows  Mobil Service Station (Circle K)

SRC_SHA256 by rows
        54  034129e93d15f569b9de02762159ba2bf245c9fae4c4f98893d70e305770887d

SRC_SHA256 by dollars
        1.8K       54 rows  034129e93d15f569b9de02762159ba2bf245c9fae4c4f98893d70e305770

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITIUDE
  Avendale Village Club                     2026:33.55
  Canterra Plunge                           2026:33.55
  Cherry Plunge                             2026:33.55
  Cinnabar Equestrian Operations / Coto de  2026:33.62
  Coto Sports & Recreation Park             2026:33.63
  Coto Valley Community/Sports Club         2026:33.62
  Coto de Caza Country / Golf & Racquet Cl  2026:33.60
  Creighton Plunge                          2026:33.55
  Cypress Point Park                        2026:33.60
  Dana Point Shipyard (Industrial)          2026:33.46
  Eton Park                                 2026:33.55
  Ewles Materials- San Juan Capistrano      2026:33.52
  Lapeyre Industrial Sands Inc./P.W. Gilli  2026:33.50
  Las Flores Chevron                        2026:33.58
  Las Flores Hand Wash                      2026:33.58
  Lazy W Ranch Camp                         2026:33.60
  Mobil Service Station (Circle K)          2026:33.56
  Oak Tree Park and Pool                    2026:33.59
  Oso Grande Park                           2026:33.54
  Quest Diagnostics / Nichols Institute (A  2026:33.56
  Rancho Las Lomas Wedding Center and Zoo   2026:33.69
  Ronald G. Wells Park                      2026:33.59
  Sakaida Nursery                           2026:33.66
  Santiago Ranch Stables (Lease)            2026:33.69
  Starlight Ridge Park                      2026:33.59
  TY Nursery                                2026:33.66
  Town Green                                2026:33.56
  Township Plunge                           2026:33.56
  Tree of Life Nursery                      2026:33.53
  Wagsdale Park                             2026:33.56

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITIUDE
  034129e93d15f569b9de02762159ba2bf245c9fa  2026:1.8K

## what

WDID: <Null> 85%, 930I005780 2%, 930I024451 2%, CA0109313 2%, 930I005771 2%, 930I014449 2%, 930I011101 2%, 930I014441 2%, 930I024079 2%

SIC_CODE: 7999 58%, 7997 12%, 5541 6%, 4952 4%, 5032 4%, 5261 4%, 3732 2%, 2875 2%, 4953 2%, 1446 2%, 8071 2%, 7032 2%

SIC_DESCRIPTION: Amusement and recreation servi 58%, Membership Sports and Recreati 12%, Gasoline service stations 6%, Sewerage systems 4%, Brick, stone and related const 4%, Retail Nurseries 4%, Boat building and repairing 2%, Fertilizers, mixing only 2%, Refuse systems 2%, Industrial sand 2%, Medical Laboratories 2%, Sporting and Recreational Camp 2%

STREET_NUMBER: 1 20%, 600 13%, 28303 7%, 32502 7%, 34671 7%, 28793 7%, 31748 7%, 32501 7%, 31641 7%, 31302 7%, 33608 7%, 23852 7%

CITY: Ladera Ranch 46%, San Juan Capistrano 17%, Coto de Caza 15%, Las Flores 7%, Laguna Beach 4%, Trabuco Canyon 4%, Laguna Niguel 2%, Dana Point 2%, Santiago Canyon 2%, Lake Forest  2%

ZIP: 92694 46%, 92675 17%, 92679 15%, 92688 7%, 92651 4%, 92676 4%, 92678 4%, 92677 2%, 92629 2%

WATERSHED: San Juan Creek 89%, Aliso Creek 6%, Laguna Coastal Streams 4%, Dana Point Coastal Streams 2%

PRIORITY: <Null> 83%, High 17%

INSPECTION_FREQ: Permit Term 83%, Annually 17%

FACILITY_TYPE: Commercial 85%, Industrial 15%

STREET_NAM: Ortega 23%, Sienna 13%, Oso 10%, O'neill 10%, Covenant Hills 7%, Crown Valley 7%, Vista Del Verde 7%, Emerald Bay 7%, Trabuco Canyon 7%, Alicia 3%, Puerto  3%, La Pata 3%

STREET_TYP: Pkwy. 24%, <Null> 20%, Hwy. 14%, Street 12%, Drive 8%, Road 6%, Rd. 6%, Lane 4%, Pkwy 2%, Pl. 2%, Ave. 2%, Parkway 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 54 | 0 | 54 1; 53 1; 52 1; 51 1 |
| REGION | other | 1 | 0 | SDR 54 |
| WDID | category | 9 | 0 | <Null> 46; 930I005780 1; 930I024451 1; CA0109313 1 |
| SIC_CODE | category | 16 | 0 | 7999 29; 7997 6; 5541 3; 4952 2 |
| SIC_DESCRIPTION | category | 16 | 0 | Amusement and recreation  29; Membership Sports and Rec 6; Gasoline service stations 3; Sewerage systems 2 |
| BUSINESS_NAME | who | 54 | 0 | SOCWA - Coastal Treatment 1; Greenstone Materials 1; Dana Point Shipyard (Indu 1; Santa Margarita Water Dis 1 |
| STREET_NUMBER | category | 50 | 0 | 1 3; 600 2; 28303 1; 32502 1 |
| CITY | category | 10 | 0 | Ladera Ranch 25; San Juan Capistrano 9; Coto de Caza 8; Las Flores 4 |
| ZIP | category | 8 | 0 | 92694 25; 92675 9; 92679 8; 92688 4 |
| WATERSHED | category | 4 | 0 | San Juan Creek 48; Aliso Creek 3; Laguna Coastal Streams 2; Dana Point Coastal Stream 1 |
| LATITIUDE | amount | 54 | 0 | 33.51874 1; 33.5195963 1; 33.460474 1; 33.542262 1 |
| LONGITUDE | amount | 54 | 0 | -117.737012 1; -117.5715765 1; -117.69049 1; -117.60839 1 |
| PRIORITY | category | 2 | 0 | <Null> 45; High 9 |
| INSPECTION_FREQ | category | 2 | 0 | Permit Term 45; Annually 9 |
| INVENTORY_ID | other | 54 | 0 | SDR_Exist_Dev_109 1; SDR_Exist_Dev_63 1; SDR_Exist_Dev_61 1; SDR_Exist_Dev_60 1 |
| FACILITY_TYPE | category | 2 | 0 | Commercial 46; Industrial 8 |
| STREET_NAM | category | 36 | 0 | Ortega 7; Sienna 4; Oso 3; O'neill 3 |
| STREET_TYP | category | 15 | 0 | Pkwy. 12; <Null> 10; Hwy. 7; Street 6 |
| GEOMETRY | other | 53 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:23.71729 54 |
| SOURCE_RUN_ID | audit | 1 | 0 | b049b07f-5994-4038-a680-0 54 |
| SRC_SHA256 | who | 1 | 0 | 034129e93d15f569b9de02762 54 |
