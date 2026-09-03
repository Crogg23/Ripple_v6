# PORTAL_CKA_OPEN_DATA_SA_2F8287A9CB

rows 1.4K  columns 15  scan 2.8s

roles: amount 1, audit 2, category 6, date 1, empty 2, id 2, who 2

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__LENGTH | 1.4K | 9.08 | 4.2K | 23.7K | 36.2K | 7.38M |

## who

STREETNAME by rows
        41  EAST & WEST CONNECTOR
        18  S ST MARY'S
        17  NORTH & SOUTH CONNECTOR
        17  CULEBRA RD
        17  GOLIAD RD
        16  BLANCO RD
        16  FREDERICKSBURG RD
        16  ZARZAMORA ST
        15  NACOGDOCHES RD
        15  BABCOCK RD
        15  SOMERSET RD
        15  McCULLOUGH AVE
        14  HUEBNER RD
        14  PLEASANTON RD
        13  FM 78
        13  BULVERDE RD
        13  CESAR CHAVEZ BLVD
        13  BANDERA RD
        12  WURZBACH PARKWAY
        12  W COMMERCE ST

STREETNAME by dollars
      312.7K       41 rows  EAST & WEST CONNECTOR
      150.0K       17 rows  NORTH & SOUTH CONNECTOR
      113.4K       16 rows  BLANCO RD
       90.3K       14 rows  PLEASANTON RD
       89.1K       15 rows  BABCOCK RD
       87.0K       17 rows  CULEBRA RD
       86.5K       15 rows  NACOGDOCHES RD
       84.1K        9 rows  FM 1518
       84.0K       13 rows  FM 78
       83.6K        8 rows  FM 3009
       81.4K        9 rows  South Texas Parkway
       79.0K        6 rows  FM 1346
       78.9K       15 rows  SOMERSET RD
       74.8K       14 rows  HUEBNER RD
       73.6K       12 rows  W MILITARY DR
       71.8K       10 rows  EVANS RD
       71.6K        4 rows  WILDERNESS OAK
       68.9K       13 rows  BULVERDE RD
       68.4K       11 rows  MARBACH RD
       68.0K       11 rows  FM 1516

SRC_SHA256 by rows
      1.4K  e9c70cadf79b3d6fa5e411be1bcdc28a2147c6733b64e26344ce684801408ffe

SRC_SHA256 by dollars
       7.38M     1.4K rows  e9c70cadf79b3d6fa5e411be1bcdc28a2147c6733b64e26344ce68480140

## who x when

STREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  BABCOCK RD                                2026:89.1K
  BANDERA RD                                2026:64.0K
  BLANCO RD                                 2026:113.4K
  BULVERDE RD                               2026:68.9K
  CESAR CHAVEZ BLVD                         2026:7.4K
  CULEBRA RD                                2026:87.0K
  EAST & WEST CONNECTOR                     2026:312.7K
  EVANS RD                                  2026:71.8K
  FM 1346                                   2026:79.0K
  FM 1516                                   2026:68.0K
  FM 1518                                   2026:84.1K
  FM 3009                                   2026:83.6K
  FM 78                                     2026:84.0K
  FREDERICKSBURG RD                         2026:47.6K
  GOLIAD RD                                 2026:23.8K
  HUEBNER RD                                2026:74.8K
  MARBACH RD                                2026:68.4K
  McCULLOUGH AVE                            2026:35.0K
  NACOGDOCHES RD                            2026:86.5K
  NORTH & SOUTH CONNECTOR                   2026:150.0K
  PLEASANTON RD                             2026:90.3K
  S ST MARY'S                               2026:16.5K
  SOMERSET RD                               2026:78.9K
  South Texas Parkway                       2026:81.4K
  W COMMERCE ST                             2026:42.3K
  W MILITARY DR                             2026:73.6K
  WILDERNESS OAK                            2026:71.6K
  WURZBACH PARKWAY                          2026:62.4K
  ZARZAMORA ST                              2026:61.8K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__LENGTH
  e9c70cadf79b3d6fa5e411be1bcdc28a2147c673  2026:7.38M

## what

COLOR: GREY 47%, GREEN 23%, RED 16%, BLUE 4%, PURPLE 3%, YELLOW 3%, ORANGE 1%, PINK 1%, BLACK 1%, BROWN 1%, GREY'' 0%, GREY  0%

CURRENTROW: 86' 57%, 120' 16%, 70' - 86' 16%, 70' - 120' 4%, 120'-142' 3%, 200'-250' 3%, 250'-500' 1%, 86 0%

CHANGECODE: D 40%, 1 20%, P 20%, E 10%, X 10%

TYPE: Secondary Arterial Type A 47%, Secondary Arterial Type B 23%, Primary Arterial Type A 16%, Primary Arterial Type B 4%, Enhanced Secondary Arterial 3%, Arterial Type C 3%, Super Arterial Type A 1%, Super Arterial Type B 1%, Freeway 1%, Rural Roadway 1%

DOWNTOWN: Yes 100%

ORDINANCE: 0 97%, 201806140457 0%, 201702230120 0%, 201401160033 0%, 201303210198 0%, 201010070877 0%, 200911190944 0%, 202105200373 0%, 201110060832 0%, 202105200374 0%, 202106030405 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.4K | 0 | 1405 8; 1404 8; 1403 8; 1402 8 |
| STREETNAME | who | 299 | 0 | EAST & WEST CONNECTOR 41; GOLIAD RD 18; S ST MARY'S 18; CULEBRA RD 17 |
| COLOR | category | 12 | 0 | GREY 655; GREEN 328; RED 222; BLUE 50 |
| CURRENTROW | category | 8 | 0 | 86' 798; 120' 230; 70' - 86' 228; 70' - 120' 50 |
| PROPROW | empty | 2 | 1.4K |  |
| CHANGECODE | category | 7 | 1.4K | D 4; 1 2; P 2; E 1 |
| TYPE | category | 10 | 0 | Secondary Arterial Type A 660; Secondary Arterial Type B 328; Primary Arterial Type A 223; Primary Arterial Type B 50 |
| STREETNAME1 | empty | 1 | 1.4K |  |
| DOWNTOWN | category | 3 | 1.2K | Yes 245 |
| ORDINANCE | category | 23 | 2 | 0 1.4K; 201806140457 5; 201702230120 5; 201401160033 4 |
| GLOBALID | id | 1.4K | 0 | c1318a23-ac96-465e-ae85-f 8; 01adca2b-4340-4e7d-bdbd-9 8; d1bfc4e4-ce51-428c-9ff1-e 8; 06796634-d061-427e-a0da-7 8 |
| SHAPE__LENGTH | amount | 1.4K | 0 | 3428.20130419002 8; 6226.64036133615 8; 257.884894117773 8; 335.254360338085 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:54:05.97505 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 092987d1-3261-4e05-a88a-e 1.4K |
| SRC_SHA256 | who | 1 | 0 | e9c70cadf79b3d6fa5e411be1 1.4K |
