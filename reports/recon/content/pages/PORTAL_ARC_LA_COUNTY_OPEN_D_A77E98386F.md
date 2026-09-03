# PORTAL_ARC_LA_COUNTY_OPEN_D_A77E98386F

rows 2.0K  columns 28  scan 4.0s

roles: amount 1, audit 2, category 10, date 1, empty 1, id 3, other 6, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 2.0K | 85 | 100 | 100 | 100 | 199.9K |

## who

CONAME by rows
         6  WASHINGTON ELEMENTARY SCHOOL
         5  TRAINING & RESEARCH FOUNDATION
         5  ROOSEVELT ELEMENTARY SCHOOL
         5  PLAZA DE LA RAZA
         4  MCKINLEY ELEMENTARY SCHOOL
         4  RAMONA ELEMENTARY SCHOOL
         4  JEFFERSON ELEMENTARY SCHOOL
         3  LOS ANGELES LEADERSHIP ACADEMY
         3  THOMAS JEFFERSON ELEMENTARY
         3  HACIENDA-LA PUENTE UNIFIED SCH
         3  WILLOW ELEMENTARY SCHOOL
         3  LAUREL ELEMENTARY SCHOOL
         3  FREMONT ELEMENTARY SCHOOL
         3  FOUNDATION FOR EARLY CHILDHOOD
         3  EMERSON ELEMENTARY SCHOOL
         3  WEBSTER ELEMENTARY SCHOOL
         3  RIO VISTA ELEMENTARY SCHOOL
         3  EDISON ELEMENTARY SCHOOL
         3  TUTOR TIME CHILD CARE/LEARNING
         3  LONGFELLOW ELEMENTARY SCHOOL

CONAME by dollars
         600        6 rows  WASHINGTON ELEMENTARY SCHOOL
         500        5 rows  PLAZA DE LA RAZA
         500        5 rows  ROOSEVELT ELEMENTARY SCHOOL
         500        5 rows  TRAINING & RESEARCH FOUNDATION
         400        4 rows  JEFFERSON ELEMENTARY SCHOOL
         400        4 rows  MCKINLEY ELEMENTARY SCHOOL
         400        4 rows  RAMONA ELEMENTARY SCHOOL
         300        3 rows  WEBSTER ELEMENTARY SCHOOL
         300        3 rows  THOMAS JEFFERSON ELEMENTARY
         300        3 rows  EDISON ELEMENTARY SCHOOL
         300        3 rows  FREMONT ELEMENTARY SCHOOL
         300        3 rows  LONGFELLOW ELEMENTARY SCHOOL
         300        3 rows  HACIENDA-LA PUENTE UNIFIED SCH
         300        3 rows  LAUREL ELEMENTARY SCHOOL
         300        3 rows  LOS ANGELES LEADERSHIP ACADEMY
         300        3 rows  EMERSON ELEMENTARY SCHOOL
         300        3 rows  FOUNDATION FOR EARLY CHILDHOOD
         300        3 rows  RIO VISTA ELEMENTARY SCHOOL
         300        3 rows  TUTOR TIME CHILD CARE/LEARNING
         300        3 rows  WILLOW ELEMENTARY SCHOOL

STATE_NAME by rows
      2.0K  California

STATE_NAME by dollars
      199.9K     2.0K rows  California

SOURCE by rows
      2.0K  INFOGROUP

SOURCE by dollars
      199.9K     2.0K rows  INFOGROUP

CITY by rows
       479  LOS ANGELES
        82  LONG BEACH
        42  TORRANCE
        39  VAN NUYS
        37  WHITTIER
        33  PASADENA
        32  GLENDALE
        29  NORTH HOLLYWOOD
        28  COMPTON
        27  SANTA MONICA
        26  DOWNEY
        26  LANCASTER
        23  LA PUENTE
        22  SAN PEDRO
        22  HAWTHORNE
        21  EL MONTE
        21  BURBANK
        21  GRANADA HILLS
        20  ALHAMBRA
        19  PALMDALE

