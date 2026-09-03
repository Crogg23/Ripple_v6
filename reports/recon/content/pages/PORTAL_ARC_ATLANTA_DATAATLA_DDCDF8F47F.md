# PORTAL_ARC_ATLANTA_DATAATLA_DDCDF8F47F

rows 2.0K  columns 34  scan 5.1s

roles: amount 4, audit 2, category 9, date 3, id 2, other 3, who 12

## when

CREATIONDATE
  2024      2.0K  ##############################

EDITDATE
  2024      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EMPNUM | 1.8K | 1 | 4 | 80 | 200 | 14.4K |
| SALESVOL | 1.3K | 28.0K | 599.0K | 16.40M | 179.55M | 2.23B |
| LATITUDE | 2.0K | 33.67 | 33.71 | 33.74 | 33.74 | 67.4K |
| LONGITUDE | 2.0K | -84.54 | -84.45 | -84.40 | -84.40 | -168.9K |

## who

CONAME by rows
        59  ATM
         9  Family Dollar
         8  LibertyX Bitcoin ATM
         7  Metro by T-Mobile Authorized Retailer
         5  American Deli
         5  Subway
         4  Blue Rhino
         4  Chevron
         3  ATC Income Tax
         3  Dollar General
         3  AmeriGas Propane Exchange
         3  Atlanta Board of Education
         3  Allstate Insurance
         3  Church's Texas Chicken
         3  Redbox
         3  AutoZone
         3  CVS Pharmacy
         3  Dollar Tree
         3  ecoATM
         3  Citi Trends

CONAME by dollars
        2.0K       59 rows  ATM
      303.37        9 rows  Family Dollar
      269.69        8 rows  LibertyX Bitcoin ATM
      236.02        7 rows  Metro by T-Mobile Authorized Retailer
      168.60        5 rows  Subway
      168.57        5 rows  American Deli
      134.84        4 rows  Chevron
      134.84        4 rows  Blue Rhino
      101.17        3 rows  Citi Trends
      101.17        3 rows  Redbox
      101.16        3 rows  AmeriGas Propane Exchange
      101.15        3 rows  CVS Pharmacy
      101.15        3 rows  Atlanta Board of Education
      101.15        3 rows  Allstate Insurance
      101.14        3 rows  Dollar Tree
      101.14        3 rows  ATC Income Tax
      101.14        3 rows  Church's Texas Chicken
      101.14        3 rows  Rainbow
      101.13        3 rows  AutoZone
      101.12        3 rows  ecoATM

HQNAME by rows
         9  Metro by T-Mobile
         9  Family Dollar Stores, Inc
         8  NCR Corporation
         8  Chevron Global Downstream LLC
         8  The Kroger Co
         5  Franchise World Headquarters, LLC
         5  American Deli International Inc
         5  The Salvation Army Georgia Division
         5  Shell Oil Products Co LLC
         4  Blue Rhino Global Sourcing, Inc
         4  TMX Finance LLC
         4  Rainbow USA Inc
         3  CITGO Petroleum Corporation
         3  Redbox Automated Retail LLC
         3  International Association of Sheet Metal, Air, Rail, & Transportation 
         3  Allstate Insurance Company
         3  Dollar General Corporation
         3  AutoZone, Inc
         3  Exxon Mobil Downstream
         3  Citi Trends, Inc

HQNAME by dollars
      303.47        9 rows  Metro by T-Mobile
      303.37        9 rows  Family Dollar Stores, Inc
      269.77        8 rows  The Kroger Co
      269.70        8 rows  Chevron Global Downstream LLC
      269.69        8 rows  NCR Corporation
      168.65        5 rows  The Salvation Army Georgia Division
      168.60        5 rows  Franchise World Headquarters, LLC
      168.57        5 rows  American Deli International Inc
      168.55        5 rows  Shell Oil Products Co LLC
      134.84        4 rows  Blue Rhino Global Sourcing, Inc
      134.83        4 rows  Rainbow USA Inc
      134.81        4 rows  TMX Finance LLC
      101.17        3 rows  Citi Trends, Inc
      101.17        3 rows  Redbox Automated Retail LLC
      101.16        3 rows  AmeriGas Propane, Inc
      101.15        3 rows  CVS Pharmacy, Inc
      101.15        3 rows  Allstate Insurance Company
      101.14        3 rows  Cajun Global LLC
      101.14        3 rows  Dollar Tree Stores Inc
      101.13        3 rows  Exxon Mobil Downstream

STATE_NAME by rows
      2.0K  Georgia

STATE_NAME by dollars
       67.4K     2.0K rows  Georgia

