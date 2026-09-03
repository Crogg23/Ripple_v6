# PORTAL_CKA_WPRDC_ALLEGHENY_F38F393B45

rows 161  columns 23  scan 4.0s

roles: amount 2, audit 2, category 9, date 1, other 8, who 2

## when

INGESTED_AT
  2026       161  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 161 | 0 | 718.31 | 37.4K | 37.4K | 578.8K |
| SQMI | 161 | 0 | 1.12 | 58.36 | 58.36 | 904.30 |

## who

NAME by rows
         2  SPRINGDALE
         2  ELIZABETH
         2  BALDWIN
         1  ROSSLYN FARMS
         1  MCDONALD
         1  PITTSBURGH 14
         1  CHESWICK
         1  ETNA
         1  LIBERTY
         1  PLEASANT HILLS
         1  EMSWORTH
         1  FOX CHAPEL
         1  BEN AVON HEIGHTS
         1  WHITE OAK
         1  THORNBURG
         1  NEVILLE
         1  WHITAKER
         1  INDIANA
         1  OAKMONT
         1  HAMPTON

NAME by dollars
       37.4K        1 rows  PITTSBURGH 21
       37.4K        1 rows  PITTSBURGH 1
       37.4K        1 rows  PITTSBURGH 5
       37.4K        1 rows  PITTSBURGH 19
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

SRC_SHA256 by rows
       161  520a8bf80602cfab519a652905636115d0f78031a4e7b682c51699692eaa4f62

SRC_SHA256 by dollars
      578.8K      161 rows  520a8bf80602cfab519a652905636115d0f78031a4e7b682c51699692eaa

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  BALDWIN                                   2026:4.0K
  BEN AVON HEIGHTS                          2026:109.54
  CHESWICK                                  2026:350.19
  ELIZABETH                                 2026:15.0K
  EMSWORTH                                  2026:434.31
  ETNA                                      2026:505.65
  FINDLAY                                   2026:20.7K
  FOX CHAPEL                                2026:5.0K
  HAMPTON                                   2026:10.4K
  INDIANA                                   2026:11.3K
  LIBERTY                                   2026:943.40
  MCDONALD                                  2026:121.23
  MOON                                      2026:15.4K
  NEVILLE                                   2026:1.5K
  NORTH FAYETTE                             2026:16.1K
  OAKMONT                                   2026:1.1K
  PITTSBURGH 1                              2026:37.4K
  PITTSBURGH 14                             2026:0
  PITTSBURGH 19                             2026:37.4K
  PITTSBURGH 21                             2026:37.4K
  PITTSBURGH 5                              2026:37.4K
  PLEASANT HILLS                            2026:1.8K
  PLUM                                      2026:18.5K
  ROSSLYN FARMS                             2026:353.49
  SOUTH FAYETTE                             2026:13.0K
  SPRINGDALE                                2026:2.3K
  THORNBURG                                 2026:276.67
  WEST DEER                                 2026:18.5K
  WHITAKER                                  2026:211.79
  WHITE OAK                                 2026:4.2K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  520a8bf80602cfab519a652905636115d0f78031  2026:578.8K

## what

CNTYCOUNCIL: 13 20%, 4 13%, 8 12%, 3 11%, 1 10%, 9 9%, 2 8%, 7 5%, 6 5%, 5 4%, 11 2%, 12 2%

COG: Turtle Creek Valley 16%, Char-West 16%, North Hills 15%, South Hills Area 12%, Quaker Valley 11%, Allegheny Valley North 11%, Twin Rivers 10%, Steel Valley 7%

CONGDIST: 18 41%, 14 40%, 20 11%, 4 8%

EOC: City of Pittsburgh 21%, NEWCOM 17%, Northwest Regional 16%, East Regional 15%, Mon-Valley 12%, Southwest Regional 11%, South Hills Regional 8%

MAGISTERIAL_DISTRICT: Magisterial District 05-3-02 17%, Magisterial District 05-2-01 10%, Magisterial District 05-2-08 8%, Magisterial District 05-2-04 8%, Magisterial District 05-2-23 8%, Magisterial District 05-3-14 7%, Magisterial District 05-2-40 7%, Magisterial District 05-2-47 7%, Magisterial District 05-2-11 7%, Magisterial District 05-2-05 7%, Magisterial District 05-3-03 7%, Magisterial District 05-2-28 6%

