# PORTAL_CKA_ANALYZE_BOSTON_9A0FE05B1B

rows 10.0K  columns 20  scan 4.0s

roles: amount 1, audit 2, category 7, date 3, id 1, other 4, who 3

## when

CNTRCT_HDR_CNTRCT_BEGIN_DT
  2018       686  #############
  2019      1.2K  ######################
  2020      1.0K  ####################
  2021      1.2K  ######################
  2022      1.4K  ##########################
  2023      1.4K  ###########################
  2024      1.6K  ##############################
  2025      1.4K  ##########################
  2026       197  ####

CNTRCT_HDR_CNTRCT_EXPIRE_DT
  2018       111  ##
  2019       909  ###################
  2020       934  ###################
  2021      1.1K  ######################
  2022      1.2K  ########################
  2023      1.4K  ##############################
  2024      1.4K  ##############################
  2025      1.4K  #############################
  2026      1.1K  #######################
  2027       226  #####
  2028       163  ###
  2029        10  
  2030         1  
  2031         2  
  2033         2  

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMT_CNTRCT_MAX | 10.0K | 0 | 45.9K | 9.20M | 651.10M | 6.46B |

## who

VENDOR_NAME1 by rows
       115  Liberty Chevrolet
        95  Colonial Ford Inc
        91  Safeware Inc,
        91  McGovern MHQ Inc.
        86  Dedham Sportsman's Center, Inc.dba
        74  Fleming Bros Inc
        67  A&M Home Services LLC
        64  Northeast Rescue Systems, Inc.
        61  Firematic Supply Co., Inc.
        58  Bonnell Motors, Inc.
        53  W.B. Mason Co., Inc.
        53  T. C. Murphy, Inc.
        46  Industrial Protection Services LLC
        46  PJ Systems Inc. d/b/a
        44  Northern Contracting Corp.
        44  Paul J Rogan Company Inc
        42  McGovern MHQ Inc
        39  Casablanca Services Inc.
        38  Leahy Landscaping, Inc.
        38  Atlantic Tactical, Inc.

VENDOR_NAME1 by dollars
     843.94M        3 rows  TRANSDEV SERVICES. INC
     228.50M        2 rows  Bond Building Construction Inc
     216.60M       12 rows  J & J Contractors, Inc.
     214.28M        2 rows  Shawmut Design and Construction
     180.53M        2 rows  Turner Construction Co.
     148.86M        5 rows  Capitol Waste Services, Inc.
     109.24M       44 rows  Northern Contracting Corp.
     102.15M       74 rows  Fleming Bros Inc
      99.46M       25 rows  Mario Susi & Son, Inc.
      92.22M        6 rows  Boston Building & Bridge Corp.
      91.78M        5 rows  Covanta Sustainable Solutions LLC
      91.03M       29 rows  Lorusso Corporation
      81.86M       21 rows  G V W Inc.
      81.33M        8 rows  Eastern Minerals
      78.72M       27 rows  Fred Deroma & Son, Inc
      67.04M        6 rows  ENE Systems, Inc.
      66.14M       35 rows  WCI CORP.
      65.94M       18 rows  Spring City Elect. Mfg. Corp
      60.75M        9 rows  Dennis K. Burke, Inc.
      60.16M        4 rows  SPS New England, Inc.

DEPT_TBL_DESCR_3_DIGIT by rows
      2.5K  Procurement
      2.2K  Boston Public School Dept
       872  Police Department
       586  Parks & Recreation Department
       442  Public Works Department
       425  Fire Department
       306  Dpt of Innovation & Technology
       244  Mayor's Office of Housing
       212  Property Management
       183  Emergency Preparedness
       170  Transportation Department
       142  Age Strong Commission
       116  Office of Eco Opp & Inclusion
        97  Public Facilities Dept
        82  Library Department
        77  Boston Center-Youth & Families
        48  Office of Arts & Culture
        43  Central Fleet Management
        39  Environment Department
        33  Office of Human Services

