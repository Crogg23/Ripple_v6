# PORTAL_CKA_WPRDC_ALLEGHENY_4CE939751E

rows 1.3K  columns 18  scan 4.1s

roles: amount 2, audit 2, category 3, date 1, id 6, other 2, who 3

## when

INGESTED_AT
  2026      1.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 1.3K | 404.4K | 5.98M | 154.87M | 574.79M | 20.75B |
| SHAPE_LENGTH | 1.3K | 2.8K | 13.1K | 67.6K | 129.2K | 22.93M |

## who

NAME by rows
       402  PITTSBURGH
        50  PENN HILLS
        38  MOUNT LEBANON
        34  SHALER
        33  ROSS
        32  MCKEESPORT
        28  BETHEL PARK
        25  MONROEVILLE
        21  PLUM
        21  WEST MIFFLIN
        21  MCCANDLESS
        20  BALDWIN
        18  UPPER ST. CLAIR
        18  SCOTT
        17  WILKINSBURG
        16  WHITEHALL
        13  MOON
        13  NORTH VERSAILLES
        13  HAMPTON
        13  SOUTH PARK

NAME by dollars
       1.63B      402 rows  PITTSBURGH
     899.35M        3 rows  FINDLAY
     806.65M        8 rows  WEST DEER
     806.23M       21 rows  PLUM
     702.32M        5 rows  NORTH FAYETTE
     674.00M       13 rows  MOON
     656.82M       12 rows  ELIZABETH
     566.10M       12 rows  SOUTH FAYETTE
     554.15M        4 rows  FORWARD
     549.73M       25 rows  MONROEVILLE
     540.03M       50 rows  PENN HILLS
     489.83M        5 rows  INDIANA
     473.05M        8 rows  PINE
     466.86M        8 rows  JEFFERSON HILLS
     462.88M       21 rows  MCCANDLESS
     451.73M       13 rows  HAMPTON
     430.42M        7 rows  MARSHALL
     427.05M        9 rows  ROBINSON
     407.78M        8 rows  RICHLAND
     404.30M       21 rows  WEST MIFFLIN

LABEL by rows
       402  Pittsburgh
        50  Penn Hills Municipality
        38  Mount Lebanon Township
        34  Shaler Township
        33  Ross Township
        32  McKeesport
        28  Bethel Park Municipality
        25  Monroeville Municipality
        21  McCandless Township
        21  Plum Borough
        21  West Mifflin Borough
        18  Upper St. Clair Municipality
        18  Baldwin Borough
        18  Scott Township
        17  Wilkinsburg Borough
        16  Whitehall Borough
        13  Hampton Township
        13  South Park Township
        13  North Versailles Township
        13  Moon Township

LABEL by dollars
       1.63B      402 rows  Pittsburgh
     899.35M        3 rows  Findlay Township
     806.65M        8 rows  West Deer Township
     806.23M       21 rows  Plum Borough
     702.32M        5 rows  North Fayette Township
     674.00M       13 rows  Moon Township
     645.21M       11 rows  Elizabeth Township
     566.10M       12 rows  South Fayette Township
     554.15M        4 rows  Forward Township
     549.73M       25 rows  Monroeville Municipality
     540.03M       50 rows  Penn Hills Municipality
     489.83M        5 rows  Indiana Township
     473.05M        8 rows  Pine Township
     466.86M        8 rows  Jefferson Hills Borough
     462.88M       21 rows  McCandless Township
     451.73M       13 rows  Hampton Township
     430.42M        7 rows  Marshall Township
     427.05M        9 rows  Robinson Township
     407.78M        8 rows  Richland Township
     404.30M       21 rows  West Mifflin Borough

SRC_SHA256 by rows
      1.3K  851616e397d47ec436a20bcd730f68c4d6243d7736d9599ee0e74b9368ffae30

SRC_SHA256 by dollars
      20.75B     1.3K rows  851616e397d47ec436a20bcd730f68c4d6243d7736d9599ee0e74b9368ff

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  BALDWIN                                   2026:177.93M
  BETHEL PARK                               2026:326.24M
  ELIZABETH                                 2026:656.82M
  FINDLAY                                   2026:899.35M
  FORWARD                                   2026:554.15M
  HAMPTON                                   2026:451.73M
  INDIANA                                   2026:489.83M
  JEFFERSON HILLS                           2026:466.86M
  MARSHALL                                  2026:430.42M
  MCCANDLESS                                2026:462.88M
  MCKEESPORT                                2026:151.80M
  MONROEVILLE                               2026:549.73M
  MOON                                      2026:674.00M
  MOUNT LEBANON                             2026:169.51M
  NORTH FAYETTE                             2026:702.32M
  NORTH VERSAILLES                          2026:227.94M
  PENN HILLS                                2026:540.03M
  PINE                                      2026:473.05M
  PITTSBURGH                                2026:1.63B
  PLUM                                      2026:806.23M
  ROSS                                      2026:403.41M
  SCOTT                                     2026:108.50M
  SHALER                                    2026:311.09M
  SOUTH FAYETTE                             2026:566.10M
  SOUTH PARK                                2026:260.28M
  UPPER ST. CLAIR                           2026:273.50M
  WEST DEER                                 2026:806.65M
  WEST MIFFLIN                              2026:404.30M
  WHITEHALL                                 2026:92.67M
  WILKINSBURG                               2026:62.79M

