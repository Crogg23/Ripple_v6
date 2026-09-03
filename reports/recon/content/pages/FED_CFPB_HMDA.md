# FED_CFPB_HMDA

rows 28.3K  columns 102  scan 5.9s

roles: amount 16, audit 2, category 70, empty 3, other 7, who 4

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LOAN_AMOUNT | 28.3K | 5.0K | 415.0K | 2.78M | 216.21M | 17.75B |
| LOAN_TO_VALUE_RATIO | 17.9K | 0.05 | 75.47 | 103.59 | 1.9K | 1.29M |
| INTEREST_RATE | 18.8K | 0 | 4.25 | 8.75 | 13.75 | 84.0K |
| RATE_SPREAD | 13.3K | -7.17 | 0.09 | 3.93 | 100 | 1.8K |
| TOTAL_LOAN_COSTS | 14.9K | 0 | 7.0K | 36.6K | 81.1K | 136.18M |
| TOTAL_POINTS_AND_FEES | 31 | 0 | 1.5K | 26.1K | 27.0K | 145.6K |

## who

TRACT_OWNER_OCCUPIED_UNITS by rows
       479  0
       424  999
       396  876
       395  1911
       383  911
       380  666
       374  1139
       348  1070
       340  839
       311  1452
       308  902
       307  1097
       306  494
       301  466
       294  1415
       291  945
       282  532
       281  633
       268  457
       263  471

TRACT_OWNER_OCCUPIED_UNITS by dollars
     451.97M      202 rows  284
     424.80M      479 rows  0
     286.83M      395 rows  1911
     264.68M      231 rows  1328
     256.21M      340 rows  839
     251.95M      374 rows  1139
     248.30M      268 rows  457
     239.18M      396 rows  876
     238.92M      424 rows  999
     236.29M      168 rows  1014
     233.23M      184 rows  1089
     224.72M      281 rows  633
     196.91M      165 rows  556
     193.59M      236 rows  1353
     192.97M      225 rows  892
     192.63M      232 rows  1509
     189.59M      308 rows  902
     183.40M      212 rows  1124
     181.72M      230 rows  1195
     175.98M      380 rows  666

LEI by rows
      1.4K  JJKC32MCHWDI71265Z06
      1.3K  KB1H1DSPRFMYMCUFXT09
      1.0K  B4TYDEB6GKMZO031MB27
       897  549300FGXN1K3HLB1R50
       896  549300CF8MP6S7MZV277
       887  AD6GFRVSDT01YPT1CS68
       807  549300J7XKT2BI5WX213
       787  5493003GQDUH26DNNH17
       735  03D0JEWFDFUS0SEEKG89
       670  549300GPO6DWUZR4UY30
       599  7H6GLXDRUGQFU57RNE97
       517  549300FNXYY540N23N64
       496  549300FX7K8PTEQUU487
       460  2549006II76YXSS5XM65
       458  HIDXEG9BLUJZKBGUT764
       430  5493005PKOSG7MYX0B34
       414  RVDPPPGHCGZ40J4VQ731
       402  E57ODZWZ7FF32TWEFA76
       378  549300NQA30MEKPQP417
       361  6BYL5QZYBDK8S7L73M02

LEI by dollars
     929.61M     1.3K rows  KB1H1DSPRFMYMCUFXT09
     909.91M     1.4K rows  JJKC32MCHWDI71265Z06
     698.60M       15 rows  KD3XUN7C6T14HNAYLU02
     684.02M      599 rows  7H6GLXDRUGQFU57RNE97
     623.33M      896 rows  549300CF8MP6S7MZV277
     539.21M      887 rows  AD6GFRVSDT01YPT1CS68
     483.77M     1.0K rows  B4TYDEB6GKMZO031MB27
     480.44M      735 rows  03D0JEWFDFUS0SEEKG89
     422.48M      402 rows  E57ODZWZ7FF32TWEFA76
     391.44M      807 rows  549300J7XKT2BI5WX213
     360.83M      897 rows  549300FGXN1K3HLB1R50
     337.75M      181 rows  WVM1F03F86RQLLTEVE84
     337.24M      670 rows  549300GPO6DWUZR4UY30
     311.17M        8 rows  549300DH8EI64ITBY388
     301.30M      460 rows  2549006II76YXSS5XM65
     259.58M      430 rows  5493005PKOSG7MYX0B34
     258.71M       42 rows  2549009GDCGUR2T6KU55
     250.88M      787 rows  5493003GQDUH26DNNH17
     241.06M       71 rows  254900SOAE0WU8JM0177
     236.66M      458 rows  HIDXEG9BLUJZKBGUT764