DEPT_TBL_DESCR_3_DIGIT by dollars
       2.26B     2.2K rows  Boston Public School Dept
       1.06B       97 rows  Public Facilities Dept
       1.05B      442 rows  Public Works Department
     767.87M     2.5K rows  Procurement
     319.11M      586 rows  Parks & Recreation Department
     160.66M      212 rows  Property Management
     155.20M      170 rows  Transportation Department
     105.29M       82 rows  Library Department
      75.07M      872 rows  Police Department
      72.73M      425 rows  Fire Department
      70.60M      142 rows  Age Strong Commission
      55.90M      306 rows  Dpt of Innovation & Technology
      54.07M      116 rows  Office of Eco Opp & Inclusion
      35.91M       11 rows  Parking Clerk
      33.18M      244 rows  Mayor's Office of Housing
      15.29M        9 rows  Office of Finance
      11.32M       77 rows  Boston Center-Youth & Families
      10.69M       43 rows  Central Fleet Management
       7.40M      183 rows  Emergency Preparedness
       7.33M       39 rows  Environment Department

SRC_SHA256 by rows
     10.0K  2eeec032410b3e1ebeee27c9d03611ee3c9805fe5fd6b8273ddb81f535e29df8

SRC_SHA256 by dollars
       6.46B    10.0K rows  2eeec032410b3e1ebeee27c9d03611ee3c9805fe5fd6b8273ddb81f535e2

## who x when

