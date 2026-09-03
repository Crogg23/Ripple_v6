# FED_HUD_MF_SECTION8_CONTRACTS

rows 24.3K  columns 34  scan 3.7s

roles: amount 1, audit 2, category 12, date 3, id 2, other 12, who 2

## when

TRACS_EFFECTIVE_DATE
  1977         1  
  1979         1  
  1980         4  
  1981         4  
  1982         6  
  1983         1  
  1984         1  
  1986         3  
  1991         3  
  1995         1  
  2000         2  
  2001         5  
  2002         2  
  2003         8  
  2004         8  
  2005         8  
  2006       123  #
  2007       164  #
  2008       161  #
  2009       282  ##
  2010       399  ###
  2011       749  ######
  2012       819  ######
  2013       842  ######
  2014       966  #######
  2015       930  #######
  2016       948  #######
  2017       929  #######
  2018      1.0K  #######
  2019       990  #######
  2020      1.0K  #######
  2021      1.3K  ##########
  2022      1.2K  #########
  2023      2.6K  ###################
  2024      3.0K  ######################
  2025      4.1K  ##############################
  2026      1.9K  ##############
  2027         2  

TRACS_OVERALL_EXPIRATION_DATE
  1997         1  
  1999         1  
  2010         1  
  2015         1  
  2016         1  
  2017         1  
  2018         1  
  2019         1  
  2020         3  
  2021        11  
  2022        16  
  2023        26  
  2024        54  #
  2025       179  ##
  2026      2.5K  ##############################
  2027      1.7K  #####################
  2028      1.6K  ###################
  2029      1.9K  ######################
  2030      1.4K  ################
  2031      1.1K  #############
  2032      1.0K  ############
  2033      1.0K  ############
  2034      1.2K  ##############
  2035      1.1K  #############

TRACS_CURRENT_EXPIRATION_DATE
  1900         3  
  1997         1  
  1999         1  
  2010         1  
  2015         1  
  2016         1  
  2017         1  
  2018         1  
  2019         1  
  2020         3  
  2021        11  
  2022        16  
  2023        26  
  2024        54  
  2025       181  
  2026     13.3K  ##############################
  2027      5.9K  #############
  2028       615  #
  2029       665  ##
  2030       457  #
  2031        96  
  2032        97  
  2033        94  
  2034       121  
  2035       159  

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RENT_TO_FMR_RATIO | 24.2K | 0 | 93 | 176.98 | 471.65 | 2.26M |

## who

PROPERTY_NAME_TEXT by rows
        20  Subsidized Housing Corporation 65                 
        17  Christopher Homes Inc.                            
        14  Subsidized Housing Corporation 4                  
        13  Subsidized Housing Corporation 44                 
        13  ELDRIDGE/BARSTOW                                  
        12  RIVERVIEW APARTMENTS                              
        12  Subsidized Housing Corporation 116                
        10  Subsidized Housing Corporation 28                 
         9  HERITAGE HOUSE                                    
         9  PHOENIX VILLA APTS                                
         9  Subsidized Housing Corporation 35                 
         8  WESTBY HOUSING                                    
         8  PARKVIEW APARTMENTS                               
         8  Lakeview Apartments                               
         8  WOODSIDE VILLAGE                                  
         8  PARKVIEW MANOR                                    
         8  HILLCREST APARTMENTS                              
         7  HILLSIDE APARTMENTS                               
         7  RIVERSIDE APARTMENTS                              
         7  Greenpointe Regional Housing                      

PROPERTY_NAME_TEXT by dollars
        2.3K       17 rows  Christopher Homes Inc.                            
        1.1K       20 rows  Subsidized Housing Corporation 65                 
        1.1K       12 rows  RIVERVIEW APARTMENTS                              
        1.0K        8 rows  WESTBY HOUSING                                    
        1.0K        9 rows  PHOENIX VILLA APTS                                
        1.0K       13 rows  ELDRIDGE/BARSTOW                                  
      892.28        9 rows  HERITAGE HOUSE                                    
      882.30        8 rows  WOODSIDE VILLAGE                                  
      845.95        8 rows  HILLCREST APARTMENTS                              
      803.73        6 rows  TRIBOROUGH PRESERVATION                           
      771.93        6 rows  Heritage Manors of Southeast Arkansas (HAP)       
      766.14        8 rows  PARKVIEW MANOR                                    
      755.54       14 rows  Subsidized Housing Corporation 4                  
      730.02        6 rows  Riverview Apartments                              
      724.07        7 rows  Greenpointe Regional Housing                      
      702.06       13 rows  Subsidized Housing Corporation 44                 
      696.32        8 rows  PARKVIEW APARTMENTS                               
      685.30        6 rows  SUNRISE APARTMENTS                                
      651.94       12 rows  Subsidized Housing Corporation 116                
      646.79        8 rows  Lakeview Apartments                               

