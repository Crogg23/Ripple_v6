# PORTAL_CKA_OKLAHOMA_OPEN_DA_840020A9DE

rows 1.2K  columns 11  scan 3.9s

roles: amount 1, audit 2, date 1, other 5, who 3

## when

INGESTED_AT
  2026      1.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POSTED_TOTAL_AMT | 1.2K | -19.0K | 10.9K | 39.41M | 266.51M | 2.26B |

## who

OCP_AGNCY_NAME by rows
        94  CAPITOL IMPROVEMENT AUTHORITY
        44  OKLAHOMA STATE DEPARTMENT OF HEALTH
        43  OFFICE OF MANAGEMENT AND ENTERPRISE SERV
        34  DEPARTMENT OF HUMAN SERVICES
        29  DEPARTMENT OF EDUCATION
        29  DCAM-OMES
        28  DEPARTMENT OF COMMERCE
        28  DEPARTMENT OF REHABILITATION SERVICES
        23  DEPT OF AGRICULTURE FOOD & FORESTRY
        21  WATER RESOURCES BOARD
        18  ATTORNEY GENERAL
        16  OKLAHOMA STATE UNIVERSITY
        16  DEPARTMENT OF TOURISM AND RECREATION
        16  MENTAL HEALTH AND SUBSTANCE ABUSE SERV.
        16  CORPORATION COMMISSION
        16  REGENTS FOR HIGHER EDUCATION
        16  DEPARTMENT OF TRANSPORTATION
        15  DEPARTMENT OF PUBLIC SAFETY
        14  CONSERVATION COMMISSION
        12  UNIV. OF CENTRAL OKLA.

OCP_AGNCY_NAME by dollars
     531.85M       16 rows  DEPARTMENT OF TRANSPORTATION
     170.98M       94 rows  CAPITOL IMPROVEMENT AUTHORITY
     113.22M       21 rows  WATER RESOURCES BOARD
     101.44M       43 rows  OFFICE OF MANAGEMENT AND ENTERPRISE SERV
     100.93M       10 rows  UNIVERSITY OF OKLAHOMA
      89.93M        6 rows  UNIV. OF OKLA. HEALTH SCIENCES CENTER
      82.70M       16 rows  OKLAHOMA STATE UNIVERSITY
      64.64M        9 rows  HEALTH CARE AUTHORITY
      53.00M       12 rows  UNIV. OF CENTRAL OKLA.
      49.94M       16 rows  DEPARTMENT OF TOURISM AND RECREATION
      48.43M       29 rows  DEPARTMENT OF EDUCATION
      42.44M       34 rows  DEPARTMENT OF HUMAN SERVICES
      36.74M       11 rows  DEPARTMENT OF VETERANS AFFAIRS
      34.05M       28 rows  DEPARTMENT OF COMMERCE
      28.74M        8 rows  OKLAHOMA TAX COMMISSION
      27.47M       15 rows  DEPARTMENT OF PUBLIC SAFETY
      26.55M       44 rows  OKLAHOMA STATE DEPARTMENT OF HEALTH
      21.63M        3 rows  COMM. OF THE LAND OFFICE
      21.01M        2 rows  TEACHERS RETIREMENT SYSTEM
      20.85M       11 rows  NORTHEASTERN STATE UNIVERSITY

BUSINESS_UNIT by rows
        94  10500
        44  34000
        43  9000
        34  83000
        29  58000
        29  26500
        28  16000
        28  80500
        23  4000
        21  83500
        18  4900
        16  45200
        16  1000
        16  60500
        16  34500
        16  18500
        16  56600
        15  58500
        14  64500
        12  12000

BUSINESS_UNIT by dollars
     531.85M       16 rows  34500
     170.98M       94 rows  10500
     113.22M       21 rows  83500
     101.44M       43 rows  9000
     100.93M       10 rows  76000
      89.93M        6 rows  77000
      82.70M       16 rows  1000
      64.64M        9 rows  80700
      53.00M       12 rows  12000
      49.94M       16 rows  56600
      48.43M       29 rows  26500
      42.44M       34 rows  83000
      36.74M       11 rows  65000
      34.05M       28 rows  16000
      28.74M        8 rows  69500
      27.47M       15 rows  58500
      26.55M       44 rows  34000
      21.63M        3 rows  41000
      21.01M        2 rows  71500
      20.85M       11 rows  48500

SRC_SHA256 by rows
      1.2K  3e56d5c90ff745426a4d40a77c40a32b1894e3871900e4d6d8b763fbf6cfeef3

SRC_SHA256 by dollars
       2.26B     1.2K rows  3e56d5c90ff745426a4d40a77c40a32b1894e3871900e4d6d8b763fbf6cf

