# FED_CMS_HCRIS

rows 6.1K  columns 120  scan 5.4s

roles: amount 65, audit 2, category 4, date 2, id 5, other 25, state 1, who 16

## when

FISCAL_YEAR_BEGIN_DATE
  2022       985  ######
  2023      5.1K  ##############################

FISCAL_YEAR_END_DATE
  2022         5  
  2023      3.5K  ##############################
  2024      2.6K  ######################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FTE___EMPLOYEES_ON_PAYROLL | 6.0K | 0.05 | 287.49 | 9.4K | 295.3K | 5.83M |
| TOTAL_DAYS_TITLE_V | 127 | 1 | 885 | 30.8K | 59.6K | 344.7K |
| TOTAL_DAYS_TITLE_XVIII | 5.9K | 1 | 2.6K | 53.5K | 208.2K | 42.76M |
| TOTAL_DAYS_TITLE_XIX | 5.1K | 1 | 648.50 | 36.9K | 183.1K | 16.85M |
| TOTAL_DAYS__V___XVIII___XIX___UNKNOWN | 6.0K | 1 | 12.0K | 250.3K | 911.9K | 190.90M |
| TOTAL_BED_DAYS_AVAILABLE | 6.0K | 26 | 22.0K | 304.7K | 1.04M | 288.46M |

## who

HOSPITAL_NAME by rows
       104  ENCOMPASS HEALTH REHABILITATION HOSP
         8  COMMUNITY MEMORIAL HOSPITAL
         8  GOOD SAMARITAN HOSPITAL
         8  MEMORIAL HOSPITAL
         6  MERCY MEDICAL CENTER
         5  SHRINERS HOSPITAL FOR CHILDREN
         5  MERCY HOSPITAL
         4  WASHINGTON COUNTY HOSPITAL
         4  COMMUNITY HOSPITAL
         4  ST. LUKES HOSPITAL
         4  NORTHWEST MEDICAL CENTER
         4  MOUNTAIN VIEW HOSPITAL
         4  JEFFERSON COUNTY HOSPITAL
         4  HOLY CROSS HOSPITAL
         4  ST. MARY MEDICAL CENTER
         4  ST. JOSEPH MEDICAL CENTER
         4  ST. FRANCIS HOSPITAL
         3  COMMUNITY MEDICAL CENTER
         3  FAIRVIEW HOSPITAL
         3  ST. JOSEPHS MEDICAL CENTER

HOSPITAL_NAME by dollars
       2.53M      104 rows  ENCOMPASS HEALTH REHABILITATION HOSP
       1.04M        1 rows  NEW YORK PRESBYTERIAN HOSPITAL
       1.02M        1 rows  ADVENTHEALTH ORLANDO
      861.9K        8 rows  GOOD SAMARITAN HOSPITAL
      632.4K        1 rows  METHODIST HOSPITAL
      592.0K        1 rows  NYU LANGONE HOSPITALS
      586.9K        1 rows  JACKSON MEMORIAL
      580.1K        1 rows  BAPTIST HEALTH SYSTEM
      553.0K        1 rows  NORTON HOSPITALS  INC
      550.8K        2 rows  PRESBYTERIAN HOSPITAL
      536.2K        3 rows  ST. JOSEPHS HOSPITAL
      535.5K        1 rows  ORLANDO HEALTH
      527.2K        1 rows  MONTEFIORE MEDICAL CENTER
      516.1K        1 rows  MEMORIAL HERMANN  HOSPITAL SYS
      489.1K        1 rows  YALE NEW HAVEN HOSPITAL
      482.5K        1 rows  METHODIST H/C MEMPHIS HOSPT.
      477.5K        1 rows  CLEVELAND CLINIC HOSPITAL
      476.6K        2 rows  SAINT FRANCIS HOSPITAL
      464.9K        1 rows  INDIANA UNIVERSITY HEALTH
      461.6K        1 rows  BARNES-JEWISH HOSPITAL