REGION: NH 23%, PGH 20%, MV 19%, AA 19%, SH 11%, ES 8%

SCHOOLD: City of Pittsburgh 34%, Woodland Hills 12%, Quaker Valley 11%, Fox Chapel Area 6%, Avonworth 5%, Montour 5%, McKeesport Area 5%, Chartiers Valley 4%, North Allegheny 4%, East Allegheny 4%, Shaler Area 4%, Highlands 4%

TYPE: BOROUGH 51%, TOWNSHIP 24%, CITY 22%, MUNICIPALI 3%

YEARCONVERTED: 1948 32%, 1953 9%, 1954 9%, 2007 9%, 1974 7%, 1971 6%, 1955 6%, 1956 5%, 1959 4%, 1972 4%, 1977 4%, 1975 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACRES | amount | 126 | 0 | 0.0 28; 37352.0703125 4; 1510.90808105 2; 7491.74658203 2 |
| CNTL_ID | other | 125 | 0 | 003435 32; 003370 2; 003045 2; 003180 2 |
| CNTYCOUNCIL | category | 14 | 0 | 13 32; 4 20; 8 19; 3 17 |
| COG | category | 9 | 39 | Turtle Creek Valley 20; Char-West 20; North Hills 18; South Hills Area 15 |
| CONGDIST | category | 4 | 0 | 18 66; 14 65; 20 17; 4 13 |
| COVERAGE | other | 160 | 0 | Elizabeth 2; Baldwin 2; Springdale 2; Pittsburgh 32 1 |
| EOC | category | 8 | 1 | City of Pittsburgh 33; NEWCOM 27; Northwest Regional 26; East Regional 24 |
| FIPS | other | 128 | 0 | 61000 32; 6064 2; 26592 1; 66264 1 |
| GLOBALID | other | 162 | 0 | 2f1a2d6e-ab0d-4120-95d4-6 1; 697dadb3-521f-408b-a1db-a 1; 8ca546db-8662-4908-8942-5 1; a32d9fb4-a548-44d1-9841-0 1 |
| LABEL | other | 130 | 0 | Pittsburgh 32; Forest Hills Borough 1; Ross Township 1; West View Borough 1 |
| MUNICODE | other | 162 | 0 | 132 1; 129 1; 131 1; 130 1 |
| MAGISTERIAL_DISTRICT | category | 45 | 0 | Magisterial District 05-3 12; Magisterial District 05-2 7; Magisterial District 05-2 6; Magisterial District 05-2 6 |
| NAME | who | 158 | 0 | ELIZABETH 2; BALDWIN 2; SPRINGDALE 2; PITTSBURGH 32 1 |
| OBJECTID | other | 161 | 0 | 194 1; 193 1; 192 1; 191 1 |
| REGION | category | 6 | 0 | NH 37; PGH 33; MV 31; AA 30 |
| SCHOOLD | category | 45 | 0 | City of Pittsburgh 33; Woodland Hills 12; Quaker Valley 11; Fox Chapel Area 6 |
| SQMI | amount | 129 | 0 | 0.0 28; 58.3626098632813 4; 2.36079382 2; 11.70585441 2 |
| TYPE | category | 4 | 0 | BOROUGH 82; TOWNSHIP 39; CITY 35; MUNICIPALI 5 |
| YEARCONVERTED | category | 44 | 0 | 1948 32; 1953 9; 1954 9; 2007 9 |
| GEOMETRY | other | 162 | 0 | POLYGON ((584814.24648084 1; POLYGON ((585538.02713004 1; POLYGON ((590129.89284758 1; POLYGON ((585839.22203280 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:35:58.08223 161 |
| SOURCE_RUN_ID | audit | 1 | 0 | 53044261-934e-45b1-9d73-0 161 |
| SRC_SHA256 | who | 1 | 0 | 520a8bf80602cfab519a65290 161 |
