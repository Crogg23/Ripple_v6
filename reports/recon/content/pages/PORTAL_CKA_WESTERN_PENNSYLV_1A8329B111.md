# PORTAL_CKA_WESTERN_PENNSYLV_1A8329B111

rows 10.0K  columns 10  scan 3.5s

roles: audit 2, category 1, date 1, empty 1, id 2, other 2, who 2

## when

INGESTED_AT
  2026     10.0K  ##############################

## who

TYPE by rows
      2.0K  Other Commercial
       672  Restaurant
       515  Fire Department
       386  Doctors Office
       303  Professional Agency
       276  Gas Station
       272  Auto Repair
       268  Retail
       248  Municipal Government Facility
       235  Place of Worship
       229  Salon-Spa
       229  Home Maintenance
       228  Office Park-Building
       213  Police Department
       207  Apartment - Condo Complex
       201  Cafe
       187  Bank-Financial
       184  Elementary School
       182  Grocery Store
       180  Bar

SRC_SHA256 by rows
     10.0K  4c5f545145bd88f01d344ce15e534d6fcbdd4d0a71c21c2a93bf309fc2f6f883

## who x when

TYPE by INGESTED_AT  LOAD STAMP, not an event date
  Apartment - Condo Complex                 2026:207
  Auto Repair                               2026:272
  Bank-Financial                            2026:187
  Bar                                       2026:180
  Cafe                                      2026:201
  Doctors Office                            2026:386
  Elementary School                         2026:184
  Fire Department                           2026:515
  Gas Station                               2026:276
  Grocery Store                             2026:182
  Home Maintenance                          2026:229
  Municipal Government Facility             2026:248
  Office Park-Building                      2026:228
  Other Commercial                          2026:2.0K
  Place of Worship                          2026:235
  Police Department                         2026:213
  Professional Agency                       2026:303
  Restaurant                                2026:672
  Retail                                    2026:268
  Salon-Spa                                 2026:229

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  4c5f545145bd88f01d344ce15e534d6fcbdd4d0a  2026:10.0K

## what

CLASS: 0 63%, 6 9%, 2 9%, 7 6%, 1 6%, 3 3%, 9 2%, 4 1%, 8 0%, 5 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.1K | 0 | 120547 50; 120546 50; 120544 50; 120542 50 |
| ADDRESS_ID | other | 7.6K | 0 | 129242 55; 488406 54; 342782 53; 433032 51 |
| LANDMARK | other | 8.6K | 0 | GET GO 65; FIRST COMMONWEALTH BANK 65; EAT N PARK 65; FIRST NATIONAL BANK 62 |
| GLOBALID | id | 10.0K | 0 | {97C277DB-3627-40A5-B1F4- 50; {400426DE-5E3C-408B-BA50- 50; {DE67C9A9-C34F-4D70-8404- 50; {91180631-60E6-4B57-8DFB- 50 |
| CLASS | category | 10 | 0 | 0 6.3K; 6 948; 2 871; 7 649 |
| TYPE | who | 119 | 0 | Other Commercial 2.0K; Restaurant 672; Fire Department 515; Doctors Office 386 |
| PUB | empty | 1 | 10.0K |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:47:53.70276 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9849fdb7-e6ef-4ba1-b5b2-c 10.0K |
| SRC_SHA256 | who | 1 | 0 | 4c5f545145bd88f01d344ce15 10.0K |
