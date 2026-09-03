# PORTAL_CKA_ANALYZE_BOSTON_80FF6D8E34

rows 1.2K  columns 20  scan 4.3s

roles: amount 2, audit 2, category 4, date 3, id 1, other 3, who 6

## when

ISSUED
  2014       570  ##############################
  2015        36  ##
  2016        40  ##
  2017        55  ###
  2018        56  ###
  2019        96  #####
  2020        27  #
  2021        43  ##
  2022        71  ####
  2023        82  ####
  2024        69  ####
  2025        59  ###
  2026        35  ##

EXPIRES
  2019         1  
  2025        26  #
  2026      1.2K  ##############################

INGESTED_AT
  2026      1.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GPSX | 1.2K | 0 | 773.8K | 788.9K | 792.1K | 917.20M |
| GPSY | 1.2K | 0 | 2.95M | 2.97M | 2.97M | 3.51B |

## who

DBA_NAME by rows
         5  Tatte Bakery & Cafe
         5  Dunkin Donuts
         3  J.P. Licks
         3  Dave's Hot Chicken
         3  Wendy's
         3  Sweetgreen
         3  Five Guys
         3  Serafina
         2  Delta Sky Club
         2  Nan Xiang Express
         2  New York Pizza
         2  J.P. Licks Homemade Ice Cream
         2  Wahlburgers
         2  Shy Bird
         2  Davio's
         2  J.J. Foley's
         2  Shake Shack
         2  Row 34
         2  The Daily Catch
         2  Democracy Brewing

DBA_NAME by dollars
       3.83M        5 rows  Dunkin Donuts
       3.10M        5 rows  Tatte Bakery & Cafe
       2.32M        3 rows  Serafina
       2.31M        3 rows  Dave's Hot Chicken
       2.31M        3 rows  Wendy's
       2.30M        3 rows  Sweetgreen
       2.30M        3 rows  J.P. Licks
       1.57M        2 rows  Boston Harbor Distillery
       1.56M        2 rows  Democracy Brewing
       1.55M        2 rows  The Daily Catch
       1.55M        2 rows  Marriott's Custom House
       1.55M        2 rows  Potbelly Sandwich Shop
       1.55M        2 rows  Room Escapers
       1.55M        2 rows  Wahlburgers
       1.55M        2 rows  Del Frisco's Double Eagle Steakhouse
       1.55M        2 rows  J.J. Foley's
       1.55M        2 rows  Joe's American Bar & Grill
       1.55M        2 rows  Wagamama
       1.55M        2 rows  Nan Xiang Express
       1.54M        2 rows  South End Buttery

BUSINESS_NAME by rows
        26  Starbucks Corporation
         9  Tatte Holdings, LLC
         6  LSF LOGAN AIRPORT, LLC
         5  TRUSTEES OF BOSTON UNIVERSITY
         4  Northeastern University
         4  Chipotle Mexican Grill of Colorado, LLC
         4  Boston College
         3  SODEXO OPERATIONS, LLC
         3  Trustees of Boston University
         3  Air Ventures, LLC
         3  Delaware North Boston Flight, LLC.
         3  Colwen Management, Inc.
         3  HSI MCA BOS FB, LLC.
         2  J.P. Lick's Homemade Ice Cream Co., Inc.
         2  MARRIOTT RESORTS HOSPITALITY CORPORATION
         2  BBRG TR, LLC
         2  Air Ventures, LLC.
         2  Hyde Park Burgers, LLC
         2  CT Eatery, LLC
         2  Room Escapers, LLC.

BUSINESS_NAME by dollars
      18.50M       26 rows  Starbucks Corporation
       6.18M        9 rows  Tatte Holdings, LLC
       3.81M        5 rows  TRUSTEES OF BOSTON UNIVERSITY
       3.07M        4 rows  Northeastern University
       3.07M        4 rows  Chipotle Mexican Grill of Colorado, LLC
       2.98M        4 rows  Boston College
       2.36M        3 rows  SODEXO OPERATIONS, LLC
       2.35M        6 rows  LSF LOGAN AIRPORT, LLC
       2.29M        3 rows  Colwen Management, Inc.
       2.29M        3 rows  Trustees of Boston University
       1.57M        2 rows  Air Ventures, LLC.
       1.57M        2 rows  SSP AMERICA, INC.
       1.57M        3 rows  Delaware North Boston Flight, LLC.
       1.56M        2 rows  APCV Boston Hotel LLC
       1.55M        2 rows  MARRIOTT RESORTS HOSPITALITY CORPORATION
       1.55M        2 rows  Hampshire House Corporation
       1.55M        2 rows  Potbelly Sandwich Works, LLC
       1.55M        2 rows  Room Escapers, LLC.
       1.55M        2 rows  Emerson College
       1.54M        2 rows  Big House Fine Dining, LLC

