# PORTAL_SOC_UTAH_OPEN_DATA_P_4AD0B626C8

rows 5.0K  columns 22  scan 3.0s

roles: audit 2, category 7, date 1, id 2, other 7, who 4

## when

INGESTED_AT
  2026      5.0K  ##############################

## who

NAME by rows
        10  H & R BLOCK
        10  AMERICA FIRST CREDIT UNION
         9  DEPT OF HUMAN SERVICES
         7  DEPT OF NATURAL RESOURCES
         7  DEPT OF CORRECTIONS
         7  MCDONALDS
         6  AUTOZONE
         6  FAMILY DOLLAR  INC
         6  DOLLAR TREE STORES
         6  JUDICIAL BRANCH
         6  DEPT OF PUBLIC SAFETY
         6  JIFFY LUBE
         5  GOWIRELESS, INC.
         5  MOUNTAIN AMERICA CREDIT UNION
         5  JPMORGAN CHASE BANK  NA
         5  ALCOHOLIC BEVERAGE CONTROL
         4  DEPT OF TECHNOLOGY SERVICES
         4  ALTABANK
         4  CVS RX SERVICES  INC
         4  EDWARD D JONES & CO

NAICS by rows
       135  624120
       121  722513
       120  236115
       119  531210
       116  621210
       102  722511
        97  621111
        90  561730
        77  611110
        76  524210
        68  541611
        65  541110
        63  238221
        57  447110
        55  541613
        53  541511
        48  811111
        46  721110
        45  238211
        42  454390

CITY by rows
       384  OGDEN
       325  SAINT GEORGE
       301  OREM
       245  PROVO
       193  LOGAN
       189  PARK CITY
       185  LEHI
       181  LAYTON
       138  BOUNTIFUL
       120  AMERICAN FORK
       108  SPANISH FORK
       107  CEDAR CITY
        94  VERNAL
        91  PLEASANT GROVE
        86  KAYSVILLE
        82  SPRINGVILLE
        76  HEBER CITY
        74  WASHINGTON
        68  BRIGHAM CITY
        68  CLEARFIELD

SRC_SHA256 by rows
      5.0K  c5d6828c752f47af2ba6f88b16458286f68f683670b2bfa19499a19376c4cbab

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date
  ALCOHOLIC BEVERAGE CONTROL                2026:5
  ALTABANK                                  2026:4
  AMERICA FIRST CREDIT UNION                2026:10
  AUTOZONE                                  2026:6
  CVS RX SERVICES  INC                      2026:4
  DEPT OF CORRECTIONS                       2026:7
  DEPT OF HUMAN SERVICES                    2026:9
  DEPT OF NATURAL RESOURCES                 2026:7
  DEPT OF PUBLIC SAFETY                     2026:6
  DEPT OF TECHNOLOGY SERVICES               2026:4
  DOLLAR TREE STORES                        2026:6
  EDWARD D JONES & CO                       2026:4
  FAMILY DOLLAR  INC                        2026:6
  GOWIRELESS, INC.                          2026:5
  H & R BLOCK                               2026:10
  JIFFY LUBE                                2026:6
  JPMORGAN CHASE BANK  NA                   2026:5
  JUDICIAL BRANCH                           2026:6
  MCDONALDS                                 2026:7
  MOUNTAIN AMERICA CREDIT UNION             2026:5

NAICS by INGESTED_AT  LOAD STAMP, not an event date
  236115                                    2026:120
  238211                                    2026:45
  238221                                    2026:63
  447110                                    2026:57
  454390                                    2026:42
  524210                                    2026:76
  531210                                    2026:119
  541110                                    2026:65
  541511                                    2026:53
  541611                                    2026:68
  541613                                    2026:55
  561730                                    2026:90
  611110                                    2026:77
  621111                                    2026:97
  621210                                    2026:116
  624120                                    2026:135
  721110                                    2026:46
  722511                                    2026:102
  722513                                    2026:121
  811111                                    2026:48

## what

COUNTYCODE: 49 33%, 11 17%, 57 13%, 53 11%, 5 7%, 43 5%, 3 3%, 21 3%, 47 2%, 45 2%, 51 2%, 41 2%