CENSUS_TRACT by rows
       395  11001001500
       380  11001008802
       348  11001002101
       311  11001009400
       308  11001003200
       307  11001011100
       294  11001001600
       291  11001007601
       268  11001008702
       261  11001009000
       255  11001002400
       252  11001002102
       249  11001009509
       241  11001002900
       240  11001003301
       238  11001007901
       236  11001000300
       236  11001001901
       236  11001009504
       234  11001010400

CENSUS_TRACT by dollars
     423.56M      109 rows  11001004702
     286.83M      395 rows  11001001500
     264.68M      231 rows  11001000202
     248.30M      268 rows  11001008702
     236.29M      168 rows  11001000804
     233.23M      184 rows  11001000102
     217.78M        5 rows  11001010603
     196.91M      165 rows  11001007100
     193.59M      236 rows  11001000300
     192.97M      225 rows  11001005202
     192.63M      232 rows  11001000600
     189.59M      308 rows  11001003200
     183.40M      212 rows  11001009301
     181.72M      230 rows  11001001100
     176.14M      212 rows  11001002702
     175.98M      380 rows  11001008802
     174.60M      214 rows  11001010602
     169.98M      294 rows  11001001600
     166.30M      124 rows  11001005503
     166.05M      160 rows  11001000902

_SRC_SHA256 by rows
     28.3K  68e928049b3664f47f90a2abdc0f823828cd5bd1dcd024c4ddaad6fb75ef6a36

_SRC_SHA256 by dollars
      17.75B    28.3K rows  68e928049b3664f47f90a2abdc0f823828cd5bd1dcd024c4ddaad6fb75ef

## what

DERIVED_MSA_MD: 47894 98%, 99999 2%

COUNTY_CODE: 11001 100%

CONFORMING_LOAN_LIMIT: C 90%, NC 10%

DERIVED_LOAN_PRODUCT_TYPE: Conventional:First Lien 74%, Conventional:Subordinate Lien 15%, FHA:First Lien 6%, VA:First Lien 4%, FHA:Subordinate Lien 0%, FSA/RHS:Subordinate Lien 0%

DERIVED_DWELLING_CATEGORY: Single Family (1-4 Units):Site 99%, Multifamily:Site-Built 1%, Single Family (1-4 Units):Manu 0%

DERIVED_ETHNICITY: Not Hispanic or Latino 61%, Ethnicity Not Available 33%, Hispanic or Latino 5%, Joint 2%, Free Form Text Only 0%

DERIVED_RACE: White 34%, Race Not Available 34%, Black or African American 24%, Asian 5%, Joint 3%, 2 or more minority races 0%, American Indian or Alaska Nati 0%, Native Hawaiian or Other Pacif 0%, Free Form Text Only 0%

DERIVED_SEX: Female 27%, Male 27%, Sex Not Available 25%, Joint 21%

ACTION_TAKEN: 1 51%, 6 15%, 3 14%, 4 14%, 5 4%, 2 2%, 8 0%, 7 0%

PURCHASER_TYPE: 0 61%, 1 11%, 3 9%, 6 7%, 71 6%, 2 3%, 8 2%, 9 1%, 5 1%, 72 0%

PREAPPROVAL: 2 98%, 1 2%

LOAN_TYPE: 1 90%, 2 6%, 3 4%, 4 0%

LOAN_PURPOSE: 1 51%, 32 19%, 31 14%, 2 9%, 4 6%, 5 0%

LIEN_STATUS: 1 85%, 2 15%

REVERSE_MORTGAGE: 2 98%, 1111 1%, 1 1%

OPEN_END_LINE_OF_CREDIT: 2 84%, 1 15%, 1111 1%

