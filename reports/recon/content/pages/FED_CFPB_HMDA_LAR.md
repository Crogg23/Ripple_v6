# FED_CFPB_HMDA_LAR

rows 17.5K  columns 102  scan 8.0s

roles: amount 16, audit 2, category 65, empty 3, other 12, who 4

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LOAN_AMOUNT | 17.5K | 5.0K | 385.0K | 3.00M | 400.00M | 11.46B |
| LOAN_TO_VALUE_RATIO | 11.3K | 0.05 | 79.99 | 106.13 | 4.4K | 839.3K |
| INTEREST_RATE | 11.0K | 0 | 6.56 | 11 | 13.99 | 74.0K |
| RATE_SPREAD | 8.0K | -7.25 | 0.13 | 4.19 | 11.78 | 2.2K |
| TOTAL_LOAN_COSTS | 8.5K | 0 | 7.6K | 38.7K | 105.1K | 83.52M |
| TOTAL_POINTS_AND_FEES | 14 | 0 | 785.14 | 30.6K | 33.5K | 58.7K |

## who

TRACT_OWNER_OCCUPIED_UNITS by rows
       250  876
       238  1415
       238  999
       238  911
       235  666
       224  902
       219  839
       212  1070
       195  1266
       195  532
       192  1452
       186  1097
       183  1139
       179  633
       174  1058
       173  1911
       172  494
       166  1152
       156  610
       155  1150

TRACT_OWNER_OCCUPIED_UNITS by dollars
     528.90M      238 rows  999
     247.94M       40 rows  107
     220.04M      219 rows  839
     215.45M       60 rows  85
     208.41M      250 rows  876
     196.80M       56 rows  120
     173.84M      111 rows  1089
     169.03M      154 rows  457
     168.71M       41 rows  358
     168.31M      166 rows  1152
     165.76M      132 rows  0
     165.68M      138 rows  511
     147.24M      129 rows  1328
     143.81M      107 rows  413
     140.25M      129 rows  523
     139.45M      114 rows  1014
     127.26M      238 rows  1415
     125.44M      173 rows  1911
     125.28M       33 rows  350
     122.89M      179 rows  633

LEI by rows
       742  5493003GQDUH26DNNH17
       731  JJKC32MCHWDI71265Z06
       666  B4TYDEB6GKMZO031MB27
       586  AD6GFRVSDT01YPT1CS68
       559  549300CF8MP6S7MZV277
       543  03D0JEWFDFUS0SEEKG89
       499  549300FGXN1K3HLB1R50
       478  549300GPO6DWUZR4UY30
       453  7H6GLXDRUGQFU57RNE97
       435  E57ODZWZ7FF32TWEFA76
       429  KB1H1DSPRFMYMCUFXT09
       383  RVDPPPGHCGZ40J4VQ731
       297  549300FNXYY540N23N64
       287  5493005PKOSG7MYX0B34
       275  DRMSV1Q0EKMEXLAU1P80
       262  2549006II76YXSS5XM65
       256  254900HA4DQWAE0W3342
       236  549300U3721PJGQZYY68
       235  HIDXEG9BLUJZKBGUT764
       234  54930044OSTKOJMHF287

LEI by dollars
     836.97M      586 rows  AD6GFRVSDT01YPT1CS68
     558.74M      429 rows  KB1H1DSPRFMYMCUFXT09
     523.84M      453 rows  7H6GLXDRUGQFU57RNE97
     481.12M       11 rows  KD3XUN7C6T14HNAYLU02
     441.26M        7 rows  254900YA1AQXNM8QVZ06
     396.64M      435 rows  E57ODZWZ7FF32TWEFA76
     357.21M      559 rows  549300CF8MP6S7MZV277
     326.71M      543 rows  03D0JEWFDFUS0SEEKG89
     313.00M      731 rows  JJKC32MCHWDI71265Z06
     222.42M      666 rows  B4TYDEB6GKMZO031MB27
     220.12M      478 rows  549300GPO6DWUZR4UY30
     216.16M      383 rows  RVDPPPGHCGZ40J4VQ731
     204.49M      742 rows  5493003GQDUH26DNNH17
     178.38M      499 rows  549300FGXN1K3HLB1R50
     172.69M       50 rows  254900SOAE0WU8JM0177
     167.60M      287 rows  5493005PKOSG7MYX0B34
     146.44M      236 rows  549300U3721PJGQZYY68
     135.16M      262 rows  2549006II76YXSS5XM65
     130.40M      256 rows  254900HA4DQWAE0W3342
     127.16M      297 rows  549300FNXYY540N23N64

