# PORTAL_CKA_WESTERN_PENNSYLV_203EC904CD

rows 32  columns 22  scan 2.8s

roles: audit 2, category 16, date 1, other 3, who 1

## when

INGESTED_AT
  2026        32  ##############################

## who

SRC_SHA256 by rows
        32  d2b8669fad9f80eb874158f4dfa79c02394ad021e70ddc3c4764dcd50fd3f82a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  d2b8669fad9f80eb874158f4dfa79c02394ad021  2026:32

## what

OBJECTID: 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%

ADDRESS: 1395 Washington Blvd 8%, 2945 Railroad St 8%, 3284 Central Ave 8%, 1519 Orchlee St 8%, 159 Homestead St 8%, 2500 Allequippa St 8%, 605 Ross Ave 8%, 1401 Penn Ave. 8%, 259 McKee Place 8%, 4156 Winterburn St. 8%, 1729 Mary St. 8%, 4603 Stanton Ave. 8%

DISTRICT: 1 28%, 3 25%, 2 25%, 4 22%

FIREHOUS: 0 45%, 21 5%, 17 5%, 33 5%, 31 5%, 29 5%, 25 5%, 24 5%, 23 5%, 22 5%, 20 5%, 19 5%

FIREHOUS_I: 0 45%, 22 5%, 18 5%, 34 5%, 32 5%, 30 5%, 26 5%, 25 5%, 24 5%, 23 5%, 21 5%, 20 5%

LABEL: ACAD 8%, HQ/W 8%, T33 8%, E35 8%, E19 8%, E10 8%, E16 8%, E3 & MAC 8%, T14 8%, E12 8%, E24 & T24 8%, E7 8%

LABEL2: FA 8%, HQ 8%, 33 8%, 35 8%, 19 8%, 10 8%, 16 8%, 3 8%, 14 8%, 12 8%, 24 8%, 7 8%

NHOOD: Highland Park 8%, Strip District 8%, Marshall-Shadeland 8%, Brighton Heights 8%, Swisshelm Park 8%, West Oakland 8%, Wilkinsburg 8%, Strip 8%, Central Oakland 8%, Greenfield 8%, Southside Flats 8%, Stanton Heights 8%

NOTES: Pittsburgh Police & Fire TC 17%, Headquarters/ Warehouse 17%, BC4, 1729 Mary St, 488-8350 17%, BC3, 161 N Euclid,  665-3615 17%, BC5 @ 488-8353 17%, BC1 @ 323-7213 17%

PHONE: 422-6527 10%, 488-8348 10%, 782-7550 10%, 255-2290 10%, 622-6923 10%, 665-3616 10%, 665-3614 10%, 244-4182 10%, 422-6530 10%, 422-6529 10%

STATION: 0 15%, 33 8%, 35 8%, 19 8%, 10 8%, 16 8%, 3 8%, 14 8%, 12 8%, 24 8%, 7 8%, 4 8%

SYMBOL: 202 47%, 0 28%, 219 25%

TYPE: Engine 50%, Engine and Truck 28%, Quint 9%, Truck 6%, Fire Academy 3%, Headquarters/WareH 3%

X: E 59%, E & T 28%, T 6%, ACAD 3%, HQ/W 3%

ZIPCODE: 15212 17%, 15206 12%, 15201 12%, 15207 12%, 15213 8%, 15210 8%, 15220 8%, 15218 4%, 15221 4%, 15222 4%, 15203 4%, 15219 4%

GEOMETRY: POINT (592450.5644971772562712 8%, POINT (586911.0563133195973933 8%, POINT (582247.1091762114083394 8%, POINT (581455.6566275330260396 8%, POINT (593329.2538353920681402 8%, POINT (587548.8296348287258297 8%, POINT (594486.2085505271097645 8%, POINT (585667.5517729374114424 8%, POINT (588405.7042536599328741 8%, POINT (589914.1566838293801993 8%, POINT (586432.2508099233964458 8%, POINT (590072.4822448253398761 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 32 | 0 | 32 1; 31 1; 30 1; 29 1 |
| ADDRESS | category | 31 | 0 | 1395 Washington Blvd 1; 2945 Railroad St 1; 3284 Central Ave 1; 1519 Orchlee St 1 |
| AREA | other | 1 | 0 | 0 32 |
| DISTRICT | category | 4 | 0 | 1 9; 3 8; 2 8; 4 7 |
| FIREHOUS | category | 24 | 0 | 0 9; 21 1; 17 1; 33 1 |
| FIREHOUS_I | category | 24 | 0 | 0 9; 22 1; 18 1; 34 1 |
| LABEL | category | 32 | 0 | ACAD 1; HQ/W 1; T33 1; E35 1 |
| LABEL2 | category | 32 | 0 | FA 1; HQ 1; 33 1; 35 1 |
| NHOOD | category | 32 | 0 | Highland Park 1; Strip District 1; Marshall-Shadeland 1; Brighton Heights 1 |
| NOTES | category | 8 | 26 | Pittsburgh Police & Fire  1; Headquarters/ Warehouse 1; BC4, 1729 Mary St, 488-83 1; BC3, 161 N Euclid,  665-3 1 |
| PERIMETER | other | 1 | 0 | 0 32 |
| PHONE | category | 25 | 9 | 422-6527 1; 488-8348 1; 782-7550 1; 255-2290 1 |
| STATION | category | 31 | 0 | 0 2; 33 1; 35 1; 19 1 |
| SYMBOL | category | 3 | 0 | 202 15; 0 9; 219 8 |
| TYPE | category | 6 | 0 | Engine 16; Engine and Truck 9; Quint 3; Truck 2 |
| X | category | 5 | 0 | E 19; E & T 9; T 2; ACAD 1 |
| ZIPCODE | category | 20 | 0 | 15212 4; 15206 3; 15201 3; 15207 3 |
| ZONE | other | 1 | 0 | 0 32 |
| GEOMETRY | category | 32 | 0 | POINT (592450.56449717725 1; POINT (586911.05631331959 1; POINT (582247.10917621140 1; POINT (581455.65662753302 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:19:47.75719 32 |
| SOURCE_RUN_ID | audit | 1 | 0 | b658f056-3abb-4324-a7bb-b 32 |
| SRC_SHA256 | who | 1 | 0 | d2b8669fad9f80eb874158f4d 32 |
