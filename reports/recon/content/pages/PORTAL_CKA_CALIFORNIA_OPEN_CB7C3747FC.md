# PORTAL_CKA_CALIFORNIA_OPEN_CB7C3747FC

rows 1.5K  columns 16  scan 5.8s

roles: amount 2, audit 2, category 1, date 3, id 2, other 3, who 4

## when

CREATED_DATE
  2025        25  ##############################
  2026         2  ##

LAST_EDITED_DATE
  2026      1.5K  ##############################

INGESTED_AT
  2026      1.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 1.5K | 49.46 | 1.32M | 14.12B | 73.94B | 671.90B |
| SHAPE__LENGTH | 1.5K | 36.68 | 6.6K | 937.8K | 2.03M | 80.35M |

## who

LAST_EDITED_USER by rows
      1.5K  APRICE1

LAST_EDITED_USER by dollars
     671.90B     1.5K rows  APRICE1

CITY by rows
       714  Unincorporated
        22  Big Bear Lake
        20  Santa Rosa
        12  Long Beach
         9  Tustin
         9  Modesto
         8  Porterville
         8  Healdsburg
         8  Coalinga
         8  Napa
         7  Watsonville
         7  Redlands
         7  Fort Bragg
         6  Windsor
         6  Patterson
         5  Los Angeles
         5  Vallejo
         5  Petaluma
         5  Soledad
         5  Adelanto

CITY by dollars
     636.31B      714 rows  Unincorporated
       1.79B        5 rows  Los Angeles
       1.26B        5 rows  San Diego
     963.10M        2 rows  San Francisco
     789.53M        1 rows  California
     741.46M        3 rows  San Jose
     603.58M        1 rows  Bakersfield
     474.93M        2 rows  Fresno
     426.75M        1 rows  Sacramento
     407.23M        1 rows  Palmdale
     406.07M        1 rows  Lancaster
     364.46M        1 rows  Fremont
     355.55M        1 rows  Palm Springs
     323.08M        1 rows  Oakland
     307.57M        1 rows  Riverside
     294.70M        1 rows  Apple Valley
     283.19M        1 rows  Victorville
     281.10M        4 rows  Santa Clarita
     278.05M        1 rows  Stockton
     277.21M        1 rows  Hesperia

COUNTY by rows
       218  Los Angeles County
       102  Sonoma County
        91  San Bernardino County
        82  Orange County
        78  Santa Clara County
        65  San Diego County
        63  Fresno County
        57  Stanislaus County
        53  Ventura County
        52  Riverside County
        45  San Mateo County
        43  Contra Costa County
        43  San Joaquin County
        41  Tulare County
        35  Kern County
        29  Solano County
        26  Napa County
        26  Marin County
        26  Santa Barbara County
        25  Monterey County

COUNTY by dollars
      77.50B       91 rows  San Bernardino County
      41.10B        4 rows  Inyo County
      31.84B       35 rows  Kern County
      29.42B       10 rows  Siskiyou County
      27.42B       52 rows  Riverside County
      24.30B       63 rows  Fresno County
      21.28B        6 rows  Lassen County
      19.48B        3 rows  Modoc County
      19.31B       41 rows  Tulare County
      18.28B       12 rows  Humboldt County
      18.03B      218 rows  Los Angeles County
      17.41B        7 rows  Shasta County
      16.85B       18 rows  Mendocino County
      16.72B       65 rows  San Diego County
      16.56B       13 rows  Imperial County
      15.05B       25 rows  Monterey County
      14.49B       26 rows  Santa Barbara County
      14.45B        1 rows  Trinity County
      14.12B       10 rows  San Luis Obispo County
      13.12B        9 rows  Tehama County

SRC_SHA256 by rows
      1.5K  353219e4f0a07b82a9b2bb376450a4fbdb7ee44435723d990f6cea65d1ed20f4

SRC_SHA256 by dollars
     671.90B     1.5K rows  353219e4f0a07b82a9b2bb376450a4fbdb7ee44435723d990f6cea65d1ed

## who x when

LAST_EDITED_USER by LAST_EDITED_DATE, dollars = SHAPE__AREA
  APRICE1                                   2026:671.90B

CITY by LAST_EDITED_DATE, dollars = SHAPE__AREA
  Adelanto                                  2026:202.54M
  Bakersfield                               2026:603.58M
  Big Bear Lake                             2026:24.46M
  California                                2026:789.53M
  Coalinga                                  2026:26.87M
  Fort Bragg                                2026:12.72M
  Fremont                                   2026:364.46M
  Fresno                                    2026:474.93M
  Healdsburg                                2026:18.23M
  Lancaster                                 2026:406.07M
  Long Beach                                2026:194.86M
  Los Angeles                               2026:1.79B
  Modesto                                   2026:188.20M
  Napa                                      2026:77.41M
  Palmdale                                  2026:407.23M
  Patterson                                 2026:41.77M
  Petaluma                                  2026:61.12M
  Porterville                               2026:75.39M
  Redlands                                  2026:137.16M
  Sacramento                                2026:426.75M
  San Diego                                 2026:1.26B
  San Francisco                             2026:963.10M
  San Jose                                  2026:741.46M
  Santa Rosa                                2026:181.26M
  Soledad                                   2026:18.97M
  Tustin                                    2026:41.81M
  Unincorporated                            2026:636.31B
  Vallejo                                   2026:208.87M
  Watsonville                               2026:27.80M
  Windsor                                   2026:31.83M

## what

CREATED_USER: APRICE1 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.5K | 0 | 1743 8; 1732 8; 1707 8; 1704 8 |
| CO | other | 58 | 0 | 19 218; 49 102; 36 91; 30 82 |
| COUNTY | who | 58 | 0 | Los Angeles County 218; Sonoma County 102; San Bernardino County 91; Orange County 82 |
| CITY | who | 481 | 0 | Unincorporated 714; Big Bear Lake 23; Santa Rosa 22; Long Beach 12 |
| COPRI | other | 544 | 0 | 19000 110; 43000 62; 49000 55; 37000 43 |
| CDTFA_ID | other | 537 | 0 | 19998 110; 43998 62; 49998 55; 37998 43 |
| CREATED_USER | category | 2 | 1.5K | APRICE1 27 |
| CREATED_DATE | date | 27 | 1.5K | 6/18/2026 4:13:56 AM 1; 3/9/2026 11:24:07 PM 1; 11/5/2025 5:27:33 AM 1; 11/5/2025 3:30:26 AM 1 |
| LAST_EDITED_USER | who | 1 | 0 | APRICE1 1.5K |
| LAST_EDITED_DATE | date | 57 | 0 | 2/13/2026 3:17:22 AM 1.4K; 6/9/2026 12:48:12 AM 2; 6/3/2026 11:55:32 PM 2; 6/9/2026 2:00:33 AM 2 |
| GLOBALID | id | 1.5K | 0 | 49eac6c1-6d97-4222-a32f-a 8; caf5b1ce-cd88-4d86-831a-2 8; c7be63b0-7508-4377-9c20-8 8; 91ab341b-d2e9-4b2b-a202-e 8 |
| SHAPE__AREA | amount | 1.5K | 0 | 232172.97265625 8; 271451.234375 8; 65143.3203125 8; 8552.28515625 8 |
| SHAPE__LENGTH | amount | 1.5K | 0 | 1928.94546678178 8; 2137.60047018673 8; 4554.45568456556 8; 569.415238998113 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:55:19.38025 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | e92ca644-0e3e-40c7-a899-1 1.5K |
| SRC_SHA256 | who | 1 | 0 | 353219e4f0a07b82a9b2bb376 1.5K |
