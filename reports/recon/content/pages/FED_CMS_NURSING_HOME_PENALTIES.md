# FED_CMS_NURSING_HOME_PENALTIES

rows 16.2K  columns 17  scan 5.6s

roles: amount 2, audit 2, category 1, date 3, id 1, other 2, state 1, who 5

## when

PENALTY_DATE
  2023      4.8K  #######################
  2024      6.3K  ##############################
  2025      4.4K  #####################
  2026       670  ###

PAYMENT_DENIAL_START_DATE
  2023       450  ############
  2024      1.1K  ##############################
  2025       772  #####################
  2026       138  ####

PROCESSING_DATE
  2026     16.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FINE_AMOUNT | 13.7K | 344 | 14.8K | 226.1K | 713.8K | 459.05M |
| PAYMENT_DENIAL_LENGTH_IN_DAYS | 2.5K | 1 | 19 | 126 | 458 | 67.5K |

## who

PROVIDER_NAME by rows
        27  ABODE HEALTH AND WELLNESS CENTER
        27  BERKELEY NURSING & REHAB CENTER
        26  THE GARDENS OF FAIRFAX HEALTH CARE CENTER
        25  THE VILLAS AT NEW BRIGHTON
        25  CHOWCHILLA MEMORIAL HEALTHCARE DISTRICT
        25  PEACE CARE ST JOSEPH'S
        24  EVERVELLA OF SWANSEA
        24  CAMPBELL HALL REHABILITATION CENTER INC
        24  Harbor Post Acute Center
        23  GOLDEN ROSE CARE CENTER
        23  CROWN CENTER AT LAUREL LAKE
        23  LATIMER NURSING HOME
        22  BAYSHIRE TORREY PINES POST-ACUTE
        20  CHANDLER THERAPY & LIVING CENTER LLC
        20  Henson Park Health & Rehabilitation
        20  SEAGATE REHABILITATION AND NURSING CENTER
        20  FRUITVALE HEALTHCARE CENTER
        20  ASPEN HEALTH AND WELLNESS
        19  Odd Fellow Home
        19  REAGAN COUNTY CARE CENTER

PROVIDER_NAME by dollars
      883.2K        9 rows  CHICAGO RIDGE SNF
      821.6K        9 rows  Nexus Pavilion at Belleville
      810.4K       11 rows  MAJESTIC GARDENS AT MEMPHIS REHAB & SNC
      804.8K        3 rows  Waterview Heights Rehabilitation and Nursing Cente
      798.5K       12 rows  BRIA OF CAHOKIA
      754.4K        5 rows  AVIR AT LINDALE
      738.3K        3 rows  MOHAWK MEADOWS
      702.0K        5 rows  La Bella of Cahokia
      699.6K        4 rows  BISHOP REHABILITATION AND NURSING CENTER
      656.5K        6 rows  Legacy Nursing at St. Christina
      656.3K        7 rows  GRAND MANOR NURSING & REHABILITATION CENTER
      631.9K       11 rows  MORGAN PARK HEALTHCARE
      626.0K       16 rows  Mission Point Nursing & Physical Rehabilitation Ce
      625.1K        7 rows  Whispering Pines Lodge
      619.6K        6 rows  Van Duyn Center For Rehabilitation And Nursing
      616.6K        4 rows  Natchitoches Nursing and Rehabilitation Center, LL
      607.3K       10 rows  AUSTIN OASIS, THE
      596.5K        7 rows  ARCHER HEIGHTS HEALTHCARE
      591.7K        6 rows  RIVER VIEW REHAB CENTER
      582.6K       15 rows  BRIDGEWOOD HEALTH CARE CENTER

