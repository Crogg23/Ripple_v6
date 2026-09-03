# PORTAL_CKA_INDIANA_DATA_HUB_66A945CF17

rows 5.0K  columns 21  scan 4.0s

roles: amount 4, audit 2, category 3, date 1, other 1, state 1, who 10

## when

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PROVIDER_GEOCODE_LATITUDE | 5.0K | 0 | 39.91 | 41.72 | 44.06 | 200.2K |
| PROVIDER_GEOCODE_LONGITUDE | 5.0K | -105.96 | -86.16 | -84.57 | 0 | -431.4K |
| TOTAL_DOLLAR_AMOUNT_OF_CLAIMS | 5.0K | 0 | 24.1K | 5.11M | 26.17M | 1.13B |
| RECIPIENTS_AVERAGE_TRAVELLED_DISTANCE_MILES | 5.0K | 0.86 | 21.00 | 234.80 | 6.1K | 176.2K |

## who

PROVIDER_NAME by rows
        81  COMMUNITY PHYSICIANS OF INDIANA INC
        70  ST VINCENT MEDICAL GROUP INC
        59  FRANCISCAN PHYSICIAN NETWORK
        49  ST. VINCENT MEDICAL GROUP, INC.
        49  AMERICAN HEALTH NETWORK OF INDIANA LLC
        35  UNIVERSITY FAMILY PHYSICIANS INC
        34  MERIDIAN HEALTH SERVICES CORP
        26  ST VINCENT EVANSVILLE MEDICAL GROUP
        25  PARKVIEW PHYSICIANS GROUP
        24  REID ENT
        23  PLANNED PARENTHOOD OF INDIANA AND KY
        22  IMMEDIADENT
        20  COMMUNITY HOWARD PHYSICIAN NETWORK LLC
        19  CLINIC OF FAMILY MEDICINE
        18  LUTHERAN MEDICAL GROUP LLC
        18  BLUFFTON PHYSICIAN SERVICES LLC
        18  PEDIATRICS CENTER LLC
        18  SINGH                    URMILA
        18  UNIVERSITY OF LOUISVILLE PHYSICIANS INC
        18  AMERICAN HEALTH NETWORK OF IND.LLC

PROVIDER_NAME by dollars
     147.10M       10 rows  S.J.R.M.C. SOUTH BEND CAMPUS, INC.
     104.80M       12 rows  MARION GENERAL HOSPITAL
      93.28M       15 rows  TERRE HAUTE REGIONAL HOSPITAL
      81.76M       18 rows  GOSHEN GENERAL HOSPITAL
      39.17M       13 rows  HENRY COUNTY MEM HOSP
      37.41M        6 rows  REGIONAL MENTAL HEALTH CENTER
      23.55M        6 rows  NORTHEASTERN CENTER -KENDALLVILLE
      21.46M       12 rows  FRANCISCAN HEALTH CRAWFORDSVILLE
      20.63M       12 rows  FT WAYNE MEDICAL ONCOLOGY & HE
      18.95M       12 rows  ADVOCATE CHRIST HOSPITAL & MEDICAL CENT
      16.39M       12 rows  PREMIER HEALTHCARE LLC
      15.12M        6 rows  OAKLAWN PSYCHIATRIC CENTER INC
      13.53M       13 rows  ORTHOPAEDICS NORTHEAST-CLINTON
      12.19M        6 rows  ADULT & CHILD MENTAL HEALTH CTR-CLINICA
      11.48M       12 rows  PULASKI MEMORIAL HOSPITAL
      11.21M       10 rows  ST VINCENT FISHERS HOSPITAL INC
      10.88M        6 rows  PORTER STARKE SERVICES INC MRO SERV (A)
       9.73M       24 rows  REID ENT
       9.66M        8 rows  REHABILITATION UNIT
       9.56M       13 rows  FOUR COUNTY COUNSELING CENTER

TOTAL_NUMBER_OF_RECIPIENTS by rows
        65  22
        62  25
        59  26
        56  27
        54  23
        52  24
        46  31
        44  30
        42  43
        40  35
        40  29
        40  36
        38  37
        38  28
        37  39
        37  34
        34  62
        33  42
        32  50
        32  52

