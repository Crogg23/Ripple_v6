# PORTAL_CKA_VIRGINIA_OPEN_DA_039AACD655

rows 10.0K  columns 64  scan 5.8s

roles: amount 6, audit 2, category 7, date 4, empty 23, id 4, other 11, who 8

## when

DATEUPDATE
  2020      9.9K  ##############################
  2021         7  
  2022         5  
  2023        28  
  2024         4  
  2025         6  
  2026         8  

EFFDATE
  2020     10.0K  ##############################
  2023         1  
  2026         1  

EXPIREDATE

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 10.0K | 11.31M | 11.32M | 11.33M | 11.34M | 113.17B |
| Y | 10.0K | 38.17 | 6.74M | 6.75M | 6.76M | 67.40B |
| LONGITUDE | 10.0K | -79.11 | -79.08 | -79.02 | 38.13 | -790.7K |
| LATITUDE | 10.0K | 38.12 | 38.16 | 38.19 | 38.20 | 381.6K |
| X2 | 10.0K | -8.81M | -8.80M | -8.80M | -8.80M | -88.03B |
| Y2 | 10.0K | 4.60M | 4.60M | 4.61M | 4.61M | 46.02B |

## who

STNAME by rows
       548  BEVERLEY
       329  SPRINGHILL
       257  AUGUSTA
       224  COALTER
       182  CHURCHVILLE
       156  ENGLEWOOD
       150  COMMUNITY
       138  MONTGOMERY
       128  FRONTIER RIDGE
       118  ORANGE
       113  WOODLEE
       112  MADISON
       112  HILLSMERE
       109  NEW
       105  SETH
       104  BARE
       102  MIDDLEBROOK
       100  WAVERLEY
        87  FREDERICK
        86  JOHNSON

STNAME by dollars
       6.20B      548 rows  BEVERLEY
       3.72B      329 rows  SPRINGHILL
       2.91B      257 rows  AUGUSTA
       2.54B      224 rows  COALTER
       2.06B      182 rows  CHURCHVILLE
       1.76B      156 rows  ENGLEWOOD
       1.70B      150 rows  COMMUNITY
       1.56B      138 rows  MONTGOMERY
       1.45B      128 rows  FRONTIER RIDGE
       1.33B      118 rows  ORANGE
       1.28B      113 rows  WOODLEE
       1.27B      112 rows  MADISON
       1.27B      112 rows  HILLSMERE
       1.23B      109 rows  NEW
       1.19B      105 rows  SETH
       1.18B      104 rows  BARE
       1.15B      102 rows  MIDDLEBROOK
       1.13B      100 rows  WAVERLEY
     984.69M       87 rows  FREDERICK
     973.19M       86 rows  JOHNSON

LEGSTNAME by rows
       548  BEVERLEY
       329  SPRINGHILL
       257  AUGUSTA
       224  COALTER
       182  CHURCHVILLE
       156  ENGLEWOOD
       150  COMMUNITY
       138  MONTGOMERY
       128  FRONTIER RIDGE
       118  ORANGE
       113  WOODLEE
       112  MADISON
       112  HILLSMERE
       109  NEW
       105  SETH
       104  BARE
       102  MIDDLEBROOK
       100  WAVERLEY
        87  FREDERICK
        86  JOHNSON

LEGSTNAME by dollars
       6.20B      548 rows  BEVERLEY
       3.72B      329 rows  SPRINGHILL
       2.91B      257 rows  AUGUSTA
       2.54B      224 rows  COALTER
       2.06B      182 rows  CHURCHVILLE
       1.76B      156 rows  ENGLEWOOD
       1.70B      150 rows  COMMUNITY
       1.56B      138 rows  MONTGOMERY
       1.45B      128 rows  FRONTIER RIDGE
       1.33B      118 rows  ORANGE
       1.28B      113 rows  WOODLEE
       1.27B      112 rows  MADISON
       1.27B      112 rows  HILLSMERE
       1.23B      109 rows  NEW
       1.19B      105 rows  SETH
       1.18B      104 rows  BARE
       1.15B      102 rows  MIDDLEBROOK
       1.13B      100 rows  WAVERLEY
     984.69M       87 rows  FREDERICK
     973.19M       86 rows  JOHNSON

ADD_ALIAS by rows
     10.0K  PERMANENT

ADD_ALIAS by dollars
     113.17B    10.0K rows  PERMANENT

INCORMUN by rows
     10.0K  STAUNTON

INCORMUN by dollars
     113.17B    10.0K rows  STAUNTON

## who x when

