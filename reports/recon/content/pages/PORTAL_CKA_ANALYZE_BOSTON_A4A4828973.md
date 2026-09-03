# PORTAL_CKA_ANALYZE_BOSTON_A4A4828973

rows 10.0K  columns 37  scan 5.0s

roles: amount 10, audit 2, category 13, date 2, empty 3, id 2, other 2, who 4

## when

INSP_DATE
  2007      5.7K  ##############################
  2008      1.3K  #######
  2009      1.4K  #######
  2010      1.5K  ########

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| APRON_SL | 10.0K | 0 | 7.60 | 19.45 | 35.80 | 76.9K |
| LANDING_SL | 10.0K | 0 | 1.60 | 11.85 | 33 | 25.9K |
| RCI | 10.0K | 0 | 40 | 90 | 90 | 480.3K |
| NPR | 10.0K | 0 | 6.12 | 11.36 | 17.89 | 65.9K |
| REVEAL | 10.0K | 0 | 0 | 7 | 12 | 14.7K |
| SWK_WIDTH | 10.0K | 0 | 0 | 15 | 55 | 21.1K |

## who

HIGHWAY by rows
       190  WASHINGTON ST
       151  DORCHESTER AV DO
       115  HYDE PARK AV
       113  HARRISON AV
       113  RIVER ST HP
        83  COMMONWEALTH AV WB
        81  BEACON ST BP
        81  TREMONT ST RX BP
        73  OLD COLONY AV SB
        72  COMMONWEALTH AV EB
        72  BOYLSTON ST BP
        72  D ST
        65  TALBOT AV
        63  MASSACHUSETTS AV
        63  CONGRESS ST
        58  ALBANY ST
        57  CENTRE ST WR JP RX
        57  SUMMER ST SB
        55  A ST SB
        54  DARTMOUTH ST

HIGHWAY by dollars
        1.3K      190 rows  WASHINGTON ST
        1.1K      151 rows  DORCHESTER AV DO
      893.20      115 rows  HYDE PARK AV
      837.70      113 rows  HARRISON AV
      807.30      113 rows  RIVER ST HP
      685.30       81 rows  TREMONT ST RX BP
      657.90       73 rows  OLD COLONY AV SB
      649.60       83 rows  COMMONWEALTH AV WB
      594.20       72 rows  COMMONWEALTH AV EB
      593.60       81 rows  BEACON ST BP
         538       55 rows  A ST SB
         535       72 rows  BOYLSTON ST BP
      489.60       63 rows  MASSACHUSETTS AV
      486.90       72 rows  D ST
      468.10       52 rows  CLARENDON ST
      463.50       58 rows  ALBANY ST
      425.40       63 rows  CONGRESS ST
      414.20       65 rows  TALBOT AV
      413.50       57 rows  SUMMER ST SB
      400.90       46 rows  COLUMBIA RD DO SB

PARENT by rows
       190  WASHI1
       151  DORCH1
       115  HYDE 1
       113  HARRI5
       113  RIVER1
        83  COMMO1
        81  TREMO1
        81  BEACO1
        73  OLD C3
        72  BOYLS6
        72  D ST 1
        72  COMMO5
        65  TALBO1
        63  MASSA3
        63  CONGR1
        58  ALBAN3
        57  CENTR6
        57  SUMME10
        55  A ST 1
        54  DARTM2

PARENT by dollars
        1.3K      190 rows  WASHI1
        1.1K      151 rows  DORCH1
      893.20      115 rows  HYDE 1
      837.70      113 rows  HARRI5
      807.30      113 rows  RIVER1
      685.30       81 rows  TREMO1
      657.90       73 rows  OLD C3
      649.60       83 rows  COMMO1
      594.20       72 rows  COMMO5
      593.60       81 rows  BEACO1
         538       55 rows  A ST 1
         535       72 rows  BOYLS6
      489.60       63 rows  MASSA3
      486.90       72 rows  D ST 1
      468.10       52 rows  CLARE5
      463.50       58 rows  ALBAN3
      425.40       63 rows  CONGR1
      414.20       65 rows  TALBO1
      413.50       57 rows  SUMME10
      400.90       46 rows  COLUM3

