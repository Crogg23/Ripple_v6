# PORTAL_CKA_WESTERN_PENNSYLV_4A48DEDEFA

rows 749  columns 11  scan 4.9s

roles: amount 2, audit 2, date 1, other 3, who 4

## when

INGESTED_AT
  2026       749  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__LENGTH | 749 | 154.85 | 1.7K | 21.4K | 107.0K | 2.57M |
| SHAPE__AREA | 749 | 987.26 | 131.1K | 8.95M | 50.26M | 542.44M |

## who

NAME by rows
         4  RIVERVIEW PARK
         3  RIVERFRONT PARK
         3  HIGHLAND PARK
         3  DENNY PARK
         2  KELLY PARK
         2  HAYS PARK
         2  FRICK PARK
         2  CHARTIERS PARK
         2  KENNEDY PARK
         2  ARMSTRONG PARK
         2  TRIANGLE PARK
         2  HAMILTON AVENUE PLAYGROUND
         2  GRANDVIEW PARK
         2  ORMSBY PARK
         2  BON AIR PARK
         2  KABOOM PLAYGROUND
         2  TUSTIN PARK
         2  FRIENDSHIP PARK
         2  OVERLOOK PARK
         2  MEMORIAL PARK

NAME by dollars
      107.0K        1 rows  SEWICKLEY HEIGHTS PARK
       89.7K        3 rows  HIGHLAND PARK
       80.3K        1 rows  EMERALD VIEW PARK
       76.1K        2 rows  FRICK PARK
       39.0K        1 rows  SCHENLEY PARK
       37.8K        1 rows  HAYS WOODS
       30.1K        1 rows  BOYCE MAYVIEW PARK
       27.0K        4 rows  RIVERVIEW PARK
       21.6K        1 rows  FALL RUN PARK
       20.8K        1 rows  MOUNT WASHINGTON PARK
       19.5K        1 rows  BELL ACRES NATURE PARK
       18.3K        1 rows  LOCKHART PARK
       18.2K        1 rows  RENZIEHAUSEN PARK
       17.9K        1 rows  MOON PARK
       17.8K        1 rows  MCKINLEY PARK
       17.6K        1 rows  MONROEVILLE COMMUNITY PARK WEST
       17.4K        1 rows  SALAMANDER PARK
       17.3K        1 rows  TRILLIUM TRAIL 
       16.4K        1 rows  ELMLEAF PARK
       15.8K        1 rows  WALKER PARK

MUNICIPALITY by rows
       169  CITY OF PITTSBURGH
        23  ROSS TOWNSHIP
        22  MONROEVILLE MUNICIPALITY
        20  UPPER SAINT CLAIR MUNICIPALITY
        18  WEST MIFFLIN BOROUGH
        17  PENN HILLS MUNICIPALITY
        17  CITY OF MCKEESPORT
        15  BETHEL PARK MUNICIPALITY
        15  MOUNT LEBANON MUNICIPALITY
        13  SHALER TOWNSHIP
        10  SCOTT TOWNSHIP
        10  ELIZABETH TOWNSHIP
        10  FOX CHAPEL BOROUGH
        10  CITY OF CLAIRTON
        10  MOON TOWNSHIP
         9  OHARA TOWNSHIP
         8  HOMESTEAD BOROUGH
         8  SEWICKLEY BOROUGH
         8  GREEN TREE BOROUGH
         8  MUNHALL BOROUGH

MUNICIPALITY by dollars
      705.6K      169 rows  CITY OF PITTSBURGH
      130.4K       22 rows  MONROEVILLE MUNICIPALITY
      116.4K        2 rows  SEWICKLEY HEIGHTS BOROUGH
      100.8K       10 rows  FOX CHAPEL BOROUGH
       89.1K       20 rows  UPPER SAINT CLAIR MUNICIPALITY
       68.1K       23 rows  ROSS TOWNSHIP
       56.6K       15 rows  MOUNT LEBANON MUNICIPALITY
       53.8K       13 rows  SHALER TOWNSHIP
       49.3K       17 rows  PENN HILLS MUNICIPALITY
       48.7K       10 rows  MOON TOWNSHIP
       48.7K       18 rows  WEST MIFFLIN BOROUGH
       40.1K        5 rows  SOUTH FAYETTE TOWNSHIP
       39.0K       15 rows  BETHEL PARK MUNICIPALITY
       35.9K       17 rows  CITY OF MCKEESPORT
       30.2K        5 rows  FRANKLIN PARK BOROUGH
       30.0K        7 rows  BALDWIN BOROUGH
       28.1K       10 rows  ELIZABETH TOWNSHIP
       26.9K        3 rows  PINE TOWNSHIP
       26.5K        7 rows  COLLIER TOWNSHIP
       24.8K        9 rows  OHARA TOWNSHIP

TYPE by rows
       749  MUNICIPAL PARK

TYPE by dollars
       2.57M      749 rows  MUNICIPAL PARK

SRC_SHA256 by rows
       749  a4de39d762fb4ebaafa21ca3397d32eaf603d0e91e60c877436a6f825af98124