VENDOR_NAME1 by CNTRCT_HDR_CNTRCT_BEGIN_DT, dollars = AMT_CNTRCT_MAX
  A&M Home Services LLC                     2018:159.6K 2019:3.44M 2020:311.4K 2021:470.0K 2022:2.06M 2023:847.5K 2024:2.38M 2025:2.00M 2026:265.5K
  Atlantic Tactical, Inc.                   2018:14.6K 2019:278.7K 2020:251.7K 2021:45.8K 2022:138.7K 2023:65.2K 2024:80.2K 2025:268.4K
  Bond Building Construction Inc            2022:93.46M 2024:135.04M
  Bonnell Motors, Inc.                      2018:71.9K 2019:143.8K 2020:752.2K 2021:2.10M 2022:1.04M 2023:1.57M 2024:1.31M 2025:280.1K 2026:250.9K
  Boston Building & Bridge Corp.            2018:6.66M 2019:33.20M 2020:27.71M 2021:11.22M 2023:13.43M
  Capitol Waste Services, Inc.              2019:148.86M
  Casablanca Services Inc.                  2020:105.4K 2021:197.1K 2022:1.52M 2023:320.6K 2024:390.8K 2025:10.15M 2026:3.55M
  Colonial Ford Inc                         2018:1.11M 2019:110.0K 2021:2.27M 2022:4.82M 2023:6.41M 2024:3.52M 2025:5.67M 2026:239.1K
  Covanta Sustainable Solutions LLC         2019:72.84M 2024:18.95M
  Dedham Sportsman's Center, Inc.dba        2018:2.97M 2019:806.7K 2020:940.9K 2021:2.23M 2022:1.12M 2023:2.04M 2024:620.2K 2025:1.41M 2026:1.52M
  Firematic Supply Co., Inc.                2018:294.8K 2019:391.0K 2020:318.4K 2021:598.1K 2022:170.3K 2023:501.5K 2024:105.8K 2025:311.1K
  Fleming Bros Inc                          2018:8.20M 2019:14.32M 2020:4.97M 2021:17.21M 2022:5.75M 2023:9.70M 2024:9.69M 2025:32.32M
  Industrial Protection Services LLC        2018:53.5K 2019:131.1K 2020:178.3K 2021:192.1K 2022:138.2K 2023:131.0K 2024:110.4K 2025:235.3K 2026:24.4K
  J & J Contractors, Inc.                   2019:38.89M 2020:7.95M 2021:4.78M 2022:59.98M 2023:70.11M 2024:13.16M 2025:21.73M
  Leahy Landscaping, Inc.                   2018:778.9K 2019:153.6K 2020:238.6K 2021:1.89M 2022:337.0K 2023:344.2K 2024:313.9K 2025:296.3K 2026:528.8K
  Liberty Chevrolet                         2018:952.2K 2019:1.26M 2020:1.93M 2021:1.21M 2022:1.44M 2023:4.41M 2024:1.95M 2025:1.72M 2026:128.2K
  Lorusso Corporation                       2018:184.1K 2019:7.82M 2020:9.57M 2021:3.62M 2022:7.03M 2023:5.18M 2024:17.58M 2025:21.71M 2026:18.34M
  Mario Susi & Son, Inc.                    2018:3.41M 2019:22.05M 2020:12.32M 2021:8.55M 2022:1.78M 2023:19.95M 2024:8.47M 2025:15.75M 2026:7.18M
  McGovern MHQ Inc                          2024:4.13M 2025:2.29M 2026:1.07M
  McGovern MHQ Inc.                         2018:4.14M 2019:10.15M 2020:4.81M 2021:2.10M
  Northeast Rescue Systems, Inc.            2018:147.3K 2019:540.6K 2020:198.1K 2021:292.6K 2022:544.3K 2023:234.9K 2024:3.73M 2025:2.15M
  Northern Contracting Corp.                2019:16.33M 2020:3.68M 2021:19.71M 2022:5.34M 2023:41.43M 2024:16.40M 2025:3.25M 2026:3.10M
  PJ Systems Inc. d/b/a                     2018:148.1K 2019:318.1K 2020:62.0K 2021:113.2K 2022:40.6K 2023:390.8K 2024:121.3K 2025:30.7K
  Paul J Rogan Company Inc                  2018:1.89M 2019:3.34M 2020:6.46M 2021:5.16M 2022:5.85M 2023:9.77M 2024:11.82M 2025:4.54M
  Safeware Inc,                             2018:114.1K 2019:470.8K 2020:217.3K 2021:525.1K 2022:388.7K 2023:977.8K 2024:410.6K 2025:681.5K 2026:215.6K
  Shawmut Design and Construction           2020:83.15M 2022:131.13M
  T. C. Murphy, Inc.                        2018:257.9K 2019:3.44M 2020:246.6K 2021:371.8K 2022:465.7K 2023:822.1K 2024:53.6K 2025:1.09M 2026:109.2K
  TRANSDEV SERVICES. INC                    2018:92.70M 2020:100.14M 2023:651.10M
  Turner Construction Co.                   2021:180.35M 2025:175.0K
  W.B. Mason Co., Inc.                      2018:1.28M 2019:3.64M 2020:3.74M 2021:1.76M 2022:2.99M 2023:2.49M 2024:4.90M 2025:2.50M 2026:257.8K