BUSINESS_OR_COMMERCIAL_PURPOSE: 2 92%, 1 7%, 1111 1%

HOEPA_STATUS: 2 57%, 3 43%, 1 0%

INTRO_RATE_PERIOD: 1 46%, 84 15%, 120 14%, 60 9%, 6 4%, Exempt 4%, 3 4%, 12 1%, 180 1%, 36 1%, 2 1%

NEGATIVE_AMORTIZATION: 2 99%, 1111 1%, 1 0%

OTHER_NONAMORTIZING_FEATURES: 2 99%, 1111 1%, 1 0%

CONSTRUCTION_METHOD: 1 100%, 2 0%

OCCUPANCY_TYPE: 1 87%, 3 11%, 2 2%

MANUFACTURED_HOME_SECURED_PROPERTY_TYPE: 3 99%, 1111 1%, 1 0%

MANUFACTURED_HOME_LAND_PROPERTY_INTEREST: 5 99%, 1111 1%, 1 0%

TOTAL_UNITS: 1 94%, 2 3%, 4 1%, 5-24 1%, 3 0%, 25-49 0%, 50-99 0%, >149 0%, 100-149 0%

MULTIFAMILY_AFFORDABLE_UNITS: Exempt 53%, 0 30%, 100 14%, 8 1%, 80 1%, 87 0%, 64 0%, 3 0%, 75 0%, 57 0%, 58 0%

DEBT_TO_INCOME_RATIO: 20%-<30% 25%, 30%-<36% 22%, <20% 11%, 50%-60% 8%, >60% 7%, 42 5%, 40 4%, 44 4%, 39 4%, 43 4%, 41 4%

APPLICANT_CREDIT_SCORE_TYPE: 9 39%, 1 22%, 2 16%, 3 16%, 8 3%, 7 2%, 1111 1%, 11 1%, 6 0%, 5 0%, 4 0%

CO_APPLICANT_CREDIT_SCORE_TYPE: 9 45%, 10 44%, 1 4%, 3 3%, 2 3%, 1111 1%, 8 1%, 7 0%, 11 0%, 6 0%, 4 0%, 5 0%

APPLICANT_ETHNICITY_1: 2 62%, 3 18%, 4 15%, 1 5%, 14 0%, 12 0%, 11 0%, 13 0%

APPLICANT_ETHNICITY_2: 14 53%, 11 25%, 12 14%, 13 4%, 2 3%, 1 1%

APPLICANT_ETHNICITY_3: 14 40%, 12 20%, 13 20%, 11 16%, 1 4%

APPLICANT_ETHNICITY_4: 13 100%

APPLICANT_ETHNICITY_5: 14 100%

CO_APPLICANT_ETHNICITY_1: 5 61%, 2 20%, 4 12%, 3 6%, 1 2%, 14 0%, 11 0%, 12 0%, 13 0%

CO_APPLICANT_ETHNICITY_2: 14 54%, 11 26%, 12 13%, 13 6%, 2 1%

CO_APPLICANT_ETHNICITY_3: 14 40%, 11 20%, 13 20%, 12 20%

APPLICANT_ETHNICITY_OBSERVED: 2 79%, 3 19%, 1 2%

CO_APPLICANT_ETHNICITY_OBSERVED: 4 61%, 2 26%, 3 13%, 1 0%

APPLICANT_RACE_1: 5 36%, 3 24%, 6 19%, 7 15%, 2 4%, 1 1%, 21 1%, 27 0%, 22 0%, 4 0%, 23 0%, 25 0%

APPLICANT_RACE_2: 21 23%, 5 22%, 22 15%, 27 12%, 25 8%, 3 7%, 23 6%, 26 4%, 24 2%, 2 1%, 44 1%

APPLICANT_RACE_3: 5 19%, 23 17%, 22 15%, 27 14%, 24 12%, 21 9%, 25 8%, 3 3%, 42 1%, 44 1%, 2 1%

APPLICANT_RACE_4: 23 20%, 44 20%, 22 20%, 4 10%, 27 10%, 26 10%, 5 10%

APPLICANT_RACE_5: 5 20%, 24 20%, 25 20%, 27 20%, 44 20%

