# PORTAL_SOC_UTAH_OPEN_DATA_P_B0F7881369

rows 107  columns 92  scan 4.2s

roles: amount 7, audit 2, category 31, date 2, other 48, who 3

## when

DOC_CTRL_NUM
  2011        36  ###############
  2014        71  ##############################

INGESTED_AT
  2026       107  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ON_SITE_RELEASE_TOTAL | 107 | 0 | 200 | 20.2K | 23.2K | 233.9K |
| OFF_SITE_RELEASE_TOTAL | 107 | 0 | 0 | 2.6K | 6.7K | 16.6K |
| OFF_SITE_RECYCLED_TOTAL | 107 | 0 | 0 | 12.64 | 1.6K | 1.6K |
| OFF_SITE_RECOVERY_TOTAL | 107 | 0 | 0 | 89.58 | 910 | 1.1K |
| OFF_SITE_TREATED_TOTAL | 107 | 0 | 0 | 5.88 | 10 | 28 |
| TOTAL_RELEASES | 107 | 0 | 204 | 20.8K | 25.1K | 250.5K |

## who

UNIT_OF_MEASURE by rows
       107  Pounds

UNIT_OF_MEASURE by dollars
      233.9K      107 rows  Pounds

COUNTY by rows
       107  DUCHESNE

COUNTY by dollars
      233.9K      107 rows  DUCHESNE

SRC_SHA256 by rows
       107  887f69fcd7dc9ef5131b8cb1b3e6119ee6e10c2d7683da0b5ea1895186dcd4e7

SRC_SHA256 by dollars
      233.9K      107 rows  887f69fcd7dc9ef5131b8cb1b3e6119ee6e10c2d7683da0b5ea1895186dc

## who x when

UNIT_OF_MEASURE by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  Pounds                                    2011:3.1K 2014:230.8K

COUNTY by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  DUCHESNE                                  2011:3.1K 2014:230.8K

## what

YEAR: 1992 15%, 1994 14%, 1993 14%, 1991 14%, 1990 14%, 2013 8%, 2010 7%, 2012 6%, 2011 5%, 2009 2%, 2006 2%, 2005 2%

TRI_FACILITY_ID: 84066PNNZLWESTH 66%, 84066BJSRV1661W 31%, 8406WBJCHM1382S 3%

FACILITY_NAME: PENNZOIL PRODUCTS CO. ROOSEVEL 66%, MULTI-CHEM GROUP ROOSEVELT UT  31%, BAKER HUGHES INC. 3%

STREET_ADDRESS: WEST. HWY. 40 66%, 1661 W HWY 40 31%, 1382 S 2300 W 3%

PRIMARY_SIC: 2911 66%, nan 29%, 5169 5%

SIC_2: NA 65%, nan 35%

PRIMARY_NAICS: 324110 66%, 424690 34%

CHEMICAL: METHANOL 14%, XYLENE (MIXED ISOMERS) 12%, ETHYLBENZENE 11%, TOLUENE 11%, 1,2,4-TRIMETHYLBENZENE 9%, CYCLOHEXANE 6%, NAPHTHALENE 6%, AMMONIA 6%, CRESOL (MIXED ISOMERS) 6%, BENZENE 6%, PROPYLENE 6%, CUMENE 6%

CAS_COMPOUND_ID: 67561 14%, 1330207 12%, 100414 11%, 108883 11%, 95636 9%, 110827 6%, 91203 6%, 7664417 6%, 1319773 6%, 71432 6%, 115071 6%, 98828 6%

CLEAR_AIR_ACT_CHEMICAL: YES 66%, NO 34%

CARCINOGEN: NO 93%, YES 7%

FORM_TYPE: R 70%, A 30%

C_5_2_STACK_AIR: 0 74%, 2900 3%, 270 3%, 2400 3%, 3900 3%, 3400 3%, 44 3%, 100 3%, 11000 3%, 660 1%, 460 1%, 950 1%

C_6_1_POTW_TRANSFERS_FOR_TREATM: 0 82%, 5 5%, 110 2%, 440 2%, 370 1%, 32000 1%, 75 1%, 24 1%, 13 1%, 300 1%, 1500 1%, 50 1%