SRC_SHA256 by rows
     24.3K  d4d745f27ac454a3829ef5f2d574fbeb3573b80f3fcfdea943a0942b365628c5

SRC_SHA256 by dollars
       2.26M    24.3K rows  d4d745f27ac454a3829ef5f2d574fbeb3573b80f3fcfdea943a0942b3656

## who x when

PROPERTY_NAME_TEXT by TRACS_EFFECTIVE_DATE, dollars = RENT_TO_FMR_RATIO
  Christopher Homes Inc.                    2008:129.11 2011:575.09 2012:264.07 2013:259.84 2014:280.48 2015:410.43 2024:125.94 2025:277.45
  ELDRIDGE/BARSTOW                          2022:154.57 2023:639.33 2025:144.63 2026:72.34
  Greenpointe Regional Housing              2013:724.07
  HERITAGE HOUSE                            2010:182.90 2017:192.04 2018:211.32 2019:109.19 2021:106.58 2024:90.25
  HILLCREST APARTMENTS                      2007:91.12 2008:62.63 2012:98.39 2014:98.91 2015:116.08 2016:88.12 2019:191.34 2025:99.36
  HILLSIDE APARTMENTS                       2008:96.41 2010:104.67 2014:88 2017:151.91 2019:114.48 2025:91.30
  Heritage Manors of Southeast Arkansas (H  2015:127.89 2024:644.04
  Lakeview Apartments                       2014:107.74 2016:33.20 2018:153.24 2021:191.97 2022:75.95 2023:0 2025:84.69
  PARKVIEW APARTMENTS                       2017:82.02 2018:111.23 2023:72.78 2024:75.85 2025:156.48 2026:197.96
  PARKVIEW MANOR                            2011:121 2013:99.86 2019:115.23 2021:87.23 2022:87.44 2023:152.82 2025:102.56
  PHOENIX VILLA APTS                        2013:100.05 2023:112.40 2024:113.63 2025:243.61 2026:461.73
  RIVERSIDE APARTMENTS                      2009:111.25 2011:82.72 2018:69.69 2020:134.03 2022:109.30 2025:53.07 2026:66.97
  RIVERVIEW APARTMENTS                      2007:107.69 2010:80.78 2012:139.46 2014:0 2015:98.64 2017:111.61 2019:102.33 2020:90.15 2024:265.94 2026:74.39
  Riverview Apartments                      2011:171.13 2014:121.49 2016:80.13 2022:111.17 2023:167.71 2025:78.39
  SUNRISE APARTMENTS                        2009:65.33 2012:162.16 2021:103.58 2023:269.02 2024:85.21
  Subsidized Housing Corporation 116        2025:176.63 2026:475.31
  Subsidized Housing Corporation 28         2025:286.61 2026:264.60
  Subsidized Housing Corporation 35         2025:427.58 2026:119.14
  Subsidized Housing Corporation 4          2025:285.81 2026:469.73
  Subsidized Housing Corporation 44         2024:38.86 2025:492.68 2026:170.52
  Subsidized Housing Corporation 65         2025:947.03 2026:175.02
  TRIBOROUGH PRESERVATION                   2014:322.32 2023:481.41
  WESTBY HOUSING                            2021:1.0K
  WOODSIDE VILLAGE                          2015:203.64 2016:75.51 2017:114.90 2023:241.24 2025:141.03 2026:105.98

SRC_SHA256 by TRACS_EFFECTIVE_DATE, dollars = RENT_TO_FMR_RATIO
  d4d745f27ac454a3829ef5f2d574fbeb3573b80f  1977:140.03 1979:106.96 1980:393.51 1981:347.25 1982:349 1983:80.56 1984:161.19 1986:267.31 1991:238.65 1995:68.07 2000:221.06 2001:437.81 2002:123.98 2003:673.04 2004:648.71 2005:878.45 2006:12.0K 2007:16.3K 2008:15.9K 2009:28.4K 2010:40.7K 2011:75.6K 2012:83.5K 2013:85.6K 2014:98.1K 2015:94.6K 2016:85.4K 2017:88.9K 2018:98.5K 2019:96.4K 2020:100.2K 2021:122.4K 2022:115.9K 2023:233.3K 2024:262.8K 2025:345.2K 2026:154.4K 2027:127.59

## what

TRACS_OVERALL_EXP_FISCAL_YEAR: 2027 15%, 2029 11%, 2026 11%, 2030 9%, 2028 9%, 2034 7%, 2031 7%, 2044 6%, 2035 6%, 2045 6%, 2033 6%, 2036 6%

TRACS_OVERALL_EXPIRE_QUARTER: Q1 26%, Q4 26%, Q3 26%, Q2 22%

TRACS_STATUS_NAME: Active               97%, Expired              2%, Pending              0%, Executed             0%, Suspended            0%, Terminated           0%

IS_HUD_ADMINISTERED_IND: N 71%, Y 29%

IS_ACC_OLD_IND: N 100%, Y 0%

IS_ACC_PERFORMANCE_BASED_IND: Y 71%, N 29%

CONTRACT_DOC_TYPE_CODE: HAP   72%, PRAC  23%, RAC   4%, PAC   0%, COOP  0%

PROGRAM_TYPE_NAME: Sec 8 NC             16%, 202/8 NC             16%, LMSA                 15%, PRAC/811             13%, PRAC/202             12%, HFDA/8 NC            10%, 515/8 NC             6%, 811 PRA DEMO         4%, Sec 8 SR             4%, RAD PH Conv          3%, HFDA/8 SR            2%, Preservation         2%

PROGRAM_TYPE_GROUP_CODE: PRAC                 23%, 202                  16%, S8NC                 15%, LMSA                 14%, HFDA                 11%, 515                  5%, S8 RAD Conv          4%, PRAD                 4%, S8SR                 3%, PD                   2%, PRES                 2%, PAC                  0%

PROGRAM_TYPE_GROUP_NAME: PRAC 202/811         24%, Sec. 202             16%, Other S8 New         15%, S8 Loan Mgmt         14%, S8 State Agency      11%, S8 FmHA              5%, 811 PRA Demo         4%, Other S8 Rehab       3%, S8 RAD PH Conv       3%, S8 Prop. Disp.       2%, S8 Preservation      2%, PAC 202/811          1%

RENT_TO_FMR_DESCRIPTION: Below 80% FMR 30%, Between 80% & 100% FMR 30%, Between 101% & 120% FMR 23%, Between 121% & 130% FMR 6%, Between 131% & 140% FMR 4%, Between 141% & 160% FMR 4%, Over 160% FMR 2%, Unknown 1%

C_5PLUSBR_COUNT: 0 99%, 1 0%, 2 0%, 4 0%, 3 0%, 6 0%, 5 0%, 8 0%, 7 0%, 10 0%, 16 0%, 12 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONTRACT_NUMBER | id | 23.9K | 0 | MI33A008003 123; MN39RDD1909 122; NJ39RDD1902 122; NJ39RDD1345 122 |
| PROPERTY_ID | id | 23.4K | 0 | 800501591 124; 800502388 123; 800502541 122; 800502499 122 |
| PROPERTY_NAME_TEXT | who | 22.7K | 0 | 21 WESTON 4               124; West Pond Apartments      124; MN39RDD1909               122; Galloway Phase 2          122 |
| TRACS_EFFECTIVE_DATE | date | 3.3K | 0 | 2025-10-01 00:00:00 406; 2025-07-01 00:00:00 387; 2025-08-01 00:00:00 364; 2026-01-01 00:00:00 362 |
| TRACS_OVERALL_EXPIRATION_DATE | date | 2.6K | 0 | 2026-09-30 00:00:00 299; 2026-06-30 00:00:00 268; 2026-10-31 00:00:00 267; 2026-12-31 00:00:00 259 |
| TRACS_OVERALL_EXP_FISCAL_YEAR | category | 41 | 0 | 2027 2.4K; 2029 1.8K; 2026 1.7K; 2030 1.5K |
| TRACS_OVERALL_EXPIRE_QUARTER | category | 4 | 0 | Q1 6.3K; Q4 6.3K; Q3 6.3K; Q2 5.4K |
| TRACS_CURRENT_EXPIRATION_DATE | date | 1.3K | 0 | 2026-12-31 00:00:00 1.6K; 2026-06-30 00:00:00 1.5K; 2026-09-30 00:00:00 1.5K; 2026-08-31 00:00:00 1.3K |
| TRACS_STATUS_NAME | category | 6 | 0 | Active               23.7K; Expired              584; Pending              25; Executed             4 |
| CONTRACT_TERM_MONTHS_QTY | other | 222 | 0 | 240 14.5K; 60 4.1K; 12 3.2K; 120 888 |
| ASSISTED_UNITS_COUNT | other | 431 | 0 | 40 766; 24 764; 50 743; 8 723 |
| IS_HUD_ADMINISTERED_IND | category | 2 | 0 | N 17.1K; Y 7.2K |
| IS_ACC_OLD_IND | category | 2 | 0 | N 24.3K; Y 9 |
| IS_ACC_PERFORMANCE_BASED_IND | category | 2 | 0 | Y 17.1K; N 7.2K |
| CONTRACT_DOC_TYPE_CODE | category | 5 | 0 | HAP   17.6K; PRAC  5.7K; RAC   868; PAC   109 |
| PROGRAM_TYPE_NAME | category | 28 | 0 | Sec 8 NC             3.7K; 202/8 NC             3.6K; LMSA                 3.4K; PRAC/811             2.9K |
| PROGRAM_TYPE_GROUP_CODE | category | 13 | 0 | PRAC                 5.7K; 202                  3.9K; S8NC                 3.7K; LMSA                 3.4K |
| PROGRAM_TYPE_GROUP_NAME | category | 16 | 0 | PRAC 202/811         5.7K; Sec. 202             3.9K; Other S8 New         3.7K; S8 Loan Mgmt         3.4K |
| RENT_TO_FMR_RATIO | amount | 23.9K | 81 | 0 339; 100 121; 120.1175197154786 121; 124.69884140259342 121 |
| RENT_TO_FMR_DESCRIPTION | category | 8 | 81 | Below 80% FMR 7.3K; Between 80% & 100% FMR 7.2K; Between 101% & 120% FMR 5.6K; Between 121% & 130% FMR 1.5K |
| C_0BR_COUNT | other | 173 | 81 | 0 20.0K; 6 393; 10 267; 8 266 |
| C_1BR_COUNT | other | 303 | 81 | 0 3.1K; 8 1.0K; 12 875; 6 736 |
| C_2BR_COUNT | other | 240 | 81 | 0 12.5K; 2 696; 1 661; 4 660 |
| C_3BR_COUNT | other | 174 | 81 | 0 17.1K; 8 517; 12 434; 4 410 |
| C_4BR_COUNT | other | 73 | 81 | 0 21.9K; 4 323; 2 268; 8 209 |
| C_5PLUSBR_COUNT | category | 24 | 81 | 0 23.9K; 1 121; 2 53; 4 41 |
| C_0BR_FMR | other | 492 | 81 | 0 20.1K; 2529 319; 1863 167; 1480 154 |
| C_1BR_FMR | other | 672 | 81 | 0 3.3K; 2655 716; 2085 500; 2476 487 |
| C_2BR_FMR | other | 650 | 81 | 0 12.6K; 973 446; 2910 435; 2941 292 |
| C_3BR_FMR | other | 744 | 81 | 0 17.2K; 3644 326; 2294 195; 3526 168 |
| C_4BR_FMR | other | 517 | 81 | 0 21.9K; 3959 98; 3894 92; 3672 67 |
| INGESTED_AT | audit | 1 | 0 | 1786134034494425 24.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8ad5231e-5f22-41fa-8ae0-5 24.3K |
| SRC_SHA256 | who | 1 | 0 | d4d745f27ac454a3829ef5f2d 24.3K |
