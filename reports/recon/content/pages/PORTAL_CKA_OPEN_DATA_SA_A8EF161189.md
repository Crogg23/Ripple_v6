# PORTAL_CKA_OPEN_DATA_SA_A8EF161189

rows 6.5K  columns 12  scan 4.3s

roles: amount 2, audit 2, date 4, id 1, other 1, who 3

## when

RECORDATIONDATE
  2003         3  
  2004         1  
  2005         5  
  2006         4  
  2007         5  
  2008         3  
  2009         1  
  2010         1  
  2011         1  
  2012        26  #
  2013       466  ########################
  2014       457  #######################
  2015       508  ##########################
  2016       447  #######################
  2017       485  ########################
  2018       500  #########################
  2019       511  ##########################
  2020       533  ###########################
  2021       504  #########################
  2022       594  ##############################
  2023       534  ###########################
  2024       489  #########################
  2025       415  #####################

CREATED_DATE
  2017       180  ##
  2018       455  #####
  2019       492  ######
  2020       585  #######
  2021      2.7K  ##############################
  2022       626  #######
  2023       546  ######
  2024       491  ######
  2025       455  #####

LAST_EDITED_DATE
  2017        25  
  2018        49  #
  2019        61  #
  2020       108  #
  2021      1.6K  ################
  2022      2.9K  ##############################
  2023       567  ######
  2024       637  #######
  2025       553  ######

INGESTED_AT
  2026      6.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 6.5K | 16.70 | 200.0K | 3.50M | 37.84M | 3.13B |
| SHAPE__LENGTH | 6.5K | 29.23 | 2.1K | 12.5K | 40.6K | 18.73M |

## who

PLATNAME by rows
         5  The Canyons at Scenic Loop Unit 5B
         4  Shops at Overlook
         3  Fallbrook Unit 1 Enclave
         3  Southton Cove Unit 2B and 3
         3  Broadway Office Development
         3  Timms Subdivision Unit 1
         3  U-Haul 4
         3  Forest Crest Lot 37
         3  Vantage at Fair Oaks
         3  West Highlands
         3  FUCD Subdivision
         3  255 Brahan
         3  Univision Redevelopment
         3  Burleson Subdivision
         3  McCrary Tract Unit 18
         3  Cantera Hills Unit 3
         3  Cresta Bella Unit 3
         3  Blackbuck Ranch Phase 1 Unit 5
         3  Westover Hills 80 Acres
         3  Luckey Ranch South Unit 1

PLATNAME by dollars
      37.84M        1 rows  S Foster and E Houston Subdivision
      27.00M        1 rows  Arcadia Ridge Offsite Sanitary Sewer
      25.58M        1 rows  NSSA National Shooting Complex
      18.34M        1 rows  Black Briar
      17.64M        1 rows  JCB Project Sky
      10.58M        1 rows  La Cantera Residential Enclave
       8.91M        1 rows  SWSD Legacy Subdivision
       8.57M        1 rows  Chariot
       7.47M        1 rows  San Antonio International Airport Unit 15
       7.34M        1 rows  CAB Subdivision
       7.30M        1 rows  Rafter 2
       7.10M        1 rows  Palo Alto College Replat II
       6.81M        2 rows  Pecan Springs Ranch Unit 3
       6.61M        1 rows  Evans Road High School
       6.61M        1 rows  Verterans Memorial High School 
       6.59M        1 rows  Smile Subdivision
       6.42M        1 rows  AC-North Central Campus
       6.38M        1 rows  Holt Cat Replat
       6.08M        1 rows  Brook Stone Creek Unit 2E
       5.96M        1 rows  Hickory Hollow U6

ENGINEER by rows
      1.6K  Pape Dawson Engineers
       518  KFW Engineers and Surveying
       151  K Love Engineering
       132  Seda Consulting Engineers Inc
       129  MW Cude Engineers
       118  Moy Tarin Ramirez Engineers LLC
       103  Macina Bose Copeland & Associates Inc
       101  Dye Enterprises
        98  Civil Engineering Consultants
        95  Pape Dawson
        88  GE Reaves Engineering
        81  Bendicion Engineering LLC
        78  Jones Carter
        77  Big Red Dog Engineering Consulting
        74  CDS Muery Engineers Surveyors
        70  Denham Ramones Engineering and Associates Inc
        68  MHR Engineering LLC
        60  Vickrey and Associates Inc
        59  Villagomez Engineering Co
        56  Villagomez Enginnering Co