TOTAL_NUMBER_OF_RECIPIENTS by dollars
      34.05M        2 rows  3028
      26.17M        1 rows  3638
      18.71M        1 rows  18363
      17.14M        1 rows  3306
      16.94M        2 rows  2542
      14.94M        2 rows  1337
      13.76M        1 rows  1621
      11.67M        1 rows  13620
      10.90M        1 rows  13321
      10.17M        1 rows  11517
       9.73M        1 rows  16136
       9.38M        1 rows  10791
       9.20M        1 rows  11079
       9.02M        1 rows  1431
       8.85M        1 rows  14678
       8.60M        2 rows  1578
       8.59M        1 rows  13882
       8.50M        1 rows  7781
       8.49M        1 rows  12352
       8.08M        1 rows  1617

PROVIDER_NPI by rows
       135  1144513375
        92  1619105244
        61  1831236272
        59  1225327984
        43  1265689111
        40  1902032832
        35  1043275787
        31  1780634964
        30  1164852539
        30  1932130952
        24  1891743092
        22  1336192665
        22  1518044692
        21  1376586719
        21  1992755490
        21  1720290349
        20  1457610487
        20  1841416369
        20  1164662805
        20  1013358365

PROVIDER_NPI by dollars
     147.10M       10 rows  1841245594
     104.80M       12 rows  1770679201
      93.04M       12 rows  1073550133
      81.76M       18 rows  1740268846
      39.17M       13 rows  1356428429
      37.41M        6 rows  1902043672
      23.55M        6 rows  1720140908
      21.46M       12 rows  1588774558
      20.63M       12 rows  1376533158
      18.95M       12 rows  1548375082
      16.51M       17 rows  1548580764
      15.12M        6 rows  1598847212
      13.53M       13 rows  1740268796
      12.19M        6 rows  1154368512
      11.48M       12 rows  1306928213
      11.21M       10 rows  1881956167
      10.88M        6 rows  1982726220
      10.31M      135 rows  1144513375
      10.02M       43 rows  1265689111
       9.56M       13 rows  1972545945

PROVIDER_PRIME_SPECIALTY by rows
       848  General Dentistry Practitioner                                        
       526  Medical Clinic                                                        
       511  Family Practitioner                                                   
       233  Optometrist                                                           
       200  General Internist                                                     
       182  Acute Care                                                            
       151  General Pediatrician                                                  
       143  Obstetrician/Gynecologist                                             
       141  Radiologist                                                           
       106  Outpatient Mental Health Clinic                                       
       106  Emergency Medicine Practitioner                                       
        99  Ophthalmologist                                                       
        98  Federally Qualified Health Clinic (FQHC)                              
        89  General Surgeon                                                       
        86  Anesthesiologist                                                      
        86  Community Mental Health Center (CMHC)                                 
        81  Urologist                                                             
        79  General Practitioner                                                  
        72  Health Service Provider in Psychology (HSPP)                          
        71  Orthopedic Surgeon                                                    

PROVIDER_PRIME_SPECIALTY by dollars
     558.55M      182 rows  Acute Care                                                  
     122.45M       86 rows  Community Mental Health Center (CMHC)                       
      78.58M      848 rows  General Dentistry Practitioner                              
      50.12M      526 rows  Medical Clinic                                              
      36.71M      106 rows  Emergency Medicine Practitioner                             
      25.08M      511 rows  Family Practitioner                                         
      22.55M       44 rows  Oncologist                                                  
      19.88M      106 rows  Outpatient Mental Health Clinic                             
      18.52M       98 rows  Federally Qualified Health Clinic (FQHC)                    
      15.79M       71 rows  Orthopedic Surgeon                                          
      15.36M      233 rows  Optometrist                                                 
      13.34M       86 rows  Anesthesiologist                                            
      11.87M       64 rows  Pediatric Dentist                                           
      11.54M      143 rows  Obstetrician/Gynecologist                                   
      11.13M       64 rows  Otologist, Laryngologist, Rhinologist                       
      10.63M      200 rows  General Internist                                           
      10.57M       52 rows  Oral Surgeon                                                
       9.35M       67 rows  Independent Lab                                             
       8.93M      151 rows  General Pediatrician                                        
       7.16M      141 rows  Radiologist                                                 

