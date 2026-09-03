# PORTAL_SOC_UTAH_OPEN_DATA_P_F023097D74

rows 2.0K  columns 29  scan 4.1s

roles: amount 5, audit 2, category 4, date 1, other 16, who 2

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1998 | 2.0K | -18.82M | 20.0K | 56.72M | 574.56M | 6.36B |
| CY1999 | 2.0K | -34.53M | 25.0K | 56.73M | 590.95M | 6.50B |
| CY2002 | 2.0K | -4.18M | 25.0K | 57.49M | 498.85M | 6.69B |
| CY2005 | 2.0K | -7.29M | 35.0K | 65.94M | 388.18M | 8.19B |
| CY2009 | 2.0K | -6.87M | 30.0K | 71.82M | 452.84M | 8.35B |

## who

LOCATION_1 by rows
       165  {"latitude": "40.758478", "longitude": "-111.888142", "human_address":
        41  {"latitude": "40.233677", "longitude": "-111.663926", "human_address":
        32  {"latitude": "39.359772", "longitude": "-111.584173", "human_address":
        31  {"latitude": "40.295836", "longitude": "-111.694436", "human_address":
        30  {"latitude": "40.569705", "longitude": "-111.897282", "human_address":
        29  {"latitude": "41.222761", "longitude": "-111.970419", "human_address":
        23  {"human_address": "{\"address\": \"\", \"city\": \"Hill Air Force Base
        22  {"latitude": "40.696682", "longitude": "-111.959172", "human_address":
        21  {"latitude": "41.060161", "longitude": "-111.966274", "human_address":
        20  {"latitude": "40.610919", "longitude": "-111.938765", "human_address":
        19  {"latitude": "37.677344", "longitude": "-113.061742", "human_address":
        19  {"latitude": "37.108284", "longitude": "-113.583277", "human_address":
        17  {"latitude": "40.653066", "longitude": "-111.955295", "human_address":
        16  {"latitude": "41.735211", "longitude": "-111.834857", "human_address":
        16  {"latitude": "40.616306", "longitude": "-111.810524", "human_address":
        15  {"latitude": "38.279582", "longitude": "-112.641291", "human_address":
        15  {"latitude": "40.685351", "longitude": "-111.871404", "human_address":
        14  {"latitude": "40.921499", "longitude": "-111.878961", "human_address":
        13  {"latitude": "39.629733", "longitude": "-111.439223", "human_address":
        13  {"latitude": "40.562242", "longitude": "-111.938666", "human_address":

LOCATION_1 by dollars
       1.44B      165 rows  {"latitude": "40.758478", "longitude": "-111.888142", "human
     446.45M       11 rows  {"latitude": "40.656114", "longitude": "-111.886241", "human
     435.86M       17 rows  {"latitude": "40.653066", "longitude": "-111.955295", "human
     307.29M        6 rows  {"latitude": "40.71786", "longitude": "-111.882616", "human_
     291.68M       16 rows  {"latitude": "40.616306", "longitude": "-111.810524", "human
     274.32M       21 rows  {"latitude": "41.060161", "longitude": "-111.966274", "human
     269.94M       30 rows  {"latitude": "40.569705", "longitude": "-111.897282", "human
     235.65M       31 rows  {"latitude": "40.295836", "longitude": "-111.694436", "human
     227.15M        7 rows  {"latitude": "41.182613", "longitude": "-112.006723", "human
     194.05M       19 rows  {"latitude": "37.108284", "longitude": "-113.583277", "human
     190.42M       29 rows  {"latitude": "41.222761", "longitude": "-111.970419", "human
     155.96M       12 rows  {"latitude": "40.666615", "longitude": "-111.829228", "human
     154.92M        8 rows  {"latitude": "40.52505", "longitude": "-111.864203", "human_
     134.19M       16 rows  {"latitude": "41.735211", "longitude": "-111.834857", "human
     106.70M       41 rows  {"latitude": "40.233677", "longitude": "-111.663926", "human
      99.89M       20 rows  {"latitude": "40.610919", "longitude": "-111.938765", "human
      97.29M       14 rows  {"latitude": "40.921499", "longitude": "-111.878961", "human
      75.59M       13 rows  {"latitude": "40.506311", "longitude": "-111.411672", "human
      68.53M        9 rows  {"latitude": "41.191869", "longitude": "-111.969659", "human
      66.85M       22 rows  {"latitude": "40.696682", "longitude": "-111.959172", "human

SRC_SHA256 by rows
      2.0K  d51d27f80835ab1dcb244e85bd678826fa14f2e5e879a6e99f2e7ac989d60aa2

SRC_SHA256 by dollars
       6.50B     2.0K rows  d51d27f80835ab1dcb244e85bd678826fa14f2e5e879a6e99f2e7ac989d6

## who x when

LOCATION_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY1999

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY1999
  d51d27f80835ab1dcb244e85bd678826fa14f2e5  2026:6.50B

## what

COUNTY: Salt Lake 29%, Utah 13%, Washington 10%, Weber 7%, Cache 7%, Box Elder 7%, Davis 6%, Sanpete 5%, Duchesne 4%, Emery 4%, Sevier 4%, Iron 4%

NAICS_MAJOR_SECTOR: INFORMATION(510000-519999) 12%, PRIOR-PERIOD PAYMENTS & REFUND 10%, MANUFACTURING(310000-339999) 9%, RETAIL-MISCELLANEOUS RETAIL TR 9%, PROFESSIONAL, SCIENTIFIC, & TE 8%, ARTS, ENTERTAINMENT,AND RECREA 8%, NONSTORE RETAILERS(454000-4549 8%, OTHER SERVICES-EXECPT PUBLIC A 8%, RETAIL-ELECTRONICS & APPLIANCE 7%, CONSTRUCTION(230000-239999) 7%, REAL ESTATE, RENTAL, & LEASING 7%, FOOD SERVICES & DRINKING PLACE 7%

COMPUTED_REGION_DQJC_K29Y: 17 24%, 19 11%, 12 11%, 20 11%, 21 10%, 9 9%, 18 7%, 22 4%, 10 3%, 8 3%, 11 3%, 5 3%

COMPUTED_REGION_5D9V_6BUI: 26 26%, 5 14%, 8 9%, 3 8%, 22 7%, 6 7%, 16 7%, 14 6%, 27 5%, 17 4%, 12 4%, 15 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_1 | who | 270 | 0 | {"latitude": "40.758478", 165; {"latitude": "40.233677", 41; {"latitude": "39.359772", 32; {"latitude": "40.295836", 31 |
| COUNTY | category | 34 | 0 | Salt Lake 409; Utah 178; Washington 135; Weber 96 |
| NAICS_MAJOR_SECTOR | category | 37 | 0 | INFORMATION(510000-519999 113; PRIOR-PERIOD PAYMENTS & R 91; MANUFACTURING(310000-3399 84; RETAIL-MISCELLANEOUS RETA 84 |
| CY1998 | amount | 459 | 0 |  .  707; 1,000 68; 150,000 52; 15,000 43 |
| CY1999 | amount | 461 | 0 |  .  690; 1,000 62; 150,000 51; 200,000 45 |
| CY2000 | other | 464 | 0 | nan 668; 1000 88; 150000 47; 200000 44 |
| CY2001 | other | 472 | 0 | nan 680; 1000 67; 150000 55; 2000 45 |
| CY2002 | amount | 465 | 0 |  .  666; 1,000 82; 150,000 66; 2,000 44 |
| CY2003 | other | 474 | 0 | nan 604; 1000 92; 150000 53; 2000 51 |
| CY2004 | other | 500 | 0 | nan 598; 1000 86; 150000 54; 2000 49 |
| CY2005 | amount | 505 | 0 |  .  606; 1,000 93; 2,000 54; 150,000 51 |
| CY2006 | other | 498 | 0 | nan 622; 1000 79; 150000 52; 2000 48 |
| CY2007 | other | 537 | 0 | nan 609; 1000 77; 2000 52; 150000 38 |
| CY2008 | other | 530 | 0 | nan 607; 1000 90; 2000 52; 150000 47 |
| CY2009 | amount | 537 | 0 |  .  611; 1,000 75; 150,000 50; 2,000 46 |
| CY2010 | other | 576 | 0 | nan 574; 1000 86; 150000 55; 20000 46 |
| CY2011 | other | 557 | 0 | nan 569; 1000 86; 150000 60; 15000 52 |
| CY2012 | other | 544 | 0 | nan 538; 1000 80; 150000 52; 15000 49 |
| CY2013 | other | 537 | 0 | nan 558; 1000 74; 150000 59; 15000 44 |
| CY2014 | other | 546 | 0 | nan 570; 1000 79; 150000 46; 200000 39 |
| COMPUTED_REGION_9P4X_9CJT | other | 139 | 0 | 356 165; 44 46; 159 44; 40 41 |
| COMPUTED_REGION_DQJC_K29Y | category | 29 | 0 | 17 373; 19 176; 12 176; 20 168 |
| COMPUTED_REGION_5PHJ_CC35 | other | 58 | 0 | 71 174; 19 165; 54 133; 68 124 |
| COMPUTED_REGION_5D9V_6BUI | category | 30 | 0 | 26 386; 5 203; 8 135; 3 111 |
| ESTIMATED_POPULATION | other | 229 | 0 | 189314 165; nan 159; 115919 41; 90749 31 |
| COMPUTED_REGION_QMWN_IMPY | other | 199 | 0 | nan 269; 220 165; 204 41; 120 40 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:46.35107 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 087b4350-596d-4834-bec3-d 2.0K |
| SRC_SHA256 | who | 1 | 0 | d51d27f80835ab1dcb244e85b 2.0K |