INSP_NOTES by rows
       137  TRANSITION
       135  CRACKING
        91  NARROW RAMP
        89  NO PLANS
        80  THRESHOLD TOO HIGH
        77  CRACK
        59  REPAINT STRIPING
        42  STRIPPING FADED
        37  RAMP IN STREET
        32  PONDING AT BASE OF RAMP
        21  TRAFFIC SIGNAL
        21  MANHOLE
        18  PATCH IN RAMP
        18  HEAVILY CRACKING
        17  SNOW
        16  NEWLY CONSTRUCTED
        16  CONSTRUCTION
        14  POOR TRANSITION
        13  NO LANDING
        12  OUTSIDE PAVE LIMITS

INSP_NOTES by dollars
        1.4K       91 rows  NARROW RAMP
        1.3K      135 rows  CRACKING
        1.2K      137 rows  TRANSITION
         738       89 rows  NO PLANS
      677.50       77 rows  CRACK
      513.40       80 rows  THRESHOLD TOO HIGH
      409.80       59 rows  REPAINT STRIPING
      335.90       42 rows  STRIPPING FADED
      321.10       37 rows  RAMP IN STREET
      290.80       32 rows  PONDING AT BASE OF RAMP
      180.40       21 rows  MANHOLE
      166.50       18 rows  HEAVILY CRACKING
      153.20       18 rows  PATCH IN RAMP
      140.30       14 rows  POOR TRANSITION
      129.90       21 rows  TRAFFIC SIGNAL
      125.50       13 rows  NO LANDING
      113.90       12 rows  OUTSIDE PAVE LIMITS
      102.50        9 rows  POOLING WATER AT APRON
          98       16 rows  NEWLY CONSTRUCTED
       92.60        9 rows  MAINT AGREEMENT

SRC_SHA256 by rows
     10.0K  bf328b9f58fba37efff2d276cc0415291ba77baef9f0230399d5446607ce5488

SRC_SHA256 by dollars
       76.9K    10.0K rows  bf328b9f58fba37efff2d276cc0415291ba77baef9f0230399d5446607ce

## who x when

HIGHWAY by INSP_DATE, dollars = APRON_SL
  A ST SB                                   2007:242.50 2009:295.50
  ALBANY ST                                 2007:391.50 2009:67.80 2010:4.20
  BEACON ST BP                              2007:420.60 2008:51.30 2009:61.90 2010:59.80
  BOYLSTON ST BP                            2007:480.90 2008:54.10
  CENTRE ST WR JP RX                        2008:80.10 2009:99
  CLARENDON ST                              2007:263 2009:205.10
  COLUMBIA RD DO SB                         2007:117.30 2008:86.10 2009:105.50 2010:92
  COMMONWEALTH AV EB                        2007:25.20 2008:51.40 2009:517.60
  COMMONWEALTH AV WB                        2007:17.40 2008:123.80 2009:508.40
  CONGRESS ST                               2007:215.80 2009:209.60
  D ST                                      2007:486.90
  DARTMOUTH ST                              2007:400.60
  DORCHESTER AV DO                          2007:433.90 2008:220.70 2009:181.50 2010:261.70
  HARRISON AV                               2007:455.40 2008:27.40 2009:354.90
  HYDE PARK AV                              2007:101.80 2009:105.10 2010:686.30
  MASSACHUSETTS AV                          2007:302.50 2008:187.10
  OLD COLONY AV SB                          2007:657.90
  RIVER ST HP                               2007:248.70 2008:39.30 2009:62.40 2010:456.90
  SUMMER ST SB                              2007:413.50
  TALBOT AV                                 2008:355.10
  TREMONT ST RX BP                          2007:661.10 2009:24.20
  WASHINGTON ST                             2007:968.20 2008:85.50 2009:175.30

