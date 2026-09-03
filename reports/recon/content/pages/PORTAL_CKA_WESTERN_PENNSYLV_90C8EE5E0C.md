# PORTAL_CKA_WESTERN_PENNSYLV_90C8EE5E0C

rows 90  columns 19  scan 3.7s

roles: amount 1, audit 2, category 3, date 5, other 7, who 2

## when

IMPLEM_ON
  2020         5  ########
  2021        19  ############################
  2022        20  ##############################
  2023        10  ###############
  2024        20  ##############################
  2025        16  ########################

IMPLEMEN_1
  2020         5  ########
  2021        19  ############################
  2022        20  ##############################
  2023        10  ###############
  2024        20  ##############################
  2025        16  ########################

PLANNEDON
  2009         1  ##
  2013         1  ##
  2014         4  #########
  2015         3  #######
  2016         4  #########
  2017         3  #######
  2018        10  #######################
  2019         6  ##############
  2020        13  ##############################
  2021         7  ################
  2022         8  ##################
  2023         2  #####

PLANNEDON_2
  2009         1  ##
  2013         1  ##
  2014         4  #########
  2015         3  #######
  2016         4  #########
  2017         3  #######
  2018        10  #######################
  2019         6  ##############
  2020        13  ##############################
  2021         7  ################
  2022         8  ##################
  2023         2  #####

INGESTED_AT
  2026        90  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES_TREA | 90 | 0 | 1.38 | 10.11 | 13.50 | 202.01 |

## who

STATUS by rows
        90  Implemented

STATUS by dollars
      202.01       90 rows  Implemented

SRC_SHA256 by rows
        90  3cd32fa648a5ca27f92c3982e56aef9089cbc204ffd46f9fafd49c4a5eb5af6a

SRC_SHA256 by dollars
      202.01       90 rows  3cd32fa648a5ca27f92c3982e56aef9089cbc204ffd46f9fafd49c4a5eb5

## who x when

STATUS by IMPLEM_ON, dollars = ACRES_TREA
  Implemented                               2020:11.43 2021:49.99 2022:33.33 2023:34.45 2024:44.13 2025:28.68

SRC_SHA256 by IMPLEM_ON, dollars = ACRES_TREA
  3cd32fa648a5ca27f92c3982e56aef9089cbc204  2020:11.43 2021:49.99 2022:33.33 2023:34.45 2024:44.13 2025:28.68

## what

QUANTITY: 1 33%, 2 22%, 3 11%, 5 6%, 6 6%, 4 5%, 7 5%, 8 3%, 10 3%, 13 2%, 12 2%, 15 1%

MUNICIPALI: PITTSBURGH CITY 42%, MONROEVILLE BORO 11%, MCCANDLESS TWP 9%, MOON TWP 5%, BETHEL PARK BORO 5%, PLEASANT HILLS BORO 5%, RICHLAND TWP 4%, HAMPTON TWP 4%, PLUM BORO 4%, HARRISON TWP 4%, FINDLAY TWP 4%, LEET TWP 4%

PRACTICE: Water Quality Inserts/Inlets 91%, Oil/Grit Separators 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACRES_TREA | amount | 81 | 0 | 0.0 3; 0.23 2; 1.25 2; 0.95 2 |
| IMPLEM_ON | date | 88 | 0 | 11/5/2025 2; 04/19/2021 2; 07/27/2022 2; 8/1/2025 1 |
| IS_RC | other | 1 | 0 | No 90 |
| IS_VC | other | 1 | 0 | No 90 |
| IS_WQ | other | 1 | 0 | Yes 90 |
| QUANTITY | category | 15 | 0 | 1 29; 2 19; 3 10; 5 5 |
| VOLUMETREA | other | 1 | 0 | 0 90 |
| ADDRESS | other | 87 | 2 | 3500 Technology Drive 2; 317 Haymaker Road, Monroe 2; 2300 Defense Avenue, Cora 1; 327 N Negley Avenue, Pitt 1 |
| IDENTIFIER | other | 89 | 0 | BMP-02-02607 1; BMP-02-02599 1; BMP-02-02555 1; BMP-02-02535 1 |
| IMPLEMEN_1 | date | 88 | 0 | 20251105 2; 20210419 2; 20220727 2; 20250801 1 |
| MUNICIPALI | category | 43 | 0 | PITTSBURGH CITY 23; MONROEVILLE BORO 6; MCCANDLESS TWP 5; MOON TWP 3 |
| PLANNEDON | date | 62 | 28 | 11/19/2014 1; 7/24/2020 1; 10/18/2022 1; 8/22/2016 1 |
| PLANNEDON_2 | date | 62 | 28 | 20141119 1; 20200724 1; 20221018 1; 20160822 1 |
| PRACTICE | category | 2 | 0 | Water Quality Inserts/Inl 82; Oil/Grit Separators 8 |
| STATUS | who | 1 | 0 | Implemented 90 |
| GEOMETRY | other | 88 | 0 | MULTIPOINT ((-8928788.324 1; MULTIPOINT ((-8897644.054 1; MULTIPOINT ((-8899771.375 1; MULTIPOINT ((-8899669.157 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:31:00.34435 90 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2fd75cfa-cc94-4d4f-8e74-a 90 |
| SRC_SHA256 | who | 1 | 0 | 3cd32fa648a5ca27f92c3982e 90 |