APPLICANT by rows
         8  Tzurit Or
         7  LISA BAKER
         7  Douglas Bacon
         7  Mary Her
         6  Antonio Alicea
         6  Leonardo Leite
         5  Rory Dugan
         5  David Doward
         5  Dougles Runge
         5  So Lim Ting
         4  Jin Chong
         4  Thomas Keady, Jr
         4  Michael Shaw
         4  Jacqueline Genao
         4  Mark Clemency
         4  John Schall
         4  FRANK DEPASQUALE
         4  Michelle Freedman
         3  Thomas Devlin
         3  James Cochener

APPLICANT by dollars
       5.41M        8 rows  Tzurit Or
       5.41M        7 rows  LISA BAKER
       4.55M        7 rows  Douglas Bacon
       3.88M        5 rows  Rory Dugan
       3.85M        5 rows  So Lim Ting
       3.82M        7 rows  Mary Her
       3.11M        4 rows  FRANK DEPASQUALE
       3.10M        4 rows  Michael Shaw
       3.07M        4 rows  John Schall
       3.06M        4 rows  Michelle Freedman
       3.04M        4 rows  Jin Chong
       2.98M        4 rows  Thomas Keady, Jr
       2.36M        4 rows  Jacqueline Genao
       2.36M        4 rows  Mark Clemency
       2.35M        6 rows  Leonardo Leite
       2.33M        3 rows  Mark Malatesta
       2.33M        3 rows  Ann Somers
       2.32M        3 rows  Thomas Kershaw
       2.32M        3 rows  Mevzad Durakovic
       2.32M        3 rows  Jefferson Macklin

STATUS by rows
      1.2K  Active

STATUS by dollars
     917.20M     1.2K rows  Active

## who x when

DBA_NAME by ISSUED, dollars = GPSX
  Boston Harbor Distillery                  2019:780.3K 2023:786.0K
  Dave's Hot Chicken                        2024:1.55M 2025:765.4K
  Davio's                                   2014:772.3K 2019:0
  Del Frisco's Double Eagle Steakhouse      2014:780.9K 2025:768.9K
  Delta Sky Club                            2014:0 2023:0
  Democracy Brewing                         2018:774.5K 2025:781.0K
  Dunkin Donuts                             2014:1.51M 2018:749.9K 2022:1.57M
  Five Guys                                 2019:1.53M
  J.J. Foley's                              2014:1.55M
  J.P. Licks                                2014:749.0K 2018:1.55M
  J.P. Licks Homemade Ice Cream             2014:1.52M
  Joe's American Bar & Grill                2014:1.55M
  Marriott's Custom House                   2014:1.55M
  Nan Xiang Express                         2023:774.9K 2024:770.6K
  New York Pizza                            2014:1.54M
  Potbelly Sandwich Shop                    2014:1.55M
  Room Escapers                             2019:1.55M
  Row 34                                    2014:778.4K 2025:765.4K
  Serafina                                  2019:1.54M 2022:779.0K
  Shake Shack                               2015:0 2020:778.8K
  Shy Bird                                  2023:776.2K 2025:763.9K
  South End Buttery                         2014:772.3K
  Sweetgreen                                2018:764.1K 2022:1.54M
  Tatte Bakery & Cafe                       2019:3.10M
  The Daily Catch                           2014:776.7K 2023:777.4K
  Wagamama                                  2014:1.55M
  Wahlburgers                               2015:764.1K 2016:786.8K
  Wendy's                                   2014:2.31M

