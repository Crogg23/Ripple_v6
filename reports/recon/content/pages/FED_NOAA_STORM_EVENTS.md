# FED_NOAA_STORM_EVENTS

rows 1.78M  columns 54  scan 6.0s

roles: amount 4, audit 2, category 16, id 1, other 18, state 1, who 12

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MAGNITUDE | 917.5K | 0 | 50 | 74.61 | 22.0K | 30.77M |
| TOR_LENGTH | 42.8K | 0 | 1.28 | 20.91 | 400 | 129.6K |
| BEGIN_RANGE | 881.6K | 0 | 1.50 | 20 | 519.78 | 2.53M |
| END_RANGE | 885.5K | 0 | 1.52 | 20.00 | 519.78 | 2.57M |

## who

CZ_NAME by rows
     14.5K  WASHINGTON
     13.5K  JEFFERSON
     12.4K  JACKSON
     11.6K  FRANKLIN
     11.1K  MONTGOMERY
     10.9K  MADISON
     10.5K  LINCOLN
      8.4K  CLAY
      7.9K  UNION
      7.7K  MARION
      7.5K  MONROE
      7.5K  WAYNE
      7.4K  WARREN
      7.3K  POLK
      6.7K  GREENE
      6.5K  JOHNSON
      6.2K  MARSHALL
      6.1K  CARROLL
      6.0K  GRANT
      6.0K  LAWRENCE

CZ_NAME by dollars
      250.2K    13.5K rows  JEFFERSON
      249.3K    14.5K rows  WASHINGTON
      236.4K    11.6K rows  FRANKLIN
      226.7K    12.4K rows  JACKSON
      218.8K    11.1K rows  MONTGOMERY
      206.5K    10.9K rows  MADISON
      168.5K    10.5K rows  LINCOLN
      151.8K     7.7K rows  MARION
      140.8K     7.4K rows  WARREN
      137.7K     7.5K rows  WAYNE
      137.3K     7.5K rows  MONROE
      134.3K     8.4K rows  CLAY
      124.5K     7.9K rows  UNION
      121.1K     6.7K rows  GREENE
      117.8K     7.3K rows  POLK
      112.3K     6.1K rows  CARROLL
      109.2K     6.0K rows  LAWRENCE
      108.2K     6.2K rows  MARSHALL
      107.4K     6.5K rows  JOHNSON
      106.4K     5.6K rows  SCOTT

TOR_OTHER_CZ_NAME by rows
        56  MADISON
        40  WASHINGTON
        38  JEFFERSON
        32  MARION
        30  FRANKLIN
        30  LINCOLN
        29  JACKSON
        28  SCOTT
        28  NEWTON
        28  WAYNE
        27  MARSHALL
        24  PIKE
        23  MONTGOMERY
        23  POLK
        23  WEBSTER
        22  PERRY
        22  JASPER
        22  HENRY
        21  SHELBY
        21  CALHOUN

TOR_OTHER_CZ_NAME by dollars
           0        1 rows  YALOBUSHA
           0        1 rows  WHITLEY
           0        1 rows  SHACKELFORD
           0        1 rows  SHAWNEE
           0        1 rows  TATTNALL
           0        1 rows  OCHILTREE
           0        1 rows  HANSFORD
           0        1 rows  WAKULLA
           0        1 rows  NEWAYGO
           0        1 rows  EDMONSON
           0        1 rows  WALLACE
           0        1 rows  TELLER
           0        1 rows  ALAMANCE
           0        1 rows  TROUP
           0        2 rows  ST. BERNARD
           0        2 rows  KAY
           0        1 rows  SMYTH
           0        2 rows  ARAPAHOE
           0        1 rows  VOLUSIA
           0        3 rows  SAMPSON

