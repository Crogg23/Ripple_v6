# PORTAL_SOC_UTAH_OPEN_DATA_P_F8E4EC438D

rows 2.0K  columns 23  scan 3.9s

roles: amount 17, audit 2, category 2, date 1, who 2

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1998 | 2.0K | -490.8K | 10.0K | 60.35M | 569.59M | 6.14B |
| CY1999 | 2.0K | -34.53M | 15.0K | 60.17M | 525.18M | 6.29B |
| CY2000 | 2.0K | -851.1K | 15.0K | 60.92M | 524.39M | 6.72B |
| CY2001 | 2.0K | -7.19M | 15.0K | 58.24M | 632.62M | 7.24B |
| CY2002 | 2.0K | -1.92M | 15.0K | 57.47M | 656.82M | 7.05B |
| CY2003 | 2.0K | -4.81M | 20.0K | 57.90M | 445.42M | 6.79B |

## who

LOCATION_1 by rows
        17  {"human_address": "{\"address\": \"\", \"city\": \"\", \"state\": \"\"
        14  {"latitude": "41.086217506000025", "longitude": "-112.06638740799997",
        13  {"latitude": "37.02663976200006", "longitude": "-112.47065975499999", 
        13  {"latitude": "40.69955981100003", "longitude": "-112.08458863599998", 
        12  {"latitude": "40.715458186000035", "longitude": "-111.88832908299997",
        12  {"latitude": "40.28155724700008", "longitude": "-111.70671654299997", 
        12  {"latitude": "41.085487545000035", "longitude": "-111.92917647999997",
        12  {"latitude": "40.30802702100004", "longitude": "-110.00722847199995", 
        12  {"latitude": "40.507819064000046", "longitude": "-112.02591802699999",
        12  {"latitude": "40.131828358000064", "longitude": "-111.58224951499994",
        12  {"latitude": "40.595488240000066", "longitude": "-111.96099929999997",
        11  {"latitude": "40.617148092000036", "longitude": "-111.88374944699996",
        11  {"latitude": "39.66834662100007", "longitude": "-110.85471744899996", 
        11  {"latitude": "40.55907709300004", "longitude": "-111.95522913199994", 
        11  {"latitude": "40.70412641200005", "longitude": "-111.81487676499995", 
        11  {"human_address": "{\"address\": \"\", \"city\": \"\", \"state\": \"\"
        11  {"latitude": "40.73719624900008", "longitude": "-111.86156819399997", 
        11  {"latitude": "41.72839628400004", "longitude": "-111.83498979499996", 
        10  {"latitude": "40.03484783500005", "longitude": "-111.72960603199999", 
        10  {"latitude": "41.216128825000055", "longitude": "-111.99699766999998",

LOCATION_1 by dollars
     565.35M       12 rows  {"latitude": "40.715458186000035", "longitude": "-111.888329
     453.03M        7 rows  {"latitude": "38.273908351000046", "longitude": "-112.641257
     339.26M        9 rows  {"latitude": "40.661658328000044", "longitude": "-111.881168
     276.03M        4 rows  {"human_address": "{\"address\": \"\", \"city\": \"\", \"sta
     273.91M       12 rows  {"latitude": "40.28155724700008", "longitude": "-111.7067165
     248.50M       11 rows  {"latitude": "41.72839628400004", "longitude": "-111.8349897
     217.37M        6 rows  {"latitude": "40.39478809000008", "longitude": "-111.7957761
     208.01M       10 rows  {"latitude": "41.07592853300008", "longitude": "-111.9775059
     196.51M        6 rows  {"latitude": "40.66082843200007", "longitude": "-111.4982257
     162.67M        8 rows  {"latitude": "37.115977420000036", "longitude": "-113.600795
     159.57M        7 rows  {"latitude": "40.57814732300005", "longitude": "-111.8855395
     152.82M        6 rows  {"latitude": "37.08085674100005", "longitude": "-113.5584362
     146.94M        6 rows  {"latitude": "40.69013983900004", "longitude": "-111.9989659
     142.64M       10 rows  {"latitude": "41.216128825000055", "longitude": "-111.996997
     135.42M       11 rows  {"latitude": "40.617148092000036", "longitude": "-111.883749
     129.50M        5 rows  {"latitude": "40.314427214000034", "longitude": "-111.706507
     121.47M       10 rows  {"latitude": "40.69923828100008", "longitude": "-111.9487767
     109.80M       11 rows  {"latitude": "40.70412641200005", "longitude": "-111.8148767
     109.22M        6 rows  {"latitude": "40.626537649000056", "longitude": "-111.822037
     104.91M        6 rows  {"latitude": "41.16668700800005", "longitude": "-111.9733478

SRC_SHA256 by rows
      2.0K  65e7acee0a8300825005e6e382642c116f2be3a4aae7bea54559880b553ddf11

SRC_SHA256 by dollars
       6.79B     2.0K rows  65e7acee0a8300825005e6e382642c116f2be3a4aae7bea54559880b553d

## who x when

LOCATION_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2003

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2003
  65e7acee0a8300825005e6e382642c116f2be3a4  2026:6.79B

## what

NAICS_MAJOR_SECTOR: PRIOR-PERIOD PAYMENTS & REFUND 16%, INFORMATION(510000-519999) 10%, FOOD SERVICES & DRINKING PLACE 10%, RETAIL-MISCELLANEOUS RETAIL TR 9%, OTHER SERVICES-EXECPT PUBLIC A 8%, MANUFACTURING(310000-339999) 8%, NONSTORE RETAILERS(454000-4549 7%, RETAIL-FOOD & BEVERAGE STORES( 7%, RETAIL-BUILD. MATERIAL, GARDEN 6%, REAL ESTATE, RENTAL, & LEASING 6%, ARTS, ENTERTAINMENT,AND RECREA 6%, RETAIL-SPORTING GOODS, HOBBY,  6%

COMPUTED_REGION_9Z68_3KQ5: 3176 24%, nan 19%, 3182 11%, 901 8%, 2986 7%, 811 6%, 3201 5%, 2985 5%, 3178 4%, 900 4%, 2989 4%, 2990 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_1 | who | 457 | 0 | {"human_address": "{\"add 17; {"latitude": "41.08621750 15; {"latitude": "41.08548754 14; {"latitude": "37.02663976 14 |
| NAICS_MAJOR_SECTOR | category | 37 | 0 | PRIOR-PERIOD PAYMENTS & R 159; INFORMATION(510000-519999 101; FOOD SERVICES & DRINKING  94; RETAIL-MISCELLANEOUS RETA 90 |
| CY1998 | amount | 461 | 0 |  .  770; 1,000 73; 150,000 46; 200,000 40 |
| CY1999 | amount | 440 | 0 |  .  746; 1,000 73; 150,000 56; 2,000 42 |
| CY2000 | amount | 455 | 0 |  .  749; 1,000 84; 150,000 49; 200,000 41 |
| CY2001 | amount | 461 | 0 |  .  767; 1,000 65; 150,000 44; 15,000 40 |
| CY2002 | amount | 458 | 0 |  .  747; 1,000 62; 150,000 53; 2,000 41 |
| CY2003 | amount | 463 | 0 |  .  723; 1,000 79; 150,000 50; 200,000 39 |
| CY2004 | amount | 491 | 0 |  .  689; 1,000 84; 15,000 47; 150,000 43 |
| CY2005 | amount | 492 | 0 |  .  721; 1,000 72; 150,000 42; 15,000 42 |
| CY2006 | amount | 495 | 0 |  .  714; 1,000 51; 150,000 43; 2,000 43 |
| CY2007 | amount | 509 | 0 |  .  694; 1,000 66; 150,000 52; 2,000 43 |
| CY2008 | amount | 505 | 0 |  .  678; 1,000 78; 200,000 40; 150,000 37 |
| CY2009 | amount | 517 | 0 |  .  687; 1,000 75; 150,000 53; 15,000 40 |
| CY2010 | amount | 555 | 0 |  .  686; 1,000 66; 15,000 46; 150,000 37 |
| CY2011 | amount | 514 | 0 |  .  699; 1,000 73; 150,000 40; 15,000 39 |
| CY2012 | amount | 522 | 0 |  .  690; 1,000 62; 20,000 40; 200,000 37 |
| CY2013 | amount | 516 | 0 |  .  718; 1,000 56; 2,000 43; 150,000 41 |
| CY2014 | amount | 530 | 0 |  .  722; 1,000 50; 150,000 48; 2,000 40 |
| COMPUTED_REGION_9Z68_3KQ5 | category | 30 | 0 | 3176 360; nan 289; 3182 167; 901 114 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:40:40.74159 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | fb18df84-b56b-4fb3-a553-d 2.0K |
| SRC_SHA256 | who | 1 | 0 | 65e7acee0a8300825005e6e38 2.0K |