CENSUS_TRACT by rows
       238  11001001600
       235  11001008802
       224  11001003200
       212  11001002101
       195  11001002102
       192  11001009400
       186  11001011100
       174  11001010400
       173  11001001500
       166  11001002002
       162  11001002400
       156  11001007809
       156  11001010602
       155  11001001901
       154  11001008702
       154  11001007603
       151  11001000300
       149  11001008701
       149  11001009000
       149  11001007601

CENSUS_TRACT by dollars
     478.83M      115 rows  11001002702
     247.94M       40 rows  11001007202
     215.45M       60 rows  11001007201
     196.80M       56 rows  11001008803
     173.84M      111 rows  11001000102
     169.91M      156 rows  11001010602
     169.03M      154 rows  11001008702
     168.71M       41 rows  11001007409
     168.31M      166 rows  11001002002
     147.24M      129 rows  11001000202
     143.81M      107 rows  11001009201
     139.45M      114 rows  11001000804
     127.26M      238 rows  11001001600
     125.44M      173 rows  11001001500
     125.28M       33 rows  11001007203
     121.13M       64 rows  11001010202
     118.89M      143 rows  11001009505
     118.42M      224 rows  11001003200
     118.34M       88 rows  11001001402
     116.39M      101 rows  11001000904

SRC_SHA256 by rows
     17.5K  fb4202f4797807b6d2bcf73ee3de9b67cf0632d1f6646c018ff3f132446cbf1e

SRC_SHA256 by dollars
      11.46B    17.5K rows  fb4202f4797807b6d2bcf73ee3de9b67cf0632d1f6646c018ff3f132446c

## what

DERIVED_MSA_MD: 47894 99%, 99999 1%

CONFORMING_LOAN_LIMIT: C 93%, NC 7%

DERIVED_LOAN_PRODUCT_TYPE: Conventional:First Lien 67%, Conventional:Subordinate Lien 21%, FHA:First Lien 7%, VA:First Lien 5%, FHA:Subordinate Lien 0%, FSA/RHS:Subordinate Lien 0%

DERIVED_DWELLING_CATEGORY: Single Family (1-4 Units):Site 98%, Multifamily:Site-Built 1%, Single Family (1-4 Units):Manu 0%, Multifamily:Manufactured 0%

DERIVED_ETHNICITY: Not Hispanic or Latino 60%, Ethnicity Not Available 33%, Hispanic or Latino 5%, Joint 2%, Free Form Text Only 0%

DERIVED_RACE: Race Not Available 34%, White 33%, Black or African American 25%, Asian 4%, Joint 3%, 2 or more minority races 0%, American Indian or Alaska Nati 0%, Native Hawaiian or Other Pacif 0%, Free Form Text Only 0%

DERIVED_SEX: Female 28%, Male 27%, Sex Not Available 24%, Joint 20%

ACTION_TAKEN: 1 49%, 3 17%, 4 15%, 6 12%, 5 4%, 2 2%, 8 0%, 7 0%

PURCHASER_TYPE: 0 64%, 1 9%, 71 8%, 3 8%, 2 4%, 6 4%, 8 1%, 5 1%, 9 1%, 72 0%

PREAPPROVAL: 2 97%, 1 3%

LOAN_TYPE: 1 88%, 2 7%, 3 5%, 4 0%

LOAN_PURPOSE: 1 60%, 32 12%, 2 11%, 4 9%, 31 8%, 5 0%

LIEN_STATUS: 1 79%, 2 21%

REVERSE_MORTGAGE: 2 98%, 1111 1%, 1 0%