## who x when

PROVIDER_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOLLAR_AMOUNT_OF_CLAIMS
  ADVOCATE CHRIST HOSPITAL & MEDICAL CENT   2026:18.95M
  AMERICAN HEALTH NETWORK OF IND.LLC        2026:381.2K
  AMERICAN HEALTH NETWORK OF INDIANA LLC    2026:2.40M
  BLUFFTON PHYSICIAN SERVICES LLC           2026:2.33M
  CLINIC OF FAMILY MEDICINE                 2026:830.5K
  COMMUNITY HOWARD PHYSICIAN NETWORK LLC    2026:1.16M
  COMMUNITY PHYSICIANS OF INDIANA INC       2026:2.20M
  FRANCISCAN HEALTH CRAWFORDSVILLE          2026:21.46M
  FRANCISCAN PHYSICIAN NETWORK              2026:1.42M
  FT WAYNE MEDICAL ONCOLOGY & HE            2026:20.63M
  GOSHEN GENERAL HOSPITAL                   2026:81.76M
  HENRY COUNTY MEM HOSP                     2026:39.17M
  IMMEDIADENT                               2026:7.14M
  LUTHERAN MEDICAL GROUP LLC                2026:2.29M
  MARION GENERAL HOSPITAL                   2026:104.80M
  MERIDIAN HEALTH SERVICES CORP             2026:6.35M
  NORTHEASTERN CENTER -KENDALLVILLE         2026:23.55M
  PARKVIEW PHYSICIANS GROUP                 2026:930.1K
  PEDIATRICS CENTER LLC                     2026:1.01M
  PLANNED PARENTHOOD OF INDIANA AND KY      2026:2.03M
  REGIONAL MENTAL HEALTH CENTER             2026:37.41M
  REID ENT                                  2026:9.73M
  S.J.R.M.C. SOUTH BEND CAMPUS, INC.        2026:147.10M
  SINGH                    URMILA           2026:547.9K
  ST VINCENT EVANSVILLE MEDICAL GROUP       2026:2.86M
  ST VINCENT MEDICAL GROUP INC              2026:2.49M
  ST. VINCENT MEDICAL GROUP, INC.           2026:6.93M
  TERRE HAUTE REGIONAL HOSPITAL             2026:93.28M
  UNIVERSITY FAMILY PHYSICIANS INC          2026:3.84M
  UNIVERSITY OF LOUISVILLE PHYSICIANS INC   2026:654.1K

TOTAL_NUMBER_OF_RECIPIENTS by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOLLAR_AMOUNT_OF_CLAIMS
  11517                                     2026:10.17M
  13321                                     2026:10.90M
  1337                                      2026:14.94M
  13620                                     2026:11.67M
  1621                                      2026:13.76M
  18363                                     2026:18.71M
  22                                        2026:209.8K
  23                                        2026:211.1K
  24                                        2026:685.1K
  25                                        2026:630.3K
  2542                                      2026:16.94M
  26                                        2026:302.3K
  27                                        2026:297.2K
  28                                        2026:187.9K
  29                                        2026:242.8K
  30                                        2026:269.9K
  3028                                      2026:34.05M
  31                                        2026:422.2K
  3306                                      2026:17.14M
  34                                        2026:168.6K
  35                                        2026:259.5K
  36                                        2026:186.7K
  3638                                      2026:26.17M
  37                                        2026:370.6K
  39                                        2026:285.3K
  42                                        2026:838.8K
  43                                        2026:332.6K
  50                                        2026:497.0K
  52                                        2026:314.2K
  62                                        2026:537.0K

## where

PROVIDER_ADDRESS_STATE: IN 4.8K, KY 108, IL 45, OH 31, GA 10, TX 10, TN 7, NM 6, MN 6, AL 6, FL 5, NY 3

## what

