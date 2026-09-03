# PORTAL_CKA_HOUSTON_OPEN_DAT_9A02A5CFC0

rows 587  columns 9  scan 3.6s

roles: audit 2, category 1, date 3, other 2, who 2

## when

PER_EFFECTIVE_START_DATE
  2014       437  ##############################
  2015       150  ##########

PER_EFFECTIVE_END_DATE
  2015       437  ##############################
  2016       149  ##########
  2017         1  

INGESTED_AT
  2026       587  ##############################

## who

ENT_DISPLAY_NAME by rows
        27  Prostar Services
        21  COMCAST CABLE OF HOUSTON
        18  AT&T
        13  IRON MOUNTAIN
        13  PEPSI BEVERAGES CO
        13  PAPPAS RESTAURANT INC
         9  JOBS BLDG SERVICES INC
         8  Harris County Facilities & Property MGT
         7  ARAMARK REFRESHMENTS
         7  ADMIRAL LINEN SERVICE INC
         7  CANTEEN VENDING
         7  Treebeards Inc.
         7  MCCOY INC
         6  COPY SOURCE 1 LTD
         6  HOUSTON DISTRIBUTING COMPANY
         5  BEN E KEITH
         5  SPEC'S LIQUOR
         5  ST JOSEPH MEDICAL CENTER
         5  MACH 5 COURIERS
         5  FED EX

SRC_SHA256 by rows
       587  764de9ad3102f585840202050261919c56784f9f79b95c9c026b382d75a9ab75

## who x when

ENT_DISPLAY_NAME by PER_EFFECTIVE_END_DATE
  ADMIRAL LINEN SERVICE INC                 2015:7
  ARAMARK REFRESHMENTS                      2015:7
  AT&T                                      2015:18
  BEN E KEITH                               2015:5
  CANTEEN VENDING                           2015:6 2016:1
  COMCAST CABLE OF HOUSTON                  2015:21
  COPY SOURCE 1 LTD                         2015:6
  FED EX                                    2016:5
  HOUSTON DISTRIBUTING COMPANY              2015:6
  Harris County Facilities & Property MGT   2015:8
  IRON MOUNTAIN                             2015:11 2016:2
  JOBS BLDG SERVICES INC                    2015:9
  MACH 5 COURIERS                           2015:3 2016:2
  MCCOY INC                                 2016:7
  PAPPAS RESTAURANT INC                     2015:9 2016:4
  PEPSI BEVERAGES CO                        2015:8 2016:5
  Prostar Services                          2015:27
  SPEC'S LIQUOR                             2015:5
  ST JOSEPH MEDICAL CENTER                  2015:5
  Treebeards Inc.                           2015:6 2016:1

SRC_SHA256 by PER_EFFECTIVE_END_DATE
  764de9ad3102f585840202050261919c56784f9f  2015:437 2016:149 2017:1

## what

PEC_NAME: Class B 50%, Class C 35%, Class A 14%, REPLACEMENT CVLZ A 1%, REPLACEMENT CVLZ C 0%, REPLACEMENT CVLZ B 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PER_UID | other | 592 | 0 | 9557074 3; 9557073 3; 9557072 3; 9557071 3 |
| PER_EFFECTIVE_START_DATE | date | 209 | 0 | 2014-05-07 00:00:00 34; 2014-08-01 00:00:00 24; 2014-05-28 00:00:00 12; 2014-07-17 00:00:00 10 |
| PER_EFFECTIVE_END_DATE | date | 210 | 0 | 2015-05-07 23:59:59 34; 2015-08-01 23:59:59 24; 2015-05-28 23:59:59 12; 2015-07-17 23:59:59 10 |
| PER_NUMBER | other | 579 | 0 | CVLZC0480 3; CVLZC0479 3; CVLZC0478 3; CVLZC0477 3 |
| ENT_DISPLAY_NAME | who | 288 | 0 | Prostar Services 27; COMCAST CABLE OF HOUSTON 21; AT&T 18; IRON MOUNTAIN 13 |
| PEC_NAME | category | 6 | 0 | Class B 291; Class C 205; Class A 85; REPLACEMENT CVLZ A 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:22:12.26014 587 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1036f447-5c71-48eb-9569-8 587 |
| SRC_SHA256 | who | 1 | 0 | 764de9ad3102f585840202050 587 |
