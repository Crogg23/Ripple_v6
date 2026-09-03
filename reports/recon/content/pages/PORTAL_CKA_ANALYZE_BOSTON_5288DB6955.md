# PORTAL_CKA_ANALYZE_BOSTON_5288DB6955

rows 191  columns 20  scan 4.6s

roles: amount 2, audit 2, category 7, date 4, other 4, who 2

## when

DATE_DESIGNATED_1
  1977        11  ########################
  1978         7  ###############
  1979         3  ######
  1980         3  ######
  1981         3  ######
  1983        14  ##############################
  1984         1  ##
  1985         5  ###########
  1986         2  ####
  1987         1  ##
  1989         5  ###########
  1990         1  ##
  1991         1  ##
  1992         2  ####
  1993         1  ##
  1994         3  ######
  1995         1  ##
  1996         2  ####
  1997         1  ##
  1998         2  ####
  1999         3  ######
  2000         1  ##
  2002         1  ##
  2003         1  ##
  2004         1  ##
  2006         2  ####
  2007         2  ####
  2009         1  ##
  2011         3  ######
  2013         1  ##
  2014         1  ##
  2016         3  ######
  2021         4  #########
  2022         5  ###########
  2023         7  ###############
  2024        12  ##########################
  2025         7  ###############
  2026         4  #########

CREATED_DATE
  2024         2  #####
  2025        12  ##############################
  2026         1  ##

LAST_EDITED_DATE
  2023         2  #
  2024        15  ######
  2025        54  ####################
  2026        81  ##############################

INGESTED_AT
  2026       191  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 191 | 0 | 0 | 0.07 | 0.10 | 0.67 |
| SHAPE_AREA | 191 | 0 | 0 | 0 | 0 | 0 |

## who

COMMON_NAME by rows
         1  Keith Memorial/Opera House (int &exterior)
         1  William Monroe Trotter House
         1  Joseph H. Barnes School
         1  Old North Church & Campus
         1  Old South Building
         1  Berkeley Building
         1  Ropewalk, The
         1  Malcolm X Ella Little-Collins House
         1  Tileston House
         1  Broad Street, 66
         1  Ames-Barnard-Everett House
         1  Old South Meeting House
         1  Pope/Cahner's Building
         1  Loring-Greenough House
         1  McCormack Federal Bldg/Post Office/Courthse
         1  Proctor Building
         1  Museum of Fine Arts
         1  Trinity Church
         1  Ferdinand's Blue Store
         1  Samuel Appleton Building

