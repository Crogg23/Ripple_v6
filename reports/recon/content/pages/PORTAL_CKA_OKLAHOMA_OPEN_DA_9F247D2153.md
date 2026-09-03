# PORTAL_CKA_OKLAHOMA_OPEN_DA_9F247D2153

rows 1.1K  columns 11  scan 4.4s

roles: amount 1, audit 2, date 1, other 5, who 3

## when

INGESTED_AT
  2026      1.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POSTED_TOTAL_AMOUNT | 1.1K | -127.53M | 69.3K | 51.53M | 200.29M | 2.31B |

## who

OCP_AGNCY_NAME by rows
        83  CAPITOL IMPROVEMENT AUTHORITY
        41  OKLAHOMA STATE DEPARTMENT OF HEALTH
        37  STATE TREASURER
        34  DEPARTMENT OF HUMAN SERVICES
        28  DCAM-OMES
        26  DEPARTMENT OF COMMERCE
        25  DEPARTMENT OF REHABILITATION SERVICES
        24  DEPARTMENT OF EDUCATION
        20  WATER RESOURCES BOARD
        17  DEPT OF AGRICULTURE FOOD & FORESTRY
        17  DEPARTMENT OF TRANSPORTATION
        17  REGENTS FOR HIGHER EDUCATION
        16  DEPARTMENT OF TOURISM AND RECREATION
        16  OKLAHOMA STATE UNIVERSITY
        16  MENTAL HEALTH AND SUBSTANCE ABUSE SERV.
        16  CORPORATION COMMISSION
        14  ATTORNEY GENERAL
        13  DISTRICT ATTORNEYS COUNCIL
        13  CONSERVATION COMMISSION
        13  DEPARTMENT OF PUBLIC SAFETY

OCP_AGNCY_NAME by dollars
     397.50M       17 rows  DEPARTMENT OF TRANSPORTATION
     184.10M        9 rows  HEALTH CARE AUTHORITY
     151.61M        7 rows  UNIV. OF OKLA. HEALTH SCIENCES CENTER
     139.40M       10 rows  UNIVERSITY OF OKLAHOMA
     114.45M       83 rows  CAPITOL IMPROVEMENT AUTHORITY
      88.69M       34 rows  DEPARTMENT OF HUMAN SERVICES
      84.43M       28 rows  DCAM-OMES
      74.94M       17 rows  REGENTS FOR HIGHER EDUCATION
      62.84M       16 rows  DEPARTMENT OF TOURISM AND RECREATION
      57.06M       20 rows  WATER RESOURCES BOARD
      43.97M       37 rows  STATE TREASURER
      40.04M       41 rows  OKLAHOMA STATE DEPARTMENT OF HEALTH
      37.68M       16 rows  OKLAHOMA STATE UNIVERSITY
      35.55M       12 rows  UNIV. OF CENTRAL OKLA.
      34.60M        2 rows  TEACHERS RETIREMENT SYSTEM
      33.29M       11 rows  NORTHEASTERN STATE UNIVERSITY
      31.49M       13 rows  DEPARTMENT OF PUBLIC SAFETY
      30.59M        3 rows  CNTR. FOR ADVANC. OF SCIENCE/TECHNOLOGY
      30.59M        8 rows  OKLAHOMA TAX COMMISSION
      28.67M       10 rows  OFFICE OF MANAGEMENT AND ENTERPRISE SERV

BUSINESS_UNIT by rows
        83  10500
        41  34000
        37  74000
        34  83000
        28  58000
        26  16000
        25  80500
        24  26500
        20  83500
        17  60500
        17  4000
        17  34500
        16  45200
        16  1000
        16  56600
        16  18500
        14  4900
        13  22000
        13  64500
        13  58500

BUSINESS_UNIT by dollars
     397.50M       17 rows  34500
     184.10M        9 rows  80700
     151.61M        7 rows  77000
     139.40M       10 rows  76000
     114.45M       83 rows  10500
      88.69M       34 rows  83000
      84.43M       28 rows  58000
      74.94M       17 rows  60500
      62.84M       16 rows  56600
      57.06M       20 rows  83500
      43.97M       37 rows  74000
      40.04M       41 rows  34000
      37.68M       16 rows  1000
      35.55M       12 rows  12000
      34.60M        2 rows  71500
      33.29M       11 rows  48500
      31.49M       13 rows  58500
      30.59M        3 rows  62800
      30.59M        8 rows  69500
      28.67M       10 rows  9000

SRC_SHA256 by rows
      1.1K  2b6579edde04f6b3e8812a84034bf0859e152753887292b64d0d4c47897d2250

SRC_SHA256 by dollars
       2.31B     1.1K rows  2b6579edde04f6b3e8812a84034bf0859e152753887292b64d0d4c47897d

