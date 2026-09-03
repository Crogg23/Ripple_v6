# PORTAL_SOC_OPEN_DATA_BR_C110D5CF59

rows 1.5K  columns 28  scan 2.4s

roles: audit 2, category 10, date 1, other 10, who 6

## when

INGESTED_AT
  2026      1.5K  ##############################

## who

BUSINESS_NAME by rows
        28  KWIK STOP
        20  ON THE RUN #14
        14  TEXACO
        10  ALBERTSON # 3747
         9  SAVE MORE MARKET 4
         8  SHOPPERS VALUE FOODS
         6  S & Y GROCERY
         4  CVS PHARMACY #5343
         4  SCENIC HWY HOP IN CIRCLE K
         4  CVS PHARMACY #1116
         4  MURPHY USA 7716
         4  EXXON/ON THE RUN INC #2707651
         4  ALDENS SCHOOL OF COSMETOLOGY
         4  SAVE MORE MARKET #6
         4  SHOPPERS VALUE
         4  BURGERSMITH
         4  CVS PHARMACY #5319
         4  ALBERTSON #3792
         3  ALBASHA GREEK & LEBANESE RESTAURANT
         3  FAST STOP

ST_NAME_ID by rows
        93  106
        83  3873
        81  3808
        54  1829
        53  2355
        52  2546
        44  573
        40  2090
        35  4450
        34  3482
        34  4344
        33  1283
        29  2158
        25  4839
        25  786
        23  4475
        23  1250
        22  5377
        22  3595
        17  1699

STREET_NAME_COMPLETE by rows
        93  AIRLINE HWY
        83  PLANK RD
        81  PERKINS RD
        54  FLORIDA BLVD
        53  HIGHLAND RD
        52  JEFFERSON HWY
        44  BLUEBONNET BLVD
        40  GOVERNMENT ST
        35  S SHERWOOD FOREST BLVD
        34  SCENIC HWY
        34  NICHOLSON DR
        33  COURSEY BLVD
        29  GREENWELL SPRINGS RD
        28  MAIN ST
        25  3RD ST
        25  BURBANK DR
        23  CORPORATE BLVD
        23  SIEGEN LN
        22  O'NEAL LN
        22  OLD HAMMOND HWY

BUSINESS_ID by rows
        27  nan
        15  2142
        11  7305
         8  26600
         8  2569
         6  4430
         6  3246
         6  13748
         5  26568
         5  23381
         5  26598
         5  26566
         5  26569
         5  26590
         5  26599
         5  26592
         5  35172
         5  26561
         4  33339
         4  2024

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ALBASHA GREEK & LEBANESE RESTAURANT       2026:3
  ALBERTSON # 3747                          2026:10
  ALBERTSON #3792                           2026:4
  ALDENS SCHOOL OF COSMETOLOGY              2026:4
  BURGERSMITH                               2026:4
  CVS PHARMACY #1116                        2026:4
  CVS PHARMACY #5319                        2026:4
  CVS PHARMACY #5343                        2026:4
  EXXON/ON THE RUN INC #2707651             2026:4
  FAST STOP                                 2026:3
  KWIK STOP                                 2026:28
  MURPHY USA 7716                           2026:4
  ON THE RUN #14                            2026:20
  S & Y GROCERY                             2026:6
  SAVE MORE MARKET #6                       2026:4
  SAVE MORE MARKET 4                        2026:9
  SCENIC HWY HOP IN CIRCLE K                2026:4
  SHOPPERS VALUE                            2026:4
  SHOPPERS VALUE FOODS                      2026:8
  TEXACO                                    2026:14

ST_NAME_ID by INGESTED_AT  LOAD STAMP, not an event date
  106                                       2026:93
  1250                                      2026:23
  1283                                      2026:33
  1699                                      2026:17
  1829                                      2026:54
  2090                                      2026:40
  2158                                      2026:29
  2355                                      2026:53
  2546                                      2026:52
  3482                                      2026:34
  3595                                      2026:22
  3808                                      2026:81
  3873                                      2026:83
  4344                                      2026:34
  4450                                      2026:35
  4475                                      2026:23
  4839                                      2026:25
  5377                                      2026:22
  573                                       2026:44
  786                                       2026:25

## what

CITY: BATON ROUGE 92%, ZACHARY 3%, BAKER 2%, CENTRAL 2%, GREENWELL SPRINGS 1%, SLAUGHTER 0%, PRIDE 0%

ZIP: 70808 13%, 70802 12%, 70816 11%, 70805 10%, 70806 10%, 70809 10%, 70810 10%, 70815 6%, 70817 6%, 70807 4%, 70820 4%, 70791 3%

HOME_BASED_BUSINESS: No 94%, nan 6%, Yes 0%

CONSOLIDATED_FILER: No 62%, nan 31%, Yes 6%

RESOURCE_TYPE: RETAIL 49%, nan 25%, RESTAURANT 17%, BAR/NIGHTCLUB/LOUNGE 4%, RECREATION 2%, HOTEL/MOTEL 1%, ARTS AND ENTERTAINMENT 1%, FOOD ACCESS 0%, EDUCATION 0%, PROFESSIONAL SERVICES 0%, DISTRIBUTOR 0%, HEALTH CARE 0%

