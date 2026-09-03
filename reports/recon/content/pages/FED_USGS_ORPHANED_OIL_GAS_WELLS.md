# FED_USGS_ORPHANED_OIL_GAS_WELLS

rows 117.7K  columns 26  scan 6.9s

roles: amount 2, audit 2, category 7, date 1, id 1, other 7, who 6

## when

DATA_FILE_DATE
  2019      3.7K  ##
  2020      5.0K  ##
  2021     39.7K  #################
  2022     69.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 117.7K | 26.11 | 38.95 | 45.60 | 69.54 | 4.53M |
| LONGITUDE | 117.7K | -156.32 | -85.69 | -77.70 | -73.46 | -10.41M |

## who

WELL_NAME by rows
      1.9K  FEE
      1.1K  NO NAME
       558  UNKNOWN
       206  EUREKA COAL & MINERAL CO
       174  Well No.
       148  IDA-FAUVERGUE
       130  SMITH
       116  Fahrner Tract
       112  DRAKE, P Y
       110  BROWN
       108  Tram
       100  Hepler
        97  MILLER
        96  JONES
        95  DICKERSON (ZIMMERMAN)
        92  WILLIAMS
        88  Ulf
        83  EUREKA COAL & MINERALS CO
        80  Collins Pine - Lot 108, ANF
        75  Bell

WELL_NAME by dollars
       73.9K     1.9K rows  FEE
       45.6K     1.1K rows  NO NAME
       21.0K      558 rows  UNKNOWN
        7.8K      206 rows  EUREKA COAL & MINERAL CO
        6.0K      174 rows  Well No.
        5.6K      148 rows  IDA-FAUVERGUE
        4.9K      116 rows  Fahrner Tract
        4.7K      130 rows  SMITH
        4.5K      108 rows  Tram
        4.2K      112 rows  DRAKE, P Y
        4.2K      100 rows  Hepler
        4.0K      110 rows  BROWN
        3.7K       88 rows  Ulf
        3.6K       95 rows  DICKERSON (ZIMMERMAN)
        3.5K       97 rows  MILLER
        3.5K       96 rows  JONES
        3.3K       92 rows  WILLIAMS
        3.3K       80 rows  Collins Pine - Lot 108, ANF
        3.1K       83 rows  EUREKA COAL & MINERALS CO
        3.0K       71 rows  Roy

TYPE by rows
      8.7K  OIL
      5.4K  O
      4.9K  GAS
      4.2K  Oil Well
      3.5K  Not Listed
      2.8K  Oil & Gas
      2.4K  WI
      2.4K  NT
      2.1K  Vertical
      1.9K  Dry Hole
      1.5K  Not Available
      1.3K  Oil Development
      1.3K  DRY
      1.1K  Oil
      1.1K  Gas(Convertional, Commercial)
      1.0K  Stratigraphic Test
      1.0K  NO PRODUCT SPECIFIED
      1.0K  OG
       987  Gas Development
       958  TM

TYPE by dollars
      306.9K     8.7K rows  OIL
      211.1K     5.4K rows  O
      169.3K     4.9K rows  GAS
      146.6K     3.5K rows  Not Listed
      134.1K     4.2K rows  Oil Well
       97.8K     2.8K rows  Oil & Gas
       95.4K     2.4K rows  WI
       87.7K     2.4K rows  NT
       83.4K     2.1K rows  Vertical
       74.4K     1.9K rows  Dry Hole
       56.7K     1.5K rows  Not Available
       54.6K     1.3K rows  Oil Development
       46.6K     1.3K rows  DRY
       46.0K     1.0K rows  OG
       42.4K     1.1K rows  Oil
       42.2K      987 rows  Gas Development
       41.4K     1.0K rows  Stratigraphic Test
       41.4K      934 rows  CBM Well
       41.3K     1.1K rows  Gas(Convertional, Commercial)
       34.6K      958 rows  TM

