# PORTAL_CKA_WESTERN_PENNSYLV_D7DA51769C

rows 10.0K  columns 20  scan 4.2s

roles: amount 2, audit 2, category 8, date 2, id 1, other 3, who 3

## when

AS_OF
  2026     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PREV_TAXYR_MKT_VALUE | 10.0K | 0 | 144.8K | 5.75M | 112.21M | 3.86B |
| CUR_MKT_VALUE | 10.0K | 0 | 175.0K | 5.80M | 112.21M | 4.15B |

## who

OWNER_NAME by rows
        57  UNITED STATES STEEL CORPORATION 
        41  RP2ALL LLC 
        38  PLAZA DRIVE L P 
        29  AUX FUNDING LLC 
        26  USX CORPORATION 
        14  RP HOMES 2 LLC 
        14  COMMERCIAL ACQUISITIONS LLC 
        12  SEGAVEPO 2 LLC 
        12  ELMHURST GROUP 
        11  ALJ PENN HILLS LLC 
        11  TNA INVESTMENTS LLC 
        10  QZ FUNDING LLC 
         9  KEYWAY HOMES EAST THREE LLC 
         9  ROBINSON MALL REALTY HOLDINGS LLC 
         9  INFINITY CUSTOM HOMES LP 
         9  MARONDA HOMES LLC 
         9  RP3 FUNDING LLC 
         8  SHADOW VISION PROPERTY LLC 
         8  SFR OWNER LLC 
         8  ELMRIDGE LLC 

OWNER_NAME by dollars
     112.21M        1 rows  WEST PENN ALLEGHENY HEALTH SYSTEM INC 
      84.26M        1 rows  WESTPORT FINDLAY DEVELOPMENT LLC 
      56.04M        1 rows  PARK ASSOCIATES 
      51.96M        2 rows  PZ MIRACLE LIMITED PARTNERSHIP 
      43.61M        1 rows  GRAYBUL ASCENT 430 LLC 
      35.94M        1 rows  GUMBERG STANLEY R & TRUSTEE 
      35.85M        3 rows  CLINTON COMMERCE III LLC 
      35.63M        4 rows  PWC PITT LLC 
      30.76M        3 rows  ALLEGHENY LUDLUM STEEL CORPORATION 
      30.61M        1 rows  EA MOON TOWNSHIP PA LANDLORD LLC 
      30.25M       12 rows  ELMHURST GROUP 
      28.11M       57 rows  UNITED STATES STEEL CORPORATION 
      28.00M        1 rows  4000 OXFORD DRIVE ASSOCIATES LP 
      23.99M        1 rows  TORRENTE APARTMENT OWNER LLC 
      23.36M        2 rows  CONTINENTAL/GALLERIA LP 
      21.85M        3 rows  FRONTIER ASSOCIATES 
      21.75M        6 rows  M & J - BIG WATERFRONT TOWN CENTER I LLC 
      21.43M        2 rows  SETTLERS RIDGE LP 
      20.90M        1 rows  RICHLAND ZAMAGIAS LIMITED PARTNERSHIP 
      19.49M        1 rows  AP COSMOPOLITAN LLC 

MUNICIPALITY by rows
       478  Penn Hills  
       380  McCandless  
       378  Bethel Park  
       369  Upper St. Clair  
       345  Shaler  
       294  West Mifflin  
       272  Ross  
       263  Monroeville  
       262  South Fayette  
       259  Moon  
       233  Franklin Park 
       229  Plum  
       219  Pine  
       210  South Park  
       206  Ohio  
       203  Marshall  
       188  Baldwin Boro  
       185  North Fayette  
       171  Robinson  
       168  Hampton  