ENGINEER by dollars
       1.20B     1.6K rows  Pape Dawson Engineers
     304.54M      518 rows  KFW Engineers and Surveying
     112.54M      118 rows  Moy Tarin Ramirez Engineers LLC
      78.77M      129 rows  MW Cude Engineers
      78.01M       98 rows  Civil Engineering Consultants
      73.07M       95 rows  Pape Dawson
      59.52M       78 rows  Jones Carter
      59.21M       74 rows  CDS Muery Engineers Surveyors
      54.14M       32 rows  Stantec
      43.76M       54 rows  Kimley Horn
      43.22M       41 rows  Bain Medina Bain Inc
      33.82M       60 rows  Vickrey and Associates Inc
      33.81M       70 rows  Denham Ramones Engineering and Associates Inc
      32.97M       48 rows  Cude Engineers
      32.45M      103 rows  Macina Bose Copeland & Associates Inc
      30.50M      151 rows  K Love Engineering
      29.87M       33 rows  MW Cude Engineers LLC
      25.02M       34 rows  KFW Engineers & Surveying
      24.63M       77 rows  Big Red Dog Engineering Consulting
      21.57M       19 rows  MTR

SRC_SHA256 by rows
      6.5K  e9c5a4db4c08b5ae11a5cad4e0a24906329a3f65d40fba78e4cd14afc0470b2b

SRC_SHA256 by dollars
       3.13B     6.5K rows  e9c5a4db4c08b5ae11a5cad4e0a24906329a3f65d40fba78e4cd14afc047

## who x when

PLATNAME by CREATED_DATE, dollars = SHAPE__AREA
  255 Brahan                                2017:16.7K 2023:33.5K
  Arcadia Ridge Offsite Sanitary Sewer      2021:27.00M
  Black Briar                               2021:18.34M
  Blackbuck Ranch Phase 1 Unit 5            2018:2.35M 2020:107.2K
  Broadway Office Development               2018:135.1K 2020:135.0K 2025:135.0K
  Burleson Subdivision                      2020:25.6K 2022:6.0K
  CAB Subdivision                           2021:7.34M
  Cantera Hills Unit 3                      2022:1.91M 2023:150.2K 2024:30.6K
  Chariot                                   2018:8.57M
  Cresta Bella Unit 3                       2020:44.3K 2021:82.9K
  FUCD Subdivision                          2020:204.1K 2021:77.9K 2024:71.9K
  Fallbrook Unit 1 Enclave                  2021:4.09M
  Forest Crest Lot 37                       2021:417.0K 2023:94.8K
  JCB Project Sky                           2025:17.64M
  La Cantera Residential Enclave            2021:10.58M
  Luckey Ranch South Unit 1                 2022:2.68M 2023:2.69M
  McCrary Tract Unit 18                     2024:1.68M 2025:1.44M
  NSSA National Shooting Complex            2021:25.58M
  S Foster and E Houston Subdivision        2020:37.84M
  SWSD Legacy Subdivision                   2021:8.91M
  San Antonio International Airport Unit 1  2025:7.47M
  Shops at Overlook                         2021:226.6K 2022:679.9K
  Southton Cove Unit 2B and 3               2022:496.7K 2023:97.2K 2025:496.7K
  The Canyons at Scenic Loop Unit 5B        2021:248.2K
  Timms Subdivision Unit 1                  2022:659.5K 2023:1.30M
  U-Haul 4                                  2018:103.1K 2021:206.2K
  Univision Redevelopment                   2021:591.0K
  Vantage at Fair Oaks                      2021:944.6K 2022:1.89M
  West Highlands                            2017:13.2K 2021:15.9K
  Westover Hills 80 Acres                   2020:351.7K 2021:3.49M 2023:177.6K

