# PORTAL_CKA_OKLAHOMA_OPEN_DA_2FB541D487

rows 1.4K  columns 11  scan 3.7s

roles: amount 1, audit 2, date 1, other 5, who 3

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BALANCE | 1.4K | -7.98M | 41.6K | 95.72M | 1.05B | 8.01B |

## who

AGENCY_NAME by rows
        95  CAPITOL IMPROVEMENT AUTHORITY      
        66  OFFICE OF MANAGEMENT AND ENTERPRISE
        52  OKLAHOMA STATE DEPARTMENT OF HEALTH
        40  DEPARTMENT OF HUMAN SERVICES       
        36  DEPARTMENT OF EDUCATION            
        35  DEPARTMENT OF COMMERCE             
        32  ATTORNEY GENERAL                   
        30  MENTAL HEALTH AND SUBSTANCE ABUSE S
        29  DCAM-OMES                          
        29  DEPT OF AGRICULTURE FOOD & FORESTRY
        29  DEPARTMENT OF REHABILITATION SERVIC
        26  WATER RESOURCES BOARD              
        24  DEPARTMENT OF PUBLIC SAFETY        
        23  DEPARTMENT OF TRANSPORTATION       
        22  REGENTS FOR HIGHER EDUCATION       
        21  DEPARTMENT OF TOURISM AND RECREATIO
        19  DISTRICT ATTORNEYS COUNCIL         
        18  CORPORATION COMMISSION             
        17  DEPARTMENT OF EMERGENCY MANAGEMENT 
        17  HEALTH CARE AUTHORITY              

AGENCY_NAME by dollars
       1.52B       95 rows  CAPITOL IMPROVEMENT AUTHORITY      
       1.25B       23 rows  DEPARTMENT OF TRANSPORTATION       
     742.99M       17 rows  HEALTH CARE AUTHORITY              
     385.67M       10 rows  UNIVERSITY OF OKLAHOMA             
     298.83M       11 rows  STATE TREASURER                    
     264.82M       26 rows  WATER RESOURCES BOARD              
     259.73M       16 rows  OKLAHOMA TAX COMMISSION            
     220.75M       66 rows  OFFICE OF MANAGEMENT AND ENTERPRISE
     217.34M       36 rows  DEPARTMENT OF EDUCATION            
     210.06M       35 rows  DEPARTMENT OF COMMERCE             
     170.69M        6 rows  UNIV. OF OKLA. HEALTH SCIENCES CENT
     163.67M       40 rows  DEPARTMENT OF HUMAN SERVICES       
      99.81M       12 rows  DEPT. OF ENVIRONMENTAL QUALITY     
      94.15M        8 rows  OK DEP AEROSPACE & AERONAUTICS     
      89.49M        8 rows  EMPLOYMENT SECURITY COMMISSION     
      85.27M       52 rows  OKLAHOMA STATE DEPARTMENT OF HEALTH
      80.24M        2 rows  OK MEDICAL MARIJUANA AUTHORITY     
      79.19M       13 rows  UNIV. OF CENTRAL OKLA.             
      63.36M        5 rows  OKLAHOMA BROADBAND OFFICE          
      57.34M       17 rows  DEPARTMENT OF EMERGENCY MANAGEMENT 

AGENCY_NUMBER by rows
        95  10500     
        66  09000     
        52  34000     
        40  83000     
        36  26500     
        35  16000     
        32  04900     
        30  45200     
        29  80500     
        29  04000     
        29  58000     
        26  83500     
        24  58500     
        23  34500     
        22  60500     
        21  56600     
        19  22000     
        18  18500     
        17  80700     
        17  30900     

AGENCY_NUMBER by dollars
       1.52B       95 rows  10500     
       1.25B       23 rows  34500     
     742.99M       17 rows  80700     
     385.67M       10 rows  76000     
     298.83M       11 rows  74000     
     264.82M       26 rows  83500     
     259.73M       16 rows  69500     
     220.75M       66 rows  09000     
     217.34M       36 rows  26500     
     210.06M       35 rows  16000     
     170.69M        6 rows  77000     
     163.67M       40 rows  83000     
      99.81M       12 rows  29200     
      94.15M        8 rows  06000     
      89.49M        8 rows  29000     
      85.27M       52 rows  34000     
      80.24M        2 rows  45500     
      79.19M       13 rows  12000     
      63.36M        5 rows  08500     
      57.34M       17 rows  30900     

SRC_SHA256 by rows
      1.4K  e4e94e737674544237a0a99cfca1fcec1937f25f6ba1306be71a3a54e63c3ba4

SRC_SHA256 by dollars
       8.01B     1.4K rows  e4e94e737674544237a0a99cfca1fcec1937f25f6ba1306be71a3a54e63c

