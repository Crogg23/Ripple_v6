# PORTAL_CKA_WPRDC_ALLEGHENY_680EA60076

rows 130  columns 23  scan 4.4s

roles: amount 2, audit 2, category 10, date 1, other 7, who 2

## when

INGESTED_AT
  2026       130  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 129 | 37.14 | 1.0K | 18.5K | 20.7K | 429.4K |
| SQMI | 129 | 0.06 | 1.61 | 28.95 | 32.34 | 670.86 |

## who

NAME by rows
         2  ELIZABETH
         2  SPRINGDALE
         2  BALDWIN
         1  BETHEL PARK
         1  COLLIER
         1  ALEPPO
         1  FOREST HILLS
         1  TRAFFORD
         1  RICHLAND
         1  WEST ELIZABETH
         1  CRAFTON
         1  STOWE
         1  OAKMONT
         1  MUNHALL
         1  WEST MIFFLIN
         1  BELLEVUE
         1  FOX CHAPEL
         1  KENNEDY
         1  NORTH VERSAILLES
         1  ROBINSON

NAME by dollars
       20.7K        1 rows  FINDLAY
       18.5K        1 rows  PLUM
       18.5K        1 rows  WEST DEER
       16.1K        1 rows  NORTH FAYETTE
       15.4K        1 rows  MOON
       15.0K        2 rows  ELIZABETH
       13.0K        1 rows  SOUTH FAYETTE
       12.7K        1 rows  FORWARD
       12.6K        1 rows  MONROEVILLE
       12.5K        1 rows  PENN HILLS
       11.3K        1 rows  INDIANA
       10.8K        1 rows  JEFFERSON HILLS
       10.8K        1 rows  PINE
       10.6K        1 rows  MCCANDLESS
       10.4K        1 rows  HAMPTON
        9.9K        1 rows  MARSHALL
        9.6K        1 rows  ROBINSON
        9.4K        1 rows  RICHLAND
        9.3K        1 rows  ROSS
        8.9K        1 rows  COLLIER

SRC_SHA256 by rows
       130  9c3b91b0f0accb133732f18e9e77e5423520e9854223803d304e678587b351ef

SRC_SHA256 by dollars
      429.4K      130 rows  9c3b91b0f0accb133732f18e9e77e5423520e9854223803d304e678587b3

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  ALEPPO                                    2026:1.1K
  BALDWIN                                   2026:4.0K
  BELLEVUE                                  2026:706.69
  BETHEL PARK                               2026:7.5K
  COLLIER                                   2026:8.9K
  CRAFTON                                   2026:734.25
  ELIZABETH                                 2026:15.0K
  FINDLAY                                   2026:20.7K
  FOREST HILLS                              2026:990.76
  FORWARD                                   2026:12.7K
  FOX CHAPEL                                2026:5.0K
  INDIANA                                   2026:11.3K
  KENNEDY                                   2026:3.5K
  MONROEVILLE                               2026:12.6K
  MOON                                      2026:15.4K
  MUNHALL                                   2026:1.5K
  NORTH FAYETTE                             2026:16.1K
  NORTH VERSAILLES                          2026:5.3K
  OAKMONT                                   2026:1.1K
  PENN HILLS                                2026:12.5K
  PLUM                                      2026:18.5K
  RICHLAND                                  2026:9.4K
  ROBINSON                                  2026:9.6K
  SOUTH FAYETTE                             2026:13.0K
  SPRINGDALE                                2026:2.3K
  STOWE                                     2026:1.5K
  TRAFFORD                                  2026:93.27
  WEST DEER                                 2026:18.5K
  WEST ELIZABETH                            2026:146.38
  WEST MIFFLIN                              2026:1.5K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  9c3b91b0f0accb133732f18e9e77e5423520e985  2026:429.4K

## what

ASSESSORTERRITORY: North 28%, East 27%, South 25%, West 18%, City 2%

VALUATIONAREA: Mon Valley 30%, West 18%, North 16%, Northwest 14%, Alle-Kiski Valley 8%, South 8%, East 4%, City 1%, Pittsburgh 1%

CONGDIST: 18 51%, 14 26%, 20 13%, 4 10%