PROVIDER_CCN by rows
         3  400113
         2  321312
         2  523031
         2  390339
         2  511317
         2  230110
         2  144042
         2  241365
         2  363045
         2  110111
         2  231326
         2  341323
         2  102024
         2  670780
         2  454156
         2  230021
         2  250172
         2  673081
         2  420117
         2  460041

PROVIDER_CCN by dollars
       1.04M        1 rows  330101
       1.02M        1 rows  100007
      632.4K        1 rows  450388
      592.0K        1 rows  330214
      586.9K        1 rows  100022
      580.1K        1 rows  450058
      553.0K        1 rows  180088
      535.5K        1 rows  100006
      527.2K        1 rows  330059
      516.1K        1 rows  450184
      492.4K        1 rows  100075
      489.1K        1 rows  070022
      482.5K        1 rows  440049
      477.5K        1 rows  360180
      464.9K        1 rows  150056
      461.6K        1 rows  260032
      438.8K        1 rows  390133
      434.7K        1 rows  340113
      427.6K        1 rows  080001
      419.4K        1 rows  010033

NUMBER_OF_BEDS___TOTAL_FOR_ALL_SUBPROVIDERS by rows
       668  25
       119  40
       105  nan
        97  16
        84  60
        78  24
        73  15
        73  20
        67  50
        62  49
        61  35
        52  48
        50  30
        50  36
        49  18
        46  23
        44  14
        42  22
        42  42
        39  80

NUMBER_OF_BEDS___TOTAL_FOR_ALL_SUBPROVIDERS by dollars
       5.95M      668 rows  25
       1.68M       84 rows  60
       1.60M      119 rows  40
       1.20M       21 rows  180
       1.10M       67 rows  50
       1.08M        2 rows  1515
       1.06M        8 rows  391
       1.04M        1 rows  3287
       1.04M        8 rows  374
       1.04M       31 rows  100
       1.03M       39 rows  80
       1.03M       22 rows  144
       1.02M        1 rows  2889
       1.00M       62 rows  49
      999.8K       27 rows  110
      962.3K       27 rows  120
      944.7K       13 rows  222
      932.3K        8 rows  348
      885.0K       13 rows  208
      882.4K       37 rows  72

FIXED_EQUIPMENT by rows
      2.7K  nan
         6  8064570
         6  76323453
         3  473708
         3  386598061
         2  180075000
         2  1668007
         2  35962000
         2  217630493
         2  178009000
         2  3446275
         2  3749895
         2  7329828
         2  6103300
         2  1184271
         2  122301312
         2  378528
         2  26077417
         2  44391
         2  16726644

FIXED_EQUIPMENT by dollars
     103.43M     2.7K rows  nan
       1.04M        1 rows  138149994
       1.02M        1 rows  1650082786
      670.9K        6 rows  76323453
      632.4K        1 rows  506090927
      592.0K        1 rows  606355782
      586.9K        1 rows  120028804
      580.1K        1 rows  40308956
      553.0K        1 rows  81247608
      535.5K        1 rows  693388250
      492.4K        1 rows  447945817
      489.1K        1 rows  1128358821
      482.5K        1 rows  388445727
      477.5K        1 rows  31228269
      461.6K        1 rows  433804360
      438.8K        1 rows  7652171
      427.6K        1 rows  959029169
      419.0K        1 rows  15795000
      402.5K        1 rows  610358614
      388.3K        1 rows  805977000

## who x when

