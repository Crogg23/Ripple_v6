# PORTAL_ARC_MARICOPA_COUNTY_55B91E4BD1

rows 821  columns 7  scan 2.8s

roles: audit 2, date 1, other 2, who 3

## when

INGESTED_AT
  2026       821  ##############################

## who

LABEL by rows
        51  Global Water - Santa Cruz Water Company
        45  Ehrenberg Improvement Association
        36  Water Utility of Greater Tonopah, Inc.
        33  Arizona Water Company (Pinal Valley)
        17  Johnson Utilities, LLC
        11  Payson Water Company, Inc.
        11  Bermuda Water Company, Inc.
        11  Clear Springs Utility Company
        11  Valencia Water Company, Inc.
        10  Truxton Canyon Water Company, Inc.
        10  Bella Vista Water Company
         9  Harrisburg Utility Company, Inc.
         9  EPCOR Water Arizona, Inc. (Agua Fria)
         9  Mt. Tipton Water Company, Inc.
         8  Sterling Water Company
         7  Camp Verde Water System
         7  Francisco Grande Utility Company
         7  Tonto Basin Water Company, Inc.
         7  Brooke Water, LLC
         7  Lagoon Estates Water Company, Inc.

ACC_DOCKET by rows
        68  W-1445
        51  W20446
        45  W-2273
        41  WS1303
        36  W-2450
        17  WS2987
        11  W-1689
        11  W-1812
        11  W-1212
        11  W-3514
        10  W-2168
        10  W-2465
         9  W-2169
         9  W-2105
         8  W-3499
         7  WS1775
         7  W-1825
         7  W-3515
         7  W-3039
         7  W-2524

SRC_SHA256 by rows
       821  ae3bb956d34a548e5b3b1f08c1121bf02f8470b5f6b02c7b58ab7511891a93e7

## who x when

LABEL by INGESTED_AT  LOAD STAMP, not an event date
  Arizona Water Company (Pinal Valley)      2026:33
  Bella Vista Water Company                 2026:10
  Bermuda Water Company, Inc.               2026:11
  Brooke Water, LLC                         2026:7
  Camp Verde Water System                   2026:7
  Clear Springs Utility Company             2026:11
  EPCOR Water Arizona, Inc. (Agua Fria)     2026:9
  Ehrenberg Improvement Association         2026:45
  Francisco Grande Utility Company          2026:7
  Global Water - Santa Cruz Water Company   2026:51
  Harrisburg Utility Company, Inc.          2026:9
  Johnson Utilities, LLC                    2026:17
  Lagoon Estates Water Company, Inc.        2026:7
  Mt. Tipton Water Company, Inc.            2026:9
  Payson Water Company, Inc.                2026:11
  Sterling Water Company                    2026:8
  Tonto Basin Water Company, Inc.           2026:7
  Truxton Canyon Water Company, Inc.        2026:10
  Valencia Water Company, Inc.              2026:11
  Water Utility of Greater Tonopah, Inc.    2026:36

ACC_DOCKET by INGESTED_AT  LOAD STAMP, not an event date
  W-1212                                    2026:11
  W-1445                                    2026:68
  W-1689                                    2026:11
  W-1812                                    2026:11
  W-1825                                    2026:7
  W-2105                                    2026:9
  W-2168                                    2026:10
  W-2169                                    2026:9
  W-2273                                    2026:45
  W-2450                                    2026:36
  W-2465                                    2026:10
  W-2524                                    2026:7
  W-3039                                    2026:7
  W-3499                                    2026:8
  W-3514                                    2026:11
  W-3515                                    2026:7
  W20446                                    2026:51
  WS1303                                    2026:41
  WS1775                                    2026:7
  WS2987                                    2026:17

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 819 | 0 | 1510 5; 1509 5; 1508 5; 1507 5 |
| LABEL | who | 310 | 2 | Global Water - Santa Cruz 51; Ehrenberg Improvement Ass 45; Water Utility of Greater  37; Arizona Water Company (Pi 34 |
| ACC_DOCKET | who | 285 | 9 | W-1445 68; W20446 51; W-2273 45; WS1303 41 |
| GEOMETRY | other | 836 | 0 | {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5; {"type": "Polygon", "coor 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:51:41.60371 821 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7f373609-e450-40d1-a37c-7 821 |
| SRC_SHA256 | who | 1 | 0 | ae3bb956d34a548e5b3b1f08c 821 |
