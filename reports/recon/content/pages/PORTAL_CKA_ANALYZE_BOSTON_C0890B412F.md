# PORTAL_CKA_ANALYZE_BOSTON_C0890B412F

rows 35  columns 13  scan 2.5s

roles: amount 3, audit 2, category 7, date 1, who 1

## when

INGESTED_AT
  2026        35  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| OBJECTID_1 | 33 | 0 | 0 | 0 | 0 | 0 |
| POINT_X | 35 | -71.16 | -71.08 | -71.02 | -71.01 | -2.5K |
| POINT_Y | 35 | 42.26 | 42.33 | 42.39 | 42.39 | 1.5K |

## who

SRC_SHA256 by rows
        35  f2ef3a157e946004d60ef1908aa18406adb5e4aeaedec2e787139b895e6f39f6

SRC_SHA256 by dollars
       -2.5K       35 rows  f2ef3a157e946004d60ef1908aa18406adb5e4aeaedec2e787139b895e6f

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  f2ef3a157e946004d60ef1908aa18406adb5e4ae  2026:-2.5K

## what

SITE: BCYF Tobin Community Center 8%, Mattahunt 8%, Mason Pool* 8%, Grove Hall 8%, Clougherty Pool* 8%, Mirabella Pool* 8%, Jackson/Mann 8%, Ohrenberger 8%, Draper Pool* 8%, Roche 8%, Menino 8%, Flaherty Pool* 8%

PHONE: 635-5159 9%, 635-5241 9%, 635-1484 9%, 635-5174 9%, 635-1275 9%, 635-5153 9%, 635-5183 9%, 635-5021 9%, 635-5066 9%, 635-5256 9%, 635-5181 9%

FAX: --- 15%, 635-5079 15%, 635-5627 8%, 635-1485 8%, 635-5275 8%, 635-5283 8%, 635-5628 8%, 635-5067 8%, 635-5258 8%, 635-1225 8%, 635-5271 8%

STREET: 1481 Tremont St 8%, 100 Hebron St 8%, 159 Norfolk Ave. 8%, 51 Geneva Ave. 8%, Bunker Hill St. 8%, 475 Commercial St 8%, 500 Cambridge St. 8%, 175 W. Boundary R 8%, 5279 Washington S 8%, 1716 Centre St. 8%, 125 Brookway Rd. 8%, 160 Florence St. 8%

NEIGH: Roxbury 18%, Boston 12%, Mattapan 9%, Charlestown 9%, West Roxbury 9%, Roslindale 9%, Dorchester 9%, South Boston 9%, East Boston 9%, Mission Hill 3%, Allston 3%, Jamaica Plai 3%

ZIP: 2119.000000000000000 13%, 2126.000000000000000 10%, 2129.000000000000000 10%, 2132.000000000000000 10%, 2131.000000000000000 10%, 2127.000000000000000 10%, 2128.000000000000000 10%, 2118.000000000000000 7%, 2121.000000000000000 7%, 2113.000000000000000 7%, 2120.000000000000000 3%, 2134.000000000000000 3%

SHAPE_WKT: POINT (-71.098157242999946 42. 8%, POINT (-71.103569935999985 42. 8%, POINT (-71.070818557999985 42. 8%, POINT (-71.082323910999946 42. 8%, POINT (-71.067501163999964 42. 8%, POINT (-71.054309667999973 42. 8%, POINT (-71.137500770999964 42. 8%, POINT (-71.149466265999934 42. 8%, POINT (-71.159783226999934 42. 8%, POINT (-71.149306155999966 42. 8%, POINT (-71.120149128999969 42. 8%, POINT (-71.122208769999986 42. 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | amount | 2 | 2 | 0.000000000000000 33 |
| SITE | category | 35 | 0 | BCYF Tobin Community Cent 1; Mattahunt 1; Mason Pool* 1; Grove Hall 1 |
| PHONE | category | 35 | 1 | 635-5159 1; 635-5241 1; 635-1484 1; 635-5174 1 |
| FAX | category | 32 | 2 | --- 2; 635-5079 2; 635-5627 1; 635-1485 1 |
| STREET | category | 34 | 0 | 1481 Tremont St 1; 100 Hebron St 1; 159 Norfolk Ave. 1; 51 Geneva Ave. 1 |
| NEIGH | category | 13 | 0 | Roxbury 6; Boston 4; Mattapan 3; Charlestown 3 |
| ZIP | category | 17 | 0 | 2119.000000000000000 4; 2126.000000000000000 3; 2129.000000000000000 3; 2132.000000000000000 3 |
| SHAPE_WKT | category | 34 | 0 | POINT (-71.09815724299994 1; POINT (-71.10356993599998 1; POINT (-71.07081855799998 1; POINT (-71.08232391099994 1 |
| POINT_X | amount | 34 | 0 | -71.098157242999946 1; -71.103569935999985 1; -71.070818557999985 1; -71.082323910999946 1 |
| POINT_Y | amount | 35 | 0 | 42.332404606000068 1; 42.275811849000036 1; 42.325806577000037 1; 42.308854716000042 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:20:02.39178 35 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6d2bfc09-4ea6-4cec-8fa6-d 35 |
| SRC_SHA256 | who | 1 | 0 | f2ef3a157e946004d60ef1908 35 |
