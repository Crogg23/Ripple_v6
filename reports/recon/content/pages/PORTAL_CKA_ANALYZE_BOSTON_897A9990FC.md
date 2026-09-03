# PORTAL_CKA_ANALYZE_BOSTON_897A9990FC

rows 77  columns 17  scan 3.7s

roles: amount 4, audit 2, category 8, date 1, empty 1, who 2

## when

INGESTED_AT
  2026        77  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 77 | -71.10 | -71.07 | -71.04 | -71.04 | -5.5K |
| Y | 77 | 42.32 | 42.35 | 42.37 | 42.37 | 3.3K |
| POINT_X | 77 | -71.10 | -71.07 | -71.04 | -71.04 | -5.5K |
| POINT_Y | 77 | 42.32 | 42.35 | 42.37 | 42.37 | 3.3K |

## who

MANAGEMENT by rows
        77  City of Boston

MANAGEMENT by dollars
       -5.5K       77 rows  City of Boston

SRC_SHA256 by rows
        77  8c64bfaf03315e664b805cf82962730edf46c9dd8225a960835a6529b5dbe84f

SRC_SHA256 by dollars
       -5.5K       77 rows  8c64bfaf03315e664b805cf82962730edf46c9dd8225a960835a6529b5db

## who x when

MANAGEMENT by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  City of Boston                            2026:-5.5K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  8c64bfaf03315e664b805cf82962730edf46c9dd  2026:-5.5K

## what

DAY: Thursday 19%, Tuesday 18%, Wednesday 16%, Monday 16%, Friday 14%, Saturday 12%, Sunday 5%

TIME: Lunch 47%, Late Night 27%, Dinner 26%

TRUCK: Murl's Kitchen 13%, Aby's House 11%, Tacos Las Toxicas 11%, Extreme Flavor 11%, El Dugout 11%, Mr. Pacho Colombian Food Truck 11%, Frios Gourmet 7%, Moyeto Chimi 7%, Crepe Shop 5%, Bibim Box 5%, Stokes BBQ 4%, Bon Me 4%

LOCATION: MGH (Blossom & Emerson Streets 21%, Maverick Square (2 Sumner Stre 17%, District Hall 11%, Northeastern University (60 Op 11%, Boylston and Clarendon Streets 8%, Boston University (East Campus 7%, 310 Martin Luther King Jr. Bou 6%, Tufts Theater District (115 St 4%, 85 East Newton Street 4%, Milk & Kilby (71 Kilby St.) 4%, Summer Street 4%, MASCO Area (77 Avenue Louis Pa 3%

PINPOINT: Fenway-Kenmore 23%, West End 19%, East Boston 16%, Seaport 10%, Downtown 9%, Back Bay 8%, Roxbury 5%, Theater District 4%, South End 4%, South Boston 1%

HOURS: 11am-3pm 45%, 3pm-8pm 27%, 10pm-3am 26%, 10pn-3am 1%

LINK: https://murlskitchen.com/ 12%, https://www.abyshouse.com/ 10%, https://www.instagram.com/taco 10%, https://www.instagram.com/extr 10%, https://eldugoutrestaurant.com 10%, https://mrpachocolombianfoodtr 10%, https://friospops.com/ice-crea 7%, https://www.chick-fil-a.com/ 7%, https://www.instagram.com/moye 7%, https://munchiestation617.com/ 5%, https://www.instagram.com/crep 5%, https://www.bibimboxfood.com/ 5%

SHAPE_WKT: POINT (-71.068370899999934 42. 21%, POINT (-71.039866699999948 42. 17%, POINT (-71.045023899999933 42. 11%, POINT (-71.089166899999952 42. 11%, POINT (-71.075145599999985 42. 8%, POINT (-71.082467099999974 42. 6%, POINT (-71.066174099999955 42. 4%, POINT (-71.073034699999937 42. 4%, POINT (-71.055231599999956 42. 4%, POINT (-71.102314899999953 42. 4%, POINT (-71.102355499999987 42. 4%, POINT (-71.060278789999984 42. 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DAY | category | 7 | 0 | Thursday 15; Tuesday 14; Wednesday 12; Monday 12 |
| TIME | category | 3 | 0 | Lunch 36; Late Night 21; Dinner 20 |
| TRUCK | category | 25 | 0 | Murl's Kitchen 7; Aby's House 6; Tacos Las Toxicas 6; Extreme Flavor 6 |
| LOCATION | category | 17 | 0 | MGH (Blossom & Emerson St 15; Maverick Square (2 Sumner 12; District Hall 8; Northeastern University ( 8 |
| PINPOINT | category | 10 | 0 | Fenway-Kenmore 18; West End 15; East Boston 12; Seaport 8 |
| HOURS | category | 4 | 0 | 11am-3pm 35; 3pm-8pm 21; 10pm-3am 20; 10pn-3am 1 |
| MANAGEMENT | who | 1 | 0 | City of Boston 77 |
| NOTES | empty | 1 | 77 |  |
| LINK | category | 22 | 2 | https://murlskitchen.com/ 7; https://www.abyshouse.com 6; https://www.instagram.com 6; https://www.instagram.com 6 |
| X | amount | 16 | 0 | -71.068370900000005 15; -71.039866700000005 12; -71.045023900000004 8; -71.089166899999995 8 |
| Y | amount | 16 | 0 | 42.364052100000002 15; 42.368962099999997 15; 42.352619699999998 8; 42.340740699999998 8 |
| SHAPE_WKT | category | 17 | 0 | POINT (-71.06837089999993 15; POINT (-71.03986669999994 12; POINT (-71.04502389999993 8; POINT (-71.08916689999995 8 |
| POINT_X | amount | 16 | 0 | -71.068370899999934 15; -71.039866699999948 12; -71.045023899999933 8; -71.089166899999952 8 |
| POINT_Y | amount | 16 | 0 | 42.364052100000038 15; 42.368962100000033 15; 42.352619700000048 8; 42.340740700000026 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:45.78893 77 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5742fff4-0455-4363-8140-1 77 |
| SRC_SHA256 | who | 1 | 0 | 8c64bfaf03315e664b805cf82 77 |