## who x when

OCP_AGNCY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POSTED_TOTAL_AMT
  ATTORNEY GENERAL                          2026:3.09M
  CAPITOL IMPROVEMENT AUTHORITY             2026:170.98M
  COMM. OF THE LAND OFFICE                  2026:21.63M
  CONSERVATION COMMISSION                   2026:18.72M
  CORPORATION COMMISSION                    2026:16.07M
  DCAM-OMES                                 2026:0
  DEPARTMENT OF COMMERCE                    2026:34.05M
  DEPARTMENT OF EDUCATION                   2026:48.43M
  DEPARTMENT OF HUMAN SERVICES              2026:42.44M
  DEPARTMENT OF PUBLIC SAFETY               2026:27.47M
  DEPARTMENT OF REHABILITATION SERVICES     2026:10.60M
  DEPARTMENT OF TOURISM AND RECREATION      2026:49.94M
  DEPARTMENT OF TRANSPORTATION              2026:531.85M
  DEPARTMENT OF VETERANS AFFAIRS            2026:36.74M
  DEPT OF AGRICULTURE FOOD & FORESTRY       2026:4.75M
  HEALTH CARE AUTHORITY                     2026:64.64M
  MENTAL HEALTH AND SUBSTANCE ABUSE SERV.   2026:16.86M
  NORTHEASTERN STATE UNIVERSITY             2026:20.85M
  OFFICE OF MANAGEMENT AND ENTERPRISE SERV  2026:101.44M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2026:26.55M
  OKLAHOMA STATE UNIVERSITY                 2026:82.70M
  OKLAHOMA TAX COMMISSION                   2026:28.74M
  REGENTS FOR HIGHER EDUCATION              2026:3.89M
  TEACHERS RETIREMENT SYSTEM                2026:21.01M
  UNIV. OF CENTRAL OKLA.                    2026:53.00M
  UNIV. OF OKLA. HEALTH SCIENCES CENTER     2026:89.93M
  UNIVERSITY OF OKLAHOMA                    2026:100.93M
  WATER RESOURCES BOARD                     2026:113.22M

BUSINESS_UNIT by INGESTED_AT  LOAD STAMP, not an event date, dollars = POSTED_TOTAL_AMT
  1000                                      2026:82.70M
  10500                                     2026:170.98M
  12000                                     2026:53.00M
  16000                                     2026:34.05M
  18500                                     2026:16.07M
  26500                                     2026:48.43M
  34000                                     2026:26.55M
  34500                                     2026:531.85M
  4000                                      2026:4.75M
  41000                                     2026:21.63M
  45200                                     2026:16.86M
  48500                                     2026:20.85M
  4900                                      2026:3.09M
  56600                                     2026:49.94M
  58000                                     2026:0
  58500                                     2026:27.47M
  60500                                     2026:3.89M
  64500                                     2026:18.72M
  65000                                     2026:36.74M
  69500                                     2026:28.74M
  71500                                     2026:21.01M
  76000                                     2026:100.93M
  77000                                     2026:89.93M
  80500                                     2026:10.60M
  80700                                     2026:64.64M
  83000                                     2026:42.44M
  83500                                     2026:113.22M
  9000                                      2026:101.44M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_UNIT | who | 180 | 0 | 10500 94; 34000 44; 9000 43; 83000 34 |
| OCP_AGNCY_NAME | who | 178 | 0 | CAPITOL IMPROVEMENT AUTHO 94; OKLAHOMA STATE DEPARTMENT 44; OFFICE OF MANAGEMENT AND  43; DEPARTMENT OF HUMAN SERVI 34 |
| CLASS_FUND | other | 206 | 0 | 200 106; 490 64; 210 52; 205 46 |
| CLASS_DESCR | other | 837 | 0 | American Recov. & Reinv.  60; Agency Relationship Fund 35; Capital Bond Projects 30; Educational & Gen Operati 28 |
| OCP_STATUTORY_REF | other | 563 | 278 | TITLE 70, SEC. 3901 61; TITLE 62, SEC. 41.8 33; TITLE 70, SEC. 3904 25; TITLE 62, SEC 34.48, 34.9 24 |
| C_2017 | other | 1 | 0 | 2017 1.2K |
| C_12 | other | 1 | 0 | 12 1.2K |
| POSTED_TOTAL_AMT | amount | 704 | 0 | 0.0 464; 143331.97 4; 3442804.25 4; 4712.54 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:24:59.15671 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 14b3e49d-b807-4c71-a652-9 1.2K |
| SRC_SHA256 | who | 1 | 0 | 3e56d5c90ff745426a4d40a77 1.2K |
