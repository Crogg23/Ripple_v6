# PORTAL_CKA_WESTERN_PENNSYLV_EED8A7BFA0

rows 130  columns 19  scan 4.4s

roles: amount 2, audit 2, category 6, date 1, other 6, who 3

## when

INGESTED_AT
  2026       130  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 126 | 1.32M | 1.35M | 1.37M | 1.38M | 169.77M |
| POINT_Y | 126 | 384.6K | 411.5K | 428.9K | 429.1K | 51.88M |

## who

FIELD_NAME by rows
         1  Arsenal Band Box
         1  Overbrook Field 2
         1  Cowley Field 2
         1  Volunteers 4
         1  Fowler 1
         1  Paulson
         1  Gladstone
         1  Dan Marino
         1  Banksville Park
         1  Michael Flynn
         1  Herschel Lower
         1  Vanucci Field 1
         1  Vanucci Field 2
         1  Scherer
         1  Wightman
         1  Sam Bryan 2
         1  Warrington
         1  Farm House
         1  Loretta Miller
         1  Dean

FIELD_NAME by dollars
       1.38M        1 rows  East Hills
       1.37M        1 rows  Chadwick
       1.37M        1 rows  Braddock 1
       1.37M        1 rows  Braddock 2
       1.37M        1 rows  Willie Stargell 2
       1.37M        1 rows  Paulson
       1.37M        1 rows  Willie Stargell 1
       1.37M        1 rows  Fern Hollow
       1.37M        1 rows  McBride Park
       1.37M        1 rows  Farm House
       1.37M        1 rows  Larimer
       1.37M        1 rows  Stan Lederman
       1.37M        1 rows  Mellon Park Main
       1.37M        1 rows  Mellon Park Middle
       1.37M        1 rows  Mellon Park Little
       1.37M        1 rows  East Liberty Park
       1.36M        1 rows  Joe Natoli 1
       1.36M        1 rows  Panorama
       1.36M        1 rows  Joe Natoli 2
       1.36M        1 rows  Joe Natoli 3

DPW_NAME by rows
         9   Name
         1  Kennard  #1
         1  Michael Flynn
         1  Gladstone
         1  Heth's  #2
         1  John McGrane  #2
         1  Middle
         1  McKinley #1
         1  Banksville
         1  Banksville School
         1  East Hills
         1  Vanucci #2
         1  Willie Stargell #1
         1  Mellon # 3
         1  Jeff Rosenthal
         1  Dunbar  #2
         1  Magee  #1
         1  Sheraden  #2
         1  Mazeroski
         1  Josh Gibson #1

DPW_NAME by dollars
      12.08M        9 rows   Name
       1.38M        1 rows  East Hills
       1.37M        1 rows  Chadwick
       1.37M        1 rows  Braddock #2
       1.37M        1 rows  Jeff Rosenthal
       1.37M        1 rows  Willie Stargell #2
       1.37M        1 rows  Paulson
       1.37M        1 rows  Willie Stargell #1
       1.37M        1 rows  Fern Hollow
       1.37M        1 rows  Mcbride
       1.37M        1 rows  Farmhouse
       1.37M        1 rows  Stan Lederman
       1.37M        1 rows  Mellon # 2
       1.37M        1 rows  Mellon # 3
       1.37M        1 rows  Mellon # 1
       1.37M        1 rows  East Liberty Park (OMEGA)
       1.36M        1 rows  Joe Natoli  #1
       1.36M        1 rows  Panorama
       1.36M        1 rows  Joe Natoli  #2
       1.36M        1 rows  Joe Natoli  #3

SRC_SHA256 by rows
       130  9f8de5eb2bfa6f91aa5d232f3413affdb97b02b41fef9ba0bc9c3a3322ef24df

SRC_SHA256 by dollars
     169.77M      130 rows  9f8de5eb2bfa6f91aa5d232f3413affdb97b02b41fef9ba0bc9c3a3322ef

## who x when