SIC_ALL by rows
       110  999977
        74  723106
        63  581208
        59  602103
        58  866107
        42  999966
        30  651303
        27  821103
        25  835101
        22  581208, 581206
        20  729101
        16  874269, 999966
        15  723102
        13  811103
        13  724101
        11  609919
        11  653118
        11  753801
        11  554101, 541103
        10  592102

SIC_ALL by dollars
        3.7K      110 rows  999977
        2.5K       74 rows  723106
        2.1K       63 rows  581208
        2.0K       59 rows  602103
        2.0K       58 rows  866107
        1.4K       42 rows  999966
        1.0K       30 rows  651303
      909.98       27 rows  821103
      842.67       25 rows  835101
      741.74       22 rows  581208, 581206
      674.35       20 rows  729101
      539.37       16 rows  874269, 999966
      505.77       15 rows  723102
      438.21       13 rows  724101
      438.15       13 rows  811103
      370.86       11 rows  653118
      370.81       11 rows  753801
      370.80       11 rows  609919
      370.78       11 rows  554101, 541103
      337.18       10 rows  541105

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  ATC Income Tax                            2024:101.14
  ATM                                       2024:2.0K
  Allstate Insurance                        2024:101.15
  AmeriGas Propane Exchange                 2024:101.16
  American Deli                             2024:168.57
  Atlanta Board of Education                2024:101.15
  AutoZone                                  2024:101.13
  Blue Rhino                                2024:134.84
  CVS Pharmacy                              2024:101.15
  Chevron                                   2024:134.84
  Church's Texas Chicken                    2024:101.14
  Citi Trends                               2024:101.17
  Dollar General                            2024:101.12
  Dollar Tree                               2024:101.14
  Family Dollar                             2024:303.37
  LibertyX Bitcoin ATM                      2024:269.69
  Metro by T-Mobile Authorized Retailer     2024:236.02
  Rainbow                                   2024:101.14
  Redbox                                    2024:101.17
  Subway                                    2024:168.60
  ecoATM                                    2024:101.12

HQNAME by CREATIONDATE, dollars = LATITUDE
  Allstate Insurance Company                2024:101.15
  AmeriGas Propane, Inc                     2024:101.16
  American Deli International Inc           2024:168.57
  AutoZone, Inc                             2024:101.13
  Blue Rhino Global Sourcing, Inc           2024:134.84
  CITGO Petroleum Corporation               2024:101.09
  CVS Pharmacy, Inc                         2024:101.15
  Cajun Global LLC                          2024:101.14
  Chevron Global Downstream LLC             2024:269.70
  Citi Trends, Inc                          2024:101.17
  Dollar General Corporation                2024:101.12
  Dollar Tree Stores Inc                    2024:101.14
  Exxon Mobil Downstream                    2024:101.13
  Family Dollar Stores, Inc                 2024:303.37
  Franchise World Headquarters, LLC         2024:168.60
  International Association of Sheet Metal  2024:101.10
  Metro by T-Mobile                         2024:303.47
  NCR Corporation                           2024:269.69
  Rainbow USA Inc                           2024:134.83
  Redbox Automated Retail LLC               2024:101.17
  Shell Oil Products Co LLC                 2024:168.55
  TMX Finance LLC                           2024:134.81
  The Kroger Co                             2024:269.77
  The Salvation Army Georgia Division       2024:168.65

## what

CITY: Atlanta 95%, East Point 5%

ZIP: 30310 39%, 30311 26%, 30331 20%, 30344 11%, 30315 4%, 39901 0%, 30303 0%

AFFILIATE: Metro by T-Mobile Authorized R 38%, Boost Mobile 31%, Cricket Wireless Authorized Re 6%, Good Neighbor Pharmacy 6%, Metro by T-Mobile Authorized R 6%, YMCA 6%, American Red Cross 6%

BRAND: AMEX ATM 32%, STAR,AMEX ATM 16%, Chevron 9%, LibertyX Bitcoin ATM 9%, Shell 7%, Exxon 6%, State Farm 6%, Citgo 4%, Progressive Insurance 4%, Wells Fargo ATM,AMEX ATM 4%, STAR,AMEX ATM,Bank Of America  3%

LOC_CONF: Very High 87%, High 12%, Medium 0%, Low 0%

PLACETYPE: Independent 85%, Branch 11%, Kiosk 4%, Headquarters 0%

PROFSPEC: General Dentistry 20%, Internal Medicine 13%, Family Practice 13%, Anesthesiology 7%, Pedodontics,General Dentistry, 7%, Criminal Justice 7%, Small Animals 7%, Homeopathy 7%, Ophthalmology 7%, Obstetrics & Gynecology 7%, Pediatrics 7%

