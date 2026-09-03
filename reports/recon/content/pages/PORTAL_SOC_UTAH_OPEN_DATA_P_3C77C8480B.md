# PORTAL_SOC_UTAH_OPEN_DATA_P_3C77C8480B

rows 450  columns 93  scan 3.7s

roles: amount 20, audit 2, category 23, date 2, other 46, who 1

## when

DOC_CTRL_NUM
  2011       403  ##############################
  2014        47  ###

INGESTED_AT
  2026       450  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| C_5_1_FUGITIVE_AIR | 450 | 0 | 5.25 | 808.95 | 1.4K | 21.8K |
| C_5_2_STACK_AIR | 450 | 0 | 300 | 645.1K | 930.0K | 14.49M |
| C_5_5_2_LAND_TREATMENT | 450 | 0 | 0 | 517.86 | 2.7K | 18.5K |
| C_5_5_4_OTHER_DISPOSAL | 450 | 0 | 0 | 243.06 | 887 | 3.9K |
| ON_SITE_RELEASE_TOTAL | 450 | 0 | 43.0K | 961.5K | 1.34M | 51.56M |
| C_6_2_M10 | 450 | 0 | 0 | 0 | 0.70 | 0.70 |

## who

SRC_SHA256 by rows
       450  3b021b9f8d9ecec0c2f56d4563b44bbf58b39cae3a43dc87c91f95eed8f1f461

SRC_SHA256 by dollars
      51.56M      450 rows  3b021b9f8d9ecec0c2f56d4563b44bbf58b39cae3a43dc87c91f95eed8f1

## who x when

SRC_SHA256 by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  3b021b9f8d9ecec0c2f56d4563b44bbf58b39cae  2011:43.40M 2014:8.16M

## what

YEAR: 2002 9%, 2003 9%, 2007 9%, 2004 9%, 2001 9%, 2006 8%, 2005 8%, 2010 8%, 2009 8%, 2000 8%, 2012 8%, 2011 8%

TRI_FACILITY_ID: 84513PCFCR3MILE 51%, 84528PCFCR10MIL 48%, 84537TRLMNWONHW 1%

FACILITY_NAME: PACIFICORP HUNTER PLANT 51%, PACIFICORP ENERGY - HUNTINGTON 48%, TRAIL MOUNTAIN COTTONWOOD MINE 1%

STREET_ADDRESS: 3 MILES S OF CASTLE DALE ON ST 51%, 10 MILES W OF HUNTINGTON 48%, W. ON HWY. 29 FOR 10 MILES COT 1%

PRIMARY_SIC: 4911 50%, nan 49%, 1222 1%

SIC_2: nan 50%, 1221 26%, 1222 24%

PRIMARY_NAICS: 221112 96%, 221119 3%, 212112 1%

