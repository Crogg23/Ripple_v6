# PORTAL_CKA_OKLAHOMA_OPEN_DA_96B2C45728

rows 1.3K  columns 11  scan 4.3s

roles: amount 1, audit 2, date 1, other 5, who 3

## when

INGESTED_AT
  2026      1.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BALANCE | 1.3K | -7.98M | 28.6K | 104.08M | 770.48M | 7.18B |

## who

AGENCY_NAME by rows
        94  CAPITOL IMPROVEMENT AUTHORITY      
        60  OFFICE OF MANAGEMENT AND ENTERPRISE
        52  OKLAHOMA STATE DEPARTMENT OF HEALTH
        39  DEPARTMENT OF HUMAN SERVICES       
        35  DEPARTMENT OF COMMERCE             
        35  DEPARTMENT OF EDUCATION            
        29  DCAM-OMES                          
        29  DEPARTMENT OF REHABILITATION SERVIC
        28  DEPT OF AGRICULTURE FOOD & FORESTRY
        28  MENTAL HEALTH AND SUBSTANCE ABUSE S
        26  ATTORNEY GENERAL                   
        24  WATER RESOURCES BOARD              
        22  DEPARTMENT OF PUBLIC SAFETY        
        20  DEPARTMENT OF TOURISM AND RECREATIO
        20  DEPARTMENT OF TRANSPORTATION       
        18  CORPORATION COMMISSION             
        18  DISTRICT ATTORNEYS COUNCIL         
        18  REGENTS FOR HIGHER EDUCATION       
        16  OKLAHOMA STATE UNIVERSITY          
        15  DEPARTMENT OF EMERGENCY MANAGEMENT 

AGENCY_NAME by dollars
       1.31B       20 rows  DEPARTMENT OF TRANSPORTATION       
       1.28B       13 rows  HEALTH CARE AUTHORITY              
     647.40M       94 rows  CAPITOL IMPROVEMENT AUTHORITY      
     566.59M       35 rows  DEPARTMENT OF EDUCATION            
     308.97M       12 rows  OKLAHOMA TAX COMMISSION            
     283.49M       39 rows  DEPARTMENT OF HUMAN SERVICES       
     273.17M       24 rows  WATER RESOURCES BOARD              
     229.93M       10 rows  UNIVERSITY OF OKLAHOMA             
     220.35M       35 rows  DEPARTMENT OF COMMERCE             
     188.91M        6 rows  UNIV. OF OKLA. HEALTH SCIENCES CENT
     184.61M       60 rows  OFFICE OF MANAGEMENT AND ENTERPRISE
     113.03M        6 rows  OK DEP AEROSPACE & AERONAUTICS     
      81.45M       13 rows  UNIV. OF CENTRAL OKLA.             
      62.94M        2 rows  OK MEDICAL MARIJUANA AUTHORITY     
      62.73M       52 rows  OKLAHOMA STATE DEPARTMENT OF HEALTH
      46.60M       16 rows  OKLAHOMA STATE UNIVERSITY          
      39.55M       15 rows  CONSERVATION COMMISSION            
      39.03M        9 rows  OKLA. BUREAU OF NARCOTICS AND DANGE
      37.91M        7 rows  EMPLOYMENT SECURITY COMMISSION     
      37.01M       28 rows  MENTAL HEALTH AND SUBSTANCE ABUSE S

AGENCY_NUMBER by rows
        94  10500     
        60  09000     
        52  34000     
        39  83000     
        35  26500     
        35  16000     
        29  80500     
        29  58000     
        28  04000     
        28  45200     
        26  04900     
        24  83500     
        22  58500     
        20  34500     
        20  56600     
        18  18500     
        18  22000     
        18  60500     
        16  01000     
        15  64500     

AGENCY_NUMBER by dollars
       1.31B       20 rows  34500     
       1.28B       13 rows  80700     
     647.40M       94 rows  10500     
     566.59M       35 rows  26500     
     308.97M       12 rows  69500     
     283.49M       39 rows  83000     
     273.17M       24 rows  83500     
     229.93M       10 rows  76000     
     220.35M       35 rows  16000     
     188.91M        6 rows  77000     
     184.61M       60 rows  09000     
     113.03M        6 rows  06000     
      81.45M       13 rows  12000     
      62.94M        2 rows  45500     
      62.73M       52 rows  34000     
      46.60M       16 rows  01000     
      39.55M       15 rows  64500     
      39.03M        9 rows  47700     
      37.91M        7 rows  29000     
      37.01M       28 rows  45200     

SRC_SHA256 by rows
      1.3K  b9c9bfa9ffe700dc77f9b1b98acfe4617f8af7b57157d5910623a153f1284d86

SRC_SHA256 by dollars
       7.18B     1.3K rows  b9c9bfa9ffe700dc77f9b1b98acfe4617f8af7b57157d5910623a153f128

