# PORTAL_CKA_ANALYZE_BOSTON_38EB48CA38

rows 736  columns 7  scan 3.0s

roles: amount 1, audit 2, category 1, date 1, other 1, who 2

## when

INGESTED_AT
  2026       736  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 736 | 0 | 0 | 0.05 | 0.10 | 4.05 |

## who

FULL_NAME by rows
        55  Centre St
        24  Bennington St
        22  Columbus Ave
        20  Washington St
        19  Huntington Ave
        19  Cambridge St
        18  American Legion Hwy
        12  Tremont St
        12  Commonwealth Ave
        12  Jewish War Veterans Dr
        11  Hancock St
        10  Hyde Park Ave
        10  Cummins Hwy
        10  Morton St
        10  Gallivan Blvd
        10  Old Colony Ave
        10  Blue Hill Ave
         9  Nashua St
         9  Harrison Ave
         9  Neponset Ave

FULL_NAME by dollars
        0.20       12 rows  Commonwealth Ave
        0.18       20 rows  Washington St
        0.10       10 rows  Blue Hill Ave
        0.10        4 rows  Dorchester Ave
        0.10       55 rows  Centre St
        0.09       10 rows  Hyde Park Ave
        0.09        3 rows  River St
        0.09       19 rows  Cambridge St
        0.09        8 rows  Columbia Rd
        0.08       19 rows  Huntington Ave
        0.08        7 rows  Beacon St
        0.08       18 rows  American Legion Hwy
        0.08       12 rows  Tremont St
        0.06       22 rows  Columbus Ave
        0.06        6 rows  Massachusetts Ave
        0.06       24 rows  Bennington St
        0.06        5 rows  New Rutherford Ave
        0.05        5 rows  Adams St
        0.05       12 rows  Jewish War Veterans Dr
        0.05        5 rows  Congress St

SRC_SHA256 by rows
       736  545a3f94ea83912ae4b59342096f42a017855031e1aeef7e522cb0c129f44a9b

SRC_SHA256 by dollars
        4.05      736 rows  545a3f94ea83912ae4b59342096f42a017855031e1aeef7e522cb0c129f4

## who x when

FULL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Adams St                                  2026:0.05
  American Legion Hwy                       2026:0.08
  Beacon St                                 2026:0.08
  Bennington St                             2026:0.06
  Blue Hill Ave                             2026:0.10
  Cambridge St                              2026:0.09
  Centre St                                 2026:0.10
  Columbia Rd                               2026:0.09
  Columbus Ave                              2026:0.06
  Commonwealth Ave                          2026:0.20
  Congress St                               2026:0.05
  Cummins Hwy                               2026:0.05
  Dorchester Ave                            2026:0.10
  Gallivan Blvd                             2026:0.05
  Hancock St                                2026:0.01
  Harrison Ave                              2026:0.02
  Huntington Ave                            2026:0.08
  Hyde Park Ave                             2026:0.09
  Jewish War Veterans Dr                    2026:0.05
  Massachusetts Ave                         2026:0.06
  Morton St                                 2026:0.04
  Nashua St                                 2026:0
  Neponset Ave                              2026:0.02
  New Rutherford Ave                        2026:0.06
  Old Colony Ave                            2026:0.03
  River St                                  2026:0.09
  Tremont St                                2026:0.08
  Washington St                             2026:0.18

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  545a3f94ea83912ae4b59342096f42a017855031  2026:4.05

## what

RESPONSIBILITY: City 93%, State 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FULL_NAME | who | 215 | 4 | Centre St 55; Bennington St 24; Columbus Ave 22; Washington St 20 |
| RESPONSIBILITY | category | 2 | 0 | City 684; State 52 |
| SHAPE_LENGTH | amount | 729 | 0 | 0.013400310147893 4; 0.000753536070494 4; 0.000764437210728 4; 0.045126650317358 4 |
| SHAPE_WKT | other | 356 | 381 | MULTILINESTRING ((-71.050 2; MULTILINESTRING ((-71.051 2; MULTILINESTRING ((-71.085 2; MULTILINESTRING ((-71.146 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:46:06.09443 736 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5ef18e9e-cdfb-4710-9fb1-1 736 |
| SRC_SHA256 | who | 1 | 0 | 545a3f94ea83912ae4b593420 736 |