SCHOOLD: Woodland Hills 18%, Quaker Valley 16%, Fox Chapel Area 9%, Avonworth 7%, McKeesport Area 7%, Montour 7%, North Allegheny 6%, East Allegheny 6%, Chartiers Valley 6%, South Allegheny 6%, Allegheny Valley 6%, Shaler Area 6%

TYPE: BOROUGH 63%, TOWNSHIP 31%, CITY 3%, MUNICIPALI 3%

EOC: NEWCOM 21%, Northwest Regional 20%, East Regional 19%, Mon-Valley 16%, Southwest Regional 14%, South Hills Regional 9%, City of Pittsburgh 2%

YEARCONVERTED: 2007 13%, 1953 13%, 1954 13%, 1974 10%, 1971 9%, 1955 9%, 1956 7%, 1972 6%, 1975 6%, 1977 6%, 1959 6%, 1968 4%

COG: South Hills Area 17%, Turtle Creek Valley 16%, North Hills 15%, Steel Rivers 15%, Char-West 13%, Allegheny Valley North 11%, Quaker Valley 11%

REGION: NH 28%, MV 24%, AA 23%, SH 13%, ES 10%, PGH 2%

CNTYCOUNCIL: 4 16%, 8 15%, 3 13%, 1 12%, 9 12%, 2 9%, 6 6%, 7 6%, 5 5%, 12 2%, 11 2%, 13 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ASSESSORTERRITORY | category | 5 | 0 | North 37; East 35; South 33; West 23 |
| GLOBALID | other | 130 | 0 | 2c77dd9d-5da5-46af-bd2a-a 1; 0a3e017b-106c-4c84-bf07-a 1; 3f1307b7-1854-4b1e-a963-6 1; f45fc136-88ef-45be-b81d-1 1 |
| MUNICODE | other | 131 | 0 | 100 1; 910 1; 935 1; 907 1 |
| VALUATIONAREA | category | 9 | 0 | Mon Valley 39; West 23; North 21; Northwest 18 |
| FIPS | other | 129 | 0 | 6064 2; 61000 1; 25904 1; 60272 1 |
| CONGDIST | category | 4 | 0 | 18 66; 14 34; 20 17; 4 13 |
| CNTL_ID | other | 125 | 0 | 003045 2; 003020 2; 003370 2; 003180 2 |
| SCHOOLD | category | 45 | 0 | Woodland Hills 12; Quaker Valley 11; Fox Chapel Area 6; Avonworth 5 |
| TYPE | category | 4 | 0 | BOROUGH 82; TOWNSHIP 40; CITY 4; MUNICIPALI 4 |
| NAME | who | 127 | 0 | BALDWIN 2; ELIZABETH 2; SPRINGDALE 2; PITTSBURGH 1 |
| EOC | category | 8 | 1 | NEWCOM 27; Northwest Regional 26; East Regional 24; Mon-Valley 20 |
| ACRES | amount | 125 | 1 | 7491.74658203 2; 1510.90808105 2; 20697.90429687 1; 10785.910156 1 |
| YEARCONVERTED | category | 44 | 0 | 2007 9; 1953 9; 1954 9; 1974 7 |
| LABEL | other | 130 | 0 | Pittsburgh 1; Findlay Township 1; Pine Township 1; East Deer Township 1 |
| OBJECTID | other | 129 | 0 | 43932 1; 43531 1; 42329 1; 41527 1 |
| COG | category | 8 | 7 | South Hills Area 21; Turtle Creek Valley 20; North Hills 19; Steel Rivers 19 |
| REGION | category | 6 | 0 | NH 37; MV 31; AA 30; SH 17 |
| SQMI | amount | 128 | 1 | 11.70585441 2; 2.36079382 2; 32.34046936 1; 16.852983 1 |
| CNTYCOUNCIL | category | 14 | 0 | 4 20; 8 19; 3 17; 1 16 |
| DATASPATIAL_WKB | other | 129 | 0 | \x00000000030000000200000 1; \x00000000030000000100000 1; \x00000000030000000100000 1; \x00000000030000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:33:33.62430 130 |
| SOURCE_RUN_ID | audit | 1 | 0 | 292bde4d-d463-4361-9834-4 130 |
| SRC_SHA256 | who | 1 | 0 | 9c3b91b0f0accb133732f18e9 130 |