OPEN_END_LINE_OF_CREDIT: 2 81%, 1 18%, 1111 1%

BUSINESS_OR_COMMERCIAL_PURPOSE: 2 91%, 1 8%, 1111 1%

HOEPA_STATUS: 2 55%, 3 45%, 1 0%

INTRO_RATE_PERIOD: 1 51%, 84 17%, 60 9%, 120 8%, Exempt 4%, 3 3%, 36 2%, 6 2%, 72 1%, 12 1%, 360 1%, 00001 1%

NEGATIVE_AMORTIZATION: 2 99%, 1111 1%, 1 0%

OTHER_NONAMORTIZING_FEATURES: 2 99%, 1111 1%, 1 0%

CONSTRUCTION_METHOD: 1 100%, 2 0%

OCCUPANCY_TYPE: 1 87%, 3 11%, 2 2%

MANUFACTURED_HOME_SECURED_PROPERTY_TYPE: 3 99%, 1111 1%, 2 0%, 1 0%

MANUFACTURED_HOME_LAND_PROPERTY_INTEREST: 5 99%, 1111 1%, 1 0%, 2 0%

TOTAL_UNITS: 1 94%, 2 3%, 4 1%, 5-24 1%, 3 1%, 25-49 0%, >149 0%, 50-99 0%, 100-149 0%

MULTIFAMILY_AFFORDABLE_UNITS: Exempt 55%, 0 34%, 100 7%, 99 1%, 8 1%, 11 0%, 12 0%, 4 0%, 43 0%, 76 0%, 67 0%, 44 0%

DEBT_TO_INCOME_RATIO: 30%-<36% 19%, 20%-<30% 19%, 50%-60% 10%, >60% 10%, <20% 8%, 42 6%, 44 5%, 41 5%, 49 5%, 40 5%, 39 4%, 43 4%

APPLICANT_CREDIT_SCORE_TYPE: 9 38%, 1 22%, 3 16%, 2 15%, 8 4%, 7 3%, 11 1%, 1111 1%, 6 0%, 4 0%, 5 0%

CO_APPLICANT_CREDIT_SCORE_TYPE: 10 45%, 9 44%, 1 3%, 2 3%, 3 2%, 7 1%, 1111 1%, 8 1%, 11 0%, 4 0%, 6 0%

APPLICANT_ETHNICITY_1: 2 61%, 3 17%, 4 16%, 1 6%, 14 0%, 11 0%, 12 0%, 13 0%

APPLICANT_ETHNICITY_2: 14 55%, 11 22%, 12 15%, 13 6%, 2 1%, 1 0%

APPLICANT_ETHNICITY_3: 14 48%, 13 29%, 12 14%, 11 10%

CO_APPLICANT_ETHNICITY_1: 5 61%, 2 19%, 4 12%, 3 6%, 1 2%, 14 0%, 13 0%, 11 0%, 12 0%

CO_APPLICANT_ETHNICITY_2: 14 57%, 11 30%, 12 7%, 13 5%, 2 2%

APPLICANT_ETHNICITY_OBSERVED: 2 79%, 3 19%, 1 2%

CO_APPLICANT_ETHNICITY_OBSERVED: 4 61%, 2 26%, 3 13%, 1 1%

APPLICANT_RACE_1: 5 34%, 3 26%, 6 19%, 7 15%, 2 4%, 21 1%, 1 1%, 27 0%, 22 0%, 23 0%, 4 0%, 26 0%

APPLICANT_RACE_2: 21 23%, 5 22%, 22 15%, 25 9%, 27 9%, 23 7%, 3 5%, 24 4%, 26 3%, 4 2%, 2 1%, 44 1%

APPLICANT_RACE_3: 23 17%, 5 15%, 22 13%, 21 12%, 27 11%, 25 9%, 26 7%, 24 5%, 3 5%, 44 3%, 41 1%, 1 1%

APPLICANT_RACE_4: 44 20%, 25 20%, 41 20%, 4 20%, 22 10%, 23 10%

APPLICANT_RACE_5: 41 50%, 5 33%, 24 17%

