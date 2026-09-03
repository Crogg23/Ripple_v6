# PORTAL_SOC_UTAH_OPEN_DATA_P_AA199B616A

rows 5.0K  columns 23  scan 4.3s

roles: amount 17, audit 2, category 2, date 1, who 2

## when

INGESTED_AT
  2026      5.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CY1998 | 5.0K | -2.65M | 20.0K | 67.30M | 574.56M | 17.84B |
| CY1999 | 5.0K | -34.53M | 25.0K | 67.58M | 590.95M | 18.39B |
| CY2000 | 5.0K | -3.09M | 25.0K | 73.16M | 553.49M | 19.17B |
| CY2001 | 5.0K | -7.19M | 30.0K | 73.09M | 632.62M | 19.41B |
| CY2002 | 5.0K | -5.46M | 30.0K | 69.21M | 656.82M | 19.42B |
| CY2003 | 5.0K | -4.81M | 30.0K | 71.52M | 525.26M | 19.26B |

## who

LOCATION_1 by rows
        30  {"latitude": "40.10587998500006", "longitude": "-111.65030968199994", 
        28  {"latitude": "40.76077659400005", "longitude": "-111.88424912299996", 
        27  {"latitude": "40.39478809000008", "longitude": "-111.79577612099996", 
        27  {"latitude": "38.76948664300005", "longitude": "-112.07845783299996", 
        27  {"latitude": "40.55690893600007", "longitude": "-112.298606227", "huma
        26  {"latitude": "40.55808643200004", "longitude": "-111.82957591799999", 
        26  {"latitude": "40.72696810600007", "longitude": "-111.53960763099997", 
        26  {"latitude": "41.086217506000025", "longitude": "-112.06638740799997",
        26  {"latitude": "40.69013983900004", "longitude": "-111.99896595799999", 
        26  {"latitude": "40.231859074000056", "longitude": "-111.64507829499996",
        25  {"latitude": "41.18516631600005", "longitude": "-111.94789910799994", 
        25  {"latitude": "41.72839628400004", "longitude": "-111.83498979499996", 
        25  {"latitude": "39.71148818100005", "longitude": "-111.83322572299994", 
        25  {"latitude": "40.70412641200005", "longitude": "-111.81487676499995", 
        25  {"latitude": "40.595488240000066", "longitude": "-111.96099929999997",
        25  {"latitude": "40.92534802200004", "longitude": "-111.88019957799997", 
        25  {"latitude": "40.986347554000076", "longitude": "-111.89954788699998",
        25  {"latitude": "40.661658328000044", "longitude": "-111.88116851399997",
        24  {"latitude": "40.04524977800003", "longitude": "-111.66534774599995", 
        24  {"latitude": "38.273908351000046", "longitude": "-112.64125770599998",

LOCATION_1 by dollars
       1.09B       28 rows  {"latitude": "40.76077659400005", "longitude": "-111.8842491
     988.14M       19 rows  {"latitude": "40.57814732300005", "longitude": "-111.8855395
     986.35M       23 rows  {"latitude": "40.715458186000035", "longitude": "-111.888329
     720.29M       22 rows  {"latitude": "41.16668700800005", "longitude": "-111.9733478
     719.46M       25 rows  {"latitude": "40.661658328000044", "longitude": "-111.881168
     695.41M       24 rows  {"latitude": "40.69923828100008", "longitude": "-111.9487767
     656.51M        4 rows  {"human_address": "{\"address\": \"\", \"city\": \"\", \"sta
     522.10M       21 rows  {"latitude": "40.617148092000036", "longitude": "-111.883749
     467.52M       21 rows  {"latitude": "40.23455732300005", "longitude": "-111.6778396
     454.20M       20 rows  {"latitude": "40.746577116000026", "longitude": "-111.939078
     452.88M       24 rows  {"latitude": "40.76060713900006", "longitude": "-111.8973580
     434.68M       21 rows  {"latitude": "37.115977420000036", "longitude": "-113.600795
     432.42M       22 rows  {"latitude": "40.28155724700008", "longitude": "-111.7067165
     403.84M       20 rows  {"latitude": "40.66343978100008", "longitude": "-111.9214076
     402.57M       18 rows  {"latitude": "40.314427214000034", "longitude": "-111.706507
     382.47M       25 rows  {"latitude": "40.595488240000066", "longitude": "-111.960999
     369.18M       23 rows  {"latitude": "41.26585741300005", "longitude": "-111.9880599
     358.43M       26 rows  {"latitude": "40.69013983900004", "longitude": "-111.9989659
     342.52M       25 rows  {"latitude": "41.72839628400004", "longitude": "-111.8349897
     309.61M       27 rows  {"latitude": "40.39478809000008", "longitude": "-111.7957761

SRC_SHA256 by rows
      5.0K  846a2b1a03cb3ed8ff4c4ef5528b1f9b2bf35f6d48843270e8e7492c79acea29

SRC_SHA256 by dollars
      19.42B     5.0K rows  846a2b1a03cb3ed8ff4c4ef5528b1f9b2bf35f6d48843270e8e7492c79ac

## who x when

LOCATION_1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CY2002
  846a2b1a03cb3ed8ff4c4ef5528b1f9b2bf35f6d  2026:19.42B

## what

NAICS_MAJOR_SECTOR: PRIOR-PERIOD PAYMENTS & REFUND 13%, INFORMATION(510000-519999) 10%, MANUFACTURING(310000-339999) 9%, RETAIL-MISCELLANEOUS RETAIL TR 9%, OTHER SERVICES-EXECPT PUBLIC A 8%, FOOD SERVICES & DRINKING PLACE 8%, NONSTORE RETAILERS(454000-4549 8%, PROFESSIONAL, SCIENTIFIC, & TE 7%, RETAIL-FOOD & BEVERAGE STORES( 7%, WHOLESALE TRADE-DURABLE GOODS( 7%, REAL ESTATE, RENTAL, & LEASING 7%, CONSTRUCTION(230000-239999) 7%

COMPUTED_REGION_9Z68_3KQ5: 3176 28%, 3182 14%, 901 9%, 2986 8%, 811 8%, 3201 7%, 900 6%, 2985 6%, 3178 5%, 3179 5%, 2989 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOCATION_1 | who | 472 | 0 | {"latitude": "40.55690893 31; {"latitude": "40.10587998 31; {"latitude": "40.51054772 30; {"latitude": "40.66165832 30 |
| NAICS_MAJOR_SECTOR | category | 37 | 0 | PRIOR-PERIOD PAYMENTS & R 291; INFORMATION(510000-519999 218; MANUFACTURING(310000-3399 206; RETAIL-MISCELLANEOUS RETA 192 |
| CY1998 | amount | 1.1K | 0 |  .  1.8K; 1,000 186; 150,000 142; 2,000 99 |
| CY1999 | amount | 1.1K | 0 |  .  1.7K; 1,000 183; 150,000 135; 2,000 102 |
| CY2000 | amount | 1.2K | 0 |  .  1.7K; 1,000 195; 150,000 129; 2,000 84 |
| CY2001 | amount | 1.1K | 0 |  .  1.7K; 1,000 169; 150,000 121; 200,000 90 |
| CY2002 | amount | 1.2K | 0 |  .  1.7K; 1,000 157; 150,000 120; 2,000 99 |
| CY2003 | amount | 1.2K | 0 |  .  1.6K; 1,000 187; 150,000 122; 15,000 97 |
| CY2004 | amount | 1.3K | 0 |  .  1.6K; 1,000 195; 150,000 123; 2,000 97 |
| CY2005 | amount | 1.3K | 0 |  .  1.5K; 1,000 196; 2,000 110; 150,000 110 |
| CY2006 | amount | 1.3K | 0 |  .  1.6K; 1,000 152; 150,000 110; 2,000 100 |
| CY2007 | amount | 1.3K | 0 |  .  1.5K; 1,000 162; 150,000 116; 2,000 94 |
| CY2008 | amount | 1.2K | 0 |  .  1.5K; 1,000 199; 150,000 118; 200,000 97 |
| CY2009 | amount | 1.3K | 0 |  .  1.6K; 1,000 181; 150,000 114; 15,000 105 |
| CY2010 | amount | 1.4K | 0 |  .  1.5K; 1,000 178; 150,000 104; 15,000 100 |
| CY2011 | amount | 1.3K | 0 |  .  1.5K; 1,000 172; 15,000 113; 150,000 112 |
| CY2012 | amount | 1.3K | 0 |  .  1.5K; 1,000 179; 150,000 108; 200,000 92 |
| CY2013 | amount | 1.3K | 0 |  .  1.5K; 1,000 157; 150,000 118; 200,000 103 |
| CY2014 | amount | 1.3K | 0 |  .  1.6K; 1,000 146; 150,000 126; 2,000 85 |
| COMPUTED_REGION_9Z68_3KQ5 | category | 30 | 289 | 3176 939; 3182 481; 901 311; 2986 268 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:46:49.68894 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b33bf582-c162-423e-abaf-5 5.0K |
| SRC_SHA256 | who | 1 | 0 | 846a2b1a03cb3ed8ff4c4ef55 5.0K |