DEPT_TBL_DESCR_3_DIGIT by CNTRCT_HDR_CNTRCT_BEGIN_DT, dollars = AMT_CNTRCT_MAX
  Age Strong Commission                     2018:631.5K 2019:188.0K 2020:5.87M 2021:18.60M 2022:9.97M 2023:7.73M 2024:27.40M 2025:220.4K
  Boston Center-Youth & Families            2018:170.1K 2019:1.21M 2020:1.60M 2021:5.61M 2022:1.25M 2023:890.1K 2024:242.6K 2025:323.9K 2026:18.3K
  Boston Public School Dept                 2018:179.95M 2019:77.62M 2020:180.90M 2021:79.44M 2022:184.14M 2023:855.33M 2024:326.28M 2025:365.15M 2026:15.04M
  Central Fleet Management                  2018:3.52M 2019:472.1K 2020:15.6K 2022:13.3K 2023:1.08M 2024:1.83M 2025:3.36M 2026:401.4K
  Dpt of Innovation & Technology            2018:21.20M 2019:3.85M 2020:3.74M 2021:15.02M 2022:3.97M 2023:3.24M 2024:112.9K 2025:4.19M 2026:602.3K
  Emergency Preparedness                    2018:1.38M 2019:1.33M 2020:538.5K 2021:940.9K 2022:628.3K 2023:619.9K 2024:1.38M 2025:538.3K 2026:48.6K
  Environment Department                    2019:830.9K 2020:105.0K 2021:344.8K 2022:1.42M 2023:50.0K 2024:1.91M 2025:2.60M 2026:72.8K
  Fire Department                           2018:4.28M 2019:9.23M 2020:8.21M 2021:11.82M 2022:7.22M 2023:20.23M 2024:6.79M 2025:4.77M 2026:162.1K
  Library Department                        2018:936.8K 2019:38.60M 2020:1.34M 2021:20.93M 2022:10.22M 2023:757.3K 2024:6.36M 2025:26.15M
  Mayor's Office of Housing                 2018:1.49M 2019:2.09M 2020:2.89M 2021:1.79M 2022:5.89M 2023:3.22M 2024:9.43M 2025:5.97M 2026:400.9K
  Office of Arts & Culture                  2018:14.4K 2019:10.0K 2020:132.5K 2021:18.0K 2022:619.6K 2023:181.1K 2024:89.5K 2025:271.6K 2026:33.0K
  Office of Eco Opp & Inclusion             2018:100.0K 2019:13.00M 2020:17.99M 2021:6.84M 2022:5.20M 2023:1.33M 2024:9.15M 2025:468.4K 2026:1
  Office of Finance                         2019:265.5K 2020:11.22M 2021:3.79M 2025:16.9K
  Office of Human Services                  2021:13.8K 2022:49.5K 2023:167.3K 2024:1.05M 2025:70.0K 2026:94.6K
  Parking Clerk                             2018:5.40M 2019:5.46M 2020:6.00M 2021:18.1K 2022:6.02M 2023:6.00M 2024:6.00M 2025:1.01M
  Parks & Recreation Department             2018:16.94M 2019:51.04M 2020:13.85M 2021:37.92M 2022:30.73M 2023:47.99M 2024:29.08M 2025:83.59M 2026:7.96M
  Police Department                         2018:9.01M 2019:12.13M 2020:10.40M 2021:8.74M 2022:6.85M 2023:9.28M 2024:7.52M 2025:10.80M 2026:339.6K
  Procurement                               2018:47.44M 2019:115.37M 2020:68.26M 2021:65.70M 2022:88.84M 2023:120.76M 2024:174.61M 2025:80.35M 2026:6.54M
  Property Management                       2018:10.04M 2019:15.15M 2020:89.21M 2021:9.78M 2022:2.87M 2023:4.36M 2024:13.47M 2025:15.74M 2026:36.5K
  Public Facilities Dept                    2019:59.75M 2020:62.20M 2021:233.63M 2022:302.13M 2023:100.12M 2024:209.33M 2025:84.66M 2026:4.00M
  Public Works Department                   2018:36.37M 2019:340.46M 2020:51.68M 2021:74.44M 2022:85.21M 2023:66.00M 2024:197.54M 2025:122.24M 2026:78.75M
  Transportation Department                 2018:1.80M 2019:13.62M 2020:15.52M 2021:4.78M 2022:23.70M 2023:8.29M 2024:52.12M 2025:32.86M 2026:2.51M

## what

FY_CNTRCT_BEGIN_DT: 2023 15%, 2024 15%, 2025 15%, 2022 12%, 2019 11%, 2020 11%, 2021 11%, 2026 10%

FYQ_CNTRCT_BEGIN_DT: Q1 42%, Q2 21%, Q4 19%, Q3 18%

CNTRCT_HDR_VERSION_NBR: 1 94%, 2 4%, 3 1%, 4 0%, 5 0%, 6 0%, 7 0%, 11 0%, 8 0%, 12 0%, 9 0%, 16 0%