CO_APPLICANT_RACE_1: 8 61%, 5 15%, 7 12%, 6 6%, 3 4%, 2 1%, 21 0%, 1 0%, 27 0%, 23 0%, 26 0%, 22 0%

CO_APPLICANT_RACE_2: 21 22%, 22 22%, 5 16%, 27 9%, 25 9%, 26 6%, 23 6%, 24 4%, 3 2%, 44 2%, 42 0%, 4 0%

CO_APPLICANT_RACE_3: 5 37%, 22 21%, 25 16%, 23 11%, 26 11%, 24 5%

APPLICANT_RACE_OBSERVED: 2 79%, 3 18%, 1 3%

CO_APPLICANT_RACE_OBSERVED: 4 61%, 2 26%, 3 13%, 1 1%

APPLICANT_SEX: 1 40%, 2 35%, 4 16%, 3 9%, 6 0%

CO_APPLICANT_SEX: 5 61%, 2 15%, 4 12%, 1 9%, 3 3%, 6 0%

APPLICANT_SEX_OBSERVED: 2 79%, 3 18%, 1 3%

CO_APPLICANT_SEX_OBSERVED: 4 61%, 2 26%, 3 13%, 1 1%

APPLICANT_AGE: 35-44 25%, 25-34 20%, 8888 16%, 45-54 15%, 55-64 11%, 65-74 7%, >74 3%, <25 1%

CO_APPLICANT_AGE: 9999 61%, 8888 12%, 35-44 9%, 25-34 7%, 45-54 5%, 55-64 3%, 65-74 2%, >74 1%, <25 0%

APPLICANT_AGE_ABOVE_62: No 84%, Yes 16%

CO_APPLICANT_AGE_ABOVE_62: No 86%, Yes 14%

SUBMISSION_OF_APPLICATION: 1 79%, 3 12%, 2 8%, 1111 1%

AUS_1: 6 47%, 1 28%, 2 13%, 5 4%, 3 3%, 7 3%, 1111 1%

AUS_2: 1 61%, 2 31%, 7 4%, 5 4%, 3 1%

AUS_3: 1 60%, 2 29%, 5 10%, 3 1%

AUS_4: 1 84%, 2 14%, 3 2%

AUS_5: 1 82%, 2 16%, 3 2%

DENIAL_REASON_1: 10 82%, 1 6%, 3 3%, 4 3%, 7 2%, 9 2%, 1111 1%, 6 1%, 5 0%, 2 0%, 8 0%

DENIAL_REASON_2: 4 21%, 9 19%, 1 17%, 3 17%, 6 10%, 5 8%, 7 5%, 2 2%, 8 0%

DENIAL_REASON_3: 6 34%, 9 29%, 4 16%, 5 8%, 3 6%, 7 5%, 1 3%

DENIAL_REASON_4: 9 50%, 6 25%, 4 8%, 7 8%, 5 8%

FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME: 150100 99%, 0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACTIVITY_YEAR | other | 1 | 0 | 2023 17.5K |
| LEI | who | 478 | 0 | 5493003GQDUH26DNNH17 742; JJKC32MCHWDI71265Z06 731; B4TYDEB6GKMZO031MB27 666; AD6GFRVSDT01YPT1CS68 586 |
| DERIVED_MSA_MD | category | 2 | 0 | 47894 17.3K; 99999 125 |
| STATE_CODE | other | 1 | 0 | DC 17.5K |
| COUNTY_CODE | other | 1 | 125 | 11001 17.3K |
| CENSUS_TRACT | who | 203 | 128 | 11001001600 238; 11001008802 235; 11001003200 224; 11001002101 212 |
| CONFORMING_LOAN_LIMIT | category | 2 | 237 | C 16.1K; NC 1.1K |
| DERIVED_LOAN_PRODUCT_TYPE | category | 6 | 0 | Conventional:First Lien 11.8K; Conventional:Subordinate  3.6K; FHA:First Lien 1.2K; VA:First Lien 849 |
| DERIVED_DWELLING_CATEGORY | category | 4 | 0 | Single Family (1-4 Units) 17.2K; Multifamily:Site-Built 235; Single Family (1-4 Units) 37; Multifamily:Manufactured 2 |
| DERIVED_ETHNICITY | category | 5 | 0 | Not Hispanic or Latino 10.5K; Ethnicity Not Available 5.7K; Hispanic or Latino 937; Joint 366 |
| DERIVED_RACE | category | 9 | 0 | Race Not Available 5.9K; White 5.7K; Black or African American 4.4K; Asian 720 |
| DERIVED_SEX | category | 4 | 0 | Female 4.9K; Male 4.7K; Sex Not Available 4.3K; Joint 3.6K |
| ACTION_TAKEN | category | 8 | 0 | 1 8.6K; 3 3.0K; 4 2.6K; 6 2.1K |
| PURCHASER_TYPE | category | 10 | 0 | 0 11.2K; 1 1.6K; 71 1.4K; 3 1.4K |
| PREAPPROVAL | category | 2 | 0 | 2 16.9K; 1 551 |
| LOAN_TYPE | category | 4 | 0 | 1 15.4K; 2 1.2K; 3 849; 4 1 |
| LOAN_PURPOSE | category | 6 | 0 | 1 10.5K; 32 2.0K; 2 1.9K; 4 1.5K |
| LIEN_STATUS | category | 2 | 0 | 1 13.8K; 2 3.6K |
| REVERSE_MORTGAGE | category | 3 | 0 | 2 17.2K; 1111 201; 1 70 |
| OPEN_END_LINE_OF_CREDIT | category | 3 | 0 | 2 14.2K; 1 3.1K; 1111 201 |
| BUSINESS_OR_COMMERCIAL_PURPOSE | category | 3 | 0 | 2 15.9K; 1 1.4K; 1111 201 |
| LOAN_AMOUNT | amount | 399 | 0 | 105000.0 604; 55000.0 453; 255000.0 427; 205000.0 425 |
| LOAN_TO_VALUE_RATIO | amount | 5.7K | 6.0K | 80.0 612; 80 515; 95.0 333; 90.0 273 |
| INTEREST_RATE | amount | 831 | 6.3K | 6.625 496; 6.125 477; 5.875 438; 6.375 425 |
| RATE_SPREAD | amount | 3.6K | 9.3K | Exempt 200; 1.075 41; 0.943 41; 1.268 41 |
| HOEPA_STATUS | category | 3 | 0 | 2 9.5K; 3 7.9K; 1 10 |
| TOTAL_LOAN_COSTS | amount | 6.8K | 8.8K | Exempt 216; 0.00 190; 0.0 46; 6296.45 43 |
| TOTAL_POINTS_AND_FEES | amount | 14 | 17.2K | Exempt 216; 0.0 2; 33465.31 1; 11315.00 1 |
| ORIGINATION_CHARGES | amount | 4.3K | 8.7K | 0.00 408; 0.0 264; 1390.0 233; Exempt 216 |
| DISCOUNT_POINTS | amount | 3.4K | 13.0K | Exempt 203; 9312.13 22; 12595.50 22; 6210.00 22 |
| LENDER_CREDITS | amount | 1.5K | 14.8K | Exempt 203; 750.0 95; 800.00 48; 300.0 38 |
| LOAN_TERM | other | 156 | 207 | 360 13.7K; 480 741; 180 709; 240 509 |
| PREPAYMENT_PENALTY_TERM | amount | 6 | 16.7K | 36 467; Exempt 201; 24 100; 12 5 |
| INTRO_RATE_PERIOD | category | 29 | 12.7K | 1 2.4K; 84 783; 60 410; 120 388 |
| NEGATIVE_AMORTIZATION | category | 3 | 0 | 2 17.3K; 1111 201; 1 6 |
| INTEREST_ONLY_PAYMENT | amount | 3 | 0 | 2 15.5K; 1 1.8K; 1111 201 |
| BALLOON_PAYMENT | amount | 3 | 0 | 2 16.6K; 1 708; 1111 201 |
| OTHER_NONAMORTIZING_FEATURES | category | 3 | 0 | 2 17.2K; 1111 201; 1 45 |
| PROPERTY_VALUE | amount | 477 | 3.8K | 455000 243; 425000 234; Exempt 201; 495000 195 |
| CONSTRUCTION_METHOD | category | 2 | 0 | 1 17.4K; 2 39 |
| OCCUPANCY_TYPE | category | 3 | 0 | 1 15.2K; 3 2.0K; 2 348 |
| MANUFACTURED_HOME_SECURED_PROPERTY_TYPE | category | 4 | 0 | 3 17.2K; 1111 201; 2 36; 1 1 |
| MANUFACTURED_HOME_LAND_PROPERTY_INTEREST | category | 4 | 0 | 5 17.2K; 1111 201; 1 20; 2 15 |
| TOTAL_UNITS | category | 9 | 0 | 1 16.4K; 2 502; 4 251; 5-24 157 |
| MULTIFAMILY_AFFORDABLE_UNITS | category | 19 | 17.1K | Exempt 201; 0 124; 100 26; 99 3 |
| INCOME | other | 1.2K | 2.6K | 0 170; 150 147; 100 147; 120 139 |
| DEBT_TO_INCOME_RATIO | category | 20 | 6.3K | 30%-<36% 1.7K; 20%-<30% 1.7K; 50%-60% 868; >60% 867 |
| APPLICANT_CREDIT_SCORE_TYPE | category | 11 | 0 | 9 6.6K; 1 3.9K; 3 2.8K; 2 2.6K |
| CO_APPLICANT_CREDIT_SCORE_TYPE | category | 11 | 0 | 10 7.9K; 9 7.7K; 1 554; 2 477 |
| APPLICANT_ETHNICITY_1 | category | 8 | 6 | 2 10.7K; 3 3.0K; 4 2.7K; 1 980 |
| APPLICANT_ETHNICITY_2 | category | 6 | 17.0K | 14 287; 11 114; 12 80; 13 32 |
| APPLICANT_ETHNICITY_3 | category | 4 | 17.5K | 14 10; 13 6; 12 3; 11 2 |
| APPLICANT_ETHNICITY_4 | other | 1 | 17.5K | 13 1 |
| APPLICANT_ETHNICITY_5 | other | 1 | 17.5K | 14 1 |
| CO_APPLICANT_ETHNICITY_1 | category | 9 | 1 | 5 10.6K; 2 3.4K; 4 2.1K; 3 996 |
| CO_APPLICANT_ETHNICITY_2 | category | 5 | 17.3K | 14 99; 11 52; 12 12; 13 8 |
| CO_APPLICANT_ETHNICITY_3 | empty | 0 | 17.5K |  |
| CO_APPLICANT_ETHNICITY_4 | empty | 0 | 17.5K |  |
| CO_APPLICANT_ETHNICITY_5 | empty | 0 | 17.5K |  |
| APPLICANT_ETHNICITY_OBSERVED | category | 3 | 0 | 2 13.8K; 3 3.2K; 1 434 |
| CO_APPLICANT_ETHNICITY_OBSERVED | category | 4 | 0 | 4 10.6K; 2 4.5K; 3 2.2K; 1 101 |
| APPLICANT_RACE_1 | category | 16 | 3 | 5 6.0K; 3 4.5K; 6 3.2K; 7 2.7K |
| APPLICANT_RACE_2 | category | 14 | 16.8K | 21 157; 5 153; 22 100; 25 62 |
| APPLICANT_RACE_3 | category | 12 | 17.4K | 23 13; 5 11; 22 10; 21 9 |
| APPLICANT_RACE_4 | category | 6 | 17.5K | 44 2; 25 2; 41 2; 4 2 |
| APPLICANT_RACE_5 | category | 3 | 17.5K | 41 3; 5 2; 24 1 |
| CO_APPLICANT_RACE_1 | category | 17 | 0 | 8 10.6K; 5 2.6K; 7 2.1K; 6 1.0K |
| CO_APPLICANT_RACE_2 | category | 13 | 17.2K | 21 51; 22 50; 5 37; 27 21 |
| CO_APPLICANT_RACE_3 | category | 6 | 17.5K | 5 7; 22 4; 25 3; 23 2 |
| CO_APPLICANT_RACE_4 | other | 1 | 17.5K | 22 1 |
| CO_APPLICANT_RACE_5 | other | 1 | 17.5K | 24 1 |
| APPLICANT_RACE_OBSERVED | category | 3 | 0 | 2 13.8K; 3 3.2K; 1 444 |
| CO_APPLICANT_RACE_OBSERVED | category | 4 | 0 | 4 10.6K; 2 4.5K; 3 2.2K; 1 105 |
| APPLICANT_SEX | category | 5 | 0 | 1 7.0K; 2 6.2K; 4 2.7K; 3 1.5K |
| CO_APPLICANT_SEX | category | 6 | 0 | 5 10.6K; 2 2.6K; 4 2.1K; 1 1.6K |
| APPLICANT_SEX_OBSERVED | category | 3 | 0 | 2 13.8K; 3 3.2K; 1 453 |
| CO_APPLICANT_SEX_OBSERVED | category | 4 | 0 | 4 10.6K; 2 4.5K; 3 2.2K; 1 110 |
| APPLICANT_AGE | category | 8 | 0 | 35-44 4.4K; 25-34 3.6K; 8888 2.8K; 45-54 2.7K |
| CO_APPLICANT_AGE | category | 9 | 0 | 9999 10.6K; 8888 2.1K; 35-44 1.6K; 25-34 1.2K |
| APPLICANT_AGE_ABOVE_62 | category | 2 | 2.8K | No 12.4K; Yes 2.3K |
| CO_APPLICANT_AGE_ABOVE_62 | category | 2 | 12.7K | No 4.1K; Yes 655 |
| SUBMISSION_OF_APPLICATION | category | 4 | 0 | 1 13.8K; 3 2.1K; 2 1.3K; 1111 201 |
| INITIALLY_PAYABLE_TO_INSTITUTION | amount | 4 | 0 | 1 14.4K; 3 2.6K; 2 257; 1111 201 |
| AUS_1 | category | 7 | 0 | 6 8.2K; 1 4.9K; 2 2.3K; 5 677 |
| AUS_2 | category | 5 | 16.0K | 1 882; 2 443; 7 60; 5 51 |
| AUS_3 | category | 4 | 16.7K | 1 473; 2 226; 5 76; 3 11 |
| AUS_4 | category | 3 | 17.0K | 1 433; 2 73; 3 9 |
| AUS_5 | category | 3 | 17.0K | 1 375; 2 73; 3 8 |
| DENIAL_REASON_1 | category | 11 | 0 | 10 14.3K; 1 992; 3 610; 4 490 |
| DENIAL_REASON_2 | category | 9 | 16.9K | 4 128; 9 119; 1 106; 3 103 |
| DENIAL_REASON_3 | category | 7 | 17.4K | 6 34; 9 29; 4 16; 5 8 |
| DENIAL_REASON_4 | category | 5 | 17.5K | 9 6; 6 3; 4 1; 7 1 |
| TRACT_POPULATION | other | 198 | 0 | 5099 419; 4676 278; 3927 244; 4471 238 |
| TRACT_MINORITY_POPULATION_PERCENT | amount | 188 | 0 | 75.21 241; 71.42 238; 71.38 235; 97.91 227 |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | category | 2 | 0 | 150100 17.3K; 0 125 |
| TRACT_TO_MSA_INCOME_PERCENTAGE | amount | 175 | 0 | 198.06 1.9K; 0 328; 158.02 238; 67.52 235 |
| TRACT_OWNER_OCCUPIED_UNITS | who | 183 | 0 | 876 250; 911 238; 1415 238; 999 238 |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | other | 189 | 0 | 1637 430; 0 294; 1265 241; 1513 235 |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | other | 53 | 0 | 0 6.6K; 71 655; 70 526; 67 490 |
| INGESTED_AT | audit | 1 | 0 | 1786164947435095 17.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8033afab-9319-46bf-9ab6-7 17.5K |
| SRC_SHA256 | who | 1 | 0 | fb4202f4797807b6d2bcf73ee 17.5K |
