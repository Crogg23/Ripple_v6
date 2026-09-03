# PORTAL_CKA_SAN_JOSE_OPEN_DA_4218690BB6

rows 134  columns 26  scan 4.7s

roles: amount 2, audit 2, category 8, date 1, empty 3, other 7, who 4

## when

INGESTED_AT
  2026       134  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 134 | 6.13M | 6.16M | 6.20M | 6.20M | 825.82M |
| Y | 134 | 1.90M | 1.94M | 1.97M | 1.97M | 259.28M |

## who

COMMONNAME by rows
        23  Valley Oak
         9  California Sycamore
         8  Coast Live Oak
         8  Deodar Cedar
         6  California Pepper
         4  Chilien Wine Palm
         3  Southern Magnolia
         3  American Elm
         3  Cedars
         3  Mexican Fan Palm
         3  	California Sycamore
         2  Silver Maple
         2  Live Oak
         2  Bottle Tree
         2  London Plane
         2  Coast Redwood
         2  Pecan
         2  Monkey Puzzle Tree
         2  Canary Island Date Palm
         2  California Bay

COMMONNAME by dollars
     142.08M       23 rows  Valley Oak
      55.47M        9 rows  California Sycamore
      49.36M        8 rows  Deodar Cedar
      49.22M        8 rows  Coast Live Oak
      37.02M        6 rows  California Pepper
      24.62M        4 rows  Chilien Wine Palm
      18.48M        3 rows  	California Sycamore
      18.48M        3 rows  Cedars
      18.47M        3 rows  Mexican Fan Palm
      18.46M        3 rows  American Elm
      18.45M        3 rows  Southern Magnolia
      12.37M        2 rows  Monkey Puzzle Tree
      12.32M        2 rows  California Bay
      12.32M        2 rows  Live Oak
      12.32M        2 rows  Bottle Tree
      12.32M        2 rows  Pecan
      12.31M        2 rows  Bur Oak
      12.31M        2 rows  Silver Maple
      12.31M        2 rows  Canary Island Date Palm
      12.31M        2 rows  London Plane

SCIENTIFICNAME by rows
        23  Quercus lobata
        10  Platanus racemosa
        10  Quercus agrifolia
         9  Cedrus deodara
         8  Schinus molle
         4  Jubaea chilensis
         4  Magnolia grandiflora
         3  Washingtonia robusta
         3  Phoenix canariensis
         3  Ulmus americana
         3  Umbellularia californica
         2  Juglans californica
         2  Acer saccharinum
         2  Quercus macrocarpa
         2  	Platanus racemosa
         2  Ficus carica
         2  Brachychiton populneus
         2  Carya illinoinensis
         2  Sequoia sempervirens
         2  Platanus x hispanica

SCIENTIFICNAME by dollars
     142.09M       23 rows  Quercus lobata
      61.62M       10 rows  Platanus racemosa
      61.54M       10 rows  Quercus agrifolia
      55.47M        9 rows  Cedrus deodara
      49.33M        8 rows  Schinus molle
      24.62M        4 rows  Jubaea chilensis
      24.60M        4 rows  Magnolia grandiflora
      18.48M        3 rows  Umbellularia californica
      18.47M        3 rows  Washingtonia robusta
      18.47M        3 rows  Phoenix canariensis
      18.46M        3 rows  Ulmus americana
      12.33M        2 rows  	Platanus racemosa
      12.32M        2 rows  Brachychiton populneus
      12.32M        2 rows  Carya illinoinensis
      12.31M        2 rows  Quercus macrocarpa
      12.31M        2 rows  Acer saccharinum
      12.31M        2 rows  Platanus x hispanica
      12.31M        2 rows  Juglans californica
      12.30M        2 rows  Olea europaea
      12.30M        2 rows  Sequoia sempervirens

FACILITYID by rows
         1  60
         1  20
         1  74
         1  98
         1  72
         1  107
         1  112
         1  21
         1  55
         1  27
         1  49
         1  32
         1  89
         1  86
         1  31
         1  2
         1  104
         1  83
         1  56
         1  42

