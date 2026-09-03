# PORTAL_SOC_PA_OPEN_DATA_POR_7D4F8FCE94

rows 1.4K  columns 21  scan 6.2s

roles: amount 3, audit 2, category 3, date 1, other 10, who 3

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LONGITUDE | 1.4K | -80.35 | -77.34 | -75.03 | -75.03 | -110.8K |
| LATITUDE | 1.4K | 39.35 | 40.80 | 41.99 | 41.99 | 58.3K |
| WEEKLY_WAGES | 1.3K | 0 | 860 | 2.6K | 3.4K | 1.22M |

## who

AREA_NAME by rows
        21  Huntingdon County
        21  Lebanon County
        21  Cambria County
        21  Wayne County
        21  Centre County
        21  Adams County
        21  Mifflin County
        21  Elk County
        21  Perry County
        21  Lawrence County
        21  Pike County
        21  Jefferson County
        21  Northumberland County
        21  Lehigh County
        21  Clearfield County
        21  Warren County
        21  Dauphin County
        21  Crawford County
        21  Luzerne County
        21  Snyder County

AREA_NAME by dollars
       29.9K       21 rows  Chester County
       28.4K       21 rows  Montgomery County
       28.1K       21 rows  Delaware County
       27.8K       21 rows  Philadelphia County
       27.2K       21 rows  Allegheny County
       26.8K       21 rows  Washington County
       25.5K       21 rows  Pennsylvania
       24.8K       21 rows  Bucks County
       22.7K       21 rows  Butler County
       22.1K       21 rows  Dauphin County
       22.1K       21 rows  Berks County
       22.0K       21 rows  York County
       21.9K       21 rows  Northampton County
       21.7K       21 rows  Cumberland County
       21.4K       21 rows  Lehigh County
       21.0K       21 rows  Beaver County
       20.8K       21 rows  Westmoreland County
       20.7K       21 rows  Lancaster County
       20.2K       21 rows  Monroe County
       20.0K       21 rows  Indiana County

GEOCODED_COLUMN by rows
        21  {"type": "Point", "coordinates": [-78.5712202, 41.81037074]}
        21  {"type": "Point", "coordinates": [-80.26009411, 41.30237777]}
        21  {"type": "Point", "coordinates": [-76.46182575, 40.367597]}
        21  {"type": "Point", "coordinates": [-79.03100206, 39.97146299]}
        21  {"type": "Point", "coordinates": [-78.11485045, 39.92487511]}
        21  {"type": "Point", "coordinates": [-76.25138768, 40.04590796]}
        21  {"type": "Point", "coordinates": [-76.77960568, 40.41974636]}
        21  {"type": "Point", "coordinates": [-79.09333493, 40.65295497]}
        21  {"type": "Point", "coordinates": [-79.23780995, 41.51357876]}
        21  {"type": "Point", "coordinates": [-77.405775, 40.53433008]}
        21  {"type": "Point", "coordinates": [-77.07255968, 40.77113737]}
        21  {"type": "Point", "coordinates": [-77.89879229, 41.74420644]}
        21  {"type": "Point", "coordinates": [-78.34907687, 40.48555024]}
        21  {"type": "Point", "coordinates": [-75.11291241, 40.33501133]}
        21  {"type": "Point", "coordinates": [-77.62003089, 40.61274928]}
        21  {"type": "Point", "coordinates": [-79.47316899, 40.81509526]}
        21  {"type": "Point", "coordinates": [-76.72576052, 39.92192531]}
        21  {"type": "Point", "coordinates": [-79.47134118, 40.310315]}
        21  {"type": "Point", "coordinates": [-77.25788076, 41.77333834]}
        21  {"type": "Point", "coordinates": [-77.6428376, 41.23286274]}