EPISODE_NARRATIVE by rows
       885  An expansive ridge sat over the southern portion of the CONUS. This ri
       412  A cluster of supercells developed during the late afternoon hours, pro
       343  Scattered severe thunderstorms in advance of a cold front produced dam
       337  The middle part of June was unusually stormy across the area. Numerous
       294  A strong upper-level disturbance passed through the region in a northw
       275  A heat dome continued to strengthen and expand across the eastern CONU
       275  A powerful coastal storm developed along the NJ coast then moved|north
       257  Scattered severe thunderstorms in advance of a cold front produced dam
       253  Upper level high pressure built over the Mid-South. High temperatures 
       248  Scattered afternoon thunderstorms developed in an environment favorabl
       241  Upper-level high pressure continued over the region. Hot and humid con
       234  Trees down.
       232  A strong low pressure system moved through central California on Janua
       229  A cluster of thunderstorms that initiated during the night of June 28t
       221  A cold front ushered in an arctic airmass on the evening of January 17
       220  A strong, stationary heat dome brought oppressive heat to the Mid-Sout
       218  The strong upper ridge of high pressure that dominated the weather acr
       216  A severe weather outbreak occurred during the mid to late afternoon ho
       213  Scattered thunderstorms in advance of a cold front produced gusty wind
       209  From the 24th through the 27th, the arrival of a slow-moving cold fron

EPISODE_NARRATIVE by dollars
       26.0K        3 rows  Lightning sparked numerous fire across Humboldt, Trinity, an
       17.9K      412 rows  A cluster of supercells developed during the late afternoon 
       16.8K      294 rows  A strong upper-level disturbance passed through the region i
       13.8K      337 rows  The middle part of June was unusually stormy across the area
       13.5K      343 rows  Scattered severe thunderstorms in advance of a cold front pr
       13.3K      275 rows  A powerful coastal storm developed along the NJ coast then m
       13.1K      229 rows  A cluster of thunderstorms that initiated during the night o
       12.8K      257 rows  Scattered severe thunderstorms in advance of a cold front pr
       11.9K      248 rows  Scattered afternoon thunderstorms developed in an environmen
       11.1K      216 rows  A severe weather outbreak occurred during the mid to late af
       11.1K      193 rows  A very hot and potentially unstable airmass interacted with 
       10.5K      185 rows  A widespread, long-lived thunderstorm line (bow echo) raced 
        9.7K      178 rows  During the late morning through the afternoon of Monday Augu
        9.5K      146 rows  A potent upper level system and surface low approached the r
        9.4K      206 rows  A strong cold front, driven by an unusually strong upper-lev
        9.2K      213 rows  Scattered thunderstorms in advance of a cold front produced 
        9.2K      182 rows  A strong shortwave trough pushed through the Ohio Valley bri
        8.9K      180 rows  A typical summer pattern persisted with scattered thundersto
        8.7K      171 rows  In a 4-6 hour period during the late afternoon and evening h
        7.9K      119 rows  A volatile environment featured a warm front from parts of e

END_LOCATION by rows
     19.7K  COUNTYWIDE
      1.4K  SPRINGFIELD
      1.2K  AMARILLO
      1.1K  LEXINGTON
      1.1K  CLINTON
      1.1K  COLUMBIA
      1.1K  MADISON
      1.0K  MARION
      1.0K  JACKSON
      1.0K  GREENVILLE
       994  KEY WEST
       961  LEBANON
       914  FRANKLIN
       896  BURLINGTON
       875  SALEM
       862  FAIRVIEW
       853  MT VERNON
       830  PLAYALINDA BEACH
       820  BUFFALO
       819  GREENWOOD

END_LOCATION by dollars
      217.7K    19.7K rows  COUNTYWIDE
       32.6K      830 rows  PLAYALINDA BEACH
       31.4K     1.4K rows  SPRINGFIELD
       28.9K     1.1K rows  CLINTON
       28.7K     1.1K rows  LEXINGTON
       25.4K      961 rows  LEBANON
       25.1K     1.1K rows  COLUMBIA
       24.7K     1.0K rows  GREENVILLE
       24.2K     1.0K rows  MARION
       23.5K     1.1K rows  MADISON
       22.9K      875 rows  SALEM
       22.2K      994 rows  KEY WEST
       22.0K        3 rows  WEOTT
       21.7K      557 rows  CAPE CANAVERAL
       21.3K      862 rows  FAIRVIEW
       21.1K      896 rows  BURLINGTON
       20.4K      735 rows  NASHVILLE
       20.3K      914 rows  FRANKLIN
       20.3K     1.0K rows  JACKSON
       19.9K      776 rows  WASHINGTON

