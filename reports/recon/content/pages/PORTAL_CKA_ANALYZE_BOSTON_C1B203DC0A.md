# PORTAL_CKA_ANALYZE_BOSTON_C1B203DC0A

rows 3.6K  columns 29  scan 4.7s

roles: amount 2, audit 2, category 5, date 3, id 2, other 8, who 8

## when

ISSUED
  2013      1.8K  ##############################
  2014       566  ##########
  2015        95  ##
  2016        94  ##
  2017        73  #
  2018        67  #
  2019        72  #
  2020        55  #
  2021        78  #
  2022        67  #
  2023        98  ##
  2024       181  ###
  2025       256  ####
  2026       147  ##

EXPIRES
  2020         1  
  2024         2  
  2025       183  ##
  2026      3.1K  ##############################
  2027       365  ####
  2028         2  

INGESTED_AT
  2026      3.6K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GPSX | 3.6K | 0 | 770.7K | 786.8K | 792.1K | 2.64B |
| GPSY | 3.6K | 0 | 2.95M | 2.97M | 2.97M | 10.12B |

## who

BUSINESS_NAME by rows
       160  TRUSTEES OF BOSTON UNIVERSITY
        35  NORTHEASTERN UNIVERSITY
        26  Starbucks Corporation
        16  THE WALDWIN GROUP, INC.
        16  WENTWORTH INSTITUTE OF TECHNOLOGY
        13  Caffe Nero Americas, Inc.
        13  Tatte Holdings, LLC
        11  HSI MCA BOS FB, LLC
        10  SWEETGREEN BOSTON, LLC
         9  WATERMARK DONUT COMPANY
         9  SIMMONS COLLEGE
         8  Selhi Associates, LLC
         8  Delaware North Boston Flight, LLC
         8  SODEXO OPERATIONS, LLC
         8  Air Ventures, LLC
         8  CHIPOTLE MEXICAN GRILL OF COLORADO, LLC
         8  PINE STREET INN
         7  WHOLE FOODS MARKET GROUP, INC.
         6  FISHER COLLEGE
         6  STAR MARKETS COMPANY, INC.

BUSINESS_NAME by dollars
     122.14M      160 rows  TRUSTEES OF BOSTON UNIVERSITY
      26.85M       35 rows  NORTHEASTERN UNIVERSITY
      18.50M       26 rows  Starbucks Corporation
      12.24M       16 rows  WENTWORTH INSTITUTE OF TECHNOLOGY
      10.80M       16 rows  THE WALDWIN GROUP, INC.
      10.02M       13 rows  Caffe Nero Americas, Inc.
       9.27M       13 rows  Tatte Holdings, LLC
       7.72M       10 rows  SWEETGREEN BOSTON, LLC
       6.97M        9 rows  WATERMARK DONUT COMPANY
       6.87M        9 rows  SIMMONS COLLEGE
       6.17M        8 rows  Selhi Associates, LLC
       6.15M        8 rows  PINE STREET INN
       6.14M        8 rows  CHIPOTLE MEXICAN GRILL OF COLORADO, LLC
       5.40M        7 rows  WHOLE FOODS MARKET GROUP, INC.
       4.71M        8 rows  Delaware North Boston Flight, LLC
       4.66M        6 rows  BOSTON HOSPITALITY PARTNERS LLC
       4.64M        6 rows  Make Life Sweeter, LLC
       4.63M        6 rows  WATERMARK DONUT CO.
       4.63M        6 rows  FISHER COLLEGE
       4.62M        6 rows  STAR MARKETS COMPANY, INC.

DBA_NAME by rows
       147  BOSTON UNIVERSITY
        73  DUNKIN DONUTS
        31  NORTHEASTERN UNIVERSITY
        21  M.I.T
        16  Dunkin Donuts
        16  WENTWORTH INSTITUTE OF TECHNOLOGY
        13  McDonald's
        12  Tatte Bakery & Cafe
        12  Caffe Nero
        10  BURGER KING
         9  Sweetgreen
         8  HARVARD BUSINESS SCHOOL
         6  Domino's Pizza
         6  Panera Bread
         6  P. SULLIVAN HOUSING TRUST
         6  SUBWAY
         5  Taco Bell
         5  Gong Cha
         5  Flour Bakery & Cafe
         5  Legal Sea Foods

