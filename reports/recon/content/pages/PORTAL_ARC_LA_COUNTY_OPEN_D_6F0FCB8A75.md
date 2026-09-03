# PORTAL_ARC_LA_COUNTY_OPEN_D_6F0FCB8A75

rows 411  columns 28  scan 4.3s

roles: amount 1, audit 2, category 10, date 1, empty 1, other 9, who 5

## when

INGESTED_AT
  2026       411  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 411 | 85 | 100 | 100 | 100 | 40.9K |

## who

CONAME by rows
        10  COUNTY OF LOS ANGELES
         6  LOS ANGELES COUNTY LIBRARY
         4  LOS ANGELES PUBLIC LIBRARY
         3  CITY OF PASADENA
         3  CITY OF LOS ANGELES
         2  PASADENA PUBLIC LIBRARY
         2  LAKE VIEW TERRACE LIBRARY
         2  I AM LIBRARY & INSTRUMENTS
         2  BEVERLY HILLS PUBLIC LIBRARY
         2  MARK TWAIN PUBLIC LIBRARY
         2  REDONDO BEACH PUBLIC LIBRARY
         2  CERRITOS PUBLIC LIBRARY
         2  CHARLES E YOUNG LIBRARY
         2  LOS ANGELES COUNTY
         2  PENINSULA CENTER LIBRARY
         1  EDENDALE PUBLIC LIBRARY
         1  WATTS BRANCH LIBRARY
         1  HAWAIIAN GARDENS PUBL LIBRARY
         1  CROWELL PUBLIC LIBRARY
         1  SPOTLIGHTING SUPPLIES

CONAME by dollars
        1.0K       10 rows  COUNTY OF LOS ANGELES
      586.94        6 rows  LOS ANGELES COUNTY LIBRARY
         400        4 rows  LOS ANGELES PUBLIC LIBRARY
         300        3 rows  CITY OF LOS ANGELES
         300        3 rows  CITY OF PASADENA
         200        2 rows  REDONDO BEACH PUBLIC LIBRARY
         200        2 rows  CERRITOS PUBLIC LIBRARY
         200        2 rows  PASADENA PUBLIC LIBRARY
         200        2 rows  I AM LIBRARY & INSTRUMENTS
         200        2 rows  PENINSULA CENTER LIBRARY
         200        2 rows  MARK TWAIN PUBLIC LIBRARY
         200        2 rows  BEVERLY HILLS PUBLIC LIBRARY
         200        2 rows  LAKE VIEW TERRACE LIBRARY
      199.34        2 rows  LOS ANGELES COUNTY
      185.50        2 rows  CHARLES E YOUNG LIBRARY
         100        1 rows  PACOIMA BRANCH LIBRARY
         100        1 rows  EL SEGUNDO PUBLIC LIBRARY
         100        1 rows  CROWELL PUBLIC LIBRARY
         100        1 rows  WILMINGTON PUBLIC LIBRARY
         100        1 rows  SIGNAL HILL PUBLIC LIBRARY

STATE_NAME by rows
       411  California

STATE_NAME by dollars
       40.9K      411 rows  California

SOURCE by rows
       411  INFOGROUP

SOURCE by dollars
       40.9K      411 rows  INFOGROUP

CITY by rows
       126  LOS ANGELES
        23  PASADENA
        19  LONG BEACH
        11  WHITTIER
         8  GLENDALE
         8  COMMERCE
         6  BURBANK
         5  SANTA MONICA
         5  BEVERLY HILLS
         5  TORRANCE
         5  CARSON
         5  NORTHRIDGE
         5  CLAREMONT
         4  ALTADENA
         4  SOUTH GATE
         4  REDONDO BEACH
         4  INGLEWOOD
         4  NORTH HOLLYWOOD
         4  NORWALK
         3  DOWNEY

CITY by dollars
       12.4K      126 rows  LOS ANGELES
        2.3K       23 rows  PASADENA
        1.9K       19 rows  LONG BEACH
        1.1K       11 rows  WHITTIER
         800        8 rows  GLENDALE
         800        8 rows  COMMERCE
         600        6 rows  BURBANK
         500        5 rows  SANTA MONICA
         500        5 rows  TORRANCE
         500        5 rows  BEVERLY HILLS
         500        5 rows  CARSON
         500        5 rows  CLAREMONT
      498.50        5 rows  NORTHRIDGE
         400        4 rows  REDONDO BEACH
         400        4 rows  NORWALK
         400        4 rows  ALTADENA
         400        4 rows  NORTH HOLLYWOOD
         400        4 rows  INGLEWOOD
         400        4 rows  SOUTH GATE
         300        3 rows  LA PUENTE

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  BEVERLY HILLS PUBLIC LIBRARY              2026:200
  CERRITOS PUBLIC LIBRARY                   2026:200
  CHARLES E YOUNG LIBRARY                   2026:185.50
  CITY OF LOS ANGELES                       2026:300
  CITY OF PASADENA                          2026:300
  COUNTY OF LOS ANGELES                     2026:1.0K
  CROWELL PUBLIC LIBRARY                    2026:100
  EDENDALE PUBLIC LIBRARY                   2026:100
  EL SEGUNDO PUBLIC LIBRARY                 2026:100
  HAWAIIAN GARDENS PUBL LIBRARY             2026:100
  I AM LIBRARY & INSTRUMENTS                2026:200
  LAKE VIEW TERRACE LIBRARY                 2026:200
  LOS ANGELES COUNTY                        2026:199.34
  LOS ANGELES COUNTY LIBRARY                2026:586.94
  LOS ANGELES PUBLIC LIBRARY                2026:400
  MARK TWAIN PUBLIC LIBRARY                 2026:200
  PACOIMA BRANCH LIBRARY                    2026:100
  PASADENA PUBLIC LIBRARY                   2026:200
  PENINSULA CENTER LIBRARY                  2026:200
  REDONDO BEACH PUBLIC LIBRARY              2026:200
  SIGNAL HILL PUBLIC LIBRARY                2026:100
  SPOTLIGHTING SUPPLIES                     2026:100
  WATTS BRANCH LIBRARY                      2026:100
  WILMINGTON PUBLIC LIBRARY                 2026:100

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:40.9K

