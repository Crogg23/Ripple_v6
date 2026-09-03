# FED_EPA_RCRA_FACILITIES

rows 1.61M  columns 18  scan 4.4s

roles: amount 2, audit 2, category 6, id 1, other 3, state 2, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE83 | 1.51M | -14.34 | 37.71 | 47.46 | 80 | 56.59M |
| LONGITUDE83 | 1.51M | -179.29 | -97.26 | -70.92 | 145.81 | -151.09M |

## who

FACILITY_NAME by rows
     43.7K  RESIDENCE
     17.2K  CON EDISON
      2.6K  SUNOCO SERVICE STATION
      2.4K  MI DEPT/TRANSPORTATION
      1.6K  PACIFIC BELL
      1.1K  NEW CINGULAR WIRELESS PCS LLC
       959  PENSKE TRUCK LEASING CO LP
       881  MI DEPT/STATE POLICE
       842  SHELL OIL CO
       764  SHELL SERVICE STATION
       713  MI DEPT/NATURAL RESOURCES AND ENVIRONMENT
       606  BANK OF AMERICA
       586  EXXON MOBIL CORPORATION
       527  STAR ENTERPRISE
       511  ASPEN DENTAL
       505  CHEVRON USA INC
       487  CSX TRANSPORTATION INC
       433  SHERWIN WILLIAMS CO
       419  AMOCO OIL CO
       419  TEXACO SERVICE STATION

FACILITY_NAME by dollars
       1.32M    43.7K rows  RESIDENCE
      648.6K    17.2K rows  CON EDISON
       99.2K     2.6K rows  SUNOCO SERVICE STATION
       52.8K     1.6K rows  PACIFIC BELL
       46.9K     2.4K rows  MI DEPT/TRANSPORTATION
       36.7K     1.1K rows  NEW CINGULAR WIRELESS PCS LLC
       33.5K      959 rows  PENSKE TRUCK LEASING CO LP
       32.8K      881 rows  MI DEPT/STATE POLICE
       31.3K      842 rows  SHELL OIL CO
       26.9K      764 rows  SHELL SERVICE STATION
       26.5K      713 rows  MI DEPT/NATURAL RESOURCES AND ENVIRONMENT
       21.0K      606 rows  BANK OF AMERICA
       19.3K      511 rows  ASPEN DENTAL
       17.1K      419 rows  AMOCO OIL CO
       17.0K      527 rows  STAR ENTERPRISE
       17.0K      398 rows  SPEEDWAY LLC
       16.8K      392 rows  FAMILY DOLLAR STORES
       14.6K      487 rows  CSX TRANSPORTATION INC
       14.5K      586 rows  EXXON MOBIL CORPORATION
       14.5K      396 rows  PENSKE AUTO CENTER

CITY_NAME by rows
     33.8K  SAN DIEGO
     32.4K  LOS ANGELES
     26.5K  NEW YORK
     19.7K  BROOKLYN
     19.0K  SAN FRANCISCO
     17.6K  SAN JOSE
     10.5K  SACRAMENTO
      9.6K  OAKLAND
      9.1K  FRESNO
      7.8K  LONG BEACH
      7.8K  CHICAGO
      7.5K  ANAHEIM
      7.5K  HUNTINGTON BEACH
      7.0K  BAKERSFIELD
      6.9K  BRONX
      6.6K  SANTA ANA
      6.5K  RIVERSIDE
      5.9K  HOUSTON
      5.3K  TORRANCE
      5.2K  FREMONT

CITY_NAME by dollars
       1.07M    33.8K rows  SAN DIEGO
       1.07M    32.4K rows  LOS ANGELES
      980.3K    26.5K rows  NEW YORK
      760.8K    19.7K rows  BROOKLYN
      692.2K    19.0K rows  SAN FRANCISCO
      634.5K    17.6K rows  SAN JOSE
      385.3K    10.5K rows  SACRAMENTO
      350.2K     9.6K rows  OAKLAND
      315.2K     9.1K rows  FRESNO
      315.0K     7.8K rows  CHICAGO
      259.2K     6.9K rows  BRONX
      252.3K     7.8K rows  LONG BEACH
      247.6K     7.5K rows  ANAHEIM
      246.1K     7.5K rows  HUNTINGTON BEACH
      229.9K     7.0K rows  BAKERSFIELD
      216.6K     6.6K rows  SANTA ANA
      211.3K     6.5K rows  RIVERSIDE
      190.2K     5.2K rows  FREMONT
      188.0K     4.2K rows  MINNEAPOLIS
      184.9K     5.0K rows  CONCORD

## where