OTHER_NOTES by rows
      3.6K  Operator Unknown and Unknown with Abandoned well status
      2.8K  Pot. Des. 2018: Yes, Pot. Des. 2019: Yes
       634  Status Date: 1901/01/01
       431  Coordinates: KGS generated using LeoWEB
       410  Pot. Des. 2018: No, Pot. Des. 2019: Yes
        73  Pot. Des. 2018: Yes, Pot. Des. 2019: No
        68  no API found from state
        64  0330N 0330W SEc NE SW
        55  0330N 0330W SEc SW
        53  0330N 0330W SEc NW NW
        52  0330N 0330W SEc NW
        52  0330N 0330W SEc NE NE
        52  0330S 0330E NWc NE NW
        52  0330N 0330W SEc NE
        52  0330S 0330W NEc NW SE
        52  0330S 0330W NEc SE
        52  0330S 0330E NWc
        51  0330N 0330W SEc SW NE
        51  0330S 0330E NWc SW NE
        50  0330N 0330W SEc

OTHER_NOTES by dollars
      140.2K     3.6K rows  Operator Unknown and Unknown with Abandoned well status
       97.6K     2.8K rows  Pot. Des. 2018: Yes, Pot. Des. 2019: Yes
       24.8K      634 rows  Status Date: 1901/01/01
       16.3K      431 rows  Coordinates: KGS generated using LeoWEB
       14.8K      410 rows  Pot. Des. 2018: No, Pot. Des. 2019: Yes
        2.6K       68 rows  no API found from state
        2.5K       73 rows  Pot. Des. 2018: Yes, Pot. Des. 2019: No
        2.5K       64 rows  0330N 0330W SEc NE SW
        2.1K       55 rows  0330N 0330W SEc SW
        2.0K       53 rows  0330N 0330W SEc NW NW
        2.0K       52 rows  0330S 0330W NEc SE
        2.0K       52 rows  0330S 0330E NWc NE NW
        2.0K       52 rows  0330N 0330W SEc NE
        2.0K       52 rows  0330N 0330W SEc NE NE
        2.0K       52 rows  0330S 0330E NWc
        2.0K       52 rows  0330S 0330W NEc NW SE
        2.0K       52 rows  0330N 0330W SEc NW
        2.0K       51 rows  0330N 0330W SEc SW NE
        2.0K       51 rows  0330S 0330E NWc SW NE
        2.0K       50 rows  0330N 0330W SEc

WELL_INFO_NOTES by rows
     12.7K  API and lat/long acquired from KY Geode: KGS Oil and Gas Search tool
      3.7K  Priority 1C Well
      1.4K  Priority 1B Well
       649  Type Date: 1901/01/01
       462  Shut In to be converted to "AB" or "OR" by source
       412  Priority 2 Well
        79  Status date: 08/04/2009
        75  Status date: 03/12/2010
        70  Orphan-No Responsible Operator
        61  Status date: 06/25/2015
        59  Status date: 11/19/2009
        50  Status date: 06/01/2012
        35  Status date: 07/01/2009
        34  Status date: 06/31/2005
        33  Type Date: 1984/12/15
        30  Type Date: 1985/06/15
        28  Status date: 07/01/2012
        24  Type Date: 1985/04/15
        24  Status date: 06/29/2012
        24  Type Date: 1931/06/15

WELL_INFO_NOTES by dollars
      474.5K    12.7K rows  API and lat/long acquired from KY Geode: KGS Oil and Gas Sea
      138.4K     3.7K rows  Priority 1C Well
       51.6K     1.4K rows  Priority 1B Well
       25.3K      649 rows  Type Date: 1901/01/01
       18.8K      462 rows  Shut In to be converted to "AB" or "OR" by source
       15.7K      412 rows  Priority 2 Well
        3.5K       79 rows  Status date: 08/04/2009
        3.3K       75 rows  Status date: 03/12/2010
        2.7K       70 rows  Orphan-No Responsible Operator
        2.7K       61 rows  Status date: 06/25/2015
        2.6K       59 rows  Status date: 11/19/2009
        2.2K       50 rows  Status date: 06/01/2012
        1.6K       35 rows  Status date: 07/01/2009
        1.5K       34 rows  Status date: 06/31/2005
        1.2K       33 rows  Type Date: 1984/12/15
        1.2K       28 rows  Status date: 07/01/2012
        1.1K       30 rows  Type Date: 1985/06/15
        1.1K       24 rows  Status date: 06/29/2012
      932.58       24 rows  Type Date: 1931/06/15
      906.72       24 rows  Type Date: 1985/04/15