PROVIDER_TYPE: Physician                      48%, Dentist                        19%, Clinic                         15%, Mental Health Provider         5%, Optometrist                    5%, Hospital                       4%, Laboratory                     1%, Radiology                      1%, Public Health Agency           1%, Podiatrist                     1%, Chiropractor                   0%, First Steps Provider           0%

CATEGORY_OF_SERVICES: 06 - Physician Services 34%, 27 - Dental Services - Child 11%, 17 - Clinic Services 11%, 28 - Dental Services - Adult 9%, 38 - EPSDT Services 7%, 26 - Mental Health Services 6%, 31 - Eye Care and Exams 6%, 12 - X-Ray Services 6%, 11 - Lab Services 5%, 03 - Outpatient Services 2%, 01 - Inpatient Services 2%

YEAR: 2016 17%, 2012 17%, 2015 17%, 2013 17%, 2014 16%, 2017 16%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROVIDER_ID | who | 1.1K | 0 | 201060820H      36; 200301630A      35; 200439370A      33; 100162290A      31 |
| PROVIDER_NPI | who | 837 | 0 | 1144513375 135; 1619105244 92; 1831236272 61; 1225327984 59 |
| PROVIDER_NAME | who | 894 | 0 | COMMUNITY PHYSICIANS OF I 81; ST VINCENT MEDICAL GROUP  72; FRANCISCAN PHYSICIAN NETW 59; AMERICAN HEALTH NETWORK O 49 |
| PROVIDER_ADDRESS_STREET_LINE_1 | who | 949 | 0 | Rendering Provider No Add 49; 1001 BROAD RIPPLE AVE     36; 2054 GRANT STREET         35; 202 WALNUT ST             33 |
| PROVIDER_ADDRESS_STREET_LINE_2 | who | 116 | 4.3K | STE A                     41; STE B                     23; STE 100                   22; STE 301                   21 |
| PROVIDER_ADDRESS_CITY | who | 198 | 0 | INDIANAPOLIS              816; FORT WAYNE                211; TERRE HAUTE               150; MUNCIE                    139 |
| PROVIDER_ADDRESS_STATE | state | 14 | 0 | IN 4.8K; KY 108; IL 45; OH 31 |
| PROVIDER_ADDRESS_ZIP_CODE | who | 280 | 0 | 46202 132; 47304 114; 46410 104; 46227 102 |
| PROVIDER_GEOCODE_LATITUDE | amount | 862 | 0 | 39.77058 50; 40.93361 40; 41.683295 36; 39.86974 35 |
| PROVIDER_GEOCODE_LONGITUDE | amount | 864 | 0 | -86.15618 50; -86.25056 36; -86.14169 35; -85.38245 35 |
| PROVIDER_TYPE | category | 16 | 0 | Physician                 2.4K; Dentist                   964; Clinic                    731; Mental Health Provider    264 |
| PROVIDER_PRIME_SPECIALTY | who | 62 | 0 | General Dentistry Practit 848; Medical Clinic            526; Family Practitioner       511; Optometrist               233 |
| CATEGORY_OF_SERVICES | category | 11 | 0 | 06 - Physician Services 1.7K; 27 - Dental Services - Ch 543; 17 - Clinic Services 536; 28 - Dental Services - Ad 467 |
| TOTAL_NUMBER_OF_RECIPIENTS | who | 1.3K | 0 | 22 65; 25 62; 26 59; 27 56 |
| TOTAL_NUMBER_OF_CLAIMS | other | 1.9K | 0 | 43 30; 28 29; 36 29; 37 28 |
| TOTAL_DOLLAR_AMOUNT_OF_CLAIMS | amount | 4.8K | 0 | 24662 25; 37748 25; 16115 25; 24857 25 |
| RECIPIENTS_AVERAGE_TRAVELLED_DISTANCE_MILES | amount | 4.9K | 0 | 4.04047554786621 25; 15.9569729032258 25; 22.529924137931 25; 6.83603130434783 25 |
| YEAR | category | 6 | 0 | 2016 860; 2012 859; 2015 829; 2013 826 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 20:51:16.86804 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | f16c8dd2-f901-472f-ac36-5 5.0K |
| SRC_SHA256 | who | 1 | 0 | 2a8065a8df1d7709fb823e0b9 5.0K |