LANDMARK_NAME: nan 98%, SHAW CENTER FOR THE ARTS 0%, ST. JAMES PLACE 0%, BROOKWOOD VILLAGE SHOPPING CEN 0%, ACADIAN THRUWAY SHOPPING CENTE 0%, PERKINS-COLLEGE DRIVE SHOPPING 0%, GATEWAY CENTER 0%, BLUEBONNET VILLAGE SHOPPING CE 0%, REEVES SHOPPING CENTER 0%, FORET AND MCCALL SHOPPING CENT 0%, WEBB MEMORIAL PARK 0%, VILLAGE SQUARE SHOPPING CENTER 0%

SUB_RESOURCE_TYPE: nan 52%, SNAP RETAILER 21%, CONVENIENCE STORE 11%, GAS STATION 8%, PHARMACY 2%, GROCERY 2%, GROCERY/PHARMACY 2%, HEALTHY CORNER STORE 0%, VOCATIONAL TECHNICAL SCHOOL 0%, CASINO 0%, MOVIE THEATER 0%, NURSING HOME 0%

NOTATION: nan 99%, SEE STREET NAME CHANGE LIST 1%

PLACE_NAME: nan 90%, SHENANDOAH 3%, OAK HILLS PLACE 2%, INNISWOLD 2%, GARDERE 1%, VILLAGE ST. GEORGE 1%, MERRYDALE 1%, BROWNFIELDS 1%, OLD JEFFERSON 0%, WESTMINSTER 0%, MONTICELLO 0%

WEBSITE: nan 88%, http://circlek.com/ 4%, http://walgreens.com/ 2%, http://albertsons.com/ 2%, http://cvs.com/ 1%, http://walmart.com/ 1%, http://shoppersvaluefoodla.com 1%, https://winndixie.com 0%, http://hinabor.com/ 0%, http://maxwells-market.com/ 0%, http://wholefoodsmarket.com/ 0%, http://samsclub.com/ 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_NAME | who | 1.0K | 0 | KWIK STOP 31; ON THE RUN #14 24; TEXACO 19; SHOPPERS VALUE FOODS 13 |
| FULL_ADDRESS | other | 1.0K | 0 | 5255 HIGHLAND RD 10; 2956 NICHOLSON DR 10; 11825 HOOPER RD 9; 7079 WINBOURNE AVE 9 |
| CITY | category | 7 | 0 | BATON ROUGE 1.4K; ZACHARY 42; BAKER 31; CENTRAL 25 |
| ZIP | category | 24 | 0 | 70808 165; 70802 148; 70816 145; 70805 130 |
| ABC | other | 1 | 0 | Yes 1.5K |
| BUSINESS_NAICS_CODE | who | 66 | 0 | 722000 375; 445000 217; 447000 212; 445110 138 |
| BUSINESS_ID | who | 936 | 0 | nan 27; 2142 15; 7305 15; 4430 11 |
| THE_GEOM | other | 1.0K | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 9; {"type": "Point", "coordi 9 |
| ADDRESS_POINT_ID | other | 1.0K | 0 | 167485 10; 22192 10; 199625 9; 8593 9 |
| POINT_X | other | 1.0K | 0 | 3335506 10; 3326688 10; 3368091 9; 3335361 9 |
| POINT_Y | other | 1.0K | 0 | 689275 10; 698640 10; 744873 9; 720118 9 |
| ADDRESS_NO_COMPLETE | other | 969 | 0 | 5255 10; 2956 10; 11825 9; 2001 9 |
| ST_NAME_ID | who | 235 | 0 | 106 93; 3873 83; 3808 81; 1829 54 |
| STREET_NAME_COMPLETE | who | 231 | 0 | AIRLINE HWY 93; PLANK RD 83; PERKINS RD 81; FLORIDA BLVD 54 |
| METADATA_ID | other | 1.0K | 0 | 167485 10; 23046 10; 195793 9; 9715 9 |
| REVENUE_ACCOUNT_NUMBER | other | 1.0K | 0 | 00781403 31; 00679667 24; 00916703 19; 00000000 14 |
| HOME_BASED_BUSINESS | category | 3 | 0 | No 1.4K; nan 86; Yes 5 |
| CONSOLIDATED_FILER | category | 3 | 0 | No 915; nan 461; Yes 92 |
| RESOURCE_TYPE | category | 22 | 0 | RETAIL 710; nan 362; RESTAURANT 251; BAR/NIGHTCLUB/LOUNGE 60 |
| LANDMARK_NAME | category | 40 | 0 | nan 1.4K; SHAW CENTER FOR THE ARTS 3; ST. JAMES PLACE 3; BROOKWOOD VILLAGE SHOPPIN 3 |
| SUB_RESOURCE_TYPE | category | 23 | 0 | nan 763; SNAP RETAILER 306; CONVENIENCE STORE 164; GAS STATION 113 |
| PHONE_NUMBER | other | 96 | 0 | nan 1.2K; 225-768-7775 14; 225-769-0404 9; 225-355-0025 4 |
| NOTATION | category | 2 | 0 | nan 1.5K; SEE STREET NAME CHANGE LI 10 |
| PLACE_NAME | category | 11 | 0 | nan 1.3K; SHENANDOAH 37; OAK HILLS PLACE 24; INNISWOLD 23 |
| WEBSITE | category | 21 | 0 | nan 1.3K; http://circlek.com/ 63; http://walgreens.com/ 32; http://albertsons.com/ 22 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:44:35.78410 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 75a3b932-9d71-43fa-a99e-e 1.5K |
| SRC_SHA256 | who | 1 | 0 | b54e1ed8834620ff2dc7f85ce 1.5K |