CITY_OR_STATE_MBE_WBE_CERTIFIED: Not certified 91%, WBE 5%, MBE 3%, MWBE 1%

CITY_SLBE_SBE_CERTIFIED: Not certified 97%, SLBE 2%, SBE 1%

PROCUREMENT_OR_OTHER_CATEGORY: Procurement Contract 91%, Other Contract 9%

CONTRACT_METHOD_SUBCATEGORY: Competitive 91%, Needs more information 8%, Revenue Contract 0%, Government-to-Government Agree 0%, Limited Competition 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CNTRCT_HDR_CNTRCT_ID | id | 10.1K | 0 | 0000000000000000000051949 50; 0000000000000000000052083 50; 0000000000000000000050153 50; 0000000000000000000054261 50 |
| FY_CNTRCT_BEGIN_DT | category | 8 | 0 | 2023 1.5K; 2024 1.5K; 2025 1.5K; 2022 1.2K |
| FYQ_CNTRCT_BEGIN_DT | category | 4 | 0 | Q1 4.2K; Q2 2.1K; Q4 1.9K; Q3 1.8K |
| CS_DOC_HDR_DEPTID | other | 294 | 859 | 143 2.2K; 101 1.3K; 211000 744; 300 552 |
| DEPT_TBL_DESCR_3_DIGIT | who | 66 | 859 | Procurement 2.5K; Boston Public School Dept 2.2K; Police Department 872; Parks & Recreation Depart 586 |
| CNTRCT_HDR_VERSION_NBR | category | 13 | 0 | 1 9.4K; 2 431; 3 113; 4 33 |
| VENDOR_NAME1 | who | 3.2K | 0 | Liberty Chevrolet 138; Colonial Ford Inc 119; McGovern MHQ Inc. 117; Safeware Inc, 103 |
| CNTRCT_HDR_DESCR | other | 8.0K | 357 | On Call Private Trans EV1 73; Tech Asst Small Bus. in B 72; Curriculum and Instructio 69; EV00010770 PO 65 |
| CNTRCT_HDR_VNDR_CNTRCT_REF | other | 7.4K | 2.2K | Solely for: DOT 71; FFY2023 IIIB RFP 59; EV00014253 IFB 54; EV14253IFB 1st Option to  48 |
| CNTRCT_HDR_CNTRCT_BEGIN_DT | date | 1.9K | 0 | 2025-07-01 325; 2022-07-01 283; 2024-07-01 269; 2023-07-01 269 |
| CNTRCT_HDR_CNTRCT_EXPIRE_DT | date | 1.0K | 11 | 2025-06-30 745; 2023-06-30 724; 2026-06-30 676; 2024-06-30 641 |
| AMT_CNTRCT_MAX | amount | 6.8K | 0 | 25000 142; 50000 142; 30000 96; 20000 87 |
| CS_DOC_HDR_DESCR60 | other | 7.7K | 692 | EV00010770 PO 76; On Call Private Trans EV1 72; Tech Asst Small Bus. in B 71; Curriculum and Instructio 65 |
| CITY_OR_STATE_MBE_WBE_CERTIFIED | category | 4 | 0 | Not certified 9.1K; WBE 472; MBE 334; MWBE 111 |
| CITY_SLBE_SBE_CERTIFIED | category | 3 | 0 | Not certified 9.7K; SLBE 192; SBE 82 |
| PROCUREMENT_OR_OTHER_CATEGORY | category | 2 | 0 | Procurement Contract 9.1K; Other Contract 868 |
| CONTRACT_METHOD_SUBCATEGORY | category | 5 | 0 | Competitive 9.1K; Needs more information 791; Revenue Contract 50; Government-to-Government  27 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:43:39.83400 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0c29034f-51f7-4ad5-8e0f-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | 2eeec032410b3e1ebeee27c9d 10.0K |