DBA_NAME by dollars
     112.23M      147 rows  BOSTON UNIVERSITY
      49.23M       73 rows  DUNKIN DONUTS
      23.78M       31 rows  NORTHEASTERN UNIVERSITY
      16.10M       21 rows  M.I.T
      12.24M       16 rows  WENTWORTH INSTITUTE OF TECHNOLOGY
       9.25M       12 rows  Caffe Nero
       8.50M       12 rows  Tatte Bakery & Cafe
       8.44M       13 rows  McDonald's
       7.71M       16 rows  Dunkin Donuts
       6.95M        9 rows  Sweetgreen
       6.92M       10 rows  BURGER KING
       6.07M        8 rows  HARVARD BUSINESS SCHOOL
       4.63M        6 rows  P. SULLIVAN HOUSING TRUST
       4.61M        6 rows  SUBWAY
       4.60M        6 rows  Panera Bread
       4.56M        6 rows  Domino's Pizza
       3.87M        5 rows  Flour Bakery & Cafe
       3.86M        5 rows  Dunkin'
       3.85M        5 rows  Taco Bell
       3.85M        5 rows  Anna's Taqueria

APPLICANT by rows
       146   TRUSTEES OF BOSTON UNIVERSITY
        24   NORTHEASTERN UNIVERSITY
        23   STARBUCKS CORPORATION
        17   WENTWORTH INSTITUTE OF TECHNOLOGY
        15   Northeastern University
        15   Trustees of Boston University
        12   Tatte Holdings, LLC
        11   HSI MCA BOS FB, LLC
        10   THE WALDWIN GROUP, INC.
        10   Sweetgreen Boston, LLC
        10   WATERMARK DONUT COMPANY
        10   Caffe Nero Americas, Inc.
         9   SIMMONS COLLEGE
         8   Delaware North Boston Flight, LLC
         8   Selhi Associates, LLC
         8   PINE STREET INN
         7   WATERMARK DONUT CO.
         6   Sodexo Operations, LLC
         6   Air Ventures, LLC
         6   Nicosia Family 2012 Irrevocable Trust

APPLICANT by dollars
     111.45M      146 rows   TRUSTEES OF BOSTON UNIVERSITY
      18.41M       24 rows   NORTHEASTERN UNIVERSITY
      16.18M       23 rows   STARBUCKS CORPORATION
      13.01M       17 rows   WENTWORTH INSTITUTE OF TECHNOLOGY
      11.51M       15 rows   Northeastern University
      11.45M       15 rows   Trustees of Boston University
       8.50M       12 rows   Tatte Holdings, LLC
       7.74M       10 rows   WATERMARK DONUT COMPANY
       7.73M       10 rows   Sweetgreen Boston, LLC
       7.71M       10 rows   THE WALDWIN GROUP, INC.
       7.71M       10 rows   Caffe Nero Americas, Inc.
       6.87M        9 rows   SIMMONS COLLEGE
       6.17M        8 rows   Selhi Associates, LLC
       6.15M        8 rows   PINE STREET INN
       5.41M        7 rows   WATERMARK DONUT CO.
       4.71M        8 rows   Delaware North Boston Flight, LLC
       4.63M        6 rows   FISHER COLLEGE
       4.61M        6 rows   Nicosia Family 2012 Irrevocable Trust
       4.55M        6 rows   HARVARD UNIVERSITY
       3.88M        5 rows   Boston Hospitality Partners LLC

CLOSING by rows
       731  11:00 PM
       642  2:00 AM
       410  1:00 AM
       324  10:00 PM
       184  9:00 PM
       163  12:00 AM
       122  MIDNIGHT
        96  8:00 PM
        91  7:00 PM
        41  6:00 PM
        32  5:00 PM
        32  10:30 PM
        29  3:00 AM
        23  3:00 PM
        23  11:30 PM
        22  Midnight
        18  9:30 PM
        18  24 HOURS
        15  4:00 PM
        12  N/A

CLOSING by dollars
     533.32M      731 rows  11:00 PM
     436.07M      642 rows  2:00 AM
     294.66M      410 rows  1:00 AM
     239.18M      324 rows  10:00 PM
     132.32M      184 rows  9:00 PM
     118.52M      163 rows  12:00 AM
      91.49M      122 rows  MIDNIGHT
      72.60M       96 rows  8:00 PM
      69.46M       91 rows  7:00 PM
      30.87M       41 rows  6:00 PM
      24.62M       32 rows  10:30 PM
      22.40M       32 rows  5:00 PM
      21.47M       29 rows  3:00 AM
      17.76M       23 rows  3:00 PM
      17.68M       23 rows  11:30 PM
      16.21M       22 rows  Midnight
      13.77M       18 rows  9:30 PM
      11.55M       15 rows  4:00 PM
      10.77M       18 rows  24 HOURS
       9.23M       12 rows  N/A

## who x when

