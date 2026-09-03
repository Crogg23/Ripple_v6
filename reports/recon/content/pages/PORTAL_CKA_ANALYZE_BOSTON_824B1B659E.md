# PORTAL_CKA_ANALYZE_BOSTON_824B1B659E

rows 988  columns 28  scan 4.7s

roles: amount 6, audit 2, category 7, date 3, other 8, who 3

## when

LAST_FILED_DATE
  1998         1  
  1999         1  
  2000         2  #
  2001         1  
  2002         3  #
  2003         3  #
  2004         3  #
  2005         2  #
  2006         3  #
  2007        11  ####
  2008        14  #####
  2009         4  #
  2010        15  #####
  2011        24  ########
  2012        21  #######
  2013        45  ###############
  2014        39  #############
  2015        53  ##################
  2016        53  ##################
  2017        45  ###############
  2018        53  ##################
  2019        62  #####################
  2020        54  ##################
  2021        75  ##########################
  2022        74  #########################
  2023        88  ##############################
  2024        74  #########################
  2025        79  ###########################
  2026        47  ################

LAST_BOARD_APPROVED_DATE
  1999         1  
  2000         4  #
  2001         1  
  2002         2  #
  2003         1  
  2004         5  ##
  2005         1  
  2006         7  ##
  2007        10  ###
  2008        11  ####
  2009         5  ##
  2010        18  ######
  2011        29  ##########
  2012        22  ########
  2013        52  ##################
  2014        37  #############
  2015        47  ################
  2016        72  #########################
  2017        43  ###############
  2018        47  ################
  2019        62  ######################
  2020        51  ##################
  2021        55  ###################
  2022        72  #########################
  2023        75  ##########################
  2024        73  #########################
  2025        86  ##############################
  2026        35  ############

INGESTED_AT
  2026       988  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_RESIDENTIAL_UNITS | 755 | 0 | 40 | 793.12 | 2.7K | 77.4K |
| TOTAL_DEVELOPMENT_COST | 941 | 0 | 25.00M | 1.00B | 1.90B | 90.49B |
| LONGITUDE | 988 | -71.18 | -71.07 | -71.01 | -71 | -70.2K |
| LATITUDE | 988 | 42.24 | 42.34 | 42.39 | 42.40 | 41.8K |
| POINT_X | 988 | -71.18 | -71.07 | -71.01 | -71 | -70.2K |
| POINT_Y | 988 | 42.24 | 42.34 | 42.39 | 42.40 | 41.8K |

## who

PROJECT__PROJECT_NAME by rows
         1  1400 Boylston Street
         1  1035 Commonwealth Avenue
         1  12-28 Lansdowne Street (Fenway Theater)
         1  103 North Beacon Street
         1  1545-1555 VFW Parkway (Parkway Apartments)
         1  11 Taft Hill Terrace
         1  120 Braintree Street
         1  134 Hampden Street
         1  12 Post Office Square
         1  141 Addison Street
         1  1595-1599 Columbus Avenue
         1  148-152 Dorchester Avenue
         1  131 North Beacon Street
         1  135 Morrissey Boulevard
         1  105 West First Street
         1  1 & 10 Emerson Place
         1  154 Terrace Street
         1  157 Humboldt Avenue
         1  11 Avenue De Lafayette
         1  114-122 Harvard Street and 18-24 Standish Street

PROJECT__PROJECT_NAME by dollars
       1.90B        1 rows  South Station Air Rights
       1.88B        1 rows  MGH Clinical Building
       1.65B        1 rows  1 Joslin Place Hospital
       1.46B        1 rows  Bunker Hill Housing Redevelopment
       1.45B        1 rows  Exchange South End
       1.44B        1 rows  Fenway Corners (West)
       1.30B        1 rows  115 Winthrop Square
       1.20B        1 rows  244-284 A Street
       1.00B        1 rows  Back Bay/South End Gateway Project
       1.00B        1 rows  776 Summer Street - Phase 1
       1.00B        1 rows  776 Summer Street - Phase 2
       1.00B        1 rows  Harvard Enterprise Research Campus (ERC) Phase A
       1.00B        1 rows  66 Cambridge Street
       1.00B        1 rows  Harvard University - Science and Engineering Complex
     864.32M        1 rows  Seaport Square - Block M
     850.00M        1 rows  176 Lincoln Street
     850.00M        1 rows  Boston Childrens Hospital - Clinical Building
     800.00M        1 rows  Fan Pier - Parcels A and B
     780.00M        1 rows  40 Roland Street
     750.00M        1 rows  Seaport Square - Block L3 & L6