SRC_SHA256 by dollars
       2.57M      749 rows  a4de39d762fb4ebaafa21ca3397d32eaf603d0e91e60c877436a6f825af9

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  ARMSTRONG PARK                            2026:4.6K
  BELL ACRES NATURE PARK                    2026:19.5K
  BON AIR PARK                              2026:2.0K
  BOYCE MAYVIEW PARK                        2026:30.1K
  CHARTIERS PARK                            2026:7.6K
  DENNY PARK                                2026:9.8K
  EMERALD VIEW PARK                         2026:80.3K
  FALL RUN PARK                             2026:21.6K
  FRICK PARK                                2026:76.1K
  FRIENDSHIP PARK                           2026:2.6K
  GRANDVIEW PARK                            2026:12.2K
  HAMILTON AVENUE PLAYGROUND                2026:2.1K
  HAYS PARK                                 2026:2.5K
  HAYS WOODS                                2026:37.8K
  HIGHLAND PARK                             2026:89.7K
  KABOOM PLAYGROUND                         2026:1.1K
  KELLY PARK                                2026:3.8K
  KENNEDY PARK                              2026:3.2K
  LOCKHART PARK                             2026:18.3K
  MEMORIAL PARK                             2026:2.6K
  MOUNT WASHINGTON PARK                     2026:20.8K
  ORMSBY PARK                               2026:2.2K
  OVERLOOK PARK                             2026:4.8K
  RENZIEHAUSEN PARK                         2026:18.2K
  RIVERFRONT PARK                           2026:7.3K
  RIVERVIEW PARK                            2026:27.0K
  SCHENLEY PARK                             2026:39.0K
  SEWICKLEY HEIGHTS PARK                    2026:107.0K
  TRIANGLE PARK                             2026:5.9K
  TUSTIN PARK                               2026:2.7K

MUNICIPALITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  BALDWIN BOROUGH                           2026:30.0K
  BETHEL PARK MUNICIPALITY                  2026:39.0K
  CITY OF CLAIRTON                          2026:19.2K
  CITY OF MCKEESPORT                        2026:35.9K
  CITY OF PITTSBURGH                        2026:705.6K
  COLLIER TOWNSHIP                          2026:26.5K
  ELIZABETH TOWNSHIP                        2026:28.1K
  FOX CHAPEL BOROUGH                        2026:100.8K
  FRANKLIN PARK BOROUGH                     2026:30.2K
  GREEN TREE BOROUGH                        2026:19.1K
  HOMESTEAD BOROUGH                         2026:5.8K
  MONROEVILLE MUNICIPALITY                  2026:130.4K
  MOON TOWNSHIP                             2026:48.7K
  MOUNT LEBANON MUNICIPALITY                2026:56.6K
  MUNHALL BOROUGH                           2026:12.5K
  OHARA TOWNSHIP                            2026:24.8K
  PENN HILLS MUNICIPALITY                   2026:49.3K
  PINE TOWNSHIP                             2026:26.9K
  ROSS TOWNSHIP                             2026:68.1K
  SCOTT TOWNSHIP                            2026:18.1K
  SEWICKLEY BOROUGH                         2026:15.6K
  SEWICKLEY HEIGHTS BOROUGH                 2026:116.4K
  SHALER TOWNSHIP                           2026:53.8K
  SOUTH FAYETTE TOWNSHIP                    2026:40.1K
  UPPER SAINT CLAIR MUNICIPALITY            2026:89.1K
  WEST MIFFLIN BOROUGH                      2026:48.7K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SHAPE__LENGTH | amount | 747 | 0 | 4033.403658473019 4; 37773.25139481057 4; 2020.0184094520432 4; 8529.708950850167 4 |
| TYPE | who | 1 | 0 | MUNICIPAL PARK 749 |
| SHAPE__AREA | amount | 762 | 0 | 48312.18518066406 4; 27340141.36657715 4; 115462.6195678711 4; 982748.0737915039 4 |
| OBJECTID | other | 734 | 0 | 1400 4; 1399 4; 1389 4; 1388 4 |
| MUNICIPALITY | who | 122 | 0 | CITY OF PITTSBURGH 169; ROSS TOWNSHIP 23; MONROEVILLE MUNICIPALITY 22; UPPER SAINT CLAIR MUNICIP 20 |
| FULL_ADDRESS | other | 756 | 4 | 601 FORT DUQUESNE BLVD 4; 501 WASHINGTON PL 4; 1230 DRIFTWOOD DR 4; 2201 EDEN PARK BLVD 4 |
| NAME | who | 701 | 2 | MEMORIAL PARK 5; ALLEGHENY RIVERFRONT PARK 4; HAYS WOODS 4; FRANKIE PACE PARK 4 |
| DATASPATIAL_WKB | other | 746 | 0 | \x00000000060000000400000 4; \x00000000060000000400000 4; \x00000000060000000200000 4; \x00000000060000000200000 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:46:26.48632 749 |
| SOURCE_RUN_ID | audit | 1 | 0 | ef2bc688-8997-4f12-85bb-f 749 |
| SRC_SHA256 | who | 1 | 0 | a4de39d762fb4ebaafa21ca33 749 |