## who x when

OCP_AGNCY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POSTED_TOTAL_AMOUNT
  ATTORNEY GENERAL                          2026:5.89M
  CAPITOL IMPROVEMENT AUTHORITY             2026:114.45M
  CNTR. FOR ADVANC. OF SCIENCE/TECHNOLOGY   2026:30.59M
  CONSERVATION COMMISSION                   2026:15.11M
  CORPORATION COMMISSION                    2026:14.51M
  DCAM-OMES                                 2026:84.43M
  DEPARTMENT OF COMMERCE                    2026:20.37M
  DEPARTMENT OF EDUCATION                   2026:-28.06M
  DEPARTMENT OF HUMAN SERVICES              2026:88.69M
  DEPARTMENT OF PUBLIC SAFETY               2026:31.49M
  DEPARTMENT OF REHABILITATION SERVICES     2026:10.31M
  DEPARTMENT OF TOURISM AND RECREATION      2026:62.84M
  DEPARTMENT OF TRANSPORTATION              2026:397.50M
  DEPT OF AGRICULTURE FOOD & FORESTRY       2026:5.05M
  DISTRICT ATTORNEYS COUNCIL                2026:22.14M
  HEALTH CARE AUTHORITY                     2026:184.10M
  MENTAL HEALTH AND SUBSTANCE ABUSE SERV.   2026:8.23M
  NORTHEASTERN STATE UNIVERSITY             2026:33.29M
  OFFICE OF MANAGEMENT AND ENTERPRISE SERV  2026:28.67M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2026:40.04M
  OKLAHOMA STATE UNIVERSITY                 2026:37.68M
  OKLAHOMA TAX COMMISSION                   2026:30.59M
  REGENTS FOR HIGHER EDUCATION              2026:74.94M
  STATE TREASURER                           2026:43.97M
  TEACHERS RETIREMENT SYSTEM                2026:34.60M
  UNIV. OF CENTRAL OKLA.                    2026:35.55M
  UNIV. OF OKLA. HEALTH SCIENCES CENTER     2026:151.61M
  UNIVERSITY OF OKLAHOMA                    2026:139.40M
  WATER RESOURCES BOARD                     2026:57.06M

BUSINESS_UNIT by INGESTED_AT  LOAD STAMP, not an event date, dollars = POSTED_TOTAL_AMOUNT
  1000                                      2026:37.68M
  10500                                     2026:114.45M
  12000                                     2026:35.55M
  16000                                     2026:20.37M
  18500                                     2026:14.51M
  22000                                     2026:22.14M
  26500                                     2026:-28.06M
  34000                                     2026:40.04M
  34500                                     2026:397.50M
  4000                                      2026:5.05M
  45200                                     2026:8.23M
  48500                                     2026:33.29M
  4900                                      2026:5.89M
  56600                                     2026:62.84M
  58000                                     2026:84.43M
  58500                                     2026:31.49M
  60500                                     2026:74.94M
  62800                                     2026:30.59M
  64500                                     2026:15.11M
  69500                                     2026:30.59M
  71500                                     2026:34.60M
  74000                                     2026:43.97M
  76000                                     2026:139.40M
  77000                                     2026:151.61M
  80500                                     2026:10.31M
  80700                                     2026:184.10M
  83000                                     2026:88.69M
  83500                                     2026:57.06M
  9000                                      2026:28.67M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_UNIT | who | 176 | 0 | 10500 83; 34000 41; 74000 37; 83000 34 |
| OCP_AGNCY_NAME | who | 174 | 0 | CAPITOL IMPROVEMENT AUTHO 83; OKLAHOMA STATE DEPARTMENT 41; STATE TREASURER 37; DEPARTMENT OF HUMAN SERVI 34 |
| CLASS_FUND | other | 223 | 0 | 200 104; 490 66; 210 46; 290 42 |
| OCP_CLASS_DESCR | other | 779 | 0 | American Recov. & Reinv.  62; Agency Relationship Fund 34; Capital Improvements Rev  30; Revolving Fund 29 |
| OCP_STATUTORY_REF | other | 574 | 163 | TITLE 70, SEC. 3901 62; TITLE 62, SEC. 41.8 33; TITLE 70, SEC. 3904 25; TITLE 62, SEC 34.48, 34.9 23 |
| YEAR | other | 1 | 0 | 2018 1.1K |
| MONTH | other | 1 | 0 | 1 1.1K |
| POSTED_TOTAL_AMOUNT | amount | 821 | 0 | 0.0 276; 5000.0 5; 70100.4 5; 1034115.81 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:24:36.15507 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | ea16f601-77c5-4a03-a5e7-1 1.1K |
| SRC_SHA256 | who | 1 | 0 | 2b6579edde04f6b3e8812a840 1.1K |