C_6_2_M72: 0 88%, 1 2%, 3 1%, 57 1%, 2600 1%, 12 1%, 194 1%, 7 1%, 39 1%, 221 1%, 6526 1%, 1306 1%

C_6_2_M94: 0 92%, 5 2%, 7 1%, 9 1%, 130 1%, 27 1%, 75 1%, 8 1%, 40 1%

C_6_2_M20: 0 97%, 6 1%, 7 1%, 13 1%

C_6_2_M93: 0 99%, 1600 1%

C_6_2_M92: 0 96%, 910 1%, 83 1%, 3 1%, 90 1%

C_6_2_M95: 0 93%, 2 2%, 6 1%, 10 1%, 3 1%, 4 1%, 1 1%

C_8_1_RELEASES: 0 75%, 13000 5%, 1400 4%, 3300 3%, 10000 3%, 4700 3%, 6500 1%, 58 1%, 70 1%, 4300 1%, 130 1%, 5400 1%

C_8_1B_ON_SITE_OTHER_RELEASES: 0 96%, 990 1%, 670 1%, 980 1%, 430 1%

C_8_1D_OFF_SITE_OTHER_RELEASES: 0 97%, 7 1%, 5 1%, 9 1%

C_8_3_ENERGY_RECOVERY_OFF_SITE: 0 96%, 910 1%, 83 1%, 3 1%, 90 1%

C_8_4_RECYCLING_ON_SITE: 0 87%, 110 2%, 1600 2%, 1800 1%, 360 1%, 61 1%, 530 1%, 1100 1%, 5500 1%, 190 1%, 350 1%, 2300 1%

C_8_5_RECYCLING_OFF_SITE: 0 94%, 7 2%, 1600 1%, 13 1%, 50000 1%, 67000 1%

C_8_7_TREATMENT_OFF_SITE: 0 90%, 370 1%, 32000 1%, 75 1%, 24 1%, 13 1%, 110 1%, 300 1%, 1500 1%, 50 1%, 39000 1%, 440 1%

PARENT_COMPANY_NAME: PENNZOIL CO 66%, HALLIBURTON ENERGY SERVICES IN 31%, BAKER HUGHES INC 3%

PARENT_COMPANY_DB_NUMBER: 8106429 66%, 43296920 31%, nan 3%