GEOCODED_COLUMN by dollars
       29.9K       21 rows  {"type": "Point", "coordinates": [-75.75626498, 39.97487056]
       28.4K       21 rows  {"type": "Point", "coordinates": [-75.37252001, 40.20989874]
       28.1K       21 rows  {"type": "Point", "coordinates": [-75.40627712, 39.91657867]
       27.8K       21 rows  {"type": "Point", "coordinates": [-75.140236, 40.00444354]}
       27.2K       21 rows  {"type": "Point", "coordinates": [-79.98619843, 40.46735543]
       26.8K       21 rows  {"type": "Point", "coordinates": [-80.25180083, 40.19109663]
       25.5K       21 rows  {"type": "Point", "coordinates": [-75.167756, 39.346129]}
       24.8K       21 rows  {"type": "Point", "coordinates": [-75.11291241, 40.33501133]
       22.7K       21 rows  {"type": "Point", "coordinates": [-79.91711779, 40.91083185]
       22.1K       21 rows  {"type": "Point", "coordinates": [-76.77960568, 40.41974636]
       22.1K       21 rows  {"type": "Point", "coordinates": [-75.93077327, 40.41939635]
       22.0K       21 rows  {"type": "Point", "coordinates": [-76.72576052, 39.92192531]
       21.9K       21 rows  {"type": "Point", "coordinates": [-75.31263726, 40.7545954]}
       21.7K       21 rows  {"type": "Point", "coordinates": [-77.26866271, 40.16759839]
       21.4K       21 rows  {"type": "Point", "coordinates": [-75.60099481, 40.61464794]
       21.0K       21 rows  {"type": "Point", "coordinates": [-80.35107356, 40.68349245]
       20.8K       21 rows  {"type": "Point", "coordinates": [-79.47134118, 40.310315]}
       20.7K       21 rows  {"type": "Point", "coordinates": [-76.25138768, 40.04590796]
       20.2K       21 rows  {"type": "Point", "coordinates": [-75.34083603, 41.06091787]
       20.0K       21 rows  {"type": "Point", "coordinates": [-79.09333493, 40.65295497]

SRC_SHA256 by rows
      1.4K  d7b5adeec98cf6dfb8f0b2c1d5560b54553a232d4a5c491955472f4ac3cb0241

SRC_SHA256 by dollars
       1.22M     1.4K rows  d7b5adeec98cf6dfb8f0b2c1d5560b54553a232d4a5c491955472f4ac3cb

## who x when

AREA_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = WEEKLY_WAGES
  Adams County                              2026:16.2K
  Allegheny County                          2026:27.2K
  Berks County                              2026:22.1K
  Bucks County                              2026:24.8K
  Butler County                             2026:22.7K
  Cambria County                            2026:16.9K
  Centre County                             2026:19.2K
  Chester County                            2026:29.9K
  Clearfield County                         2026:17.0K
  Crawford County                           2026:17.1K
  Dauphin County                            2026:22.1K
  Delaware County                           2026:28.1K
  Elk County                                2026:14.0K
  Huntingdon County                         2026:16.7K
  Jefferson County                          2026:15.0K
  Lawrence County                           2026:18.2K
  Lebanon County                            2026:17.5K
  Lehigh County                             2026:21.4K
  Luzerne County                            2026:19.8K
  Mifflin County                            2026:16.4K
  Montgomery County                         2026:28.4K
  Northumberland County                     2026:14.9K
  Pennsylvania                              2026:25.5K
  Perry County                              2026:11.3K
  Philadelphia County                       2026:27.8K
  Pike County                               2026:16.2K
  Snyder County                             2026:11.4K
  Warren County                             2026:15.5K
  Washington County                         2026:26.8K
  Wayne County                              2026:17.1K

GEOCODED_COLUMN by INGESTED_AT  LOAD STAMP, not an event date, dollars = WEEKLY_WAGES
  {"type": "Point", "coordinates": [-75.11  2026:24.8K
  {"type": "Point", "coordinates": [-75.14  2026:27.8K
  {"type": "Point", "coordinates": [-75.16  2026:25.5K
  {"type": "Point", "coordinates": [-75.31  2026:21.9K
  {"type": "Point", "coordinates": [-75.37  2026:28.4K
  {"type": "Point", "coordinates": [-75.40  2026:28.1K
  {"type": "Point", "coordinates": [-75.75  2026:29.9K
  {"type": "Point", "coordinates": [-75.93  2026:22.1K
  {"type": "Point", "coordinates": [-76.25  2026:20.7K
  {"type": "Point", "coordinates": [-76.46  2026:17.5K
  {"type": "Point", "coordinates": [-76.72  2026:22.0K
  {"type": "Point", "coordinates": [-76.77  2026:22.1K
  {"type": "Point", "coordinates": [-77.07  2026:11.4K
  {"type": "Point", "coordinates": [-77.25  2026:16.2K
  {"type": "Point", "coordinates": [-77.40  2026:10.8K
  {"type": "Point", "coordinates": [-77.62  2026:16.4K
  {"type": "Point", "coordinates": [-77.64  2026:13.6K
  {"type": "Point", "coordinates": [-77.89  2026:10.8K
  {"type": "Point", "coordinates": [-78.11  2026:10.2K
  {"type": "Point", "coordinates": [-78.34  2026:18.4K
  {"type": "Point", "coordinates": [-78.57  2026:17.4K
  {"type": "Point", "coordinates": [-79.03  2026:17.4K
  {"type": "Point", "coordinates": [-79.09  2026:20.0K
  {"type": "Point", "coordinates": [-79.23  2026:5.1K
  {"type": "Point", "coordinates": [-79.47  2026:20.8K
  {"type": "Point", "coordinates": [-79.47  2026:19.0K
  {"type": "Point", "coordinates": [-79.91  2026:22.7K
  {"type": "Point", "coordinates": [-79.98  2026:27.2K
  {"type": "Point", "coordinates": [-80.25  2026:26.8K
  {"type": "Point", "coordinates": [-80.26  2026:19.3K

## what

NAICS: 42 8%, 52 8%, 62 8%, 10 8%, 11 8%, 61 8%, 44-45 8%, 81 8%, 55 8%, 23 8%, 54 8%, 71 8%

NAICS_TITLE: Wholesale Trade 8%, Finance and Insurance 8%, Health Care and Social Assista 8%, Total, All Industries 8%, Agriculture, Forestry, Fishing 8%, Educational Services 8%, Retail Trade 8%, Other Services (except Public  8%, Management of Companies and En 8%, Construction 8%, Professional, Scientific, and  8%, Arts, Entertainment, and Recre 8%

COMPUTED_REGION_D3GW_ZNNF: 14 17%, 5 12%, 21 12%, 22 10%, 16 7%, 3 7%, 17 7%, 18 7%, 29 7%, 38 5%, 2 5%, 23 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA_NAME | who | 69 | 0 | Montgomery County 21; York County 21; Northampton County 21; Beaver County 21 |
| COUNTY_CODE | other | 69 | 0 | 46 21; 67 21; 48 21; 04 21 |
| STATE_FIPS | other | 1 | 0 | 42 1.4K |
| COUNTY_FIPS | other | 69 | 0 | 091 21; 133 21; 095 21; 007 21 |
| CALENDAR_YEAR | other | 1 | 0 | 2018 1.4K |
| NAICS | category | 21 | 0 | 42 68; 52 68; 62 68; 10 68 |
| NAICS_TITLE | category | 21 | 0 | Wholesale Trade 68; Finance and Insurance 68; Health Care and Social As 68; Total, All Industries 68 |
| ESTABLISHMENTS | other | 552 | 0 | 7 23; 11 21; 12 19; 2 17 |
| LONGITUDE | amount | 68 | 0 | -75.37252001 21; -76.72576052 21; -75.31263726 21; -80.35107356 21 |
| LATITUDE | amount | 69 | 0 | 40.20989874 21; 39.92192531 21; 40.7545954 21; 40.68349245 21 |
| GEOCODED_COLUMN | who | 66 | 0 | {"type": "Point", "coordi 21; {"type": "Point", "coordi 21; {"type": "Point", "coordi 21; {"type": "Point", "coordi 21 |
| COMPUTED_REGION_NMSQ_HQVV | other | 69 | 0 | 57 21; 12 21; 59 21; 42 21 |
| COMPUTED_REGION_D3GW_ZNNF | category | 32 | 0 | 14 147; 5 105; 21 105; 22 84 |
| COMPUTED_REGION_AMQZ_JBR4 | other | 69 | 0 | 1082 21; 470 21; 1339 21; 379 21 |
| COMPUTED_REGION_R6RF_P9ET | other | 59 | 0 | 14 63; 88 42; 74 42; 36 42 |
| COMPUTED_REGION_RAYF_JJGK | other | 67 | 0 | 249 21; 43 21; 280 21; 2 21 |
| EMPLOYMENT | other | 1.1K | 0 | nan 92; 1499 8; 0 8; 22693 7 |
| WEEKLY_WAGES | amount | 847 | 0 | nan 92; 918 8; 447 8; 982 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:27.15645 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 7d065d7f-5a62-4c15-8d6f-3 1.4K |
| SRC_SHA256 | who | 1 | 0 | d7b5adeec98cf6dfb8f0b2c1d 1.4K |
