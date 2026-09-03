# PORTAL_CKA_ANALYZE_BOSTON_97789AB639

rows 52  columns 21  scan 3.9s

roles: amount 2, audit 2, category 8, date 3, empty 2, other 3, who 2

## when

CREATIONDATE
  2017        50  ##############################
  2018         2  #

EDITDATE
  2017        31  ##############################
  2019        21  ####################

INGESTED_AT
  2026        52  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 52 | -71.16 | -71.08 | -71.04 | -71.04 | -3.7K |
| POINT_Y | 52 | 42.26 | 42.34 | 42.38 | 42.38 | 2.2K |

## who

NAME by rows
         1  Municipal Lot #032
         1  Municipal Lot #010
         1  Municipal Lot #004
         1  Greenhouse Parking Garage/Ultimate
         1  Municipal Lot #014
         1  Municipal Lot #021
         1  Municipal Lot #006
         1  Auditorium Garage
         1  Christian Science Garage
         1  Municipal Lot #022
         1  Municipal Lot #030
         1  The Prudential Center Garage
         1  Municipal Lot #034
         1  Municipal Lot #007
         1  Shipyard Garage/Mass General Hospital
         1  Harvard University/Soldiers Field Park Garage 
         1  Municipal Lot #012
         1  Municipal Lot #001
         1  Municipal Lot #015
         1  Municipal Lot #016

NAME by dollars
      -71.04        1 rows  Municipal Lot #026
      -71.04        1 rows  Municipal Lot #004
      -71.04        1 rows  Municipal Lot #021
      -71.04        1 rows  Municipal Lot #005
      -71.04        1 rows  BPDA/EDIC Garage
      -71.05        1 rows  Municipal Lot #018
      -71.05        1 rows  Shipyard Garage/Mass General Hospital
      -71.05        1 rows  Channel Center Garage
      -71.06        1 rows  Lafayette Garage
      -71.06        1 rows  Municipal Lot #020 


      -71.07        1 rows  200 Stuart Street Garage
      -71.07        1 rows  Municipal Lot #017
      -71.07        1 rows  Municipal Lot #016
      -71.07        1 rows  Municipal Lot #019
      -71.07        1 rows  Municipal Lot #031
      -71.07        1 rows  Municipal Lot #015
      -71.07        1 rows  Municipal Lot #022
      -71.07        1 rows  100 Clarendon Street Garage
      -71.07        1 rows  Motor Mart Garage
      -71.07        1 rows  Crosstown Center Garage

SRC_SHA256 by rows
        52  84d112667208559127315bb94ff93ed5f31ab4dea30c9ba2422394fa2ae323bb

SRC_SHA256 by dollars
       -3.7K       52 rows  84d112667208559127315bb94ff93ed5f31ab4dea30c9ba2422394fa2ae3

## who x when

NAME by CREATIONDATE, dollars = POINT_X
  200 Stuart Street Garage                  2018:-71.07
  Auditorium Garage                         2017:-71.09
  BPDA/EDIC Garage                          2017:-71.04
  Channel Center Garage                     2017:-71.05
  Christian Science Garage                  2017:-71.08
  Greenhouse Parking Garage/Ultimate        2017:-71.08
  Harvard University/Soldiers Field Park G  2017:-71.12
  Lafayette Garage                          2017:-71.06
  Municipal Lot #001                        2017:-71.08
  Municipal Lot #004                        2017:-71.04
  Municipal Lot #005                        2017:-71.04
  Municipal Lot #006                        2017:-71.12
  Municipal Lot #007                        2017:-71.11
  Municipal Lot #010                        2017:-71.15
  Municipal Lot #012                        2017:-71.12
  Municipal Lot #014                        2017:-71.10
  Municipal Lot #015                        2017:-71.07
  Municipal Lot #016                        2017:-71.07
  Municipal Lot #017                        2017:-71.07
  Municipal Lot #018                        2017:-71.05
  Municipal Lot #019                        2017:-71.07
  Municipal Lot #020 

                     2017:-71.06
  Municipal Lot #021                        2017:-71.04
  Municipal Lot #022                        2017:-71.07
  Municipal Lot #026                        2017:-71.04
  Municipal Lot #030                        2017:-71.08
  Municipal Lot #032                        2017:-71.11
  Municipal Lot #034                        2017:-71.16
  Shipyard Garage/Mass General Hospital     2017:-71.05
  The Prudential Center Garage              2017:-71.08

