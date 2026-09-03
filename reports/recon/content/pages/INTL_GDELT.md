# INTL_GDELT

rows 1.0K  columns 64  scan 4.3s

roles: amount 7, audit 2, category 27, date 1, empty 5, id 1, other 13, who 8

## when

SQLDATE
  2025        10  
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACTIONGEO_FULLNAME | 1.0K | -17.11 | -0.54 | 6.69 | 8.44 | -1.3K |
| EXTRA_COL_0 | 900 | -42.87 | 35.77 | 60 | 61.39 | 29.4K |
| EXTRA_COL_1 | 900 | -157.53 | -71.80 | 146.82 | 149.22 | -25.6K |
| EXTRA_COL_8 | 735 | -42.87 | 36.17 | 60 | 61.39 | 23.9K |
| EXTRA_COL_9 | 735 | -157.53 | -71.53 | 147.38 | 149.22 | -18.6K |
| EXTRA_COL_16 | 1.0K | -42.87 | 36.09 | 55.95 | 61.39 | 32.9K |

## who

ACTOR1NAME by rows
       170  UNITED STATES
        30  NIGERIA
        26  PRESIDENT
        23  UNITED KINGDOM
        22  ISRAEL
        22  POLICE
        21  CANADA
        21  CHINESE
        16  ADMINISTRATION
        12  AUSTRALIA
        12  COMMUNITY
        11  RESIDENTS
        11  VOTER
        11  SCHOOL
        11  GOVERNMENT
        10  AMERICAN
         9  LEBANON
         9  CHINA
         8  PHILIPPINE
         8  HOSPITAL

ACTOR1NAME by dollars
       53.52        8 rows  PHILIPPINE
       40.22       30 rows  NIGERIA
       36.17        8 rows  TELEVISION
       35.75       12 rows  COMMUNITY
       25.72       11 rows  RESIDENTS
       14.22        3 rows  SCOTLAND
       13.33        2 rows  INDUSTRY
       13.24       11 rows  SCHOOL
       10.74        3 rows  KINGSTON
       10.52        2 rows  MOROCCAN
       10.02        6 rows  TANKER
        9.72        2 rows  TEXAS
        9.27        3 rows  THE US
        9.26        2 rows  CHRISTIAN
        8.90        2 rows  ATLANTA
        8.84        4 rows  GOVERNANCE
        7.94        1 rows  AIRLINE
           7        1 rows  HONDURAN
        6.73        5 rows  SPAIN
        6.72        2 rows  SPANISH

EXTRA_COL_12 by rows
        32  Beijing, Beijing, China
        22  United States
        22  Washington, District of Columbia, United States
        18  New Haven, Connecticut, United States
        17  Damascus, Dimashq, Syria
        17  Abuja, Abuja Federal Capital Territory, Nigeria
        15  Worcester, Massachusetts, United States
        15  Santa Clarita, California, United States
        14  United Kingdom
        14  Nigeria
        14  Florida, United States
        13  Australia
        13  Hawaii, United States
        12  New York, United States
        12  Gaza, Israel (general), Israel
        12  Lebanon
        11  Israel
        11  Cloudcroft, New Mexico, United States
        11  Wirral, Wirral, United Kingdom
        11  Melbourne, Victoria, Australia

EXTRA_COL_12 by dollars
       68.70       15 rows  Santa Clarita, California, United States
       59.11       10 rows  Ottawa, Ontario, Canada
       51.31       14 rows  United Kingdom
       33.99       11 rows  Cloudcroft, New Mexico, United States
          32        5 rows  Long Beach, California, United States
       28.76        4 rows  Ebbetts Pass, California, United States
       26.64        6 rows  Middle Belt, Nigeria (general), Nigeria
       25.53       22 rows  United States
       23.62        6 rows  Toronto, Ontario, Canada
       22.27       17 rows  Damascus, Dimashq, Syria
       17.94        6 rows  Kwara, Zamfara, Nigeria
       17.92        7 rows  Texas, United States
       17.64        3 rows  Idlewild, Michigan, United States
       15.86        4 rows  Minnesota, United States
       15.28        8 rows  Roberts Bank, British Columbia, Canada
       14.82        8 rows  Tinubu, Lagos, Nigeria
       14.46        5 rows  Paris, France (general), France
       13.38        2 rows  Philippine, Benguet, Philippines
       13.32        3 rows  Plateau State, Plateau, Nigeria
       13.29        4 rows  Indiana, United States