ACTIVITY_LOCATION: CA 681.1K, NY 126.2K, FL 53.7K, MI 49.8K, MN 48.8K, IL 43.7K, TX 38.9K, NJ 38.1K, OH 36.4K, MA 35.8K, PA 35.1K, WI 27.5K

STATE_CODE: CA 681.2K, NY 126.1K, FL 53.7K, MI 49.8K, MN 48.8K, IL 43.7K, TX 38.9K, NJ 38.1K, OH 36.4K, MA 35.8K, PA 35.1K, WI 27.5K

## what

FULL_ENFORCEMENT: ------ 100%, L----- 0%, ---S-- 0%, ---ST- 0%, -----H 0%, L--S-- 0%, L--ST- 0%, ----T- 0%, L----H 0%, L---T- 0%, ---S-H 0%, --BS-- 0%

HREPORT_UNIVERSE_RECORD: Other 73%, VSQG 18%, SQG 7%, LQG 2%, Transporter 1%, Transporter, VSQG 0%, SQG, Transporter 0%, LQG, Transporter 0%, LQG, Operating TSDF 0%, Legacy TSDF 0%, LQG, Legacy TSDF 0%, Legacy TSDF, VSQG 0%

FED_WASTE_GENERATOR: N   73%, 3   18%, 2   7%, 1   2%

TRANSPORTER: N   99%, Y   1%

ACTIVE_SITE: ----- 42%, H---- 34%, ----S 22%, H---S 2%, HPA-- 0%, H-A-- 0%, --A-- 0%, -PA-- 0%, HP--- 0%, HPA-S 0%, H-A-S 0%, -P--- 0%

OPERATING_TSDF: ------          100%, ---S--          0%, ---ST-          0%, ----T-          0%, L--ST-          0%, --BS--          0%, L-----          0%, --B---          0%, L--S--          0%, --BST-          0%, -I-S--          0%, -I-ST-          0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID_NUMBER | id | 1.64M | 0 | CAC003352384 1.2K; CAC003357148 1.2K; FLR000275388 1.2K; MDR000528593 1.2K |
| FACILITY_NAME | who | 1.29M | 12 | RESIDENCE 46.1K; CON EDISON 17.8K; NEW CINGULAR WIRELESS PCS 3.8K; CITY OF ONTARIO FIRE DEPA 2.8K |
| ACTIVITY_LOCATION | state | 66 | 0 | CA 681.1K; NY 126.2K; FL 53.7K; MI 49.8K |
| FULL_ENFORCEMENT | category | 32 | 0 | ------ 1.61M; L----- 651; ---S-- 440; ---ST- 221 |
| HREPORT_UNIVERSE_RECORD | category | 23 | 0 | Other 1.17M; VSQG 286.4K; SQG 108.4K; LQG 32.1K |
| STREET_ADDRESS | other | 1.42M | 1.4K | LAT/LONG_USED 6.2K; 5232 CLAREMONT AVE 1.2K; 1342 9TH STREET 1.2K; 11900 HENRY FLAGLER AVE 1.2K |
| CITY_NAME | who | 23.7K | 800 | SAN DIEGO 33.3K; LOS ANGELES 32.6K; NEW YORK 27.2K; BROOKLYN 19.5K |
| STATE_CODE | state | 69 | 0 | CA 681.2K; NY 126.1K; FL 53.7K; MI 49.8K |
| ZIP_CODE | other | 218.3K | 961 | 92637 4.1K; 92646 4.0K; 91001 4.0K; 94080 4.0K |
| LATITUDE83 | amount | 1.18M | 104.9K | 34.132873 2.1K; 34.067668 2.1K; 34.169824 1.7K; 37.838928 1.1K |
| LONGITUDE83 | amount | 1.22M | 104.9K | -118.200253 2.1K; -118.453504 2.1K; -118.518519 1.7K; -122.260934 1.1K |
| FED_WASTE_GENERATOR | category | 4 | 9.1K | N   1.17M; 3   288.2K; 2   109.4K; 1   33.8K |
| TRANSPORTER | category | 2 | 608 | N   1.60M; Y   14.3K |
| ACTIVE_SITE | category | 25 | 0 | ----- 679.8K; H---- 545.2K; ----S 355.8K; H---S 28.3K |
| OPERATING_TSDF | category | 21 | 0 | ------          1.61M; ---S--          262; ---ST-          209; ----T-          33 |
| INGESTED_AT | audit | 1 | 0 | 1786163847152640 1.61M |
| SOURCE_RUN_ID | audit | 1 | 0 | ee35a6a3-0939-44ee-a263-f 1.61M |
| SRC_SHA256 | other | 1 | 0 | 8457e99a525f9546773bc2e3f 1.61M |
