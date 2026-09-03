# PORTAL_CKA_ANALYZE_BOSTON_5DD692715C

rows 3.3K  columns 17  scan 3.9s

roles: amount 2, audit 2, category 5, date 2, other 4, who 3

## when

LICENSE_ADD_DT_TM
  2006       507  ##############################
  2007       129  ########
  2008        78  #####
  2009        80  #####
  2010        85  #####
  2011        70  ####
  2012        69  ####
  2013        77  #####
  2014        89  #####
  2015       108  ######
  2016       114  #######
  2017       112  #######
  2018       172  ##########
  2019       217  #############
  2020        92  #####
  2021       184  ###########
  2022       232  ##############
  2023       234  ##############
  2024       259  ###############
  2025       266  ################
  2026       128  ########

INGESTED_AT
  2026      3.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 3.1K | 42.24 | 42.35 | 42.38 | 42.40 | 131.0K |
| LONGITUDE | 3.1K | -71.17 | -71.07 | -71.02 | -71 | -220.0K |

## who

BUSINESSNAME by rows
        36  Dunkin Donuts
        16  Caffe Nero
        15  Mcdonalds
        14  Tatte Bakery & Cafe
        13  Subway
        12  Dunkin' Donuts
        11  Sweetgreen
         9  Burger King
         9  Starbucks Coffee
         7  Chipotle Mexican Grill
         7  Domino's Pizza
         7  Starbucks
         6  Taco Bell
         6  Gong Cha
         6  Chilacates
         6  Domino's
         6  Anna's Taqueria
         6  DUNKIN'
         5  FLOUR BAKERY & CAFE
         5  Cava

BUSINESSNAME by dollars
        1.4K       36 rows  Dunkin Donuts
      635.22       16 rows  Caffe Nero
      634.85       15 rows  Mcdonalds
      550.56       14 rows  Tatte Bakery & Cafe
      550.28       13 rows  Subway
      465.87       11 rows  Sweetgreen
      465.77       12 rows  Dunkin' Donuts
      381.21        9 rows  Starbucks Coffee
      338.65        9 rows  Burger King
      254.12        7 rows  Starbucks
      254.11        6 rows  Taco Bell
      254.08        6 rows  Anna's Taqueria
      254.07        7 rows  Chipotle Mexican Grill
      254.05        6 rows  Gong Cha
      254.03        7 rows  Domino's Pizza
         254        6 rows  Chilacates
      253.99        6 rows  DUNKIN'
      211.76        5 rows  Blank Street Coffee
      211.75        5 rows  Cava
      211.71        5 rows  FLOUR BAKERY & CAFE

LICSTATUS by rows
      3.3K  Active

LICSTATUS by dollars
      131.0K     3.3K rows  Active

SRC_SHA256 by rows
      3.3K  ed13953d0b511693cc8d9279f944a1d924629933a3eeb0f34c1f2645308fcc94

SRC_SHA256 by dollars
      131.0K     3.3K rows  ed13953d0b511693cc8d9279f944a1d924629933a3eeb0f34c1f2645308f

## who x when

BUSINESSNAME by LICENSE_ADD_DT_TM, dollars = LATITUDE
  Anna's Taqueria                           2008:42.36 2017:42.35 2022:42.34 2024:84.69 2025:42.34
  Blank Street Coffee                       2022:84.71 2023:42.34 2024:84.71
  Burger King                               2006:127.02 2010:42.37 2013:127 2018:42.26
  Caffe Nero                                2014:84.66 2015:84.68 2016:42.36 2017:127.04 2018:84.71 2019:84.70 2020:42.37 2023:42.35 2024:42.35
  Cava                                      2017:42.34 2018:42.35 2022:84.70 2026:42.36
  Chilacates                                2015:42.32 2017:42.31 2018:84.67 2022:42.34 2023:42.36
  Chipotle Mexican Grill                    2007:42.34 2008:1 2014:42.35 2016:84.70 2017:42.33 2025:42.35
  DUNKIN'                                   2006:84.63 2019:42.36 2020:42.35 2025:84.65
  Domino's                                  2017:42.36 2019:84.56 2023:84.63
  Domino's Pizza                            2012:42.33 2016:42.27 2017:42.38 2019:84.70 2022:42.35
  Dunkin Donuts                             2006:338.58 2007:42.36 2008:42.35 2009:1 2010:42.35 2014:127.05 2017:127 2018:84.71 2019:84.69 2022:296.09 2023:84.69 2024:126.99
  Dunkin' Donuts                            2006:338.63 2021:127.14
  FLOUR BAKERY & CAFE                       2006:42.34 2012:42.35 2016:42.35 2018:42.34 2025:42.33
  Gong Cha                                  2018:42.35 2021:84.64 2022:42.35 2023:84.71
  Mcdonalds                                 2006:42.36 2011:42.36 2016:169.19 2018:42.32 2019:127 2022:169.25 2023:42.37
  Starbucks                                 2006:1 2008:42.35 2015:84.69 2018:42.36 2021:42.37 2023:42.35
  Starbucks Coffee                          2007:84.73 2016:127.04 2017:84.74 2023:42.35 2024:42.35
  Subway                                    2006:84.64 2011:42.29 2013:42.37 2014:84.63 2016:42.26 2017:42.33 2019:84.67 2023:84.73 2024:42.36
  Sweetgreen                                2013:42.35 2015:127.05 2016:84.70 2017:127.07 2021:84.70
  Taco Bell                                 2019:42.35 2021:42.34 2023:42.35 2024:84.72 2025:42.35
  Tatte Bakery & Cafe                       2014:42.36 2017:84.69 2018:127.04 2019:169.42 2021:42.34 2022:42.36 2023:42.35

