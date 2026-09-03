# PORTAL_SOC_UTAH_OPEN_DATA_P_3CCC1D14AC

rows 5.0K  columns 28  scan 5.1s

roles: amount 17, audit 2, category 3, date 1, other 4, who 2

## when

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1998 | 5.0K | -18.82M | 25.0K | 55.76M | 569.59M | 14.88B |
| CY1999 | 5.0K | -34.53M | 30.0K | 54.88M | 525.18M | 15.19B |
| CY2000 | 5.0K | -16.23M | 30.0K | 60.56M | 524.39M | 16.19B |
| CY2001 | 5.0K | -7.19M | 30.0K | 60.50M | 632.62M | 17.28B |
| CY2002 | 5.0K | -5.46M | 30.0K | 60.30M | 656.82M | 17.29B |
| CY2003 | 5.0K | -6.31M | 35.0K | 63.70M | 525.26M | 17.46B |

## who

LOCATION_1 by rows
        28  {"latitude": "40.505349", "longitude": "-111.950757", "human_address":
        28  {"latitude": "40.737242", "longitude": "-111.535381", "human_address":
        27  {"latitude": "37.125739", "longitude": "-113.496708", "human_address":
        26  {"latitude": "40.393723", "longitude": "-110.198982", "human_address":
        26  {"latitude": "41.842716", "longitude": "-111.895368", "human_address":
        26  {"latitude": "40.571476", "longitude": "-111.861826", "human_address":
        26  {"latitude": "40.180046", "longitude": "-111.566495", "human_address":
        26  {"latitude": "38.626619", "longitude": "-112.096818", "human_address":
        26  {"latitude": "38.328251", "longitude": "-112.586277", "human_address":
        25  {"latitude": "40.406511", "longitude": "-111.867989", "human_address":
        25  {"latitude": "40.503754", "longitude": "-111.870521", "human_address":
        25  {"latitude": "41.69484", "longitude": "-111.815537", "human_address": 
        25  {"latitude": "40.984905", "longitude": "-111.892731", "human_address":
        25  {"latitude": "37.0", "longitude": "-112.97", "human_address": "{\"addr
        25  {"latitude": "38.71854", "longitude": "-111.788562", "human_address": 
        25  {"latitude": "39.503388", "longitude": "-111.483154", "human_address":
        24  {"latitude": "37.209087", "longitude": "-113.220178", "human_address":
        24  {"latitude": "40.379361", "longitude": "-111.74327", "human_address": 
        24  {"latitude": "40.232858", "longitude": "-111.685041", "human_address":
        24  {"latitude": "41.161268", "longitude": "-111.968246", "human_address":

LOCATION_1 by dollars
     948.59M       24 rows  {"latitude": "40.657894", "longitude": "-111.883531", "human
     711.27M       22 rows  {"latitude": "40.700752", "longitude": "-111.950515", "human
     657.30M       19 rows  {"latitude": "40.755889", "longitude": "-111.884326", "human
     656.51M        4 rows  {"latitude": "40.758478", "longitude": "-111.888142", "human
     584.32M       20 rows  {"latitude": "40.577727", "longitude": "-111.887315", "human
     523.76M       26 rows  {"latitude": "38.328251", "longitude": "-112.586277", "human
     511.75M       23 rows  {"latitude": "40.757172", "longitude": "-111.899872", "human
     484.56M       22 rows  {"latitude": "37.144705", "longitude": "-113.676419", "human
     419.38M       19 rows  {"latitude": "40.314542", "longitude": "-111.710522", "human
     414.78M       22 rows  {"latitude": "40.71583", "longitude": "-111.891406", "human_
     394.84M       24 rows  {"latitude": "40.232858", "longitude": "-111.685041", "human
     374.42M       24 rows  {"latitude": "40.747921", "longitude": "-111.954751", "human
     361.50M       24 rows  {"latitude": "41.161268", "longitude": "-111.968246", "human
     335.71M       22 rows  {"latitude": "40.595075", "longitude": "-111.964518", "human
     317.73M       20 rows  {"latitude": "41.07251", "longitude": "-111.981708", "human_
     316.66M       24 rows  {"latitude": "40.200344", "longitude": "-109.464332", "human
     313.90M       24 rows  {"latitude": "41.689169", "longitude": "-111.732518", "human
     301.29M       19 rows  {"latitude": "40.615838", "longitude": "-111.887981", "human
     296.85M       21 rows  {"latitude": "41.21655", "longitude": "-112.012936", "human_
     281.46M       20 rows  {"latitude": "41.273685", "longitude": "-112.026533", "human

SRC_SHA256 by rows
      5.0K  e22335b6959ed6402fac391f66837d19810fe1f29ca02724a04bdf8be335fc52

SRC_SHA256 by dollars
      17.29B     5.0K rows  e22335b6959ed6402fac391f66837d19810fe1f29ca02724a04bdf8be335

## who x when

LOCATION_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002
  e22335b6959ed6402fac391f66837d19810fe1f2  2026:17.29B

## what

NAICS_MAJOR_SECTOR: PRIOR-PERIOD PAYMENTS & REFUND 13%, INFORMATION(510000-519999) 10%, RETAIL-MISCELLANEOUS RETAIL TR 9%, MANUFACTURING(310000-339999) 9%, OTHER SERVICES-EXECPT PUBLIC A 8%, NONSTORE RETAILERS(454000-4549 8%, FOOD SERVICES & DRINKING PLACE 8%, RETAIL-ELECTRONICS & APPLIANCE 8%, PROFESSIONAL, SCIENTIFIC, & TE 7%, CONSTRUCTION(230000-239999) 7%, RETAIL-FOOD & BEVERAGE STORES( 7%, REAL ESTATE, RENTAL, & LEASING 6%

COUNTY: Salt Lake 30%, Utah 14%, Washington 10%, Cache 8%, Weber 8%, Box Elder 6%, Sanpete 6%, Davis 5%, Sevier 5%, Duchesne 4%, Summit 4%

COMPUTED_REGION_DQJC_K29Y: 17 26%, 19 11%, 20 10%, 9 10%, 21 9%, 12 9%, 18 8%, 11 5%, 22 5%, 8 4%, 10 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAICS_MAJOR_SECTOR | category | 37 | 0 | PRIOR-PERIOD PAYMENTS & R 298; INFORMATION(510000-519999 221; RETAIL-MISCELLANEOUS RETA 204; MANUFACTURING(310000-3399 191 |
| CY1998 | amount | 1.1K | 0 |  .  1.7K; 1,000 192; 150,000 147; 200,000 98 |
| CY1999 | amount | 1.1K | 0 |  .  1.7K; 1,000 185; 150,000 139; 2,000 108 |
| CY2000 | amount | 1.1K | 0 |  .  1.7K; 1,000 210; 150,000 128; 200,000 100 |
| CY2001 | amount | 1.2K | 0 |  .  1.7K; 1,000 162; 150,000 129; 2,000 98 |
| CY2002 | amount | 1.1K | 0 |  .  1.7K; 1,000 174; 150,000 141; 15,000 104 |
| CY2003 | amount | 1.2K | 0 |  .  1.6K; 1,000 198; 150,000 124; 2,000 104 |
| CY2004 | amount | 1.2K | 0 |  .  1.5K; 1,000 219; 150,000 127; 15,000 96 |
| CY2005 | amount | 1.3K | 0 |  .  1.6K; 1,000 201; 150,000 112; 2,000 110 |
| CY2006 | amount | 1.2K | 0 |  .  1.6K; 1,000 165; 150,000 113; 2,000 108 |
| CY2007 | amount | 1.3K | 0 |  .  1.5K; 1,000 177; 150,000 112; 2,000 101 |
| CY2008 | amount | 1.3K | 0 |  .  1.5K; 1,000 212; 150,000 108; 2,000 97 |
| CY2009 | amount | 1.3K | 0 |  .  1.5K; 1,000 201; 150,000 129; 2,000 108 |
| CY2010 | amount | 1.4K | 0 |  .  1.5K; 1,000 191; 150,000 115; 200,000 102 |
| CY2011 | amount | 1.3K | 0 |  .  1.5K; 1,000 182; 150,000 123; 15,000 121 |
| CY2012 | amount | 1.3K | 0 |  .  1.4K; 1,000 182; 150,000 138; 200,000 101 |
| CY2013 | amount | 1.3K | 0 |  .  1.5K; 1,000 186; 150,000 127; 200,000 107 |
| CY2014 | amount | 1.3K | 0 |  .  1.5K; 1,000 177; 150,000 131; 2,000 89 |
| LOCATION_1 | who | 444 | 0 | {"latitude": "40.757172", 30; {"latitude": "38.328251", 30; {"latitude": "41.842716", 30; {"latitude": "40.737242", 30 |
| COUNTY | category | 35 | 132 | Salt Lake 1.0K; Utah 478; Washington 340; Cache 287 |
| ESTIMATED_POPULATION | other | 230 | 391 | 189314 393; 115919 113; 89344 78; 83793 75 |
| COMPUTED_REGION_9P4X_9CJT | other | 71 | 2.7K | 44 99; 34 85; 159 84; 118 82 |
| COMPUTED_REGION_DQJC_K29Y | category | 30 | 161 | 17 910; 19 400; 20 368; 9 346 |
| COMPUTED_REGION_5PHJ_CC35 | other | 75 | 161 | 71 459; 68 265; 54 259; 49 258 |
| COMPUTED_REGION_QMWN_IMPY | other | 117 | 2.3K | 220 374; 148 104; 180 93; 204 93 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:46:25.01022 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c1b4d954-32de-4ff7-b3dd-9 5.0K |
| SRC_SHA256 | who | 1 | 0 | e22335b6959ed6402fac391f6 5.0K |
