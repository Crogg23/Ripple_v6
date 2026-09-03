# PORTAL_CKA_WESTERN_PENNSYLV_B26184ED51

rows 602  columns 8  scan 2.9s

roles: audit 2, date 1, other 2, who 4

## when

INGESTED_AT
  2026       602  ##############################

## who

LAST_NAME by rows
        10  MILLER
         6  SMITH
         5  POREMSKI
         4  MEYERS
         3  BOYD
         3  NAVARI
         3  KIGER
         3  THOMAS
         3  CARUSO
         3  MERTZ
         3  MASCILLI
         3  REDINGER
         3  WILLIAMS
         3  ZIMMERMAN
         3  KICINSKI
         2  BROWN
         2  CERRA
         2  CHAMBERS
         2  HALL
         2  BITSURA

FIRST_NAME by rows
        31  ROBERT
        27  JOHN
        22  WILLIAM
        21  MICHAEL
        21  DAVID
        18  THOMAS
        17  JAMES
        16  RICHARD
        15  JOSEPH
        13  MARK
        12  ANTHONY
        10  KEVIN
         9  RONALD
         9  SCOTT
         9  MATTHEW
         9  TIMOTHY
         9  CHRISTOPHER
         8  EDWARD
         8  JEFFREY
         8  DANIEL

CITY by rows
       189  PITTSBURGH
        14  BETHEL PARK
        14  MCKEESPORT
        11  CORAOPOLIS
        11  GIBSONIA
        10  ELIZABETH
        10  MUNHALL
        10  CARNEGIE
         9  NEW KENSINGTON
         9  CANONSBURG
         9  FINLEYVILLE
         9  JEFFERSON HILLS
         8  MURRYSVILLE
         8  ALIQUIPPA
         8  SEWICKLEY
         8  VERONA
         8  OAKDALE
         8  IRWIN
         8  APOLLO
         7  SOUTH PARK

SRC_SHA256 by rows
       602  0e88233bef65efc63ad777c08a2bd62e77ce6ddd6889745a9ef4b39d4ed2eb9f

## who x when

LAST_NAME by INGESTED_AT  LOAD STAMP, not an event date
  BITSURA                                   2026:2
  BOYD                                      2026:3
  BROWN                                     2026:2
  CARUSO                                    2026:3
  CERRA                                     2026:2
  CHAMBERS                                  2026:2
  HALL                                      2026:2
  KICINSKI                                  2026:3
  KIGER                                     2026:3
  MASCILLI                                  2026:3
  MERTZ                                     2026:3
  MEYERS                                    2026:4
  MILLER                                    2026:10
  NAVARI                                    2026:3
  POREMSKI                                  2026:5
  REDINGER                                  2026:3
  SMITH                                     2026:6
  THOMAS                                    2026:3
  WILLIAMS                                  2026:3
  ZIMMERMAN                                 2026:3

FIRST_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ANTHONY                                   2026:12
  CHRISTOPHER                               2026:9
  DANIEL                                    2026:8
  DAVID                                     2026:21
  EDWARD                                    2026:8
  JAMES                                     2026:17
  JEFFREY                                   2026:8
  JOHN                                      2026:27
  JOSEPH                                    2026:15
  KEVIN                                     2026:10
  MARK                                      2026:13
  MATTHEW                                   2026:9
  MICHAEL                                   2026:21
  RICHARD                                   2026:16
  ROBERT                                    2026:31
  RONALD                                    2026:9
  SCOTT                                     2026:9
  THOMAS                                    2026:18
  TIMOTHY                                   2026:9
  WILLIAM                                   2026:22

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REGISTRATION_NUMBER | other | 602 | 0 | 02846 4; 03414 4; 04966 3; 04588 3 |
| FIRST_NAME | who | 181 | 0 | ROBERT 31; JOHN 27; WILLIAM 22; MICHAEL 21 |
| LAST_NAME | who | 497 | 0 | MILLER 10; SMITH 6; POREMSKI 6; WILLIAMS 4 |
| CITY | who | 135 | 2 | PITTSBURGH 189; MCKEESPORT 14; BETHEL PARK 14; GIBSONIA 11 |
| ZIP_CODE | other | 150 | 2 | 15227 19; 15237 16; 15236 16; 15642 14 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:44:26.93180 602 |
| SOURCE_RUN_ID | audit | 1 | 0 | 09a1749a-f0c7-4c53-bf8c-1 602 |
| SRC_SHA256 | who | 1 | 0 | 0e88233bef65efc63ad777c08 602 |