BUSINESS_NAME by ISSUED, dollars = GPSX
  APCV Boston Hotel LLC                     2016:1.56M
  Air Ventures, LLC                         2014:0 2018:0
  Air Ventures, LLC.                        2019:786.3K 2020:786.3K
  BBRG TR, LLC                              2014:1.54M
  Big House Fine Dining, LLC                2014:1.54M
  Boston College                            2014:2.98M
  CT Eatery, LLC                            2021:771.7K 2023:771.6K
  Chipotle Mexican Grill of Colorado, LLC   2014:3.07M
  Colwen Management, Inc.                   2018:1.53M 2019:769.3K
  Delaware North Boston Flight, LLC.        2019:786.0K 2021:785.4K
  Emerson College                           2014:1.55M
  HSI MCA BOS FB, LLC.                      2019:786.3K 2020:0
  Hampshire House Corporation               2014:1.55M
  Hyde Park Burgers, LLC                    2019:775.5K
  J.P. Lick's Homemade Ice Cream Co., Inc.  2014:1.52M
  LSF LOGAN AIRPORT, LLC                    2021:1.57M 2024:784.4K
  MARRIOTT RESORTS HOSPITALITY CORPORATION  2014:1.55M
  Northeastern University                   2014:2.30M 2021:767.3K
  Potbelly Sandwich Works, LLC              2014:1.55M
  Room Escapers, LLC.                       2019:1.55M
  SODEXO OPERATIONS, LLC                    2018:786.8K 2023:786.0K 2025:786.3K
  SSP AMERICA, INC.                         2023:786.0K 2024:786.0K
  Starbucks Corporation                     2014:11.53M 2016:2.33M 2017:772.6K 2018:2.32M 2024:1.54M
  TRUSTEES OF BOSTON UNIVERSITY             2014:759.5K 2018:761.8K 2026:2.29M
  Tatte Holdings, LLC                       2017:764.5K 2018:2.32M 2019:3.10M
  Trustees of Boston University             2014:2.29M

## what

LICENSE_TYPE: Non-Live Entertainment 69%, Live Entertainment 18%, Night Club 13%

CITY: Boston 56%, East Boston 10%, Dorchester 7%, Roxbury 6%, Allston 5%, South Boston 4%, Brighton 4%, Jamaica Plain 2%, Charlestown 2%, Hyde Park 1%, Roslindale 1%, West Roxbury 1%

STATE: MA 100%, Ma 0%

ZIP: 02116 15%, 02128 15%, 02210 10%, 02215 8%, 02113 7%, 02134 7%, 02111 7%, 02118 6%, 02115 6%, 02127 6%, 02108 6%, 02109 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LICENSE_NUM | id | 1.2K | 0 | CAL-133030 7; CAL-133494 7; CAL-133350 7; CAL-132871 7 |
| STATUS | who | 1 | 0 | Active 1.2K |
| LICENSE_TYPE | category | 3 | 0 | Non-Live Entertainment 856; Live Entertainment 223; Night Club 161 |
| ISSUED | date | 520 | 1 | 2014-09-12 569; 2021-08-17 10; 2025-12-23 9; 2017-08-28 6 |
| EXPIRES | date | 3 | 0 | 2026-12-31 1.2K; 2025-12-31 26; 2019-12-31 1 |
| BUSINESS_NAME | who | 1.2K | 1 | Starbucks Corporation 26; Tatte Holdings, LLC 10; Boston College 8; HAJJ, INC. 7 |
| DBA_NAME | who | 1.2K | 0 | Mike's City Diner 7; Alwadi Restaurant 7; Himalayan Bistro 7; Jade Garden Restaurant 7 |
| COMMENTS | who | 622 | 32 | 1 ENTERTAINMENT IS NOT PE 191; 1 Entertainment is not pe 53; 1 Entertainment is NOT pe 53; 1 ENTERTAINMENT IS NOT PE 52 |
| LOCATION_COMMENTS | other | 109 | 1.1K | 1330 Boylston Street, Bos 3; 250 Northern Avenue, Bost 3; 9 Tyler Street, Boston, M 2; 2601 Beacon Street, Bosto 2 |
| APPLICANT | who | 1.1K | 0 | Mary Her 10; LISA BAKER 10; Tzurit Or 9; Thomas Keady, Jr 8 |
| MANAGER | other | 1.1K | 0 | Mary Her 10; LISA BAKER 10; Tzurit Or 9; Thomas Keady, Jr 8 |
| ADDRESS | other | 1.1K | 0 | 200     Logan Airport Ter 8; 1330-  Boylston ST 8; 1714-  Washington ST 7; 1249-  VFW PW 7 |
| CITY | category | 17 | 0 | Boston 685; East Boston 128; Dorchester 80; Roxbury 70 |
| STATE | category | 3 | 1 | MA 1.2K; Ma 2 |
| ZIP | category | 30 | 0 | 02116 136; 02128 128; 02210 91; 02215 74 |
| GPSX | amount | 1.1K | 10 | 0 41; 764631.7121359706 8; 774534.1339321434 7; 775108.7915754765 7 |
| GPSY | amount | 1.1K | 10 | 0 41; 2950640.718398556 8; 2958753.264181316 7; 2955385.2082533985 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:51:36.05316 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | b171568b-1a33-463b-b195-2 1.2K |
| SRC_SHA256 | who | 1 | 0 | d11fdf761f21a43941d2c7b5f 1.2K |
