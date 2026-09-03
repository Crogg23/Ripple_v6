# PORTAL_ARC_ATLANTA_DATAATLA_93AA493487

rows 280  columns 34  scan 3.9s

roles: amount 4, audit 2, category 8, date 3, empty 2, other 4, who 12

## when

CREATIONDATE
  2023       280  ##############################

EDITDATE
  2023       280  ##############################

INGESTED_AT
  2026       280  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EMPNUM | 278 | 1 | 7 | 304.38 | 2.6K | 7.6K |
| SALESVOL | 222 | 115.0K | 1.12M | 11.62M | 126.86M | 526.79M |
| LATITUDE | 280 | 33.67 | 33.76 | 33.79 | 33.79 | 9.5K |
| LONGITUDE | 280 | -84.50 | -84.39 | -84.38 | -84.38 | -23.6K |

## who

CONAME by rows
         3  Emory Healthcare
         3  Planned Parenthood
         2  Atlanta Gastroenterology Associates
         2  Georgia Department-Pubc Health
         2  Reliable Health-Rehab at LKWD
         2  CVS Pharmacy
         1  Del Mazo Medical Service
         1  DaVita Southwest Atlanta Home at Home
         1  Grady Health FDN
         1  Aga's the Liver Center
         1  Promised Land Women's Center
         1  National Senior League LLC
         1  Ascensa Health
         1  Richard J Myung
         1  Goals Plastic Surgery
         1  Ridge, Margaret, Siobhan, MD
         1  R & R Support Service
         1  Camille Williams Davis PC
         1  Innovative Health Group Inc
         1  Behavioral Health Link

CONAME by dollars
      101.28        3 rows  Emory Healthcare
      101.27        3 rows  Planned Parenthood
       67.54        2 rows  Atlanta Gastroenterology Associates
       67.50        2 rows  Georgia Department-Pubc Health
       67.45        2 rows  CVS Pharmacy
       67.40        2 rows  Reliable Health-Rehab at LKWD
       33.79        1 rows  DaVita Southwest Atlanta Home at Home
       33.79        1 rows  Optimal Healthcare Solutions
       33.79        1 rows  Alorica at Home
       33.79        1 rows  D.O.T. Physicals Atlanta
       33.79        1 rows  Professional Counseling Center
       33.78        1 rows  PruittHealth
       33.78        1 rows  Pruitt of West Atlanta
       33.78        1 rows  Centerwell Senior Primary Care GA PC
       33.78        1 rows  Abiola Olutayo Ojewole, MD
       33.78        1 rows  DaVita Center Hill Dialysis
       33.78        1 rows  Jan Delroy Johnson, APRN
       33.78        1 rows  Body Perfections
       33.78        1 rows  Benson Home Health Care
       33.78        1 rows  Chiro Onsite LLC

STATE_NAME by rows
       280  Georgia

STATE_NAME by dollars
        9.5K      280 rows  Georgia

SIC_ALL by rows
        42  801101
        26  809907
        17  801104
        14  802101
         7  801104, 806201
         7  806201
         6  801104, 801101
         6  804101
         5  801101, 805905, 807111, 809906
         5  804301
         4  809203, 801104
         4  809921
         3  808201
         3  804922
         2  809907, 801104
         2  801101, 999966
         2  806203
         2  801101, 809907
         2  809927
         2  801101, 801104, 806201

SIC_ALL by dollars
        1.4K       42 rows  801101
      877.58       26 rows  809907
      573.92       17 rows  801104
      472.57       14 rows  802101
      236.39        7 rows  801104, 806201
      236.29        7 rows  806201
      202.55        6 rows  801104, 801101
      202.53        6 rows  804101
      168.76        5 rows  804301
      168.72        5 rows  801101, 805905, 807111, 809906
      134.92        4 rows  809203, 801104
      134.92        4 rows  809921
      101.29        3 rows  804922
      101.28        3 rows  808201
       67.55        2 rows  809203, 999966
       67.54        2 rows  801101, 801104, 806201
       67.54        2 rows  801104, 801101, 806201
       67.53        2 rows  807101
       67.53        2 rows  801105
       67.53        2 rows  805904

