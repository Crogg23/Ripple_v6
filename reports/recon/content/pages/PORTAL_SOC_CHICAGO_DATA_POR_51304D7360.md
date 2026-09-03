# PORTAL_SOC_CHICAGO_DATA_POR_51304D7360

rows 2.0K  columns 28  scan 4.8s

roles: amount 8, audit 2, category 6, date 3, other 7, who 3

## when

ISSUED_DATE
  2004         1  
  2006         1  
  2011       270  ###########################
  2012       274  ############################
  2013       292  #############################
  2014       285  #############################
  2015       298  ##############################
  2016       206  #####################
  2017       166  #################
  2018        80  ########
  2019        51  #####
  2020        26  ###
  2021        15  ##
  2022        21  ##
  2023         9  #
  2024         3  
  2025         2  

LAST_HEARING_DATE
  2001         2  
  2011       209  ####################
  2012       278  ###########################
  2013       287  ############################
  2014       308  ##############################
  2015       291  ############################
  2016       206  ####################
  2017       186  ##################
  2018        97  #########
  2019        50  #####
  2020        35  ###
  2021        15  #
  2022        19  ##
  2023        12  #
  2024         3  
  2025         2  

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_FINES | 2.0K | 0 | 0 | 4.3K | 8.5K | 898.5K |
| INTEREST_AMOUNT | 2.0K | 0 | 0 | 4.5K | 10.7K | 319.2K |
| COLLECTION_COSTS_OR_ATTORNEY_FEES | 2.0K | 0 | 0 | 1.2K | 2.4K | 195.3K |
| COURT_COST | 2.0K | 0 | 0 | 54.18 | 496 | 5.6K |
| ORIGINAL_TOTAL_AMOUNT_DUE | 2.0K | 0 | 0 | 10.5K | 21.7K | 1.44M |
| CURRENT_AMOUNT_DUE | 2.0K | -1.6K | 0 | 10.4K | 21.5K | 567.4K |

## who

ENTITY_OR_PERSON_S by rows
       199  BANK OF AMERICA, 
       149  WELLS FARGO BANK, 
        97  US BANK, 
        94  DEUTSCHE BANK, 
        88  JP MORGAN CHASE BANK, 
        61  BANK OF NEW YORK MELLON, 
        54  CITI MORTGAGE INC, 
        53  WELLS FARGO BANK NA, 
        48  FEDERAL NATL MTG ASSN, 
        44  DEUTSCHE BANK NATL TRUST CO, 
        41  BAYVIEW LOAN SERVICING LLC, 
        40  OCWEN LOAN SERVICING LLC, 
        38  HSBC BANK, 
        34  NATIONWIDE REO LLC, 
        33  US BANK NA, 
        31  MIDFIRST BANK, 
        29  DEUTSCHE BANK NATL TRUST, 
        27  FANNIE MAE, 
        26  CITI MORTGAGE, 
        25  BANK OF AMERICA NA, 

ENTITY_OR_PERSON_S by dollars
       66.0K      149 rows  WELLS FARGO BANK, 
       49.1K       34 rows  NATIONWIDE REO LLC, 
       43.5K       94 rows  DEUTSCHE BANK, 
       42.0K       61 rows  BANK OF NEW YORK MELLON, 
       41.7K       18 rows  CHASE REO GROUP LLC, 
       38.0K       48 rows  FEDERAL NATL MTG ASSN, 
       35.2K       44 rows  DEUTSCHE BANK NATL TRUST CO, 
       31.2K       88 rows  JP MORGAN CHASE BANK, 
       30.1K       23 rows  REO PARTNERS LLC, 
       28.4K        8 rows  CHASE REO GROUP LLC C/O ANTWAN REID, 
       23.7K      199 rows  BANK OF AMERICA, 
       23.0K        6 rows  REO DIRECT LLC, 
       22.4K       38 rows  HSBC BANK, 
       19.6K       29 rows  DEUTSCHE BANK NATL TRUST, 
       19.6K       24 rows  HSBC BANK USA, 
       17.1K       97 rows  US BANK, 
       16.0K       53 rows  WELLS FARGO BANK NA, 
       13.6K       21 rows  HOUSING URBAN DEVELOPMENT, 
       13.3K       18 rows  DEUTSCHE BANK AND TRUST, 
       13.0K        9 rows  NATIONAL ASSET MANAGEMENT GROUP LLC, 

