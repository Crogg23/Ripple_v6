# PORTAL_SOC_UTAH_OPEN_DATA_P_79EAB10D34

rows 2.0K  columns 29  scan 4.6s

roles: amount 11, audit 2, category 5, date 1, other 9, who 2

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1999 | 2.0K | -49.82M | 20.0K | 55.05M | 332.09M | 6.36B |
| CY2000 | 2.0K | -16.23M | 20.0K | 58.53M | 342.76M | 6.72B |
| CY2001 | 2.0K | -1.49M | 25.0K | 55.78M | 361.97M | 6.70B |
| CY2002 | 2.0K | -4.18M | 25.0K | 55.43M | 372.70M | 6.70B |
| CY2003 | 2.0K | -3.09M | 25.0K | 55.39M | 378.38M | 7.14B |
| CY2004 | 2.0K | -9.86M | 25.0K | 66.37M | 381.61M | 7.93B |

## who

LOCATION_1 by rows
        17  {"human_address": "{\"address\": \"\", \"city\": \"\", \"state\": \"\"
        14  {"latitude": "40.655529", "longitude": "-111.498478", "human_address":
        14  {"latitude": "40.915143", "longitude": "-109.703974", "human_address":
        13  {"latitude": "40.180046", "longitude": "-111.566495", "human_address":
        13  {"latitude": "37.170952", "longitude": "-113.682379", "human_address":
        13  {"latitude": "40.279968", "longitude": "-111.710835", "human_address":
        13  {"latitude": "41.161268", "longitude": "-111.968246", "human_address":
        12  {"latitude": "40.577727", "longitude": "-111.887315", "human_address":
        12  {"latitude": "40.558018", "longitude": "-111.965534", "human_address":
        12  {"latitude": "37.144705", "longitude": "-113.676419", "human_address":
        12  {"latitude": "38.072666", "longitude": "-109.343426", "human_address":
        12  {"latitude": "41.273685", "longitude": "-112.026533", "human_address":
        12  {"latitude": "40.638476", "longitude": "-112.499111", "human_address":
        12  {"latitude": "40.079973", "longitude": "-110.033491", "human_address":
        12  {"latitude": "40.571476", "longitude": "-111.861826", "human_address":
        11  {"latitude": "41.689169", "longitude": "-111.732518", "human_address":
        11  {"latitude": "41.085473", "longitude": "-111.926335", "human_address":
        11  {"latitude": "40.651858", "longitude": "-112.017038", "human_address":
        11  {"latitude": "40.623579", "longitude": "-111.77648", "human_address": 
        11  {"latitude": "40.406511", "longitude": "-111.867989", "human_address":

LOCATION_1 by dollars
     714.99M        8 rows  {"latitude": "40.657894", "longitude": "-111.883531", "human
     440.34M       13 rows  {"latitude": "41.161268", "longitude": "-111.968246", "human
     365.02M       11 rows  {"latitude": "40.757172", "longitude": "-111.899872", "human
     278.43M       13 rows  {"latitude": "40.279968", "longitude": "-111.710835", "human
     268.10M        6 rows  {"latitude": "40.71583", "longitude": "-111.891406", "human_
     242.17M       12 rows  {"latitude": "37.144705", "longitude": "-113.676419", "human
     238.22M        8 rows  {"latitude": "40.747921", "longitude": "-111.954751", "human
     193.39M       14 rows  {"latitude": "40.655529", "longitude": "-111.498478", "human
     189.38M        9 rows  {"latitude": "40.70674", "longitude": "-111.85612", "human_a
     178.94M       12 rows  {"latitude": "41.273685", "longitude": "-112.026533", "human
     135.07M       11 rows  {"latitude": "40.623579", "longitude": "-111.77648", "human_
     128.08M        9 rows  {"latitude": "40.200344", "longitude": "-109.464332", "human
     116.37M        7 rows  {"latitude": "40.314542", "longitude": "-111.710522", "human
     108.57M        7 rows  {"latitude": "40.760028", "longitude": "-111.864737", "human
      97.60M        7 rows  {"latitude": "40.755889", "longitude": "-111.884326", "human
      95.67M       11 rows  {"latitude": "41.689169", "longitude": "-111.732518", "human
      95.43M       10 rows  {"latitude": "40.875793", "longitude": "-111.871601", "human
      93.67M       10 rows  {"latitude": "41.121069", "longitude": "-112.049146", "human
      91.01M        8 rows  {"latitude": "40.397262", "longitude": "-111.796071", "human
      89.61M        8 rows  {"latitude": "40.615838", "longitude": "-111.887981", "human

SRC_SHA256 by rows
      2.0K  11cfe51becd7e4de3b115b2d8ff54b83c578202deff7abedc006d4a535f07c0c

SRC_SHA256 by dollars
       6.70B     2.0K rows  11cfe51becd7e4de3b115b2d8ff54b83c578202deff7abedc006d4a535f0

## who x when

LOCATION_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002
  11cfe51becd7e4de3b115b2d8ff54b83c578202d  2026:6.70B

## what

COUNTY: Salt Lake 26%, Utah 14%, Washington 10%, nan 9%, Cache 9%, Weber 7%, Sanpete 5%, Sevier 4%, Box Elder 4%, Summit 4%, Davis 4%, Duchesne 4%

NAICS_MAJOR_SECTOR: PRIOR-PERIOD PAYMENTS & REFUND 14%, RETAIL-MISCELLANEOUS RETAIL TR 11%, INFORMATION(510000-519999) 11%, MANUFACTURING(310000-339999) 8%, OTHER SERVICES-EXECPT PUBLIC A 8%, RETAIL-FOOD & BEVERAGE STORES( 7%, RETAIL-ELECTRONICS & APPLIANCE 7%, FOOD SERVICES & DRINKING PLACE 7%, PROFESSIONAL, SCIENTIFIC, & TE 7%, RETAIL-GASOLINE STATIONS(44700 7%, NONSTORE RETAILERS(454000-4549 7%, REAL ESTATE, RENTAL, & LEASING 6%

COMPUTED_REGION_DQJC_K29Y: 17 21%, 19 11%, 20 11%, nan 10%, 9 9%, 21 8%, 18 8%, 12 7%, 22 5%, 11 4%, 10 3%, 8 3%

COMPUTED_REGION_MFUY_BEE2: nan 13%, 34 12%, 19 11%, 4 10%, 30 10%, 6 8%, 21 8%, 23 7%, 32 6%, 36 6%, 24 5%, 2 5%

COMPUTED_REGION_5D9V_6BUI: 26 24%, 5 14%, nan 10%, 8 9%, 6 8%, 16 7%, 22 6%, 3 5%, 7 5%, 12 4%, 14 4%, 27 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_1 | who | 412 | 0 | {"human_address": "{\"add 17; {"latitude": "41.913916", 14; {"latitude": "37.170952", 14; {"latitude": "40.571476", 14 |
| ESTIMATED_POPULATION | other | 224 | 0 | nan 231; 189314 127; 115919 38; 89344 36 |
| COUNTY | category | 34 | 0 | Salt Lake 363; Utah 201; Washington 135; nan 132 |
| NAICS_MAJOR_SECTOR | category | 37 | 0 | PRIOR-PERIOD PAYMENTS & R 127; RETAIL-MISCELLANEOUS RETA 99; INFORMATION(510000-519999 97; MANUFACTURING(310000-3399 75 |
| CY1999 | amount | 469 | 0 |  .  697; 1,000 81; 2,000 52; 150,000 47 |
| CY2000 | amount | 473 | 0 |  .  717; 1,000 80; 150,000 48; 200,000 37 |
| CY2001 | amount | 472 | 0 |  .  716; 1,000 58; 150,000 48; 200,000 44 |
| CY2002 | amount | 496 | 0 |  .  711; 1,000 61; 150,000 49; 200,000 46 |
| CY2003 | amount | 508 | 0 |  .  660; 1,000 88; 150,000 45; 2,000 42 |
| CY2004 | amount | 534 | 0 |  .  647; 1,000 97; 2,000 47; 150,000 46 |
| CY2005 | amount | 526 | 0 |  .  668; 1,000 75; 150,000 49; 2,000 44 |
| CY2006 | amount | 541 | 0 |  .  664; 1,000 65; 200,000 45; 2,000 42 |
| CY2007 | amount | 573 | 0 |  .  658; 1,000 61; 150,000 50; 200,000 39 |
| CY2008 | amount | 546 | 0 |  .  628; 1,000 67; 150,000 55; 2,000 43 |
| CY2009 | amount | 537 | 0 |  .  657; 1,000 73; 2,000 42; 150,000 42 |
| CY2014 | other | 547 | 0 | nan 646; 1000 71; 150000 44; 15000 38 |
| COMPUTED_REGION_DQJC_K29Y | category | 30 | 0 | 17 318; 19 169; 20 160; nan 149 |
| COMPUTED_REGION_5PHJ_CC35 | other | 75 | 0 | 71 184; nan 149; 49 113; 68 102 |
| COMPUTED_REGION_MFUY_BEE2 | category | 42 | 0 | nan 149; 34 128; 19 120; 4 110 |
| COMPUTED_REGION_5D9V_6BUI | category | 30 | 0 | 26 349; 5 205; nan 149; 8 128 |
| CY2011 | other | 569 | 0 | nan 640; 1000 72; 150000 55; 2000 41 |
| CY2012 | other | 561 | 0 | nan 635; 1000 73; 150000 54; 2000 40 |
| CY2013 | other | 548 | 0 | nan 658; 1000 69; 150000 53; 200000 44 |
| CY2010 | other | 583 | 0 | nan 630; 1000 82; 150000 46; 200000 37 |
| CY1998 | other | 460 | 0 | nan 697; 1000 101; 150000 59; 200000 41 |
| COMPUTED_REGION_QMWN_IMPY | other | 109 | 0 | nan 981; 220 120; 180 43; 148 36 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:11.77836 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 62187942-4eff-4694-8d3b-2 2.0K |
| SRC_SHA256 | who | 1 | 0 | 11cfe51becd7e4de3b115b2d8 2.0K |
