# PORTAL_CKA_WESTERN_PENNSYLV_FDE38758C9

rows 60  columns 8  scan 3.4s

roles: amount 3, audit 2, date 1, other 1, who 2

## when

INGESTED_AT
  2026        60  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_DOCKS | 60 | 11 | 19 | 24.64 | 27 | 1.1K |
| LATITUDE | 60 | 40.41 | 40.45 | 40.47 | 40.48 | 2.4K |
| LONGITUDE | 60 | -80.02 | -79.96 | -79.89 | -79.89 | -4.8K |

## who

NAME by rows
         1  Burns White Center at 3 Crossings
         1  10th St & Penn Ave
         1  Butler St & 36th St
         1  Bedford Ave & Memory Ln
         1  42nd St & Butler St
         1  Rosetta St & N Aiken Ave
         1  Penn Ave & Putnam St (Bakery Square)
         1  Centre Ave & Addison St
         1  Penn Ave & 7th St
         1  S Bouquet Ave & Sennott St
         1  Boulevard of the Allies & Parkview Ave
         1  Forbes Ave & Market Square
         1  N Braddock Ave & Hamilton Ave
         1  Hamilton Ave & Fifth Ave
         1  O'Hara St & University Place
         1  Eliza Furnace Trail & Swineburne St
         1  Centre Ave & S Millvale Ave
         1  Filmore St & S Bellefield Ave
         1  First Ave & B St
         1  Fifth Ave & S Bouquet St

NAME by dollars
          27        1 rows  Filmore St & S Bellefield Ave
          23        1 rows  S Bouquet Ave & Sennott St
          23        1 rows  Technology Dr & Bates St
          23        1 rows  Fifth Ave & S Bouquet St
          23        1 rows  North Shore Trail & Fort Duquesne Bridge
          23        1 rows  O'Hara St & University Place
          23        1 rows  Allequippa St & Darragh St
          23        1 rows  S 27th St & Sidney St. (Southside Works)
          23        1 rows  Boulevard of the Allies & Parkview Ave
          19        1 rows  Penn Ave & 7th St
          19        1 rows  21st St & Penn Ave
          19        1 rows  52nd St & Butler St
          19        1 rows  Centre Ave & S Millvale Ave
          19        1 rows  W Ohio St & Brighton Rd
          19        1 rows  Brighton Rd & Pennsylvania Ave
          19        1 rows  Penn Ave & Putnam St (Bakery Square)
          19        1 rows  Allegheny Station
          19        1 rows  17th St & Penn Ave
          19        1 rows  Bedford Ave & Memory Ln
          19        1 rows  Atwood St & Bates St

SRC_SHA256 by rows
        60  8c46aa97781b5d803e521f4c2babc091a26cab7bcc1129922732ca18a83b070a

SRC_SHA256 by dollars
        1.1K       60 rows  8c46aa97781b5d803e521f4c2babc091a26cab7bcc1129922732ca18a83b

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOCKS
  10th St & Penn Ave                        2026:15
  17th St & Penn Ave                        2026:19
  21st St & Penn Ave                        2026:19
  42nd St & Butler St                       2026:15
  52nd St & Butler St                       2026:19
  Allegheny Station                         2026:19
  Allequippa St & Darragh St                2026:23
  Bedford Ave & Memory Ln                   2026:19
  Boulevard of the Allies & Parkview Ave    2026:23
  Brighton Rd & Pennsylvania Ave            2026:19
  Burns White Center at 3 Crossings         2026:15
  Butler St & 36th St                       2026:15
  Centre Ave & Addison St                   2026:15
  Centre Ave & S Millvale Ave               2026:19
  Eliza Furnace Trail & Swineburne St       2026:15
  Fifth Ave & S Bouquet St                  2026:23
  Filmore St & S Bellefield Ave             2026:27
  First Ave & B St                          2026:15
  Forbes Ave & Market Square                2026:19
  Hamilton Ave & Fifth Ave                  2026:15
  N Braddock Ave & Hamilton Ave             2026:15
  North Shore Trail & Fort Duquesne Bridge  2026:23
  O'Hara St & University Place              2026:23
  Penn Ave & 7th St                         2026:19
  Penn Ave & Putnam St (Bakery Square)      2026:19
  Rosetta St & N Aiken Ave                  2026:15
  S 27th St & Sidney St. (Southside Works)  2026:23
  S Bouquet Ave & Sennott St                2026:23
  Technology Dr & Bates St                  2026:23
  W Ohio St & Brighton Rd                   2026:19

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOCKS
  8c46aa97781b5d803e521f4c2babc091a26cab7b  2026:1.1K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 60 | 0 | 60 1; 59 1; 58 1; 57 1 |
| NAME | who | 59 | 0 | Wilkinsburg Park & Ride 1; Forbes Ave at TCS Hall (C 1; W North Ave & Federal St 1; 52nd St & Butler St 1 |
| TOTAL_DOCKS | amount | 6 | 0 | 15 25; 19 24; 23 8; 18 1 |
| LATITUDE | amount | 59 | 0 | 40.446951 1; 40.444784 1; 40.455277 1; 40.480274 1 |
| LONGITUDE | amount | 60 | 0 | -79.888593 1; -79.947571 1; -80.006981 1; -79.954344 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:28:38.45101 60 |
| SOURCE_RUN_ID | audit | 1 | 0 | c937a339-e4c9-4227-a705-3 60 |
| SRC_SHA256 | who | 1 | 0 | 8c46aa97781b5d803e521f4c2 60 |
