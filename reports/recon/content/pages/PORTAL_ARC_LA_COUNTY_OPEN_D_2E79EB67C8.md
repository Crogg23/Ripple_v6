# PORTAL_ARC_LA_COUNTY_OPEN_D_2E79EB67C8

rows 2.0K  columns 32  scan 3.5s

roles: amount 3, audit 2, category 3, date 3, id 5, other 8, who 9

## when

CREATIONDATE
  2024      2.0K  ##############################

EDITDATE
  2024      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2.0K | 33.80 | 33.97 | 34.07 | 34.08 | 67.9K |
| LONGITUDE | 2.0K | -118.47 | -118.33 | -118.21 | -118.19 | -236.7K |
| OVERALL_INDEX | 1.9K | 0.04 | 59.04 | 99.68 | 100 | 106.0K |

## who

LOCATION_NAME by rows
        29  Dollar Tree
        17  Ross Stores
        16  Goodwill Industries
        12  GameStop
        11  99 Cents Only Stores
         9  Big 5 Sporting Goods
         7  Petco
         7  Family Dollar Stores
         6  Follett Higher Education Group
         6  Big Lots Stores
         5  PetSmart
         5  Five Below
         5  Edible Arrangements
         4  Party City
         4  Costco
         3  Centinela Feed & Pet Supplies
         3  Barnes and Noble
         3  Burn The Ships Electrics
         3  Macy's
         3  Michaels Stores

LOCATION_NAME by dollars
      983.91       29 rows  Dollar Tree
      577.05       17 rows  Ross Stores
      543.01       16 rows  Goodwill Industries
      407.38       12 rows  GameStop
      373.09       11 rows  99 Cents Only Stores
      305.53        9 rows  Big 5 Sporting Goods
      237.75        7 rows  Family Dollar Stores
      237.72        7 rows  Petco
      203.83        6 rows  Follett Higher Education Group
      203.52        6 rows  Big Lots Stores
      169.76        5 rows  PetSmart
      169.66        5 rows  Edible Arrangements
      169.49        5 rows  Five Below
      135.75        4 rows  Costco
      135.75        4 rows  Party City
      101.95        3 rows  Barnes and Noble
      101.89        3 rows  Michaels Stores
      101.81        3 rows  Centinela Feed & Pet Supplies
      101.76        3 rows  Macy's
      101.52        3 rows  Burn The Ships Electrics

STREET_NAME by rows
        97  Western
        77  Sepulveda
        69  Wilshire
        64  Washington
        64  Vermont
        52  Hawthorne
        48  Pico
        47  Crenshaw
        43  Rosecrans
        38  La Brea
        36  Pacific Coast
        36  La Cienega
        36  Avalon
        36  Jefferson
        35  Olympic
        31  Broadway
        29  Florence
        29  Manchester
        29  Artesia
        29  Slauson

STREET_NAME by dollars
        3.3K       97 rows  Western
        2.6K       77 rows  Sepulveda
        2.4K       69 rows  Wilshire
        2.2K       64 rows  Washington
        2.2K       64 rows  Vermont
        1.8K       52 rows  Hawthorne
        1.6K       48 rows  Pico
        1.6K       47 rows  Crenshaw
        1.5K       43 rows  Rosecrans
        1.3K       38 rows  La Brea
        1.2K       36 rows  La Cienega
        1.2K       36 rows  Jefferson
        1.2K       36 rows  Avalon
        1.2K       36 rows  Pacific Coast
        1.2K       35 rows  Olympic
        1.1K       31 rows  Broadway
      985.71       29 rows  Slauson
      985.13       29 rows  Florence
      984.84       29 rows  Manchester
      982.25       29 rows  Artesia

TRACTCE by rows
        39  980028
        29  541003
        27  602900
        25  212502
        24  621204
        24  703003
        24  702600
        23  702400
        22  620601
        19  702801
        19  702900
        18  214501
        17  211000
        17  292001
        16  293205
        16  621326
        15  278001
        15  217200
        15  702803
        14  620102