## where

TOR_OTHER_CZ_STATE: MS 365, AL 346, GA 241, OK 241, IL 209, AR 203, TX 190, TN 184, IA 182, MO 181, KS 160

## what

BEGIN_DAY: 1 19%, 10 8%, 9 8%, 8 7%, 24 7%, 16 7%, 13 7%, 22 7%, 15 7%, 19 7%, 21 7%, 26 7%

END_DAY: 31 12%, 30 11%, 10 8%, 9 8%, 16 8%, 24 8%, 28 8%, 7 8%, 13 8%, 15 8%, 22 8%, 26 8%

YEAR: 2011 10%, 2023 9%, 2025 9%, 2008 9%, 2022 9%, 2024 9%, 2019 8%, 2012 8%, 2010 8%, 2018 8%, 2021 8%, 2020 7%

MONTH_NAME: June 14%, July 13%, May 12%, August 9%, April 9%, January 8%, February 8%, March 7%, December 7%, September 5%, November 4%, October 4%

CZ_TYPE: C 59%, Z 40%, M 0%

CZ_TIMEZONE: CST-6 33%, EST-5 24%, CST 15%, EST 11%, MST-7 8%, PST-8 3%, MST 3%, PST 1%, HST-10 1%, AST 0%, AKST-9 0%, AST-4 0%

DEATHS_DIRECT: 0 99%, 1 0%, 2 0%, 3 0%, 4 0%, 5 0%, 6 0%, 8 0%, 7 0%, 9 0%, 10 0%, 11 0%

DEATHS_INDIRECT: 0 100%, 1 0%, 2 0%, 3 0%, 4 0%, 5 0%, 6 0%, 8 0%, 7 0%, 10 0%, 9 0%, 11 0%

MAGNITUDE_TYPE: EG 66%, MG 26%, E 4%, MS 2%, M 2%, ES 1%

FLOOD_CAUSE: Heavy Rain 91%, Heavy Rain / Snow Melt 5%, Heavy Rain / Tropical System 3%, Heavy Rain / Burn Area 1%, Ice Jam 1%, Dam / Levee Break 0%, Planned Dam Release 0%

CATEGORY: 1 71%, 2 13%, 4 8%, 3 6%, 5 2%

TOR_F_SCALE: EF0 30%, EF1 23%, F0 22%, F1 9%, EF2 6%, EFU 4%, F2 3%, EF3 2%, F3 1%, EF4 0%, F4 0%

BEGIN_AZIMUTH: N 26%, W 11%, E 10%, S 10%, NW 8%, SW 7%, NE 7%, SE 7%, WNW 5%, WSW 5%, NNW 4%

END_AZIMUTH: N 25%, W 11%, E 11%, S 10%, NW 7%, SW 7%, NE 7%, SE 7%, ENE 5%, WSW 5%, ESE 5%

DATA_SOURCE: CSV 69%, PDS 17%, PDC 13%

