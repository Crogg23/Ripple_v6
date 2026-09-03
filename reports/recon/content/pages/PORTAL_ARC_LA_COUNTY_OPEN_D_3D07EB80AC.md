# PORTAL_ARC_LA_COUNTY_OPEN_D_3D07EB80AC

rows 1.4K  columns 32  scan 4.3s

roles: amount 1, audit 2, category 13, date 1, id 3, other 5, who 8

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 1.4K | 85 | 100 | 100 | 100 | 135.4K |

## who

CONAME by rows
        43  RALPHS PHARMACY
        42  WALMART PHARMACY
        32  VONS PHARMACY
        17  ALBERTSONS SAV-ON PHARMACY
        16  COSTCO PHARMACY
         8  SAM'S CLUB PHARMACY
         8  COMMUNITY PHARMACY
         7  MEDICINE SHOPPE PHARMACY
         5  PHARMACY
         5  HORTON & CONVERSE PHARMACY
         5  SAV-ON DRUGS
         4  PAYLESS PHARMACY
         4  SANTA MARIA PHARMACY
         4  AHF PHARMACY
         3  WESTERN DRUG
         3  MEDICINE CABINET
         3  EXPRESS PHARMACY
         3  LA FARMACIA NATURAL
         3  MICKEY FINE PHARMACY
         3  ST LUKE PHARMACY

CONAME by dollars
        4.3K       43 rows  RALPHS PHARMACY
        4.2K       42 rows  WALMART PHARMACY
        3.2K       32 rows  VONS PHARMACY
        1.7K       17 rows  ALBERTSONS SAV-ON PHARMACY
        1.6K       16 rows  COSTCO PHARMACY
         800        8 rows  COMMUNITY PHARMACY
         800        8 rows  SAM'S CLUB PHARMACY
         700        7 rows  MEDICINE SHOPPE PHARMACY
         500        5 rows  SAV-ON DRUGS
         500        5 rows  PHARMACY
         500        5 rows  HORTON & CONVERSE PHARMACY
         400        4 rows  AHF PHARMACY
         400        4 rows  PAYLESS PHARMACY
         386        4 rows  SANTA MARIA PHARMACY
         300        3 rows  ST LUKE PHARMACY
         300        3 rows  MEDICINE CABINET
         300        3 rows  EXPRESS PHARMACY
         300        3 rows  WESTERN DRUG
         300        3 rows  PHARMEDQUEST PHARMACY SVC
         300        3 rows  MICKEY FINE PHARMACY

STATE_NAME by rows
      1.4K  California

STATE_NAME by dollars
      135.4K     1.4K rows  California

NAICS by rows
      1.4K  44611009

NAICS by dollars
      135.4K     1.4K rows  44611009

SIC by rows
      1.4K  591205

SIC by dollars
      135.4K     1.4K rows  591205

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  AHF PHARMACY                              2026:400
  ALBERTSONS SAV-ON PHARMACY                2026:1.7K
  COMMUNITY PHARMACY                        2026:800
  COSTCO PHARMACY                           2026:1.6K
  EXPRESS PHARMACY                          2026:300
  HORTON & CONVERSE PHARMACY                2026:500
  LA FARMACIA NATURAL                       2026:299.89
  MEDICINE CABINET                          2026:300
  MEDICINE SHOPPE PHARMACY                  2026:700
  MICKEY FINE PHARMACY                      2026:300
  PAYLESS PHARMACY                          2026:400
  PHARMACY                                  2026:500
  PHARMEDQUEST PHARMACY SVC                 2026:300
  RALPHS PHARMACY                           2026:4.3K
  SAM'S CLUB PHARMACY                       2026:800
  SANTA MARIA PHARMACY                      2026:386
  SAV-ON DRUGS                              2026:500
  ST LUKE PHARMACY                          2026:300
  VONS PHARMACY                             2026:3.2K
  WALMART PHARMACY                          2026:4.2K
  WESTERN DRUG                              2026:300

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:135.4K

## what

SALESVOL: 1318 50%, 1647 10%, 989 10%, 659 6%, 2306 6%, 1977 6%, 2636 4%, 3294 3%, 330 3%, 2965 1%, 0 1%, 3953 1%

HDBRCH: 2 97%, 1 1%, 3 1%

ULTNUM: 000000000 86%, 579284589 4%, 005889993 4%, 007521503 3%, 441311800 1%, 008288680 1%, 007539588 0%, 709210993 0%, 502590904 0%, 403504888 0%, 004373189 0%, 891326225 0%

