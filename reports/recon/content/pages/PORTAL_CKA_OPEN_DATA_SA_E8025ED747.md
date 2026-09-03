# PORTAL_CKA_OPEN_DATA_SA_E8025ED747

rows 166  columns 13  scan 3.7s

roles: amount 2, audit 2, category 3, date 1, other 4, who 2

## when

INGESTED_AT
  2026       166  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_INJURIES | 166 | 2 | 3 | 13.35 | 15 | 650 |
| SHAPE__LENGTH | 166 | 30.05 | 1.9K | 10.5K | 13.3K | 478.8K |

## who

STREETNAME by rows
         8  Military Loop 13
         5  COMMERCE
         4  Nacogdoches FM 2252
         4  Perrin Beitel FM 2252
         4  Blanco FM 2696
         4  ZARZAMORA
         3  Zarzamora
         3  Commerce
         3  Roosevelt Spur 536
         3  Bandera Spur 421
         3  Potranco FM 1957
         3  Fredericksburg
         2  Pleasanton
         2  San Pedro
         2  Roosevelt US 281
         2  FLORES
         2  RITTIMAN
         2  FREDERICKSBURG Spur 345
         2  WURZBACH
         2  Marbach

STREETNAME by dollars
          27        3 rows  Zarzamora
          25        8 rows  Military Loop 13
          20        4 rows  ZARZAMORA
          20        5 rows  COMMERCE
          19        3 rows  Bandera Spur 421
          19        4 rows  Perrin Beitel FM 2252
          17        3 rows  Commerce
          17        2 rows  GENERAL MC MULLEN
          15        1 rows  Fredericksburg Spur 345
          15        2 rows  Austin Hwy Loop 368
          15        2 rows  Culebra
          14        1 rows  Culebra Spur 421
          13        2 rows  CULEBRA
          13        1 rows  CULEBRA Spur 421
          12        3 rows  Fredericksburg
          12        1 rows  General McMullen
          12        2 rows  San Pedro
          12        4 rows  Nacogdoches FM 2252
          11        2 rows  Flores
          11        2 rows  FREDERICKSBURG

SRC_SHA256 by rows
       166  31b1698a0b360e68a0ded3177f5a94f7be379e60faa42b3ddeadaa24f5c1d47c

SRC_SHA256 by dollars
         650      166 rows  31b1698a0b360e68a0ded3177f5a94f7be379e60faa42b3ddeadaa24f5c1

## who x when

STREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_INJURIES
  Austin Hwy Loop 368                       2026:15
  Bandera Spur 421                          2026:19
  Blanco FM 2696                            2026:11
  COMMERCE                                  2026:20
  CULEBRA                                   2026:13
  CULEBRA Spur 421                          2026:13
  Commerce                                  2026:17
  Culebra                                   2026:15
  Culebra Spur 421                          2026:14
  FLORES                                    2026:10
  FREDERICKSBURG                            2026:11
  FREDERICKSBURG Spur 345                   2026:11
  Flores                                    2026:11
  Fredericksburg                            2026:12
  Fredericksburg Spur 345                   2026:15
  GENERAL MC MULLEN                         2026:17
  General McMullen                          2026:12
  Marbach                                   2026:4
  Military Loop 13                          2026:25
  Nacogdoches FM 2252                       2026:12
  Perrin Beitel FM 2252                     2026:19
  Pleasanton                                2026:8
  Potranco FM 1957                          2026:8
  RITTIMAN                                  2026:6
  Roosevelt Spur 536                        2026:8
  Roosevelt US 281                          2026:5
  San Pedro                                 2026:12
  WURZBACH                                  2026:11
  ZARZAMORA                                 2026:20
  Zarzamora                                 2026:27

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_INJURIES
  31b1698a0b360e68a0ded3177f5a94f7be379e60  2026:650

## what

INCAPACITATED_INJURIES: 2 36%, 1 24%, 3 15%, 5 6%, 4 5%, 0 5%, 6 4%, 7 3%, 10 1%, 9 1%, 11 1%, 8 1%

FATAL_INJURIES: 1 36%, 0 34%, 2 14%, 3 8%, 4 4%, 5 3%, 6 1%, 8 1%

SPIA_YEAR: 2020 54%, 2017 46%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 166 | 0 | 166 1; 165 1; 164 1; 163 1 |
| CORRIDORID | other | 168 | 0 | 156 1; 30 1; 26 1; 153 1 |
| STREETNAME | who | 103 | 0 | Military Loop 13 8; COMMERCE 5; Perrin Beitel FM 2252 4; Nacogdoches FM 2252 4 |
| FROMSTREET | other | 161 | 0 | Loop 410 3; GARDINA 2; RAYBON 2; Jerry 1 |
| TOSTREET | other | 163 | 0 | Military 4; Breeden 1; CESAR CHAVEZ 1; LAKERIDGE 1 |
| INCAPACITATED_INJURIES | category | 13 | 0 | 2 60; 1 39; 3 25; 5 10 |
| FATAL_INJURIES | category | 8 | 0 | 1 59; 0 57; 2 23; 3 13 |
| TOTAL_INJURIES | amount | 14 | 0 | 2 73; 3 37; 4 12; 5 11 |
| SPIA_YEAR | category | 2 | 0 | 2020 90; 2017 76 |
| SHAPE__LENGTH | amount | 167 | 0 | 3925.67096910453 1; 8118.31541922557 1; 1476.39833154736 1; 115.211726049929 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:36:12.38772 166 |
| SOURCE_RUN_ID | audit | 1 | 0 | dccbd699-b266-47be-9a47-3 166 |
| SRC_SHA256 | who | 1 | 0 | 31b1698a0b360e68a0ded3177 166 |
