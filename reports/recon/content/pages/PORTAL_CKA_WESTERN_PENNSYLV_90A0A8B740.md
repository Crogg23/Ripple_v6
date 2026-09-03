# PORTAL_CKA_WESTERN_PENNSYLV_90A0A8B740

rows 10.0K  columns 32  scan 6.0s

roles: amount 7, audit 2, category 8, date 4, id 1, other 7, who 4

## when

HEARING_DATE
  2015      7.8K  ##############################
  2016      2.2K  ########
  2017        26  
  2018         6  
  2019         5  
  2020         1  
  2021         1  
  2022         3  

DISPO_DATE
  2015      7.7K  ##############################
  2016      2.3K  #########
  2017        25  
  2018         8  
  2019         5  
  2021         2  
  2022         3  

AS_OF_DATE
  2026     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PRE_APPEAL_TOTAL | 10.0K | 0 | 126.8K | 3.59M | 222.22M | 3.80B |
| POST_APPEAL_TOTAL | 10.0K | 0 | 148.1K | 3.31M | 154.00M | 3.70B |
| HEARING_CHANGE_AMOUNT | 10.0K | -186.98M | 0 | 311.3K | 11.53M | -103.75M |
| CURRENT_LAND_VALUE | 10.0K | 0 | 32.7K | 759.4K | 28.73M | 775.10M |
| CURRENT_BLDG_VALUE | 10.0K | 0 | 105.8K | 2.14M | 142.57M | 2.77B |
| CURRENT_TOTAL_VALUE | 10.0K | 0 | 145.2K | 2.92M | 147.20M | 3.54B |

## who

MUNI_NAME by rows
       631  14th Ward - PITTSBURGH
       279  19th Ward - PITTSBURGH
       223  Whitehall  
       198  7th Ward - PITTSBURGH
       191  Upper St. Clair  
       190  Baldwin Boro  
       180  Penn Hills  
       179  11th Ward - PITTSBURGH
       178  McCandless  
       159  17th Ward - PITTSBURGH
       159  Moon  
       154  16th Ward - PITTSBURGH
       154  Wilkinsburg  
       153  Pine  
       152  Franklin Park 
       151  10th Ward - PITTSBURGH
       145  Robinson  
       145  Kennedy  
       144  Plum  
       143  Bellevue  

MUNI_NAME by dollars
     498.24M       65 rows  2nd Ward - PITTSBURGH
     228.24M       43 rows  Harrison  
     202.03M      631 rows  14th Ward - PITTSBURGH
     199.62M       50 rows  1st Ward  - PITTSBURGH
     140.54M      107 rows  Monroeville  
     106.19M       76 rows  Ross  
      99.91M      198 rows  7th Ward - PITTSBURGH
      82.99M      145 rows  Robinson  
      77.94M       67 rows  Greentree  
      76.62M      153 rows  Pine  
      64.37M       60 rows  22nd Ward - PITTSBURGH
      63.89M      191 rows  Upper St. Clair  
      60.19M      123 rows  Marshall  
      59.51M      122 rows  4th Ward - PITTSBURGH
      55.99M       97 rows  West Mifflin  
      55.66M      119 rows  Mt.Lebanon  
      53.77M      109 rows  North Fayette  
      50.30M      178 rows  McCandless  
      49.06M      179 rows  11th Ward - PITTSBURGH
      48.38M      279 rows  19th Ward - PITTSBURGH

HEARING_TYPE by rows
     10.0K  ANNUAL

HEARING_TYPE by dollars
       3.80B    10.0K rows  ANNUAL

STATUS by rows
     10.0K  Full BD approve

STATUS by dollars
       3.80B    10.0K rows  Full BD approve

SRC_SHA256 by rows
     10.0K  50f455cf6ed9ae58158a73b4377a1758ad7be8ebb3809f6608a6861072556e60

SRC_SHA256 by dollars
       3.80B    10.0K rows  50f455cf6ed9ae58158a73b4377a1758ad7be8ebb3809f6608a686107255

## who x when