## what

NAICS: 51912006 88%, 51912005 12%

SIC: 823106 88%, 823109 12%

HDBRCH: 2 92%, 3 7%, 1 2%

ULTNUM: 902119213 50%, 000000000 40%, 450081187 4%, 678650441 2%, 678650599 1%, 001434976 1%, 738105694 0%, 902121110 0%, 741709740 0%, 906739032 0%, 748247212 0%, 488940388 0%

FRNCOD: P 91%, C 9%, J 0%

ISCODE: 3 42%, 4 27%, 5 21%, 6 3%, 7 3%, 2 3%, 1 1%

SQFTCODE: 7 43%, 6 23%, 8 22%, 5 5%, 4 4%, 3 1%, 2 1%, 1 1%

LOC_NAME: PointAddress 67%, StreetAddress 25%, Postal 3%, Subaddress 3%, StreetName 1%, PostalExt 1%

STATUS: M 99%, T 1%

REC_TYPE: 0 99%, 2 0%, 1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 409 | 0 | 411 3; 410 3; 409 3; 408 3 |
| LOCNUM | other | 401 | 0 | 995710084 3; 987859436 3; 984899708 3; 984896712 3 |
| CONAME | who | 377 | 0 | COUNTY OF LOS ANGELES 10; LOS ANGELES COUNTY LIBRAR 6; CITY OF LOS ANGELES 4; LOS ANGELES PUBLIC LIBRAR 4 |
| STREET | other | 316 | 2 | SANTA MONICA BLVD 7; TROUSDALE PKWY 6; NORDHOFF ST 5; IMPERIAL HWY 4 |
| CITY | who | 118 | 0 | LOS ANGELES 126; PASADENA 23; LONG BEACH 19; WHITTIER 11 |
| STATE | other | 1 | 0 | CA 411 |
| STATE_NAME | who | 1 | 0 | California 411 |
| ZIP | other | 221 | 0 | 90095 19; 90089 10; 90040 7; 90012 6 |
| ZIP4 | other | 338 | 12 | 0001 19; 8200 4; 3605 3; 1832 3 |
| NAICS | category | 2 | 0 | 51912006 361; 51912005 50 |
| SIC | category | 2 | 0 | 823106 361; 823109 50 |
| SALESVOL | other | 1 | 0 | 0 411 |
| HDBRCH | category | 4 | 166 | 2 225; 3 16; 1 4 |
| ULTNUM | category | 12 | 0 | 902119213 206; 000000000 166; 450081187 16; 678650441 7 |
| PUBPRV | empty | 1 | 411 |  |
| EMPNUM | other | 55 | 0 | 10 112; 6 31; 8 19; 13 19 |
| FRNCOD | category | 4 | 151 | P 236; C 23; J 1 |
| ISCODE | category | 8 | 311 | 3 42; 4 27; 5 21; 6 3 |
| SQFTCODE | category | 8 | 0 | 7 177; 6 93; 8 90; 5 20 |
| LOC_NAME | category | 6 | 0 | PointAddress 274; StreetAddress 101; Postal 14; Subaddress 13 |
| STATUS | category | 2 | 0 | M 407; T 4 |
| SCORE | amount | 17 | 0 | 100.0 378; 86.0 12; 99.5 4; 99.890625 3 |
| SOURCE | who | 1 | 0 | INFOGROUP 411 |
| REC_TYPE | category | 3 | 0 | 0 407; 2 2; 1 2 |
| GEOMETRY | other | 345 | 0 | {"type": "Point", "coordi 12; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4; {"type": "Point", "coordi 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:23:49.40334 411 |
| SOURCE_RUN_ID | audit | 1 | 0 | decb4419-cefb-458f-b9ce-8 411 |
| SRC_SHA256 | who | 1 | 0 | 55168a661d26707c45896fa9e 411 |
