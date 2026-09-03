# PORTAL_SOC_TEXAS_OPEN_DATA_31F82D63F8

rows 2.0K  columns 17  scan 2.6s

roles: audit 2, category 8, date 2, other 5, who 1

## when

WST_STATUS_CD_DT
  2011         7  ##
  2012        55  #############
  2013        29  #######
  2014        36  ########
  2015        65  ###############
  2016        34  ########
  2017        48  ###########
  2018        54  #############
  2019        71  #################
  2020        56  #############
  2021        59  ##############
  2022        54  #############
  2023       129  ##############################
  2024        83  ###################
  2025       128  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## who

SRC_SHA256 by rows
      2.0K  ff61d92293f8a76c68ec2bc77145fdc3613d71049fec91ea366fc1b27ea2f219

## who x when

SRC_SHA256 by WST_STATUS_CD_DT
  ff61d92293f8a76c68ec2bc77145fdc3613d7104  2011:7 2012:55 2013:29 2014:36 2015:65 2016:34 2017:48 2018:54 2019:71 2020:56 2021:59 2022:54 2023:129 2024:83 2025:128

## what

SYS_TYP_CD1: H14 83%, nan 5%, H13 5%, H12 3%, H08 1%, H04 1%, H06 1%, H07 1%, H10 0%, H11 0%, H02 0%, H03 0%

EPA_FORM_CD: nan 65%, W219 9%, W319 6%, W409 4%, W801 3%, W110 3%, W119 2%, W001 2%, W203 2%, W113 2%, W210 1%, W103 1%

WST_STATUS_CD: ACTIVE 99%, INACTIVE 1%

ORIGIN_CD: 1 80%, 2 9%, 3 4%, 5 3%, 4 2%, 7 1%, nan 0%, 6 0%

WST_SOURCE_CD: nan 61%, G11 14%, G09 7%, G19 4%, G32 3%, G25 2%, G22 2%, G13 2%, G08 2%, G01 1%, G07 1%, G02 1%

WST_RADIOACT_FLG: False 99%, True 1%

NEW_CHEM_SUBST_FLG: 0 93%, 1 7%, nan 0%

WMU_REGIS_STATUS_CD: ACTIVE 95%, CLOSED 3%, INACTIVE 2%, UNDER CONSTRUCT 0%, CLOSURE PENDING 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SWR_NUM_TXT | other | 1.0K | 0 | 30459 62; 30106 62; 33983 32; 38669 31 |
| UNIT_SEQUENCE | other | 244 | 0 | 001 607; 002 128; 003 88; 004 71 |
| SYS_TYP_CD1 | category | 14 | 0 | H14 1.6K; nan 106; H13 91; H12 61 |
| TX_WST_CD | other | 1.6K | 0 | 0008219H 32; 04213021 23; 0009219H 13; 0006319H 12 |
| EPA_FORM_CD | category | 44 | 0 | nan 1.1K; W219 154; W319 107; W409 71 |
| WST_STATUS_CD | category | 2 | 0 | ACTIVE 2.0K; INACTIVE 10 |
| WST_STATUS_CD_DT | date | 627 | 0 | nan 1.1K; 2025-04-21T00:00:00.000 27; 2025-04-17T00:00:00.000 21; 2025-04-22T00:00:00.000 19 |
| WST_DESC_TXT | other | 1.7K | 0 | Miscellaneous hazardous l 28; Soil contaminated minor s 23; OXIDIZING LIQUIDS 12; Plant trash 10 |
| ORIGIN_CD | category | 8 | 0 | 1 1.6K; 2 186; 3 82; 5 66 |
| WST_SOURCE_CD | category | 33 | 0 | nan 1.1K; G11 255; G09 130; G19 65 |
| NAICS_CD | other | 142 | 0 | nan 1.1K; 444110 125; 325199 122; 452910 57 |
| WST_RADIOACT_FLG | category | 2 | 0 | False 2.0K; True 27 |
| NEW_CHEM_SUBST_FLG | category | 3 | 0 | 0 1.8K; 1 141; nan 8 |
| WMU_REGIS_STATUS_CD | category | 5 | 0 | ACTIVE 1.9K; CLOSED 51; INACTIVE 35; UNDER CONSTRUCT 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:49:04.18478 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1024beea-ad25-472e-abbb-6 2.0K |
| SRC_SHA256 | who | 1 | 0 | ff61d92293f8a76c68ec2bc77 2.0K |