LOCATION_1: {"latitude": "40.38856", "long 66%, {"latitude": "40.27724", "long 31%, {"latitude": "40.28009", "long 3%

C_8_8_ONE_TIME_RELEASE: 0 47%, nan 31%, 1 6%, 2 5%, 27 2%, 200 2%, 94 1%, 37 1%, 260 1%, 9 1%, 33 1%, 150 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 16 | 0 | 1992 15; 1994 14; 1993 14; 1991 14 |
| TRI_FACILITY_ID | category | 3 | 0 | 84066PNNZLWESTH 71; 84066BJSRV1661W 33; 8406WBJCHM1382S 3 |
| FACILITY_NAME | category | 3 | 0 | PENNZOIL PRODUCTS CO. ROO 71; MULTI-CHEM GROUP ROOSEVEL 33; BAKER HUGHES INC. 3 |
| STREET_ADDRESS | category | 3 | 0 | WEST. HWY. 40 71; 1661 W HWY 40 33; 1382 S 2300 W 3 |
| COUNTY | who | 1 | 0 | DUCHESNE 107 |
| ST | other | 1 | 0 | UT 107 |
| FEDERAL_FACILITY | other | 1 | 0 | NO 107 |
| PRIMARY_SIC | category | 3 | 0 | 2911 71; nan 31; 5169 5 |
| SIC_2 | category | 2 | 0 | NA 70; nan 37 |
| PRIMARY_NAICS | category | 2 | 0 | 324110 71; 424690 36 |
| DOC_CTRL_NUM | date | 3 | 0 | 1390000000000 71; 1310000000000 33; 1300000000000 3 |
| CHEMICAL | category | 20 | 0 | METHANOL 11; XYLENE (MIXED ISOMERS) 10; ETHYLBENZENE 9; TOLUENE 9 |
| CAS_COMPOUND_ID | category | 19 | 0 | 67561 11; 1330207 10; 100414 9; 108883 9 |
| CLEAR_AIR_ACT_CHEMICAL | category | 2 | 0 | YES 71; NO 36 |
| CLASSIFICATION | other | 1 | 0 | TRI 107 |
| METAL | other | 1 | 0 | NO 107 |
| METAL_CATEGORY | other | 1 | 0 | 0 107 |
| CARCINOGEN | category | 2 | 0 | NO 100; YES 7 |
| FORM_TYPE | category | 2 | 0 | R 75; A 32 |
| UNIT_OF_MEASURE | who | 1 | 0 | Pounds 107 |
| C_5_1_FUGITIVE_AIR | other | 55 | 0 | 0 44; 1400 3; 30 2; 490 2 |
| C_5_2_STACK_AIR | category | 45 | 0 | 0 55; 2900 2; 270 2; 2400 2 |
| C_5_3_WATER | other | 1 | 0 | 0 107 |
| C_5_4_1_UNDERGROUND_CLASS_I | other | 1 | 0 | 0 107 |
| C_5_4_2_UNDERGROUND_CLASS_II_V | other | 1 | 0 | 0 107 |
| C_5_5_1A_RCRA_C_LANDFILLS | other | 1 | 0 | 0 107 |
| C_5_5_1B_OTHER_LANDFILLS | other | 1 | 0 | 0 107 |
| C_5_5_2_LAND_TREATMENT | other | 1 | 0 | 0 107 |
| C_5_5_3_SURFACE_IMPOUNDMENT | other | 1 | 0 | 0 107 |
| C_5_5_3A_RCRA_C_SURFACE_IMP | other | 1 | 0 | 0 107 |
| C_5_5_3B_OTHER_SURFACE_IMP | other | 1 | 0 | 0 107 |
| C_5_5_4_OTHER_DISPOSAL | other | 1 | 0 | 0 107 |
| ON_SITE_RELEASE_TOTAL | amount | 61 | 0 | 0 44; 2900 2; 820 2; 990 1 |
| C_6_1_POTW_TRANSFERS_FOR_RELEASE | other | 1 | 0 | 0 107 |
| C_6_1_POTW_TRANSFERS_FOR_TREATM | category | 32 | 0 | 0 71; 5 4; 110 2; 440 2 |
| C_6_1_POTW_TOTAL_TRANSFERS | other | 1 | 0 | 0 107 |
| C_6_2_M10 | other | 1 | 0 | 0 107 |
| C_6_2_M41 | other | 1 | 0 | 0 107 |
| C_6_2_M62 | other | 1 | 0 | 0 107 |
| C_6_2_M71 | other | 1 | 0 | 0 107 |
| C_6_2_M81 | other | 1 | 0 | 0 107 |
| C_6_2_M82 | other | 1 | 0 | 0 107 |
| C_6_2_M72 | category | 21 | 0 | 0 86; 1 2; 3 1; 57 1 |
| C_6_2_M63 | other | 1 | 0 | 0 107 |
| C_6_2_M66 | other | 1 | 0 | 0 107 |
| C_6_2_M67 | other | 1 | 0 | 0 107 |
| C_6_2_M64 | other | 1 | 0 | 0 107 |
| C_6_2_M65 | other | 1 | 0 | 0 107 |
| C_6_2_M73 | other | 1 | 0 | 0 107 |
| C_6_2_M79 | other | 1 | 0 | 0 107 |
| C_6_2_M90 | other | 1 | 0 | 0 107 |
| C_6_2_M94 | category | 9 | 0 | 0 98; 5 2; 7 1; 9 1 |
| C_6_2_M99 | other | 1 | 0 | 0 107 |
| OFF_SITE_RELEASE_TOTAL | amount | 23 | 0 | 0 83; 7 2; 1 2; 5 1 |
| C_6_2_M20 | category | 4 | 0 | 0 104; 6 1; 7 1; 13 1 |
| C_6_2_M24 | other | 1 | 0 | 0 107 |
| C_6_2_M26 | other | 1 | 0 | 0 107 |
| C_6_2_M28 | other | 1 | 0 | 0 107 |
| C_6_2_M93 | category | 2 | 0 | 0 106; 1600 1 |
| OFF_SITE_RECYCLED_TOTAL | amount | 5 | 0 | 0 103; 1600 1; 6 1; 7 1 |
| C_6_2_M56 | other | 1 | 0 | 0 107 |
| C_6_2_M92 | category | 5 | 0 | 0 103; 910 1; 83 1; 3 1 |
| OFF_SITE_RECOVERY_TOTAL | amount | 5 | 0 | 0 103; 910 1; 83 1; 3 1 |
| C_6_2_M40 | other | 1 | 0 | 0 107 |
| C_6_2_M50 | other | 1 | 0 | 0 107 |
| C_6_2_M54 | other | 1 | 0 | 0 107 |
| C_6_2_M61 | other | 1 | 0 | 0 107 |
| C_6_2_M69 | other | 1 | 0 | 0 107 |
| C_6_2_M95 | category | 7 | 0 | 0 100; 2 2; 6 1; 10 1 |
| OFF_SITE_TREATED_TOTAL | amount | 7 | 0 | 0 100; 2 2; 6 1; 10 1 |
| TOTAL_RELEASES | amount | 63 | 0 | 0 43; 2900 2; 820 2; 997 1 |
| C_8_1_RELEASES | category | 43 | 0 | 0 57; 13000 4; 1400 3; 3300 2 |
| C_8_1A_ON_SITE_CONTAINED_REL | other | 1 | 0 | 0 107 |
| C_8_1B_ON_SITE_OTHER_RELEASES | category | 5 | 0 | 0 103; 990 1; 670 1; 980 1 |
| C_8_1C_OFF_SITE_CONTAINED_REL | other | 1 | 0 | 0 107 |
| C_8_1D_OFF_SITE_OTHER_RELEASES | category | 4 | 0 | 0 104; 7 1; 5 1; 9 1 |
| C_8_2_ENERGY_RECOVERY_ON_SITE | other | 1 | 0 | 0 107 |
| C_8_3_ENERGY_RECOVERY_OFF_SITE | category | 5 | 0 | 0 103; 910 1; 83 1; 3 1 |
| C_8_4_RECYCLING_ON_SITE | category | 20 | 0 | 0 86; 110 2; 1600 2; 1800 1 |
| C_8_5_RECYCLING_OFF_SITE | category | 6 | 0 | 0 101; 7 2; 1600 1; 13 1 |
| C_8_6_TREATMENT_ON_SITE | other | 1 | 0 | 0 107 |
| C_8_7_TREATMENT_OFF_SITE | category | 13 | 0 | 0 95; 370 1; 32000 1; 75 1 |
| PROD_WASTE_8_1_THRU_8_7 | other | 55 | 0 | 0 49; 1600 2; 3300 2; 67000 2 |
| PARENT_COMPANY_NAME | category | 3 | 0 | PENNZOIL CO 71; HALLIBURTON ENERGY SERVIC 33; BAKER HUGHES INC 3 |
| PARENT_COMPANY_DB_NUMBER | category | 3 | 0 | 8106429 71; 43296920 33; nan 3 |
| LOCATION_1 | category | 3 | 0 | {"latitude": "40.38856",  71; {"latitude": "40.27724",  33; {"latitude": "40.28009",  3 |
| COMPUTED_REGION_9Z68_3KQ5 | other | 1 | 0 | 2989 107 |
| C_8_9_PRODUCTION_RATIO | amount | 9 | 0 | 0 25; nan 21; 1.01 15; 0.7 14 |
| C_8_8_ONE_TIME_RELEASE | category | 22 | 0 | 0 45; nan 30; 1 6; 2 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:42:18.01462 107 |
| SOURCE_RUN_ID | audit | 1 | 0 | eee7a54a-7162-4af4-bb88-0 107 |
| SRC_SHA256 | who | 1 | 0 | 887f69fcd7dc9ef5131b8cb1b 107 |