## who x when

WELL_NAME by DATA_FILE_DATE, dollars = LATITUDE
  BROWN                                     2020:898.21 2021:2.7K 2022:382.52
  Bell                                      2019:2.5K 2021:35.80 2022:40
  Collins Pine - Lot 108, ANF               2022:3.3K
  DICKERSON (ZIMMERMAN)                     2022:3.6K
  DRAKE, P Y                                2021:4.2K
  EUREKA COAL & MINERAL CO                  2021:7.8K
  EUREKA COAL & MINERALS CO                 2021:3.1K
  FEE                                       2020:72.9K 2021:939.11 2022:128.05
  Fahrner Tract                             2022:4.9K
  Hepler                                    2022:4.2K
  IDA-FAUVERGUE                             2020:5.6K
  JONES                                     2020:816.86 2021:2.5K 2022:139.82
  MILLER                                    2019:39.78 2020:233.99 2021:2.8K 2022:393.03
  NO NAME                                   2022:45.6K
  Roy                                       2022:3.0K
  SMITH                                     2020:504.44 2021:3.4K 2022:860.52
  Tram                                      2022:4.5K
  UNKNOWN                                   2021:19.9K 2022:1.1K
  Ulf                                       2022:3.7K
  WILLIAMS                                  2020:274.13 2021:2.7K 2022:386.52
  Well No.                                  2019:6.0K

TYPE by DATA_FILE_DATE, dollars = LATITUDE
  CBM Well                                  2022:41.4K
  DRY                                       2021:46.6K
  Dry Hole                                  2019:4.6K 2020:62.1K 2021:142.88 2022:7.5K
  GAS                                       2021:111.0K 2022:58.2K
  Gas Development                           2022:42.2K
  Gas(Convertional, Commercial)             2020:41.3K
  NO PRODUCT SPECIFIED                      2022:31.9K
  NT                                        2021:87.7K
  Not Available                             2021:56.7K
  Not Listed                                2022:146.6K
  O                                         2021:3.0K 2022:208.0K
  OG                                        2021:6.6K 2022:39.5K
  OIL                                       2021:254.7K 2022:52.2K
  Oil                                       2020:23.9K 2021:5.8K 2022:12.7K
  Oil & Gas                                 2019:97.8K
  Oil Development                           2022:54.6K
  Oil Well                                  2021:130.3K 2022:3.9K
  Stratigraphic Test                        2020:41.4K
  TM                                        2021:34.6K
  Vertical                                  2021:83.4K
  WI                                        2022:95.4K

## what

STATE: Ohio 18%, Pennsylvania 17%, Oklahoma 14%, Kentucky 11%, Illinois 8%, New York 6%, Texas 5%, Kansas 5%, Missouri 4%, Louisiana 4%, West Virginia 3%, California 3%

STATUS: Orphan 28%, OR 16%, HP 14%, orphan 12%, Abandoned 10%, ACT 404 ORPHAN WELL-ENG 4%, Abandoned Well 3%, UN 3%, Idle 3%, Unknown Located 2%, Unknown 2%, Unknown Not Found 2%

PRIME_MERIDIAN: Indian 59%, 6th 22%, SB 10%, MD 3%, 2 2%, 5th 1%, 6 1%, N 0%, Cimarron 0%, INDIAN 0%, M 0%

T_DIR: N 72%, S 28%

R_DIR: E 60%, W 40%, 3 0%

QTR: NE 13%, NW4  13%, NW 13%, SW 13%, SW4  12%, NE4  12%, SE4  12%, SE 12%, UN 0%, N2 0%, S2 0%, NW4 0%