ACTIONGEO_LAT by rows
        25  Beijing, Beijing, China
        25  Washington, District of Columbia, United States
        25  United States
        21  Abuja, Abuja Federal Capital Territory, Nigeria
        17  New York, United States
        16  New Haven, Connecticut, United States
        14  Florida, United States
        14  Worcester, Massachusetts, United States
        13  United Kingdom
        13  Nigeria
        13  Israel
        13  Beirut, Beyrouth, Lebanon
        12  Gaza, Israel (general), Israel
        11  Lebanon
        11  Australia
        11  Hawaii, United States
        11  Santa Clarita, California, United States
        10  Melbourne, Victoria, Australia
        10  Arizona, United States
         9  Tel Aviv, Tel Aviv, Israel

ACTIONGEO_LAT by dollars
       50.38       11 rows  Santa Clarita, California, United States
       40.14        6 rows  Philippine, Benguet, Philippines
       37.44       25 rows  United States
          32        5 rows  Long Beach, California, United States
       28.76        4 rows  Ebbetts Pass, California, United States
       26.76        4 rows  Ottawa, Ontario, Canada
       26.64        6 rows  Middle Belt, Nigeria (general), Nigeria
       23.96       13 rows  United Kingdom
       21.63        7 rows  Cloudcroft, New Mexico, United States
       19.51        7 rows  Canada
       17.94        6 rows  Kwara, Zamfara, Nigeria
       17.03       13 rows  Beirut, Beyrouth, Lebanon
       14.82        8 rows  Tinubu, Lagos, Nigeria
       13.32        3 rows  Plateau State, Plateau, Nigeria
       13.29        4 rows  Indiana, United States
       13.22        3 rows  Minnesota, United States
       13.03       13 rows  Israel
       12.84        3 rows  Poinciana Elementary School, Florida, United States
       12.74        8 rows  Canberra, Australian Capital Territory, Australia
       12.11        7 rows  Hollywood, California, United States

EXTRA_COL_4 by rows
        23  Beijing, Beijing, China
        22  United States
        20  Washington, District of Columbia, United States
        16  Abuja, Abuja Federal Capital Territory, Nigeria
        14  Beirut, Beyrouth, Lebanon
        14  Damascus, Dimashq, Syria
        11  United Kingdom
        11  Santa Clarita, California, United States
        11  New York, United States
        11  Australia
        11  Worcester, Massachusetts, United States
        10  Gaza, Israel (general), Israel
         9  New Haven, Connecticut, United States
         9  Florida, United States
         9  London, London, City of, United Kingdom
         8  Fujian, Taoyuan Xian, Taiwan
         8  Maine, United States
         8  Nigeria
         7  Illinois, United States
         7  Louisiana, United States