NAICS_ALL by rows
        42  62111107
        26  62199921
        17  62149301
        14  62121003
         7  62211003
         7  62149301, 62211003
         6  62149301, 62111107
         6  62131002
         5  62111107, 62151108, 62199918, 62311007
         5  62139103
         4  62149202, 62149301
         4  62199952
         3  62139936
         3  62161001
         2  62199921, 62149301
         2  62149202, 99999005
         2  62331101
         2  62131002, 62199921
         2  62149301, 62111107, 62211003
         2  45611009, 45521903, 45611005, 45611006, 45612001, 45619106, 45942015, 

NAICS_ALL by dollars
        1.4K       42 rows  62111107
      877.58       26 rows  62199921
      573.92       17 rows  62149301
      472.57       14 rows  62121003
      236.39        7 rows  62149301, 62211003
      236.29        7 rows  62211003
      202.55        6 rows  62149301, 62111107
      202.53        6 rows  62131002
      168.76        5 rows  62139103
      168.72        5 rows  62111107, 62151108, 62199918, 62311007
      134.92        4 rows  62149202, 62149301
      134.92        4 rows  62199952
      101.29        3 rows  62139936
      101.28        3 rows  62161001
       67.55        2 rows  62149202, 99999005
       67.54        2 rows  62111107, 62149301, 62211003
       67.54        2 rows  62149301, 62111107, 62211003
       67.53        2 rows  62151106
       67.53        2 rows  62149302
       67.53        2 rows  62331101

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  Abiola Olutayo Ojewole, MD                2023:33.78
  Aga's the Liver Center                    2023:33.77
  Alorica at Home                           2023:33.79
  Ascensa Health                            2023:33.77
  Atlanta Gastroenterology Associates       2023:67.54
  Behavioral Health Link                    2023:33.76
  CVS Pharmacy                              2023:67.45
  Camille Williams Davis PC                 2023:33.77
  Centerwell Senior Primary Care GA PC      2023:33.78
  D.O.T. Physicals Atlanta                  2023:33.79
  DaVita Center Hill Dialysis               2023:33.78
  DaVita Southwest Atlanta Home at Home     2023:33.79
  Del Mazo Medical Service                  2023:33.77
  Emory Healthcare                          2023:101.28
  Georgia Department-Pubc Health            2023:67.50
  Goals Plastic Surgery                     2023:33.76
  Grady Health FDN                          2023:33.76
  Innovative Health Group Inc               2023:33.68
  Jan Delroy Johnson, APRN                  2023:33.78
  National Senior League LLC                2023:33.76
  Optimal Healthcare Solutions              2023:33.79
  Planned Parenthood                        2023:101.27
  Professional Counseling Center            2023:33.79
  Promised Land Women's Center              2023:33.77
  Pruitt of West Atlanta                    2023:33.78
  PruittHealth                              2023:33.78
  R & R Support Service                     2023:33.75
  Reliable Health-Rehab at LKWD             2023:67.40
  Richard J Myung                           2023:33.76
  Ridge, Margaret, Siobhan, MD              2023:33.75

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2023:9.5K

## what

CITY: Atlanta 100%, East Point 0%

ZIP: 30303 38%, 30308 33%, 30318 8%, 30331 7%, 30311 6%, 30310 2%, 30313 2%, 30315 1%, 30301 0%, 30314 0%, 30344 0%, 30326 0%

HQNAME: Emory Healthcare Network 20%, Grady Health System 14%, Emory University Hospital Midt 11%, DaVita Inc 11%, Planned Parenthood Federation  11%, Children's Healthcare of Atlan 9%, Children's Healthcare of Atlan 6%, CVS Pharmacy, Inc 6%, Emory University 6%, WellStar Health System 3%, Test Me DNA 3%

LOC_CONF: Very High 89%, High 10%, Low 1%

PLACETYPE: Independent 82%, Branch 16%, Headquarters 1%

PROFSPEC: General Dentistry 26%, Obstetrics & Gynecology 23%, Pediatrics 8%, Internal Medicine 8%, Dermatology 8%, Nephrology 5%, Gastroenterology 5%, Internal Medicine,Nephrology 5%, Oral Surgery 5%, Internal Medicine,Oncology,Hem 5%, Ophthalmology,Cardiology,Famil 3%

