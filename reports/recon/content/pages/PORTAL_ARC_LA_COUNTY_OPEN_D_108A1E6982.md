# PORTAL_ARC_LA_COUNTY_OPEN_D_108A1E6982

rows 365  columns 28  scan 3.9s

roles: amount 1, audit 2, category 12, date 1, other 9, who 4

## when

INGESTED_AT
  2026       365  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 365 | 96.83 | 100 | 100 | 100 | 36.5K |

## who

STATE_NAME by rows
       365  California

STATE_NAME by dollars
       36.5K      365 rows  California

SOURCE by rows
       365  INFOGROUP

SOURCE by dollars
       36.5K      365 rows  INFOGROUP

CITY by rows
        77  LOS ANGELES
        13  LONG BEACH
         9  LANCASTER
         7  TORRANCE
         7  WHITTIER
         7  DOWNEY
         7  NORTH HOLLYWOOD
         6  PALMDALE
         6  GARDENA
         6  NORTHRIDGE
         6  LAKEWOOD
         5  WEST COVINA
         5  GLENDALE
         5  SANTA CLARITA
         5  COMPTON
         5  PASADENA
         5  POMONA
         5  VAN NUYS
         4  CARSON
         4  WEST HOLLYWOOD

CITY by dollars
        7.7K       77 rows  LOS ANGELES
        1.3K       13 rows  LONG BEACH
         900        9 rows  LANCASTER
         700        7 rows  WHITTIER
         700        7 rows  DOWNEY
         700        7 rows  NORTH HOLLYWOOD
         700        7 rows  TORRANCE
         600        6 rows  GARDENA
         600        6 rows  PALMDALE
         600        6 rows  LAKEWOOD
      599.78        6 rows  NORTHRIDGE
         500        5 rows  COMPTON
         500        5 rows  VAN NUYS
         500        5 rows  POMONA
         500        5 rows  GLENDALE
         500        5 rows  WEST COVINA
         500        5 rows  PASADENA
      499.20        5 rows  SANTA CLARITA
         400        4 rows  INGLEWOOD
         400        4 rows  PICO RIVERA

SRC_SHA256 by rows
       365  fc223708189319034a5c0a3e265fbdf400d6ab9ce102d8767359bd7f3167f2c5

SRC_SHA256 by dollars
       36.5K      365 rows  fc223708189319034a5c0a3e265fbdf400d6ab9ce102d8767359bd7f3167

## who x when

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:36.5K

SOURCE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  INFOGROUP                                 2026:36.5K

## what

CONAME: MC DONALD'S 97%, SWANNEY & MCDONALD 0%, J S MCDONALD TRUCKING 0%, MCDONALD JOHN PAINTING CORP 0%, KIMBERLY MCDONALD FINE JEWELRY 0%, LEAK DETECTION MCDONALD'S 0%, MCDONALD WRIGHT 0%, JERE E MCDONALD A/C 0%, MCDONALD GROUP 0%, MCDONALD SELZNICK ASSOC INC 0%, WILLIAM F MCDONALD CO 0%, CAMP RONALD MCDONALD FOR GOOD 0%

NAICS: 72251301 95%, 99999004 1%, 54141003 1%, 72121403 1%, 81331104 1%, 54111002 1%, 48841006 0%, 48423013 0%, 23832003 0%, 23822045 0%, 54161401 0%, 54187005 0%

SIC: 581208 95%, 999977 1%, 738902 1%, 703203 1%, 839919 1%, 811103 1%, 754901 0%, 421304 0%, 172101 0%, 171133 0%, 874201 0%, 731908 0%

HDBRCH: 2 100%

ULTNUM: 001682400 89%, 000000000 11%, 963542345 0%

PUBPRV: 2 100%

FRNCOD: K 100%, C 0%

ISCODE: e 100%

SQFTCODE: 3 84%, 1 8%, 2 3%, 5 3%, 4 2%, 6 1%

LOC_NAME: PointAddress 84%, StreetAddress 11%, Subaddress 4%, Postal 1%, StreetInt 1%

STATUS: M 99%, T 1%

REC_TYPE: 0 99%, 1 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 364 | 0 | 365 2; 364 2; 363 2; 362 2 |
| LOCNUM | other | 357 | 0 | 998976575 2; 998865885 2; 995871423 2; 992890053 2 |
| CONAME | category | 29 | 0 | MC DONALD'S 337; SWANNEY & MCDONALD 1; J S MCDONALD TRUCKING 1; MCDONALD JOHN PAINTING CO 1 |
| STREET | other | 229 | 3 | SEPULVEDA BLVD 6; FOOTHILL BLVD 6; CRENSHAW BLVD 6; LAKEWOOD BLVD 5 |
| CITY | who | 115 | 0 | LOS ANGELES 77; LONG BEACH 13; LANCASTER 9; DOWNEY 7 |
| STATE | other | 1 | 0 | CA 365 |
| STATE_NAME | who | 1 | 0 | California 365 |
| ZIP | other | 212 | 0 | 90029 5; 90016 5; 90712 4; 91706 4 |
| ZIP4 | other | 333 | 9 | 1413 4; 2757 3; 6101 3; 5239 3 |
| NAICS | category | 22 | 0 | 72251301 337; 99999004 4; 54141003 2; 72121403 2 |
| SIC | category | 22 | 0 | 581208 337; 999977 4; 738902 2; 703203 2 |
| SALESVOL | other | 72 | 0 | 2663 71; 2959 35; 2367 22; 3255 17 |
| HDBRCH | category | 2 | 39 | 2 326 |
| ULTNUM | category | 3 | 0 | 001682400 325; 000000000 39; 963542345 1 |
| PUBPRV | category | 2 | 40 | 2 325 |
| EMPNUM | other | 65 | 0 | 45 71; 50 35; 40 23; 55 17 |
| FRNCOD | category | 3 | 27 | K 337; C 1 |
| ISCODE | category | 2 | 28 | e 337 |
| SQFTCODE | category | 6 | 0 | 3 306; 1 29; 2 10; 5 10 |
| LOC_NAME | category | 5 | 0 | PointAddress 306; StreetAddress 40; Subaddress 14; Postal 3 |
| STATUS | category | 2 | 0 | M 362; T 3 |
| SCORE | amount | 9 | 0 | 100.0 343; 99.890625 14; 98.59375 2; 99.484375 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 365 |
| REC_TYPE | category | 2 | 0 | 0 362; 1 3 |
| GEOMETRY | other | 364 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:23:02.12099 365 |
| SOURCE_RUN_ID | audit | 1 | 0 | f1b017b1-6afd-48ea-82bd-a 365 |
| SRC_SHA256 | who | 1 | 0 | fc223708189319034a5c0a3e2 365 |