SRC_SHA256 by CREATIONDATE, dollars = POINT_X
  84d112667208559127315bb94ff93ed5f31ab4de  2017:-3.6K 2018:-142.14

## what

OBJECTID_1: 53 9%, 52 9%, 51 9%, 48 9%, 47 9%, 46 9%, 45 9%, 41 9%, 40 9%, 38 9%, 37 9%

SPACES: 18 15%, 12 10%, 40 10%, 24 10%, 35 10%, 22 10%, 42 10%, 60 10%, 28 5%, 25 5%, 72 5%

FEE: No Charge 63%, $10 for each 24-hour period 8%, $15 for each 24-hour period 8%, $14 for each 24-hour period 6%, You pay 50% of the variable ra 4%, $10 for 24 hour period 2%, $0 for duration of Snow Emerge 2%, $12 for each 24-hour period 2%, FULL 2%, $10/24 hrs 2%, $1 for each night 2%

COMMENTS: Discounted parking is for Roxb 17%, Discounted parking for all Bos 8%, Bay Village resident parking p 8%, You must show proof of your Bo 8%, Discounted parking for Fenway/ 8%, Discounted parking for all Cit 8%, Stop by the garage office on t 8%, Due to construction, spaces ar 8%, Due to construction, emergency 8%, There are a limited amount of  8%, Discount only for Back Bay, Be 8%

PHONE: 617-269-1830 10%, 617-275-0151 10%, 857-293-8577 10%, 617-948-2060 10%, 617-236-3060 10%, 617-247-0588 10%, 617-247-8006 10%, 617-266-7260 10%, 617-267-9677 10%, 617-482-2487 10%

MAXSPACES: 0 100%

CREATOR: BostonGIS 92%, 143525_boston 8%

EDITOR: BostonGIS 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 47 | 6 | 53 1; 52 1; 51 1; 48 1 |
| SPACES | category | 24 | 20 | 18 3; 12 2; 40 2; 24 2 |
| FEE | category | 11 | 0 | No Charge 33; $10 for each 24-hour peri 4; $15 for each 24-hour peri 4; $14 for each 24-hour peri 3 |
| COMMENTS | category | 21 | 32 | Discounted parking is for 2; Discounted parking for al 1; Bay Village resident park 1; You must show proof of yo 1 |
| PHONE | category | 14 | 40 | 617-269-1830 1; 617-275-0151 1; 857-293-8577 1; 617-948-2060 1 |
| NAME | who | 52 | 0 | Motor Mart Garage 1; 200 Stuart Street Garage 1; Crosstown Center Garage 1; Van Ness Garage 1 |
| ADDRESS | other | 51 | 0 | 201 Stuart Street 1; 200 Stuart Street 1; 7 Melnea Cass Boulevard 1; 1335 Boylston Street 1 |
| NEIGHBORHO | empty | 2 | 52 |  |
| MAXSPACES | category | 2 | 6 | 0 46 |
| HOURS | empty | 2 | 52 |  |
| GLOBALID | other | 52 | 0 | {BE87E0F0-D77D-44B6-999F- 1; {C5AC0BC0-7CC5-403D-94AD- 1; {8843EA6C-EFF0-4C6E-8018- 1; {D2225FA8-9F8D-44BD-A961- 1 |
| CREATIONDATE | date | 7 | 0 | 12/4/2017 17:09:20.712 46; 3/12/2018 19:05:06.649 1; 1/3/2018 18:48:56.162 1; 12/8/2017 21:25:51.310 1 |
| CREATOR | category | 3 | 1 | BostonGIS 47; 143525_boston 4 |
| EDITDATE | date | 25 | 0 | 12/4/2017 17:09:20.712 28; 1/15/2019 20:00:22.654 1; 1/15/2019 19:53:03.778 1; 1/15/2019 16:46:48.417 1 |
| EDITOR | category | 2 | 3 | BostonGIS 49 |
| SHAPE_WKT | other | 52 | 0 | POINT (-71.06804550599997 1; POINT (-71.06757782499994 1; POINT (-71.07377716699994 1; POINT (-71.09972392499997 1 |
| POINT_X | amount | 52 | 0 | -71.068045505999976 1; -71.067577824999944 1; -71.073777166999946 1; -71.099723924999978 1 |
| POINT_Y | amount | 52 | 0 | 42.351030695000077 1; 42.350433727000052 1; 42.332227293000074 1; 42.344218320000039 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:27:51.55109 52 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9375bf29-26d1-48cc-a3ea-2 52 |
| SRC_SHA256 | who | 1 | 0 | 84d112667208559127315bb94 52 |