FIELD_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Arsenal Band Box                          2026:1.35M
  Banksville Park                           2026:1.33M
  Braddock 1                                2026:1.37M
  Braddock 2                                2026:1.37M
  Chadwick                                  2026:1.37M
  Cowley Field 2                            2026:1.35M
  Dan Marino                                2026:1.35M
  Dean                                      2026:1.36M
  East Hills                                2026:1.38M
  Farm House                                2026:1.37M
  Fern Hollow                               2026:1.37M
  Fowler 1                                  2026:1.34M
  Gladstone                                 2026:1.36M
  Herschel Lower                            2026:1.33M
  Larimer                                   2026:1.37M
  Loretta Miller                            2026:1.34M
  McBride Park                              2026:1.37M
  Michael Flynn                             2026:1.35M
  Overbrook Field 2                         2026:1.34M
  Paulson                                   2026:1.37M
  Sam Bryan 2                               2026:1.34M
  Scherer                                   2026:1.34M
  Stan Lederman                             2026:1.37M
  Vanucci Field 1                           2026:1.34M
  Vanucci Field 2                           2026:1.34M
  Volunteers 4                              2026:1
  Warrington                                2026:1.34M
  Wightman                                  2026:1.36M
  Willie Stargell 1                         2026:1.37M
  Willie Stargell 2                         2026:1.37M

DPW_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
   Name                                     2026:12.08M
  Banksville                                2026:1.33M
  Banksville School                         2026:1.33M
  Braddock #2                               2026:1.37M
  Chadwick                                  2026:1.37M
  Dunbar  #2                                2026:1.33M
  East Hills                                2026:1.38M
  Farmhouse                                 2026:1.37M
  Fern Hollow                               2026:1.37M
  Gladstone                                 2026:1.36M
  Heth's  #2                                2026:1.36M
  Jeff Rosenthal                            2026:1.37M
  John McGrane  #2                          2026:1.35M
  Josh Gibson #1                            2026:1.35M
  Kennard  #1                               2026:1.35M
  Magee  #1                                 2026:1.36M
  Mazeroski                                 2026:1.36M
  McKinley #1                               2026:1.34M
  Mcbride                                   2026:1.37M
  Mellon # 1                                2026:1.37M
  Mellon # 2                                2026:1.37M
  Mellon # 3                                2026:1.37M
  Michael Flynn                             2026:1.35M
  Middle                                    2026:1.35M
  Paulson                                   2026:1.37M
  Sheraden  #2                              2026:1.33M
  Stan Lederman                             2026:1.37M
  Vanucci #2                                2026:1.34M
  Willie Stargell #1                        2026:1.37M
  Willie Stargell #2                        2026:1.37M

## what

ACTIVE: Yes 99%, No 1%

ANGLE: 0 100%

AREA: 0 100%

PERIMETER: 0 100%

POLYGONID: 0 100%

SCALE: 0 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACTIVE | category | 2 | 0 | Yes 129; No 1 |
| ANGLE | category | 2 | 4 | 0 126 |
| AREA | category | 2 | 4 | 0 126 |
| BALLFIEL_1 | other | 126 | 4 | 126 1; 125 1; 124 1; 123 1 |
| BALLFIELDS | other | 126 | 4 | 126 1; 125 1; 124 1; 123 1 |
| CITYID | other | 117 | 13 | P390 2; P373 2; P368 1; P369 1 |
| DPW_NAME | who | 121 | 0 |  Name 9; Schenley # 3 1; Schenley # 2 1; Volunteers #3 1 |
| FIELD_NAME | who | 130 | 0 | Schenley  3 1; Schenley 2 1; Volunteers 3 1; Volunteers 4 1 |
| ID | other | 121 | 0 | 0 9; 98 1; 97 1; 112 1 |
| OBJECTID | other | 129 | 0 | 130 1; 129 1; 128 1; 127 1 |
| PERIMETER | category | 2 | 4 | 0 126 |
| POINT_X | amount | 125 | 4 | 1333429.28024353 1; 1333698.12353785 1; 1333613.10467902 1; 1334031.30495811 1 |
| POINT_Y | amount | 126 | 4 | 429086.77724835 1; 428987.97167169 1; 428622.62102443 1; 428358.37384953 1 |
| POLYGONID | category | 2 | 4 | 0 126 |
| SCALE | category | 2 | 4 | 0 126 |
| GEOMETRY | other | 130 | 0 | POINT (589841.56955239735 1; POINT (589708.99674926244 1; POINT (585458.85920505633 1; POINT (585345.01102324866 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:34:03.77155 130 |
| SOURCE_RUN_ID | audit | 1 | 0 | c6fee1d4-84fe-4c9e-b01d-a 130 |
| SRC_SHA256 | who | 1 | 0 | 9f8de5eb2bfa6f91aa5d232f3 130 |
