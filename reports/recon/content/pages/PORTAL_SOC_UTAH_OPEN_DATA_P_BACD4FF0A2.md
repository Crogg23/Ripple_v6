# PORTAL_SOC_UTAH_OPEN_DATA_P_BACD4FF0A2

rows 432  columns 29  scan 2.8s

roles: amount 1, audit 2, category 9, date 1, other 16, who 1

## when

INGESTED_AT
  2026       432  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1998 | 431 | -1.08M | 212.6K | 73.39M | 177.78M | 1.93B |

## who

SRC_SHA256 by rows
       432  5783ad874f502080f2eaaae46f4afad2fb9e98c99a6309f55ff2e6a6230031f3

SRC_SHA256 by dollars
       1.93B      432 rows  5783ad874f502080f2eaaae46f4afad2fb9e98c99a6309f55ff2e6a62300

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY1998
  5783ad874f502080f2eaaae46f4afad2fb9e98c9  2026:1.93B

## what

COUNTY: Davis 66%, Davis  34%

NAICS_MAJOR_SECTOR: OTHER SERVICES-EXECPT PUBLIC A 9%, PRIOR-PERIOD PAYMENTS & REFUND 9%, RETAIL-MISCELLANEOUS RETAIL TR 9%, RETAIL-HEALTH & PERSONAL CARE  8%, FOOD SERVICES & DRINKING PLACE 8%, PROFESSIONAL, SCIENTIFIC, & TE 8%, MANUFACTURING(310000-339999) 8%, TRANSPORTATION & WAREHOUSING(4 8%, CONSTRUCTION(230000-239999) 8%, RETAIL-SPORTING GOODS, HOBBY,  8%, OCCASIONAL/NONCLASSIFIABLE 8%, ADMIN. & SUPPORT & WASTE MANAG 8%

LOCATION_1: {"latitude": "41.060161", "lon 16%, {"latitude": "40.879209", "lon 11%, {"latitude": "41.094116", "lon 11%, {"latitude": "41.139865", "lon 8%, {"latitude": "40.980489", "lon 8%, {"latitude": "41.034877", "lon 8%, {"latitude": "40.921499", "lon 8%, {"latitude": "40.874763", "lon 8%, {"latitude": "40.841841", "lon 8%, {"latitude": "41.121659", "lon 6%, {"human_address": "{\"address\ 5%, {"latitude": "41.113869", "lon 1%

ESTIMATED_POPULATION: 68677 16%, 42898 11%, 25118 11%, 20805 8%, 20750 8%, 28283 8%, 16203 8%, 10212 8%, 16717 8%, 9819 6%, nan 5%, 30376 1%

COMPUTED_REGION_9P4X_9CJT: 57 17%, 231 16%, 234 11%, 156 8%, 327 8%, 235 8%, 7 8%, 62 8%, 532 8%, nan 5%, 6 1%

COMPUTED_REGION_DQJC_K29Y: 14 33%, 16 28%, 15 25%, 13 8%, nan 5%, 10 1%

COMPUTED_REGION_5PHJ_CC35: 10 16%, 13 16%, 7 16%, 6 12%, 11 11%, 5 8%, 9 8%, 4 6%, nan 5%

COMPUTED_REGION_QMWN_IMPY: 233 16%, 49 11%, 47 11%, 37 8%, 39 8%, 46 8%, 45 8%, 43 8%, 44 8%, 40 6%, nan 5%, 48 1%

COMPUTED_REGION_5D9V_6BUI: 22 95%, nan 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTY | category | 2 | 0 | Davis 286; Davis  146 |
| NAICS_MAJOR_SECTOR | category | 37 | 0 | OTHER SERVICES-EXECPT PUB 15; PRIOR-PERIOD PAYMENTS & R 15; RETAIL-MISCELLANEOUS RETA 15; RETAIL-HEALTH & PERSONAL  14 |
| CY1998 | amount | 215 | 0 |  .  101; 150,000 12; 1,000 8; 300,000 8 |
| CY2014 | other | 252 | 0 | nan 78; 150000 10; 250000 7; 1250000 7 |
| LOCATION_1 | category | 12 | 0 | {"latitude": "41.060161", 69; {"latitude": "40.879209", 49; {"latitude": "41.094116", 47; {"latitude": "41.139865", 36 |
| CY2000 | other | 219 | 0 | nan 80; 1000 15; 150000 12; 35000 9 |
| CY2001 | other | 221 | 0 | nan 74; 200000 12; 150000 12; 60000 11 |
| CY2002 | other | 224 | 0 | nan 74; 15000 11; 150000 11; 1000 10 |
| CY2003 | other | 226 | 0 | nan 76; 150000 11; 300000 8; 1000 8 |
| CY2004 | other | 236 | 0 | nan 74; 150000 12; 350000 9; 1250000 9 |
| CY2005 | other | 236 | 0 | nan 74; 200000 11; 250000 10; 150000 9 |
| CY2006 | other | 232 | 0 | nan 76; 150000 10; 15000 9; 2000000 9 |
| CY2007 | other | 240 | 0 | nan 76; 250000 11; 2000 9; 200000 8 |
| CY2008 | other | 235 | 0 | nan 70; 150000 15; 1000 13; 15000 10 |
| CY2009 | other | 232 | 0 | nan 69; 150000 12; 1000 9; 2000 9 |
| CY2010 | other | 249 | 0 | nan 67; 1000 10; 150000 10; 20000 9 |
| CY1999 | other | 220 | 0 | nan 85; 1000 14; 250000 10; 150000 9 |
| CY2011 | other | 245 | 0 | nan 74; 150000 9; 1500000 9; 200000 8 |
| CY2012 | other | 247 | 0 | nan 76; 250000 11; 150000 9; 1000 9 |
| CY2013 | other | 236 | 0 | nan 81; 150000 11; 250000 8; 1000 8 |
| ESTIMATED_POPULATION | category | 12 | 0 | 68677 69; 42898 49; 25118 47; 20805 36 |
| COMPUTED_REGION_9P4X_9CJT | category | 11 | 0 | 57 73; 231 69; 234 49; 156 36 |
| COMPUTED_REGION_DQJC_K29Y | category | 6 | 0 | 14 142; 16 119; 15 106; 13 36 |
| COMPUTED_REGION_5PHJ_CC35 | category | 9 | 0 | 10 71; 13 70; 7 69; 6 53 |
| COMPUTED_REGION_QMWN_IMPY | category | 12 | 0 | 233 69; 49 49; 47 47; 37 36 |
| COMPUTED_REGION_5D9V_6BUI | category | 2 | 0 | 22 409; nan 23 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:51:58.19392 432 |
| SOURCE_RUN_ID | audit | 1 | 0 | 817eac6d-58a7-4dcd-9705-3 432 |
| SRC_SHA256 | who | 1 | 0 | 5783ad874f502080f2eaaae46 432 |
