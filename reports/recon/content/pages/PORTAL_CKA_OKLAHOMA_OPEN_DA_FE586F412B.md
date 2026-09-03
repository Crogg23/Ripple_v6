# PORTAL_CKA_OKLAHOMA_OPEN_DA_FE586F412B

rows 1.3K  columns 11  scan 3.2s

roles: amount 1, audit 2, date 1, other 5, who 3

## when

INGESTED_AT
  2026      1.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BALANCE | 1.3K | -7.98M | 34.2K | 73.96M | 1.07B | 6.31B |

## who

AGENCY_NAME by rows
        94  CAPITOL IMPROVEMENT AUTHORITY      
        53  OFFICE OF MANAGEMENT AND ENTERPRISE
        50  OKLAHOMA STATE DEPARTMENT OF HEALTH
        38  DEPARTMENT OF HUMAN SERVICES       
        33  DEPARTMENT OF EDUCATION            
        33  DEPARTMENT OF COMMERCE             
        29  DCAM-OMES                          
        28  DEPARTMENT OF REHABILITATION SERVIC
        26  DEPT OF AGRICULTURE FOOD & FORESTRY
        26  ATTORNEY GENERAL                   
        25  MENTAL HEALTH AND SUBSTANCE ABUSE S
        24  WATER RESOURCES BOARD              
        19  DEPARTMENT OF TRANSPORTATION       
        19  DEPARTMENT OF TOURISM AND RECREATIO
        18  DEPARTMENT OF PUBLIC SAFETY        
        18  DISTRICT ATTORNEYS COUNCIL         
        17  CORPORATION COMMISSION             
        16  OKLAHOMA STATE UNIVERSITY          
        16  REGENTS FOR HIGHER EDUCATION       
        15  CONSERVATION COMMISSION            

AGENCY_NAME by dollars
       1.45B       13 rows  HEALTH CARE AUTHORITY              
       1.13B       19 rows  DEPARTMENT OF TRANSPORTATION       
     808.13M       12 rows  OKLAHOMA TAX COMMISSION            
     262.39M       33 rows  DEPARTMENT OF EDUCATION            
     223.18M       38 rows  DEPARTMENT OF HUMAN SERVICES       
     197.37M       33 rows  DEPARTMENT OF COMMERCE             
     175.53M       10 rows  UNIVERSITY OF OKLAHOMA             
     129.30M        6 rows  UNIV. OF OKLA. HEALTH SCIENCES CENT
     127.19M       94 rows  CAPITOL IMPROVEMENT AUTHORITY      
     111.88M       24 rows  WATER RESOURCES BOARD              
     110.19M        5 rows  OK DEP AEROSPACE & AERONAUTICS     
      99.01M       53 rows  OFFICE OF MANAGEMENT AND ENTERPRISE
      85.28M       12 rows  UNIV. OF CENTRAL OKLA.             
      75.10M       50 rows  OKLAHOMA STATE DEPARTMENT OF HEALTH
      72.19M        1 rows  OK MEDICAL MARIJUANA AUTHORITY     
      42.34M       16 rows  OKLAHOMA STATE UNIVERSITY          
      40.18M       15 rows  CONSERVATION COMMISSION            
      36.70M        2 rows  TEACHERS RETIREMENT SYSTEM         
      36.12M        9 rows  OKLA. BUREAU OF NARCOTICS AND DANGE
      35.97M        2 rows  ENERGY RESOURCES BOARD             

AGENCY_NUMBER by rows
        94  10500     
        53  09000     
        50  34000     
        38  83000     
        33  16000     
        33  26500     
        29  58000     
        28  80500     
        26  04000     
        26  04900     
        25  45200     
        24  83500     
        19  56600     
        19  34500     
        18  58500     
        18  22000     
        17  18500     
        16  60500     
        16  01000     
        15  64500     

AGENCY_NUMBER by dollars
       1.45B       13 rows  80700     
       1.13B       19 rows  34500     
     808.13M       12 rows  69500     
     262.39M       33 rows  26500     
     223.18M       38 rows  83000     
     197.37M       33 rows  16000     
     175.53M       10 rows  76000     
     129.30M        6 rows  77000     
     127.19M       94 rows  10500     
     111.88M       24 rows  83500     
     110.19M        5 rows  06000     
      99.01M       53 rows  09000     
      85.28M       12 rows  12000     
      75.10M       50 rows  34000     
      72.19M        1 rows  45500     
      42.34M       16 rows  01000     
      40.18M       15 rows  64500     
      36.70M        2 rows  71500     
      36.12M        9 rows  47700     
      35.97M        2 rows  35900     

SRC_SHA256 by rows
      1.3K  61838cc909aaf347ce138aaa2ec6e3a870c1895a62d913c9d39ae34967d1bc3c

