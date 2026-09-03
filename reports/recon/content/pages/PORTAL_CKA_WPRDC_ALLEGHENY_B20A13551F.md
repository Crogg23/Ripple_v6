# PORTAL_CKA_WPRDC_ALLEGHENY_B20A13551F

rows 91  columns 25  scan 3.9s

roles: amount 3, audit 2, category 8, date 1, empty 1, other 10, who 1

## when

INGESTED_AT
  2026        91  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 91 | 89.04 | 96.38 | 100 | 100 | 8.8K |
| X | 91 | -79.84 | 1.36M | 1.42M | 1.42M | 121.91M |
| Y | 91 | 40.43 | 409.0K | 481.7K | 484.0K | 37.05M |

## who

SRC_SHA256 by rows
        91  cdd870ab0b4a1e2b0c23e9db0b4d0dfaffbe91171826a31d1b5b81ad2b12494e

SRC_SHA256 by dollars
        8.8K       91 rows  cdd870ab0b4a1e2b0c23e9db0b4d0dfaffbe91171826a31d1b5b81ad2b12

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  cdd870ab0b4a1e2b0c23e9db0b4d0dfaffbe9117  2026:8.8K

## what

ARC_ZIP: 15122 14%, 15237 12%, 15146 9%, 15108 9%, 15137 7%, 15238 7%, 15235 7%, 15132 7%, 15205 7%, 15102 7%, 15217 7%, 15212 7%

ADDR_TYPE: StreetAddress 86%, Address 14%

LOC_NAME: DW_Addressing_ 99%, TANA_Streets 1%

MUNICIPA_1: Pittsburgh 61%, West Mifflin 8%, Monroeville 5%, North Versailles 4%, Bethel Park 4%, Natrona Heights 3%, Homestead 3%, Mckeesport 3%, Coraopolis 3%, Verona 3%, Mckees Rocks 3%, Tarentum 1%

NAME: Giant Eagle 43%, Shop N Save 24%, Wal Mart 7%, Target 7%, Kuhn's 7%, Sav-A-Lot 3%, Community Market 2%, Shur Save 1%, Shop N Save Village 1%, Save A Lot 1%, Pittsburgh Commissary 1%, Murray Avenue Kosher 1%

SIDE: L 69%, R 31%

STATUS: M 95%, T 5%

ZIPCODES: 15122 14%, 15237 12%, 15146 9%, 15108 9%, 15137 7%, 15238 7%, 15235 7%, 15132 7%, 15205 7%, 15102 7%, 15217 7%, 15212 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ARC_CITY | other | 76 | 0 | North Versailles 3; Brentwood 3; Moon Twp. 3; West Mifflin 2 |
| ARC_STATE | empty | 1 | 91 |  |
| ARC_STREET | other | 92 | 0 | 2351 Century Drive 1; 2010 Village Center Drive 1; 100 Wal Mart Drive 1; 250 Summit Park Drive 1 |
| ARC_ZIP | category | 49 | 0 | 15122 6; 15237 5; 15146 4; 15108 4 |
| ADDR_TYPE | category | 2 | 0 | StreetAddress 78; Address 13 |
| ADDRESS | other | 92 | 0 | 2351 Century Drive 1; 2010 Village Center Drive 1; 100 Wal Mart Drive 1; 250 Summit Park Drive 1 |
| LOC_NAME | category | 2 | 0 | DW_Addressing_ 90; TANA_Streets 1 |
| MATCH_ADDR | other | 91 | 0 | 2351 CENTURY DR, WEST MIF 1; 2010 VILLAGE CENTER DR, F 1; 100 WALMART DR, NORTH VER 1; 250 SUMMIT PARK DR, NORTH 1 |
| MATCH_TYPE | other | 1 | 0 | A 91 |
| MUNICIPA_1 | category | 28 | 0 | Pittsburgh 46; West Mifflin 6; Monroeville 4; North Versailles 3 |
| MUNICIPALI | other | 76 | 0 | North Versailles 3; Brentwood 3; Moon Twp. 3; West Mifflin 2 |
| NAME | category | 17 | 0 | Giant Eagle 37; Shop N Save 21; Wal Mart 6; Target 6 |
| OBJECTID | other | 90 | 0 | 99 1; 98 1; 97 1; 96 1 |
| REF_ID | other | 92 | 0 | 3153451 1; 2890876 1; 3159029 1; 2774136 1 |
| SCORE | amount | 47 | 0 | 100.0 28; 98.91 8; 94.29 3; 95.19 3 |
| SIDE | category | 3 | 78 | L 9; R 4 |
| STATUS | category | 2 | 0 | M 86; T 5 |
| USER_FLD | other | 1 | 0 | 0 91 |
| X | amount | 92 | 0 | 1356258.029024 1; 1397842.298009 1; 1390728.790335 1; 1293324.401022 1 |
| Y | amount | 91 | 0 | 375202.329683 1; 454987.000052 1; 390581.344765 1; 415075.49997 1 |
| ZIPCODES | category | 49 | 0 | 15122 6; 15237 5; 15146 4; 15108 4 |
| GEOMETRY | other | 90 | 0 | POINT (589465.44257032207 1; POINT (601234.04175799060 1; POINT (599790.09184814547 1; POINT (569854.71819760988 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:31:06.36220 91 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9d621b53-ca13-4082-bc08-5 91 |
| SRC_SHA256 | who | 1 | 0 | cdd870ab0b4a1e2b0c23e9db0 91 |