LOCATION by rows
       129  nan
        18  {"type": "Point", "coordinates": [-87.6498292763393, 41.78117319861422
        15  {"type": "Point", "coordinates": [-87.66079340228376, 41.7826731435223
         9  {"type": "Point", "coordinates": [-87.67745691931087, 41.8013066029604
         9  {"type": "Point", "coordinates": [-87.67018864176725, 41.7705026763619
         8  {"type": "Point", "coordinates": [-87.66611860279855, 41.8004205976400
         8  {"type": "Point", "coordinates": [-87.67773132361941, 41.8010832769825
         8  {"type": "Point", "coordinates": [-87.64783806114086, 41.7971283042222
         8  {"type": "Point", "coordinates": [-87.70616158096952, 41.7824549813490
         7  {"type": "Point", "coordinates": [-87.71223678968778, 41.7807682240264
         7  {"type": "Point", "coordinates": [-87.6732573132849, 41.79488794853346
         7  {"type": "Point", "coordinates": [-87.75286212843703, 41.8105483486666
         7  {"type": "Point", "coordinates": [-87.66334634808065, 41.7986890141114
         7  {"type": "Point", "coordinates": [-87.67455096599359, 41.7703581085261
         7  {"type": "Point", "coordinates": [-87.71706003443005, 41.7993511631648
         7  {"type": "Point", "coordinates": [-87.6862588167713, 41.7801062114115]
         7  {"type": "Point", "coordinates": [-87.68487505101264, 41.7743191443668
         7  {"type": "Point", "coordinates": [-87.67296949154296, 41.7950666791175
         6  {"type": "Point", "coordinates": [-87.66583755922996, 41.7898850231597
         6  {"type": "Point", "coordinates": [-87.71939898478763, 41.7861037745308

LOCATION by dollars
       61.9K       18 rows  {"type": "Point", "coordinates": [-87.6498292763393, 41.7811
       59.3K      129 rows  nan
       26.6K        8 rows  {"type": "Point", "coordinates": [-87.64783806114086, 41.797
       25.8K        7 rows  {"type": "Point", "coordinates": [-87.66334634808065, 41.798
       21.5K       15 rows  {"type": "Point", "coordinates": [-87.66079340228376, 41.782
       17.1K        6 rows  {"type": "Point", "coordinates": [-87.6488212668545, 41.7892
       15.8K        9 rows  {"type": "Point", "coordinates": [-87.67018864176725, 41.770
       12.7K        7 rows  {"type": "Point", "coordinates": [-87.67455096599359, 41.770
       12.0K        3 rows  {"type": "Point", "coordinates": [-87.70142227564104, 41.799
       11.4K        3 rows  {"type": "Point", "coordinates": [-87.64273278227675, 41.800
       11.4K        6 rows  {"type": "Point", "coordinates": [-87.67325551184871, 41.794
        9.9K        8 rows  {"type": "Point", "coordinates": [-87.66611860279855, 41.800
        9.8K        7 rows  {"type": "Point", "coordinates": [-87.67296949154296, 41.795
        9.5K        6 rows  {"type": "Point", "coordinates": [-87.64186433780255, 41.809
        8.9K        4 rows  {"type": "Point", "coordinates": [-87.69895413687149, 41.798
        8.6K        6 rows  {"type": "Point", "coordinates": [-87.66583755922996, 41.789
        8.6K        2 rows  {"type": "Point", "coordinates": [-87.67133993233746, 41.778
        8.6K        2 rows  {"type": "Point", "coordinates": [-87.69047456682881, 41.765
        8.5K        1 rows  {"type": "Point", "coordinates": [-87.75101485856864, 41.921
        8.4K        5 rows  {"type": "Point", "coordinates": [-87.64710216075217, 41.800

SRC_SHA256 by rows
      2.0K  821762db73792296a4c010dd1bc729c8952613766ec848adeac53be713526f43

SRC_SHA256 by dollars
      898.5K     2.0K rows  821762db73792296a4c010dd1bc729c8952613766ec848adeac53be71352

## who x when

ENTITY_OR_PERSON_S by ISSUED_DATE, dollars = TOTAL_FINES
  BANK OF AMERICA NA,                       2012:0 2013:0 2014:0 2015:0 2017:5.0K 2018:0 2019:0
  BANK OF AMERICA,                          2011:0 2012:1.3K 2013:1.4K 2014:2.6K 2015:4.2K 2016:13.0K 2017:1.2K 2018:0 2019:0 2020:0 2021:0 2022:0
  BANK OF NEW YORK MELLON,                  2011:2.8K 2012:2.6K 2013:6.8K 2014:600 2015:4.3K 2016:6.9K 2017:0 2019:0 2020:18.0K 2021:0 2022:0
  BAYVIEW LOAN SERVICING LLC,               2011:900 2012:300 2013:0 2014:700 2015:0 2016:0 2017:0 2018:0 2020:0
  CHASE REO GROUP LLC C/O ANTWAN REID,      2012:2.6K 2013:8.6K 2014:8.6K 2016:8.6K
  CHASE REO GROUP LLC,                      2012:5.6K 2013:4.3K 2014:0 2015:8.6K 2016:17.2K 2018:6.0K
  CITI MORTGAGE INC,                        2011:300 2012:0 2013:400 2014:1.4K 2015:0 2016:0 2017:1.3K 2018:0 2019:0
  CITI MORTGAGE,                            2011:0 2012:4.6K 2013:3.3K 2014:0 2015:0 2017:0 2018:0
  DEUTSCHE BANK AND TRUST,                  2012:7.4K 2013:5.9K 2014:0
  DEUTSCHE BANK NATL TRUST CO,              2011:1.3K 2012:8.9K 2013:3.5K 2014:9.1K 2015:5.6K 2016:2.8K 2017:0 2018:4.0K 2022:0
  DEUTSCHE BANK NATL TRUST,                 2004:0 2011:5.6K 2012:10.2K 2013:1.0K 2014:2.8K 2015:0 2016:0
  DEUTSCHE BANK,                            2011:13.1K 2012:19.8K 2013:2.0K 2014:0 2015:1.3K 2016:0 2017:1.3K 2018:6.0K 2019:0 2020:0 2021:0 2022:0
  FANNIE MAE,                               2011:0 2012:0 2013:0 2014:5.6K 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0
  FEDERAL NATL MTG ASSN,                    2011:0 2012:18.0K 2013:11.4K 2014:4.3K 2015:0 2016:4.3K 2017:0 2018:0 2021:0
  HOUSING URBAN DEVELOPMENT,                2011:0 2012:7.6K 2013:0 2014:0 2016:0 2017:0 2018:0 2022:6.0K
  HSBC BANK USA,                            2011:0 2014:700 2015:8.6K 2016:4.3K 2017:0 2018:0 2019:0 2020:0 2021:6.0K
  HSBC BANK,                                2011:0 2012:8.2K 2013:8.2K 2014:0 2015:0 2016:0 2017:0 2018:6.0K 2022:0
  JP MORGAN CHASE BANK,                     2011:2.8K 2012:800 2013:2.5K 2014:1.3K 2015:0 2016:4.2K 2017:13.6K 2018:0 2019:0 2024:6.0K
  MIDFIRST BANK,                            2012:0 2013:0 2014:0 2015:700 2016:600 2017:3.8K 2018:0 2019:0 2021:0 2025:6.0K
  NATIONAL ASSET MANAGEMENT GROUP LLC,      2011:2.6K 2012:10.4K
  NATIONWIDE REO LLC,                       2011:15.5K 2012:5.3K 2013:0 2014:0 2015:0 2016:0 2017:4.3K 2018:18.0K 2019:0 2021:6.0K
  OCWEN LOAN SERVICING LLC,                 2011:1.6K 2013:2.6K 2014:400 2015:0 2016:0 2017:0 2018:0 2020:0 2022:0
  REO DIRECT LLC,                           2011:23.0K
  REO PARTNERS LLC,                         2011:0 2012:25.8K 2013:4.3K 2014:0 2015:0 2016:0 2017:0 2018:0
  US BANK NA,                               2013:0 2014:1.3K 2015:4.3K 2016:400 2017:2.6K 2018:0 2019:0 2020:0 2021:0 2023:0
  US BANK,                                  2011:0 2013:3.5K 2014:3.3K 2015:6.2K 2016:0 2017:3.1K 2018:1.0K 2019:0 2020:0 2021:0 2022:0
  WELLS FARGO BANK NA,                      2011:300 2012:800 2013:600 2014:0 2015:13.7K 2016:0 2017:600 2024:0
  WELLS FARGO BANK,                         2011:10.7K 2012:11.6K 2013:28.8K 2014:6.9K 2015:0 2016:0 2017:0 2018:8.0K 2019:0 2020:0

LOCATION by ISSUED_DATE, dollars = TOTAL_FINES
  nan                                       2011:6.9K 2012:23.8K 2013:11.5K 2014:12.8K 2015:4.3K 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0
  {"type": "Point", "coordinates": [-87.64  2011:9.5K
  {"type": "Point", "coordinates": [-87.64  2012:11.4K
  {"type": "Point", "coordinates": [-87.64  2011:5.6K 2012:2.8K
  {"type": "Point", "coordinates": [-87.64  2017:8.6K 2018:12.0K 2019:0 2021:6.0K
  {"type": "Point", "coordinates": [-87.64  2011:8.6K 2012:2.5K 2013:0 2018:6.0K
  {"type": "Point", "coordinates": [-87.64  2012:4.3K 2013:8.6K 2014:8.6K 2015:8.6K 2016:25.8K 2018:6.0K
  {"type": "Point", "coordinates": [-87.66  2012:17.2K 2013:4.3K 2014:0 2015:0 2016:0 2017:0 2018:0
  {"type": "Point", "coordinates": [-87.66  2011:25.8K
  {"type": "Point", "coordinates": [-87.66  2011:0 2012:8.6K
  {"type": "Point", "coordinates": [-87.66  2011:6.5K 2012:3.4K
  {"type": "Point", "coordinates": [-87.67  2011:5.4K 2012:10.4K
  {"type": "Point", "coordinates": [-87.67  2016:8.6K
  {"type": "Point", "coordinates": [-87.67  2011:0 2012:9.0K 2013:800
  {"type": "Point", "coordinates": [-87.67  2011:11.4K
  {"type": "Point", "coordinates": [-87.67  2012:4.3K 2013:0 2014:0 2015:0
  {"type": "Point", "coordinates": [-87.67  2011:12.7K
  {"type": "Point", "coordinates": [-87.67  2012:4.2K 2013:3.0K
  {"type": "Point", "coordinates": [-87.67  2015:0 2016:4.3K 2017:0
  {"type": "Point", "coordinates": [-87.68  2013:2.6K 2014:0
  {"type": "Point", "coordinates": [-87.68  2018:0 2020:0
  {"type": "Point", "coordinates": [-87.69  2015:8.6K
  {"type": "Point", "coordinates": [-87.69  2013:8.9K
  {"type": "Point", "coordinates": [-87.70  2020:12.0K
  {"type": "Point", "coordinates": [-87.70  2016:0 2017:0 2018:0
  {"type": "Point", "coordinates": [-87.71  2015:0 2017:1.3K 2018:0
  {"type": "Point", "coordinates": [-87.71  2013:0 2014:0 2015:0
  {"type": "Point", "coordinates": [-87.71  2015:0
  {"type": "Point", "coordinates": [-87.75  2011:8.5K
  {"type": "Point", "coordinates": [-87.75  2013:300 2014:700 2015:0 2016:0

## what

ISSUING_DEPARTMENT: POLICE 100%, BLDINGS 0%

VIOLATION_TYPE: 13-12-125  Duty to secure and  52%, 13-12-125  Duty to secure and  14%, 13-12-125  Duty to secure and  10%, 13-12-140  Watchman required|1 5%, 13-12-125  Duty to secure and  4%, 13-12-140  Watchman required|1 4%, 13-12-125  Duty to secure and  3%, 13-12-140  Watchman required 3%, 13-12-125  Duty to secure and  2%, 13-12-125  Duty to secure and  2%, 13-12-125  Duty to secure and  1%, 13-12-125  Duty to secure and  1%

DISPOSITION_DESCRIPTION: City non-suit 80%, Default - Liable by prove-up 12%, Liable - By plea 3%, City Non suit - Motion to set- 3%, Not liable - City failed to es 1%, Dismissed for want of prosecut 1%, Liable - By Plea - Motion to s 0%, Vendor scanning error 0%, Not liable - Respondent came i 0%, Not liable - City failed to me 0%, Not liable - City failed to es 0%

COMPUTED_REGION_RPCA_8UM6: 37 24%, 58 16%, 23 13%, 56 9%, nan 7%, 11 7%, 30 7%, 19 3%, 25 3%, 5 3%, 32 3%, 8 3%

COMPUTED_REGION_6MKV_F3DW: 14924 24%, 21867 16%, 22257 14%, 22248 9%, nan 7%, 21572 7%, 21559 7%, 21861 3%, 21202 3%, 4299 3%, 22216 3%, 4300 3%

COMPUTED_REGION_43WA_7QMU: 2 31%, 4 12%, 31 9%, nan 8%, 3 8%, 23 7%, 30 6%, 8 5%, 6 4%, 1 4%, 14 4%, 45 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DOCKET_NUMBER | other | 1.9K | 0 | 20CP023181 11; 11CP065702 11; 18CP020723 11; 14CP010630 10 |
| VIOLATION_NUMBER | other | 1.9K | 0 | P005841966/P005841967/P00 11; P005607611/P005607612/P00 11; P004323077/P004323078/P00 10; P004077185/P004077186/P00 10 |
| ISSUED_DATE | date | 1.2K | 0 | 2015-04-08T00:00:00.000 12; 2020-08-13T00:00:00.000 11; 2011-10-04T00:00:00.000 11; 2013-06-01T00:00:00.000 11 |
| ISSUING_DEPARTMENT | category | 2 | 0 | POLICE 2.0K; BLDINGS 8 |
| LAST_HEARING_DATE | date | 352 | 0 | 2014-08-01T09:00:00.000 29; 2012-04-06T09:00:00.000 28; 2012-03-02T09:00:00.000 27; 2014-02-07T09:00:00.000 26 |
| PROPERTY_ADDRESS | other | 1.3K | 0 | 6208 S MORGAN  18; 6114 S BISHOP  15; 7033 S WASHTENAW  12; 6754 S HONORE  12 |
| VIOLATION_TYPE | category | 37 | 0 | 13-12-125  Duty to secure 1.0K; 13-12-125  Duty to secure 264; 13-12-125  Duty to secure 203; 13-12-140  Watchman requi 96 |
| ENTITY_OR_PERSON_S | who | 196 | 0 | BANK OF AMERICA,  199; WELLS FARGO BANK,  149; US BANK,  97; DEUTSCHE BANK,  94 |
| DISPOSITION_DESCRIPTION | category | 11 | 0 | City non-suit 1.6K; Default - Liable by prove 241; Liable - By plea 58; City Non suit - Motion to 56 |
| TOTAL_FINES | amount | 26 | 0 | 0 1.6K; 1300 131; 4300 80; 300 39 |
| TOTAL_ADMINISTRATIVE_COSTS | other | 1 | 0 | 0 2.0K |
| INTEREST_AMOUNT | amount | 281 | 0 | 0 1.6K; 10.24 6; 273.55 4; 67.01 3 |
| COLLECTION_COSTS_OR_ATTORNEY_FEES | amount | 34 | 0 | 0 1.7K; 377.88 88; 1223.88 68; 800.88 23 |
| COURT_COST | amount | 36 | 0 | 0 1.9K; 20 14; 42 11; 26.09 10 |
| ORIGINAL_TOTAL_AMOUNT_DUE | amount | 302 | 0 | 0 1.6K; 1340 18; 740 13; 140 9 |
| TOTAL_PAID | other | 229 | 0 | 0 1.6K; 1340 24; 340 16; 740 15 |
| CURRENT_AMOUNT_DUE | amount | 115 | 0 | 0 1.8K; -0.01 32; -185.01 6; 3398.01 3 |
| LATITUDE | amount | 1.2K | 0 | nan 129; 41.78117319861422 18; 41.78267314352238 15; 41.80130660296048 12 |
| LONGITUDE | amount | 1.2K | 0 | nan 129; -87.6498292763393 18; -87.66079340228376 15; -87.67745691931087 12 |
| LOCATION | who | 1.2K | 0 | nan 129; {"type": "Point", "coordi 18; {"type": "Point", "coordi 15; {"type": "Point", "coordi 12 |
| COMPUTED_REGION_RPCA_8UM6 | category | 39 | 0 | 37 428; 58 279; 23 233; 56 157 |
| COMPUTED_REGION_VRXF_VC4K | other | 58 | 0 | 59 378; 64 258; 65 185; nan 129 |
| COMPUTED_REGION_6MKV_F3DW | category | 38 | 0 | 14924 428; 21867 277; 22257 240; 22248 159 |
| COMPUTED_REGION_BDYS_3D7I | other | 286 | 0 | nan 129; 790 71; 767 52; 319 43 |
| COMPUTED_REGION_43WA_7QMU | category | 40 | 0 | 2 465; 4 177; 31 131; nan 129 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:07:49.61410 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | af055779-5c13-4e01-babf-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | 821762db73792296a4c010dd1 2.0K |