TRACTCE by dollars
        1.3K       39 rows  980028
      982.59       29 rows  541003
      915.60       27 rows  602900
      851.48       25 rows  212502
      815.89       24 rows  702600
      815.76       24 rows  703003
      812.28       24 rows  621204
      782.59       23 rows  702400
      745.14       22 rows  620601
      646.24       19 rows  702801
      645.56       19 rows  702900
      613.28       18 rows  214501
      579.14       17 rows  211000
      575.54       17 rows  292001
      541.12       16 rows  621326
      541.11       16 rows  293205
      510.75       15 rows  217200
      509.91       15 rows  702803
      509.39       15 rows  278001
      476.39       14 rows  219700

BRANDS by rows
        29  Dollar Tree
        17  Ross Stores
        16  Goodwill Industries
        12  GameStop
        11  99 Cents Only Stores
         9  Big 5 Sporting Goods
         7  Petco
         7  Family Dollar Stores
         6  Big Lots Stores
         5  PetSmart
         5  Edible Arrangements
         5  Five Below
         4  Walmart
         4  Party City
         4  Costco
         3  Centinela Feed & Pet Supplies
         3  Michaels Stores
         3  Macy's
         3  Barnes and Noble
         2  Paper Source

BRANDS by dollars
      983.91       29 rows  Dollar Tree
      577.05       17 rows  Ross Stores
      543.01       16 rows  Goodwill Industries
      407.38       12 rows  GameStop
      373.09       11 rows  99 Cents Only Stores
      305.53        9 rows  Big 5 Sporting Goods
      237.75        7 rows  Family Dollar Stores
      237.72        7 rows  Petco
      203.52        6 rows  Big Lots Stores
      169.76        5 rows  PetSmart
      169.66        5 rows  Edible Arrangements
      169.49        5 rows  Five Below
      135.75        4 rows  Costco
      135.75        4 rows  Party City
      135.52        4 rows  Walmart
      101.95        3 rows  Barnes and Noble
      101.89        3 rows  Michaels Stores
      101.81        3 rows  Centinela Feed & Pet Supplies
      101.76        3 rows  Macy's
       67.93        2 rows  DAISO

## who x when

LOCATION_NAME by CREATIONDATE, dollars = LATITUDE
  99 Cents Only Stores                      2024:373.09
  Barnes and Noble                          2024:101.95
  Big 5 Sporting Goods                      2024:305.53
  Big Lots Stores                           2024:203.52
  Burn The Ships Electrics                  2024:101.52
  Centinela Feed & Pet Supplies             2024:101.81
  Costco                                    2024:135.75
  Dollar Tree                               2024:983.91
  Edible Arrangements                       2024:169.66
  Family Dollar Stores                      2024:237.75
  Five Below                                2024:169.49
  Follett Higher Education Group            2024:203.83
  GameStop                                  2024:407.38
  Goodwill Industries                       2024:543.01
  Macy's                                    2024:101.76
  Michaels Stores                           2024:101.89
  Party City                                2024:135.75
  PetSmart                                  2024:169.76
  Petco                                     2024:237.72
  Ross Stores                               2024:577.05

STREET_NAME by CREATIONDATE, dollars = LATITUDE
  Artesia                                   2024:982.25
  Avalon                                    2024:1.2K
  Broadway                                  2024:1.1K
  Crenshaw                                  2024:1.6K
  Florence                                  2024:985.13
  Hawthorne                                 2024:1.8K
  Jefferson                                 2024:1.2K
  La Brea                                   2024:1.3K
  La Cienega                                2024:1.2K
  Manchester                                2024:984.84
  Olympic                                   2024:1.2K
  Pacific Coast                             2024:1.2K
  Pico                                      2024:1.6K
  Rosecrans                                 2024:1.5K
  Sepulveda                                 2024:2.6K
  Slauson                                   2024:985.71
  Vermont                                   2024:2.2K
  Washington                                2024:2.2K
  Western                                   2024:3.3K
  Wilshire                                  2024:2.4K

## what

CITY: Los Angeles 53%, Gardena 8%, Culver City 6%, Redondo Beach 6%, Inglewood 6%, Carson 4%, Hawthorne 4%, Compton 3%, Torrance 3%, Manhattan Beach 3%, El Segundo 2%, Marina del Rey 2%