STNAME by DATEUPDATE, dollars = X
  AUGUSTA                                   2020:2.91B
  BARE                                      2020:1.18B
  BEVERLEY                                  2020:6.18B 2021:11.31M 2025:11.31M
  CHURCHVILLE                               2020:2.03B 2021:22.62M 2022:11.31M
  COALTER                                   2020:2.54B
  COMMUNITY                                 2020:1.70B
  ENGLEWOOD                                 2020:1.76B
  FREDERICK                                 2020:984.69M
  FRONTIER RIDGE                            2020:1.45B
  HILLSMERE                                 2020:1.26B 2023:11.31M
  JOHNSON                                   2020:973.19M
  MADISON                                   2020:1.27B
  MIDDLEBROOK                               2020:1.15B
  MONTGOMERY                                2020:1.56B
  NEW                                       2020:1.23B
  ORANGE                                    2020:1.33B
  SETH                                      2020:1.18B 2025:11.31M
  SPRINGHILL                                2020:3.72B
  WAVERLEY                                  2020:1.13B
  WOODLEE                                   2020:1.28B

LEGSTNAME by DATEUPDATE, dollars = X
  AUGUSTA                                   2020:2.91B
  BARE                                      2020:1.18B
  BEVERLEY                                  2020:6.18B 2021:11.31M 2025:11.31M
  CHURCHVILLE                               2020:2.03B 2021:22.62M 2022:11.31M
  COALTER                                   2020:2.54B
  COMMUNITY                                 2020:1.70B
  ENGLEWOOD                                 2020:1.76B
  FREDERICK                                 2020:984.69M
  FRONTIER RIDGE                            2020:1.45B
  HILLSMERE                                 2020:1.26B 2023:11.31M
  JOHNSON                                   2020:973.19M
  MADISON                                   2020:1.27B
  MIDDLEBROOK                               2020:1.15B
  MONTGOMERY                                2020:1.56B
  NEW                                       2020:1.23B
  ORANGE                                    2020:1.33B
  SETH                                      2020:1.18B 2025:11.31M
  SPRINGHILL                                2020:3.72B
  WAVERLEY                                  2020:1.13B
  WOODLEE                                   2020:1.28B

## what

ADDNUMSUF: A 73%, B 10%, C 6%, D 4%, E 2%, F 2%, I 1%, H 1%, G 1%, J 0%

STNPREDIR: N 40%, W 27%, S 18%, E 14%,  N 0%

STNPOSTYP: ST 49%, AVE 14%, RD 12%, DR 12%, LN 4%, CT 3%, CIR 2%, WAY 2%, BLVD 1%, PL 1%, GRN 0%, TER 0%

ESN: 9 100%, 3 0%, ST 0%

BUILDING: A 18%, B 16%, C 11%, E 10%, D 10%, 100 8%, F 6%, 300 6%, 200 6%, 400 5%, 2 3%

LEGSTNPDIR: N 40%, W 26%, S 18%, E 15%,  N 0%

