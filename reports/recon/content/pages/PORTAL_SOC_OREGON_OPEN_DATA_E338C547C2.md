# PORTAL_SOC_OREGON_OPEN_DATA_E338C547C2

rows 2.0K  columns 15  scan 3.1s

roles: amount 1, audit 2, category 8, date 3, other 1, who 1

## when

RECORDED_DATE
  2025      1.3K  ##############################
  2026       681  ###############

EFFECTIVE_DATE
  2012        80  ##
  2022        15  
  2023       176  ####
  2024        54  #
  2025       450  ###########
  2026      1.2K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ESTABLISHED_RATE | 2.0K | 20 | 2.2K | 4.2K | 6.0K | 3.85M |

## who

SRC_SHA256 by rows
      2.0K  ef1a0fe118e2a50ef6830dc24f42222067a2e3e8517871550d154947a6b077fa

SRC_SHA256 by dollars
       3.85M     2.0K rows  ef1a0fe118e2a50ef6830dc24f42222067a2e3e8517871550d154947a6b0

## who x when

SRC_SHA256 by EFFECTIVE_DATE, dollars = ESTABLISHED_RATE
  ef1a0fe118e2a50ef6830dc24f42222067a2e3e8  2012:117.2K 2022:13.9K 2023:339.9K 2024:61.9K 2025:815.3K 2026:2.50M

## what

GASO_NAME: Springfield Fire and Life Safe 16%, Tualatin Valley Fire & Rescue 14%, Marion County Fire District No 12%, American Medical Response NW-M 12%, McMinnville Fire District 10%, ADVENTURE MEDICS LLC 8%, Mercy Flights, Inc 7%, Santiam Memorial Hospital 5%, South Lane County Fire & Rescu 5%, UMATILLA COUNTY FIRE DISTRICT  4%, Jefferson County Rural Fire Pr 4%, Lebanon Rural Fire Protection  3%

GASO_LICENSE_NUMBER: 2008 16%, 3402 14%, 2410 12%, 3433 12%, 3665 10%, 2919 8%, 1548 7%, 2403 5%, 2002 5%, 3003 4%, 1614 4%, 2204 3%

GASO_NPI: 1619925997 16%, 1750652673 14%, nan 14%, 1972609923 12%, 1649059148 10%, 1588105670 8%, 1134161391 7%, 1962566752 5%, 1578562112 5%, 1083061121 4%, 1649970187 4%, 1366496853 3%

FIREMED_YN: True 65%, False 35%

RATE_TYPE: Single Rate 63%, Resident 18%, Non-Resident 18%

RATE_CODE: ALS1-E (A0427) 13%, MILEAGE (A0425) 13%, BLS-E (A0429) 13%, ALS2 (A0433) 13%, BLS-NE (A0428) 12%, ALS1-NE (A0426) 12%, NON-TX (A0998) 12%, SCT (A0434) 11%

COMMENTS: nan 59%, AO424 EXTRA ATTENDANT $97 AO42 14%, A0426, A0427, A0428, A0429, A0 12%, Our fees do not have an expira 9%, EVENT STANDBY 160 PER HOUR
EXT 3%, We bill for an additional EMS  1%, Non-transport rates depend on  1%, The no transport fee is only u 0%, The Non-Tx A0998 above is if A 0%

FIREMED_INFO: nan 98%, www.lapinefire.com 1%, www.sheridanfd.org  
Cost is $ 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECORDED_DATE | date | 27 | 0 | 2025-12-30T23:30:57.000 272; 2025-12-30T23:02:36.000 240; 2025-12-31T19:06:29.000 200; 2026-01-08T17:20:52.000 200 |
| GASO_NAME | category | 27 | 0 | Springfield Fire and Life 272; Tualatin Valley Fire & Re 240; Marion County Fire Distri 200; American Medical Response 200 |
| GASO_LICENSE_NUMBER | category | 27 | 0 | 2008 272; 3402 240; 2410 200; 3433 200 |
| GASO_NPI | category | 26 | 0 | 1619925997 272; 1750652673 240; nan 235; 1972609923 200 |
| FIREMED_YN | category | 3 | 1.9K | True 53; False 28 |
| EFFECTIVE_DATE | date | 13 | 0 | 2026-01-01T00:00:00.000 1.1K; 2025-07-01T00:00:00.000 332; 2023-08-17T00:00:00.000 176; 2026-01-07T00:00:00.000 140 |
| ZIP_CODE | other | 161 | 0 | 97426 32; 97424 32; 97405 32; 97304 31 |
| RATE_TYPE | category | 3 | 0 | Single Rate 1.3K; Resident 370; Non-Resident 363 |
| RATE_CODE | category | 8 | 0 | ALS1-E (A0427) 263; MILEAGE (A0425) 262; BLS-E (A0429) 262; ALS2 (A0433) 260 |
| ESTABLISHED_RATE | amount | 108 | 0 | 2333.00 150; 2510.00 150; 4003.00 125; 2384.00 102 |
| COMMENTS | category | 9 | 0 | nan 1.2K; AO424 EXTRA ATTENDANT $97 272; A0426, A0427, A0428, A042 240; Our fees do not have an e 176 |
| FIREMED_INFO | category | 3 | 0 | nan 2.0K; www.lapinefire.com 28; www.sheridanfd.org  
Cost 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:44:36.56929 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 878c19dc-566e-4666-ad49-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | ef1a0fe118e2a50ef6830dc24 2.0K |
