# PORTAL_SOC_CONNECTICUT_OPEN_FF2B86A533

rows 2.0K  columns 40  scan 7.4s

roles: amount 5, audit 2, category 13, date 2, other 12, who 7

## when

CONTRACT_EXECUTION_DATE
  2009         6  
  2010         9  #
  2011        12  #
  2012       392  ##############################
  2013       384  #############################
  2014       270  #####################
  2015       267  ####################
  2016       230  ##################
  2017       207  ################
  2018       125  ##########
  2019        57  ####
  2020        13  #
  2021        10  #
  2022         8  #
  2023         5  
  2024         3  
  2025         2  

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GRANT_AMOUNT | 2.0K | 0 | 54.5K | 3.54M | 24.00M | 373.44M |
| LOAN_AMOUNT | 2.0K | 0 | 97.0K | 9.50M | 38.00M | 948.57M |
| TOTAL_ASSISTANCE | 2.0K | 10.0K | 110.0K | 10.76M | 48.00M | 1.32B |
| TOTAL_PROJECT_COST | 2.0K | 19.6K | 257.4K | 64.80M | 860.00M | 6.34B |
| AMOUNT_LEVERAGED | 2.0K | 0 | 100.0K | 50.61M | 817.00M | 5.02B |

## who

COMPANY_NAME by rows
         5  Nalas Engineering Services, Inc.
         3  Electric Boat Corporation
         3  Modelcraft Company, Inc.
         3  Aperture Optical Sciences, Inc.
         3  Yumi EcoSolutions, Inc.
         3  Onyx Spirits Company, LLC
         3  Ambassador Property Group, LLC dba Real Property Management of Souther
         3  Marlborough Country Bakery & Deli, Inc.
         3  Charles Island Oyster Farm, LLC
         2  Architectural Glass Industries, LLC
         2  Menaji Worldwide, LLC
         2  Greenstar, LLC
         2  Accel International Holdings, Inc.
         2  R & W Heating Energy Solutions, LLC
         2  Kimtron, Inc.
         2  Thermaxx, LLC
         2  Brenda DiCarlo, LLC dba Insurance Agency Accounting & Bookkeeping
         2  Triple Helix Corporation
         2  Ridgefield One, LLC
         2  L. M. Gill Welding & Manufacturing, LLC