FACILITYID by dollars
       6.20M        1 rows  20
       6.20M        1 rows  21
       6.20M        1 rows  23
       6.20M        1 rows  127
       6.20M        1 rows  22
       6.19M        1 rows  41
       6.19M        1 rows  8
       6.19M        1 rows  5
       6.19M        1 rows  7
       6.19M        1 rows  6
       6.19M        1 rows  128
       6.19M        1 rows  4
       6.18M        1 rows  44
       6.18M        1 rows  3
       6.18M        1 rows  43
       6.18M        1 rows  42
       6.18M        1 rows  19
       6.18M        1 rows  10
       6.18M        1 rows  18
       6.18M        1 rows  17

SRC_SHA256 by rows
       134  1e0af932e7be363f8da42d10fd5c3cd0d215118105e3d08ea7db5d6a1872bf65

SRC_SHA256 by dollars
     825.82M      134 rows  1e0af932e7be363f8da42d10fd5c3cd0d215118105e3d08ea7db5d6a1872

## who x when

COMMONNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  	California Sycamore                      2026:18.48M
  American Elm                              2026:18.46M
  Bottle Tree                               2026:12.32M
  Bur Oak                                   2026:12.31M
  California Bay                            2026:12.32M
  California Pepper                         2026:37.02M
  California Sycamore                       2026:55.47M
  Canary Island Date Palm                   2026:12.31M
  Cedars                                    2026:18.48M
  Chilien Wine Palm                         2026:24.62M
  Coast Live Oak                            2026:49.22M
  Coast Redwood                             2026:12.30M
  Deodar Cedar                              2026:49.36M
  Live Oak                                  2026:12.32M
  London Plane                              2026:12.31M
  Mexican Fan Palm                          2026:18.47M
  Monkey Puzzle Tree                        2026:12.37M
  Pecan                                     2026:12.32M
  Silver Maple                              2026:12.31M
  Southern Magnolia                         2026:18.45M
  Valley Oak                                2026:142.08M

SCIENTIFICNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  	Platanus racemosa                        2026:12.33M
  Acer saccharinum                          2026:12.31M
  Brachychiton populneus                    2026:12.32M
  Carya illinoinensis                       2026:12.32M
  Cedrus deodara                            2026:55.47M
  Ficus carica                              2026:12.30M
  Jubaea chilensis                          2026:24.62M
  Juglans californica                       2026:12.31M
  Magnolia grandiflora                      2026:24.60M
  Olea europaea                             2026:12.30M
  Phoenix canariensis                       2026:18.47M
  Platanus racemosa                         2026:61.62M
  Platanus x hispanica                      2026:12.31M
  Quercus agrifolia                         2026:61.54M
  Quercus lobata                            2026:142.09M
  Quercus macrocarpa                        2026:12.31M
  Schinus molle                             2026:49.33M
  Sequoia sempervirens                      2026:12.30M
  Ulmus americana                           2026:18.46M
  Umbellularia californica                  2026:18.48M
  Washingtonia robusta                      2026:18.47M

## what

NUMBEROFTREESONSITE: 1 73%, 2 13%, 3 7%, 21 2%, 12 1%, 80 1%, 7 1%, 9 1%, 24 1%, 356 1%, 5 1%

DIAMETER: 48 26%, 36 10%, 30 10%, 50 10%, 54 9%, 42 9%, 52 7%, 44 6%, 72 6%, 60 5%, 34 4%

CIRCUMFERENCE: 151 28%, 113 11%, 132 9%, 164 9%, 157 9%, 226 8%, 170 8%, 94 6%, 138 6%, 201 3%, 75 3%

TREESTATUS: Wehner Mansion built 1890 24%, Gone 4/2020 12%, planted circa 1913 12%, Hayes Mansion site 12%, associated with original mansi 6%, Tree heavily damaged by fire a 6%, old vine on trellis that is an 6%, part of original neighborhood  6%, planted by John McLaren 6%, a remnant from the Overfelt Ra 6%, Planted in 1976 to commemorate 6%

HISTORY: large specimen 37%, unusual species 26%, very large specimen 9%, unusually large specimen 9%, both associated with historic  5%, exceptionally large specimen 2%, unusually large native specime 2%, largest specimen in San Jose
s 2%, unusual specimen 2%, unusual specimen and species 2%, large spreading specimen 2%