ENGINEER by CREATED_DATE, dollars = SHAPE__AREA
  Bain Medina Bain Inc                      2018:10.22M 2019:1.72M 2020:4.49M 2021:15.79M 2022:1.27M 2023:83.0K 2024:157.3K 2025:9.49M
  Bendicion Engineering LLC                 2017:456.8K 2018:378.4K 2019:979.8K 2020:164.8K 2021:4.93M 2022:103.7K 2023:596.3K 2024:2.57M 2025:1.79M
  Big Red Dog Engineering Consulting        2017:1.70M 2018:2.77M 2019:2.63M 2020:2.35M 2021:15.17M
  CDS Muery Engineers Surveyors             2017:20.7K 2018:1.29M 2019:4.51M 2020:5.34M 2021:38.18M 2022:3.53M 2024:2.89M 2025:3.45M
  Civil Engineering Consultants             2017:295.2K 2018:8.13M 2019:5.02M 2020:9.11M 2021:39.28M 2022:12.11M 2023:1.60M 2024:2.46M
  Cude Engineers                            2021:21.87M 2024:8.87M 2025:2.22M
  Denham Ramones Engineering and Associate  2017:3.06M 2018:1.96M 2021:28.79M
  Dye Enterprises                           2017:23.2K 2018:646.5K 2019:973.0K 2020:945.0K 2021:8.01M 2022:383.9K 2023:80.8K 2024:595.4K 2025:435.0K
  GE Reaves Engineering                     2017:887.1K 2018:743.2K 2019:619.3K 2020:1.66M 2021:2.35M 2022:1.03M 2023:1.85M 2024:1.50M 2025:580.1K
  Jones Carter                              2017:1.52M 2018:9.36M 2019:6.73M 2020:4.07M 2021:27.92M 2022:9.39M 2023:539.8K
  K Love Engineering                        2017:1.11M 2018:2.11M 2019:3.03M 2020:3.91M 2021:9.94M 2022:1.66M 2023:2.53M 2024:4.83M 2025:1.37M
  KFW Engineers & Surveying                 2022:7.98M 2023:3.55M 2024:9.47M 2025:4.02M
  KFW Engineers and Surveying               2017:4.89M 2018:19.75M 2019:24.31M 2020:33.78M 2021:130.60M 2022:20.34M 2023:32.89M 2024:17.77M 2025:20.22M
  Kimley Horn                               2017:358.5K 2018:6.85M 2019:2.06M 2020:5.40M 2021:13.93M 2022:1.42M 2023:9.29M 2024:4.45M
  MHR Engineering LLC                       2017:357.3K 2018:1.67M 2019:983.1K 2020:437.5K 2021:2.12M 2022:555.5K 2023:98.5K 2024:403.5K 2025:1.33M
  MTR                                       2021:7.57M 2023:781.8K 2024:11.04M 2025:2.18M
  MW Cude Engineers                         2017:5.55M 2018:4.65M 2019:16.15M 2020:21.11M 2021:27.11M 2022:1.55M 2023:1.54M 2024:1.10M
  MW Cude Engineers LLC                     2021:9.34M 2022:6.03M 2023:7.59M 2024:5.58M 2025:1.33M
  Macina Bose Copeland & Associates Inc     2017:2.60M 2018:7.23M 2019:1.53M 2020:5.85M 2021:14.74M 2022:509.4K
  Moy Tarin Ramirez Engineers LLC           2017:5.44M 2018:15.57M 2019:7.81M 2020:11.81M 2021:39.19M 2022:8.20M 2023:1.90M 2024:6.69M 2025:15.93M
  Pape Dawson                               2022:49.85M 2023:23.22M
  Pape Dawson Engineers                     2017:26.19M 2018:78.38M 2019:86.76M 2020:85.86M 2021:540.39M 2022:79.99M 2023:92.08M 2024:101.99M 2025:112.22M
  Seda Consulting Engineers Inc             2017:136.5K 2018:1.03M 2019:1.94M 2020:301.9K 2021:8.32M 2022:1.36M 2023:314.8K 2024:1.66M 2025:457.4K
  Stantec                                   2017:1.39M 2018:730.7K 2019:4.22M 2020:38.62M 2021:6.00M 2022:2.94M 2023:239.2K
  Vickrey and Associates Inc                2017:362.8K 2018:6.15M 2019:1.02M 2020:3.82M 2021:21.82M 2024:645.1K
  Villagomez Engineering Co                 2017:769.3K 2018:644.2K 2019:429.2K 2020:776.9K 2021:1.87M 2022:387.9K 2023:48.3K
  Villagomez Enginnering Co                 2021:26.7K 2022:541.6K 2023:231.1K 2024:2.59M 2025:1.71M

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 6.4K | 0 | 6493 33; 6492 33; 6491 33; 6490 33 |
| PLATNUMBER | other | 5.1K | 0 | 0 1.3K; 2018000014 27; 2014000218 27; 2013000633 27 |
| PLATNAME | who | 6.3K | 1 | SFIP Unit 3A & 4A 33; Steubing Farm Unit 3A  33; Madison Self Storage 33; Westpointe Multi Family 33 |
| RECORDATIONDATE | date | 1.3K | 0 | 9/18/2020 12:00:00 AM 36; 3/25/2022 12:00:00 AM 35; 5/22/2015 12:00:00 AM 35; 10/9/2020 12:00:00 AM 35 |
| ENGINEER | who | 537 | 0 | Pape Dawson Engineers 1.6K; KFW Engineers and Surveyi 518; K Love Engineering 151; Seda Consulting Engineers 132 |
| CREATED_DATE | date | 6.4K | 0 | 9/30/2021 3:18:01 PM 33; 4/23/2021 7:39:50 PM 33; 5/18/2021 5:00:09 PM 33; 12/5/2022 4:54:11 PM 33 |
| LAST_EDITED_DATE | date | 3.6K | 0 | 5/4/2021 6:29:17 PM 83; 4/14/2021 8:53:14 PM 63; 1/11/2022 9:19:56 PM 56; 5/4/2021 4:53:19 PM 43 |
| SHAPE__AREA | amount | 6.2K | 0 | 768885.705078125 33; 799585.083984375 33; 178551.84375 33; 702755.685546875 33 |
| SHAPE__LENGTH | amount | 6.3K | 0 | 4035.34467501262 33; 4059.65908684583 33; 1678.73175195695 33; 3565.15244286305 33 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:11:51.98400 6.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 07b0f2e1-9faf-4feb-bf39-f 6.5K |
| SRC_SHA256 | who | 1 | 0 | e9c5a4db4c08b5ae11a5cad4e 6.5K |