PROJECT_STREET_NAME by rows
        60  Washington
        31  Dorchester
        18  Commonwealth
        18  West Broadway
        17  Western
        16  Centre
        14  Harrison
        14  Boylston
        13  Cambridge
        13  Huntington
        13  Tremont
        11  Blue Hill
        11  Albany
        10  River
        10  Summer
        10  Seaport
        10  Morrissey
        10  Columbus
         9  Congress
         9  A

PROJECT_STREET_NAME by dollars
       3.52B       60 rows  Washington
       3.32B       13 rows  Cambridge
       3.25B       17 rows  Western
       3.09B        8 rows  Northern
       2.91B       10 rows  Seaport
       2.80B       14 rows  Boylston
       2.66B       10 rows  Summer
       2.39B       11 rows  Albany
       2.37B        9 rows  A
       2.19B        7 rows  Brookline
       2.05B        3 rows  Atlantic
       1.88B       13 rows  Huntington
       1.82B       18 rows  Commonwealth
       1.65B        1 rows  Joslin
       1.65B        9 rows  Congress
       1.48B        2 rows  Bunker Hill
       1.44B        1 rows  Jersey
       1.34B        4 rows  Lincoln
       1.30B        1 rows  Winthrop
       1.29B        2 rows  New Sudbury

SRC_SHA256 by rows
       988  3cffa797a6fd0652c696daa7bd48c701f7282c1aea8d7309f01cc884ee316b4e

SRC_SHA256 by dollars
      90.49B      988 rows  3cffa797a6fd0652c696daa7bd48c701f7282c1aea8d7309f01cc884ee31

## who x when

