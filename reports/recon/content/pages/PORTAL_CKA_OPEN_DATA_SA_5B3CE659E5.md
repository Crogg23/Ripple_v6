# PORTAL_CKA_OPEN_DATA_SA_5B3CE659E5

rows 108  columns 17  scan 2.6s

roles: amount 2, audit 2, category 5, date 1, other 6, who 2

## when

INGESTED_AT
  2026       108  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 108 | -98.69 | -98.50 | -98.39 | -98.36 | -10.6K |
| Y | 108 | 29.27 | 29.43 | 29.64 | 29.65 | 3.2K |

## who

NAME by rows
         1  Central
         1  K
         1  Applicant Processing ^
         1  FS35
         1  FS44
         1  FS53
         1  FS54
         1  Fire Prevention
         1  AIR
         1  FCO
         1  FS31
         1  72P
         1  FS04
         1  Bomb Squad 
         1  FS50
         1  Prue
         1  Property Room ^
         1  Fire Education
         1  FS26
         1  FS51

NAME by dollars
      -98.36        1 rows  FS54
      -98.39        1 rows  FS40
      -98.39        1 rows  FS38
      -98.40        1 rows  FS20
      -98.40        1 rows  Fire Education
      -98.40        1 rows  FS53
      -98.41        1 rows  FS24
      -98.41        1 rows  FS18
      -98.42        1 rows  FS30
      -98.42        1 rows  FS39
      -98.42        1 rows  FS48
      -98.43        1 rows  East
      -98.43        1 rows  SAPD Association Office ^
      -98.44        1 rows  RAU
      -98.44        1 rows  K
      -98.44        1 rows  TAC5
      -98.44        1 rows  EOC
      -98.44        1 rows  EXPD
      -98.44        1 rows  Bomb Squad 
      -98.44        1 rows  Emergency Operations CTN ^

SRC_SHA256 by rows
       108  3d9fa5a9e9100cdabdcc4ab7bc8cd6902fe7d0c4bcbc79b2ade36cfbb28db5f3

SRC_SHA256 by dollars
      -10.6K      108 rows  3d9fa5a9e9100cdabdcc4ab7bc8cd6902fe7d0c4bcbc79b2ade36cfbb28d

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  72P                                       2026:-98.58
  AIR                                       2026:-98.49
  Applicant Processing ^                    2026:-98.53
  Bomb Squad                                2026:-98.44
  Central                                   2026:-98.50
  East                                      2026:-98.43
  FCO                                       2026:-98.50
  FS04                                      2026:-98.48
  FS18                                      2026:-98.41
  FS20                                      2026:-98.40
  FS24                                      2026:-98.41
  FS26                                      2026:-98.59
  FS30                                      2026:-98.42
  FS31                                      2026:-98.51
  FS35                                      2026:-98.63
  FS38                                      2026:-98.39
  FS39                                      2026:-98.42
  FS40                                      2026:-98.39
  FS44                                      2026:-98.66
  FS48                                      2026:-98.42
  FS50                                      2026:-98.55
  FS51                                      2026:-98.59
  FS53                                      2026:-98.40
  FS54                                      2026:-98.36
  Fire Education                            2026:-98.40
  Fire Prevention                           2026:-98.50
  K                                         2026:-98.44
  Property Room ^                           2026:-98.53
  Prue                                      2026:-98.58
  SAPD Association Office ^                 2026:-98.43

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  3d9fa5a9e9100cdabdcc4ab7bc8cd6902fe7d0c4  2026:-10.6K

## what

CITY: SAN ANTONIO 96%, SAN ANTONIO (BE) 3%, BROOKS CITY BASE 1%

ZIP: 78216 17%, 78207 15%, 78235 13%, 78229 10%, 78240 8%, 78204 7%, 78219 5%, 78227 5%, 78214 5%, 78217 5%, 78201 5%, 78221 5%

AGENCYID: 4 63%, 2 37%

AGENCYTYPE: FIRE 63%, POLICE 37%

FACILITYTYPE: FIRE STATION 51%, FIRE OTHER 10%, POLICE UNIT/POST 8%, POLICE AUX CHANNELS 7%, POLICE SUBSTATION 6%, AIRPORT OTHER 5%, POLICE OTHER FACILITY 5%, PUBLIC SAFETY OTHER 3%, POLICE STOREFRONT 3%, POLICE COMMUNICATIONS 1%, PUBLIC SAFETY HEADQUARTERS 1%, POLICE TRAINING ACADEMY 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 107 | 0 | 108 1; 107 1; 106 1; 105 1 |
| ID | other | 104 | 0 | 0 3; 88 1; 94 1; 33 1 |
| NAME | who | 106 | 0 | FS24 1; FS30 1; FS54 1;  Communications 1 |
| ADDRESS | other | 88 | 0 | 5020 PRUE RD 4; 8039 CHALLENGER DR 4; 7461 CALLAGHAN RD 4; 9800 AIRPORT BLVD 3 |
| CITY | category | 3 | 0 | SAN ANTONIO 104; SAN ANTONIO (BE) 3; BROOKS CITY BASE 1 |
| STATE | other | 1 | 0 | TX 108 |
| ZIP | category | 43 | 0 | 78216 10; 78207 9; 78235 8; 78229 6 |
| LAT | other | 96 | 0 | 29.340833 4; 29.504241 4; 29.526889 3; 29.543325 3 |
| LON | other | 97 | 0 | -98.443056 4; -98.559734 4; -98.472608 3; -98.583636 3 |
| AGENCYID | category | 2 | 0 | 4 68; 2 40 |
| AGENCYTYPE | category | 2 | 0 | FIRE 68; POLICE 40 |
| FACILITYTYPE | category | 14 | 0 | FIRE STATION 54; FIRE OTHER 11; POLICE UNIT/POST 9; POLICE AUX CHANNELS 7 |
| X | amount | 96 | 0 | -98.443056 4; -98.559734 4; -98.472608 3; -98.583636 3 |
| Y | amount | 96 | 0 | 29.340833 4; 29.504241 4; 29.526889 3; 29.543325 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:32:20.27220 108 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9e649a98-94b5-463e-9307-6 108 |
| SRC_SHA256 | who | 1 | 0 | 3d9fa5a9e9100cdabdcc4ab7b 108 |