MUNI_NAME by HEARING_DATE, dollars = PRE_APPEAL_TOTAL
  10th Ward - PITTSBURGH                    2015:12.71M 2016:6.11M 2017:133.2K
  11th Ward - PITTSBURGH                    2015:38.40M 2016:10.61M 2017:45.1K
  14th Ward - PITTSBURGH                    2015:144.61M 2016:57.27M 2017:148.1K
  16th Ward - PITTSBURGH                    2015:15.92M 2016:19.26M 2019:1.91M
  17th Ward - PITTSBURGH                    2015:19.09M 2016:10.57M 2017:76.0K
  19th Ward - PITTSBURGH                    2015:39.93M 2016:8.45M
  1st Ward  - PITTSBURGH                    2015:21.75M 2016:177.54M 2017:324.9K
  22nd Ward - PITTSBURGH                    2015:9.77M 2016:54.45M 2017:153.0K
  2nd Ward - PITTSBURGH                     2015:172.81M 2016:315.47M 2017:9.96M
  4th Ward - PITTSBURGH                     2015:22.32M 2016:36.53M 2017:246.8K 2022:408.2K
  7th Ward - PITTSBURGH                     2015:60.76M 2016:38.11M 2017:467.2K 2018:580.9K
  Baldwin Boro                              2015:14.84M 2016:7.96M
  Bellevue                                  2015:11.43M 2016:7.33M
  Franklin Park                             2015:45.18M 2016:740.4K
  Greentree                                 2015:52.24M 2016:25.70M
  Harrison                                  2015:10.67M 2016:217.58M
  Kennedy                                   2015:11.05M 2016:10.51M
  Marshall                                  2015:60.12M 2016:66.2K
  McCandless                                2015:49.94M 2016:362.8K
  Monroeville                               2015:139.56M 2016:971.2K
  Moon                                      2015:34.86M 2016:755.2K
  Penn Hills                                2015:28.04M 2016:32.0K
  Pine                                      2015:75.82M 2016:794.4K
  Plum                                      2015:25.52M 2016:481.9K
  Robinson                                  2015:69.46M 2016:13.53M
  Ross                                      2015:103.16M 2016:3.03M
  Upper St. Clair                           2015:63.89M
  West Mifflin                              2015:54.31M 2016:1.68M
  Whitehall                                 2015:28.17M 2016:3.13M
  Wilkinsburg                               2015:28.88M 2016:10.03M

HEARING_TYPE by HEARING_DATE, dollars = PRE_APPEAL_TOTAL
  ANNUAL                                    2015:2.44B 2016:1.33B 2017:15.11M 2018:5.09M 2019:2.46M 2020:192.9K 2021:3.75M 2022:746.5K

## what

TAX_YEAR: 2015 79%, 2016 21%

CLASS: RESIDENTIAL 87%, COMMERCIAL 11%, INDUSTRIAL 1%, GOVERNMENT 0%, AGRICULTURAL 0%, OTHER 0%, UTILITIES 0%

CLASS_GROUP: Residential 88%, Commercial 12%

TAX_STATUS: TAXABLE 99%, EXEMPT 1%, PURTA 0%

SCHOOL_CODE: 47 54%, 27 7%, 4 7%, 24 5%, 17 5%, 3 4%, 7 4%, 9 3%, 22 3%, 29 3%, 8 3%, 42 3%

SCHOOL_DISTRICT: Pittsburgh 54%, North Allegheny 7%, Baldwin Whitehall 7%, Montour 5%, Fox Chapel Area 5%, Pine-Richland 4%, Carlynton 4%, Woodland Hills 3%, Keystone Oaks 3%, Northgate 3%, Chartiers Valley 3%, Upper St Clair 3%

COMPLAINANT: Owner 49%, School District 36%, Municipality 14%, Owner/School 0%, Owner/Muni 0%, O/M/S 0%, Muni/School 0%

