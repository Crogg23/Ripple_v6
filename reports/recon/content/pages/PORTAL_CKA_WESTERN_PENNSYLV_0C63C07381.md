# PORTAL_CKA_WESTERN_PENNSYLV_0C63C07381

rows 574  columns 12  scan 4.0s

roles: amount 3, audit 2, category 3, date 1, other 2, who 2

## when

INGESTED_AT
  2026       574  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 574 | 1.4K | 76.0K | 3.61M | 24.50M | 217.76M |
| SHAPE_LENGTH | 574 | 156.05 | 1.5K | 20.5K | 81.7K | 1.79M |
| SQFT | 574 | 8.5K | 473.7K | 22.52M | 152.66M | 1.36B |

## who

COMBINED_DISTRICT by rows
        76  U5.H1.A2
        72  U4.H1.A2
        51  U5.H1.A1
        44  U3.H2.A3
        41  U3.H1.A3
        34  U4.H1.A3
        23  U3.H1.A2
        23  U4.H3.A4
        22  U3.H3.A4
        19  U4.H2.A3
        13  U4.H1.A1
        10  U5.H1.A3
         9  U2.H2.A3
         9  U1.H4.A5
         8  U6.H1.A1
         8  U4.H2.A4
         8  U3.H3.A5
         7  U2.H4.A3
         7  U3.H3.A3
         7  U2.H3.A3

COMBINED_DISTRICT by dollars
      69.77M       51 rows  U5.H1.A1
      42.33M       76 rows  U5.H1.A2
      23.05M       72 rows  U4.H1.A2
      15.30M        9 rows  U1.H4.A5
       7.81M        6 rows  U2.H4.A5
       7.36M       34 rows  U4.H1.A3
       7.25M       23 rows  U4.H3.A4
       5.60M       44 rows  U3.H2.A3
       5.49M       19 rows  U4.H2.A3
       5.26M        7 rows  U2.H3.A3
       4.30M        8 rows  U6.H1.A1
       3.70M       22 rows  U3.H3.A4
       2.89M        7 rows  U2.H4.A3
       1.63M       41 rows  U3.H1.A3
       1.62M        2 rows  U3.H5.A5
       1.45M        8 rows  U4.H2.A4
       1.08M        9 rows  U2.H2.A3
       1.06M        4 rows  U2.H5.A5
       1.05M       13 rows  U4.H1.A1
       1.04M        4 rows  U3.H2.A4

SRC_SHA256 by rows
       574  8bd8376d026ff7bdfc53265af7c7801d897436bd6ea7aee8f7f8c53945406a9a

SRC_SHA256 by dollars
     217.76M      574 rows  8bd8376d026ff7bdfc53265af7c7801d897436bd6ea7aee8f7f8c5394540

## who x when

COMBINED_DISTRICT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  U1.H4.A5                                  2026:15.30M
  U2.H2.A3                                  2026:1.08M
  U2.H3.A3                                  2026:5.26M
  U2.H4.A3                                  2026:2.89M
  U2.H4.A5                                  2026:7.81M
  U2.H5.A5                                  2026:1.06M
  U3.H1.A2                                  2026:701.5K
  U3.H1.A3                                  2026:1.63M
  U3.H2.A3                                  2026:5.60M
  U3.H2.A4                                  2026:1.04M
  U3.H3.A3                                  2026:1.01M
  U3.H3.A4                                  2026:3.70M
  U3.H3.A5                                  2026:639.3K
  U3.H5.A5                                  2026:1.62M
  U4.H1.A1                                  2026:1.05M
  U4.H1.A2                                  2026:23.05M
  U4.H1.A3                                  2026:7.36M
  U4.H2.A3                                  2026:5.49M
  U4.H2.A4                                  2026:1.45M
  U4.H3.A4                                  2026:7.25M
  U5.H1.A1                                  2026:69.77M
  U5.H1.A2                                  2026:42.33M
  U5.H1.A3                                  2026:866.4K
  U6.H1.A1                                  2026:4.30M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  8bd8376d026ff7bdfc53265af7c7801d897436bd  2026:217.76M

## what

AREA_DISTRICT: A-3 33%, A-2 33%, A-1 13%, A-4 12%, A-5 9%

HEIGHT_DISTRICT: H-1 59%, H-2 17%, H-3 16%, H-4 6%, H-5 1%

ZONING_DISTRICT: A Residence 34%, Commercial 29%, B Residence 24%, Light Industrial 9%, Heavy Industrial 2%, C Residence 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA_DISTRICT | category | 5 | 0 | A-3 191; A-2 187; A-1 75; A-4 70 |
| COMBINED_DISTRICT | who | 53 | 0 | U5.H1.A2 76; U4.H1.A2 72; U5.H1.A1 51; U3.H2.A3 44 |
| HEIGHT_DISTRICT | category | 5 | 0 | H-1 338; H-2 100; H-3 92; H-4 37 |
| OBJECTID | other | 562 | 0 | 583 3; 582 3; 581 3; 580 3 |
| SHAPE_AREA | amount | 576 | 0 | 21556.354957171134 3; 6662.811876371912 3; 17278.334464328156 3; 2680.849468318925 3 |
| SHAPE_LENGTH | amount | 566 | 0 | 589.7558505289023 3; 425.972431402545 3; 635.8205736526224 3; 207.1287277695243 3 |
| SQFT | amount | 566 | 0 | 134485.7875440677 3; 41529.72623413056 3; 107695.6442843674 3; 16708.536379883164 3 |
| ZONING_DISTRICT | category | 6 | 0 | A Residence 195; Commercial 166; B Residence 140; Light Industrial 50 |
| GEOMETRY | other | 568 | 0 | POLYGON ((585997.62707146 3; POLYGON ((585562.02867502 3; POLYGON ((585645.12211190 3; POLYGON ((585632.15153152 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:43:10.17677 574 |
| SOURCE_RUN_ID | audit | 1 | 0 | bf4af7ea-43a1-4946-a3b3-5 574 |
| SRC_SHA256 | who | 1 | 0 | 8bd8376d026ff7bdfc53265af 574 |
