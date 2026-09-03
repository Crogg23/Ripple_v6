# PORTAL_CKA_OPEN_DATA_SA_8B475B44A2

rows 83  columns 7  scan 3.4s

roles: amount 2, audit 2, date 1, other 1, who 2

## when

INGESTED_AT
  2026        83  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 83 | 2.06M | 2.12M | 2.17M | 2.17M | 176.02M |
| Y | 83 | 13.64M | 13.72M | 13.77M | 13.77M | 1.14B |

## who

NAME by rows
         1  Terra Oak_Culebra/Helotes Creek Greenway
         1  Grissom Trailhead
         1  Lower MLL Baseball Complex (McAllister)
         1  Old Applewhite Trailhead
         1  Hardberger Park (Walker Ranch)
         1  Mission Trail Trailhead/Parking (Mission Pkwy)
         1  Mission Trail Trailhead/Parking (VFW Blvd)
         1  Briar Glen Trailhead
         1  Alazan Creek Trailhead
         1  Loop 1604 Trailhead
         1  Mattox Park Trailhead (Medina River Greenway)
         1  Bamberger
         1  Mario Farias/Parking
         1  Medina River Greenway (Hwy 16)
         1  Wilshire Connection Trailhead
         1  Buddy Clak (Leon Greenway)
         1  Voelcker Homestead Trailhead
         1  Ingram Transit Center Trailhead
         1  Salado Creek Greenway-South Side Lions Park
         1  Cathedral Rock Trailhead Parking

NAME by dollars
       2.17M        1 rows  Comanche Lookout (Nacogdoches Rd)
       2.17M        1 rows  Comanche Lookout (Judson Rd)
       2.16M        1 rows  Wurzbach Parkway Trailhead
       2.16M        1 rows  Briar Glen Trailhead
       2.15M        1 rows  Salado Creek Greenway-Rittiman Rd
       2.15M        1 rows  Salado Creek Greenway-Martin Luther King Par
       2.15M        1 rows  Comanche County Trailhead
       2.15M        1 rows  Wilshire Connection Trailhead
       2.15M        1 rows  Pletz County Trailhead
       2.15M        1 rows  Oakwell Trailhead
       2.15M        1 rows  Salado Creek Greenway-Jack White Park
       2.15M        1 rows  Salado Creek Greenway-Commanche Park
       2.15M        1 rows  Salado Creek Greenway-South Side Lions Park
       2.15M        1 rows  Salado Creek Trlailhead (Lady Bird Johnson)
       2.15M        1 rows  Salado Creek Greenway Tobin Park Trailhead
       2.15M        1 rows  Laurens Lane Trailhead Salado Creek Greenway
       2.15M        1 rows  Salado Creek Greenway-J St Park
       2.15M        1 rows  Willow Springs Trailhead
       2.15M        1 rows  Corporate Wood_Gold Canyon Park
       2.14M        1 rows  Salado Creek near Dog Park (McAllister)

SRC_SHA256 by rows
        83  21e9b39f59d2870a7bb45b56018a2005a650166ce3b65543f77eaafa269f8565

SRC_SHA256 by dollars
     176.02M       83 rows  21e9b39f59d2870a7bb45b56018a2005a650166ce3b65543f77eaafa269f

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Alazan Creek Trailhead                    2026:2.12M
  Bamberger                                 2026:2.09M
  Briar Glen Trailhead                      2026:2.16M
  Buddy Clak (Leon Greenway)                2026:2.09M
  Cathedral Rock Trailhead Parking          2026:2.08M
  Comanche County Trailhead                 2026:2.15M
  Comanche Lookout (Judson Rd)              2026:2.17M
  Comanche Lookout (Nacogdoches Rd)         2026:2.17M
  Grissom Trailhead                         2026:2.09M
  Hardberger Park (Walker Ranch)            2026:2.13M
  Ingram Transit Center Trailhead           2026:2.09M
  Loop 1604 Trailhead                       2026:2.11M
  Lower MLL Baseball Complex (McAllister)   2026:2.14M
  Mario Farias/Parking                      2026:2.12M
  Mattox Park Trailhead (Medina River Gree  2026:2.14M
  Medina River Greenway (Hwy 16)            2026:2.10M
  Mission Trail Trailhead/Parking (Mission  2026:2.14M
  Mission Trail Trailhead/Parking (VFW Blv  2026:2.14M
  Oakwell Trailhead                         2026:2.15M
  Old Applewhite Trailhead                  2026:2.11M
  Pletz County Trailhead                    2026:2.15M
  Salado Creek Greenway-Commanche Park      2026:2.15M
  Salado Creek Greenway-Jack White Park     2026:2.15M
  Salado Creek Greenway-Martin Luther King  2026:2.15M
  Salado Creek Greenway-Rittiman Rd         2026:2.15M
  Salado Creek Greenway-South Side Lions P  2026:2.15M
  Terra Oak_Culebra/Helotes Creek Greenway  2026:2.07M
  Voelcker Homestead Trailhead              2026:2.12M
  Wilshire Connection Trailhead             2026:2.15M
  Wurzbach Parkway Trailhead                2026:2.16M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  21e9b39f59d2870a7bb45b56018a2005a650166c  2026:176.02M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 83 | 0 | 83 1; 82 1; 81 1; 80 1 |
| NAME | who | 83 | 0 | Lower MLL Baseball Comple 1; Old Applewhite Trailhead 1; Ingram Transit Center Tra 1; Prue Road Trailhead 1 |
| X | amount | 81 | 0 | 2143443.51283789 1; 2112792.33693564 1; 2087409.06519572 1; 2085042.32583472 1 |
| Y | amount | 83 | 0 | 13751108.0350276 1; 13636408.0669214 1; 13716773.9704937 1; 13744859.7666842 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:14:37.31897 83 |
| SOURCE_RUN_ID | audit | 1 | 0 | 78aa7a90-691d-45fb-bb88-1 83 |
| SRC_SHA256 | who | 1 | 0 | 21e9b39f59d2870a7bb45b560 83 |