LOCATION by rows
        27  6909 WEST NORTH AVENUE,OAK PARK,IL,60302
        27  17451 MEDICAL CENTER PARKWAY,INDEPENDENCE,MO,64057
        26  9014 CEDAR AVE,CLEVELAND,OH,44106
        25  825  FIRST AVENUE NORTHWEST,NEW BRIGHTON,MN,55112
        25  537 PAVONIA AVENUE,JERSEY CITY,NJ,07306
        25  1104 VENTURA AVE.,CHOWCHILLA,CA,93610
        24  23 KIERNAN RD,CAMPBELL HALL,NY,10916
        24  2060 Health Drive,Wyoming,MI,49519
        24  100 ROSEWOOD VILLAGE DRIVE,SWANSEA,IL,62220
        23  103 SOUTHWEST 9TH STREET,WILBURTON,OK,74578
        23  200 LAUREL LAKE DR,HUDSON,OH,44236
        23  1899 N RAYMOND AVE,PASADENA,CA,91103
        22  13101 HARTFIELD AVE,SAN DIEGO,CA,92130
        20  203 Bruce Court,Danville,KY,40422
        20  601 WEST 1ST STREET,CHANDLER,OK,74834
        20  6501 W 75TH STREET,OVERLAND PARK,KS,66204
        20  3020 EAST 15TH STREET,OAKLAND,CA,94601
        20  3015 W 29 ST,BROOKLYN,NY,11224
        19  1300 NORTH MAIN,BIG LAKE,TX,76932
        19  245 STATE HWY #153 WEST,COLEMAN,TX,76834

LOCATION by dollars
      883.2K        9 rows  10602 SOUTHWEST  HIGHWAY,CHICAGO RIDGE,IL,60415
      821.6K        9 rows  727 NORTH 17TH STREET,BELLEVILLE,IL,62226
      810.4K       11 rows  131 N TUCKER,MEMPHIS,TN,38104
      804.8K        3 rows  135 Meridan St.,Rochester,NY,14612
      798.5K       12 rows  3354 JEROME LANE,CAHOKIA,IL,62206
      754.4K        5 rows  13905 FM 2710,LINDALE,TX,75771
      738.3K        3 rows  1 O'BRIEN LANE,LAFAYETTE,NJ,07848
      702.0K        5 rows  2 ANNABLE COURT,CAHOKIA,IL,62206
      699.6K        4 rows  918 JAMES STREET,SYRACUSE,NY,13203
      656.5K        6 rows  122 Hillsdale Drive,Pineville,LA,71360
      656.3K        7 rows  700 WHITE PLAINS ROAD,BRONX,NY,10473
      631.9K       11 rows  10935 SOUTH HALSTED STREET,CHICAGO,IL,60628
      625.1K        7 rows  2131 Alpine Rd,Longview,TX,75601
      619.6K        6 rows  5075 WEST SENECA TURNPIKE,SYRACUSE,NY,13215
      616.6K        4 rows  750 Keyser Avenue,Natchitoches,LA,71457
      607.3K       10 rows  901 SOUTH AUSTIN BLVD,CHICAGO,IL,60644
      596.5K        7 rows  4437 SOUTH CICERO,CHICAGO,IL,60632
      591.7K        6 rows  50 NORTH JANE,ELGIN,IL,60123
      582.6K       15 rows  11515 TROOST,KANSAS CITY,MO,64131
      575.8K        7 rows  7001 CLEVELAND AVENUE,KANSAS CITY,MO,64132

PROVIDER_ADDRESS by rows
        27  17451 MEDICAL CENTER PARKWAY
        27  6909 WEST NORTH AVENUE
        26  9014 CEDAR AVE
        25  825  FIRST AVENUE NORTHWEST
        25  537 PAVONIA AVENUE
        25  1104 VENTURA AVE.
        24  23 KIERNAN RD
        24  100 ROSEWOOD VILLAGE DRIVE
        24  2060 Health Drive
        23  103 SOUTHWEST 9TH STREET
        23  200 LAUREL LAKE DR
        23  1899 N RAYMOND AVE
        22  13101 HARTFIELD AVE
        20  3015 W 29 ST
        20  3020 EAST 15TH STREET
        20  203 Bruce Court
        20  601 WEST 1ST STREET
        20  6501 W 75TH STREET
        19  1300 NORTH MAIN
        19  1229 S Jackson St