BUSINESS_NAME by ISSUED, dollars = GPSX
  Air Ventures, LLC                         2013:0 2014:0 2018:0 2019:0 2022:0 2026:0
  BOSTON HOSPITALITY PARTNERS LLC           2013:2.33M 2023:2.33M
  CHIPOTLE MEXICAN GRILL OF COLORADO, LLC   2013:2.29M 2014:770.8K 2016:1.55M 2020:774.5K 2025:748.3K
  Caffe Nero Americas, Inc.                 2014:774.6K 2015:2.29M 2016:1.55M 2017:2.32M 2018:1.54M 2019:770.2K 2020:770.9K
  Delaware North Boston Flight, LLC         2018:784.4K 2019:2.36M 2020:1.57M
  FISHER COLLEGE                            2014:4.63M
  HSI MCA BOS FB, LLC                       2013:0 2018:0 2019:0
  Make Life Sweeter, LLC                    2013:2.32M 2014:773.3K 2017:768.5K 2018:782.4K
  NORTHEASTERN UNIVERSITY                   2013:4.61M 2014:22.24M
  PINE STREET INN                           2014:6.15M
  SIMMONS COLLEGE                           2014:6.87M
  SODEXO OPERATIONS, LLC                    2013:1.52M 2018:0 2022:0 2023:761.7K 2024:764.2K
  STAR MARKETS COMPANY, INC.                2014:1.54M 2015:2.30M 2019:774.6K
  SWEETGREEN BOSTON, LLC                    2013:1.54M 2015:762.2K 2016:3.09M 2017:2.33M
  Selhi Associates, LLC                     2013:6.17M
  Starbucks Corporation                     2013:9.99M 2014:1.53M 2016:2.33M 2017:772.6K 2018:2.33M 2024:1.54M
  THE WALDWIN GROUP, INC.                   2013:10.03M 2018:767.9K
  TRUSTEES OF BOSTON UNIVERSITY             2013:15.26M 2014:105.35M 2025:1.53M
  Tatte Holdings, LLC                       2014:766.9K 2015:0 2017:764.5K 2018:2.33M 2019:1.54M 2020:1.55M 2021:776.3K 2023:776.8K 2024:771.0K
  WATERMARK DONUT CO.                       2013:4.63M
  WATERMARK DONUT COMPANY                   2013:6.97M
  WENTWORTH INSTITUTE OF TECHNOLOGY         2014:12.24M
  WHOLE FOODS MARKET GROUP, INC.            2013:3.08M 2014:2.32M

DBA_NAME by ISSUED, dollars = GPSX
  Anna's Taqueria                           2015:762.2K 2017:768.9K 2025:1.54M 2026:778.8K
  BOSTON UNIVERSITY                         2013:9.92M 2014:102.30M
  BURGER KING                               2013:6.16M 2014:753.8K
  Caffe Nero                                2015:2.29M 2016:1.55M 2017:2.32M 2018:1.54M 2019:770.2K 2025:771.6K
  DUNKIN DONUTS                             2013:49.23M
  Domino's Pizza                            2013:3.80M 2020:762.7K
  Dunkin Donuts                             2013:2.30M 2014:1.56M 2015:775.4K 2017:1.56M 2018:767.9K 2019:0 2023:0 2025:751.1K
  Dunkin'                                   2022:780.0K 2023:765.3K 2024:776.5K 2025:766.0K 2026:776.0K
  Flour Bakery & Cafe                       2013:1.54M 2014:773.3K 2017:768.5K 2018:782.4K
  Gong Cha                                  2016:768.8K 2021:768.0K 2024:2.31M
  HARVARD BUSINESS SCHOOL                   2014:6.07M
  Legal Sea Foods                           2013:772.3K 2014:774.6K 2017:0 2024:784.4K
  M.I.T                                     2014:16.10M
  McDonald's                                2013:6.90M 2014:1.54M 2024:0
  NORTHEASTERN UNIVERSITY                   2013:1.53M 2014:22.24M
  P. SULLIVAN HOUSING TRUST                 2014:4.63M
  Panera Bread                              2013:1.54M 2014:1.54M 2018:762.6K 2024:762.7K
  SUBWAY                                    2013:3.84M 2014:768.8K
  Sweetgreen                                2013:769.3K 2015:762.2K 2016:2.31M 2017:2.33M 2022:772.8K
  Taco Bell                                 2013:775.6K 2022:778.7K 2024:767.5K 2025:1.53M
  Tatte Bakery & Cafe                       2013:772.2K 2014:766.9K 2015:0 2017:764.5K 2018:2.33M 2019:1.54M 2021:776.3K 2023:776.8K 2024:771.0K
  WENTWORTH INSTITUTE OF TECHNOLOGY         2014:12.24M

## what

LICENSE_CATEGORY: Common Victualler 72%, Misc 23%, Inn 3%, Club 1%, General on Premise 1%

OPENING: 7:00 AM 23%, 11:00 AM 19%, 6:00 AM 16%, 10:00 AM 13%, 8:00 AM 9%, 5:00 AM 7%, 9:00 AM 5%, 11:30 AM 2%, 10:30 AM 2%, 6:30 AM 2%, 4:00 AM 1%