MUNICIPALITY by dollars
     291.13M      263 rows  Monroeville  
     265.44M      116 rows  Findlay  
     241.07M      171 rows  Robinson  
     212.31M      259 rows  Moon  
     174.16M      203 rows  Marshall  
     168.07M      369 rows  Upper St. Clair  
     148.83M      378 rows  Bethel Park  
     144.64M      272 rows  Ross  
     144.02M      380 rows  McCandless  
     100.40M      219 rows  Pine  
      94.03M      233 rows  Franklin Park 
      89.55M      165 rows  O''Hara  
      89.19M      185 rows  North Fayette  
      80.27M      206 rows  Ohio  
      79.91M      262 rows  South Fayette  
      72.58M      168 rows  Hampton  
      67.24M       94 rows  Fox Chapel  
      61.93M       68 rows  Mt.Lebanon  
      59.53M      345 rows  Shaler  
      54.31M      478 rows  Penn Hills  

SRC_SHA256 by rows
     10.0K  9bd9c06863ab8da16f188b21a4cb2cd15568ee9358fc0845c13acc3f63f289cb

SRC_SHA256 by dollars
       3.86B    10.0K rows  9bd9c06863ab8da16f188b21a4cb2cd15568ee9358fc0845c13acc3f63f2

## who x when

OWNER_NAME by AS_OF, dollars = PREV_TAXYR_MKT_VALUE
  ALJ PENN HILLS LLC                        2026:711.4K
  ALLEGHENY LUDLUM STEEL CORPORATION        2026:30.76M
  AUX FUNDING LLC                           2026:2.71M
  CLINTON COMMERCE III LLC                  2026:35.85M
  COMMERCIAL ACQUISITIONS LLC               2026:1.31M
  EA MOON TOWNSHIP PA LANDLORD LLC          2026:30.61M
  ELMHURST GROUP                            2026:30.25M
  ELMRIDGE LLC                              2026:1.56M
  GRAYBUL ASCENT 430 LLC                    2026:43.61M
  GUMBERG STANLEY R & TRUSTEE               2026:35.94M
  INFINITY CUSTOM HOMES LP                  2026:3.5K
  KEYWAY HOMES EAST THREE LLC               2026:626.9K
  MARONDA HOMES LLC                         2026:34.6K
  PARK ASSOCIATES                           2026:56.04M
  PLAZA DRIVE L P                           2026:315.4K
  PWC PITT LLC                              2026:35.63M
  PZ MIRACLE LIMITED PARTNERSHIP            2026:51.96M
  QZ FUNDING LLC                            2026:547.6K
  ROBINSON MALL REALTY HOLDINGS LLC         2026:5.08M
  RP HOMES 2 LLC                            2026:1.22M
  RP2ALL LLC                                2026:4.07M
  RP3 FUNDING LLC                           2026:963.1K
  SEGAVEPO 2 LLC                            2026:847.6K
  SFR OWNER LLC                             2026:725.7K
  SHADOW VISION PROPERTY LLC                2026:1.17M
  TNA INVESTMENTS LLC                       2026:323.5K
  UNITED STATES STEEL CORPORATION           2026:28.11M
  USX CORPORATION                           2026:3.15M
  WEST PENN ALLEGHENY HEALTH SYSTEM INC     2026:112.21M
  WESTPORT FINDLAY DEVELOPMENT LLC          2026:84.26M

MUNICIPALITY by AS_OF, dollars = PREV_TAXYR_MKT_VALUE
  Baldwin Boro                              2026:29.73M
  Bethel Park                               2026:148.83M
  Findlay                                   2026:265.44M
  Fox Chapel                                2026:67.24M
  Franklin Park                             2026:94.03M
  Hampton                                   2026:72.58M
  Marshall                                  2026:174.16M
  McCandless                                2026:144.02M
  Monroeville                               2026:291.13M
  Moon                                      2026:212.31M
  Mt.Lebanon                                2026:61.93M
  North Fayette                             2026:89.19M
  O''Hara                                   2026:89.55M
  Ohio                                      2026:80.27M
  Penn Hills                                2026:54.31M
  Pine                                      2026:100.40M
  Plum                                      2026:32.27M
  Robinson                                  2026:241.07M
  Ross                                      2026:144.64M
  Shaler                                    2026:59.53M
  South Fayette                             2026:79.91M
  South Park                                2026:30.26M
  Upper St. Clair                           2026:168.07M
  West Mifflin                              2026:45.91M