PROVIDER_ADDRESS by dollars
      883.2K        9 rows  10602 SOUTHWEST  HIGHWAY
      821.6K        9 rows  727 NORTH 17TH STREET
      810.4K       11 rows  131 N TUCKER
      804.8K        3 rows  135 Meridan St.
      798.5K       12 rows  3354 JEROME LANE
      754.4K        5 rows  13905 FM 2710
      738.3K        3 rows  1 O'BRIEN LANE
      702.0K        5 rows  2 ANNABLE COURT
      699.6K        4 rows  918 JAMES STREET
      656.5K        6 rows  122 Hillsdale Drive
      656.3K        7 rows  700 WHITE PLAINS ROAD
      631.9K       11 rows  10935 SOUTH HALSTED STREET
      625.1K        7 rows  2131 Alpine Rd
      619.6K        6 rows  5075 WEST SENECA TURNPIKE
      616.6K        4 rows  750 Keyser Avenue
      607.3K       10 rows  901 SOUTH AUSTIN BLVD
      596.5K        7 rows  4437 SOUTH CICERO
      591.7K        6 rows  50 NORTH JANE
      582.6K       15 rows  11515 TROOST
      575.8K        7 rows  7001 CLEVELAND AVENUE

CITY_TOWN by rows
       279  CHICAGO
       166  LOS ANGELES
        96  Houston
        73  LONG BEACH
        71  SAINT LOUIS
        69  Fort Worth
        60  MILWAUKEE
        58  COLUMBUS
        56  CLEVELAND
        55  SAN ANTONIO
        52  SPRINGFIELD
        49  PHILADELPHIA
        49  ORLANDO
        47  KANSAS CITY
        46  CINCINNATI
        45  Charlotte
        45  LAKEWOOD
        44  OVERLAND PARK
        41  PASADENA
        41  San Antonio

CITY_TOWN by dollars
      10.71M      279 rows  CHICAGO
       4.62M      166 rows  LOS ANGELES
       2.53M       96 rows  Houston
       2.23M       58 rows  COLUMBUS
       2.15M       71 rows  SAINT LOUIS
       1.92M       60 rows  MILWAUKEE
       1.92M       73 rows  LONG BEACH
       1.91M       69 rows  Fort Worth
       1.80M       29 rows  MEMPHIS
       1.72M       32 rows  WILMINGTON
       1.71M       31 rows  BELLEVILLE
       1.71M       27 rows  SAINT PETERSBURG
       1.54M       47 rows  KANSAS CITY
       1.52M       41 rows  San Antonio
       1.50M       17 rows  CAHOKIA
       1.48M       13 rows  SYRACUSE
       1.46M       31 rows  WASHINGTON
       1.44M       55 rows  SAN ANTONIO
       1.41M       30 rows  SARASOTA
       1.36M       25 rows  PITTSBURGH

## who x when

PROVIDER_NAME by PAYMENT_DENIAL_START_DATE, dollars = FINE_AMOUNT
  ABODE HEALTH AND WELLNESS CENTER          2025:1
  BERKELEY NURSING & REHAB CENTER           2025:1
  BISHOP REHABILITATION AND NURSING CENTER  2024:2
  BRIA OF CAHOKIA                           2024:3 2025:1
  CHANDLER THERAPY & LIVING CENTER LLC      2024:1
  CHICAGO RIDGE SNF                         2023:1 2024:1 2025:2
  EVERVELLA OF SWANSEA                      2024:1
  GOLDEN ROSE CARE CENTER                   2024:1
  Harbor Post Acute Center                  2024:1
  Henson Park Health & Rehabilitation       2023:1
  La Bella of Cahokia                       2024:1 2025:1
  Legacy Nursing at St. Christina           2023:1
  MAJESTIC GARDENS AT MEMPHIS REHAB & SNC   2023:1 2024:1
  MOHAWK MEADOWS                            2024:1
  Nexus Pavilion at Belleville              2024:1 2025:1
  PEACE CARE ST JOSEPH'S                    2025:1