CITY: Boston 51%, Dorchester 10%, East Boston 7%, Roxbury 7%, Allston 5%, Brighton 5%, South Boston 4%, Jamaica Plain 4%, Roslindale 3%, Mission Hill 2%, Charlestown 2%, Hyde Park 2%

STATE: MA 100%, Ma 0%

ZIP: 02215 14%, 02116 11%, 02128 11%, 02115 10%, 02134 8%, 02111 8%, 02210 7%, 02135 7%, 02127 7%, 02118 6%, 02130 6%, 02108 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LICENSE_NUM | id | 3.6K | 0 | LB-107749 19; LB-109265 19; LB-108942 19; LB-107560 19 |
| HISTORICALLICENSENUM | id | 2.2K | 1.4K | CLBALA0002 12; DRMTY0350 12; GOPWML0008 12; SPCMWA0012 12 |
| STATUS | who | 1 | 0 | Active 3.6K |
| LICENSE_CATEGORY | category | 5 | 0 | Common Victualler 2.6K; Misc 828; Inn 102; Club 51 |
| LICENSE_TYPE | who | 56 | 0 | Common Victualler 1.6K; CV7 All Alc. 542; Dormitory 281; Retail All Alc. 233 |
| ISSUED | date | 1.1K | 7 | 2013-11-26 209; 2013-11-25 168; 2014-05-07 167; 2013-11-27 141 |
| EXPIRES | date | 12 | 1 | 2026-12-31 3.0K; 2027-04-30 343; 2025-12-31 176; 2026-04-30 86 |
| BUSINESS_NAME | who | 3.0K | 3 | TRUSTEES OF BOSTON UNIVER 164; NORTHEASTERN UNIVERSITY 41; THE WALDWIN GROUP, INC. 29; Starbucks Corporation 29 |
| DBA_NAME | who | 2.6K | 398 | BOSTON UNIVERSITY 153; DUNKIN DONUTS 81; NORTHEASTERN UNIVERSITY 37; M.I.T 27 |
| COMMENTS | other | 1.2K | 2.2K | Board acknowledges grante 23; Board granted petition to 21; No Conditions 15; Board acknowledged grante 14 |
| LOCATION_COMMENTS | other | 2.8K | 428 | In one room on the first  68; Four story brick building 52; 4 story brick building. 33; In one room on the first  31 |
| OPENING | category | 50 | 2.0K | 7:00 AM 337; 11:00 AM 281; 6:00 AM 233; 10:00 AM 187 |
| CLOSING | who | 74 | 456 | 11:00 PM 731; 2:00 AM 642; 1:00 AM 410; 10:00 PM 324 |
| PATRONSOUT | who | 66 | 807 | 2:30 AM 635; 11:30 PM 506; 1:30 AM 398; 12:30 AM 299 |
| CAPACITY | other | 458 | 0 | 0 988; 19 121; 16 106; 18 104 |
| DESCPREMADD | other | 1.8K | 1.6K | Four story brick building 49; In one room on the first  44; 4 story brick building. 29; Three story brick buildin 17 |
| APPLICANT | who | 3.0K | 0 |  TRUSTEES OF BOSTON UNIVE 152;  NORTHEASTERN UNIVERSITY 30;  Trustees of Boston Unive 29;  STARBUCKS CORPORATION 29 |
| MANAGER | other | 2.9K | 0 | NISHMIN KASHYAP 154;  Robert S. Austin 38;  SEAN SULLIVAN 33; DANIEL BRENNAN JR. 29 |
| DAY_PHONE | other | 1.4K | 2.0K | (206)594-7273 27; (617)353-2148 20; (617)541-1911 14; (617)245-8902 13 |
| EVENING_PHONE | other | 1.3K | 2.0K | (617)353-3502 128; (617)332-0268 25; 6174644001 18; (617)353-2148 17 |
| ADDRESS | other | 3.1K | 0 | 350-  Longwood AV 19; 1585-  Commonwealth AV 19; 27-  Austin ST 19; 830-  Beacon ST 19 |
| CITY | category | 17 | 0 | Boston 1.8K; Dorchester 335; East Boston 259; Roxbury 231 |
| STATE | category | 3 | 2 | MA 3.6K; Ma 4 |
| ZIP | category | 31 | 0 | 02215 319; 02116 267; 02128 260; 02115 245 |
| GPSX | amount | 2.8K | 64 | 0 135; 776492.0000951439 20; 763564.7782462239 19; 774986.2337497175 19 |
| GPSY | amount | 2.8K | 64 | 0 135; 2956600.0001151413 20; 2951931.7971812338 19; 2954996.0577849746 19 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:06:43.48015 3.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | e8e838cd-b5be-4c36-8f71-2 3.6K |
| SRC_SHA256 | who | 1 | 0 | 4e2e020fdf304a34dd8cc8d47 3.6K |