SQFOOTAGE: 2,500 - 4,999 26%, 1,500 - 2,499 25%, 1 - 1,499 22%, 5,000 - 9,999 10%, 10,000 - 19,999 8%, 20,000 - 39,999 4%, 40,000 - 99,999 3%, 100,000+ 3%

DESC: CONAME, Atlanta, Georgia 95%, CONAME, East Point, Georgia 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| CONAME | who | 1.8K | 0 | ATM 60; Family Dollar 14; ecoATM 12; Dollar Tree 12 |
| ADDR | who | 343 | 19 | Campbellton Rd SW 268; Greenbriar Pkwy SW 143; Metropolitan Pkwy SW 130; Ralph David Abernathy Blv 125 |
| CITY | category | 2 | 0 | Atlanta 1.9K; East Point 99 |
| STATE_NAME | who | 1 | 0 | Georgia 2.0K |
| STATE | other | 1 | 0 | GA 2.0K |
| ZIP | category | 8 | 3 | 30310 775; 30311 526; 30331 401; 30344 221 |
| ZIP4 | other | 938 | 65 | 2620 43; 2467 21; 1400 15; 2627 14 |
| NAICS | who | 537 | 0 | 99999004 110; 72251117 105; 81211202 87; 81311008 70 |
| NAICS_ALL | who | 921 | 0 | 99999004 110; 81211202 74; 72251117 63; 52211001 59 |
| SIC | who | 536 | 0 | 999977 110; 581208 105; 723106 87; 866107 70 |
| SIC_ALL | who | 931 | 0 | 999977 110; 723106 74; 581208 63; 602103 59 |
| AFFILIATE | category | 8 | 2.0K | Metro by T-Mobile Authori 6; Boost Mobile 5; Cricket Wireless Authoriz 1; Good Neighbor Pharmacy 1 |
| BRAND | category | 34 | 1.9K | AMEX ATM 29; STAR,AMEX ATM 14; Chevron 8; LibertyX Bitcoin ATM 8 |
| HQNAME | who | 133 | 1.8K | Family Dollar Stores, Inc 9; Metro by T-Mobile 9; Chevron Global Downstream 8; NCR Corporation 8 |
| LOC_CONF | category | 4 | 0 | Very High 1.7K; High 243; Medium 9; Low 7 |
| PLACETYPE | category | 4 | 0 | Independent 1.7K; Branch 215; Kiosk 90; Headquarters 2 |
| PROFSPEC | category | 16 | 2.0K | General Dentistry 3; Internal Medicine 2; Family Practice 2; Anesthesiology 1 |
| SQFOOTAGE | category | 9 | 299 | 2,500 - 4,999 436; 1,500 - 2,499 427; 1 - 1,499 374; 5,000 - 9,999 176 |
| EMPNUM | amount | 67 | 0 | 3.0 320; 4.0 269; 2.0 249; nan 202 |
| SALESVOL | amount | 569 | 0 | nan 684; 148000.0 43; 599000.0 40; 737000.0 23 |
| SOURCE | who | 1 | 0 | Data Axle 2.0K |
| ESRI_PID | id | 2.0K | 0 | 6d92f03352d3e69800defec63 10; 112d86f1500b1b613b0390d3b 10; d27795f33044710f1fb88abc7 10; 68da5af374089a9d695f0fc70 10 |
| DESC | category | 2 | 0 | CONAME, Atlanta, Georgia 1.9K; CONAME, East Point, Georg 99 |
| LATITUDE | amount | 1.2K | 0 | 33.69044699993136 79; 33.736724999835715 44; 33.68834100008554 25; 33.68859300012109 24 |
| LONGITUDE | amount | 1.3K | 0 | -84.48963300026446 79; -84.41136899961266 44; -84.4873290003254 25; -84.48865200044831 24 |
| CREATIONDATE | date | 1 | 0 | 1708545288229 2.0K |
| CREATOR | who | 1 | 0 | gpickren2 2.0K |
| EDITDATE | date | 1 | 0 | 1708545288229 2.0K |
| EDITOR | who | 1 | 0 | gpickren2 2.0K |
| GEOMETRY | other | 1.3K | 0 | {"type": "Point", "coordi 79; {"type": "Point", "coordi 44; {"type": "Point", "coordi 25; {"type": "Point", "coordi 24 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:32:43.66223 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 181ff4da-0256-4c0e-8029-c 2.0K |
| SRC_SHA256 | who | 1 | 0 | ddc75f268e523e69559b0f357 2.0K |