NAICS_CODE: 451110 14%, 453110 13%, 453991 11%, 4539 10%, 451120 8%, 453920 8%, 451211 7%, 452319 7%, 453910 7%, 453310 6%, 453210 5%, 451130 5%

INDEX_CATEGORY: HIGHEST 26%, HIGH 20%, LOWEST 18%, MODERATE 17%, LOW 16%, nan 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| LOCATION_NAME | who | 1.8K | 0 | Dollar Tree 35; Ross Stores 25; Goodwill Industries 23; GameStop 19 |
| STREET_ADDRESS | other | 1.8K | 0 | 380 World Way 12; 6000 Sepulveda Blvd 11; 2701 S Western Ave 11; 6333 W 3rd St 11 |
| STREET_NAME | who | 342 | 1 | Western 97; Sepulveda 77; Wilshire 69; Washington 64 |
| CITY | category | 36 | 0 | Los Angeles 1.0K; Gardena 155; Culver City 113; Redondo Beach 104 |
| REGION | other | 1 | 0 | CA 2.0K |
| POSTAL_CODE | other | 72 | 0 | 90045 96; 90019 79; 90230 74; 90006 74 |
| NAICS_CODE | category | 23 | 0 | 451110 231; 453110 216; 453991 193; 4539 166 |
| BRANDS | who | 60 | 1.8K | Dollar Tree 29; Ross Stores 17; Goodwill Industries 16; GameStop 12 |
| PHONE_NUMBER | other | 1.5K | 374 | +15597312767 10; +12132632551 9; +13103994567 9; +14242478509 9 |
| SOURCE | who | 1 | 0 | SafeGraph 2.0K |
| SAFEGRAPH_PLACE_ID | id | 2.0K | 0 | 22d-222@5z5-3qs-rff 10; zzw-236@5z4-zxh-b49 10; zzy-223@5z6-3gq-f75 10; 228-25y@5z4-zxh-d9z 10 |
| DESC | other | 1.8K | 0 | location_name, 380 World  12; location_name, 6000 Sepul 11; location_name, 2701 S Wes 11; location_name, 6333 W 3rd 11 |
| LATITUDE | amount | 2.0K | 0 | 34.06929500037106 10; 33.98515799983961 10; 33.87163900008867 10; 33.98545100030511 10 |
| LONGITUDE | amount | 2.0K | 0 | -118.3521559999454 11; -118.293326000335 10; -118.39475199967741 10; -118.35503999984255 10 |
| CREATIONDATE | date | 1 | 0 | 1716581059678 2.0K |
| CREATOR | who | 1 | 0 | JDiaz2@isd.lacounty.gov_l 2.0K |
| EDITDATE | date | 1 | 0 | 1716581059678 2.0K |
| EDITOR | who | 1 | 0 | JDiaz2@isd.lacounty.gov_l 2.0K |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| JOIN_COUNT | other | 1 | 0 | 1 2.0K |
| TARGET_FID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| TRACTCE | who | 407 | 0 | 980028 39; 541003 29; 602900 27; 212502 25 |
| GEOID | who | 403 | 0 | 06037980028 39; 06037541003 29; 06037602900 27; 06037212502 25 |
| GEO_ID_FULL | other | 409 | 0 | 1400000US06037980028 39; 1400000US06037541003 29; 1400000US06037602900 27; 1400000US06037212502 25 |
| GEO_ID | other | 409 | 0 | 1400000US06037980028 39; 1400000US06037541003 29; 1400000US06037602900 27; 1400000US06037212502 25 |
| OVERALL_INDEX | amount | 404 | 0 | nan 53; 59.32066 29; 73.99919 27; 54.87262 25 |
| INDEX_CATEGORY | category | 6 | 0 | HIGHEST 527; HIGH 399; LOWEST 353; MODERATE 345 |
| GEOMETRY | id | 2.1K | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:32:36.44083 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6c800bcd-dae6-407a-8740-5 2.0K |
| SRC_SHA256 | who | 1 | 0 | fce6540cd9600052d249588b1 2.0K |