## who x when

AGENCY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  ATTORNEY GENERAL                          2026:55.04M
  CAPITOL IMPROVEMENT AUTHORITY             2026:1.52B
  CORPORATION COMMISSION                    2026:33.30M
  DCAM-OMES                                 2026:0
  DEPARTMENT OF COMMERCE                    2026:210.06M
  DEPARTMENT OF EDUCATION                   2026:217.34M
  DEPARTMENT OF EMERGENCY MANAGEMENT        2026:57.34M
  DEPARTMENT OF HUMAN SERVICES              2026:163.67M
  DEPARTMENT OF PUBLIC SAFETY               2026:51.35M
  DEPARTMENT OF REHABILITATION SERVIC       2026:18.06M
  DEPARTMENT OF TOURISM AND RECREATIO       2026:53.35M
  DEPARTMENT OF TRANSPORTATION              2026:1.25B
  DEPT OF AGRICULTURE FOOD & FORESTRY       2026:29.29M
  DEPT. OF ENVIRONMENTAL QUALITY            2026:99.81M
  DISTRICT ATTORNEYS COUNCIL                2026:24.59M
  EMPLOYMENT SECURITY COMMISSION            2026:89.49M
  HEALTH CARE AUTHORITY                     2026:742.99M
  MENTAL HEALTH AND SUBSTANCE ABUSE S       2026:51.63M
  OFFICE OF MANAGEMENT AND ENTERPRISE       2026:220.75M
  OK DEP AEROSPACE & AERONAUTICS            2026:94.15M
  OK MEDICAL MARIJUANA AUTHORITY            2026:80.24M
  OKLAHOMA BROADBAND OFFICE                 2026:63.36M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2026:85.27M
  OKLAHOMA TAX COMMISSION                   2026:259.73M
  REGENTS FOR HIGHER EDUCATION              2026:40.93M
  STATE TREASURER                           2026:298.83M
  UNIV. OF CENTRAL OKLA.                    2026:79.19M
  UNIV. OF OKLA. HEALTH SCIENCES CENT       2026:170.69M
  UNIVERSITY OF OKLAHOMA                    2026:385.67M
  WATER RESOURCES BOARD                     2026:264.82M

AGENCY_NUMBER by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  04000                                     2026:29.29M
  04900                                     2026:55.04M
  06000                                     2026:94.15M
  08500                                     2026:63.36M
  09000                                     2026:220.75M
  10500                                     2026:1.52B
  12000                                     2026:79.19M
  16000                                     2026:210.06M
  18500                                     2026:33.30M
  22000                                     2026:24.59M
  26500                                     2026:217.34M
  29000                                     2026:89.49M
  29200                                     2026:99.81M
  30900                                     2026:57.34M
  34000                                     2026:85.27M
  34500                                     2026:1.25B
  45200                                     2026:51.63M
  45500                                     2026:80.24M
  56600                                     2026:53.35M
  58000                                     2026:0
  58500                                     2026:51.35M
  60500                                     2026:40.93M
  69500                                     2026:259.73M
  74000                                     2026:298.83M
  76000                                     2026:385.67M
  77000                                     2026:170.69M
  80500                                     2026:18.06M
  80700                                     2026:742.99M
  83000                                     2026:163.67M
  83500                                     2026:264.82M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_NUMBER | who | 170 | 0 | 10500      95; 09000      66; 34000      52; 83000      40 |
| AGENCY_NAME | who | 168 | 0 | CAPITOL IMPROVEMENT AUTHO 95; OFFICE OF MANAGEMENT AND  66; OKLAHOMA STATE DEPARTMENT 52; DEPARTMENT OF HUMAN SERVI 40 |
| CLASS_FUND_NUMBER | other | 226 | 0 | 200        102; 490        68; 210        59; 290        46 |
| CLASS_FUND_DESCRIPTION | other | 1.0K | 0 | CARES Act 2020            68; Statewide Recovery Fund   35; Agency Relationship Fund  35; Capital Bond Projects     29 |
| STATUTORY_REFERENCE | other | 621 | 413 | TITLE 62; § 34.9          66; TITLE 70; SEC. 3901       61; 62 O.S. §34.9             45; TITLE 62; SEC. 41.8       32 |
| CALENDAR_YEAR | other | 1 | 0 | 2026 1.4K |
| CALENDAR_MONTH | other | 1 | 0 | 1  1.4K |
| BALANCE | amount | 895 | 0 | 0.00000000000000 532; 270373.650000000 5; 6461816.59000000 5; 4712.54000000000 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:26:21.80536 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 201eba24-a770-439f-b260-8 1.4K |
| SRC_SHA256 | who | 1 | 0 | e4e94e737674544237a0a99cf 1.4K |
