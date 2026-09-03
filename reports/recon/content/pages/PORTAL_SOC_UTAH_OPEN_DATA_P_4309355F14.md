# PORTAL_SOC_UTAH_OPEN_DATA_P_4309355F14

rows 49  columns 93  scan 4.1s

roles: amount 9, audit 2, category 21, date 2, other 57, who 3

## when

DOC_CTRL_NUM
  2011        41  ##############################
  2014         8  ######

INGESTED_AT
  2026        49  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| C_5_2_STACK_AIR | 49 | 0 | 0 | 111.49 | 206 | 288.42 |
| ON_SITE_RELEASE_TOTAL | 49 | 0 | 0 | 269.47 | 492 | 602.42 |
| C_6_2_M64 | 49 | 0 | 0 | 13.30 | 13.60 | 122.27 |
| OFF_SITE_RELEASE_TOTAL | 49 | 0 | 0 | 13.30 | 13.60 | 122.27 |
| TOTAL_RELEASES | 49 | 0 | 0 | 269.47 | 492 | 724.69 |
| C_8_1B_ON_SITE_OTHER_RELEASES | 49 | 0 | 0 | 269.47 | 492 | 602.32 |

## who

UNIT_OF_MEASURE by rows
        49  Pounds

UNIT_OF_MEASURE by dollars
      602.42       49 rows  Pounds

COUNTY by rows
        49  BEAVER

COUNTY by dollars
      602.42       49 rows  BEAVER

SRC_SHA256 by rows
        49  c086e86458df01408b9b872d357ea649f97f035e6dee4ecac10ac2eacc8a27b5

SRC_SHA256 by dollars
      602.42       49 rows  c086e86458df01408b9b872d357ea649f97f035e6dee4ecac10ac2eacc8a

## who x when

UNIT_OF_MEASURE by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  Pounds                                    2011:602.42 2014:0

COUNTY by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  BEAVER                                    2011:602.42 2014:0

## what

YEAR: 2011 10%, 2010 10%, 2009 10%, 2002 10%, 2012 8%, 2008 8%, 2007 8%, 2006 8%, 2005 8%, 2003 8%, 2001 8%, 2013 5%

TRI_FACILITY_ID: 84751MRPHY585E6 59%, 84713CCHVL330WE 37%, 84752SMTHF36WTH 4%

FACILITY_NAME: MURPHY-BROWN LLC CIRCLE 4 FEED 59%, DAIRY FARMERS OF AMERICA INC B 37%, SMITHFIELD BIOENERGY LLC 4%

STREET_ADDRESS: 585 E 6TH AVE 59%, 330 W 300 S 37%, 3600 W THERMO RD 4%

PRIMARY_SIC: nan 53%, 2048 27%, 2022 18%, 2869 2%

PRIMARY_NAICS: 311119 59%, 311514 18%, 311513 18%, 325199 4%