EXTRA_COL_4 by dollars
       50.38       11 rows  Santa Clarita, California, United States
       42.94       22 rows  United States
       40.14        6 rows  Ottawa, Ontario, Canada
       26.76        4 rows  Philippine, Benguet, Philippines
       25.60        4 rows  Long Beach, California, United States
       21.63        7 rows  Cloudcroft, New Mexico, United States
       20.82        6 rows  California, United States
       20.75        5 rows  Toronto, Ontario, Canada
       19.51        7 rows  Canada
       18.34       14 rows  Beirut, Beyrouth, Lebanon
       18.34       14 rows  Damascus, Dimashq, Syria
       17.64        3 rows  Idlewild, Michigan, United States
       16.21       11 rows  United Kingdom
       14.95        5 rows  Kwara, Zamfara, Nigeria
       14.38        2 rows  Ebbetts Pass, California, United States
       13.89        3 rows  Berkshire County, Massachusetts, United States
       13.32        3 rows  Plateau State, Plateau, Nigeria
       13.32        3 rows  Middle Belt, Nigeria (general), Nigeria
       12.99        7 rows  Tinubu, Lagos, Nigeria
       11.66        6 rows  Hollywood, California, United States

## who x when

ACTOR1NAME by SQLDATE, dollars = ACTIONGEO_FULLNAME
  ADMINISTRATION                            2026:-16.97
  AMERICAN                                  2026:-6.18
  ATLANTA                                   2026:8.90
  AUSTRALIA                                 2026:-3.29
  CANADA                                    2026:3.36
  CHINA                                     2026:-13.83
  CHINESE                                   2026:-23.71
  CHRISTIAN                                 2026:9.26
  COMMUNITY                                 2026:35.75
  GOVERNMENT                                2026:-9.33
  HOSPITAL                                  2026:-8.18
  INDUSTRY                                  2026:13.33
  ISRAEL                                    2026:3.83
  KINGSTON                                  2026:10.74
  LEBANON                                   2026:-38.86
  MOROCCAN                                  2026:10.52
  NIGERIA                                   2026:40.22
  PHILIPPINE                                2026:53.52
  POLICE                                    2026:-148.42
  PRESIDENT                                 2026:-3.48
  RESIDENTS                                 2026:25.72
  SCHOOL                                    2026:13.24
  SCOTLAND                                  2026:14.22
  TANKER                                    2026:10.02
  TELEVISION                                2026:36.17
  TEXAS                                     2026:9.72
  THE US                                    2026:9.27
  UNITED KINGDOM                            2025:-11.70 2026:-69.74
  UNITED STATES                             2025:0.55 2026:-202.63
  VOTER                                     2026:2.78

EXTRA_COL_12 by SQLDATE, dollars = ACTIONGEO_FULLNAME
  Abuja, Abuja Federal Capital Territory,   2026:-25.06
  Australia                                 2026:-38.44
  Beijing, Beijing, China                   2026:-34.42
  Cloudcroft, New Mexico, United States     2026:33.99
  Damascus, Dimashq, Syria                  2026:22.27
  Ebbetts Pass, California, United States   2026:28.76
  Florida, United States                    2026:-12.29
  Gaza, Israel (general), Israel            2026:2.40
  Hawaii, United States                     2025:0.55 2026:6.60
  Idlewild, Michigan, United States         2026:17.64
  Israel                                    2026:9.81
  Kwara, Zamfara, Nigeria                   2026:17.94
  Lebanon                                   2026:-79.04
  Long Beach, California, United States     2026:32
  Melbourne, Victoria, Australia            2026:-60.25
  Middle Belt, Nigeria (general), Nigeria   2026:26.64
  Minnesota, United States                  2026:15.86
  New Haven, Connecticut, United States     2026:3.96
  New York, United States                   2026:-61.66
  Nigeria                                   2026:-2.16
  Ottawa, Ontario, Canada                   2026:59.11
  Roberts Bank, British Columbia, Canada    2026:15.28
  Santa Clarita, California, United States  2026:68.70
  Texas, United States                      2026:17.92
  Toronto, Ontario, Canada                  2026:23.62
  United Kingdom                            2026:51.31
  United States                             2026:25.53
  Washington, District of Columbia, United  2025:0.55 2026:-44.28
  Wirral, Wirral, United Kingdom            2026:-64.35
  Worcester, Massachusetts, United States   2026:-89.10

## what

MONTHYEAR: 202607 98%, 202606 1%, 202507 1%

