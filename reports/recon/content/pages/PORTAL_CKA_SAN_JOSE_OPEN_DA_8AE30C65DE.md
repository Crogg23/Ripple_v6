# PORTAL_CKA_SAN_JOSE_OPEN_DA_8AE30C65DE

rows 10.0K  columns 14  scan 4.6s

roles: amount 2, audit 2, category 2, date 3, id 3, other 1, who 2

## when

LASTUPDATE
  2005      9.9K  ##############################
  2006        28  
  2007         7  
  2008         5  
  2009         5  
  2011        43  
  2013         2  
  2015        12  
  2016         2  
  2018         3  
  2020         1  
  2021         5  

CREATIONDATE
  1900     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 10.0K | 10.99 | 142.91 | 567.79 | 1.4K | 1.72M |
| SHAPE_AREA | 10.0K | 5.18 | 1.1K | 11.3K | 120.2K | 17.31M |

## who

PARCELID by rows
       210  585577
       190  579440
       128  523643
       112  579565
       112  576183
       112  1005326
       107  1001755
       100  369106
       100  579562
        98  6212894
        96  533462
        93  1001554
        92  580894
        88  576419
        88  579483
        87  392858
        84  580153
        83  579827
        81  579829
        80  582854

PARCELID by dollars
       27.6K      210 rows  585577
       25.1K      190 rows  579440
       19.6K       96 rows  533462
       19.0K       55 rows  523691
       18.4K      128 rows  523643
       18.3K       87 rows  392858
       17.9K       48 rows  523693
       17.0K       79 rows  568074
       16.6K       80 rows  582854
       16.1K      112 rows  576183
       15.6K       98 rows  6212894
       15.5K      112 rows  579565
       15.4K       75 rows  581603
       15.3K       84 rows  580153
       14.5K      112 rows  1005326
       14.4K       92 rows  580894
       14.0K      107 rows  1001755
       13.9K      100 rows  579562
       13.9K      100 rows  369106
       13.6K       71 rows  7395838

SRC_SHA256 by rows
     10.0K  89b98429e43cd80370aac3e1cf799d62732cde45b63c321e9234df0fab913492

SRC_SHA256 by dollars
       1.72M    10.0K rows  89b98429e43cd80370aac3e1cf799d62732cde45b63c321e9234df0fab91

## who x when

PARCELID by LASTUPDATE, dollars = SHAPE_LENGTH
  1001554                                   2005:12.0K
  1001755                                   2005:14.0K
  1005326                                   2005:14.5K
  369106                                    2005:13.9K
  392858                                    2005:18.3K
  523643                                    2005:18.4K
  523691                                    2005:18.7K 2021:377.29
  523693                                    2005:16.7K 2013:834.23 2021:369.93
  533462                                    2005:19.6K
  568074                                    2005:17.0K
  576183                                    2005:16.1K
  576419                                    2005:10.7K
  579440                                    2005:25.1K
  579483                                    2005:11.7K
  579562                                    2005:13.9K
  579565                                    2005:15.5K
  579827                                    2005:10.1K
  579829                                    2005:9.7K
  580153                                    2005:15.3K
  580894                                    2005:14.4K
  581603                                    2005:15.4K
  582854                                    2005:16.6K
  585577                                    2005:27.6K
  6212894                                   2005:15.6K
  7395838                                   2005:13.6K

SRC_SHA256 by LASTUPDATE, dollars = SHAPE_LENGTH
  89b98429e43cd80370aac3e1cf799d62732cde45  2005:1.70M 2006:3.5K 2007:1.8K 2008:571.21 2009:694.42 2011:6.6K 2013:834.23 2015:1.9K 2016:627.84 2018:928.73 2020:185.66 2021:1.2K

## what

PLANMOD: 3-16889 55%, T-9671 15%, APNU_20061208 11%, APNU_20080108 10%, 3-11452 9%, APNU_20070104 1%, T-9352 0%, MGE 0%, T-9668A 0%, 3-16311 0%, APNU_20091020 0%

NOTES: Distance only. 99%, Street name match + Distance. 0%, ParcelID was populated via spa 0%, APNU_20080108 0%, SW HD 50086 0%, Building 1 0%, Building 2A 0%, Building 2B 0%, BLDG. 20B, Unit 8 0%, BLDG. 20C, Unit 10 0%, BLDG. 20D, Unit 15 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 10.0K | 0 | 10494 50; 10493 50; 10492 50; 10491 50 |
| INTID | id | 9.9K | 0 | 8546082 50; 8546081 50; 8546080 50; 8546079 50 |
| PARCELID | who | 825 | 0 | 585577 210; 579440 190; 523643 128; 1001755 117 |
| CONDOPARCELID | id | 9.9K | 0 | 8546082 50; 8546081 50; 8546080 50; 8546079 50 |
| PLANCRT | other | 284 | 0 | MGE 551; T-7903 360; T-6320 300; T-7467 232 |
| PLANMOD | category | 12 | 3.4K | 3-16889 3.6K; T-9671 978; APNU_20061208 711; APNU_20080108 653 |
| LASTUPDATE | date | 105 | 0 | 2005-10-25T12:22:05 9.9K; 2015-01-13T12:45:13 2; 2011-01-07T09:31:50 2; 2011-01-07T09:32:00 2 |
| NOTES | category | 12 | 3.1K | Distance only. 6.8K; Street name match + Dista 31; ParcelID was populated vi 5; APNU_20080108 5 |
| SHAPE_LENGTH | amount | 10.1K | 0 | 149.498128320462 50; 144.621552164168 50; 148.892475703236 50; 161.552561615192 50 |
| SHAPE_AREA | amount | 10.0K | 0 | 1021.9717056551 50; 916.06437767073 50; 969.238164947169 50; 1100.67957594399 50 |
| CREATIONDATE | date | 1 | 0 | 1900-01-01T00:00:00 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:34:49.44918 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c93cc352-60b0-45b5-b6b0-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | 89b98429e43cd80370aac3e1c 10.0K |
