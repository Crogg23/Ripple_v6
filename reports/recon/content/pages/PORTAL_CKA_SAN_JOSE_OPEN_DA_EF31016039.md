# PORTAL_CKA_SAN_JOSE_OPEN_DA_EF31016039

rows 25  columns 21  scan 2.4s

roles: amount 2, audit 2, category 10, date 1, empty 5, other 1, who 1

## when

INGESTED_AT
  2026        25  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 25 | 600.60 | 1.2K | 2.0K | 2.2K | 28.3K |
| SHAPE_AREA | 25 | 16.4K | 68.6K | 155.2K | 160.3K | 1.74M |

## who

SRC_SHA256 by rows
        25  40c5e779aa1f74b0d97332cd0d2546e3879159e0f7d8800abcabd814a509e457

SRC_SHA256 by dollars
       28.3K       25 rows  40c5e779aa1f74b0d97332cd0d2546e3879159e0f7d8800abcabd814a509

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  40c5e779aa1f74b0d97332cd0d2546e3879159e0  2026:28.3K

## what

OBJECTID: 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

FACILITYID: 56 8%, 71 8%, 54 8%, 53 8%, 51 8%, 45 8%, 44 8%, 43 8%, 37 8%, 42 8%, 41 8%, 40 8%

INTID: 56 8%, 71 8%, 54 8%, 53 8%, 51 8%, 45 8%, 44 8%, 43 8%, 37 8%, 42 8%, 41 8%, 40 8%

NAME: Mt. Pleasant Neighborhood Libr 8%, Village Square Branch Library 8%, Educational Park Library 8%, Tully Community Library 8%, Bascom Library 8%, Seven Trees Library 8%, Santa Teresa Library 8%, Rose Garden Library 8%, Dr. Roberto Cruz Alum Rock Lib 8%, Pearl Avenue Library 8%, Hillview Library 8%, Evergreen Library 8%

FULLADDR: 3411 Rocky Mountain Drive 8%, 4001 Evergreen Village Square 8%, 1772 Educational Park Drive 8%, 880 Tully Road 8%, 1000 S. Bascom Avenue 8%, 3590 Cas Drive 8%, 290 International Circle 8%, 1580 Naglee Avenue 8%, 3090 Alum Rock Avenue 8%, 4270 Pearl Avenue 8%, 1600 Hopkins Drive 8%, 2635 Aborn Road 8%

ZIPCODE: 95127 13%, 95111 13%, 95112 13%, 95135 7%, 95133 7%, 95121 7%, 95128 7%, 95119 7%, 95126 7%, 95136 7%, 95122 7%, 95148 7%

CONTACT: Tiffany Bradford-Oldham 12%, Margaret Yamasaki 8%, Mark Giannuzzi 8%, Trina Richbourg 8%, Joan Bowlby 8%, Nancy Donnell 8%, Chieu Nguyen 8%, Oscar Hernandez 8%, Candice Tran 8%, Rebekah Gonzalez 8%, Rachel Gaither 8%, Paul Wilson 4%

PHONE: 408-808-3088 8%, 408-808-3093 8%, 408-808-3073 8%, 408-808-3030 8%, 408-808-3077 8%, 408-808-3056 8%, 408-808-3068 8%, 408-808-3070 8%, 408-808-3090 8%, 408-808-3053 8%, 408-808-3033 8%, 408-808-3060 8%

EMAIL: tiffany.bradford-oldham@sjlibr 12%, margaret.yamasaki@sjlibrary.or 8%, mark.giannuzzi@sjlibrary.org 8%, trina.richbourg@sjlibrary.org 8%, joan.bowlby@sjlibrary.org 8%, nancy.donnell@sjlibrary.org 8%, chieu.nguyen@sjlibrary.org 8%, oscar.hernandez@sjlibrary.org 8%, candice.tran@sjlibrary.org 8%, rebekah.gonzalez@sjlibrary.org 8%, rachel.gaither@sjlibrary.org 8%, paul.wilson@sjlibrary.org 4%

LASTUPDATE: 2022/02/07 19:18:54+00 8%, 2021/05/04 22:08:51+00 8%, 2021/05/04 22:04:30+00 8%, 2022/02/07 19:39:15+00 8%, 2021/05/04 21:56:57+00 8%, 2022/02/07 19:38:36+00 8%, 2021/05/04 22:07:53+00 8%, 2021/05/04 22:07:25+00 8%, 2022/02/07 19:22:25+00 8%, 2022/02/07 19:25:49+00 8%, 2022/02/07 19:25:17+00 8%, 2021/05/04 22:04:44+00 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 25 | 0 | 25 1; 24 1; 23 1; 22 1 |
| FACILITYID | category | 25 | 0 | 56 1; 71 1; 54 1; 53 1 |
| INTID | category | 25 | 0 | 56 1; 71 1; 54 1; 53 1 |
| NAME | category | 25 | 0 | Mt. Pleasant Neighborhood 1; Village Square Branch Lib 1; Educational Park Library 1; Tully Community Library 1 |
| FULLADDR | category | 25 | 0 | 3411 Rocky Mountain Drive 1; 4001 Evergreen Village Sq 1; 1772 Educational Park Dri 1; 880 Tully Road 1 |
| ZIPCODE | category | 22 | 0 | 95127 2; 95111 2; 95112 2; 95135 1 |
| STATUS | other | 1 | 0 | Open 25 |
| PROJECTEDOPENING | empty | 1 | 25 |  |
| AGENCYURL | empty | 1 | 25 |  |
| OPERDAYS | empty | 1 | 25 |  |
| OPERHOURS | empty | 1 | 25 |  |
| CONTACT | category | 13 | 0 | Tiffany Bradford-Oldham 3; Margaret Yamasaki 2; Mark Giannuzzi 2; Trina Richbourg 2 |
| PHONE | category | 25 | 0 | 408-808-3088 1; 408-808-3093 1; 408-808-3073 1; 408-808-3030 1 |
| EMAIL | category | 13 | 1 | tiffany.bradford-oldham@s 3; margaret.yamasaki@sjlibra 2; mark.giannuzzi@sjlibrary. 2; trina.richbourg@sjlibrary 2 |
| LASTUPDATE | category | 25 | 0 | 2022/02/07 19:18:54+00 1; 2021/05/04 22:08:51+00 1; 2021/05/04 22:04:30+00 1; 2022/02/07 19:39:15+00 1 |
| NOTES | empty | 1 | 25 |  |
| SHAPE_LENGTH | amount | 25 | 0 | 600.60327594512 1; 688.47849825292 1; 1176.74586543102 1; 1541.01351414091 1 |
| SHAPE_AREA | amount | 25 | 0 | 16370.5576109368 1; 26354.9089330729 1; 84157.3895278727 1; 139116.589567957 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:18:13.57869 25 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9340dd42-eafb-481b-9afd-7 25 |
| SRC_SHA256 | who | 1 | 0 | 40c5e779aa1f74b0d97332cd0 25 |