PROJECT__PROJECT_NAME by LAST_FILED_DATE, dollars = TOTAL_DEVELOPMENT_COST
  1 & 10 Emerson Place                      2025:12.00M
  1 Joslin Place Hospital                   2025:1.65B
  103 North Beacon Street                   2023:200.00M
  1035 Commonwealth Avenue                  2023:15.00M
  105 West First Street                     2017:150.00M
  11 Avenue De Lafayette                    2026:7.40M
  11 Taft Hill Terrace                      2019:6.10M
  114-122 Harvard Street and 18-24 Standis  2023:12.50M
  115 Winthrop Square                       2020:1.30B
  12 Post Office Square                     2025:9.50M
  12-28 Lansdowne Street (Fenway Theater)   2019:100.00M
  120 Braintree Street                      2025:10.38M
  131 North Beacon Street                   2023:46.00M
  134 Hampden Street                        2025:10.00M
  135 Morrissey Boulevard                   2023:130.00M
  1400 Boylston Street                      2023:600.00M
  141 Addison Street                        2023:7.00M
  148-152 Dorchester Avenue                 2013:10.00M
  154 Terrace Street                        2025:33.00M
  1545-1555 VFW Parkway (Parkway Apartment  2018:70.12M
  157 Humboldt Avenue                       2023:17.64M
  1595-1599 Columbus Avenue                 2019:30.00M
  244-284 A Street                          2026:1.20B
  776 Summer Street - Phase 1               2022:1.00B
  Back Bay/South End Gateway Project        2017:1.00B
  Bunker Hill Housing Redevelopment         2021:1.46B
  Exchange South End                        2018:1.45B
  Fenway Corners (West)                     2023:1.44B
  MGH Clinical Building                     2021:1.88B
  South Station Air Rights                  2017:1.90B

PROJECT_STREET_NAME by LAST_FILED_DATE, dollars = TOTAL_DEVELOPMENT_COST
  A                                         2012:225.00M 2014:37.60M 2015:8.25M 2018:150.00M 2024:720.00M 2026:1.22B
  Albany                                    2005:375.00M 2007:125.00M 2013:303.00M 2015:50.00M 2018:1.45B 2019:50.00M 2024:34.00M
  Atlantic                                  2017:1.90B 2022:150.00M 2026:1
  Blue Hill                                 2009:7.00M 2014:22.50M 2015:41.19M 2019:9.50M 2022:8.50M 2023:13.43M 2025:9.36M 2026:72.30M
  Boylston                                  2007:271.50M 2010:250.00M 2013:80.00M 2014:100.00M 2015:265.90M 2018:63.00M 2019:320.00M 2021:700.00M 2023:600.00M 2026:7.76M
  Brookline                                 2007:300.00M 2008:300.00M 2015:125.00M 2016:240.00M 2021:550.00M 2022:250.00M 2026:423.88M
  Bunker Hill                               2014:22.09M 2021:1.46B
  Cambridge                                 2008:7.87M 2010:6.00M 2014:7.00M 2016:52.00M 2021:1.88B 2024:1.01B 2025:202.00M 2026:153.32M
  Centre                                    2003:5.50M 2006:0 2015:15.30M 2020:5.00M 2021:261.00M 2022:46.25M 2023:157.38M 2025:62.50M 2026:61.83M
  Columbus                                  2013:225.00M 2017:40.00M 2019:490.00M 2022:24.00M 2023:38.00M 2024:365.00M
  Commonwealth                              2012:172.00M 2013:40.00M 2014:188.00M 2016:49.00M 2018:22.00M 2019:289.00M 2020:459.00M 2022:13.00M 2023:135.00M 2024:450.00M 2025:5.50M
  Congress                                  2011:17.50M 2013:175.00M 2019:148.00M 2020:450.00M 2022:460.00M 2026:112.00M
  Dorchester                                2013:30.50M 2014:48.50M 2015:11.00M 2016:14.00M 2017:11.00M 2018:20.00M 2019:212.00M 2020:25.95M 2021:17.00M 2022:211.00M 2023:65.00M 2024:45.00M 2025:45.70M 2026:1
  Harrison                                  2012:6.00M 2013:183.00M 2014:30.00M 2015:218.00M 2016:54.00M 2017:255.15M 2019:45.00M 2021:129.00M 2024:1
  Huntington                                2003:450.00M 2007:20.00M 2010:60.00M 2012:79.00M 2019:340.00M 2021:74.00M 2022:200.00M 2024:390.00M 2026:234.00M
  Jersey                                    2023:1.44B
  Joslin                                    2025:1.65B
  Lincoln                                   2019:39.50M 2022:1.30B
  Morrissey                                 2012:12.00M 2019:1.00M 2020:90.00M 2021:13.50M 2022:163.93M 2023:180.00M 2025:450.00M
  New Sudbury                               2021:1.29B
  Northern                                  1999:800.00M 2014:600.00M 2016:317.00M 2021:270.00M 2022:700.00M
  River                                     2015:30.00M 2017:77.91M 2019:18.75M 2021:32.00M 2023:35.00M 2025:12.00M
  Seaport                                   2007:103.60M 2008:230.00M 2015:281.00M 2016:1.34B 2017:1 2019:300.00M 2022:650.00M
  Summer                                    2008:32.00M 2016:160.00M 2017:100.00M 2019:200.00M 2022:1.00B 2023:75.00M 2024:17.00M 2025:1.00B 2026:73.30M
  Tremont                                   2014:9.70M 2016:8.50M 2017:43.50M 2018:3.10M 2022:56.00M 2023:35.00M 2024:100.00M 2025:99.40M
  Washington                                2008:42.00M 2010:230.00M 2011:7.27M 2012:3.43M 2013:127.37M 2014:83.50M 2015:25.00M 2016:39.70M 2017:40.03M 2018:69.50M 2019:126.50M 2020:293.53M 2021:409.88M 2022:104.70M 2023:1.00B 2024:16.70M 2025:210.67M 2026:17.50M
  West Broadway                             2008:5.00M 2010:25.50M 2012:12.50M 2013:35.00M 2014:53.50M 2016:101.10M 2018:8.00M 2019:18.00M 2020:108.50M 2021:30.00M 2025:29.00M
  Western                                   2009:180.00M 2013:43.00M 2015:120.00M 2016:251.50M 2017:1.00B 2019:18.00M 2021:310.00M 2022:1.00B 2023:100.00M 2024:160.00M 2026:13.00M
  Winthrop                                  2020:1.30B

## what

PROJECT_STREET_SUFFIX: Street 65%, Avenue 23%, Road 3%, Blvd 2%, Place 1%, Way 1%, Highway 1%, Drive 1%, Square 1%, Parkway 1%, Court 0%, Park 0%

NEIGHBORHOOD: Dorchester 14%, South Boston 13%, Roxbury 10%, Brighton 10%, South Boston Waterfront 9%, Allston 8%, East Boston 8%, Jamaica Plain 6%, Fenway 6%, Downtown 6%, South End 5%, Mission Hill 4%

PROJECT_ZIP_CODE: 02127 17%, 02135 12%, 02210 11%, 02128 10%, 02134 9%, 02119 8%, 02130 8%, 02118 7%, 02125 7%, 02215 6%, 02115 5%

PROJECT_STATUS: Construction Complete 59%, Board Approved 26%, Permitted / Under Construction 10%, Under Review 5%, Letter of Intent 1%, Prefile (Default) 0%

PROJECT__RECORD_TYPE: Large Project 54%, Small Project 46%

POPS: 0 82%, 1 18%

PROJECT_USES: Residential 39%, Residential; Retail 34%, Residential; Retail; Parking 6%, Residential; Parking 5%, Hotel 5%, Industrial 2%, Residential; Office; Retail 2%, Office; Retail; Research Lab 2%, Dormitory 2%, Education 2%, Retail; Hotel 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROJECT_ID | other | 967 | 0 | 1503 5; 1633 5; 1460 5; 3608 5 |
| PROJECT__PROJECT_NAME | who | 982 | 0 | YMCA Renovation (Fenway) 5; YMCA (West Roxbury) 5; Winsor School Project 5; Willow Baker Development 5 |
| PROJECT_STREET_NUMBER | other | 628 | 0 | 1 23; 100 15; 10 13; 50 11 |
| PROJECT_STREET_NAME | who | 384 | 0 | Washington 60; Dorchester 31; West Broadway 18; Commonwealth 18 |
| PROJECT_STREET_SUFFIX | category | 17 | 0 | Street 637; Avenue 221; Road 33; Blvd 24 |
| NEIGHBORHOOD | category | 25 | 0 | Dorchester 113; South Boston 106; Roxbury 78; Brighton 76 |
| PROJECT_ZIP_CODE | category | 45 | 75 | 02127 103; 02135 71; 02210 63; 02128 61 |
| PROJECT_STATUS | category | 6 | 0 | Construction Complete 582; Board Approved 252; Permitted / Under Constru 96; Under Review 48 |
| PROJECT__RECORD_TYPE | category | 2 | 0 | Large Project 535; Small Project 453 |
| DISPLAY_ON_WEB | other | 1 | 0 | 1 988 |
| POPS | category | 2 | 0 | 0 815; 1 173 |
| LAST_FILED_DATE | date | 793 | 39 | 6/30/2025 10; 10/28/2020 9; 2/20/2024 8; 5/6/2022 7 |
| LAST_BOARD_APPROVED_DATE | date | 244 | 64 | 11/14/2013 18; 12/11/2025 12; 6/16/2022 11; 3/13/2025 11 |
| PROJECT_USES | category | 42 | 765 | Residential 74; Residential; Retail 63; Residential; Retail; Park 11; Residential; Parking 10 |
| TOTAL_RESIDENTIAL_UNITS | amount | 228 | 233 | 0 94; 18 21; 36 19; 24 19 |
| GROSS_SQUARE_FOOTAGE | other | 868 | 0 | 0 88; 350000 7; 105000 6; 112000 6 |
| TOTAL_DEVELOPMENT_COST | amount | 390 | 47 | 10000000 24; 12000000 24; 6000000 19; 30000000 18 |
| SAM_IDS | other | 750 | 245 | 76356 4; 13911 4; 439771,150196,7609 4; 459503 4 |
| DESCRIPTION | other | 973 | 27 | Proposal calls for the de 5; Proposal calls for the de 5; Pilgrim Road Project/Long 5; The proposed project cons 5 |
| WEBSITE_URL | other | 993 | 0 | http://www.bostonplans.or 5; http://www.bostonplans.or 5; http://www.bostonplans.or 5; http://www.bostonplans.or 5 |
| LONGITUDE | amount | 878 | 0 | -71.062200000000004 7; -71.100427730000007 7; -71.122767089999996 7; -71.073280749999995 7 |
| LATITUDE | amount | 811 | 0 | 42.347400000000000 8; 42.332299999999996 7; 42.338944980000001 7; 42.366700039999998 7 |
| SHAPE_WKT | other | 964 | 0 | POINT (-71.10042712699998 7; POINT (-71.12276647699997 7; POINT (-71.07328015599995 7; POINT (-71.08659940199993 6 |
| POINT_X | amount | 936 | 0 | -71.100427126999989 7; -71.122766476999971 7; -71.073280155999953 7; -71.046342713999934 6 |
| POINT_Y | amount | 916 | 0 | 42.338936312000044 7; 42.366691368000033 7; 42.334982542000034 7; 42.340491331000067 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:48:15.79345 988 |
| SOURCE_RUN_ID | audit | 1 | 0 | 797cb05e-ffbd-440c-bb4c-8 988 |
| SRC_SHA256 | who | 1 | 0 | 3cffa797a6fd0652c696daa7b 988 |
