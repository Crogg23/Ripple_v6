# PORTAL_SOC_UTAH_OPEN_DATA_P_F259CD7FC8

rows 2.0K  columns 97  scan 4.9s

roles: amount 36, audit 2, category 31, date 2, other 24, who 3

## when

DOC_CTRL_NUM
  2011      1.1K  ##############################
  2014       866  #######################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| C_5_1_FUGITIVE_AIR | 2.0K | 0 | 27.35 | 64.5K | 530.0K | 6.39M |
| C_5_2_STACK_AIR | 2.0K | 0 | 0 | 54.8K | 130.0K | 4.19M |
| C_5_5_3B_OTHER_SURFACE_IMP | 2.0K | 0 | 0 | 0 | 46 | 217.50 |
| C_5_5_4_OTHER_DISPOSAL | 2.0K | 0 | 0 | 0 | 6.3K | 31.4K |
| ON_SITE_RELEASE_TOTAL | 2.0K | 0 | 174 | 72.4K | 660.0K | 10.62M |
| C_6_1_POTW_TRANSFERS_FOR_RELEASE | 2.0K | 0 | 0 | 165.68 | 3.9K | 26.0K |

## who

CHEMICAL by rows
       144  TOLUENE
       125  XYLENE (MIXED ISOMERS)
        96  ETHYLBENZENE
        78  N-HEXANE
        78  BENZENE
        73  1,2,4-TRIMETHYLBENZENE
        66  CYCLOHEXANE
        58  LEAD
        54  POLYCYCLIC AROMATIC COMPOUNDS
        53  NAPHTHALENE
        49  STYRENE
        47  ETHYLENE GLYCOL
        45  SULFURIC ACID (1994 AND AFTER ACID AEROSOLS" ONLY)"
        44  LEAD COMPOUNDS
        43  METHYL ETHYL KETONE
        43  PROPYLENE
        40  METHANOL
        36  HYDROGEN FLUORIDE
        36  ETHYLENE
        35  MANGANESE

CHEMICAL by dollars
       3.29M       23 rows  1,1,1-TRICHLOROETHANE
      904.2K       18 rows  DICHLOROMETHANE
      576.8K       78 rows  N-HEXANE
      574.7K       14 rows  CHLORODIFLUOROMETHANE
      554.5K      144 rows  TOLUENE
      512.1K       15 rows  ACETONE
      498.1K      125 rows  XYLENE (MIXED ISOMERS)
      491.7K       43 rows  METHYL ETHYL KETONE
      487.3K       14 rows  1,1-DICHLORO-1-FLUOROETHANE
      372.4K       22 rows  MANGANESE COMPOUNDS
      295.6K       19 rows  PHENOL
      259.1K       78 rows  BENZENE
      205.8K       49 rows  STYRENE
      166.6K       33 rows  AMMONIA
      126.2K       66 rows  CYCLOHEXANE
      117.4K       47 rows  ETHYLENE GLYCOL
      113.4K       25 rows  CHROMIUM COMPOUNDS(EXCEPT CHROMITE ORE MINED IN THE TRANSVAA
       91.5K        3 rows  COPPER COMPOUNDS
       88.8K       43 rows  PROPYLENE
       87.4K       36 rows  HYDROGEN FLUORIDE

UNIT_OF_MEASURE by rows
      2.0K  Pounds

UNIT_OF_MEASURE by dollars
      10.62M     2.0K rows  Pounds

SRC_SHA256 by rows
      2.0K  97ba049efce74e2d9f4bbf8063101235826a38f0c15d4d298894f6a05ffc903d

SRC_SHA256 by dollars
      10.62M     2.0K rows  97ba049efce74e2d9f4bbf8063101235826a38f0c15d4d298894f6a05ffc

## who x when

CHEMICAL by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  1,1,1-TRICHLOROETHANE                     2014:3.29M
  1,1-DICHLORO-1-FLUOROETHANE               2011:310.6K 2014:176.8K
  1,2,4-TRIMETHYLBENZENE                    2011:19.9K 2014:39.3K
  ACETONE                                   2014:512.1K
  AMMONIA                                   2011:157.8K 2014:8.8K
  BENZENE                                   2011:151.5K 2014:107.6K
  CHLORODIFLUOROMETHANE                     2011:310.6K 2014:264.1K
  CHROMIUM COMPOUNDS(EXCEPT CHROMITE ORE M  2011:941 2014:112.4K
  COPPER COMPOUNDS                          2011:0 2014:91.5K
  CYCLOHEXANE                               2011:62.4K 2014:63.8K
  DICHLOROMETHANE                           2011:433.5K 2014:470.7K
  ETHYLBENZENE                              2011:33.7K 2014:31.7K
  ETHYLENE                                  2011:27.0K 2014:4.4K
  ETHYLENE GLYCOL                           2011:78.1K 2014:39.3K
  HYDROGEN FLUORIDE                         2011:35.8K 2014:51.6K
  LEAD                                      2011:2.6K 2014:838
  LEAD COMPOUNDS                            2011:1.4K 2014:6.1K
  MANGANESE                                 2011:1.5K 2014:33.6K
  MANGANESE COMPOUNDS                       2011:0 2014:372.4K
  METHANOL                                  2011:10.3K 2014:2.7K
  METHYL ETHYL KETONE                       2011:144.4K 2014:347.3K
  N-HEXANE                                  2011:383.9K 2014:192.9K
  NAPHTHALENE                               2011:3.7K 2014:6.2K
  PHENOL                                    2011:147.2K 2014:148.4K
  POLYCYCLIC AROMATIC COMPOUNDS             2011:269.47
  PROPYLENE                                 2011:48.9K 2014:39.9K
  STYRENE                                   2011:101.8K 2014:104.0K
  SULFURIC ACID (1994 AND AFTER ACID AEROS  2014:9.4K
  TOLUENE                                   2011:274.3K 2014:280.2K
  XYLENE (MIXED ISOMERS)                    2011:248.3K 2014:249.8K

UNIT_OF_MEASURE by DOC_CTRL_NUM, dollars = ON_SITE_RELEASE_TOTAL
  Pounds                                    2011:3.17M 2014:7.45M

## what

YEAR: 2002 10%, 2003 10%, 2006 9%, 2007 9%, 2004 9%, 2005 9%, 2000 9%, 2001 8%, 1999 8%, 1998 8%, 1994 6%, 1996 6%

TRI_FACILITY_ID: 84087PHLLP393SO 23%, 84054BGWST333WE 18%, 84087CRYSN2355S 11%, 84056SRFRC7274W 10%, 84054CNCNR245E1 8%, 84016SHLNDFREEP 6%, 84087VLLYP727SO 5%, 84087CHMCN2465S 4%, 84014SYRST950WE 4%, 84016LFTMPBUILD 4%, 84015NPTCH851SF 4%, 84016FTRHMBLDGH 4%

FACILITY_NAME: HOLLY REFINING & MARKETING CO  23%, BIG WEST OIL LLC 18%, SILVER EAGLE REFINING WOODS CR 11%, US DOD USAF HILL AFB 10%, PHILLIPS 66 CO  NORTH SALT LAK 8%, NEXEO SOLUTIONS LLC - CLEARFIE 6%, VALLEY PAINT MANUFACTURING 5%, CHEMCENTRAL/SALT LAKE CITY 4%, TRINITY HIGHWAY PRODUCTS LLC P 4%, LIFETIME PRODUCTS INC 4%, SHAW NAPTECH INC 4%, FUTURA INDUSTRIES 4%

STREET_ADDRESS: 393 S 800 W 23%, 333 W CENTER ST 18%, 2355 S 1100 W 11%, 6044 DOGWOOD AVE 10%, 245 E 1100 N 8%, FREEPORT CENTER BUILDING 12 PO 6%, 727 S 950 W 5%, 2465 S 1100 W 4%, 950 W 400 S 4%, FREEPORT CENTER BUILDING D-11 4%, 210 E 700 S ST 4%, BUILDING H-11 FREEPORT CENTER 4%

FEDERAL_FACILITY: NO 92%, YES 8%

PRIMARY_SIC: 2911 39%, nan 18%, 5169 8%, 5171 7%, 9711 7%, 3949 4%, 2851 3%, 2951 3%, 3354 3%, 3715 3%, 3469 2%, 3441 2%

SIC_2: nan 65%, NA 27%, 3479 2%, 3471 2%, 4581 1%, 3084 0%, 2026 0%, NA34 0%, 5171 0%, 3441 0%, 5032 0%, 1442 0%

SIC_3: nan 97%, NA 2%, 3471 1%, 71 0%

PRIMARY_NAICS: 324110 46%, 424710 10%, 424690 9%, 928110 8%, 339920 4%, 325510 4%, 332312 3%, 324121 3%, 331316 3%, 336212 3%, 332116 3%, 332996 3%

CLEAR_AIR_ACT_CHEMICAL: YES 71%, NO 29%

CLASSIFICATION: TRI 93%, PBT 7%

METAL: NO 84%, YES 16%

METAL_CATEGORY: 0 82%, 1 16%, 2 1%, 3 0%

CARCINOGEN: NO 80%, YES 20%

FORM_TYPE: R 86%, A 14%

C_5_3_WATER: 0 99%, 1 0%, 3 0%, 14 0%, 6 0%, 64 0%, 28 0%, 60 0%, 27 0%, 19 0%, 43 0%, 750 0%

C_5_5_1B_OTHER_LANDFILLS: 0 100%, 3 0%

C_5_5_2_LAND_TREATMENT: 0 100%, 250 0%, 750 0%, 10 0%

C_6_2_M10: 0 99%, 3 0%, 1 0%, 12000 0%, 19 0%, 44 0%, 26 0%, 17 0%, 5 0%, 180 0%, 27 0%, 140 0%

C_6_2_M62: 0 100%, 260 0%

C_6_2_M71: 0 100%, 5 0%, 250 0%, 1 0%

C_6_2_M92: 0 99%, 5 0%, 1300 0%, 2 0%, 500 0%, 6523 0%, 39 0%, 67 0%, 2530 0%, 155 0%, 662 0%, 9 0%

C_6_2_M40: 0 99%, 5 1%, 4 0%, 18 0%, 57910 0%, 30 0%, 2346 0%

C_6_2_M95: 0 99%, 5 0%, 10 0%, 500 0%, 18500 0%, 17005 0%, 11100 0%, 250 0%, 1000 0%, 255 0%, 2250 0%, 14600 0%

PARENT_COMPANY_NAME: NA 21%, HOLLY CORP 20%, FJ MANAGEMENT 16%, THE INTERNATIONAL GROUP INC. 10%, US DEPARTMENT OF DEFENSE 9%, PHILLIPS 66 CO 7%, CHEMCENTRAL COPORATION 4%, TRINITY INDUSTRIES INC 3%, THE SHAW GROUP INC 3%, FUTURA CORP 3%, THOMAS PETROLEUM LLC 3%, THE KROGER CO 2%

PARENT_COMPANY_DB_NUMBER: NA 44%, 8965808 19%, 2358455 9%, 78378508 6%, 6929095 3%, 41075896 3%, 1.80E+08 3%, 37791530 3%, 8286908 3%, 39846068 3%, 43700194 2%, 72955826 2%

LOCATION_1: {"latitude": "40.88405", "long 21%, {"latitude": "40.83839", "long 17%, {"latitude": "41.08962", "long 12%, {"latitude": "40.86639", "long 10%, {"latitude": "41.12833", "long 9%, {"latitude": "40.86162", "long 7%, {"latitude": "41.08962", "long 5%, {"latitude": "40.88321", "long 4%, {"latitude": "40.86359", "long 4%, {"latitude": "40.91309", "long 4%, {"latitude": "41.10161", "long 3%, {"latitude": "40.86053", "long 3%

SIC_4: nan 99%, 3479 1%

SIC_5: nan 99%, 3728 1%

SIC_6: nan 99%, 3769 1%

NAICS_2: nan 99%, 331210 0%, 332813 0%, 327320 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 19 | 0 | 2002 147; 2003 144; 2006 141; 2007 138 |
| TRI_FACILITY_ID | category | 42 | 0 | 84087PHLLP393SO 344; 84054BGWST333WE 278; 84087CRYSN2355S 168; 84056SRFRC7274W 155 |
| FACILITY_NAME | category | 41 | 0 | HOLLY REFINING & MARKETIN 344; BIG WEST OIL LLC 278; SILVER EAGLE REFINING WOO 168; US DOD USAF HILL AFB 155 |
| STREET_ADDRESS | category | 41 | 0 | 393 S 800 W 344; 333 W CENTER ST 278; 2355 S 1100 W 168; 6044 DOGWOOD AVE 155 |
| COUNTY | other | 1 | 0 | DAVIS 2.0K |
| ST | other | 1 | 0 | UT 2.0K |
| FEDERAL_FACILITY | category | 2 | 0 | NO 1.8K; YES 155 |
| PRIMARY_SIC | category | 32 | 0 | 2911 678; nan 314; 5169 142; 5171 121 |
| SIC_2 | category | 12 | 0 | nan 1.3K; NA 544; 3479 46; 3471 39 |
| SIC_3 | category | 4 | 0 | nan 1.9K; NA 44; 3471 16; 71 8 |
| PRIMARY_NAICS | category | 39 | 0 | 324110 790; 424710 168; 424690 161; 928110 139 |
| DOC_CTRL_NUM | date | 4 | 0 | 1300000000000 681; 1400000000000 465; 1310000000000 441; 1390000000000 401 |
| CHEMICAL | who | 84 | 0 | TOLUENE 144; XYLENE (MIXED ISOMERS) 125; ETHYLBENZENE 96; N-HEXANE 78 |
| CAS_COMPOUND_ID | other | 69 | 0 | nan 278; 108883 144; 1330207 125; 100414 96 |
| CLEAR_AIR_ACT_CHEMICAL | category | 2 | 0 | YES 1.4K; NO 569 |
| CLASSIFICATION | category | 2 | 0 | TRI 1.8K; PBT 148 |
| METAL | category | 2 | 0 | NO 1.7K; YES 322 |
| METAL_CATEGORY | category | 4 | 0 | 0 1.6K; 1 322; 2 22; 3 6 |
| CARCINOGEN | category | 2 | 0 | NO 1.6K; YES 403 |
| FORM_TYPE | category | 2 | 0 | R 1.7K; A 273 |
| UNIT_OF_MEASURE | who | 1 | 0 | Pounds 2.0K |
| C_5_1_FUGITIVE_AIR | amount | 691 | 0 | 0 707; 250 117; 5 74; 1 26 |
| C_5_2_STACK_AIR | amount | 569 | 0 | 0 1.0K; 250 85; 5 35; 750 32 |
| C_5_3_WATER | category | 13 | 0 | 0 2.0K; 1 4; 3 2; 14 1 |
| C_5_4_1_UNDERGROUND_CLASS_I | other | 1 | 0 | 0 2.0K |
| C_5_4_2_UNDERGROUND_CLASS_II_V | other | 1 | 0 | 0 2.0K |
| C_5_5_1A_RCRA_C_LANDFILLS | other | 1 | 0 | 0 2.0K |
| C_5_5_1B_OTHER_LANDFILLS | category | 2 | 0 | 0 2.0K; 3 1 |
| C_5_5_2_LAND_TREATMENT | category | 4 | 0 | 0 2.0K; 250 5; 750 3; 10 1 |
| C_5_5_3_SURFACE_IMPOUNDMENT | other | 1 | 0 | 0 2.0K |
| C_5_5_3A_RCRA_C_SURFACE_IMP | other | 1 | 0 | 0 2.0K |
| C_5_5_3B_OTHER_SURFACE_IMP | amount | 7 | 0 | 0 2.0K; 29 1; 46 1; 44.78 1 |
| C_5_5_4_OTHER_DISPOSAL | amount | 17 | 0 | 0 2.0K; 0.1 2; 19 2; 1345 1 |
| ON_SITE_RELEASE_TOTAL | amount | 959 | 0 | 0 562; 250 34; 500 34; 5 28 |
| C_6_1_POTW_TRANSFERS_FOR_RELEASE | amount | 45 | 0 | 0 1.9K; 5 8; 250 6; 8.4 2 |
| C_6_1_POTW_TRANSFERS_FOR_TREATM | other | 257 | 0 | 0 1.5K; 250 43; 750 27; 5 20 |
| C_6_1_POTW_TOTAL_TRANSFERS | amount | 45 | 0 | 0 1.9K; 5 8; 250 6; 8.4 2 |
| C_6_2_M10 | category | 19 | 0 | 0 2.0K; 3 3; 1 3; 12000 2 |
| C_6_2_M41 | amount | 18 | 0 | 0 2.0K; 1 3; 767 3; 10.9 1 |
| C_6_2_M62 | category | 2 | 0 | 0 2.0K; 260 1 |
| C_6_2_M71 | category | 4 | 0 | 0 2.0K; 5 3; 250 2; 1 1 |
| C_6_2_M81 | other | 1 | 0 | 0 2.0K |
| C_6_2_M82 | other | 1 | 0 | 0 2.0K |
| C_6_2_M72 | amount | 52 | 0 | 0 1.9K; 250 17; 5 6; 1 3 |
| C_6_2_M63 | amount | 4 | 0 | 0 2.0K; 3.8 1; 1.8 1; 30000 1 |
| C_6_2_M66 | other | 1 | 0 | 0 2.0K |
| C_6_2_M67 | other | 1 | 0 | 0 2.0K |
| C_6_2_M64 | amount | 50 | 0 | 0 1.9K; 0.1 5; 750 2; 14 2 |
| C_6_2_M65 | amount | 32 | 0 | 0 2.0K; 5 2; 3.6 2; 1 2 |
| C_6_2_M73 | amount | 34 | 0 | 0 2.0K; 0.183 1; 0.22 1; 3.7189999999999999 1 |
| C_6_2_M79 | amount | 7 | 0 | 0 2.0K; 5 6; 21.8 1; 5.3 1 |
| C_6_2_M90 | amount | 5 | 0 | 0 2.0K; 0.084000000000000005 1; 750 1; 255 1 |
| C_6_2_M94 | amount | 29 | 0 | 0 2.0K; 5 4; 3.1 2; 270 1 |
| C_6_2_M99 | amount | 100 | 0 | 0 1.9K; 3 2; 250 2; 505 2 |
| OFF_SITE_RELEASE_TOTAL | amount | 241 | 0 | 0 1.7K; 250 20; 5 18; 1 6 |
| C_6_2_M20 | amount | 9 | 0 | 0 2.0K; 5 10; 8 3; 7 3 |
| C_6_2_M24 | amount | 103 | 0 | 0 1.9K; 55966 2; 4963 1; 849.2 1 |
| C_6_2_M26 | amount | 58 | 0 | 0 1.9K; 2 4; 4 3; 9 2 |
| C_6_2_M28 | other | 1 | 0 | 0 2.0K |
| C_6_2_M93 | amount | 33 | 0 | 0 2.0K; 15 2; 22000 2; 761 1 |
| OFF_SITE_RECYCLED_TOTAL | amount | 195 | 0 | 0 1.8K; 5 10; 2 5; 7 5 |
| C_6_2_M56 | amount | 103 | 0 | 0 1.9K; 250 12; 5 5; 500 3 |
| C_6_2_M92 | category | 26 | 0 | 0 2.0K; 5 6; 1300 3; 2 2 |
| OFF_SITE_RECOVERY_TOTAL | amount | 124 | 0 | 0 1.8K; 250 6; 255 6; 5 5 |
| C_6_2_M40 | category | 7 | 0 | 0 2.0K; 5 15; 4 1; 18 1 |
| C_6_2_M50 | other | 155 | 0 | 0 1.8K; 5 18; 250 13; 2 11 |
| C_6_2_M54 | amount | 44 | 0 | 0 1.9K; 5 12; 1 7; 2 3 |
| C_6_2_M61 | amount | 21 | 0 | 0 2.0K; 250 6; 750 4; 0.2 2 |
| C_6_2_M69 | other | 59 | 0 | 0 1.9K; 1 4; 7 3; 13 2 |
| C_6_2_M95 | category | 14 | 0 | 0 2.0K; 5 2; 10 2; 500 2 |
| OFF_SITE_TREATED_TOTAL | amount | 223 | 0 | 0 1.6K; 5 21; 1 16; 250 14 |
| TOTAL_RELEASES | amount | 1.0K | 0 | 0 512; 250 30; 500 27; 5 26 |
| C_8_1_RELEASES | other | 630 | 0 | 0 1.1K; 20 11; 15 11; 10000 7 |
| C_8_1A_ON_SITE_CONTAINED_REL | other | 1 | 0 | 0 2.0K |
| C_8_1B_ON_SITE_OTHER_RELEASES | amount | 394 | 0 | 0 1.5K; 0.1 10; 1 9; 4 7 |
| C_8_1C_OFF_SITE_CONTAINED_REL | amount | 67 | 0 | 0 1.9K; 4 3; 750 2; 14 2 |
| C_8_1D_OFF_SITE_OTHER_RELEASES | amount | 86 | 0 | 0 1.9K; 3 2; 3.1 2; 7499 2 |
| C_8_2_ENERGY_RECOVERY_ON_SITE | other | 55 | 0 | 0 1.9K; 34000 5; 1 3; 10258 2 |
| C_8_3_ENERGY_RECOVERY_OFF_SITE | amount | 138 | 0 | 0 1.8K; 1 7; 1300 4; 2 3 |
| C_8_4_RECYCLING_ON_SITE | amount | 379 | 0 | 0 1.5K; 68 8; 1 7; 3100 7 |
| C_8_5_RECYCLING_OFF_SITE | other | 193 | 0 | 0 1.8K; 5 9; 7 5; 2 4 |
| C_8_6_TREATMENT_ON_SITE | other | 258 | 0 | 0 1.7K; 13000 5; 3801 5; 16000 4 |
| C_8_7_TREATMENT_OFF_SITE | other | 372 | 0 | 0 1.4K; 1 13; 2 9; 11 7 |
| PROD_WASTE_8_1_THRU_8_7 | amount | 1.4K | 0 | 0 446; 0.1 16; 1 11; 15 11 |
| PARENT_COMPANY_NAME | category | 31 | 0 | NA 360; HOLLY CORP 344; FJ MANAGEMENT 278; THE INTERNATIONAL GROUP I 168 |
| PARENT_COMPANY_DB_NUMBER | category | 25 | 0 | NA 824; 8965808 344; 2358455 168; 78378508 117 |
| LOCATION_1 | category | 35 | 0 | {"latitude": "40.88405",  344; {"latitude": "40.83839",  278; {"latitude": "41.08962",  193; {"latitude": "40.86639",  168 |
| COMPUTED_REGION_9Z68_3KQ5 | other | 1 | 0 | 811 2.0K |
| C_8_8_ONE_TIME_RELEASE | other | 94 | 0 | nan 1.0K; 0 831; 1 13; 2 8 |
| C_8_9_PRODUCTION_RATIO | amount | 160 | 0 | nan 374; 1 245; 0 132; 1.02 82 |
| SIC_4 | category | 2 | 0 | nan 2.0K; 3479 16 |
| SIC_5 | category | 2 | 0 | nan 2.0K; 3728 16 |
| SIC_6 | category | 2 | 0 | nan 2.0K; 3769 16 |
| NAICS_2 | category | 4 | 0 | nan 2.0K; 331210 8; 332813 6; 327320 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:39:03.95218 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b1a99f8a-32cd-489a-b987-4 2.0K |
| SRC_SHA256 | who | 1 | 0 | 97ba049efce74e2d9f4bbf806 2.0K |