COUNCILDISTRICT: 6 37%, 10 21%, 3 15%, 8 8%, 2 7%, 4 4%, 7 4%, 9 1%, 1 1%, 5 1%

PHOTODATE: 2008/04/01 00:00:00+00 65%, 1995/08/01 00:00:00+00 25%, 1985/08/01 00:00:00+00 5%, 2020/02/01 00:00:00+00 2%, 2013/11/01 00:00:00+00 2%, 2020/04/30 02:31:00+00 1%

LASTUPDATE: 2019/06/05 23:25:05+00 66%, 2019/06/05 23:25:06+00 25%, 2022/02/10 23:40:03+00 4%, 2022/02/10 23:40:04+00 1%, 2020/04/30 18:30:53+00 1%, 2022/10/05 20:19:26+00 1%, 2020/04/30 18:31:10+00 1%, 2020/10/19 23:32:01+00 1%, 2020/10/19 23:29:13+00 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 136 | 0 | 6161088.593602 1; 6163661.62520133 1; 6147113.01558208 1; 6168704.63644075 1 |
| Y | amount | 131 | 0 | 1916006.07644181 1; 1901206.9606989 1; 1911579.57676464 1; 1916314.75266173 1 |
| OBJECTID | other | 134 | 0 | 268 1; 267 1; 266 1; 265 1 |
| FACILITYID | who | 133 | 0 | 134 1; 133 1; 132 1; 131 1 |
| INTID | other | 133 | 0 | 134 1; 133 1; 132 1; 131 1 |
| SALESFORCEID | empty | 1 | 134 |  |
| FILENUMBER | other | 134 | 0 | HT-10-016 1; HT-10-015 1; HT-10-014 1; HT-10-006 1 |
| COMMONNAME | who | 60 | 2 | Valley Oak 23; California Sycamore 9; Coast Live Oak 8; Deodar Cedar 8 |
| SCIENTIFICNAME | who | 55 | 0 | Quercus lobata 23; Quercus agrifolia 10; Platanus racemosa 10; Cedrus deodara 9 |
| ADDRESS | other | 113 | 0 | 1590 The Alameda 4; Prestwick Circle, Wehner  4; 800 Malone Road 3; 1616 Newport Avenue 2 |
| TREELOCATION | other | 63 | 32 | park strip 13; Garden Alameda 9; back yard 7; front yard 6 |
| NUMBEROFTREESONSITE | category | 14 | 5 | 1 93; 2 16; 3 9; 21 2 |
| DIAMETER | category | 35 | 15 | 48 21; 36 8; 30 8; 50 8 |
| CIRCUMFERENCE | category | 31 | 48 | 151 18; 113 7; 132 6; 164 6 |
| TREESTATUS | category | 18 | 111 | Wehner Mansion built 1890 4; Gone 4/2020 2; planted circa 1913 2; Hayes Mansion site 2 |
| HISTORY | category | 26 | 77 | large specimen 16; unusual species 11; very large specimen 4; unusually large specimen 4 |
| ASSOCIATEDAPN | other | 93 | 30 | 696-01-016 4; 439-26-059 3; 649-01-061 3; 665-58-083 3 |
| COUNCILDISTRICT | category | 10 | 0 | 6 49; 10 28; 3 20; 8 11 |
| PHOTODATE | category | 7 | 21 | 2008/04/01 00:00:00+00 74; 1995/08/01 00:00:00+00 28; 1985/08/01 00:00:00+00 6; 2020/02/01 00:00:00+00 2 |
| IMAGELINK | other | 116 | 21 | https://gis.sanjoseca.gov 1; https://gis.sanjoseca.gov 1; https://gis.sanjoseca.gov 1; https://gis.sanjoseca.gov 1 |
| CREATIONDATE | empty | 1 | 134 |  |
| LASTUPDATE | category | 9 | 0 | 2019/06/05 23:25:05+00 88; 2019/06/05 23:25:06+00 34; 2022/02/10 23:40:03+00 5; 2022/02/10 23:40:04+00 2 |
| NOTES | empty | 1 | 134 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:15:58.25138 134 |
| SOURCE_RUN_ID | audit | 1 | 0 | b03430d3-3c57-4b2b-b884-5 134 |
| SRC_SHA256 | who | 1 | 0 | 1e0af932e7be363f8da42d10f 134 |