CO_APPLICANT_RACE_1: 8 61%, 5 15%, 7 12%, 6 6%, 3 4%, 2 1%, 21 0%, 1 0%, 27 0%, 22 0%, 4 0%, 24 0%

CO_APPLICANT_RACE_2: 21 27%, 5 20%, 22 17%, 27 12%, 25 7%, 23 7%, 26 5%, 3 3%, 24 1%, 2 1%, 44 1%

CO_APPLICANT_RACE_3: 25 23%, 24 19%, 22 14%, 23 9%, 5 9%, 21 7%, 44 7%, 27 5%, 42 2%, 4 2%, 2 2%

CO_APPLICANT_RACE_4: 25 60%, 5 20%, 22 20%

APPLICANT_RACE_OBSERVED: 2 79%, 3 19%, 1 2%

CO_APPLICANT_RACE_OBSERVED: 4 61%, 2 26%, 3 13%, 1 0%

APPLICANT_SEX: 1 41%, 2 34%, 4 15%, 3 10%, 6 0%

CO_APPLICANT_SEX: 5 61%, 2 15%, 4 12%, 1 9%, 3 3%, 6 0%

APPLICANT_SEX_OBSERVED: 2 79%, 3 19%, 1 2%

CO_APPLICANT_SEX_OBSERVED: 4 61%, 2 26%, 3 13%, 1 0%

APPLICANT_AGE: 35-44 26%, 25-34 19%, 45-54 17%, 8888 15%, 55-64 12%, 65-74 7%, >74 3%, <25 1%

CO_APPLICANT_AGE: 9999 60%, 8888 12%, 35-44 9%, 25-34 7%, 45-54 5%, 55-64 3%, 65-74 2%, >74 1%, <25 0%

APPLICANT_AGE_ABOVE_62: No 84%, Yes 16%

CO_APPLICANT_AGE_ABOVE_62: No 87%, Yes 13%

SUBMISSION_OF_APPLICATION: 1 79%, 3 15%, 2 6%, 1111 1%

AUS_1: 6 46%, 1 31%, 2 14%, 7 3%, 3 3%, 5 2%, 1111 1%

AUS_2: 1 53%, 2 36%, 7 6%, 5 4%, 3 1%

AUS_3: 1 58%, 2 35%, 5 6%, 3 1%

AUS_4: 1 79%, 2 20%, 3 1%

AUS_5: 1 80%, 2 19%, 3 1%

DENIAL_REASON_1: 10 85%, 1 4%, 3 3%, 4 2%, 7 2%, 9 1%, 1111 1%, 6 1%, 5 0%, 2 0%, 8 0%

DENIAL_REASON_2: 9 21%, 3 18%, 4 17%, 1 16%, 6 11%, 7 7%, 5 6%, 2 3%, 8 0%

DENIAL_REASON_3: 9 36%, 4 17%, 6 17%, 5 14%, 1 6%, 3 6%, 7 4%

DENIAL_REASON_4: 9 62%, 6 25%, 4 12%

FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME: 139700 98%, 0 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACTIVITY_YEAR | other | 1 | 0 | 2022 28.3K |
| LEI | who | 531 | 0 | JJKC32MCHWDI71265Z06 1.4K; KB1H1DSPRFMYMCUFXT09 1.3K; B4TYDEB6GKMZO031MB27 1.0K; 549300CF8MP6S7MZV277 912 |
| DERIVED_MSA_MD | category | 2 | 0 | 47894 27.8K; 99999 460 |
| STATE_CODE | other | 1 | 0 | DC 28.3K |
| COUNTY_CODE | category | 2 | 465 | 11001 27.8K |
| CENSUS_TRACT | who | 208 | 463 | 11001001500 395; 11001008802 380; 11001002101 348; 11001009400 311 |
| CONFORMING_LOAN_LIMIT | category | 3 | 291 | C 25.3K; NC 2.7K |
| DERIVED_LOAN_PRODUCT_TYPE | category | 6 | 0 | Conventional:First Lien 21.0K; Conventional:Subordinate  4.4K; FHA:First Lien 1.8K; VA:First Lien 1.2K |
| DERIVED_DWELLING_CATEGORY | category | 3 | 0 | Single Family (1-4 Units) 28.0K; Multifamily:Site-Built 291; Single Family (1-4 Units) 3 |
| DERIVED_ETHNICITY | category | 5 | 0 | Not Hispanic or Latino 17.2K; Ethnicity Not Available 9.2K; Hispanic or Latino 1.3K; Joint 604 |
| DERIVED_RACE | category | 9 | 0 | White 9.7K; Race Not Available 9.6K; Black or African American 6.7K; Asian 1.3K |
| DERIVED_SEX | category | 4 | 0 | Female 7.8K; Male 7.7K; Sex Not Available 7.0K; Joint 5.8K |
| ACTION_TAKEN | category | 8 | 0 | 1 14.3K; 6 4.2K; 3 4.0K; 4 4.0K |
| PURCHASER_TYPE | category | 10 | 0 | 0 17.3K; 1 3.0K; 3 2.5K; 6 1.9K |
| PREAPPROVAL | category | 2 | 0 | 2 27.7K; 1 569 |
| LOAN_TYPE | category | 4 | 0 | 1 25.3K; 2 1.8K; 3 1.2K; 4 2 |
| LOAN_PURPOSE | category | 6 | 0 | 1 14.5K; 32 5.4K; 31 4.0K; 2 2.5K |
| LIEN_STATUS | category | 2 | 0 | 1 23.9K; 2 4.4K |
| REVERSE_MORTGAGE | category | 3 | 0 | 2 27.8K; 1111 251; 1 218 |
| OPEN_END_LINE_OF_CREDIT | category | 3 | 0 | 2 23.7K; 1 4.3K; 1111 251 |
| BUSINESS_OR_COMMERCIAL_PURPOSE | category | 3 | 0 | 2 26.1K; 1 1.9K; 1111 251 |
| LOAN_AMOUNT | amount | 454 | 0 | 105000.0 714; 205000.0 671; 255000.0 662; 305000.0 610 |
| LOAN_TO_VALUE_RATIO | amount | 8.2K | 10.2K | 80.0 1.8K; 95.0 900; 75.0 801; 90.0 639 |
| INTEREST_RATE | amount | 780 | 9.2K | 3.25 718; 3.75 689; 3.875 604; 4.25 584 |
| RATE_SPREAD | amount | 4.0K | 14.7K | Exempt 250; -0.227 69; -0.451 68; -0.237 68 |
| HOEPA_STATUS | category | 3 | 0 | 2 16.2K; 3 12.1K; 1 8 |
| TOTAL_LOAN_COSTS | amount | 11.5K | 13.1K | 0.0 277; Exempt 257; 437.75 79; 872.75 78 |
| TOTAL_POINTS_AND_FEES | amount | 29 | 28.0K | Exempt 257; 0.0 5; 10220.7 1; 1790.0 1 |
| ORIGINATION_CHARGES | amount | 6.5K | 13.1K | 0.0 893; 1350.0 570; 1299.0 515; 1295.0 268 |
| DISCOUNT_POINTS | amount | 5.2K | 20.7K | Exempt 257; 10625.0 39; 15015.08 38; 9289.47 38 |
| LENDER_CREDITS | amount | 2.5K | 23.3K | Exempt 257; 750.0 229; 1000.0 108; 500.0 81 |
| LOAN_TERM | other | 103 | 350 | 360 22.9K; 180 1.6K; 480 947; 240 791 |
| PREPAYMENT_PENALTY_TERM | amount | 9 | 27.1K | 36 594; Exempt 250; 24 181; 2 155 |
| INTRO_RATE_PERIOD | category | 28 | 21.4K | 1 3.1K; 84 1.0K; 120 932; 60 623 |
| NEGATIVE_AMORTIZATION | category | 3 | 0 | 2 28.0K; 1111 250; 1 77 |
| INTEREST_ONLY_PAYMENT | amount | 3 | 0 | 2 25.7K; 1 2.3K; 1111 250 |
| BALLOON_PAYMENT | amount | 3 | 0 | 2 27.2K; 1 806; 1111 250 |
| OTHER_NONAMORTIZING_FEATURES | category | 3 | 0 | 2 28.0K; 1111 250; 1 43 |
| PROPERTY_VALUE | amount | 539 | 5.7K | 405000 341; 505000 336; 455000 329; 705000 325 |
| CONSTRUCTION_METHOD | category | 2 | 0 | 1 28.3K; 2 3 |
| OCCUPANCY_TYPE | category | 3 | 0 | 1 24.5K; 3 3.1K; 2 633 |
| MANUFACTURED_HOME_SECURED_PROPERTY_TYPE | category | 3 | 0 | 3 28.0K; 1111 250; 1 3 |
| MANUFACTURED_HOME_LAND_PROPERTY_INTEREST | category | 3 | 0 | 5 28.0K; 1111 250; 1 3 |
| TOTAL_UNITS | category | 9 | 0 | 1 26.7K; 2 797; 4 405; 5-24 159 |
| MULTIFAMILY_AFFORDABLE_UNITS | category | 17 | 27.8K | Exempt 250; 0 141; 100 64; 8 4 |
| INCOME | other | 1.1K | 3.2K | 0 374; 110 218; 90 212; 100 203 |
| DEBT_TO_INCOME_RATIO | category | 21 | 10.6K | 20%-<30% 3.5K; 30%-<36% 2.9K; <20% 1.5K; 50%-60% 1.0K |
| APPLICANT_CREDIT_SCORE_TYPE | category | 11 | 0 | 9 11.1K; 1 6.2K; 2 4.5K; 3 4.5K |
| CO_APPLICANT_CREDIT_SCORE_TYPE | category | 12 | 0 | 9 12.6K; 10 12.5K; 1 1.0K; 3 862 |
| APPLICANT_ETHNICITY_1 | category | 9 | 11 | 2 17.5K; 3 5.0K; 4 4.2K; 1 1.4K |
| APPLICANT_ETHNICITY_2 | category | 7 | 27.5K | 14 437; 11 210; 12 120; 13 36 |
| APPLICANT_ETHNICITY_3 | category | 6 | 28.3K | 14 10; 12 5; 13 5; 11 4 |
| APPLICANT_ETHNICITY_4 | category | 2 | 28.3K | 13 1 |
| APPLICANT_ETHNICITY_5 | category | 2 | 28.3K | 14 1 |
| CO_APPLICANT_ETHNICITY_1 | category | 9 | 0 | 5 17.2K; 2 5.5K; 4 3.4K; 3 1.6K |
| CO_APPLICANT_ETHNICITY_2 | category | 6 | 28.0K | 14 149; 11 72; 12 37; 13 18 |
| CO_APPLICANT_ETHNICITY_3 | category | 5 | 28.3K | 14 4; 11 2; 13 2; 12 2 |
| CO_APPLICANT_ETHNICITY_4 | empty | 1 | 28.3K |  |
| CO_APPLICANT_ETHNICITY_5 | empty | 1 | 28.3K |  |
| APPLICANT_ETHNICITY_OBSERVED | category | 3 | 0 | 2 22.4K; 3 5.3K; 1 589 |
| CO_APPLICANT_ETHNICITY_OBSERVED | category | 4 | 0 | 4 17.2K; 2 7.2K; 3 3.7K; 1 127 |
| APPLICANT_RACE_1 | category | 16 | 2 | 5 10.1K; 3 6.9K; 6 5.4K; 7 4.2K |
| APPLICANT_RACE_2 | category | 15 | 27.1K | 21 276; 5 269; 22 180; 27 141 |
| APPLICANT_RACE_3 | category | 13 | 28.1K | 5 30; 23 27; 22 23; 27 21 |
| APPLICANT_RACE_4 | category | 8 | 28.3K | 23 2; 44 2; 22 2; 4 1 |
| APPLICANT_RACE_5 | category | 6 | 28.3K | 5 1; 24 1; 25 1; 27 1 |
| CO_APPLICANT_RACE_1 | category | 16 | 1 | 8 17.2K; 5 4.3K; 7 3.4K; 6 1.7K |
| CO_APPLICANT_RACE_2 | category | 14 | 27.9K | 21 104; 5 76; 22 67; 27 45 |
| CO_APPLICANT_RACE_3 | category | 12 | 28.3K | 25 10; 24 8; 22 6; 23 4 |
| CO_APPLICANT_RACE_4 | category | 4 | 28.3K | 25 3; 5 1; 22 1 |
| CO_APPLICANT_RACE_5 | empty | 1 | 28.3K |  |
| APPLICANT_RACE_OBSERVED | category | 3 | 0 | 2 22.4K; 3 5.3K; 1 589 |
| CO_APPLICANT_RACE_OBSERVED | category | 4 | 0 | 4 17.2K; 2 7.2K; 3 3.7K; 1 126 |
| APPLICANT_SEX | category | 5 | 0 | 1 11.6K; 2 9.7K; 4 4.2K; 3 2.8K |
| CO_APPLICANT_SEX | category | 6 | 0 | 5 17.3K; 2 4.2K; 4 3.3K; 1 2.6K |
| APPLICANT_SEX_OBSERVED | category | 3 | 0 | 2 22.4K; 3 5.3K; 1 600 |
| CO_APPLICANT_SEX_OBSERVED | category | 4 | 0 | 4 17.3K; 2 7.2K; 3 3.6K; 1 126 |
| APPLICANT_AGE | category | 8 | 0 | 35-44 7.2K; 25-34 5.3K; 45-54 4.8K; 8888 4.3K |
| CO_APPLICANT_AGE | category | 9 | 0 | 9999 17.1K; 8888 3.5K; 35-44 2.6K; 25-34 1.9K |
| APPLICANT_AGE_ABOVE_62 | category | 3 | 4.3K | No 20.2K; Yes 3.8K |
| CO_APPLICANT_AGE_ABOVE_62 | category | 3 | 20.6K | No 6.6K; Yes 1.0K |
| SUBMISSION_OF_APPLICATION | category | 4 | 0 | 1 22.2K; 3 4.2K; 2 1.6K; 1111 251 |
| INITIALLY_PAYABLE_TO_INSTITUTION | amount | 4 | 0 | 1 22.6K; 3 5.1K; 2 398; 1111 251 |
| AUS_1 | category | 7 | 0 | 6 12.9K; 1 8.8K; 2 4.1K; 7 928 |
| AUS_2 | category | 6 | 25.7K | 1 1.4K; 2 936; 7 145; 5 109 |
| AUS_3 | category | 5 | 27.1K | 1 696; 2 427; 5 73; 3 7 |
| AUS_4 | category | 4 | 27.5K | 1 611; 2 153; 3 5 |
| AUS_5 | category | 4 | 27.7K | 1 509; 2 122; 3 4 |
| DENIAL_REASON_1 | category | 11 | 0 | 10 24.0K; 1 1.2K; 3 859; 4 639 |
| DENIAL_REASON_2 | category | 10 | 27.6K | 9 159; 3 137; 4 125; 1 117 |
| DENIAL_REASON_3 | category | 8 | 28.2K | 9 41; 4 19; 6 19; 5 16 |
| DENIAL_REASON_4 | category | 4 | 28.3K | 9 5; 6 2; 4 1 |
| TRACT_POPULATION | other | 202 | 0 | 5099 560; 4676 493; 0 463; 3927 405 |
| TRACT_MINORITY_POPULATION_PERCENT | amount | 192 | 0 | 0 463; 75.21 424; 25.24 395; 71.38 380 |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | category | 2 | 0 | 139700 27.8K; 0 460 |
| TRACT_TO_MSA_INCOME_PERCENTAGE | amount | 177 | 0 | 198.06 3.2K; 0 742; 67.52 380; 75.33 348 |
| TRACT_OWNER_OCCUPIED_UNITS | who | 184 | 0 | 0 479; 999 424; 876 396; 1911 395 |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | other | 192 | 0 | 0 745; 1637 605; 2098 395; 1513 380 |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | other | 54 | 0 | 0 11.1K; 71 1.0K; 62 812; 76 728 |
| _INGESTED_AT | audit | 1 | 0 | 1782942019856122 28.3K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 01868c1d-0c0a-4870-901f-6 28.3K |
| _SRC_SHA256 | who | 1 | 0 | 68e928049b3664f47f90a2abd 28.3K |