SRC_SHA256 by dollars
       6.31B     1.3K rows  61838cc909aaf347ce138aaa2ec6e3a870c1895a62d913c9d39ae34967d1

## who x when

AGENCY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  ATTORNEY GENERAL                          2026:27.59M
  CAPITOL IMPROVEMENT AUTHORITY             2026:127.19M
  CONSERVATION COMMISSION                   2026:40.18M
  CORPORATION COMMISSION                    2026:34.63M
  DCAM-OMES                                 2026:0
  DEPARTMENT OF COMMERCE                    2026:197.37M
  DEPARTMENT OF EDUCATION                   2026:262.39M
  DEPARTMENT OF HUMAN SERVICES              2026:223.18M
  DEPARTMENT OF PUBLIC SAFETY               2026:32.45M
  DEPARTMENT OF REHABILITATION SERVIC       2026:16.86M
  DEPARTMENT OF TOURISM AND RECREATIO       2026:26.93M
  DEPARTMENT OF TRANSPORTATION              2026:1.13B
  DEPT OF AGRICULTURE FOOD & FORESTRY       2026:14.08M
  DISTRICT ATTORNEYS COUNCIL                2026:9.97M
  ENERGY RESOURCES BOARD                    2026:35.97M
  HEALTH CARE AUTHORITY                     2026:1.45B
  MENTAL HEALTH AND SUBSTANCE ABUSE S       2026:15.89M
  OFFICE OF MANAGEMENT AND ENTERPRISE       2026:99.01M
  OK DEP AEROSPACE & AERONAUTICS            2026:110.19M
  OK MEDICAL MARIJUANA AUTHORITY            2026:72.19M
  OKLA. BUREAU OF NARCOTICS AND DANGE       2026:36.12M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2026:75.10M
  OKLAHOMA STATE UNIVERSITY                 2026:42.34M
  OKLAHOMA TAX COMMISSION                   2026:808.13M
  REGENTS FOR HIGHER EDUCATION              2026:24.03M
  TEACHERS RETIREMENT SYSTEM                2026:36.70M
  UNIV. OF CENTRAL OKLA.                    2026:85.28M
  UNIV. OF OKLA. HEALTH SCIENCES CENT       2026:129.30M
  UNIVERSITY OF OKLAHOMA                    2026:175.53M
  WATER RESOURCES BOARD                     2026:111.88M

AGENCY_NUMBER by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  01000                                     2026:42.34M
  04000                                     2026:14.08M
  04900                                     2026:27.59M
  06000                                     2026:110.19M
  09000                                     2026:99.01M
  10500                                     2026:127.19M
  12000                                     2026:85.28M
  16000                                     2026:197.37M
  18500                                     2026:34.63M
  22000                                     2026:9.97M
  26500                                     2026:262.39M
  34000                                     2026:75.10M
  34500                                     2026:1.13B
  35900                                     2026:35.97M
  45200                                     2026:15.89M
  45500                                     2026:72.19M
  47700                                     2026:36.12M
  56600                                     2026:26.93M
  58000                                     2026:0
  58500                                     2026:32.45M
  60500                                     2026:24.03M
  64500                                     2026:40.18M
  69500                                     2026:808.13M
  71500                                     2026:36.70M
  76000                                     2026:175.53M
  77000                                     2026:129.30M
  80500                                     2026:16.86M
  80700                                     2026:1.45B
  83000                                     2026:223.18M
  83500                                     2026:111.88M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_NUMBER | who | 167 | 0 | 10500      94; 09000      53; 34000      50; 83000      38 |
| AGENCY_NAME | who | 165 | 0 | CAPITOL IMPROVEMENT AUTHO 94; OFFICE OF MANAGEMENT AND  53; OKLAHOMA STATE DEPARTMENT 50; DEPARTMENT OF HUMAN SERVI 38 |
| CLASS_FUND_NUMBER | other | 213 | 0 | 200        99; 490        68; 210        53; 290        45 |
| CLASS_FUND_DESCRIPTION | other | 943 | 0 | CARES Act 2020            68; Agency Relationship Fund  35; Capital Bond Projects     30; Educational & Gen Operati 28 |
| STATUTORY_REFERENCE | other | 620 | 262 | TITLE 62; § 34.9          66; TITLE 70; SEC. 3901       61; 62 O.S. §34.9             45; TITLE 62; SEC. 41.8       32 |
| CALENDAR_YEAR | other | 1 | 0 | 2023 1.3K |
| CALENDAR_MONTH | other | 1 | 0 | 01 1.3K |
| BALANCE | amount | 820 | 0 | 0.00000000000000 475; 168604.480000000 5; 4021952.92000000 5; 4712.54000000000 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:25:20.16771 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5b5801f5-0862-4534-b693-3 1.3K |
| SRC_SHA256 | who | 1 | 0 | 61838cc909aaf347ce138aaa2 1.3K |