## who x when

AGENCY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  ATTORNEY GENERAL                          2026:28.37M
  CAPITOL IMPROVEMENT AUTHORITY             2026:647.40M
  CONSERVATION COMMISSION                   2026:39.55M
  CORPORATION COMMISSION                    2026:33.12M
  DCAM-OMES                                 2026:0
  DEPARTMENT OF COMMERCE                    2026:220.35M
  DEPARTMENT OF EDUCATION                   2026:566.59M
  DEPARTMENT OF EMERGENCY MANAGEMENT        2026:17.45M
  DEPARTMENT OF HUMAN SERVICES              2026:283.49M
  DEPARTMENT OF PUBLIC SAFETY               2026:29.23M
  DEPARTMENT OF REHABILITATION SERVIC       2026:20.72M
  DEPARTMENT OF TOURISM AND RECREATIO       2026:34.86M
  DEPARTMENT OF TRANSPORTATION              2026:1.31B
  DEPT OF AGRICULTURE FOOD & FORESTRY       2026:25.93M
  DISTRICT ATTORNEYS COUNCIL                2026:11.22M
  EMPLOYMENT SECURITY COMMISSION            2026:37.91M
  HEALTH CARE AUTHORITY                     2026:1.28B
  MENTAL HEALTH AND SUBSTANCE ABUSE S       2026:37.01M
  OFFICE OF MANAGEMENT AND ENTERPRISE       2026:184.61M
  OK DEP AEROSPACE & AERONAUTICS            2026:113.03M
  OK MEDICAL MARIJUANA AUTHORITY            2026:62.94M
  OKLA. BUREAU OF NARCOTICS AND DANGE       2026:39.03M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2026:62.73M
  OKLAHOMA STATE UNIVERSITY                 2026:46.60M
  OKLAHOMA TAX COMMISSION                   2026:308.97M
  REGENTS FOR HIGHER EDUCATION              2026:32.16M
  UNIV. OF CENTRAL OKLA.                    2026:81.45M
  UNIV. OF OKLA. HEALTH SCIENCES CENT       2026:188.91M
  UNIVERSITY OF OKLAHOMA                    2026:229.93M
  WATER RESOURCES BOARD                     2026:273.17M

AGENCY_NUMBER by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  01000                                     2026:46.60M
  04000                                     2026:25.93M
  04900                                     2026:28.37M
  06000                                     2026:113.03M
  09000                                     2026:184.61M
  10500                                     2026:647.40M
  12000                                     2026:81.45M
  16000                                     2026:220.35M
  18500                                     2026:33.12M
  22000                                     2026:11.22M
  26500                                     2026:566.59M
  29000                                     2026:37.91M
  34000                                     2026:62.73M
  34500                                     2026:1.31B
  45200                                     2026:37.01M
  45500                                     2026:62.94M
  47700                                     2026:39.03M
  56600                                     2026:34.86M
  58000                                     2026:0
  58500                                     2026:29.23M
  60500                                     2026:32.16M
  64500                                     2026:39.55M
  69500                                     2026:308.97M
  76000                                     2026:229.93M
  77000                                     2026:188.91M
  80500                                     2026:20.72M
  80700                                     2026:1.28B
  83000                                     2026:283.49M
  83500                                     2026:273.17M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_NUMBER | who | 167 | 0 | 10500      94; 09000      60; 34000      52; 83000      39 |
| AGENCY_NAME | who | 165 | 0 | CAPITOL IMPROVEMENT AUTHO 94; OFFICE OF MANAGEMENT AND  60; OKLAHOMA STATE DEPARTMENT 52; DEPARTMENT OF HUMAN SERVI 39 |
| CLASS_FUND_NUMBER | other | 220 | 0 | 200        99; 490        68; 210        56; 205        44 |
| CLASS_FUND_DESCRIPTION | other | 977 | 0 | CARES Act 2020            68; Agency Relationship Fund  35; Statewide Recovery Fund   30; Capital Bond Projects     29 |
| STATUTORY_REFERENCE | other | 618 | 330 | TITLE 62; § 34.9          66; TITLE 70; SEC. 3901       61; 62 O.S. §34.9             45; TITLE 62; SEC. 41.8       32 |
| CALENDAR_YEAR | other | 1 | 0 | 2024 1.3K |
| CALENDAR_MONTH | other | 1 | 0 | 01 1.3K |
| BALANCE | amount | 868 | 0 | 0.00000000000000 500; 2072146.90000000 5; 4440614.79000000 5; 4712.54000000000 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:25:33.89130 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | ebff09df-8e24-4336-a4bd-5 1.3K |
| SRC_SHA256 | who | 1 | 0 | b9c9bfa9ffe700dc77f9b1b98 1.3K |
