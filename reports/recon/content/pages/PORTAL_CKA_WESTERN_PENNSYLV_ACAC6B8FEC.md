# PORTAL_CKA_WESTERN_PENNSYLV_ACAC6B8FEC

rows 76  columns 8  scan 3.0s

roles: amount 2, audit 2, category 1, date 1, other 1, who 2

## when

INGESTED_AT
  2026        76  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 76 | 40.41 | 40.45 | 40.47 | 40.48 | 3.1K |
| LONGITUDE | 76 | -80.02 | -79.96 | -79.92 | -79.90 | -6.1K |

## who

STATION_NAME by rows
         1  14th St & Penn Ave
         1  Ellsworth Ave & N Neville St
         1  Penn Ave & N Atlantic Ave
         1  Alder St & S Highland Ave
         1  Penn Ave & S Whitfield St
         1  S Winebiddle St & Penn Ave
         1  Hobart St & Wightman St
         1  Lytle St & Eliza St
         1  Penn Ave & 39th St
         1  12th St & Penn Ave
         1  10th St & Penn Ave
         1  Fifth Ave & S Bouquet St
         1  24th St & Smallman St
         1  Beacon St & Murray Ave
         1  Boulevard of the Allies & Parkview Ave
         1  Liberty Ave & Stanwix St
         1  S Bouquet Ave & Sennott St
         1  Penn Ave & Putnam St (Bakery Square)
         1  Eliza Furnace Trail at Swinburne St
         1  Zulema St & Coltart Ave

STATION_NAME by dollars
       40.48        1 rows  Butler St & Stanton Ave
       40.47        1 rows  42nd St & Butler St
       40.47        1 rows  42nd & Penn Ave.
       40.47        1 rows  Butler St & 36th St
       40.46        1 rows  Penn Ave & N Fairmount St
       40.46        1 rows  Taylor St & Liberty Ave
       40.46        1 rows  Alder St & S Highland Ave
       40.46        1 rows  Smallman St & 31st St
       40.46        1 rows  Arch St & Jacksonia St
       40.46        1 rows  Penn Ave & N Atlantic Ave
       40.46        1 rows  Penn Ave & 39th St
       40.46        1 rows  Penn Ave & Putnam St (Bakery Square)
       40.46        1 rows  Liberty Ave & 37th St
       40.46        1 rows  S Winebiddle St & Penn Ave
       40.46        1 rows  Penn Ave & 29th St
       40.46        1 rows  S Negley Ave & Baum Blvd
       40.46        1 rows  Maryland Ave & Ellsworth Ave
       40.46        1 rows  Penn Ave & S Whitfield St
       40.46        1 rows  Federal St & E North Ave
       40.46        1 rows  33rd St & Penn Ave 

SRC_SHA256 by rows
        76  f1fe85c0eb81f11fc40ef4ad5cf8b604ada88d0bbbf4c65027eba3466b308460

SRC_SHA256 by dollars
        3.1K       76 rows  f1fe85c0eb81f11fc40ef4ad5cf8b604ada88d0bbbf4c65027eba3466b30

## who x when

STATION_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  10th St & Penn Ave                        2026:40.44
  12th St & Penn Ave                        2026:40.45
  14th St & Penn Ave                        2026:40.45
  24th St & Smallman St                     2026:40.45
  42nd & Penn Ave.                          2026:40.47
  42nd St & Butler St                       2026:40.47
  Alder St & S Highland Ave                 2026:40.46
  Arch St & Jacksonia St                    2026:40.46
  Beacon St & Murray Ave                    2026:40.44
  Boulevard of the Allies & Parkview Ave    2026:40.43
  Butler St & 36th St                       2026:40.47
  Butler St & Stanton Ave                   2026:40.48
  Eliza Furnace Trail at Swinburne St       2026:40.43
  Ellsworth Ave & N Neville St              2026:40.45
  Fifth Ave & S Bouquet St                  2026:40.44
  Hobart St & Wightman St                   2026:40.43
  Liberty Ave & 37th St                     2026:40.46
  Liberty Ave & Stanwix St                  2026:40.44
  Lytle St & Eliza St                       2026:40.41
  Penn Ave & 29th St                        2026:40.46
  Penn Ave & 39th St                        2026:40.46
  Penn Ave & N Atlantic Ave                 2026:40.46
  Penn Ave & N Fairmount St                 2026:40.46
  Penn Ave & Putnam St (Bakery Square)      2026:40.46
  Penn Ave & S Whitfield St                 2026:40.46
  S Bouquet Ave & Sennott St                2026:40.44
  S Winebiddle St & Penn Ave                2026:40.46
  Smallman St & 31st St                     2026:40.46
  Taylor St & Liberty Ave                   2026:40.46
  Zulema St & Coltart Ave                   2026:40.44

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  f1fe85c0eb81f11fc40ef4ad5cf8b604ada88d0b  2026:3.1K

## what

OF_RACKS: 19 18%, 6 17%, 5 15%, 8 11%, 15 11%, 10 7%, 7 4%, 13 4%, 12 3%, 16 3%, 18 3%, 17 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATION | other | 75 | 0 | 49951 1; 49941 1; 49921 1; 49881 1 |
| STATION_NAME | who | 76 | 0 | Butler St & 36th St 1; Allegheny Station 1; W General Robinson St & C 1; Arch St & Jacksonia St 1 |
| OF_RACKS | category | 17 | 0 | 19 13; 6 12; 5 11; 8 8 |
| LATITUDE | amount | 77 | 0 | 40.46529884 1; 40.44812685 1; 40.44741245 1; 40.45777261 1 |
| LONGITUDE | amount | 75 | 0 | -79.96527672 1; -80.01799822 1; -80.01206517 1; -80.00945807 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:40.35663 76 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4a199e22-5bf0-453e-b034-d 76 |
| SRC_SHA256 | who | 1 | 0 | f1fe85c0eb81f11fc40ef4ad5 76 |
