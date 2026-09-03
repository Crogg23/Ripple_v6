# PORTAL_ARC_MARICOPA_COUNTY_91150B6A88

rows 195  columns 7  scan 3.2s

roles: audit 2, date 1, other 2, who 3

## when

INGESTED_AT
  2026       195  ##############################

## who

LABEL by rows
        40  Global Water - Palo Verde Utilities Co
        12  EPCOR Water Arizona, Inc. (Luke 303)
        11  Johnson Utilities, LLC
         7  EPCOR Water Arizona, Inc.
         7  Livco Sewer Company
         7  Far West Water & Sewer, Inc.
         7  EPCOR Water Arizona, Inc. (Agua Fria)
         6  Perkins Mountain Utility Company
         6  Litchfield Park Service Company
         5  EPCOR Water Arizona, Inc. (Sun City)
         5  Hassayampa Utility Company, Inc.
         5  Black Mountain Sewer Corporation
         4  Pima Utility Company
         4  Pine Meadows Utilities, LLC
         3  Sacramento Utilities, LLC
         3  The Links at Coyote Wash Utilities, LLC
         3  Sunrise Utilities, LLC
         3  Bensch Ranch Utilities, LLC
         3  Willow Springs Utilities, LLC
         3  Rio Verde Utilities, Inc.

ACC_DOCKET by rows
        40  SW3575
        37  WS1303
        11  WS2987
         7  SW2563
         7  WS3478
         5  SW2361
         5  SW2042
         4  WS2199
         4  SW1428
         4  SW3962
         3  WS4247
         3  S20576
         3  SW4026
         3  SW4210
         3  WS2156
         3  WS2043
         2  SW2519
         2  WS1678
         2  20878
         2  W-1427

SRC_SHA256 by rows
       195  cd7ad1b5543a6598f8cf5608febb1074bd6874ec499ff4d9d9a37ad2688bbf2a

## who x when

LABEL by INGESTED_AT  LOAD STAMP, not an event date
  Bensch Ranch Utilities, LLC               2026:3
  Black Mountain Sewer Corporation          2026:5
  EPCOR Water Arizona, Inc.                 2026:7
  EPCOR Water Arizona, Inc. (Agua Fria)     2026:7
  EPCOR Water Arizona, Inc. (Luke 303)      2026:12
  EPCOR Water Arizona, Inc. (Sun City)      2026:5
  Far West Water & Sewer, Inc.              2026:7
  Global Water - Palo Verde Utilities Co    2026:40
  Hassayampa Utility Company, Inc.          2026:5
  Johnson Utilities, LLC                    2026:11
  Litchfield Park Service Company           2026:6
  Livco Sewer Company                       2026:7
  Perkins Mountain Utility Company          2026:6
  Pima Utility Company                      2026:4
  Pine Meadows Utilities, LLC               2026:4
  Rio Verde Utilities, Inc.                 2026:3
  Sacramento Utilities, LLC                 2026:3
  Sunrise Utilities, LLC                    2026:3
  The Links at Coyote Wash Utilities, LLC   2026:3
  Willow Springs Utilities, LLC             2026:3

ACC_DOCKET by INGESTED_AT  LOAD STAMP, not an event date
  20878                                     2026:2
  S20576                                    2026:3
  SW1428                                    2026:4
  SW2042                                    2026:5
  SW2361                                    2026:5
  SW2519                                    2026:2
  SW2563                                    2026:7
  SW3575                                    2026:40
  SW3962                                    2026:4
  SW4026                                    2026:3
  SW4210                                    2026:3
  W-1427                                    2026:2
  WS1303                                    2026:37
  WS1678                                    2026:2
  WS2043                                    2026:3
  WS2156                                    2026:3
  WS2199                                    2026:4
  WS2987                                    2026:11
  WS3478                                    2026:7
  WS4247                                    2026:3

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 192 | 0 | 369 1; 368 1; 367 1; 366 1 |
| LABEL | who | 61 | 0 | Global Water - Palo Verde 40; EPCOR Water Arizona, Inc. 12; Johnson Utilities, LLC 11; EPCOR Water Arizona, Inc. 7 |
| ACC_DOCKET | who | 52 | 11 | SW3575 40; WS1303 37; WS2987 11; WS3478 7 |
| GEOMETRY | other | 197 | 0 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:50:05.06741 195 |
| SOURCE_RUN_ID | audit | 1 | 0 | ea3c7731-e83d-4b00-aed9-d 195 |
| SRC_SHA256 | who | 1 | 0 | cd7ad1b5543a6598f8cf5608f 195 |
