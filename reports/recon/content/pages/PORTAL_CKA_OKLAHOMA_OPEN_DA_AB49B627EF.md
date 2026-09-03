# PORTAL_CKA_OKLAHOMA_OPEN_DA_AB49B627EF

rows 1.2K  columns 11  scan 3.6s

roles: amount 1, audit 2, date 1, other 5, who 3

## when

INGESTED_AT
  2026      1.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BALANCE | 1.2K | -49.15 | 15.5K | 48.53M | 211.11M | 2.79B |

## who

AGENCY_NAME by rows
        93  CAPITOL IMPROVEMENT AUTHORITY      
        47  OKLAHOMA STATE DEPARTMENT OF HEALTH
        46  OFFICE OF MANAGEMENT AND ENTERPRISE
        34  DEPARTMENT OF HUMAN SERVICES       
        31  DEPARTMENT OF EDUCATION            
        29  DEPARTMENT OF REHABILITATION SERVIC
        29  DCAM-OMES                          
        28  DEPARTMENT OF COMMERCE             
        23  DEPT OF AGRICULTURE FOOD & FORESTRY
        21  WATER RESOURCES BOARD              
        19  ATTORNEY GENERAL                   
        17  DEPARTMENT OF TOURISM AND RECREATIO
        16  OKLAHOMA STATE UNIVERSITY          
        16  DEPARTMENT OF PUBLIC SAFETY        
        16  REGENTS FOR HIGHER EDUCATION       
        16  DEPARTMENT OF TRANSPORTATION       
        16  MENTAL HEALTH AND SUBSTANCE ABUSE S
        16  CORPORATION COMMISSION             
        15  CONSERVATION COMMISSION            
        12  OKLAHOMA MILITARY DEPARTMENT       

AGENCY_NAME by dollars
     661.00M       16 rows  DEPARTMENT OF TRANSPORTATION       
     245.00M       93 rows  CAPITOL IMPROVEMENT AUTHORITY      
     189.47M       21 rows  WATER RESOURCES BOARD              
     130.23M       31 rows  DEPARTMENT OF EDUCATION            
     107.67M       46 rows  OFFICE OF MANAGEMENT AND ENTERPRISE
      97.13M        8 rows  HEALTH CARE AUTHORITY              
      95.72M       34 rows  DEPARTMENT OF HUMAN SERVICES       
      72.22M        6 rows  UNIV. OF OKLA. HEALTH SCIENCES CENT
      68.54M       12 rows  UNIV. OF CENTRAL OKLA.             
      68.15M       10 rows  UNIVERSITY OF OKLAHOMA             
      56.90M       17 rows  DEPARTMENT OF TOURISM AND RECREATIO
      55.57M       47 rows  OKLAHOMA STATE DEPARTMENT OF HEALTH
      48.59M       16 rows  OKLAHOMA STATE UNIVERSITY          
      43.60M       11 rows  DEPARTMENT OF VETERANS AFFAIRS     
      32.77M        8 rows  OKLAHOMA TAX COMMISSION            
      30.22M        2 rows  TEACHERS RETIREMENT SYSTEM         
      27.23M       16 rows  DEPARTMENT OF PUBLIC SAFETY        
      26.71M        4 rows  UNIV. HOSPITALS AUTHORITY          
      26.35M       28 rows  DEPARTMENT OF COMMERCE             
      25.67M       11 rows  NORTHEASTERN STATE UNIVERSITY      

AGENCY_NUMBER by rows
        93  10500
        47  34000
        46  9000
        34  83000
        31  26500
        29  58000
        29  80500
        28  16000
        23  4000
        21  83500
        19  4900
        17  56600
        16  18500
        16  1000
        16  45200
        16  34500
        16  60500
        16  58500
        15  64500
        12  22000

AGENCY_NUMBER by dollars
     661.00M       16 rows  34500
     245.00M       93 rows  10500
     189.47M       21 rows  83500
     130.23M       31 rows  26500
     107.67M       46 rows  9000
      97.13M        8 rows  80700
      95.72M       34 rows  83000
      72.22M        6 rows  77000
      68.54M       12 rows  12000
      68.15M       10 rows  76000
      56.90M       17 rows  56600
      55.57M       47 rows  34000
      48.59M       16 rows  1000
      43.60M       11 rows  65000
      32.77M        8 rows  69500
      30.22M        2 rows  71500
      27.23M       16 rows  58500
      26.71M        4 rows  82500
      26.35M       28 rows  16000
      25.67M       11 rows  48500

SRC_SHA256 by rows
      1.2K  5747efe2eb919f9595d4ec3c96f95992117dedc5747f23b50ec052f34e4f42c8

SRC_SHA256 by dollars
       2.79B     1.2K rows  5747efe2eb919f9595d4ec3c96f95992117dedc5747f23b50ec052f34e4f