YEAR: 2026 99%, 2025 1%

FRACTIONDATE: 2026.4986 98%, 2025.4986 1%, 2026.4795 1%, 2026.4164 0%

ACTOR1COUNTRYCODE: USA 53%, NGA 9%, CHN 7%, GBR 6%, CAN 6%, ISR 6%, AUS 4%, TUR 2%, SYR 2%, LBN 2%, ESP 2%

ACTOR2CODE: haw 67%, lam 33%

ACTOR2NAME: CHR 50%, MOS 25%, HIN 25%

ACTOR2TYPE1CODE: GOV 34%, CVL 17%, COP 11%, EDU 7%, BUS 7%, MED 5%, LEG 4%, JUD 4%, MIL 4%, HLH 3%, ELI 3%

ISROOTEVENT: BUS 23%, MIL 15%, CVL 15%, MED 15%, GOV 15%, HRI 8%, ENV 8%

QUADCLASS: USA 59%, CAN 7%, GBR 6%, LBN 5%, NGA 5%, SYR 4%, ISR 4%, CHN 3%, IRQ 3%, PSE 2%, AUS 2%

GOLDSTEINSCALE: WAS 100%

NUMMENTIONS: haw 62%, idg 38%

NUMSOURCES: MOS 40%, JEW 40%, HIN 20%

AVGTONE: GOV 27%, CVL 21%, EDU 15%, MED 8%, COP 7%, LEG 6%, BUS 5%, ELI 3%, MIL 3%, OPP 3%, HLH 2%

ACTOR1GEO_TYPE: MED 37%, BUS 26%, GOV 11%, EDU 11%, CRM 5%, HLH 5%, ENV 5%

ACTOR1GEO_COUNTRYCODE: 1 54%, 0 46%

ACTOR2GEO_TYPE: 04 28%, 01 15%, 05 11%, 19 8%, 02 7%, 11 7%, 03 6%, 17 6%, 08 4%, 12 3%, 07 2%, 06 2%

ACTOR2GEO_FULLNAME: 1 62%, 4 15%, 3 13%, 2 10%

ACTOR2GEO_COUNTRYCODE: 0.0 13%, 1.9 11%, -2.0 10%, 3.4 9%, 1.0 9%, 2.8 9%, -10.0 9%, -5.0 9%, 4.0 7%, 7.0 6%, 3.0 6%, -4.0 3%

ACTOR2GEO_LAT: 2 25%, 1 18%, 4 15%, 6 11%, 10 10%, 3 8%, 5 6%, 8 5%, 7 1%, 12 1%, 40 1%, 30 0%

ACTOR2GEO_LONG: 1 97%, 2 2%, 3 1%

ACTIONGEO_TYPE: 2 25%, 1 18%, 4 16%, 10 11%, 6 10%, 3 8%, 5 6%, 8 4%, 7 1%, 40 0%, 12 0%, 30 0%

ACTIONGEO_COUNTRYCODE: 4 33%, 3 25%, 2 15%, 1 15%, 0 11%, 5 1%

ACTIONGEO_LONG: US 55%, NI 9%, CA 8%, UK 6%, IS 5%, AS 4%, CH 3%, LE 3%, TW 3%, IN 2%, RP 2%

EXTRA_COL_3: 0 28%, 4 27%, 3 20%, 1 13%, 2 12%, 5 1%

EXTRA_COL_5: US 56%, NI 8%, CA 8%, UK 5%, AS 4%, IS 4%, CH 4%, LE 3%, TW 3%, IN 2%, SY 2%

EXTRA_COL_11: 4 37%, 3 29%, 1 16%, 2 16%, 5 1%, 0 1%

