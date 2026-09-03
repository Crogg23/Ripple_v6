# PORTAL_CKA_WPRDC_ALLEGHENY_7103930983

rows 130  columns 19  scan 4.5s

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
         1  Bandi Shaum
         1  Fern Hollow
         1  Bud Hammer
         1  West Penn 2
         1  Willie Stargell 1
         1  Cowley Field 2
         1  Dean
         1  Camelius Sangnini
         1  Michael Flynn
         1  Brighton Heights 4
         1  Paulson
         1  Braddock 1
         1  Heth's 2
         1  Winters
         1  Kennard 2
         1  Overbrook Field 2
         1  Wightman
         1  Martin Luther King
         1  Quary
         1  Volunteers 1

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
         1  Westwood  #1
         1  West Penn #1
         1  Volunteers #1
         1  Magee  #2
         1  Banksville
         1  Ray Miller
         1  Stan Lederman
         1  Herschel #2 (Upper)
         1  Dunbar  #1
         1  Jeff Rosenthal
         1  Willie Stargell #1
         1  Farmhouse
         1  Four Mile Run
         1  Westwood  #2
         1  Burgwin
         1  Officer Paul J. Sciullo II Memorial Field
         1  East Hills
         1  Phillip Murray
         1  Southside # 1 (Behind Arlington Firehouse)

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
  Bandi Shaum                               2026:1.35M
  Braddock 1                                2026:1.37M
  Braddock 2                                2026:1.37M
  Brighton Heights 4                        2026:1.33M
  Bud Hammer                                2026:1.36M
  Camelius Sangnini                         2026:1.33M
  Chadwick                                  2026:1.37M
  Cowley Field 2                            2026:1.35M
  Dean                                      2026:1.36M
  East Hills                                2026:1.38M
  Farm House                                2026:1.37M
  Fern Hollow                               2026:1.37M
  Heth's 2                                  2026:1.36M
  Kennard 2                                 2026:1.35M
  Larimer                                   2026:1.37M
  Martin Luther King                        2026:1.34M
  McBride Park                              2026:1.37M
  Mellon Park Main                          2026:1.37M
  Mellon Park Middle                        2026:1.37M
  Michael Flynn                             2026:1.35M
  Overbrook Field 2                         2026:1.34M
  Paulson                                   2026:1.37M
  Quary                                     2026:1.35M
  Stan Lederman                             2026:1.37M
  Volunteers 1                              2026:1.34M
  West Penn 2                               2026:1.35M
  Wightman                                  2026:1.36M
  Willie Stargell 1                         2026:1.37M
  Willie Stargell 2                         2026:1.37M
  Winters                                   2026:1.35M

DPW_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
   Name                                     2026:12.08M
  Banksville                                2026:1.33M
  Braddock #2                               2026:1.37M
  Burgwin                                   2026:1.36M
  Chadwick                                  2026:1.37M
  Dunbar  #1                                2026:1.33M
  East Hills                                2026:1.38M
  East Liberty Park (OMEGA)                 2026:1.37M
  Farmhouse                                 2026:1.37M
  Fern Hollow                               2026:1.37M
  Four Mile Run                             2026:1.36M
  Herschel #2 (Upper)                       2026:1.33M
  Jeff Rosenthal                            2026:1.37M
  Magee  #2                                 2026:1.36M
  Mcbride                                   2026:1.37M
  Mellon # 1                                2026:1.37M
  Mellon # 2                                2026:1.37M
  Mellon # 3                                2026:1.37M
  Officer Paul J. Sciullo II Memorial Fiel  2026:1.36M
  Paulson                                   2026:1.37M
  Phillip Murray                            2026:1.35M
  Ray Miller                                2026:1.36M
  Southside # 1 (Behind Arlington Firehous  2026:1.35M
  Stan Lederman                             2026:1.37M
  Volunteers #1                             2026:1.34M
  West Penn #1                              2026:1.35M
  Westwood  #1                              2026:1.33M
  Westwood  #2                              2026:1.33M
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
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:33:47.27736 130 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5686df29-112d-433b-bc5e-5 130 |
| SRC_SHA256 | who | 1 | 0 | 9f8de5eb2bfa6f91aa5d232f3 130 |