LEGSTNPOTY: ST 49%, AVE 14%, RD 12%, DR 12%, LN 4%, CT 3%, CIR 2%, WAY 2%, BLVD 1%, PL 1%, GRN 0%, TER 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 10.1K | 0 | 11318097.295 50; 11318050.94 50; 11318050.68 50; 11308928.2697 50 |
| Y | amount | 9.8K | 0 | 6743436.088 50; 6743435.306 50; 6743414.733 50; 6745712.24329 50 |
| LABEL_FLD | other | 1.9K | 0 | A 162; 1 153; B 152; 2 145 |
| PARCEL_IDA | other | 6.9K | 0 | 11633 150; 11317 148; 10068 138; 11310 135 |
| ADD_ALIAS | who | 1 | 0 | PERMANENT 10.0K |
| ADDRESS | id | 9.9K | 0 | 333 LAMBERT ST APT 3 50; 333 LAMBERT ST APT 2 50; 333 LAMBERT ST APT 1 50; 333 YOUNT AVE 50 |
| CITY | who | 1 | 0 | STAUNTON 10.0K |
| FID | id | 10.0K | 0 | 10000 50; 9999 50; 9998 50; 9997 50 |
| DA_ID | other | 1 | 0 | sttnvapd1.stauntoncity.va 10.0K |
| REGSOURCE | empty | 1 | 10.0K |  |
| DATEUPDATE | date | 32 | 0 | 2/19/2020 12:00:00 AM 9.9K; 2/16/2023 12:00:00 AM 12; 2/15/2023 12:00:00 AM 5; 4/12/2023 12:00:00 AM 5 |
| EFFDATE | date | 4 | 0 | 2/10/2020 12:00:00 AM 10.0K; 10/8/2020 12:00:00 AM 1; 10/30/2023 12:00:00 AM 1; 2/19/2026 12:00:00 AM 1 |
| EXPIREDATE | date | 1 | 0 | 12/30/3000 12:00:00 AM 10.0K |
| SITEUNIQID | id | 10.0K | 0 | AP06620@sttnvapd1.staunto 50; AP06619@sttnvapd1.staunto 50; AP06618@sttnvapd1.staunto 50; AP14583@sttnvapd1.staunto 50 |
| COUNTRY | other | 1 | 0 | US 10.0K |
| STATE | other | 1 | 0 | VA 10.0K |
| COUNTY | who | 1 | 0 | AUGUSTA 10.0K |
| ADDCODE | empty | 1 | 10.0K |  |
| ADDDATAURI | empty | 1 | 10.0K |  |
| INCORMUN | who | 1 | 0 | STAUNTON 10.0K |
| UNINCORCOM | empty | 1 | 10.0K |  |
| NEIGHCOM | empty | 1 | 10.0K |  |
| ADDNUMPRE | empty | 1 | 10.0K |  |
| ADDNUMBER | other | 1.1K | 0 | 107 245; 20 189; 21 138; 1701 137 |
| ADDNUMSUF | category | 11 | 9.7K | A 189; B 27; C 15; D 10 |
| STNPREMOD | empty | 1 | 10.0K |  |
| STNPREDIR | category | 6 | 7.9K | N 831; W 564; S 375; E 301 |
| STNPRETYP | empty | 1 | 10.0K |  |
| STNPTYSEP | empty | 1 | 10.0K |  |
| STNAME | who | 381 | 0 | BEVERLEY 548; SPRINGHILL 329; AUGUSTA 257; COALTER 224 |
| STNPOSTYP | category | 20 | 0 | ST 4.8K; AVE 1.4K; RD 1.2K; DR 1.1K |
| STNPOSDIR | empty | 1 | 10.0K |  |
| STNPOSMOD | empty | 1 | 10.0K |  |
| ESN | category | 3 | 0 | 9 10.0K; 3 4; ST 1 |
| MSAGCOM | who | 1 | 0 | STAUNTON 10.0K |
| POSTALCOMN | empty | 1 | 10.0K |  |
| POSTALCODE | other | 1 | 0 | 24401 10.0K |
| ZIPPLUS4 | empty | 1 | 10.0K |  |
| BUILDING | category | 37 | 9.9K | A 11; B 10; C 7; E 6 |
| FLOOR | empty | 1 | 10.0K |  |
| UNIT | other | 692 | 7.4K | A 191; B 184; 2 146; 1 146 |
| ROOM | empty | 1 | 10.0K |  |
| SEAT | empty | 1 | 10.0K |  |
| ADDLOCINFO | empty | 1 | 10.0K |  |
| COMPLANDN | empty | 1 | 10.0K |  |
| MILEPOST | empty | 1 | 10.0K |  |
| PLACETYPE | empty | 1 | 10.0K |  |
| PLMETHOD | empty | 1 | 10.0K |  |
| LONGITUDE | amount | 10.2K | 0 | -79.0732620904 50; -79.0734232636 50; -79.073423752 50; -79.1052042756 50 |
| LATITUDE | amount | 10.1K | 0 | 38.164393747 50; 38.1643905683 50; 38.164334309 50; 38.170482236 50 |
| ELEVATION | other | 1 | 0 | 0 10.0K |
| LEGSTNPDIR | category | 6 | 7.9K | N 831; W 545; S 375; E 301 |
| LEGSTNAME | who | 381 | 0 | BEVERLEY 548; SPRINGHILL 329; AUGUSTA 257; COALTER 224 |
| LEGSTNPOTY | category | 20 | 0 | ST 4.8K; AVE 1.4K; RD 1.2K; DR 1.1K |
| LEGSTPODIR | empty | 1 | 10.0K |  |
| EXCEPTION | empty | 1 | 10.0K |  |
| ID | id | 9.9K | 0 | 10071 50; 10070 50; 10069 50; 10068 50 |
| STNUMBER | other | 1.1K | 0 | 107 245; 20 189; 21 138; 1701 137 |
| STRUCTURE | other | 989 | 7.3K | A 163; B 156; 2 121; 1 119 |
| X2 | amount | 10.2K | 0 | -8802395.59164372 50; -8802413.53347306 50; -8802413.58783429 50; -8805951.38062267 50 |
| Y2 | amount | 10.2K | 0 | 4602676.30662709 50; 4602675.85658299 50; 4602667.8910688 50; 4603538.37794625 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:33:15.00531 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 65e2b78f-e259-4d01-81a4-f 10.0K |
| SRC_SHA256 | who | 1 | 0 | b62d0b8bc76f56036814b1072 10.0K |