PUBPRV: 2 100%

EMPNUM: 4 50%, 5 10%, 3 10%, 7 6%, 2 6%, 6 5%, 8 4%, 1 4%, 10 3%, 9 1%, 12 1%, 15 1%

FRNCOD: Z 39%, L 20%, à 11%, J 10%, v 8%, g 4%, x 4%, t 2%, O 1%, LZ 0%, ) 0%

ISCODE: I 97%, M 3%

SQFTCODE: 3 31%, 4 21%, 2 18%, 1 15%, 5 8%, 6 4%, 7 2%, 8 1%

LOC_NAME: PointAddress 53%, Subaddress 25%, StreetAddress 21%, Postal 1%, PostalExt 0%, StreetName 0%, StreetAddressExt 0%

STATUS: M 99%, T 1%

REC_TYPE: 0 99%, 1 1%, 2 0%

DISTRICT: 3 29%, 1 22%, 5 21%, 4 16%, 2 12%

LABEL: District 3 29%, District 1 22%, District 5 21%, District 4 16%, District 2 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.3K | 0 | 1356 7; 1355 7; 1354 7; 1353 7 |
| JOIN_COUNT | other | 1 | 0 | 1 1.4K |
| TARGET_FID | id | 1.3K | 0 | 1920 7; 1914 7; 1913 7; 1912 7 |
| LOCNUM | id | 1.4K | 0 | 997274758 7; 992954974 7; 992927251 7; 992920645 7 |
| CONAME | who | 1.1K | 0 | WALMART PHARMACY 43; RALPHS PHARMACY 43; VONS PHARMACY 32; ALBERTSONS SAV-ON PHARMAC 17 |
| STREET | who | 556 | 16 | VENTURA BLVD 46; WILSHIRE BLVD 35; SANTA MONICA BLVD 25; W OLYMPIC BLVD 18 |
| CITY | who | 122 | 0 | LOS ANGELES 289; GLENDALE 73; LONG BEACH 43; VAN NUYS 38 |
| STATE | other | 1 | 0 | CA 1.4K |
| STATE_NAME | who | 1 | 0 | California 1.4K |
| ZIP | other | 264 | 0 | 91205 23; 90006 20; 91770 19; 91356 19 |
| ZIP4 | other | 1.1K | 33 | 1413 8; 1167 7; 4264 7; 2255 7 |
| NAICS | who | 1 | 0 | 44611009 1.4K |
| SIC | who | 1 | 0 | 591205 1.4K |
| SALESVOL | category | 39 | 0 | 1318 649; 1647 127; 989 123; 659 74 |
| HDBRCH | category | 4 | 1.2K | 2 197; 1 3; 3 3 |
| ULTNUM | category | 26 | 0 | 000000000 1.2K; 579284589 52; 005889993 50; 007521503 39 |
| PUBPRV | category | 2 | 1.2K | 2 122 |
| EMPNUM | category | 34 | 0 | 4 653; 5 129; 3 125; 7 78 |
| FRNCOD | category | 14 | 945 | Z 159; L 82; à 43; J 42 |
| ISCODE | category | 3 | 1.1K | I 266; M 9 |
| SQFTCODE | category | 9 | 7 | 3 419; 4 280; 2 248; 1 206 |
| LOC_NAME | category | 7 | 0 | PointAddress 712; Subaddress 338; StreetAddress 280; Postal 18 |
| STATUS | category | 2 | 0 | M 1.3K; T 7 |
| SCORE | amount | 20 | 0 | 100.0 1.3K; 99.890625 24; 98.0 5; 98.328125 2 |
| SOURCE | who | 1 | 0 | INFOGROUP 1.4K |
| REC_TYPE | category | 3 | 0 | 0 1.3K; 1 16; 2 3 |
| DISTRICT | category | 5 | 0 | 3 393; 1 295; 5 287; 4 212 |
| LABEL | category | 5 | 0 | District 3 393; District 1 295; District 5 287; District 4 212 |
| GEOMETRY | other | 1.3K | 0 | {"type": "Point", "coordi 8; {"type": "Point", "coordi 8; {"type": "Point", "coordi 7; {"type": "Point", "coordi 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:30:56.47892 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | f2cfdd9e-b1f2-4449-aca5-9 1.4K |
| SRC_SHA256 | who | 1 | 0 | 4e0d1ecb4361895fcfe58e49e 1.4K |