CHEMICAL: ZINC (FUME OR DUST) 27%, NITRIC ACID 22%, COPPER COMPOUNDS 14%, COPPER 12%, NITRATE COMPOUNDS 6%, MANGANESE 6%, SULFURIC ACID (1994 AND AFTER  6%, METHANOL 4%, PHOSPHORIC ACID 2%

CAS_COMPOUND_ID: 7440666 27%, 7697372 22%, N100 14%, 7440508 12%, N511 6%, 7439965 6%, 7664939 6%, 67561 4%, 7664382 2%

CLEAR_AIR_ACT_CHEMICAL: NO 90%, YES 10%

METAL: NO 67%, YES 33%

METAL_CATEGORY: 0 41%, 1 33%, 4 27%

C_5_1_FUGITIVE_AIR: 0 96%, 28 2%, 286 2%

C_6_1_POTW_TRANSFERS_FOR_TREATM: 0 77%, 19206 2%, 18899 2%, 19195 2%, 105 2%, 106 2%, 180 2%, 130 2%, 150 2%, 170 2%, 100 2%, 10700 2%

C_8_6_TREATMENT_ON_SITE: 0 77%, 14055 2%, 19512 2%, 19201 2%, 19501 2%, 16641 2%, 10371 2%, 10469 2%, 18020 2%, 13070 2%, 15000 2%, 17000 2%

C_8_7_TREATMENT_OFF_SITE: 0 80%, 19206 2%, 18899 2%, 19195 2%, 105 2%, 106 2%, 180 2%, 130 2%, 150 2%, 200 2%, 100 2%

PARENT_COMPANY_NAME: MURPHY BROWN LLC 59%, DAIRY FARMERS OF AMERICA INC 37%, SMITHFIELD BIOENERGY LLC 4%

PARENT_COMPANY_DB_NUMBER: 24847444 59%, 29855640 37%, nan 4%

LOCATION_1: {"latitude": "38.38871", "long 59%, {"latitude": "38.21091", "long 37%, {"latitude": "38.21404", "long 4%

SIC_2: nan 92%, NA 8%

C_8_8_ONE_TIME_RELEASE: nan 90%, 0 10%

NAICS_2: nan 88%, 311513 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 18 | 0 | 2011 4; 2010 4; 2009 4; 2002 4 |
| TRI_FACILITY_ID | category | 3 | 0 | 84751MRPHY585E6 29; 84713CCHVL330WE 18; 84752SMTHF36WTH 2 |
| FACILITY_NAME | category | 3 | 0 | MURPHY-BROWN LLC CIRCLE 4 29; DAIRY FARMERS OF AMERICA  18; SMITHFIELD BIOENERGY LLC 2 |
| STREET_ADDRESS | category | 3 | 0 | 585 E 6TH AVE 29; 330 W 300 S 18; 3600 W THERMO RD 2 |
| COUNTY | who | 1 | 0 | BEAVER 49 |
| ST | other | 1 | 0 | UT 49 |
| FEDERAL_FACILITY | other | 1 | 0 | NO 49 |
| PRIMARY_SIC | category | 4 | 0 | nan 26; 2048 13; 2022 9; 2869 1 |
| PRIMARY_NAICS | category | 4 | 0 | 311119 29; 311514 9; 311513 9; 325199 2 |
| DOC_CTRL_NUM | date | 4 | 0 | 1310000000000 29; 1300000000000 12; 1390000000000 5; 1400000000000 3 |
| CHEMICAL | category | 9 | 0 | ZINC (FUME OR DUST) 13; NITRIC ACID 11; COPPER COMPOUNDS 7; COPPER 6 |
| CAS_COMPOUND_ID | category | 9 | 0 | 7440666 13; 7697372 11; N100 7; 7440508 6 |
| CLEAR_AIR_ACT_CHEMICAL | category | 2 | 0 | NO 44; YES 5 |
| CLASSIFICATION | other | 1 | 0 | TRI 49 |
| METAL | category | 2 | 0 | NO 33; YES 16 |
| METAL_CATEGORY | category | 3 | 0 | 0 20; 1 16; 4 13 |
| CARCINOGEN | other | 1 | 0 | NO 49 |
| FORM_TYPE | other | 1 | 0 | R 49 |
| UNIT_OF_MEASURE | who | 1 | 0 | Pounds 49 |
| C_5_1_FUGITIVE_AIR | category | 3 | 0 | 0 47; 28 1; 286 1 |
| C_5_2_STACK_AIR | amount | 20 | 0 | 0 27; 2.29 2; 4.3899999999999997 2; 4.0999999999999996 2 |
| C_5_3_WATER | other | 1 | 0 | 0 49 |
| C_5_4_1_UNDERGROUND_CLASS_I | other | 1 | 0 | 0 49 |
| C_5_4_2_UNDERGROUND_CLASS_II_V | other | 1 | 0 | 0 49 |
| C_5_5_1A_RCRA_C_LANDFILLS | other | 1 | 0 | 0 49 |
| C_5_5_1B_OTHER_LANDFILLS | other | 1 | 0 | 0 49 |
| C_5_5_2_LAND_TREATMENT | other | 1 | 0 | 0 49 |
| C_5_5_3_SURFACE_IMPOUNDMENT | other | 1 | 0 | 0 49 |
| C_5_5_3A_RCRA_C_SURFACE_IMP | other | 1 | 0 | 0 49 |
| C_5_5_3B_OTHER_SURFACE_IMP | other | 1 | 0 | 0 49 |
| C_5_5_4_OTHER_DISPOSAL | other | 1 | 0 | 0 49 |
| ON_SITE_RELEASE_TOTAL | amount | 20 | 0 | 0 27; 2.29 2; 4.3899999999999997 2; 4.0999999999999996 2 |
| C_6_1_POTW_TRANSFERS_FOR_RELEASE | other | 1 | 0 | 0 49 |
| C_6_1_POTW_TRANSFERS_FOR_TREATM | category | 14 | 0 | 0 36; 19206 1; 18899 1; 19195 1 |
| C_6_1_POTW_TOTAL_TRANSFERS | other | 1 | 0 | 0 49 |
| C_6_2_M10 | other | 1 | 0 | 0 49 |
| C_6_2_M41 | other | 1 | 0 | 0 49 |
| C_6_2_M62 | other | 1 | 0 | 0 49 |
| C_6_2_M71 | other | 1 | 0 | 0 49 |
| C_6_2_M81 | other | 1 | 0 | 0 49 |
| C_6_2_M82 | other | 1 | 0 | 0 49 |
| C_6_2_M72 | other | 1 | 0 | 0 49 |
| C_6_2_M63 | other | 1 | 0 | 0 49 |
| C_6_2_M66 | other | 1 | 0 | 0 49 |
| C_6_2_M67 | other | 1 | 0 | 0 49 |
| C_6_2_M64 | amount | 21 | 0 | 0 29; 3.42 1; 8.0500000000000007 1; 12.98 1 |
| C_6_2_M65 | other | 1 | 0 | 0 49 |
| C_6_2_M73 | other | 1 | 0 | 0 49 |
| C_6_2_M79 | other | 1 | 0 | 0 49 |
| C_6_2_M90 | other | 1 | 0 | 0 49 |
| C_6_2_M94 | other | 1 | 0 | 0 49 |
| C_6_2_M99 | other | 1 | 0 | 0 49 |
| OFF_SITE_RELEASE_TOTAL | amount | 21 | 0 | 0 29; 3.42 1; 8.0500000000000007 1; 12.98 1 |
| C_6_2_M20 | other | 1 | 0 | 0 49 |
| C_6_2_M24 | other | 1 | 0 | 0 49 |
| C_6_2_M26 | other | 1 | 0 | 0 49 |
| C_6_2_M28 | other | 1 | 0 | 0 49 |
| C_6_2_M93 | other | 1 | 0 | 0 49 |
| OFF_SITE_RECYCLED_TOTAL | other | 1 | 0 | 0 49 |
| C_6_2_M56 | other | 1 | 0 | 0 49 |
| C_6_2_M92 | other | 1 | 0 | 0 49 |
| OFF_SITE_RECOVERY_TOTAL | other | 1 | 0 | 0 49 |
| C_6_2_M40 | other | 1 | 0 | 0 49 |
| C_6_2_M50 | other | 1 | 0 | 0 49 |
| C_6_2_M54 | other | 1 | 0 | 0 49 |
| C_6_2_M61 | other | 1 | 0 | 0 49 |
| C_6_2_M69 | other | 1 | 0 | 0 49 |
| C_6_2_M95 | other | 1 | 0 | 0 49 |
| OFF_SITE_TREATED_TOTAL | other | 1 | 0 | 0 49 |
| TOTAL_RELEASES | amount | 23 | 0 | 0 27; 5.71 1; 13.44 1; 21.67 1 |
| C_8_1_RELEASES | other | 1 | 0 | 0 49 |
| C_8_1A_ON_SITE_CONTAINED_REL | other | 1 | 0 | 0 49 |
| C_8_1B_ON_SITE_OTHER_RELEASES | amount | 21 | 0 | 0 27; 2.29 2; 4.3899999999999997 2; 5.39 1 |
| C_8_1C_OFF_SITE_CONTAINED_REL | amount | 21 | 0 | 0 29; 3.42 1; 8.0500000000000007 1; 12.98 1 |
| C_8_1D_OFF_SITE_OTHER_RELEASES | other | 1 | 0 | 0 49 |
| C_8_2_ENERGY_RECOVERY_ON_SITE | other | 1 | 0 | 0 49 |
| C_8_3_ENERGY_RECOVERY_OFF_SITE | other | 1 | 0 | 0 49 |
| C_8_4_RECYCLING_ON_SITE | other | 1 | 0 | 0 49 |
| C_8_5_RECYCLING_OFF_SITE | other | 1 | 0 | 0 49 |
| C_8_6_TREATMENT_ON_SITE | category | 13 | 0 | 0 37; 14055 1; 19512 1; 19201 1 |
| C_8_7_TREATMENT_OFF_SITE | category | 11 | 0 | 0 39; 19206 1; 18899 1; 19195 1 |
| PROD_WASTE_8_1_THRU_8_7 | amount | 38 | 0 | 0 12; 5.71 1; 13.44 1; 21.67 1 |
| PARENT_COMPANY_NAME | category | 3 | 0 | MURPHY BROWN LLC 29; DAIRY FARMERS OF AMERICA  18; SMITHFIELD BIOENERGY LLC 2 |
| PARENT_COMPANY_DB_NUMBER | category | 3 | 0 | 24847444 29; 29855640 18; nan 2 |
| LOCATION_1 | category | 3 | 0 | {"latitude": "38.38871",  29; {"latitude": "38.21091",  18; {"latitude": "38.21404",  2 |
| COMPUTED_REGION_9Z68_3KQ5 | other | 1 | 0 | 2968 49 |
| SIC_2 | category | 2 | 0 | nan 45; NA 4 |
| C_8_8_ONE_TIME_RELEASE | category | 2 | 0 | nan 44; 0 5 |
| C_8_9_PRODUCTION_RATIO | amount | 25 | 0 | nan 15; 0.99 3; 1.04 3; 0.98 3 |
| NAICS_2 | category | 2 | 0 | nan 43; 311513 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:08.81971 49 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2f1ac298-659c-49c9-9a2b-1 49 |
| SRC_SHA256 | who | 1 | 0 | c086e86458df01408b9b872d3 49 |