COMPANY_NAME by dollars
     990.50M        3 rows  Electric Boat Corporation
     527.50M        1 rows  Bridgewater Associates, LP*
     283.30M        1 rows  Seven Stars Cloud Group, Inc.
     167.68M        1 rows  CareCentrix, Inc.
     155.00M        1 rows  Cigna Health & Life Insurance Company
     140.16M        2 rows  Charter Communications Holding Company, LLC
     130.00M        1 rows  General Re Corporation
     127.85M        1 rows  NBC Sports Network, LP
     121.30M        1 rows  HANWHA Aerospace USA, LLC (f/k/a EDAC Technologies Corporati
     105.00M        2 rows  Starwood Hotels & Resorts Worldwide, Inc.
     103.80M        1 rows  Dollar Tree Distribution, Inc.
      98.58M        1 rows  Sustainable Building Systems USA, LLC
      85.33M        1 rows  Mount Sinai Genomics, Inc. dba Sema4
      82.91M        1 rows  ASML US, LLC
      81.95M        1 rows  Deloitte Services, LP
      72.78M        1 rows  AQR Capital Management, LLC
      71.30M        1 rows  Synchrony Bank
      69.70M        1 rows  Praxair, Inc.
      65.64M        1 rows  FuelCell Energy, Inc.
      63.97M        2 rows  Accel International Holdings, Inc.

BUSINESS_INDUSTRY by rows
       352  Manufacturing
        54  Restaurant
        54  Service
        21  Retail
        18  Construction
        12  Automotive
        11  Financial Services
        11  Healthcare
        10  Full Service Restaurant
        10  Food Service
        10  Dentistry
        10  Beauty Salon
         9  nan
         9  Food Manufacturing
         9  Machine Shop
         9  Insurance
         8  Other
         7  Brewery
         7  Manufacturer
         7  Architectural Services

BUSINESS_INDUSTRY by dollars
       5.00B      352 rows  Manufacturing
     127.25M        5 rows  Telecommunications
      87.53M        8 rows  Other
      77.14M        9 rows  nan
      69.70M        1 rows  Industrial Gas Manufacturing
      59.46M        2 rows  Defense
      58.89M        7 rows  Manufacturer
      43.32M       54 rows  Service
      41.06M        1 rows  Technology Services & Consulting
      36.69M        6 rows  Service Company
      33.30M        3 rows  Retail Trade
      25.46M        5 rows  Education
      22.77M       54 rows  Restaurant
      20.15M       21 rows  Retail
      14.68M        4 rows  Transportation
      12.22M       11 rows  Financial Services
      11.86M        3 rows  Finance
      11.00M        2 rows  Tourism
       9.48M       18 rows  Construction
       9.42M        2 rows  New and Used Vehicle Sales and Service

FORGIVENESS_EARNED_IF_APPLICABLE by rows
      1.8K  n/a
        24  nan
        15  $   100,000
        12  $   50,000
        12  $   20,000
         9  1,000,000
         8  $   125,000
         8  $   150,000
         8  $   40,000
         8  2,000,000
         7  $   10,000
         7  $   30,000
         6  1,500,000
         6  200,000
         5  250,000
         5  $   80,000
         5  750,000
         4  $   60,000
         4  Pending
         4  10,000,000

FORGIVENESS_EARNED_IF_APPLICABLE by dollars
       3.61B     1.8K rows  n/a
     527.50M        1 rows  10,837,500
     261.60M        4 rows  10,000,000
     203.80M        3 rows  7,000,000
     140.38M        8 rows  2,000,000
     130.00M        1 rows  6,000,000
     127.85M        1 rows  26,000,000
     126.48M        1 rows  9,000,000
     121.30M        1 rows  28,000,000
      87.03M        9 rows  1,000,000
      85.33M        1 rows  7,250,000
      78.28M        3 rows  2,500,000
      73.24M        6 rows  1,500,000
      72.78M        1 rows  13,000,000
      69.70M        1 rows  9,583,330
      53.00M        1 rows  4,000,000
      52.72M        5 rows  750,000
      50.27M        1 rows  20,000,000
      46.79M        3 rows  3,000,000
      42.50M        2 rows  5,000,000

PENALTY_IF_APPLICABLE by rows
      1.5K  n/a
        51  OOB
        38  from 2% to 3%
        29  Rate increase from 2% to 3%
        25  2% to 3%
        25  $1,000
        19  $3,000
        18  $2,000
        14  from 3% to 4%
        12  nan
         9  Pending
         9  Loan repaid
         6  $5,000
         6  3% to 4%
         5  $4,000
         5  $25,000
         5  $6,000
         5  Rate increase from 3% to 4%
         4  $20,000
         4  See EXP

PENALTY_IF_APPLICABLE by dollars
       5.93B     1.5K rows  n/a
      72.78M        1 rows  $   9,075,747.00
      48.08M        9 rows  Pending
      19.80M       51 rows  OOB
      15.40M        1 rows  $   657,090.00
      14.06M        4 rows  See EXP
      14.05M       38 rows  from 2% to 3%
      13.46M        1 rows  Waived Loan Pd in full
      13.08M        1 rows  $   1,710,000.00
      10.96M        1 rows  $   1,082,916.00
      10.83M       12 rows  nan
       9.04M       29 rows  Rate increase from 2% to 3%
       8.98M        1 rows  460,000
       7.50M        1 rows  $360,963 Waived
       7.41M        1 rows  3% to 4% and $17,757
       6.47M       14 rows  from 3% to 4%
       6.30M        1 rows  $   281,768.03
       6.04M       25 rows  2% to 3%
       5.99M        9 rows  Loan repaid
       5.54M       19 rows  $3,000

## who x when

COMPANY_NAME by CONTRACT_EXECUTION_DATE, dollars = TOTAL_PROJECT_COST
  Accel International Holdings, Inc.        2016:20.97M 2019:43.00M
  Ambassador Property Group, LLC dba Real   2015:149.0K 2017:189.0K 2018:200.0K
  Aperture Optical Sciences, Inc.           2011:1.14M 2012:241.9K 2015:3.16M
  Architectural Glass Industries, LLC       2012:223.3K 2015:303.0K
  Brenda DiCarlo, LLC dba Insurance Agency  2013:140.5K 2016:206.0K
  Bridgewater Associates, LP*               2016:527.50M
  CareCentrix, Inc.                         2013:167.68M
  Charles Island Oyster Farm, LLC           2013:619.2K 2014:100.0K
  Charter Communications Holding Company,   2014:13.68M 2019:126.48M
  Cigna Health & Life Insurance Company     2011:155.00M
  Dollar Tree Distribution, Inc.            2012:103.80M
  Electric Boat Corporation                 2010:99.00M 2015:31.50M 2018:860.00M
  General Re Corporation                    2010:130.00M
  Greenstar, LLC                            2012:200.0K 2014:100.0K
  HANWHA Aerospace USA, LLC (f/k/a EDAC Te  2014:121.30M
  Kimtron, Inc.                             2013:288.5K 2017:134.9K
  L. M. Gill Welding & Manufacturing, LLC   2019:800.0K
  Marlborough Country Bakery & Deli, Inc.   2012:27.0K 2016:80.0K 2017:300.0K
  Menaji Worldwide, LLC                     2012:550.0K 2013:120.0K
  Modelcraft Company, Inc.                  2012:288.9K 2015:510.1K 2018:369.0K
  NBC Sports Network, LP                    2014:127.85M
  Nalas Engineering Services, Inc.          2012:500.0K 2013:200.0K 2015:1.57M 2018:9.10M
  Onyx Spirits Company, LLC                 2012:651.2K 2013:58.9K
  R & W Heating Energy Solutions, LLC       2013:106.0K 2014:94.0K
  Ridgefield One, LLC                       2012:100.0K 2013:110.6K
  Seven Stars Cloud Group, Inc.             2018:283.30M
  Starwood Hotels & Resorts Worldwide, Inc  2010:75.00M 2014:30.00M
  Thermaxx, LLC                             2012:199.0K 2014:423.0K
  Triple Helix Corporation                  2012:260.0K 2015:240.0K
  Yumi EcoSolutions, Inc.                   2012:450.0K 2015:126.4K 2016:250.0K

BUSINESS_INDUSTRY by CONTRACT_EXECUTION_DATE, dollars = TOTAL_PROJECT_COST
  Architectural Services                    2013:414.4K 2015:99.3K 2016:1.06M 2017:600.0K
  Automotive                                2012:200.0K 2013:160.0K 2014:802.8K 2015:1.01M 2016:1.19M 2017:445.0K 2018:120.0K
  Beauty Salon                              2012:66.3K 2013:198.0K 2014:160.7K 2015:444.0K 2017:64.4K
  Brewery                                   2012:200.0K 2013:210.6K 2014:1.50M 2015:620.0K 2016:100.0K 2017:1.23M 2018:82.0K
  Construction                              2013:1.67M 2014:2.75M 2015:3.20M 2016:500.0K 2017:1.36M
  Defense                                   2017:46.00M 2019:13.46M
  Dentistry                                 2012:900.6K 2013:777.0K 2015:201.6K 2016:89.0K 2017:521.0K
  Education                                 2012:450.1K 2013:670.0K 2016:99.0K 2018:973.1K 2021:23.27M
  Finance                                   2016:319.2K 2024:11.54M
  Financial Services                        2012:2.76M 2015:246.3K 2016:88.3K 2017:138.0K 2018:409.4K 2019:8.58M
  Food Manufacturing                        2013:582.4K 2014:2.50M 2015:1.31M 2017:2.00M 2020:1.00M
  Food Service                              2012:897.6K 2013:125.8K 2014:200.0K 2015:577.2K 2017:529.7K 2018:150.0K
  Full Service Restaurant                   2012:1.50M 2013:1.31M 2015:150.0K 2016:668.0K
  Healthcare                                2013:463.4K 2014:1.11M 2016:1.05M 2017:608.5K 2019:500.0K
  Industrial Gas Manufacturing              2016:69.70M
  Insurance                                 2012:288.6K 2013:335.4K 2015:1.60M 2016:150.0K 2017:200.0K
  Machine Shop                              2012:875.0K 2013:1.21M 2014:400.0K
  Manufacturer                              2012:450.0K 2013:350.0K 2016:144.7K 2018:5.70M 2019:52.25M
  Manufacturing                             2009:24.14M 2010:394.63M 2011:228.01M 2012:245.14M 2013:342.76M 2014:695.15M 2015:367.58M 2016:918.01M 2017:94.37M 2018:1.64B 2019:13.09M 2021:1.00M 2022:763.0K 2023:22.53M 2025:10.66M
  Other                                     2017:32.37M 2019:3.74M 2020:16.11M 2022:12.14M 2025:23.17M
  Restaurant                                2012:1.91M 2013:1.28M 2014:1.33M 2015:3.32M 2016:4.51M 2017:3.39M 2018:5.81M 2019:902.0K 2020:335.0K
  Retail                                    2012:3.29M 2013:1.98M 2014:12.52M 2015:1.10M 2016:1.00M 2017:250.0K
  Retail Trade                              2012:33.20M 2014:103.0K
  Service                                   2012:12.72M 2013:140.0K 2014:30.00M 2015:161.6K 2016:297.0K
  Service Company                           2018:15.60M 2019:21.09M
  Technology Services & Consulting          2019:41.06M
  Telecommunications                        2015:150.0K 2017:283.0K 2019:126.48M 2020:341.6K
  Tourism                                   2021:6.00M 2022:5.00M
  Transportation                            2014:1.02M 2016:13.30M 2018:351.5K
  nan                                       2013:186.0K 2018:143.0K 2022:39.46M 2023:35.36M 2024:2.00M

## what

FISCAL_YEAR: 2013 24%, 2014 15%, 2015 14%, 2017 13%, 2016 11%, 2018 8%, 2012 8%, 2019 4%, 2020 1%, 2021 1%, 2010 1%, 2023 0%

COUNTY_1: Hartford 35%, Fairfield 21%, New Haven 20%, New London 6%, Middlesex 6%, Litchfield 4%, Tolland 3%, Windham 2%, nan 1%, New 0%, New York 0%, n/a 0%

STATE: CT 99%, NY 0%, nan 0%, NH 0%, n/a 0%, UT 0%, OH 0%, DE 0%, NJ 0%

WOMAN_MINORITY_VETERAN_INTERNATIONAL_EXPORT: No 61%, no 13%, Yes Woman 13%, Yes Woman/Minority 3%, Yes Minority 3%, Yes International Export 2%, Yes Veteran 1%, Yes 1%, nan 1%, yes 1%, Yes Woman/Veteran 0%, Yes Woman/International Export 0%

FUNDING_SOURCE: Small Business Express Program 87%, Manufacturing Assistance Act 9%, Manufacturing Assistance Act/S 1%, Manufacturing Assistance Act R 1%, Manufacturing Assistance Act/U 1%, Manufacturing Assistance Act - 0%, Manufacturing Assistance Act - 0%, Manufacturing Assistance Act-  0%, Manufacturing Assistance Act R 0%, Manufacturing Assistance Act/  0%, Manufacturing Assistance Act R 0%, Manufacturing Assistance Act/M 0%

STATUTORY_REFERENCE: CGS Sec. 32-7g 86%, CH 588l 11%, PA 10-75 1%, CH588l 1%, nan 0%, 32-321 0%

PER_CONTRACT_PART_TIME_CT_JOBS_TO_BE_RETAINED: 0 91%, nan 7%, n/a 1%, 1 0%, See EXP 0%, 6 0%, 5 0%, 27 0%, 2 0%, 8 0%, 7 0%, 16 0%

PER_CONTRACT_PART_TIME_CT_JOBS_TO_BE_CREATED: 0 91%, nan 7%, n/a 1%, See EXP 0%, 2 0%, 1 0%, 4 0%, 9 0%, 19 0%

JOB_OBLIGATION_STATUS: Met 43%, Not Met 24%, Pending 23%, met 5%, n/a 2%, nan 1%, not met 1%, met goal 0%, See EXP 0%, OOB 0%, Funding repaid 0%, Loan repaid 1/31/20 0%

PER_APPLICATION_EXISTING_PART_TIME_JOBS_IN_CT: 0 87%, 1 4%, 2 3%, 4 1%, 3 1%, 7 1%, n/a 1%, 10 1%, nan 1%, 5 1%, 6 1%, 8 0%

PER_APPLICATION_PART_TIME_JOBS_TO_BE_CREATED_IN_CT: 0 92%, 1 2%, 2 2%, 5 1%, n/a 1%, nan 1%, 4 1%, 3 0%, 10 0%, 6 0%, 12 0%, 20 0%

COMPUTED_REGION_SND5_K6ZV: 1 37%, 7 14%, 9 14%, 4 11%, 2 7%, 3 6%, 8 5%, nan 3%, 6 2%, 5 2%

COMPUTED_REGION_DAM5_Q64J: 1041 35%, 1040 21%, 1044 20%, 1043 6%, 1045 5%, 1042 4%, 38 3%, 39 2%, nan 2%, 2095 0%, 3176 0%, 2442 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | category | 16 | 0 | 2013 470; 2014 301; 2015 285; 2017 259 |
| COMPANY_NAME | who | 1.9K | 0 | CPR Training Professional 11; Foresite Technologies, In 11; ABC Printing, Inc. 10; Copperwood, LLC 10 |
| COMPANY_ADDRESS | who | 1.8K | 0 | 99 East River Drive, 7th  11; 875 Foxon Road 10; 24 Eugene O'Neill Drive 10; 10 Bevin Road 10 |
| MUNICIPALITY | who | 197 | 0 | Hartford 114; Stamford 94; New Haven 66; Bridgeport 59 |
| COUNTY_1 | category | 16 | 0 | Hartford 704; Fairfield 428; New Haven 406; New London 124 |
| STATE | category | 9 | 0 | CT 2.0K; NY 6; nan 5; NH 2 |
| ZIP_CODE | other | 265 | 0 | 06902 42; 06410 42; 06002 36; 06033 35 |
| BUSINESS_INDUSTRY | who | 1.1K | 0 | Manufacturing 352; Service 54; Restaurant 54; Retail 22 |
| NAICS_CODE | other | 705 | 0 | 722511 39; 332710 29; 524210 25; 722110 22 |
| WOMAN_MINORITY_VETERAN_INTERNATIONAL_EXPORT | category | 27 | 0 | No 1.2K; no 249; Yes Woman 249; Yes Woman/Minority 66 |
| CONTRACT_EXECUTION_DATE | date | 970 | 0 | 2013-02-26T00:00:00.000 12; 2012-09-24T00:00:00.000 11; 2013-04-17T00:00:00.000 11; 2013-02-07T00:00:00.000 11 |
| GRANT_AMOUNT | amount | 263 | 0 | 100000 654; 0 504; 50000 108; 40000 84 |
| LOAN_AMOUNT | amount | 326 | 0 | 0 780; 300000 292; 100000 123; 250000 72 |
| TOTAL_ASSISTANCE | amount | 531 | 0 | $100,000 381; $400,000 195; $300,000 91; $50,000 75 |
| TOTAL_PROJECT_COST | amount | 1.2K | 0 | 200000 162; 100000 83; 500000 77; 300000 36 |
| AMOUNT_LEVERAGED | amount | 1.0K | 0 | $100,000 280; $0 198; $50,000 74; $40,000 45 |
| FUNDING_SOURCE | category | 14 | 0 | Small Business Express Pr 1.7K; Manufacturing Assistance  185; Manufacturing Assistance  24; Manufacturing Assistance  22 |
| STATUTORY_REFERENCE | category | 6 | 0 | CGS Sec. 32-7g 1.7K; CH 588l 219; PA 10-75 25; CH588l 22 |
| PER_CONTRACT_FULL_TIME_CT_JOBS_TO_BE_RETAINED | other | 183 | 0 | 0 302; 2 150; 1 140; 3 128 |
| PER_CONTRACT_FULL_TIME_CT_JOBS_TO_BE_CREATED | other | 114 | 0 | 5 366; 2 299; 3 257; 1 206 |
| PER_CONTRACT_PART_TIME_CT_JOBS_TO_BE_RETAINED | category | 15 | 0 | 0 1.8K; nan 145; n/a 20; 1 5 |
| PER_CONTRACT_PART_TIME_CT_JOBS_TO_BE_CREATED | category | 9 | 0 | 0 1.8K; nan 145; n/a 20; See EXP 4 |
| ACTUAL_JOBS_AT_TIME_OF_REVIEW | other | 184 | 0 | Pending 459; 0 102; 3 83; 5 76 |
| JOB_OBLIGATION_STATUS | category | 24 | 0 | Met 857; Not Met 483; Pending 465; met 104 |
| PENALTY_IF_APPLICABLE | who | 210 | 0 | n/a 1.5K; OOB 51; from 2% to 3% 38; Rate increase from 2% to  29 |
| FORGIVENESS_EARNED_IF_APPLICABLE | who | 84 | 0 | n/a 1.8K; nan 24; $   100,000 15; $   50,000 12 |
| PER_APPLICATION_EXISTING_FULL_TIME_JOBS_IN_CT | other | 170 | 0 | 0 296; 2 150; 1 143; 3 126 |
| PER_APPLICATION_FULL_TIME_JOBS_TO_BE_CREATED_IN_CT | other | 118 | 0 | 2 320; 5 301; 3 243; 1 202 |
| PER_APPLICATION_EXISTING_PART_TIME_JOBS_IN_CT | category | 45 | 0 | 0 1.7K; 1 68; 2 54; 4 28 |
| PER_APPLICATION_PART_TIME_JOBS_TO_BE_CREATED_IN_CT | category | 28 | 0 | 0 1.8K; 1 36; 2 31; 5 17 |
| LOCATION_1 | other | 1.8K | 0 | 99 East River Drive, 7th  11; 875 Foxon Road 10; 24 Eugene O'Neill Drive 10; 10 Bevin Road 10 |
| GEOCODED_LOCATION | other | 1.8K | 0 | nan 39; {"latitude": "41.32194",  10; {"latitude": "41.35405",  10; {"latitude": "41.57755",  10 |
| COMPUTED_REGION_SND5_K6ZV | category | 10 | 0 | 1 736; 7 284; 9 279; 4 211 |
| COMPUTED_REGION_DAM5_Q64J | category | 20 | 0 | 1041 702; 1040 427; 1044 405; 1043 116 |
| COMPUTED_REGION_NHMP_CQ6B | other | 224 | 0 | nan 54; 7 41; 119 40; 63 39 |
| COMPUTED_REGION_M4Y2_WHSE | other | 151 | 0 | 64 109; 135 94; 93 67; 15 59 |
| FULL_TIME_CT_EMPLOYMENT_AT_6_30_18 | other | 72 | 0 | nan 1.8K; 3 9; 6 8; 2 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:48:29.94946 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b71ab0aa-3670-41c9-ba72-2 2.0K |
| SRC_SHA256 | who | 1 | 0 | d857fcdaf8956ebb0603843ae 2.0K |