LAST_UPDATE_REASON: HF:BPAAR - HEARING FORMAL 73%, C1:COURT STIPULATION 25%, X2:ACT 202 1%, EC:ERROR CORRECTION 0%, HR:BPAAR - HEARING RESCIND 0%, X3:HOMESTEAD/FARMSTEAD 0%, A4:ADMINISTRATIVE CHANGE 0%, X7:LERTA 0%, B2:BUILDING PERMIT CHANGE 0%, PE:PARTIAL EXEMPT 0%, X4:HOMESTEAD DELETE 0%, N1:PLAN - COMBINATION 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PARCEL_ID | id | 9.8K | 0 | 0189S00120000000 50; 0189S00091000000 50; 0189S00032000000 50; 0189R00144000000 50 |
| TAX_YEAR | category | 2 | 0 | 2015 7.9K; 2016 2.1K |
| CLASS | category | 7 | 0 | RESIDENTIAL 8.7K; COMMERCIAL 1.1K; INDUSTRIAL 97; GOVERNMENT 26 |
| CLASS_GROUP | category | 2 | 0 | Residential 8.8K; Commercial 1.2K |
| TAX_STATUS | category | 3 | 0 | TAXABLE 9.9K; EXEMPT 80; PURTA 2 |
| MUNI_CODE | other | 174 | 0 | 114 631; 119 279; 874 223; 107 198 |
| MUNI_NAME | who | 174 | 0 | 14th Ward - PITTSBURGH 631; 19th Ward - PITTSBURGH 279; Whitehall   223; 7th Ward - PITTSBURGH 198 |
| SCHOOL_CODE | category | 43 | 0 | 47 3.6K; 27 462; 4 451; 24 364 |
| SCHOOL_DISTRICT | category | 42 | 0 | Pittsburgh 3.6K; North Allegheny 462; Baldwin Whitehall 451; Montour 364 |
| HEARING_TYPE | who | 1 | 0 | ANNUAL 10.0K |
| COMPLAINANT | category | 7 | 0 | Owner 4.9K; School District 3.6K; Municipality 1.4K; Owner/School 32 |
| HEARING_STATUS | other | 1 | 0 | 04A 10.0K |
| STATUS | who | 1 | 0 | Full BD approve 10.0K |
| PRE_APPEAL_LAND | other | 1.8K | 0 | 0 378; 35200 73; 26200 71; 20100 68 |
| PRE_APPEAL_BLDG | other | 3.5K | 0 | 0 727; 54500 48; 69300 48; 82000 48 |
| PRE_APPEAL_TOTAL | amount | 4.1K | 0 | 118200 51; 87400 51; 102000 51; 96500 51 |
| POST_APPEAL_LAND | other | 1.8K | 0 | 0 379; 20000 107; 40000 86; 10000 77 |
| POST_APPEAL_BLDG | other | 3.8K | 0 | 0 744; 37100 49; 108000 48; 54500 48 |
| POST_APPEAL_TOTAL | amount | 3.7K | 0 | 96600 54; 115000 53; 78200 52; 13800 52 |
| HEARING_CHANGE_AMOUNT | amount | 2.5K | 0 | 0 4.1K; 31800 31; 37400 31; 2300 31 |
| LAST_UPDATE_REASON | category | 12 | 0 | HF:BPAAR - HEARING FORMAL 7.3K; C1:COURT STIPULATION 2.5K; X2:ACT 202 125; EC:ERROR CORRECTION 8 |
| CURRENT_LAND_VALUE | amount | 1.8K | 0 | 0 381; 20000 109; 10000 83; 40000 82 |
| CURRENT_BLDG_VALUE | amount | 3.8K | 0 | 0 751; 4701 50; 108000 48; 59900 48 |
| CURRENT_TOTAL_VALUE | amount | 3.3K | 0 | 30000 70; 25000 63; 10000 62; 40000 58 |
| CURRENT_VALUE_VS_PRE_APPEAL | amount | 3.0K | 0 | 0 2.3K; 2300 40; 10700 40; -24300 40 |
| HEARING_DATE | date | 151 | 0 | 16-Jun-15 277; 30-Jun-15 236; 15-May-15 215; 23-Jun-15 206 |
| DISPO_DATE | date | 53 | 0 | 2-Oct-15 805; 4-Sep-15 700; 26-Jun-15 623; 7-Aug-15 601 |
| ELAPSED_DAYS | other | 166 | 0 | 24 296; 25 250; 53 213; 37 209 |
| AS_OF_DATE | date | 1 | 0 | 2026-01-06 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:54:06.53129 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1f2fe7da-1804-4aa9-8c48-0 10.0K |
| SRC_SHA256 | who | 1 | 0 | 50f455cf6ed9ae58158a73b43 10.0K |