CHEMICAL: COPPER COMPOUNDS 9%, HYDROGEN FLUORIDE 9%, CHROMIUM COMPOUNDS(EXCEPT CHRO 9%, BARIUM COMPOUNDS 9%, HYDROCHLORIC ACID (1995 AND AF 9%, LEAD COMPOUNDS 9%, NICKEL COMPOUNDS 9%, MANGANESE COMPOUNDS 9%, ZINC COMPOUNDS 8%, MERCURY COMPOUNDS 8%, SULFURIC ACID (1994 AND AFTER  8%, VANADIUM COMPOUNDS 8%

CAS_COMPOUND_ID: N100 9%, 7664393 9%, N090 9%, N040 9%, 7647010 9%, N420 9%, N495 9%, N450 9%, N982 8%, N458 8%, 7664939 8%, N770 8%

CLEAR_AIR_ACT_CHEMICAL: YES 62%, NO 38%

CLASSIFICATION: TRI 76%, PBT 19%, Dioxin 6%

METAL: YES 57%, NO 43%

METAL_CATEGORY: 1 57%, 0 32%, 3 7%, 2 4%

CARCINOGEN: NO 94%, YES 6%

FORM_TYPE: R 97%, A 3%

UNIT_OF_MEASURE: Pounds 94%, Grams 6%

C_5_3_WATER: 0 100%, 6 0%

C_6_2_M72: 0 98%, 1 1%, 5 0%, 9 0%, 20 0%

C_6_2_M20: 0 100%, 1 0%

C_8_8_ONE_TIME_RELEASE: nan 73%, 0 27%

PARENT_COMPANY_NAME: BERKSHIRE HATHAWAY 99%, SCOTTISH POWER 1%

LOCATION_1: {"latitude": "39.17315", "long 51%, {"latitude": "39.3815", "longi 48%, {"latitude": "39.31639", "long 1%

NAICS_2: nan 51%, 213113 25%, 212112 18%, 212111 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 16 | 0 | 2002 33; 2003 32; 2007 30; 2004 30 |
| TRI_FACILITY_ID | category | 3 | 0 | 84513PCFCR3MILE 229; 84528PCFCR10MIL 218; 84537TRLMNWONHW 3 |
| FACILITY_NAME | category | 3 | 0 | PACIFICORP HUNTER PLANT 229; PACIFICORP ENERGY - HUNTI 218; TRAIL MOUNTAIN COTTONWOOD 3 |
| STREET_ADDRESS | category | 3 | 0 | 3 MILES S OF CASTLE DALE  229; 10 MILES W OF HUNTINGTON 218; W. ON HWY. 29 FOR 10 MILE 3 |
| COUNTY | other | 1 | 0 | EMERY 450 |
| ST | other | 1 | 0 | UT 450 |
| FEDERAL_FACILITY | other | 1 | 0 | NO 450 |
| PRIMARY_SIC | category | 3 | 0 | 4911 226; nan 221; 1222 3 |
| SIC_2 | category | 3 | 0 | nan 224; 1221 117; 1222 109 |
| PRIMARY_NAICS | category | 3 | 0 | 221112 432; 221119 15; 212112 3 |
| DOC_CTRL_NUM | date | 3 | 0 | 1310000000000 250; 1300000000000 153; 1400000000000 47 |
| CHEMICAL | category | 20 | 0 | COPPER COMPOUNDS 32; HYDROGEN FLUORIDE 32; CHROMIUM COMPOUNDS(EXCEPT 32; BARIUM COMPOUNDS 32 |
| CAS_COMPOUND_ID | category | 20 | 0 | N100 32; 7664393 32; N090 32; N040 32 |
| CLEAR_AIR_ACT_CHEMICAL | category | 2 | 0 | YES 280; NO 170 |
| CLASSIFICATION | category | 3 | 0 | TRI 340; PBT 84; Dioxin 26 |
| METAL | category | 2 | 0 | YES 258; NO 192 |
| METAL_CATEGORY | category | 4 | 0 | 1 258; 0 142; 3 32; 2 18 |
| CARCINOGEN | category | 2 | 0 | NO 421; YES 29 |
| FORM_TYPE | category | 2 | 0 | R 437; A 13 |
| UNIT_OF_MEASURE | category | 2 | 0 | Pounds 424; Grams 26 |
| C_5_1_FUGITIVE_AIR | amount | 149 | 0 | 0 163; 7 14; 0.1 12; 10 11 |
| C_5_2_STACK_AIR | amount | 354 | 0 | 0 22; 1100 5; 112 4; 480 4 |
| C_5_3_WATER | category | 2 | 0 | 0 449; 6 1 |
| C_5_4_1_UNDERGROUND_CLASS_I | other | 1 | 0 | 0 450 |
| C_5_4_2_UNDERGROUND_CLASS_II_V | other | 1 | 0 | 0 450 |
| C_5_5_1A_RCRA_C_LANDFILLS | other | 1 | 0 | 0 450 |
| C_5_5_1B_OTHER_LANDFILLS | other | 229 | 0 | 0 160; 34000 4; 46000 4; 59000 4 |
| C_5_5_2_LAND_TREATMENT | amount | 86 | 0 | 0 340; 99 3; 84 3; 10 3 |
| C_5_5_3_SURFACE_IMPOUNDMENT | other | 1 | 0 | 0 450 |
| C_5_5_3A_RCRA_C_SURFACE_IMP | other | 1 | 0 | 0 450 |
| C_5_5_3B_OTHER_SURFACE_IMP | other | 1 | 0 | 0 450 |
| C_5_5_4_OTHER_DISPOSAL | amount | 47 | 0 | 0 363; 1 12; 2 7; 3 4 |
| ON_SITE_RELEASE_TOTAL | amount | 426 | 0 | 0 19; 62700 4; 0.65348799999999996 3; 51707 3 |
| C_6_1_POTW_TRANSFERS_FOR_RELEASE | other | 1 | 0 | 0 450 |
| C_6_1_POTW_TRANSFERS_FOR_TREATM | other | 1 | 0 | 0 450 |
| C_6_1_POTW_TOTAL_TRANSFERS | other | 1 | 0 | 0 450 |
| C_6_2_M10 | amount | 2 | 0 | 0 449; 0.7 1 |
| C_6_2_M41 | amount | 9 | 0 | 0 441; 0.2 2; 185 1; 0.4 1 |
| C_6_2_M62 | other | 1 | 0 | 0 450 |
| C_6_2_M71 | other | 1 | 0 | 0 450 |
| C_6_2_M81 | other | 1 | 0 | 0 450 |
| C_6_2_M82 | other | 1 | 0 | 0 450 |
| C_6_2_M72 | category | 5 | 0 | 0 443; 1 3; 5 2; 9 1 |
| C_6_2_M63 | other | 1 | 0 | 0 450 |
| C_6_2_M66 | other | 1 | 0 | 0 450 |
| C_6_2_M67 | other | 1 | 0 | 0 450 |
| C_6_2_M64 | other | 1 | 0 | 0 450 |
| C_6_2_M65 | other | 1 | 0 | 0 450 |
| C_6_2_M73 | other | 1 | 0 | 0 450 |
| C_6_2_M79 | amount | 78 | 0 | 0 369; 26 2; 0.1 2; 1100 2 |
| C_6_2_M90 | other | 1 | 0 | 0 450 |
| C_6_2_M94 | amount | 32 | 0 | 0 414; 5 3; 0.1 2; 1 2 |
| C_6_2_M99 | other | 1 | 0 | 0 450 |
| OFF_SITE_RELEASE_TOTAL | amount | 105 | 0 | 0 337; 0.1 4; 5 3; 26 2 |
| C_6_2_M20 | category | 2 | 0 | 0 449; 1 1 |
| C_6_2_M24 | other | 1 | 0 | 0 450 |
| C_6_2_M26 | amount | 19 | 0 | 0 429; 1 3; 2 2; 0.3 1 |
| C_6_2_M28 | other | 1 | 0 | 0 450 |
| C_6_2_M93 | amount | 79 | 0 | 0 363; 1.2 4; 1 4; 4 3 |
| OFF_SITE_RECYCLED_TOTAL | amount | 94 | 0 | 0 342; 1 8; 1.2 4; 2 4 |
| C_6_2_M56 | other | 1 | 0 | 0 450 |
| C_6_2_M92 | other | 1 | 0 | 0 450 |
| OFF_SITE_RECOVERY_TOTAL | other | 1 | 0 | 0 450 |
| C_6_2_M40 | other | 1 | 0 | 0 450 |
| C_6_2_M50 | other | 1 | 0 | 0 450 |
| C_6_2_M54 | other | 1 | 0 | 0 450 |
| C_6_2_M61 | other | 1 | 0 | 0 450 |
| C_6_2_M69 | other | 1 | 0 | 0 450 |
| C_6_2_M95 | other | 1 | 0 | 0 450 |
| OFF_SITE_TREATED_TOTAL | other | 1 | 0 | 0 450 |
| TOTAL_RELEASES | amount | 428 | 0 | 0 19; 62700 4; 0.65349999999999997 3; 51707 3 |
| C_8_1_RELEASES | other | 93 | 0 | 0 320; 50000 5; 34000 4; 54000 4 |
| C_8_1A_ON_SITE_CONTAINED_REL | amount | 195 | 0 | 0 252; 59000 3; 35700 2; 93000 2 |
| C_8_1B_ON_SITE_OTHER_RELEASES | amount | 291 | 0 | 0 149; 133 3; 378 3; 316 3 |
| C_8_1C_OFF_SITE_CONTAINED_REL | other | 1 | 0 | 0 450 |
| C_8_1D_OFF_SITE_OTHER_RELEASES | amount | 53 | 0 | 0 393; 0.1 4; 5 3; 9.1999999999999993 1 |
| C_8_2_ENERGY_RECOVERY_ON_SITE | other | 1 | 0 | 0 450 |
| C_8_3_ENERGY_RECOVERY_OFF_SITE | other | 1 | 0 | 0 450 |
| C_8_4_RECYCLING_ON_SITE | other | 1 | 0 | 0 450 |
| C_8_5_RECYCLING_OFF_SITE | amount | 92 | 0 | 0 347; 1 7; 1.2 4; 2 3 |
| C_8_6_TREATMENT_ON_SITE | other | 86 | 0 | 0 357; 2000000 3; 1300000 2; 450000 2 |
| C_8_7_TREATMENT_OFF_SITE | other | 1 | 0 | 0 450 |
| PROD_WASTE_8_1_THRU_8_7 | amount | 405 | 0 | 0 19; 34000 4; 54000 4; 50000 4 |
| C_8_8_ONE_TIME_RELEASE | category | 2 | 0 | nan 327; 0 123 |
| C_8_9_PRODUCTION_RATIO | amount | 22 | 0 | 0.96 43; 1 42; 1.04 38; 0.92 28 |
| PARENT_COMPANY_NAME | category | 2 | 0 | BERKSHIRE HATHAWAY 447; SCOTTISH POWER 3 |
| PARENT_COMPANY_DB_NUMBER | other | 1 | 0 | 7909013 450 |
| LOCATION_1 | category | 3 | 0 | {"latitude": "39.17315",  229; {"latitude": "39.3815", " 218; {"latitude": "39.31639",  3 |
| COMPUTED_REGION_9Z68_3KQ5 | other | 1 | 0 | 2990 450 |
| NAICS_2 | category | 4 | 0 | nan 229; 213113 112; 212112 79; 212111 30 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:50:07.97967 450 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9e42d5b7-ab04-478e-8647-d 450 |
| SRC_SHA256 | who | 1 | 0 | 3b021b9f8d9ecec0c2f56d456 450 |