LOCATION by PAYMENT_DENIAL_START_DATE, dollars = FINE_AMOUNT
  1 O'BRIEN LANE,LAFAYETTE,NJ,07848         2024:1
  100 ROSEWOOD VILLAGE DRIVE,SWANSEA,IL,62  2024:1
  10602 SOUTHWEST  HIGHWAY,CHICAGO RIDGE,I  2023:1 2024:1 2025:2
  122 Hillsdale Drive,Pineville,LA,71360    2023:1
  131 N TUCKER,MEMPHIS,TN,38104             2023:1 2024:1
  17451 MEDICAL CENTER PARKWAY,INDEPENDENC  2025:1
  1899 N RAYMOND AVE,PASADENA,CA,91103      2024:1
  2 ANNABLE COURT,CAHOKIA,IL,62206          2024:1 2025:1
  203 Bruce Court,Danville,KY,40422         2023:1
  2060 Health Drive,Wyoming,MI,49519        2024:1
  3354 JEROME LANE,CAHOKIA,IL,62206         2024:3 2025:1
  537 PAVONIA AVENUE,JERSEY CITY,NJ,07306   2025:1
  601 WEST 1ST STREET,CHANDLER,OK,74834     2024:1
  6909 WEST NORTH AVENUE,OAK PARK,IL,60302  2025:1
  727 NORTH 17TH STREET,BELLEVILLE,IL,6222  2024:1 2025:1
  918 JAMES STREET,SYRACUSE,NY,13203        2024:2

## where

STATE: TX 2.0K, IL 1.9K, CA 1.4K, FL 699, OH 683, MO 611, NC 598, PA 583, MI 503, WI 387, KS 380, NY 369

## what

PENALTY_TYPE: Fine 85%, Payment Denial 15%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CMS_CERTIFICATION_NUMBER_CCN | other | 6.8K | 0 | 555530 94; 675687 92; 555746 92; 745019 89 |
| PROVIDER_NAME | who | 6.7K | 0 | CHOWCHILLA MEMORIAL HEALT 94; HOLIDAY HILL INC 92; BAYSHIRE TORREY PINES POS 92; James L West Center for D 89 |
| PROVIDER_ADDRESS | who | 6.9K | 0 | 1104 VENTURA AVE. 94; 245 STATE HWY #153 WEST 92; 13101 HARTFIELD AVE 92; 1111 Summit Ave 89 |
| CITY_TOWN | who | 3.5K | 0 | CHICAGO 287; LOS ANGELES 166; Houston 152; Fort Worth 125 |
| STATE | state | 53 | 0 | TX 2.0K; IL 1.9K; CA 1.4K; FL 699 |
| ZIP_CODE | other | 5.3K | 0 | 93610 94; 77584 92; 76834 92; 92130 92 |
| PENALTY_DATE | date | 950 | 0 | 2023-07-17 152; 2023-12-11 145; 2024-01-22 132; 2023-08-14 128 |
| PENALTY_TYPE | category | 2 | 0 | Fine 13.7K; Payment Denial 2.5K |
| FINE_ID | id | 13.7K | 2.5K | 138194 69; 136610 69; 136447 69; 137697 69 |
| FINE_AMOUNT | amount | 6.6K | 2.5K | 4587 636; 8018 147; 4545 147; 16801 145 |
| PAYMENT_DENIAL_START_DATE | date | 721 | 13.7K | 2024-06-27 16; 2024-08-20 14; 2024-04-05 14; 2024-12-12 14 |
| PAYMENT_DENIAL_LENGTH_IN_DAYS | amount | 133 | 13.7K | 2 90; 7 90; 6 90; 1 89 |
| LOCATION | who | 6.9K | 0 | 1104 VENTURA AVE.,CHOWCHI 94; 245 STATE HWY #153 WEST,C 92; 13101 HARTFIELD AVE,SAN D 92; 1111 Summit Ave,Fort Wort 89 |
| PROCESSING_DATE | date | 1 | 0 | 2026-06-01 16.2K |
| _INGESTED_AT | audit | 1 | 0 | 1785104738770320 16.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 6797c8fe-cdea-43d7-9d1a-4 16.2K |
| _SRC_SHA256 | who | 1 | 0 | 937687ecb01f742663172947b 16.2K |
