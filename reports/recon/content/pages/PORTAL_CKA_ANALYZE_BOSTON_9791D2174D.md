# PORTAL_CKA_ANALYZE_BOSTON_9791D2174D

rows 129  columns 12  scan 4.2s

roles: amount 2, audit 2, date 1, empty 3, other 3, who 2

## when

INGESTED_AT
  2026       129  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| Y_LATITUDE | 129 | 42.24 | 42.32 | 42.39 | 42.39 | 5.5K |
| X_LONGITUDE | 129 | -71.18 | -71.08 | -71.02 | -71.01 | -9.2K |

## who

PARK_NAME by rows
         7  Carter Playground
         6  Hannon Playground
         5  Smith Playground
         4  Crawford Street Playground
         4  Cutillo Park
         3  Franklin Park (excludes Playgrounds)
         3  Children's Park
         3  Clarendon Street Playlot
         2  Garvey Playground
         1  Rossmore/Stedman Park
         1  Jeep Jones Park
         1  Oak Square
         1  Walker Playground
         1  Harambee Park
         1  Gibbons Playground
         1  Draper Playground
         1  Ryan Play Area
         1  Ripley Playground
         1  Ramler Park
         1  Dennis Street Park

PARK_NAME by dollars
      296.38        7 rows  Carter Playground
      253.92        6 rows  Hannon Playground
      211.81        5 rows  Smith Playground
      169.44        4 rows  Cutillo Park
      169.26        4 rows  Crawford Street Playground
      127.05        3 rows  Clarendon Street Playlot
      126.93        3 rows  Children's Park
      126.92        3 rows  Franklin Park (excludes Playgrounds)
       84.58        2 rows  Garvey Playground
       42.39        1 rows  Caldwell Street Play Area
       42.39        1 rows  Noyes Playground
       42.38        1 rows  Leo F. McCarthy Playground
       42.38        1 rows  Menino Park
       42.38        1 rows  Cuneo Park
       42.38        1 rows  Doherty Playground
       42.38        1 rows  Barry Playground
       42.37        1 rows  Langone Park
       42.37        1 rows  Paris Street Playground
       42.37        1 rows  Puopolo Playground
       42.37        1 rows  Porzio Park

SRC_SHA256 by rows
       129  a9055e41aab0bb770e7a0cb798b09a5a8c148b6298a20e274c4c8b642f5a4e64

SRC_SHA256 by dollars
        5.5K      129 rows  a9055e41aab0bb770e7a0cb798b09a5a8c148b6298a20e274c4c8b642f5a

## who x when

PARK_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = Y_LATITUDE
  Barry Playground                          2026:42.38
  Caldwell Street Play Area                 2026:42.39
  Carter Playground                         2026:296.38
  Children's Park                           2026:126.93
  Clarendon Street Playlot                  2026:127.05
  Crawford Street Playground                2026:169.26
  Cuneo Park                                2026:42.38
  Cutillo Park                              2026:169.44
  Dennis Street Park                        2026:42.32
  Doherty Playground                        2026:42.38
  Draper Playground                         2026:42.26
  Franklin Park (excludes Playgrounds)      2026:126.92
  Garvey Playground                         2026:84.58
  Gibbons Playground                        2026:42.33
  Hannon Playground                         2026:253.92
  Harambee Park                             2026:42.29
  Jeep Jones Park                           2026:42.33
  Langone Park                              2026:42.37
  Leo F. McCarthy Playground                2026:42.38
  Menino Park                               2026:42.38
  Noyes Playground                          2026:42.39
  Oak Square                                2026:42.35
  Paris Street Playground                   2026:42.37
  Puopolo Playground                        2026:42.37
  Ramler Park                               2026:42.34
  Ripley Playground                         2026:42.30
  Rossmore/Stedman Park                     2026:42.30
  Ryan Play Area                            2026:42.32
  Smith Playground                          2026:211.81
  Walker Playground                         2026:42.28

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = Y_LATITUDE
  a9055e41aab0bb770e7a0cb798b09a5a8c148b62  2026:5.5K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| POLYGON_ID | other | 101 | 0 | 43 7; 141 6; 284 5; 77 4 |
| PARK_NAME | who | 102 | 0 | Carter Playground 7; Hannon Playground 6; Smith Playground 5; Cutillo Park 4 |
| COORDINATES | other | 131 | 0 | 42.378272, -71.048710 1; 42.352863, -71.049340 1; 42.346157, -71.074686 1; 42.314292, -71.094064 1 |
| Y_LATITUDE | amount | 125 | 0 | 42.3637123 2; 42.3782730 1; 42.3528633 1; 42.3461571 1 |
| X_LONGITUDE | amount | 125 | 0 | -71.0565262 2; -71.0562744 2; -71.0919952 2; -71.0768280 2 |
| ADDRESS_FOR_GPS | other | 124 | 0 | 539 Commercial St, Boston 2; 625 Dudley St, Boston, MA 2; 603 Dudley St, Dorchester 2; 2 Howard Ave, Boston, MA  2 |
| SHAPE_WKT | empty | 1 | 129 |  |
| POINT_X | empty | 1 | 129 |  |
| POINT_Y | empty | 1 | 129 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:33:27.48293 129 |
| SOURCE_RUN_ID | audit | 1 | 0 | 78519dcc-71c9-47a3-9e05-6 129 |
| SRC_SHA256 | who | 1 | 0 | a9055e41aab0bb770e7a0cb79 129 |