SOURCE: Ohio Department of Natural Res 18%, Pennsylvania Department of Env 17%, Oklahoma Corporation Commissio 14%, Kentucky Geological Survey 11%, Illinois Department of Natural 8%, New York State Department of E 6%, Railroad Commission of Texas 5%, Kansas Corporation Commission 5%, Missouri Department of Natural 4%, Louisiana Department of Natura 4%, West Virginia Department of En 3%, Geologic Energy Management Div 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| WELL_IDENTIFIER | id | 118.9K | 0 | API:49045601710000 589; API:49045292820000 589; API:49045292750000 589; API:49045226890000 589 |
| STATE | category | 27 | 0 | Ohio 20.6K; Pennsylvania 19.2K; Oklahoma 16.0K; Kentucky 12.7K |
| COUNTY | who | 906 | 467 | Venango 4.9K; Washington 4.0K; McKean 3.4K; Allegany 3.1K |
| WELL_NAME | who | 78.1K | 26 | FEE 2.1K; NO NAME 1.4K; UNKNOWN 648; O NEAL SAN ANDRES UNIT 605 |
| WELL_NUMBER | other | 7.7K | 64.2K | 1 14.6K; 2 5.8K; 3 3.4K; 4 2.4K |
| TYPE | who | 118 | 59.9K | OIL 8.7K; O 5.4K; GAS 4.9K; Oil Well 4.2K |
| STATUS | category | 43 | 5.9K | Orphan 29.7K; OR 16.8K; HP 15.5K; orphan 12.7K |
| LATITUDE | amount | 105.1K | 0 | 39.23744909 672; 38.70635392 611; 38.21670544 594; 39.55107142 592 |
| LONGITUDE | amount | 107.9K | 0 | -80.93934416 672; -81.2817217 611; -81.95212465 594; -80.45773151 592 |
| PRIME_MERIDIAN | category | 11 | 91.0K | Indian 15.8K; 6th 6.0K; SB 2.6K; MD 781 |
| TOWNSHIP | other | 99 | 70.0K | 1 2.7K; 2 2.0K; 28 1.7K; 14 1.7K |
| T_DIR | category | 3 | 70.0K | N 34.3K; S 13.4K |
| RANGE | other | 108 | 70.0K | 13 3.4K; 14 3.4K; 15 2.5K; 10 2.4K |
| R_DIR | category | 3 | 70.0K | E 28.7K; W 18.9K; 3 1 |
| SECTION | other | 101 | 70.1K | 28 1.6K; 19 1.6K; 21 1.6K; 20 1.5K |
| QTR | category | 49 | 94.1K | NE 3.0K; NW4  3.0K; NW 2.9K; SW 2.9K |
| QTR_QTR | other | 77 | 96.0K | NE4  2.6K; NW4  2.6K; SE4  2.6K; SW4  2.5K |
| QTR_QTR_QTR | other | 84 | 100.5K | SW4  2.3K; NW4  2.3K; SE4  2.2K; NE4  2.2K |
| SOURCE | category | 27 | 0 | Ohio Department of Natura 20.6K; Pennsylvania Department o 19.2K; Oklahoma Corporation Comm 16.0K; Kentucky Geological Surve 12.7K |
| DATA_FILE_DATE | date | 27 | 0 | 5/11/2022 20.6K; 5/9/2022 19.2K; 11/19/2021 16.0K; 7/1/2021 12.7K |
| WELL_INFO_NOTES | who | 3.4K | 92.7K | API and lat/long acquired 12.7K; Priority 1C Well 3.7K; Priority 1B Well 1.4K; Type Date: 1901/01/01 649 |
| LOCATION_NOTES | who | 1.3K | 62.2K | Coordinate datum unconfir 7.7K; Coordinates: USGS generat 6.0K; Municipality: Foster Twp. 1.0K; Township: Jackson 952 |
| OTHER_NOTES | who | 7.9K | 96.8K | Operator Unknown and Unkn 3.7K; Pot. Des. 2018: Yes, Pot. 2.8K; Status Date: 1901/01/01 674; Coordinates: KGS generate 471 |
| INGESTED_AT | audit | 1 | 0 | 1786164039385777 117.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 11cdd2eb-9d09-4898-8056-8 117.7K |
| SRC_SHA256 | other | 1 | 0 | 231ba0154dbc2c7a10b7d3ef4 117.7K |