## who x when

AGENCY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  ATTORNEY GENERAL                          2026:6.50M
  CAPITOL IMPROVEMENT AUTHORITY             2026:245.00M
  CONSERVATION COMMISSION                   2026:17.60M
  CORPORATION COMMISSION                    2026:22.71M
  DCAM-OMES                                 2026:0
  DEPARTMENT OF COMMERCE                    2026:26.35M
  DEPARTMENT OF EDUCATION                   2026:130.23M
  DEPARTMENT OF HUMAN SERVICES              2026:95.72M
  DEPARTMENT OF PUBLIC SAFETY               2026:27.23M
  DEPARTMENT OF REHABILITATION SERVIC       2026:11.58M
  DEPARTMENT OF TOURISM AND RECREATIO       2026:56.90M
  DEPARTMENT OF TRANSPORTATION              2026:661.00M
  DEPARTMENT OF VETERANS AFFAIRS            2026:43.60M
  DEPT OF AGRICULTURE FOOD & FORESTRY       2026:5.00M
  HEALTH CARE AUTHORITY                     2026:97.13M
  MENTAL HEALTH AND SUBSTANCE ABUSE S       2026:9.39M
  NORTHEASTERN STATE UNIVERSITY             2026:25.67M
  OFFICE OF MANAGEMENT AND ENTERPRISE       2026:107.67M
  OKLAHOMA MILITARY DEPARTMENT              2026:2.57M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2026:55.57M
  OKLAHOMA STATE UNIVERSITY                 2026:48.59M
  OKLAHOMA TAX COMMISSION                   2026:32.77M
  REGENTS FOR HIGHER EDUCATION              2026:8.03M
  TEACHERS RETIREMENT SYSTEM                2026:30.22M
  UNIV. HOSPITALS AUTHORITY                 2026:26.71M
  UNIV. OF CENTRAL OKLA.                    2026:68.54M
  UNIV. OF OKLA. HEALTH SCIENCES CENT       2026:72.22M
  UNIVERSITY OF OKLAHOMA                    2026:68.15M
  WATER RESOURCES BOARD                     2026:189.47M

AGENCY_NUMBER by INGESTED_AT  LOAD STAMP, not an event date, dollars = BALANCE
  1000                                      2026:48.59M
  10500                                     2026:245.00M
  12000                                     2026:68.54M
  16000                                     2026:26.35M
  18500                                     2026:22.71M
  22000                                     2026:10.24M
  26500                                     2026:130.23M
  34000                                     2026:55.57M
  34500                                     2026:661.00M
  4000                                      2026:5.00M
  45200                                     2026:9.39M
  48500                                     2026:25.67M
  4900                                      2026:6.50M
  56600                                     2026:56.90M
  58000                                     2026:0
  58500                                     2026:27.23M
  60500                                     2026:8.03M
  64500                                     2026:17.60M
  65000                                     2026:43.60M
  69500                                     2026:32.77M
  71500                                     2026:30.22M
  76000                                     2026:68.15M
  77000                                     2026:72.22M
  80500                                     2026:11.58M
  80700                                     2026:97.13M
  82500                                     2026:26.71M
  83000                                     2026:95.72M
  83500                                     2026:189.47M
  9000                                      2026:107.67M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_NUMBER | who | 172 | 0 | 10500 93; 34000 47; 9000 46; 83000 34 |
| AGENCY_NAME | who | 168 | 0 | CAPITOL IMPROVEMENT AUTHO 93; OKLAHOMA STATE DEPARTMENT 47; OFFICE OF MANAGEMENT AND  46; DEPARTMENT OF HUMAN SERVI 34 |
| CLASS_FUND_NUMBER | other | 208 | 0 | 200 103; 490 64; 210 53; 290 44 |
| CLASS_FUND_DESCRIPTION | other | 868 | 0 | American Recov. & Reinv.  60; Agency Relationship Fund  35; Capital Bond Projects     30; Educational & Gen Operati 28 |
| STATUTORY_REFERENCE | other | 611 | 170 | TITLE 62; § 34.9          66; TITLE 70; SEC. 3901       61; 62 O.S. §34.9             40; TITLE 62; SEC. 41.8       33 |
| CALENDAR_YEAR | other | 1 | 0 | 2019 1.2K |
| CALENDAR_MONTH | other | 1 | 0 | 1 1.2K |
| BALANCE | amount | 711 | 0 | 0.0 449; 5000.0 4; 2997035.41 4; 4712.54 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:25:04.65695 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | e548cb34-faf4-4b87-8930-7 1.2K |
| SRC_SHA256 | who | 1 | 0 | 5747efe2eb919f9595d4ec3c9 1.2K |