## what

CLASS: RESIDENTIAL 90%, COMMERCIAL 8%, INDUSTRIAL 1%, AGRICULTURAL 0%, GOVERNMENT 0%, OTHER 0%, UTILITIES 0%

CLASS_GROUP: Residential 90%, Commercial 10%

TAX_STATUS: TAXABLE 100%, EXEMPT 0%, PURTA 0%

ON_BEHALF_OF: School District 53%, Owner 44%, Municipality 2%, Owner/School 1%, Owner/Muni 0%, Muni/School 0%

HRSTATUS: 04A 90%, WDN 9%, DNA 1%, ABV 0%, 03A 0%

HEARING_STATUS: Full Board approval 90%, Appeal withdrawn 9%, Did Not Appear 1%, At Board of Viewers 0%, Pending Full Board approval 0%

SCHOOL_DISTRICT_CODE: 27 17%, 30 9%, 34 9%, 17 9%, 09 9%, 05 8%, 42 7%, 04 7%, 28 7%, 43 6%, 45 6%, 03 6%

SCHOOL_DISTRICT_NAME: North Allegheny 17%, Penn Hills Twp 9%, Shaler Area 9%, Fox Chapel Area 9%, Woodland Hills 9%, Bethel Park 8%, Upper St Clair 7%, Baldwin Whitehall 7%, North Hills 7%, West Allegheny 6%, West Mifflin Area 6%, Pine-Richland 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TAX_YEAR | other | 1 | 0 | 2023 10.0K |
| PARCEL_ID | id | 10.2K | 0 | 0386N00100000000 50; 0386N00029000000 50; 0386M00014000000 50; 0386M00006000000 50 |
| CLASS | category | 7 | 0 | RESIDENTIAL 9.0K; COMMERCIAL 837; INDUSTRIAL 131; AGRICULTURAL 46 |
| CLASS_GROUP | category | 2 | 0 | Residential 9.0K; Commercial 984 |
| TAX_STATUS | category | 3 | 0 | TAXABLE 10.0K; EXEMPT 36; PURTA 2 |
| HEAR_TYPE | other | 1 | 0 | A 10.0K |
| ON_BEHALF_OF | category | 6 | 0 | School District 5.3K; Owner 4.4K; Municipality 177; Owner/School 69 |
| HRSTATUS | category | 5 | 0 | 04A 9.0K; WDN 886; DNA 134; ABV 26 |
| HEARING_STATUS | category | 5 | 0 | Full Board approval 9.0K; Appeal withdrawn 886; Did Not Appear 134; At Board of Viewers 26 |
| OWNER_NAME | who | 9.0K | 0 | PLAZA DRIVE L P  85; UNITED STATES STEEL CORPO 67; USX CORPORATION  61; TECH ONE ASSOCIATES  52 |
| SCHOOL_DISTRICT_CODE | category | 41 | 0 | 27 836; 30 478; 34 454; 17 452 |
| SCHOOL_DISTRICT_NAME | category | 40 | 0 | North Allegheny 836; Penn Hills Twp 478; Shaler Area 454; Fox Chapel Area 452 |
| MUNI_CODE | other | 136 | 0 | 934 478; 927 380; 876 378; 950 369 |
| MUNICIPALITY | who | 138 | 0 | Penn Hills   478; McCandless   380; Bethel Park   378; Upper St. Clair   369 |
| PREV_TAXYR_MKT_VALUE | amount | 3.8K | 0 | 1000 85; 0 56; 2400 52; 190500 51 |
| CUR_MKT_VALUE | amount | 3.5K | 0 | 1000 71; 139900 70; 159000 68; 108100 63 |
| AS_OF | date | 1 | 0 | 2026-06-26 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:39:25.01733 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0e020a61-9c31-4e73-a0d6-b 10.0K |
| SRC_SHA256 | who | 1 | 0 | 9bd9c06863ab8da16f188b21a 10.0K |