LABEL by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  Baldwin Borough                           2026:163.81M
  Bethel Park Municipality                  2026:326.24M
  Elizabeth Township                        2026:645.21M
  Findlay Township                          2026:899.35M
  Forward Township                          2026:554.15M
  Hampton Township                          2026:451.73M
  Indiana Township                          2026:489.83M
  Jefferson Hills Borough                   2026:466.86M
  Marshall Township                         2026:430.42M
  McCandless Township                       2026:462.88M
  McKeesport                                2026:151.80M
  Monroeville Municipality                  2026:549.73M
  Moon Township                             2026:674.00M
  Mount Lebanon Township                    2026:169.51M
  North Fayette Township                    2026:702.32M
  North Versailles Township                 2026:227.94M
  Penn Hills Municipality                   2026:540.03M
  Pine Township                             2026:473.05M
  Pittsburgh                                2026:1.63B
  Plum Borough                              2026:806.23M
  Ross Township                             2026:403.41M
  Scott Township                            2026:108.50M
  Shaler Township                           2026:311.09M
  South Fayette Township                    2026:566.10M
  South Park Township                       2026:260.28M
  Upper St. Clair Municipality              2026:273.50M
  West Deer Township                        2026:806.65M
  West Mifflin Borough                      2026:404.30M
  Whitehall Borough                         2026:92.67M
  Wilkinsburg Borough                       2026:62.79M

## what

TYPE: CITY 34%, BOROUGH 29%, TOWNSHIP 27%, MUNICIPALI 9%

DISTRICT_1: 1 22%, 2 20%, 3 14%, 4 10%, 5 7%, 6 6%, 7 5%, 0 4%, 8 4%, 9 3%, 10 3%, 11 2%

WARD_1: 0 39%, 1 10%, 3 9%, 2 9%, 4 7%, 5 6%, 7 5%, 14 4%, 6 4%, 19 4%, 8 3%, 9 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.3K | 0 | 1324 7; 1323 7; 1322 7; 1321 7 |
| NAME | who | 127 | 0 | PITTSBURGH 402; PENN HILLS 50; MOUNT LEBANON 38; SHALER 34 |
| TYPE | category | 4 | 0 | CITY 456; BOROUGH 390; TOWNSHIP 356; MUNICIPALI 121 |
| LABEL | who | 130 | 0 | Pittsburgh 402; Penn Hills Municipality 50; Mount Lebanon Township 38; Shaler Township 34 |
| DISTRICT_1 | category | 42 | 0 | 1 259; 2 236; 3 163; 4 111 |
| WARD_1 | category | 33 | 0 | 0 419; 1 103; 3 96; 2 94 |
| MUNICODE_1 | other | 128 | 0 | 188 402; 185 50; 173 38; 202 34 |
| MWD_NOPA_1 | id | 1.3K | 0 | 12401 8; 20501 8; 1881430 7; 16505 7 |
| OPA_MUNI_1 | other | 131 | 0 | 100 402; 934 50; 926 38; 944 34 |
| MWD_PAD_1 | id | 1.3K | 0 | 1881430 7; 1650007 7; 2100011 7; 1240005 7 |
| PSEUD4_12 | id | 1.3K | 0 | 0128 8; 1153 8; 0768 7; 0314 7 |
| PSEUDONU_5 | id | 1.3K | 0 | 128 8; 1153 8; 768 7; 314 7 |
| MUNI_WAR_1 | id | 1.3K | 0 | PITTSBURGH WARD 14 DIST 3 7; MARSHALL DIST 7 7; SWISSVALE DIST 11 7; COLLIER DIST 5 7 |
| SHAPE_AREA | amount | 1.4K | 0 | 2295185.82458496 7; 37078125.5874634 7; 2191104.07550049 7; 40657969.3500061 7 |
| SHAPE_LENGTH | amount | 1.3K | 0 | 7355.7888167948 7; 29210.148599904 7; 7204.20816581686 7; 39766.3232087157 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:52:40.79522 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 22f3303a-6efc-487f-8a2f-6 1.3K |
| SRC_SHA256 | who | 1 | 0 | 851616e397d47ec436a20bcd7 1.3K |