SQFOOTAGE: 2,500 - 4,999 24%, 20,000 - 39,999 17%, 1,500 - 2,499 13%, 10,000 - 19,999 12%, 5,000 - 9,999 11%, 100,000+ 8%, 1 - 1,499 8%, 40,000 - 99,999 8%

DESC: CONAME, Atlanta, Georgia 100%, CONAME, East Point, Georgia 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 280 | 0 | 284 2; 283 2; 282 2; 281 2 |
| CONAME | who | 275 | 0 | Planned Parenthood 3; Emory Healthcare 3; Winship at Emory Universi 2; Whole & Healthy Youth LLC 2 |
| ADDR | who | 71 | 11 | Peachtree St NE 89; Jesse Hill Jr Dr SE 26; Peachtree St NW 11; Donald Lee Hollowell Pkwy 10 |
| CITY | category | 2 | 0 | Atlanta 279; East Point 1 |
| STATE_NAME | who | 1 | 0 | Georgia 280 |
| STATE | other | 1 | 0 | GA 280 |
| ZIP | category | 12 | 0 | 30303 106; 30308 93; 30318 23; 30331 20 |
| ZIP4 | other | 160 | 20 | 2247 20; 3031 9; 1620 8; 2837 5 |
| NAICS | who | 55 | 0 | 62111107 67; 62149301 47; 62199921 34; 62121003 17 |
| NAICS_ALL | who | 130 | 0 | 62111107 42; 62199921 26; 62149301 17; 62121003 14 |
| SIC | who | 55 | 0 | 801101 67; 801104 47; 809907 34; 802101 17 |
| SIC_ALL | who | 131 | 0 | 801101 42; 809907 26; 801104 17; 802101 14 |
| AFFILIATE | empty | 1 | 280 |  |
| BRAND | empty | 1 | 280 |  |
| HQNAME | category | 26 | 231 | Emory Healthcare Network 7; Grady Health System 5; Emory University Hospital 4; DaVita Inc 4 |
| LOC_CONF | category | 3 | 0 | Very High 250; High 27; Low 3 |
| PLACETYPE | category | 3 | 0 | Independent 231; Branch 46; Headquarters 3 |
| PROFSPEC | category | 41 | 212 | General Dentistry 10; Obstetrics & Gynecology 9; Pediatrics 3; Internal Medicine 3 |
| SQFOOTAGE | category | 9 | 42 | 2,500 - 4,999 56; 20,000 - 39,999 41; 1,500 - 2,499 30; 10,000 - 19,999 28 |
| EMPNUM | amount | 43 | 0 | 7.0 46; 5.0 30; 6.0 23; 3.0 22 |
| SALESVOL | amount | 94 | 0 | nan 58; 888000.0 26; 1562000.0 16; 1116000.0 16 |
| SOURCE | who | 1 | 0 | Data Axle 280 |
| ESRI_PID | other | 277 | 0 | 05993a8268514907766cb1691 2; d1475e7cf74e97af1f9a22d76 2; f5d77ff89eba06912ee7e2ae7 2; 43bb46966e7acca5bed7d6b8a 2 |
| DESC | category | 2 | 0 | CONAME, Atlanta, Georgia 279; CONAME, East Point, Georg 1 |
| LATITUDE | amount | 124 | 0 | 33.7689539999208 56; 33.7518450002084 12; 33.7601609999757 10; 33.768566999844 9 |
| LONGITUDE | amount | 126 | 0 | -84.3862860003993 56; -84.3820155002684 12; -84.3864075002364 10; -84.3884054998537 9 |
| CREATIONDATE | date | 1 | 0 | 1703001016019 280 |
| CREATOR | who | 1 | 0 | gpickren2 280 |
| EDITDATE | date | 1 | 0 | 1703001016019 280 |
| EDITOR | who | 1 | 0 | gpickren2 280 |
| GEOMETRY | who | 125 | 0 | {"type": "Point", "coordi 56; {"type": "Point", "coordi 12; {"type": "Point", "coordi 10; {"type": "Point", "coordi 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:21:53.67163 280 |
| SOURCE_RUN_ID | audit | 1 | 0 | 12c189a1-c16f-49ad-a75a-5 280 |
| SRC_SHA256 | who | 1 | 0 | bc7c0d9a52a924802d2f03799 280 |