PARENT by INSP_DATE, dollars = APRON_SL
  A ST 1                                    2007:242.50 2009:295.50
  ALBAN3                                    2007:391.50 2009:67.80 2010:4.20
  BEACO1                                    2007:420.60 2008:51.30 2009:61.90 2010:59.80
  BOYLS6                                    2007:480.90 2008:54.10
  CENTR6                                    2008:80.10 2009:99
  CLARE5                                    2007:263 2009:205.10
  COLUM3                                    2007:117.30 2008:86.10 2009:105.50 2010:92
  COMMO1                                    2007:17.40 2008:123.80 2009:508.40
  COMMO5                                    2007:25.20 2008:51.40 2009:517.60
  CONGR1                                    2007:215.80 2009:209.60
  D ST 1                                    2007:486.90
  DARTM2                                    2007:400.60
  DORCH1                                    2007:433.90 2008:220.70 2009:181.50 2010:261.70
  HARRI5                                    2007:455.40 2008:27.40 2009:354.90
  HYDE 1                                    2007:101.80 2009:105.10 2010:686.30
  MASSA3                                    2007:302.50 2008:187.10
  OLD C3                                    2007:657.90
  RIVER1                                    2007:248.70 2008:39.30 2009:62.40 2010:456.90
  SUMME10                                   2007:413.50
  TALBO1                                    2008:355.10
  TREMO1                                    2007:661.10 2009:24.20
  WASHI1                                    2007:968.20 2008:85.50 2009:175.30

## what

COND: F - FAIR MINOR MAINTENANCE 66%, E - EXCELLENT LIKE NEW 21%, P - POOR MAJOR MAINTENANCE 13%, U - UNKNOWN 1%

INSP: BWT 42%, MJM 17%, PJF 12%, PHILLIP 12%, BV 6%, MO 5%, TR 4%, KHW 3%

ACCESS: 1 66%, 2 24%, 0 9%, 3 2%

C_CROSS: 2 56%, 0 39%, 1 5%

LIP: UNKNOWN 48%, NO 37%, YES 15%

PWD: 1-1C 24%, 3-05 19%, 3-03 17%, 2-08 14%, 1-1B 11%, 1-10A 4%, 1-10B 3%, 2-02 3%, 3-07 2%, 2-06 1%, 2-04 1%, 1-1A 0%

CITYCODE: PUBLIC WAY 93%, DCR 3%, PRIVATE WAY 2%, UNKNOWN 2%, STATE 0%, PARK 0%

REPAIR_ALT: RCCR 81%, RBRR 12%, RBCR 3%, UNKNOWN 2%, RSPR 1%

SWK_MATL: CC - CEMENT CONCRETE 76%, BR - BRICK 15%, CB - CEMENT CONCRETE W/ ACCENT 3%, BC - BITUMINOUS CONCRETE 3%, BL - BLOCK 1%, UN - UNKNOWN 1%, GB - GRANITE BLOCK 1%

MATL: CC - CEMENT CONCRETE 72%, BR - BRICK 14%, NO - NONE 9%, BC - BITUMINOUS CONCRETE 3%, BL - BLOCK 1%, CB - CEMENT CONCRETE W/ ACCENT 1%, GB - GRANITE BLOCK 0%

RAMP_CAT: MAINT 77%, RECON 23%

AAB_COMP: NO 77%, YES 23%