HOSPITAL_NAME by FISCAL_YEAR_BEGIN_DATE, dollars = TOTAL_BED_DAYS_AVAILABLE
  ADVENTHEALTH ORLANDO                      2023:1.02M
  BAPTIST HEALTH SYSTEM                     2023:580.1K
  COMMUNITY HOSPITAL                        2023:189.8K
  COMMUNITY MEDICAL CENTER                  2023:296.1K
  COMMUNITY MEMORIAL HOSPITAL               2022:8.0K 2023:114.3K
  ENCOMPASS HEALTH REHABILITATION HOSP      2022:196.4K 2023:2.33M
  FAIRVIEW HOSPITAL                         2022:8.7K 2023:179.2K
  GOOD SAMARITAN HOSPITAL                   2023:861.9K
  HOLY CROSS HOSPITAL                       2023:306.7K
  JACKSON MEMORIAL                          2022:586.9K
  JEFFERSON COUNTY HOSPITAL                 2022:2.9K 2023:18.3K
  MEMORIAL HOSPITAL                         2022:15.0K 2023:195.1K
  MERCY HOSPITAL                            2022:28.0K 2023:289.0K
  MERCY MEDICAL CENTER                      2023:344.6K
  METHODIST HOSPITAL                        2023:632.4K
  MOUNTAIN VIEW HOSPITAL                    2023:191.7K
  NEW YORK PRESBYTERIAN HOSPITAL            2023:1.04M
  NORTHWEST MEDICAL CENTER                  2022:209.1K 2023:19.4K
  NORTON HOSPITALS  INC                     2023:553.0K
  NYU LANGONE HOSPITALS                     2023:592.0K
  ORLANDO HEALTH                            2022:535.5K
  PRESBYTERIAN HOSPITAL                     2023:550.8K
  SHRINERS HOSPITAL FOR CHILDREN            2023:5
  ST. FRANCIS HOSPITAL                      2022:9.1K 2023:260.8K
  ST. JOSEPH MEDICAL CENTER                 2022:45.3K 2023:224.0K
  ST. JOSEPHS HOSPITAL                      2023:536.2K
  ST. JOSEPHS MEDICAL CENTER                2023:211.5K
  ST. LUKES HOSPITAL                        2022:18.3K 2023:386.3K
  ST. MARY MEDICAL CENTER                   2022:29.6K 2023:298.2K
  WASHINGTON COUNTY HOSPITAL                2022:5.5K 2023:25.2K

PROVIDER_CCN by FISCAL_YEAR_BEGIN_DATE, dollars = TOTAL_BED_DAYS_AVAILABLE
  100006                                    2022:535.5K
  100007                                    2023:1.02M
  100022                                    2022:586.9K
  102024                                    2022:13.5K 2023:22.0K
  110111                                    2023:13.7K
  144042                                    2022:14.8K 2023:58.8K
  180088                                    2023:553.0K
  230021                                    2023:123.9K
  230110                                    2023:21.3K
  231326                                    2023:13.7K
  241365                                    2023:6.0K
  250172                                    2022:3.2K 2023:2.3K
  321312                                    2023:11.2K
  330059                                    2023:527.2K
  330101                                    2023:1.04M
  330214                                    2023:592.0K
  341323                                    2022:6.3K 2023:8.4K
  363045                                    2023:13.1K
  390339                                    2022:20.7K 2023:36.6K
  400113                                    2022:21.8K 2023:50.1K
  420117                                    2023:12.8K
  450058                                    2023:580.1K
  450184                                    2023:516.1K
  450388                                    2023:632.4K
  454156                                    2023:31.0K
  460041                                    2023:52.2K
  511317                                    2023:9.1K
  523031                                    2023:18.2K
  670780                                    2023:2
  673081                                    2023:18.6K

## where

STATE_CODE: TX 587, CA 407, FL 264, OH 231, PA 212, IL 210, LA 205, NY 189, MI 172, IN 169, GA 166, WI 153

## what

RURAL_VERSUS_URBAN: U 55%, R 44%, nan 1%

CCN_FACILITY_TYPE: STH 53%, CAH 23%, PH 11%, RH 6%, LTCH 6%, CH 1%, RNMHC 0%, ORD 0%, TC 0%

PROVIDER_TYPE: 1 75%, 4 10%, 5 6%, 2 6%, 7 1%, 12 0%, 3 0%, 6 0%, 11 0%, 10 0%