COUNTYNAME: Utah 33%, Davis 17%, Weber 13%, Washington 11%, Cache 7%, Summit 5%, Box Elder 3%, Iron 3%, Uintah 2%, Tooele 2%, Wasatch 2%, Sevier 2%

EMPRANGE: 1-4 44%, 5-9 17%, 10-19 13%, 0 12%, 20-49 10%, 50-99 3%, 100-249 1%, 250-499 0%, 500-999 0%, 2000-2999 0%, 1000-1999 0%

EMPRANGECODE: B 44%, C 17%, D 13%, A 12%, E 10%, F 3%, G 1%, H 0%, I 0%, K 0%, J 0%

OWNERSHIP: Private 95%, Local 3%, State 1%, Federal 0%

COMPUTED_REGION_5D9V_6BUI: 5 32%, 22 17%, 16 12%, 8 11%, 6 8%, 7 5%, 14 3%, 15 3%, 10 2%, 19 2%, 11 2%, 12 2%

COMPUTED_REGION_MI24_NG5Q: 19 32%, 23 17%, 4 12%, 15 11%, 12 8%, 8 5%, 11 3%, 2 3%, 13 2%, 17 2%, 9 2%, 27 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NAME | who | 4.8K | 0 | DEPT OF HUMAN SERVICES 26; CLASSIC JACK CONSTRUCTION 25; JBW SALES, INC. 25; DIAMOND VALLEY ELEMENTARY 25 |
| ADDRESS1 | id | 4.8K | 49 | 1565 N 500 E 25; 13900 N WILLOW CREEK DR 25; 1411 W DIAMOND VALLEY DR 25; 2185 N CLIFFROSE DR 25 |
| CITY | who | 205 | 0 | OGDEN 384; SAINT GEORGE 325; OREM 301; PROVO 245 |
| STATE | other | 1 | 0 | UT 5.0K |
| ZIP | other | 3.1K | 0 | 84043 63; 84041 62; 84770 60; 84003 59 |
| COUNTYCODE | category | 27 | 0 | 49 1.5K; 11 775; 57 569; 53 507 |
| COUNTYNAME | category | 27 | 0 | Utah 1.5K; Davis 775; Weber 569; Washington 507 |
| EMPRANGE | category | 11 | 0 | 1-4 2.2K; 5-9 864; 10-19 627; 0 597 |
| EMPRANGECODE | category | 11 | 0 | B 2.2K; C 864; D 627; A 597 |
| NAICS | who | 603 | 0 | 624120 135; 722513 121; 236115 120; 531210 119 |
| OWNERSHIP | category | 4 | 0 | Private 4.7K; Local 169; State 74; Federal 14 |
| GEOCODED_COLUMN | id | 4.8K | 0 | {"type": "Point", "coordi 25; {"type": "Point", "coordi 25; {"type": "Point", "coordi 25; {"type": "Point", "coordi 25 |
| COMPUTED_REGION_5D9V_6BUI | category | 29 | 2 | 5 1.5K; 22 780; 16 556; 8 506 |
| COMPUTED_REGION_QMWN_IMPY | other | 188 | 475 | 159 316; 193 295; 204 245; 148 201 |
| COMPUTED_REGION_JDNU_JMST | other | 186 | 2 | 287 185; 195 170; 109 157; 171 154 |
| COMPUTED_REGION_2FPW_SWV9 | other | 51 | 2 | 59 325; 44 249; 50 239; 3 237 |
| COMPUTED_REGION_MI24_NG5Q | category | 29 | 2 | 19 1.5K; 23 780; 4 556; 15 506 |
| PHONE | other | 3.8K | 782 | (801) 359-4699 74; (435) 750-5566 31; (623) 792-6100 24; (435) 752-1510 22 |
| ADDRESS2 | other | 163 | 4.8K | STE 101 7; STE B 7; STE 200 6; STE 1 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:44:28.47947 5.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | ccfa1004-dc75-478c-ba29-7 5.0K |
| SRC_SHA256 | who | 1 | 0 | c5d6828c752f47af2ba6f88b1 5.0K |
