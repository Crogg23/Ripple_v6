# PORTAL_CKA_WPRDC_ALLEGHENY_5FE14C3854

rows 76  columns 8  scan 3.6s

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
         1  S 18th St & Sidney St
         1  Ridge Ave & Brighton Rd (CCAC)
         1  Penn Ave & 29th St
         1  Forbes Ave & Murray Ave
         1  Schenley Dr & Forbes Ave
         1  Third Ave & Wood St
         1  Penn Ave & Putnam St (Bakery Square)
         1  Smallman St & 31st St
         1  Beacon St & Murray Ave
         1  Zulema St & Coltart Ave
         1  Technology Dr & Bates St 
         1  W Station Square Dr & Bessemer Court
         1  Glasshouse
         1  Forbes Ave & Market Square
         1  42nd & Penn Ave.
         1  Ross St & Sixth Ave (Steel Plaza T Station)
         1  Hot Metal St & Tunnel Blvd
         1  Penn Ave & N Atlantic Ave
         1  Fifth Ave & S Bouquet St
         1  Fort Duquesne Blvd & 7th St

STATION_NAME by dollars
       40.48        1 rows  Butler St & Stanton Ave
       40.47        1 rows  42nd & Penn Ave.
       40.47        1 rows  42nd St & Butler St
       40.47        1 rows  Butler St & 36th St
       40.46        1 rows  Smallman St & 31st St
       40.46        1 rows  S Winebiddle St & Penn Ave
       40.46        1 rows  Burns White Center at 3 Crossings
       40.46        1 rows  Arch St & Jacksonia St
       40.46        1 rows  33rd St & Penn Ave 
       40.46        1 rows  S Negley Ave & Baum Blvd
       40.46        1 rows  Taylor St & Liberty Ave
       40.46        1 rows  Penn Ave & N Fairmount St
       40.46        1 rows  Alder St & S Highland Ave
       40.46        1 rows  Liberty Ave & Baum Blvd
       40.46        1 rows  Federal St & E North Ave
       40.46        1 rows  Penn Ave & Putnam St (Bakery Square)
       40.46        1 rows  Penn Ave & 39th St
       40.46        1 rows  Penn Ave & 29th St
       40.46        1 rows  Liberty Ave & S Millvale Ave (West Penn Hospital)
       40.46        1 rows  Liberty Ave & 37th St

SRC_SHA256 by rows
        76  f1fe85c0eb81f11fc40ef4ad5cf8b604ada88d0bbbf4c65027eba3466b308460

SRC_SHA256 by dollars
        3.1K       76 rows  f1fe85c0eb81f11fc40ef4ad5cf8b604ada88d0bbbf4c65027eba3466b30

## who x when

STATION_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  33rd St & Penn Ave                        2026:40.46
  42nd & Penn Ave.                          2026:40.47
  42nd St & Butler St                       2026:40.47
  Arch St & Jacksonia St                    2026:40.46
  Beacon St & Murray Ave                    2026:40.44
  Burns White Center at 3 Crossings         2026:40.46
  Butler St & 36th St                       2026:40.47
  Butler St & Stanton Ave                   2026:40.48
  Fifth Ave & S Bouquet St                  2026:40.44
  Forbes Ave & Market Square                2026:40.44
  Forbes Ave & Murray Ave                   2026:40.44
  Fort Duquesne Blvd & 7th St               2026:40.44
  Glasshouse                                2026:40.43
  Hot Metal St & Tunnel Blvd                2026:40.43
  Penn Ave & 29th St                        2026:40.46
  Penn Ave & N Atlantic Ave                 2026:40.46
  Penn Ave & N Fairmount St                 2026:40.46
  Penn Ave & Putnam St (Bakery Square)      2026:40.46
  Ridge Ave & Brighton Rd (CCAC)            2026:40.45
  Ross St & Sixth Ave (Steel Plaza T Stati  2026:40.44
  S 18th St & Sidney St                     2026:40.43
  S Negley Ave & Baum Blvd                  2026:40.46
  S Winebiddle St & Penn Ave                2026:40.46
  Schenley Dr & Forbes Ave                  2026:40.44
  Smallman St & 31st St                     2026:40.46
  Taylor St & Liberty Ave                   2026:40.46
  Technology Dr & Bates St                  2026:40.43
  Third Ave & Wood St                       2026:40.44
  W Station Square Dr & Bessemer Court      2026:40.43
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
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:34.45522 76 |
| SOURCE_RUN_ID | audit | 1 | 0 | 897910ed-69bb-4ab5-9cf0-0 76 |
| SRC_SHA256 | who | 1 | 0 | f1fe85c0eb81f11fc40ef4ad5 76 |