COMMON_NAME by dollars
        0.10        1 rows  Emerald Necklace (Riverway, Olmsted Park, Willow Pond Meadow
        0.10        1 rows  Charles River Esplanade
        0.07        1 rows  Franklin Park
        0.05        1 rows  Chestnut Hill Reservoir & Pumping Station Comp
        0.05        1 rows  Brook Farm
        0.05        1 rows  Commonwealth Avenue Mall
        0.04        1 rows  Back Bay Fens
        0.02        1 rows  Boston Common
        0.01        1 rows  Boston Fish Pier
        0.01        1 rows  Mission Church Complex
        0.01        1 rows  Public Garden
        0.01        1 rows  Boston Public Library, main branch
        0.01        1 rows  Harvard Medical School
        0.01        1 rows  Christian Science Church Complex
        0.01        1 rows  Dorchester North Burying Ground
        0.01        1 rows  Fenway Park
        0.01        1 rows  Blessed Sacrament Church Complex
        0.01        1 rows  Shirley-Eustis Place
        0.01        1 rows  Adams Nervine Asylum
        0.01        1 rows  St. Gabriel's Monastery Building (see #51)

SRC_SHA256 by rows
       191  10e420c2fa42b0443af7f07ffbdadb498a31253c81683cfb10d94818fe1d7635

SRC_SHA256 by dollars
        0.67      191 rows  10e420c2fa42b0443af7f07ffbdadb498a31253c81683cfb10d94818fe1d

## who x when

COMMON_NAME by LAST_EDITED_DATE, dollars = SHAPE_LENGTH
  Ames-Barnard-Everett House                2026:0
  Back Bay Fens                             2026:0.04
  Berkeley Building                         2025:0
  Boston Common                             2026:0.02
  Boston Fish Pier                          2026:0.01
  Chestnut Hill Reservoir & Pumping Statio  2026:0.05
  Emerald Necklace (Riverway, Olmsted Park  2026:0.10
  Ferdinand's Blue Store                    2025:0
  Franklin Park                             2026:0.07
  Joseph H. Barnes School                   2026:0
  Keith Memorial/Opera House (int &exterio  2025:0
  Malcolm X Ella Little-Collins House       2026:0
  McCormack Federal Bldg/Post Office/Court  2025:0
  Mission Church Complex                    2026:0.01
  Museum of Fine Arts                       2026:0.01
  Old North Church & Campus                 2025:0
  Old South Building                        2026:0
  Old South Meeting House                   2026:0
  Ropewalk, The                             2024:0.01
  Samuel Appleton Building                  2025:0
  Trinity Church                            2025:0
  William Monroe Trotter House              2026:0

SRC_SHA256 by LAST_EDITED_DATE, dollars = SHAPE_LENGTH
  10e420c2fa42b0443af7f07ffbdadb498a31253c  2023:0 2024:0.03 2025:0.03 2026:0.37

## what

NEIGHBORHOOD: Downtown 35%, Dorchester 13%, Roxbury 9%, Back Bay 9%, Jamaica Plain 6%, Fenway / Kenmore 6%, Charlestown 6%, Brighton 6%, East Boston 3%, North End 3%, Mission Hill 3%

STATUS: Approved Landmark 68%, Pending Landmark 32%

PETITIONER: 10 Voters 51%, Commissioner 26%, 10 voters 14%, 10 Registered Voters 9%, 10 Bowdoin Street 1%, Mayor 1%

DISPLAY: Yes 100%

DEMOLISHED: No 99%, NO 1%

CREATED_USER: 149321 100%

LAST_EDITED_USER: 149321 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNIQUE_ID | other | 175 | 15 | 297.250000000000000 1; 299.250000000000000 1; 298.250000000000000 1; 296.250000000000000 1 |
| NEIGHBORHOOD | category | 27 | 23 | Downtown 50; Dorchester 19; Roxbury 13; Back Bay 13 |
| COMMON_NAME | who | 190 | 0 | Five Cents Savings Bank 1; 3-4 Folsom Ave 1; Jordan Marsh 1; Wesleyan Association Buil 1 |
| STATUS | category | 2 | 0 | Approved Landmark 130; Pending Landmark 61 |
| AREAS_UNDER_JURISDICTION | other | 89 | 49 | Exterior Only 31; Exterior 12; Interior 5; Exterior Only  4 |
| PETITIONER | category | 7 | 1 | 10 Voters 96; Commissioner 49; 10 voters 26; 10 Registered Voters 17 |
| STUDY_REPORT | other | 129 | 61 | https://www.boston.gov/si 1; https://www.boston.gov/si 1; https://www.boston.gov/si 1; https://www.boston.gov/si 1 |
| DISPLAY | category | 2 | 15 | Yes 176 |
| DEMOLISHED | category | 3 | 27 | No 163; NO 1 |
| DATE_DESIGNATED_1 | date | 103 | 63 | 11/1/1983 0:00:00 6; 5/10/1977 0:00:00 5; 4/25/1978 0:00:00 3; 4/9/1985 0:00:00 3 |
| CREATED_USER | category | 2 | 176 | 149321 15 |
| CREATED_DATE | date | 16 | 176 | 7/10/2025 20:36:43 1; 4/16/2026 15:23:45 1; 11/13/2025 16:05:15 1; 7/10/2025 20:35:21 1 |
| LAST_EDITED_USER | category | 2 | 39 | 149321 152 |
| LAST_EDITED_DATE | date | 154 | 39 | 7/10/2025 20:36:43 1; 4/16/2026 15:23:45 1; 11/13/2025 16:05:15 1; 7/10/2025 20:35:21 1 |
| SHAPE_LENGTH | amount | 191 | 0 | 0.000716061473820 3; 0.000644867788904 2; 0.002281621443905 2; 0.002104932139574 1 |
| SHAPE_AREA | amount | 190 | 0 | 0.000000027479196 3; 0.000000021243816 2; 0.000000278421167 2; 0.000000219988857 1 |
| SHAPE_WKT | other | 96 | 93 | MULTIPOLYGON (((-71.05320 3; MULTIPOLYGON (((-71.05464 2; MULTIPOLYGON (((-71.09951 1; MULTIPOLYGON (((-71.06045 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:36:40.59417 191 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8ae30610-17e3-4a5c-a712-a 191 |
| SRC_SHA256 | who | 1 | 0 | 10e420c2fa42b0443af7f07ff 191 |