LICSTATUS by LICENSE_ADD_DT_TM, dollars = LATITUDE
  Active                                    2006:20.0K 2007:4.4K 2008:2.9K 2009:1.3K 2010:3.4K 2011:2.8K 2012:2.5K 2013:3.2K 2014:3.7K 2015:4.4K 2016:4.6K 2017:4.7K 2018:7.2K 2019:8.3K 2020:3.9K 2021:7.5K 2022:9.7K 2023:9.7K 2024:10.8K 2025:11.2K 2026:5.2K

## what

DBANAME: HSI MCA BOS FB  LLC 32%, Aramark Corporation 21%, Golden Rice Bowl 5%, Windy City Pizza  LLC 5%, Top of the Hill Seafood & Subs 5%, The Next Place LLC 5%, Thornton's Restaurant 5%, Sweet Rice Thai Sushi 5%, FJS INC. 5%, Hynes Fine Dining  LLC 5%, PB Husky  LLC 5%

CITY: Boston 54%, Dorchester 8%, East Boston 7%, Roxbury 5%, Brighton 5%, Allston 5%, South Boston 3%, Jamaica Plain 3%, BOSTON 3%, Charlestown 3%, Roslindale 2%, West Roxbury 2%

ZIP: 02116 11%, 02128 11%, 02215 11%, 02210 10%, 02114 9%, 02115 8%, 02111 8%, 02135 8%, 02134 7%, 02110 7%, 02127 5%, 02118 5%

LICENSECAT: FS 53%, FT 47%

DESCRIPT: Eating & Drinking 53%, Eating & Drinking w/ Take Out 47%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESSNAME | who | 3.0K | 0 | Dunkin Donuts 40; Tatte Bakery & Cafe 27; Subway 26; Sweetgreen 24 |
| DBANAME | category | 26 | 3.3K | HSI MCA BOS FB  LLC 6; Aramark Corporation 4; Golden Rice Bowl 1; Windy City Pizza  LLC 1 |
| ADDRESS | other | 2.3K | 4 | 100 Legends 71; 4 Jersey 55; 32 Cambridge 40; 290 Northern 25 |
| CITY | category | 37 | 4 | Boston 1.7K; Dorchester 254; East Boston 230; Roxbury 165 |
| STATE | other | 1 | 0 | MA 3.3K |
| ZIP | category | 33 | 4 | 02116 247; 02128 241; 02215 230; 02210 220 |
| LICSTATUS | who | 1 | 0 | Active 3.3K |
| LICENSECAT | category | 2 | 0 | FS 1.8K; FT 1.5K |
| DESCRIPT | category | 2 | 0 | Eating & Drinking 1.8K; Eating & Drinking w/ Take 1.5K |
| LICENSE_ADD_DT_TM | date | 3.0K | 0 | 2006-12-07 18:36:13+00 19; 2006-12-07 18:36:25+00 18; 2006-12-07 18:34:00+00 18; 2006-12-07 18:34:43+00 18 |
| DAYPHN_CLEANED | other | 2.2K | 468 | 6176241610 50; 0 28; 7742054363 26; 3236404678 24 |
| PROPERTY_ID | other | 2.2K | 312 | 25110 40; 424258 31; 156417 25; 341023 25 |
| LATITUDE | amount | 2.3K | 207 | 42.383569999309664 40; 42.34673007807398 31; 42.346768333561606 25; 42.34818065230851 25 |
| LONGITUDE | amount | 2.2K | 207 | -71.0743500017016 40; -71.0986629781914 31; -71.09864788266272 25; -71.03661799221628 25 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:05:54.51145 3.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 21f4bbfa-7070-4cd4-88d6-2 3.3K |
| SRC_SHA256 | who | 1 | 0 | ed13953d0b511693cc8d9279f 3.3K |
