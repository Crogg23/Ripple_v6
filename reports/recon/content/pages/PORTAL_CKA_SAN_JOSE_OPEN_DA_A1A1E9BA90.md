# PORTAL_CKA_SAN_JOSE_OPEN_DA_A1A1E9BA90

rows 45  columns 18  scan 5.8s

roles: amount 2, audit 2, category 8, date 1, empty 1, other 1, who 4

## when

INGESTED_AT
  2026        45  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 45 | 544.07 | 5.0K | 58.3K | 69.7K | 469.4K |
| SHAPE_AREA | 45 | 17.2K | 1.07M | 112.85M | 155.24M | 341.88M |

## who

STATUS by rows
        45  Effective

STATUS by dollars
      469.4K       45 rows  Effective

DFIRMID by rows
        45  06085C

DFIRMID by dollars
      469.4K       45 rows  06085C

LASTUPDATE by rows
        45  2021/12/22 00:00:00+00

LASTUPDATE by dollars
      469.4K       45 rows  2021/12/22 00:00:00+00

SRC_SHA256 by rows
        45  91632a065800936b7de38eab7ccb98630cb2cb83eb0fa07bb15c16afe80bec4e

SRC_SHA256 by dollars
      469.4K       45 rows  91632a065800936b7de38eab7ccb98630cb2cb83eb0fa07bb15c16afe80b

## who x when

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Effective                                 2026:469.4K

DFIRMID by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  06085C                                    2026:469.4K

## what

OBJECTID: 86 8%, 85 8%, 84 8%, 83 8%, 82 8%, 81 8%, 80 8%, 79 8%, 78 8%, 77 8%, 76 8%, 75 8%

FACILITYID: 45 8%, 44 8%, 43 8%, 42 8%, 41 8%, 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%

VERSIONID: 1.1.1.0 84%, 2.1.3.0 16%

LOMRID: 06085C_45 8%, 06085C_44 8%, 06085C_43 8%, 06085C_42 8%, 06085C_41 8%, 06085C_40 8%, 06085C_39 8%, 06085C_38 8%, 06085C_37 8%, 06085C_36 8%, 06085C_35 8%, 06085C_34 8%

EFFDATE: 2010/12/17 00:00:00+00 25%, 2010/02/25 00:00:00+00 15%, 2010/11/23 00:00:00+00 15%, 2021/11/26 00:00:00+00 5%, 2021/09/16 00:00:00+00 5%, 2020/11/18 00:00:00+00 5%, 2020/06/01 00:00:00+00 5%, 2019/12/19 00:00:00+00 5%, 2019/12/03 00:00:00+00 5%, 2019/10/10 00:00:00+00 5%, 2019/03/07 00:00:00+00 5%, 2018/10/09 00:00:00+00 5%

CASENO: 11-09-0419P 25%, 09-09-0375P 15%, 11-09-0246P 15%, 20-09-1371P 5%, 20-09-1627P 5%, 20-09-0849P 5%, 19-09-1592P 5%, 19-09-0759P 5%, 19-09-1253P 5%, 18-09-2460P 5%, 18-09-1360P 5%, 17-09-0578P 5%

SCALE: 6000 96%, 12000 4%

SOURCECIT: 06085C_LOMC34 26%, 06085C_LOMC33 16%, 06085C_LOMC25 11%, 06085C_LOMC69 5%, 06085C_LOMC68 5%, 06085C_LOMC67 5%, 06085C_LOMC66 5%, 06085C_LOMC65 5%, 06085C_LOMC64 5%, 06085C_LOMC63 5%, 06085C_LOMC62 5%, 06085C_LOMC61 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 44 | 0 | 86 1; 85 1; 84 1; 83 1 |
| FACILITYID | category | 45 | 0 | 45 1; 44 1; 43 1; 42 1 |
| DFIRMID | who | 1 | 0 | 06085C 45 |
| VERSIONID | category | 2 | 0 | 1.1.1.0 38; 2.1.3.0 7 |
| LOMRID | category | 45 | 0 | 06085C_45 1; 06085C_44 1; 06085C_43 1; 06085C_42 1 |
| EFFDATE | category | 37 | 0 | 2010/12/17 00:00:00+00 5; 2010/02/25 00:00:00+00 3; 2010/11/23 00:00:00+00 3; 2021/11/26 00:00:00+00 1 |
| CASENO | category | 37 | 0 | 11-09-0419P 5; 09-09-0375P 3; 11-09-0246P 3; 20-09-1371P 1 |
| SCALE | category | 2 | 0 | 6000 43; 12000 2 |
| STATUS | who | 1 | 0 | Effective 45 |
| SOURCECIT | category | 38 | 0 | 06085C_LOMC34 5; 06085C_LOMC33 3; 06085C_LOMC25 2; 06085C_LOMC69 1 |
| AGENCY | other | 1 | 0 | FEMA 45 |
| LASTUPDATE | who | 1 | 0 | 2021/12/22 00:00:00+00 45 |
| NOTES | empty | 1 | 45 |  |
| SHAPE_LENGTH | amount | 44 | 0 | 69663.1484682162 1; 10515.7022333634 1; 7097.64821587745 1; 6396.0389659344 1 |
| SHAPE_AREA | amount | 44 | 0 | 155236934.785217 1; 5649310.24959471 1; 2320717.83398438 1; 2178223.37015334 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:21:47.44986 45 |
| SOURCE_RUN_ID | audit | 1 | 0 | dc2187a5-ad66-44ec-ad23-7 45 |
| SRC_SHA256 | who | 1 | 0 | 91632a065800936b7de38eab7 45 |