CITY by dollars
       47.9K      479 rows  LOS ANGELES
        8.2K       82 rows  LONG BEACH
        4.2K       42 rows  TORRANCE
        3.9K       39 rows  VAN NUYS
        3.7K       37 rows  WHITTIER
        3.3K       33 rows  PASADENA
        3.2K       32 rows  GLENDALE
        2.9K       29 rows  NORTH HOLLYWOOD
        2.8K       28 rows  COMPTON
        2.7K       27 rows  SANTA MONICA
        2.6K       26 rows  DOWNEY
        2.6K       26 rows  LANCASTER
        2.3K       23 rows  LA PUENTE
        2.2K       22 rows  SAN PEDRO
        2.2K       22 rows  HAWTHORNE
        2.1K       21 rows  BURBANK
        2.1K       21 rows  EL MONTE
        2.1K       21 rows  GRANADA HILLS
        2.0K       20 rows  ALHAMBRA
        1.9K       19 rows  SOUTH GATE

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  EDISON ELEMENTARY SCHOOL                  2026:300
  EMERSON ELEMENTARY SCHOOL                 2026:300
  FOUNDATION FOR EARLY CHILDHOOD            2026:300
  FREMONT ELEMENTARY SCHOOL                 2026:300
  HACIENDA-LA PUENTE UNIFIED SCH            2026:300
  JEFFERSON ELEMENTARY SCHOOL               2026:400
  LAUREL ELEMENTARY SCHOOL                  2026:300
  LONGFELLOW ELEMENTARY SCHOOL              2026:300
  LOS ANGELES LEADERSHIP ACADEMY            2026:300
  MCKINLEY ELEMENTARY SCHOOL                2026:400
  PLAZA DE LA RAZA                          2026:500
  RAMONA ELEMENTARY SCHOOL                  2026:400
  RIO VISTA ELEMENTARY SCHOOL               2026:300
  ROOSEVELT ELEMENTARY SCHOOL               2026:500
  THOMAS JEFFERSON ELEMENTARY               2026:300
  TRAINING & RESEARCH FOUNDATION            2026:500
  TUTOR TIME CHILD CARE/LEARNING            2026:300
  WASHINGTON ELEMENTARY SCHOOL              2026:600
  WEBSTER ELEMENTARY SCHOOL                 2026:300
  WILLOW ELEMENTARY SCHOOL                  2026:300

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:199.9K

## what

NAICS: 61111007 79%, 62441006 21%, 61111004 0%

SIC: 821103 79%, 835102 21%, 821101 0%

SALESVOL: 0 84%, 190 6%, 254 1%, 148 1%, 127 1%, 85 1%, 106 1%, 169 1%, 212 1%, 317 1%, 64 1%, 423 1%

HDBRCH: 2 100%

ULTNUM: 000000000 99%, 898922828 0%, 458014073 0%, 479607046 0%, 634660898 0%, 597899889 0%, 466104361 0%

ISCODE: C 43%, D 29%, B 18%, A 10%

SQFTCODE: 8 31%, 7 31%, 1 11%, 3 7%, 2 7%, 6 6%, 4 5%, 5 3%

LOC_NAME: PointAddress 74%, StreetAddress 24%, Subaddress 2%, StreetName 0%, Postal 0%, StreetAddressExt 0%

STATUS: M 99%, T 1%

REC_TYPE: 0 100%, 1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| LOCNUM | id | 2.0K | 0 | 450062922 10; 450062906 10; 450062872 10; 450062666 10 |
| CONAME | who | 1.9K | 0 | HACIENDA-LA PUENTE UNIFIE 12; NORWALK LA MIRADA UNIFIED 11; WILLIAM S HART UNION HIGH 11; PACE HEADSTART 11 |
| STREET | other | 1.4K | 1 | BURBANK BLVD 13; S FIGUEROA ST 13; S WESTERN AVE 12; S NORMANDIE AVE 11 |
| CITY | who | 136 | 0 | LOS ANGELES 479; LONG BEACH 82; TORRANCE 42; VAN NUYS 39 |
| STATE | other | 1 | 0 | CA 2.0K |
| STATE_NAME | who | 1 | 0 | California 2.0K |
| ZIP | other | 271 | 0 | 91744 25; 90011 22; 90250 22; 91344 21 |
| ZIP4 | other | 1.4K | 28 | 3199 13; 4317 11; 3616 11; 3499 11 |
| NAICS | category | 3 | 0 | 61111007 1.6K; 62441006 414; 61111004 8 |
| SIC | category | 3 | 0 | 821103 1.6K; 835102 414; 821101 8 |
| SALESVOL | category | 42 | 0 | 0 1.6K; 190 108; 254 26; 148 24 |
| HDBRCH | category | 2 | 2.0K | 2 17 |
| ULTNUM | category | 7 | 0 | 000000000 2.0K; 898922828 4; 458014073 3; 479607046 3 |
| PUBPRV | empty | 1 | 2.0K |  |
| EMPNUM | other | 148 | 0 | 9 208; 60 112; 50 85; 100 82 |
| FRNCOD | other | 101 | 506 | EKN 669; NS 115; JN 102; E 56 |
| ISCODE | category | 5 | 1.1K | C 376; D 255; B 161; A 88 |
| SQFTCODE | category | 8 | 0 | 8 617; 7 614; 1 211; 3 135 |
| LOC_NAME | category | 6 | 0 | PointAddress 1.5K; StreetAddress 482; Subaddress 32; StreetName 5 |
| STATUS | category | 2 | 0 | M 2.0K; T 16 |
| SCORE | amount | 19 | 0 | 100.0 1.9K; 99.890625 46; 98.59375 3; 85.0 3 |
| SOURCE | who | 1 | 0 | INFOGROUP 2.0K |
| REC_TYPE | category | 2 | 0 | 0 2.0K; 1 1 |
| GEOMETRY | id | 2.0K | 0 | {"type": "Point", "coordi 11; {"type": "Point", "coordi 11; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:33:23.02044 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c9ec7e11-507d-4939-98f3-e 2.0K |
| SRC_SHA256 | who | 1 | 0 | 701c7a6ad45e51d4b9e9f11ff 2.0K |