EXTRA_COL_13: US 54%, CA 9%, NI 8%, UK 5%, IS 4%, CH 4%, AS 4%, IN 3%, LE 2%, TW 2%, SY 2%, RP 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GLOBALEVENTID | id | 1.0K | 0 | 1311830296 6; 1311830295 6; 1311830294 6; 1311830293 6 |
| SQLDATE | date | 4 | 0 | 20260702 994; 20250702 10; 20260625 8; 20260602 3 |
| MONTHYEAR | category | 3 | 0 | 202607 994; 202606 11; 202507 10 |
| YEAR | category | 2 | 0 | 2026 1.0K; 2025 10 |
| FRACTIONDATE | category | 4 | 0 | 2026.4986 994; 2025.4986 10; 2026.4795 8; 2026.4164 3 |
| ACTOR1CODE | other | 117 | 108 | USA 187; GOV 96; CVL 58; COP 33 |
| ACTOR1NAME | who | 221 | 108 | UNITED STATES 170; NIGERIA 30; PRESIDENT 26; UNITED KINGDOM 23 |
| ACTOR1COUNTRYCODE | category | 41 | 458 | USA 244; NGA 42; CHN 34; GBR 30 |
| ACTOR1TYPE1CODE | empty | 1 | 1.0K |  |
| ACTOR2CODE | category | 3 | 1.0K | haw 2; lam 1 |
| ACTOR2NAME | category | 4 | 1.0K | CHR 4; MOS 2; HIN 2 |
| ACTOR2COUNTRYCODE | empty | 1 | 1.0K |  |
| ACTOR2TYPE1CODE | category | 20 | 556 | GOV 144; CVL 74; COP 48; EDU 31 |
| ISROOTEVENT | category | 8 | 1.0K | BUS 3; MIL 2; CVL 2; MED 2 |
| EVENTCODE | empty | 1 | 1.0K |  |
| EVENTBASECODE | other | 109 | 277 | USA 149; GOV 61; CVL 57; EDU 44 |
| EVENTROOTCODE | who | 203 | 277 | UNITED STATES 120; RESIDENTS 21; CANADA 20; SCHOOL 19 |
| QUADCLASS | category | 46 | 591 | USA 193; CAN 22; GBR 19; LBN 16 |
| GOLDSTEINSCALE | category | 2 | 1.0K | WAS 3 |
| NUMMENTIONS | category | 3 | 1.0K | haw 5; idg 3 |
| NUMSOURCES | category | 4 | 1.0K | MOS 2; JEW 2; HIN 1 |
| NUMARTICLES | empty | 1 | 1.0K |  |
| AVGTONE | category | 21 | 627 | GOV 95; CVL 72; EDU 52; MED 27 |
| ACTOR1GEO_TYPE | category | 8 | 996 | MED 7; BUS 5; GOV 2; EDU 2 |
| ACTOR1GEO_FULLNAME | empty | 1 | 1.0K |  |
| ACTOR1GEO_COUNTRYCODE | category | 2 | 0 | 1 549; 0 466 |
| ACTOR1GEO_LAT | other | 76 | 0 | 042 90; 010 81; 051 78; 040 77 |
| ACTOR1GEO_LONG | other | 66 | 0 | 042 90; 010 81; 051 78; 040 77 |
| ACTOR2GEO_TYPE | category | 19 | 0 | 04 261; 01 145; 05 101; 19 72 |
| ACTOR2GEO_FULLNAME | category | 4 | 0 | 1 632; 4 153; 3 130; 2 100 |
| ACTOR2GEO_COUNTRYCODE | category | 33 | 0 | 0.0 108; 1.9 90; -2.0 82; 3.4 80 |
| ACTOR2GEO_LAT | category | 19 | 0 | 2 245; 1 180; 4 150; 6 107 |
| ACTOR2GEO_LONG | category | 3 | 0 | 1 980; 2 21; 3 14 |
| ACTIONGEO_TYPE | category | 18 | 0 | 2 247; 1 180; 4 158; 10 107 |
| ACTIONGEO_FULLNAME | amount | 203 | 0 | -1.40127388535032 41; 0 35; 1.31147540983607 29; 0.55493895671476 28 |
| ACTIONGEO_COUNTRYCODE | category | 6 | 0 | 4 331; 3 251; 2 154; 1 154 |
| ACTIONGEO_LAT | who | 232 | 115 | Washington, District of C 25; United States 25; Beijing, Beijing, China 25; Abuja, Abuja Federal Capi 21 |
| ACTIONGEO_LONG | category | 46 | 115 | US 430; NI 69; CA 63; UK 45 |
| DATEADDED | other | 135 | 115 | USMA 44; USDC 43; USCA 33; USFL 26 |
| SOURCEURL | other | 133 | 436 | DC001 38; MA027 26; CA037 25; 13001 25 |
| EXTRA_COL_0 | amount | 218 | 115 | 38.8951 30; 39.828175 25; 39.9289 25; 9.08333 21 |
| EXTRA_COL_1 | amount | 223 | 115 | -77.0364 30; -98.5795 25; 116.388 25; 7.53333 21 |
| EXTRA_COL_2 | other | 226 | 115 | 531871 30; US 25; -1898541 25; -1997013 21 |
| EXTRA_COL_3 | category | 6 | 0 | 0 280; 4 277; 3 203; 1 130 |
| EXTRA_COL_4 | who | 216 | 280 | Beijing, Beijing, China 23; United States 22; Washington, District of C 20; Abuja, Abuja Federal Capi 16 |
| EXTRA_COL_5 | category | 41 | 280 | US 342; NI 51; CA 49; UK 30 |
| EXTRA_COL_6 | other | 129 | 280 | USDC 38; USCA 32; USMA 30; CH22 23 |
| EXTRA_COL_7 | other | 94 | 648 | 13001 23; DC001 20; 191147 17; 26324 14 |
| EXTRA_COL_8 | amount | 201 | 280 | 38.8951 26; 39.9289 23; 39.828175 22; 9.08333 16 |
| EXTRA_COL_9 | amount | 206 | 280 | -77.0364 26; 116.388 23; -98.5795 22; 7.53333 16 |
| EXTRA_COL_10 | other | 210 | 280 | 531871 26; -1898541 23; US 22; -1997013 16 |
| EXTRA_COL_11 | category | 6 | 0 | 4 380; 3 291; 1 165; 2 159 |
| EXTRA_COL_12 | who | 243 | 9 | Beijing, Beijing, China 32; Washington, District of C 22; United States 22; New Haven, Connecticut, U 18 |
| EXTRA_COL_13 | category | 44 | 9 | US 472; CA 78; NI 67; UK 46 |
| EXTRA_COL_14 | other | 139 | 9 | USMA 50; USDC 44; USCA 41; CH22 32 |
| EXTRA_COL_15 | other | 112 | 504 | 13001 32; DC001 22; 154724 22; 191147 20 |
| EXTRA_COL_16 | amount | 225 | 9 | 39.9289 32; 38.8951 27; 39.828175 22; 41.3082 18 |
| EXTRA_COL_17 | amount | 232 | 9 | 116.388 32; -77.0364 27; -98.5795 22; 8 20 |
| EXTRA_COL_18 | other | 236 | 9 | -1898541 32; 531871 27; US 22; 209231 18 |
| EXTRA_COL_19 | who | 1 | 0 | 20260702201500 1.0K |
| EXTRA_COL_20 | who | 202 | 0 | https://www.aei.org/op-ed 41; https://english.aawsat.co 29; https://www.hawaiipublicr 28; http://www.jpost.com/opin 24 |
| _INGESTED_AT | audit | 1 | 0 | 1783023003917290 1.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | a125b3db-fdcd-4ecb-8b5d-9 1.0K |
| _SRC_SHA256 | who | 1 | 0 | 6b8e1c66afb099d1f2e9177fb 1.0K |