SRC_SHA256: be3b40cd098a879be12c2c3e614700 10%, 713784bed40d9e5a95b1d6240a654f 9%, a964c130071cf493e9e6b429d2a6c3 9%, c97260e82760b17bc571d55e1ca1f5 9%, 7d6b79d0049a6edec96b061738289d 9%, 48465bd9bac65e00ecea0f7e55a04d 9%, f5043ecc776818b0feffdf1e0fcbaf 8%, 673db47f6dc9e97e06ffec3b628f53 8%, d109f8a6ab1a71e70f60fe42d30a0e 8%, 19702480f50cd2a8dacce5e57891fe 8%, 60c1daf96dbe8eafd48c80df5b70df 8%, 895c56fd46991c4d9a135d67558dc4 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BEGIN_YEARMONTH | who | 364 | 0 | 200806 14.6K; 202307 13.8K; 201104 12.0K; 201106 11.9K |
| BEGIN_DAY | category | 31 | 0 | 1 147.3K; 10 60.3K; 9 59.0K; 8 57.1K |
| BEGIN_TIME | other | 1.5K | 0 | 0 133.7K; 1200 38.4K; 1100 32.0K; 1000 30.6K |
| END_YEARMONTH | who | 364 | 0 | 200806 14.6K; 202307 13.8K; 201104 12.0K; 201106 11.9K |
| END_DAY | category | 31 | 0 | 31 88.6K; 30 83.5K; 10 60.2K; 9 59.6K |
| END_TIME | other | 1.5K | 0 | 2359 100.1K; 1800 50.4K; 1200 39.6K; 1900 37.6K |
| EPISODE_ID | other | 401.2K | 3 | 142499 1.4K; 135643 1.4K; 56735 1.4K; 49864 1.3K |
| EVENT_ID | id | 1.75M | 0 | 861733 1.2K; 856814 1.2K; 856812 1.2K; 835260 1.2K |
| STATE | who | 71 | 1 | TEXAS 131.1K; KANSAS 78.0K; MISSOURI 62.7K; OKLAHOMA 62.0K |
| STATE_FIPS | other | 71 | 1 | 48 131.1K; 20 78.0K; 29 62.7K; 40 62.0K |
| YEAR | category | 30 | 0 | 2011 79.1K; 2023 75.6K; 2025 72.4K; 2008 71.2K |
| MONTH_NAME | category | 12 | 0 | June 251.4K; July 230.4K; May 210.7K; August 168.0K |
| EVENT_TYPE | who | 56 | 0 | Thunderstorm Wind 450.6K; Hail 337.9K; Flash Flood 110.3K; High Wind 95.8K |
| CZ_TYPE | category | 3 | 0 | C 1.06M; Z 714.6K; M 7.5K |
| CZ_FIPS | other | 670 | 0 | 3 33.9K; 1 30.2K; 19 28.6K; 5 28.0K |
| CZ_NAME | who | 5.6K | 0 | WASHINGTON 14.5K; JEFFERSON 13.5K; JACKSON 12.4K; FRANKLIN 11.7K |
| WFO | other | 125 | 3 | LWX 54.3K; PHI 45.7K; PAH 44.0K; OUN 43.5K |
| BEGIN_DATE_TIME | who | 932.5K | 0 | 01-JUL-12 00:00:00 1.8K; 01-AUG-12 00:00:00 1.8K; 01-SEP-11 00:00:00 1.7K; 01-SEP-12 00:00:00 1.7K |
| CZ_TIMEZONE | category | 19 | 0 | CST-6 581.2K; EST-5 429.3K; CST 264.7K; EST 202.0K |
| END_DATE_TIME | who | 906.4K | 0 | 31-JUL-12 23:59:00 1.7K; 31-AUG-12 23:59:00 1.7K; 30-SEP-11 23:59:00 1.6K; 31-JUL-11 23:59:00 1.6K |
| INJURIES_DIRECT | other | 154 | 0 | 0 1.77M; 1 7.5K; 2 2.6K; 3 1.1K |
| INJURIES_INDIRECT | other | 67 | 0 | 0 1.78M; 1 1.3K; 2 617; 3 325 |
| DEATHS_DIRECT | category | 50 | 0 | 0 1.77M; 1 8.4K; 2 1.4K; 3 399 |
| DEATHS_INDIRECT | category | 22 | 0 | 0 1.78M; 1 2.2K; 2 421; 3 142 |
| DAMAGE_PROPERTY | other | 3.1K | 612.8K | 0.00K 736.1K; 1.00K 40.0K; 5.00K 33.4K; 10.00K 28.2K |
| DAMAGE_CROPS | other | 1.5K | 724.9K | 0.00K 983.7K; 0 26.8K; 0K 8.9K; 1.00K 2.5K |
| SOURCE | who | 75 | 113.6K | Trained Spotter 187.7K; Public 152.1K; Emergency Manager 109.6K; Law Enforcement 95.3K |
| MAGNITUDE | amount | 643 | 863.3K | 50.00 128.4K; 1.00 108.0K; 52.00 80.5K; 0.75 65.7K |
| MAGNITUDE_TYPE | category | 7 | 1.24M | EG 361.1K; MG 138.8K; E 23.2K; MS 8.6K |
| FLOOD_CAUSE | category | 8 | 1.65M | Heavy Rain 114.3K; Heavy Rain / Snow Melt 5.9K; Heavy Rain / Tropical Sys 3.3K; Heavy Rain / Burn Area 1.3K |
| CATEGORY | category | 6 | 1.78M | 1 399; 2 75; 4 44; 3 33 |
| TOR_F_SCALE | category | 14 | 1.74M | EF0 12.7K; EF1 9.8K; F0 9.5K; F1 4.0K |
| TOR_LENGTH | amount | 2.0K | 1.74M | .1 3.1K; 1 1.9K; .5 1.6K; .2 1.5K |
| TOR_WIDTH | other | 441 | 1.74M | 50 7.7K; 100 5.0K; 25 3.3K; 75 2.6K |
| TOR_OTHER_WFO | other | 91 | 1.78M | JAN 324; BMX 208; FFC 180; PAH 151 |
| TOR_OTHER_CZ_STATE | state | 49 | 1.78M | MS 365; AL 346; GA 241; OK 241 |
| TOR_OTHER_CZ_FIPS | other | 207 | 1.78M | 017 72; 083 63; 125 62; 089 56 |
| TOR_OTHER_CZ_NAME | who | 997 | 1.78M | MADISON 56; WASHINGTON 40; JEFFERSON 38; MARION 32 |
| BEGIN_RANGE | amount | 4.4K | 899.2K | 0 123.3K; .69 35.7K; 2 28.9K; 1 25.4K |
| BEGIN_AZIMUTH | category | 17 | 895.3K | N 193.9K; W 82.0K; E 75.9K; S 74.7K |
| BEGIN_LOCATION | who | 51.4K | 672.4K | COUNTYWIDE 19.9K; UNION 3.0K; CLINTON 2.9K; BROOKSVILLE 2.3K |
| END_RANGE | amount | 4.4K | 895.3K | 0 114.5K; .69 33.4K; 2 29.5K; 1 25.8K |
| END_AZIMUTH | category | 17 | 895.6K | N 183.2K; W 79.2K; E 77.9K; S 75.4K |
| END_LOCATION | who | 51.6K | 672.4K | COUNTYWIDE 19.9K; CLINTON 2.9K; COLLINS 2.3K; FEARNS SPGS 1.6K |
| BEGIN_LAT | other | 136.3K | 736.1K | 32.75 2.9K; 32.6 2.7K; 41.28 2.7K; 41.57 2.5K |
| BEGIN_LON | other | 185.6K | 736.1K | -91.35 2.8K; -91.2 2.7K; -89.53 2.1K; -90.87 2.1K |
| END_LAT | other | 145.3K | 736.1K | 32.6 2.7K; 41.28 2.7K; 41.57 2.5K; 32.32 2.1K |
| END_LON | other | 205.2K | 736.1K | -91.2 2.7K; -89.53 2.1K; -90.87 2.1K; -91.13 2.1K |
| EPISODE_NARRATIVE | who | 258.7K | 246.9K | Scattered thunderstorms i 2.2K; A powerful coastal storm  1.3K; Powerful and damaging thu 1.3K; During the daytime hours  1.3K |
| EVENT_NARRATIVE | other | 940.8K | 690.3K | A few trees were blown do 2.2K; Several trees were blown  1.3K; MPing report. 937; The remnants of Tropical  870 |
| DATA_SOURCE | category | 4 | 3 | CSV 1.23M; PDS 307.7K; PDC 239.9K |
| INGESTED_AT | audit | 30 | 0 | 1782670375721602 79.1K; 1782670475663108 75.6K; 1782620758619766 72.4K; 1782670350140428 71.2K |
| SOURCE_RUN_ID | audit | 2 | 0 | db3c7fe38dea47eb 1.71M; 11f7d7b4-d35d-4e4f-be40-4 72.4K |
| SRC_SHA256 | category | 30 | 0 | be3b40cd098a879be12c2c3e6 79.1K; 713784bed40d9e5a95b1d6240 75.6K; a964c130071cf493e9e6b429d 72.4K; c97260e82760b17bc571d55e1 71.2K |