AAB_LIKE_C: NO 55%, YES 45%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RAMP_ID | id | 10.0K | 0 | 14864.000000000000000 50; 14623.000000000000000 50; 14622.000000000000000 50; 14786.000000000000000 50 |
| COND | category | 4 | 0 | F - FAIR MINOR MAINTENANC 6.6K; E - EXCELLENT LIKE NEW 2.1K; P - POOR MAJOR MAINTENANC 1.3K; U - UNKNOWN 64 |
| INSP | category | 9 | 23 | BWT 4.2K; MJM 1.7K; PJF 1.2K; PHILLIP 1.2K |
| ACCESS | category | 5 | 64 | 1 6.5K; 2 2.3K; 0 858; 3 231 |
| C_CROSS | category | 4 | 65 | 2 5.6K; 0 3.8K; 1 509 |
| APRON_SL | amount | 249 | 0 | 0.000000000000000 896; 8.100000000000000 121; 8.300000000000001 120; 6.300000000000000 115 |
| LANDING_SL | amount | 162 | 0 | 0.000000000000000 3.3K; 0.900000000000000 136; 2.100000000000000 129; 1.800000000000000 128 |
| LIP | category | 3 | 0 | UNKNOWN 4.8K; NO 3.7K; YES 1.5K |
| PWD | category | 12 | 0 | 1-1C 2.4K; 3-05 1.9K; 3-03 1.7K; 2-08 1.4K |
| CITYCODE | category | 6 | 0 | PUBLIC WAY 9.3K; DCR 281; PRIVATE WAY 249; UNKNOWN 171 |
| RCI | amount | 7 | 0 | 40.000000000000000 5.5K; 30.000000000000000 1.2K; 50.000000000000000 1.2K; 80.000000000000000 1.0K |
| REPAIR_ALT | category | 6 | 2.0K | RCCR 6.5K; RBRR 999; RBCR 234; UNKNOWN 171 |
| HIGHWAY | who | 1.3K | 0 | WASHINGTON ST 190; DORCHESTER AV DO 151; HYDE PARK AV 115; RIVER ST HP 115 |
| ADDRESS | other | 1.7K | 172 | 1 186; 2 178; 30 89; 29 79 |
| NPR | amount | 8.5K | 0 | 0.000000000000000 173; 5.000000000000000 52; 7.748000000000000 50; 5.183800000000000 50 |
| REVEAL | amount | 26 | 0 | 0.000000000000000 7.1K; 6.000000000000000 1.0K; 5.000000000000000 542; 4.000000000000000 512 |
| SWK_WIDTH | amount | 105 | 0 | 0.000000000000000 7.1K; 6.000000000000000 745; 5.000000000000000 345; 7.000000000000000 258 |
| CONST_DATE | other | 187 | 0 | 18991230 9.1K; 40724 92; 40406 25; 40350 23 |
| SWK_MATL | category | 7 | 0 | CC - CEMENT CONCRETE 7.6K; BR - BRICK 1.5K; CB - CEMENT CONCRETE W/ A 342; BC - BITUMINOUS CONCRETE 294 |
| MATL | category | 7 | 0 | CC - CEMENT CONCRETE 7.2K; BR - BRICK 1.4K; NO - NONE 898; BC - BITUMINOUS CONCRETE 270 |
| CONST_PROG | empty | 1 | 10.0K |  |
| RAMP_CAT | category | 3 | 8.3K | MAINT 1.3K; RECON 404 |
| INSP_NOTES | who | 353 | 8.5K | TRANSITION 137; CRACKING 135; NARROW RAMP 91; NO PLANS 89 |
| INSP_DATE | date | 136 | 64 | 10/22/2007 0:00:00 325; 9/21/2007 0:00:00 311; 10/4/2007 0:00:00 308; 10/10/2007 0:00:00 299 |
| CONST_NOTE | empty | 1 | 10.0K |  |
| EST_COST | amount | 5 | 0 | 8000.000000000000000 6.5K; 0.000000000000000 2.1K; 12500.000000000000000 999; 4500.000000000000000 234 |
| GIS_NOTES | empty | 1 | 10.0K |  |
| AAB_COMP | category | 3 | 35 | NO 7.6K; YES 2.3K |
| PARENT | who | 1.3K | 52 | WASHI1 190; DORCH1 151; HYDE 1 115; RIVER1 115 |
| POINT_X | amount | 9.8K | 0 | -71.088099077999971 50; -71.091526664999947 50; -71.091533405999940 50; -71.094642404999945 50 |
| POINT_Y | amount | 10.1K | 0 | 42.345163444000036 50; 42.349656398000036 50; 42.349763990000042 50; 42.347078949000036 50 |
| ID2 | amount | 10.0K | 0 | 14864.000000000000000 50; 14623.000000000000000 50; 14622.000000000000000 50; 14786.000000000000000 50 |
| AAB_LIKE_C | category | 3 | 2 | NO 5.5K; YES 4.5K |
| SHAPE_WKT | id | 9.9K | 0 | POINT (-71.08809907799997 50; POINT (-71.09152666499994 50; POINT (-71.09153340599994 50; POINT (-71.09464240499994 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:44:19.64042 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | bd0f098f-1765-4897-9288-a 10.0K |
| SRC_SHA256 | who | 1 | 0 | bf328b9f58fba37efff2d276c 10.0K |