TYPE_OF_CONTROL: 2 40%, 4 23%, 1 10%, 9 6%, 11 6%, 5 5%, 10 4%, 6 2%, 13 1%, 8 1%, 12 1%, 7 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RPT_REC_NUM | id | 6.1K | 0 | 807303 31; 807296 31; 807290 31; 807244 31 |
| PROVIDER_CCN | who | 6.1K | 0 | 670090 31; 470003 31; 450771 31; 251331 31 |
| HOSPITAL_NAME | who | 5.8K | 0 | ENCOMPASS HEALTH REHABILI 106; CRESCENT MEDICAL CENTER L 31; UNIVERSITY OF VERMONT MED 31; TEXAS HEALTH PRESBYTERIAN 31 |
| STREET_ADDRESS | id | 5.9K | 0 | 2600 W. PLEASANT RUN RD. 31; 111 COLCHESTER AVENUE 31; 6200 WEST PARKER ROAD 31; 140 BURKE CALHOUN CITY RO 31 |
| CITY | who | 3.1K | 0 | HOUSTON 39; CHICAGO 39; PHILADELPHIA 36; COLUMBUS 35 |
| STATE_CODE | state | 55 | 0 | TX 587; CA 407; FL 264; OH 231 |
| ZIP_CODE | other | 5.4K | 0 | 75146 31; 05401 31; 75093 31; 38916 31 |
| COUNTY | who | 1.6K | 0 | nan 556; LOS ANGELES 92; MARICOPA 63; MONTGOMERY 61 |
| MEDICARE_CBSA_NUMBER | other | 470 | 0 | 99945 141; 99917 99; 31084 98; 26420 96 |
| RURAL_VERSUS_URBAN | category | 3 | 0 | U 3.3K; R 2.7K; nan 82 |
| CCN_FACILITY_TYPE | category | 9 | 0 | STH 3.2K; CAH 1.4K; PH 646; RH 389 |
| PROVIDER_TYPE | category | 10 | 0 | 1 4.6K; 4 634; 5 392; 2 346 |
| TYPE_OF_CONTROL | category | 13 | 0 | 2 2.5K; 4 1.4K; 1 598; 9 366 |
| FISCAL_YEAR_BEGIN_DATE | date | 95 | 0 | 01/01/2023 2.4K; 07/01/2023 1.8K; 10/01/2022 893; 09/01/2023 273 |
| FISCAL_YEAR_END_DATE | date | 88 | 0 | 12/31/2023 2.4K; 06/30/2024 1.7K; 09/30/2023 896; 08/31/2024 257 |
| FTE___EMPLOYEES_ON_PAYROLL | amount | 5.5K | 0 | nan 141; 230 32; 112 32; 90 32 |
| NUMBER_OF_INTERNS_AND_RESIDENTS__FTE | other | 1.3K | 0 | nan 4.6K; 6 13; 21 12; 4 10 |
| TOTAL_DAYS_TITLE_V | amount | 123 | 0 | nan 6.0K; 4 4; 102 2; 2160 2 |
| TOTAL_DAYS_TITLE_XVIII | amount | 4.3K | 0 | nan 183; 4920 31; 616 30; 42735 30 |
| TOTAL_DAYS_TITLE_XIX | amount | 2.7K | 0 | nan 1.0K; 1 43; 3 38; 2 35 |
| TOTAL_DAYS__V___XVIII___XIX___UNKNOWN | amount | 5.5K | 0 | nan 119; 4303 31; 140185 31; 92701 31 |
| NUMBER_OF_BEDS | other | 676 | 0 | 25 817; 40 124; 16 114; nan 112 |
| TOTAL_BED_DAYS_AVAILABLE | amount | 1.7K | 0 | 9125 463; 9150 318; nan 112; 5840 65 |
| TOTAL_DISCHARGES_TITLE_V | amount | 96 | 0 | nan 6.0K; 3 9; 1 7; 40 3 |
| TOTAL_DISCHARGES_TITLE_XVIII | amount | 2.4K | 0 | nan 177; 1 38; 2 35; 5 33 |
| TOTAL_DISCHARGES_TITLE_XIX | amount | 1.4K | 0 | nan 1.1K; 1 215; 2 136; 3 115 |
| TOTAL_DISCHARGES__V___XVIII___XIX___UNKNOWN | amount | 3.9K | 0 | nan 121; 1071 31; 20252 31; 19681 31 |
| NUMBER_OF_BEDS___TOTAL_FOR_ALL_SUBPROVIDERS | who | 707 | 0 | 25 668; 40 119; nan 105; 16 97 |
| HOSPITAL_TOTAL_DAYS_TITLE_V_FOR_ADULTS___PEDS | amount | 105 | 0 | nan 6.0K; 4 7; 87 2; 6 2 |
| HOSPITAL_TOTAL_DAYS_TITLE_XVIII_FOR_ADULTS___PEDS | amount | 4.1K | 0 | nan 197; 170 31; 481 30; 38717 30 |
| HOSPITAL_TOTAL_DAYS_TITLE_XIX_FOR_ADULTS___PEDS | amount | 2.4K | 0 | nan 1.1K; 1 52; 3 43; 2 42 |
| HOSPITAL_TOTAL_DAYS__V___XVIII___XIX___UNKNOWN__FOR_ADULTS___PEDS | amount | 5.2K | 0 | nan 124; 4006 31; 116395 31; 68192 31 |
| HOSPITAL_NUMBER_OF_BEDS_FOR_ADULTS___PEDS | other | 553 | 0 | 25 654; 40 128; 21 127; 16 126 |
| HOSPITAL_TOTAL_BED_DAYS_AVAILABLE_FOR_ADULTS___PEDS | amount | 1.5K | 0 | 9125 370; 9150 257; nan 115; 5840 71 |
| HOSPITAL_TOTAL_DISCHARGES_TITLE_V_FOR_ADULTS___PEDS | amount | 96 | 0 | nan 6.0K; 3 9; 1 7; 40 3 |
| HOSPITAL_TOTAL_DISCHARGES_TITLE_XVIII_FOR_ADULTS___PEDS | amount | 2.4K | 0 | nan 177; 1 38; 2 35; 5 33 |
| HOSPITAL_TOTAL_DISCHARGES_TITLE_XIX_FOR_ADULTS___PEDS | amount | 1.4K | 0 | nan 1.1K; 1 215; 2 136; 3 115 |
| HOSPITAL_TOTAL_DISCHARGES__V___XVIII___XIX___UNKNOWN__FOR_ADULTS___PEDS | amount | 3.9K | 0 | nan 121; 1071 31; 20252 31; 19681 31 |
| COST_OF_CHARITY_CARE | amount | 4.2K | 0 | nan 1.9K; 9061626 22; 22995143 22; 669418 22 |
| TOTAL_BAD_DEBT_EXPENSE | amount | 4.4K | 0 | nan 1.7K; 6049924 23; 18899098 23; 63998032 23 |
| COST_OF_UNCOMPENSATED_CARE | amount | 4.4K | 0 | nan 1.6K; 869477 23; 15716911 23; 37879433 23 |
| TOTAL_UNREIMBURSED_AND_UNCOMPENSATED_CARE | amount | 4.6K | 0 | nan 1.6K; 881235 23; 85531505 23; 37879433 23 |
| TOTAL_SALARIES_FROM_WORKSHEET_A | amount | 5.9K | 0 | nan 86; 15487442 31; 800101552 31; 156836461 31 |
| OVERHEAD_NON_SALARY_COSTS | amount | 6.0K | 0 | nan 82; 26734780 31; 1044640910 31; 294922564 31 |
| DEPRECIATION_COST | amount | 6.0K | 0 | nan 146; 664056 30; 69411741 30; 28273229 30 |
| TOTAL_COSTS | amount | 6.1K | 0 | nan 82; 37523898 31; 1259505980 31; 401642913 31 |
| INPATIENT_TOTAL_CHARGES | amount | 6.0K | 0 | nan 103; 90182914 31; 1380289475 31; 1122376693 31 |
| OUTPATIENT_TOTAL_CHARGES | amount | 5.4K | 0 | nan 641; 170912889 28; 2193234307 28; 618246310 28 |
| COMBINED_OUTPATIENT___INPATIENT_TOTAL_CHARGES | amount | 5.9K | 0 | nan 82; 261095803 31; 3573523782 31; 1740623003 31 |
| WAGE_RELATED_COSTS__CORE | amount | 3.5K | 0 | nan 2.5K; 1 29; 2850844 18; 127970026 18 |
| WAGE_RELATED_COSTS__RHC_FQHC | amount | 372 | 0 | nan 5.7K; 293608 2; 344264 2; 11179 2 |
| TOTAL_SALARIES__ADJUSTED | amount | 3.7K | 0 | nan 2.4K; 15487442 19; 806713018 19; 156836461 19 |
| CONTRACT_LABOR__DIRECT_PATIENT_CARE | who | 3.0K | 0 | nan 3.0K; 100693315 16; 1397516 16; 10661535 16 |
| WAGE_RELATED_COSTS_FOR_PART___A_TEACHING_PHYSICIANS | amount | 416 | 0 | nan 5.7K; 1257744 3; 2234972 3; 134124 3 |
| WAGE_RELATED_COSTS_FOR_INTERNS_AND_RESIDENTS | amount | 863 | 0 | nan 5.2K; 6957383 5; 529604 5; 1099413 5 |
| CASH_ON_HAND_AND_IN_BANKS | other | 5.5K | 0 | nan 605; 800 29; 1689382 29; 267626 28 |
| TEMPORARY_INVESTMENTS | who | 1.0K | 0 | nan 5.1K; 179288000 7; 104554955 6; 8406477 6 |
| NOTES_RECEIVABLE | who | 240 | 0 | nan 5.9K; 10000 3; 8499165 3; 18982223 2 |
| ACCOUNTS_RECEIVABLE | other | 5.7K | 0 | nan 374; 812454891 30; 30585961 29; 207634474 29 |
| LESS__ALLOWANCES_FOR_UNCOLLECTIBLE_NOTES_AND_ACCOUNTS_RECEIVABLE | other | 4.2K | 0 | nan 2.0K; -2673060 21; -6004177 21; -12404670 21 |
| INVENTORY | other | 5.2K | 0 | nan 929; 179100907 27; 1596307 26; 54190441 26 |
| PREPAID_EXPENSES | other | 4.9K | 0 | nan 1.1K; 75619640 27; 764375 26; 1048097 26 |
| OTHER_CURRENT_ASSETS | who | 2.4K | 0 | nan 3.7K; 192600019 16; 126328679 13; 1521508 13 |
| TOTAL_CURRENT_ASSETS | amount | 5.8K | 0 | nan 317; 28004140 30; 640073938 30; 101982596 30 |
| LAND | other | 4.0K | 0 | nan 1.9K; 78815208 23; 29857748 22; 10554981 22 |
| LAND_IMPROVEMENTS | other | 3.8K | 0 | nan 2.3K; 37824404 22; 7390982 20; 1165179 20 |
| BUILDINGS | other | 5.0K | 0 | nan 1.0K; 3355263455 27; 739843 26; 800624103 26 |
| LEASEHOLD_IMPROVEMENTS | who | 3.0K | 0 | nan 3.1K; 34806398 18; 82478056 15; 2866130 15 |
| FIXED_EQUIPMENT | who | 3.4K | 0 | nan 2.7K; 76323453 20; 61648188 18; 2620037 18 |
| MAJOR_MOVABLE_EQUIPMENT | other | 5.2K | 0 | nan 880; 1802762092 28; 9705346 27; 535039420 27 |
| MINOR_EQUIPMENT_DEPRECIABLE | who | 935 | 0 | nan 5.2K; 41319000 6; 1840246 6; 49861793 5 |
| HEALTH_INFORMATION_TECHNOLOGY_DESIGNATED_ASSETS | who | 440 | 0 | nan 5.7K; 8610648 3; 713103 3; 491348 3 |
| TOTAL_FIXED_ASSETS | amount | 5.7K | 0 | nan 363; 3071294986 30; 4399752 29; 587568615 29 |
| INVESTMENTS | who | 2.2K | 0 | nan 3.8K; 98078635 15; 211878 12; 457666940 12 |
| OTHER_ASSETS | other | 4.8K | 0 | nan 1.3K; 1246765 24; 45453916 24; 227990 24 |
| TOTAL_OTHER_ASSETS | amount | 5.1K | 0 | nan 941; 1606318 26; 537889048 26; 2447956 26 |
| TOTAL_ASSETS | amount | 5.6K | 0 | nan 298; 34010210 30; 1765531601 30; 253071757 30 |
| ACCOUNTS_PAYABLE | amount | 5.8K | 0 | nan 412; 8253674 29; 30343553 29; 13962598 29 |
| SALARIES__WAGES__AND_FEES_PAYABLE | amount | 5.2K | 0 | nan 900; 420610 27; 95894487 27; 11926119 27 |
| PAYROLL_TAXES_PAYABLE | amount | 2.3K | 0 | nan 3.9K; 13166179 12; 66342 12; 3267825 12 |
| NOTES_AND_LOANS_PAYABLE__SHORT_TERM | amount | 2.6K | 0 | nan 3.5K; 1130000 14; 20560073 13; 22130 13 |
| DEFERRED_INCOME | other | 1.0K | 0 | nan 5.1K; 3441444 6; 102322 6; 42794945 6 |
| OTHER_CURRENT_LIABILITIES | other | 5.1K | 0 | nan 1.0K; 98570727 26; 1533162 26; 2248462 26 |
| TOTAL_CURRENT_LIABILITIES | amount | 5.9K | 0 | nan 328; 8674284 30; 245368840 30; 42496340 30 |
| MORTGAGE_PAYABLE | amount | 681 | 0 | nan 5.4K; 2939221000 6; 931812637 6; 679369262 4 |
| NOTES_PAYABLE | amount | 2.4K | 0 | nan 3.7K; 386879788 13; 47220 13; 21705037 13 |
| UNSECURED_LOANS | who | 316 | 0 | nan 5.8K; -162996938 2; 1988773 2; 31083217 2 |
| OTHER_LONG_TERM_LIABILITIES | other | 3.9K | 0 | nan 2.0K; 263854487 23; 7802928 21; 46100666 21 |
| TOTAL_LONG_TERM_LIABILITIES | amount | 5.0K | 0 | nan 979; 263854487 27; 7802928 26; 432980454 26 |
| TOTAL_LIABILITIES | amount | 5.8K | 0 | nan 326; 16477212 30; 678349294 30; 44317704 30 |
| GENERAL_FUND_BALANCE | other | 5.8K | 0 | nan 311; 17532998 30; 1005496305 30; 208754053 30 |
| TOTAL_FUND_BALANCES | amount | 5.8K | 0 | nan 309; 17532998 30; 1087182307 30; 208754053 30 |
| TOTAL_LIABILITIES_AND_FUND_BALANCES | amount | 5.6K | 0 | nan 301; 34010210 30; 1765531601 30; 253071757 30 |
| DRG_AMOUNTS_OTHER_THAN_OUTLIER_PAYMENTS | other | 1 | 0 | nan 6.1K |
| DRG_AMOUNTS_BEFORE_OCTOBER_1 | amount | 2.5K | 0 | nan 3.5K; 32257669 13; 1781595 13; 33355439 13 |
| DRG_AMOUNTS_AFTER_OCTOBER_1 | amount | 3.0K | 0 | nan 3.1K; 1553946 16; 68591422 16; 10894686 16 |
| OUTLIER_PAYMENTS_FOR_DISCHARGES | other | 1 | 0 | nan 6.1K |
| DISPROPORTIONATE_SHARE_ADJUSTMENT | other | 2.7K | 0 | nan 3.4K; 13014 14; 2628766 14; 814501 14 |
| ALLOWABLE_DSH_PERCENTAGE | amount | 1.5K | 0 | nan 3.4K; 0.12 405; 0 264; 1 16 |
| MANAGED_CARE_SIMULATED_PAYMENTS | amount | 2.0K | 0 | nan 4.1K; 34316985 10; 36655038 10; 8138209 10 |
| TOTAL_IME_PAYMENT | amount | 1.3K | 0 | nan 4.8K; 17131599 7; 360590 7; 6596253 7 |
| INPATIENT_REVENUE | amount | 5.7K | 0 | nan 253; 90079125 30; 1380305326 30; 1122376692 30 |
| OUTPATIENT_REVENUE | amount | 5.3K | 0 | nan 785; 171016892 27; 3034927620 27; 618246308 27 |
| TOTAL_PATIENT_REVENUE | amount | 5.8K | 0 | nan 238; 261096017 30; 4415232946 30; 1740623000 30 |
| LESS_CONTRACTUAL_ALLOWANCE_AND_DISCOUNTS_ON_PATIENTS__ACCOUNTS | id | 5.8K | 0 | nan 309; 220834693 30; 2565553384 30; 1193392314 30 |
| NET_PATIENT_REVENUE | amount | 5.7K | 0 | nan 237; 40261324 30; 1849679562 30; 547230686 30 |
| LESS_TOTAL_OPERATING_EXPENSE | amount | 5.9K | 0 | nan 84; 42222222 31; 2058745014 31; 451759025 31 |
| NET_INCOME_FROM_SERVICE_TO_PATIENTS | id | 5.9K | 0 | nan 84; -1960898 31; -209065452 31; 95471661 31 |
| TOTAL_OTHER_INCOME | amount | 5.8K | 0 | nan 304; 6179409 30; 328946452 30; 4402332 30 |
| TOTAL_INCOME | amount | 6.0K | 0 | nan 88; 4218511 31; 119881000 31; 99873993 31 |
| TOTAL_OTHER_EXPENSES | amount | 1.5K | 0 | nan 4.4K; 1 51; 2 37; -1 24 |
| NET_INCOME | id | 6.1K | 0 | nan 89; 4218511 31; 119881000 31; 99873993 31 |
| COST_TO_CHARGE_RATIO | amount | 4.1K | 0 | nan 1.5K; 0 348; 1 108; 2 26 |
| NET_REVENUE_FROM_MEDICAID | other | 4.4K | 0 | nan 1.7K; 1 23; 19106 22; 98671557 22 |
| MEDICAID_CHARGES | other | 4.3K | 0 | nan 1.7K; 10 23; 214755 22; 548187058 22 |
| NET_REVENUE_FROM_STAND_ALONE_CHIP | amount | 945 | 0 | nan 5.2K; 22154 5; 2758522 5; 17806 5 |
| STAND_ALONE_CHIP_CHARGES | other | 974 | 0 | nan 5.1K; 52606 5; 86078038 5; 54242 5 |
| _INGESTED_AT | audit | 1 | 0 | 1781673011749547 6.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 6b1de5a7-5500-4a0f-b8cb-6 6.1K |
| _SRC_SHA256 | who | 1 | 0 | 614f3d94dfeb84092ca775f90 6.1K |
