# PORTAL_ARC_HARRIS_COUNTY_OP_32D5FF05CA

rows 100  columns 123  scan 9.7s

roles: amount 12, audit 2, category 43, date 2, empty 22, other 38, who 5

## when

USER_UPDAT
  2023       100  ##############################

INGESTED_AT
  2026       100  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 100 | 84 | 100 | 100 | 100 | 9.9K |
| RANK | 100 | 4.50 | 20 | 20 | 20 | 2.0K |
| DISTANCE | 100 | 0 | 0 | 304.7K | 304.8K | 1.81M |
| X | 100 | -95.76 | -95.67 | -95.52 | -95.50 | -9.6K |
| Y | 100 | 29.83 | 29.90 | 30.01 | 30.02 | 3.0K |
| DISPLAYX | 100 | -95.76 | -95.67 | -95.52 | -95.50 | -9.6K |

## who

STNAME by rows
         5  Greenhouse
         4  Kieth Harrow
         4  Fry
         4  Little York
         3  Queenston
         3  Huffmeister
         3  Mason
         2  Warner Smith
         2  Grant
         2  Perry
         2  Kluge
         2  Fairfield Place
         2  Telge
         2  Jones
         2  Westgreen
         2  Barker Cypress
         2  Woods Spillane
         2  Tuckerton
         2  Eldridge
         1  Willowbridge Park

STNAME by dollars
      498.57        5 rows  Greenhouse
         400        4 rows  Fry
         400        4 rows  Kieth Harrow
      398.02        4 rows  Little York
         300        3 rows  Mason
         299        3 rows  Huffmeister
         299        3 rows  Queenston
         200        2 rows  Jones
         200        2 rows  Woods Spillane
         200        2 rows  Grant
         200        2 rows  Perry
         200        2 rows  Westgreen
         200        2 rows  Eldridge
         200        2 rows  Telge
         200        2 rows  Warner Smith
         199        2 rows  Kluge
         199        2 rows  Fairfield Place
      197.21        2 rows  Barker Cypress
      194.17        2 rows  Tuckerton
         100        1 rows  Willow River

IN_POSTAL by rows
        19  77433
        10  77449
         8  77429
         3  77084
         3  77041
         2  77040
         2  77095
         1  77095-4618
         1  77433-0000
         1  77064
         1  77064-3001
         1  77449-7004
         1  77064-3108
         1  77070-4612
         1  77040-5459
         1  77095-2307
         1  77092-1006
         1  77064-7137
         1  77095-4441
         1  77040-5438

IN_POSTAL by dollars
        1.9K       19 rows  77433
      992.74       10 rows  77449
      796.21        8 rows  77429
         300        3 rows  77041
      299.01        3 rows  77084
      197.39        2 rows  77040
      190.59        2 rows  77095
         100        1 rows  77449-4208
         100        1 rows  77070
         100        1 rows  77070-4501
         100        1 rows  77095-1703
         100        1 rows  77433-0000
         100        1 rows  77040-5438
         100        1 rows  77064-4551
         100        1 rows  77040-5459
         100        1 rows  77070-4438
         100        1 rows  77040-2400
         100        1 rows  77070-2814
         100        1 rows  77084-5722
         100        1 rows  77429-3386

USER_SCH_9 by rows
        19  77433
        10  77449
         8  77429
         3  77084
         3  77041
         2  77095
         2  77040
         1  77429-2452
         1  77070-2628
         1  77040-5438
         1  77433-0000
         1  77065-2413
         1  77433-3240
         1  77095-1703
         1  77449-4382
         1  77095-2612
         1  77449-4208
         1  77084-1523
         1  77429-3281
         1  77429-5722

USER_SCH_9 by dollars
        1.9K       19 rows  77433
      992.74       10 rows  77449
      796.21        8 rows  77429
         300        3 rows  77041
      299.01        3 rows  77084
      197.39        2 rows  77040
      190.59        2 rows  77095
         100        1 rows  77070
         100        1 rows  77433-0188
         100        1 rows  77041-1883
         100        1 rows  77064-4551
         100        1 rows  77095-1703
         100        1 rows  77065-2413
         100        1 rows  77070-2814
         100        1 rows  77065
         100        1 rows  77449-4382
         100        1 rows  77084-2554
         100        1 rows  77040-2134
         100        1 rows  77429-2452
         100        1 rows  77069-1801

SUBREGION by rows
       100  Harris County

SUBREGION by dollars
        9.9K      100 rows  Harris County

## who x when

STNAME by USER_UPDAT, dollars = SCORE
  Barker Cypress                            2023:197.21
  Eldridge                                  2023:200
  Fairfield Place                           2023:199
  Fry                                       2023:400
  Grant                                     2023:200
  Greenhouse                                2023:498.57
  Huffmeister                               2023:299
  Jones                                     2023:200
  Kieth Harrow                              2023:400
  Kluge                                     2023:199
  Little York                               2023:398.02
  Mason                                     2023:300
  Perry                                     2023:200
  Queenston                                 2023:299
  Telge                                     2023:200
  Tuckerton                                 2023:194.17
  Warner Smith                              2023:200
  Westgreen                                 2023:200
  Willow River                              2023:100
  Willowbridge Park                         2023:100
  Woods Spillane                            2023:200

IN_POSTAL by USER_UPDAT, dollars = SCORE
  77040                                     2023:197.39
  77040-2400                                2023:100
  77040-5438                                2023:100
  77040-5459                                2023:100
  77041                                     2023:300
  77064                                     2023:100
  77064-3001                                2023:98.34
  77064-3108                                2023:99
  77064-4551                                2023:100
  77064-7137                                2023:99
  77070                                     2023:100
  77070-2814                                2023:100
  77070-4438                                2023:100
  77070-4501                                2023:100
  77070-4612                                2023:100
  77084                                     2023:299.01
  77084-5722                                2023:100
  77092-1006                                2023:100
  77095                                     2023:190.59
  77095-1703                                2023:100
  77095-2307                                2023:100
  77095-4441                                2023:100
  77095-4618                                2023:99
  77429                                     2023:796.21
  77429-3386                                2023:100
  77433                                     2023:1.9K
  77433-0000                                2023:100
  77449                                     2023:992.74
  77449-4208                                2023:100
  77449-7004                                2023:100

## what

STATUS: M 99%, T 1%

ADDR_TYPE: PointAddress 69%, StreetAddress 26%, Postal 3%, StreetName 2%

PLACENAME: 77433 67%, 77095 33%

ADDNUMFROM: 10601 23%, 17501 8%, 20298 8%, 19001 8%, 19500 8%, 19664 8%, 22100 8%, 21000 8%, 9249 8%, 12443 8%, 7917 8%

ADDNUMTO: 10707 23%, 17561 8%, 19890 8%, 19099 8%, 19580 8%, 19634 8%, 22410 8%, 21030 8%, 9201 8%, 12381 8%, 7979 8%

ADDRANGE: 10601-10707 23%, 17501-17561 8%, 19890-20298 8%, 19001-19099 8%, 19500-19580 8%, 19634-19664 8%, 22100-22410 8%, 21000-21030 8%, 9201-9249 8%, 12381-12443 8%, 7917-7979 8%

SIDE: L 59%, R 41%

STPREDIR: W 57%, N 43%

STTYPE: Rd 47%, Dr 23%, Blvd 18%, St 5%, Pkwy 3%, Ln 3%, Hwy 1%

STDIR: W 100%

NBRHD: Bridgeland 36%, Towne Lake 18%, Fairfield 18%, Westbridge 9%, Copperfield 9%, Brookhollow West 9%

CITY: Houston 50%, Cypress 36%, Katy 14%

METROAREA: Houston-Galveston Metro Area 100%

POSTAL: 77433 23%, 77449 14%, 77429 13%, 77095 10%, 77084 9%, 77064 8%, 77040 7%, 77070 6%, 77041 4%, 77065 4%, 77069 1%, 77092 1%

EXINFO: 10330 PRAIRIELAND CROSSING | W 12%, 21211 12%, HOUSTON 12%, 18425 W RD 12%, 5722 12%, CYRESS 12%, 16823 W RD 12%, 22855 12%

IN_CITY: HOUSTON 51%, CYPRESS 34%, KATY 14%, CYRESS 1%

IN_SUBREGI: HARRIS COUNTY 99%, WALLER COUNTY 1%

USER_COUNT: 101 99%, 237 1%

USER_COU_1: HARRIS COUNTY 99%, WALLER COUNTY 1%

USER_DISTR: 101907 93%, 101858 4%, 237904 1%, 101845 1%, 101803 1%

USER_DIS_1: CYPRESS-FAIRBANKS ISD 93%, HARMONY PUBLIC SCHOOLS - HOUST 4%, WALLER ISD 1%, YES PREP PUBLIC SCHOOLS INC 1%, ARISTOI CLASSICAL ACADEMY 1%

USER_DIS_2: INDEPENDENT 94%, CHARTER 6%

USER_NCES: 4816110 93%, 4800274 4%, 4844430 1%, 4800209 1%, 4800019 1%

USER_DIS_3: P O BOX 692003 93%, 9321 W SAM HOUSTON PKWY S 4%, 2214 WALLER ST 1%, 5455 S LOOP E FWY 1%, 5610 MORTON RD 1%

USER_DIS_4: HOUSTON 98%, WALLER 1%, KATY 1%

USER_DIS_6: 77269-2003 93%, 77099 4%, 77484 1%, 77033 1%, 77493 1%

USER_DIS_7: 10300 JONES RD 93%, 3203 N SAM HOUSTON PKWY W 4%, 2214 WALLER ST 1%, 5455 S LOOP E FWY 1%, 5610 MORTON RD 1%

USER_DIS_8: HOUSTON 98%, WALLER 1%, KATY 1%

USER_DIS10: 77065-4208 93%, 77038 4%, 77484 1%, 77033 1%, 77493 1%

USER_DIS11: (281) 897-4000 93%, (713) 343-3333 4%, (936) 931-3685 1%, (713) 967-9000 1%, (281) 391-5003 1%

USER_DIS12: (281) 897-4125 93%, (713) 777-8555 4%, (936) 310-6589 1%, (713) 589-2502 1%, (281) 391-5010 1%

USER_DIS13: holly.reichert@cfisd.net 93%, superintendent.office@harmonyt 4%, kmoran@wallerisd.net 1%, publicinfo@yesprep.org 1%, bdavidson@aristoiclassical.org 1%

USER_DIS14: www.cfisd.net 93%, www.harmonytx.org 4%, www.wallerisd.net 1%, www.yesprep.org 1%, www.aristoiclassical.org 1%

USER_DIS15: DR MARK HENRY 93%, MR FATIH AY 4%, KEVIN MORAN 1%, MR MARK DIBELLA 1%, MRS BRENDA DAVIDSON 1%

USER_DIS16: 118010 93%, 6731 4%, 8834 1%, 16366 1%, 1316 1%

USER_INSTR: REGULAR INSTRUCTIONAL 97%, DAEP INSTRUCTIONAL 2%, JJAEP INSTRUCTIONAL 1%

USER_CHART: OPEN ENROLLMENT CHARTER 100%

USER_SCH_3: HOUSTON 53%, CYPRESS 31%, KATY 14%, WALLER 1%, CYRESS 1%

USER_SCH_7: HOUSTON 51%, CYPRESS 34%, KATY 14%, CYRESS 1%

USER_SCH13: www.cfisd.net 94%, HARMONYTX.ORG 1%, hsacypress.harmonytx.org/ 1%, hsdharmonytx.org/ 1%, hsehouston.harmonytx.org/ 1%, northwest.yesprep.org 1%

USER_GRADE: EE-05 39%, 06-08 20%, PK-05 13%, 09-12 12%, KG-05 5%, 06-12 5%, PK-02 1%, EE KG-05 1%, 03-05 1%, PK-06 1%, PK-12 1%, KG-08 1%

USER_SCH16: Active 97%, Under Construction 3%

PRECINCT: 4 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | other | 99 | 0 | 100 1; 99 1; 98 1; 97 1 |
| OBJECTID | other | 98 | 0 | 9226 1; 4561 1; 4539 1; 4538 1 |
| STATUS | category | 2 | 0 | M 99; T 1 |
| SCORE | amount | 13 | 0 | 100.0 75; 99.0 10; 98.34 3; 90.59 2 |
| MATCH_TYPE | other | 1 | 0 | A 100 |
| MATCH_ADDR | other | 99 | 0 | 77433, Cypress, Texas 2; 17501 Cypress-North Houst 1; Tuckerton Rd, Cypress, Te 1; 20220 Clay Rd, Katy, Texa 1 |
| LONGLABEL | other | 100 | 0 | 77433, Cypress, TX, USA 2; 17501 Cypress-North Houst 1; Tuckerton Rd, Cypress, TX 1; 20220 Clay Rd, Katy, TX,  1 |
| SHORTLABEL | other | 98 | 0 | 77433 2; 17501 Cypress-North Houst 1; Tuckerton Rd 1; 20220 Clay Rd 1 |
| ADDR_TYPE | category | 4 | 0 | PointAddress 69; StreetAddress 26; Postal 3; StreetName 2 |
| TYPE | empty | 1 | 100 |  |
| PLACENAME | category | 3 | 97 | 77433 2; 77095 1 |
| PLACE_ADDR | other | 99 | 0 | Cypress, Texas, 77433 2; 17501 Cypress-North Houst 1; Tuckerton Rd, Cypress, Te 1; 20220 Clay Rd, Katy, Texa 1 |
| PHONE | empty | 1 | 100 |  |
| URL | empty | 1 | 100 |  |
| RANK | amount | 2 | 0 | 20.0 97; 4.5 3 |
| ADDBLDG | empty | 1 | 100 |  |
| ADDNUM | other | 96 | 5 | 7600 2; 17501 1; 20220 1; 6425 1 |
| ADDNUMFROM | category | 25 | 74 | 10601 3; 17501 1; 20298 1; 19001 1 |
| ADDNUMTO | category | 25 | 74 | 10707 3; 17561 1; 19890 1; 19099 1 |
| ADDRANGE | category | 24 | 74 | 10601-10707 3; 17501-17561 1; 19890-20298 1; 19001-19099 1 |
| SIDE | category | 3 | 73 | L 16; R 11 |
| STPREDIR | category | 3 | 93 | W 4; N 3 |
| STPRETYPE | empty | 1 | 100 |  |
| STNAME | who | 68 | 3 | Greenhouse 5; Little York 4; Fry 4; Kieth Harrow 4 |
| STTYPE | category | 8 | 4 | Rd 45; Dr 22; Blvd 17; St 5 |
| STDIR | category | 2 | 99 | W 1 |
| BLDGTYPE | empty | 1 | 100 |  |
| BLDGNAME | empty | 1 | 100 |  |
| LEVELTYPE | empty | 1 | 100 |  |
| LEVELNAME | empty | 1 | 100 |  |
| UNITTYPE | empty | 1 | 100 |  |
| UNITNAME | empty | 1 | 100 |  |
| SUBADDR | empty | 1 | 100 |  |
| STADDR | other | 97 | 3 | 17501 Cypress-North Houst 1; Tuckerton Rd 1; 20220 Clay Rd 1; 6425 Greenhouse Rd 1 |
| BLOCK | empty | 1 | 100 |  |
| SECTOR | empty | 1 | 100 |  |
| NBRHD | category | 7 | 89 | Bridgeland 4; Towne Lake 2; Fairfield 2; Westbridge 1 |
| DISTRICT | empty | 1 | 100 |  |
| CITY | category | 3 | 0 | Houston 50; Cypress 36; Katy 14 |
| METROAREA | category | 2 | 71 | Houston-Galveston Metro A 29 |
| SUBREGION | who | 1 | 0 | Harris County 100 |
| REGION | other | 1 | 0 | Texas 100 |
| REGIONABBR | other | 1 | 0 | TX 100 |
| TERRITORY | empty | 1 | 100 |  |
| ZONE | empty | 1 | 100 |  |
| POSTAL | category | 12 | 0 | 77433 23; 77449 14; 77429 13; 77095 10 |
| POSTALEXT | other | 80 | 20 | 7097 2; 5722 2; 58ND 1; 5476 1 |
| COUNTRY | other | 1 | 0 | USA 100 |
| LANGCODE | other | 1 | 0 | ENG 100 |
| DISTANCE | amount | 7 | 0 | 0.0 93; 192597.344231 2; 304459.761634 1; 304793.623272 1 |
| X | amount | 100 | 0 | -95.7408812 2; -95.6787316444475 1; -95.7536650242999 1; -95.7197731472291 1 |
| Y | amount | 97 | 0 | 30.0000124000001 2; 29.9424108150852 1; 29.9218599870437 1; 29.8313040473433 1 |
| DISPLAYX | amount | 99 | 0 | -95.7408812 2; -95.660946 2; -95.6787316444475 1; -95.7536650242999 1 |
| DISPLAYY | amount | 98 | 0 | 30.0000124000001 2; 29.9424108150852 1; 29.9218599870437 1; 29.8313040473433 1 |
| XMIN | amount | 98 | 0 | -95.8738812 2; -95.661946 2; -95.6797316444475 1; -95.7546650243 1 |
| XMAX | amount | 97 | 0 | -95.6078812 2; -95.659946 2; -95.6777316444475 1; -95.7526650242999 1 |
| YMIN | amount | 97 | 0 | 29.8670124000001 2; 29.9414108150852 1; 29.9208599870437 1; 29.8303040473433 1 |
| YMAX | amount | 100 | 0 | 30.1330124000001 2; 29.9434108150852 1; 29.9228599870437 1; 29.8323040473433 1 |
| EXINFO | category | 9 | 92 | 10330 PRAIRIELAND CROSSIN 1; 21211 1; HOUSTON 1; 18425 W RD 1 |
| IN_ADDRESS | other | 101 | 0 | 10330 PRAIRIELAND CROSSIN 1; 17501 CYPRESS N HOUSTON R 1; 21211 TUCKERTON RD 1; 20220 CLAY RD 1 |
| IN_ADDRE_1 | empty | 1 | 100 |  |
| IN_ADDRE_2 | empty | 1 | 100 |  |
| IN_NEIGHBO | empty | 1 | 100 |  |
| IN_CITY | category | 4 | 0 | HOUSTON 51; CYPRESS 34; KATY 14; CYRESS 1 |
| IN_SUBREGI | category | 2 | 0 | HARRIS COUNTY 99; WALLER COUNTY 1 |
| IN_REGION | other | 1 | 0 | TX 100 |
| IN_POSTAL | who | 60 | 0 | 77433 19; 77449 10; 77429 8; 77041 3 |
| IN_POSTALE | empty | 1 | 100 |  |
| IN_COUNTRY | empty | 1 | 100 |  |
| USER_COUNT | category | 2 | 0 | 101 99; 237 1 |
| USER_COU_1 | category | 2 | 0 | HARRIS COUNTY 99; WALLER COUNTY 1 |
| USER_ESC_R | other | 1 | 0 | 4 100 |
| USER_ESC_1 | other | 1 | 0 | 4 100 |
| USER_ESC_2 | other | 1 | 0 | 4 100 |
| USER_DISTR | category | 5 | 0 | 101907 93; 101858 4; 237904 1; 101845 1 |
| USER_DIS_1 | category | 5 | 0 | CYPRESS-FAIRBANKS ISD 93; HARMONY PUBLIC SCHOOLS -  4; WALLER ISD 1; YES PREP PUBLIC SCHOOLS I 1 |
| USER_DIS_2 | category | 2 | 0 | INDEPENDENT 94; CHARTER 6 |
| USER_NCES | category | 5 | 0 | 4816110 93; 4800274 4; 4844430 1; 4800209 1 |
| USER_DIS_3 | category | 5 | 0 | P O BOX 692003 93; 9321 W SAM HOUSTON PKWY S 4; 2214 WALLER ST 1; 5455 S LOOP E FWY 1 |
| USER_DIS_4 | category | 3 | 0 | HOUSTON 98; WALLER 1; KATY 1 |
| USER_DIS_5 | other | 1 | 0 | TX 100 |
| USER_DIS_6 | category | 5 | 0 | 77269-2003 93; 77099 4; 77484 1; 77033 1 |
| USER_DIS_7 | category | 5 | 0 | 10300 JONES RD 93; 3203 N SAM HOUSTON PKWY W 4; 2214 WALLER ST 1; 5455 S LOOP E FWY 1 |
| USER_DIS_8 | category | 3 | 0 | HOUSTON 98; WALLER 1; KATY 1 |
| USER_DIS_9 | other | 1 | 0 | TX 100 |
| USER_DIS10 | category | 5 | 0 | 77065-4208 93; 77038 4; 77484 1; 77033 1 |
| USER_DIS11 | category | 5 | 0 | (281) 897-4000 93; (713) 343-3333 4; (936) 931-3685 1; (713) 967-9000 1 |
| USER_DIS12 | category | 5 | 0 | (281) 897-4125 93; (713) 777-8555 4; (936) 310-6589 1; (713) 589-2502 1 |
| USER_DIS13 | category | 5 | 0 | holly.reichert@cfisd.net 93; superintendent.office@har 4; kmoran@wallerisd.net 1; publicinfo@yesprep.org 1 |
| USER_DIS14 | category | 5 | 0 | www.cfisd.net 93; www.harmonytx.org 4; www.wallerisd.net 1; www.yesprep.org 1 |
| USER_DIS15 | category | 5 | 0 | DR MARK HENRY 93; MR FATIH AY 4; KEVIN MORAN 1; MR MARK DIBELLA 1 |
| USER_DIS16 | category | 5 | 0 | 118010 93; 6731 4; 8834 1; 16366 1 |
| USER_SCHOO | other | 101 | 0 | 237904109 1; 101907157 1; 101907160 1; 101907161 1 |
| USER_SCH_1 | other | 100 | 0 | NEW EL 2; WOODARD EL 1; MCGOWN EL 1; HOOVER EL 1 |
| USER_INSTR | category | 3 | 0 | REGULAR INSTRUCTIONAL 97; DAEP INSTRUCTIONAL 2; JJAEP INSTRUCTIONAL 1 |
| USER_CHART | category | 2 | 94 | OPEN ENROLLMENT CHARTER 6 |
| USER_AEA | other | 1 | 0 | N 100 |
| USER_MAGNE | other | 1 | 0 | N 100 |
| USER_RESID | other | 1 | 0 | N 100 |
| USER_NCE_1 | other | 97 | 0 | 0 3; 481611012935 1; 481611014254 1; 481611013432 1 |
| USER_SCH_2 | other | 98 | 0 | P O BOX 692003 4; 2214 WALLER ST 1; 21211 TUCKERTON RD 1; 20220 CLAY RD 1 |
| USER_SCH_3 | category | 5 | 0 | HOUSTON 53; CYPRESS 31; KATY 14; WALLER 1 |
| USER_SCH_4 | other | 1 | 0 | TX 100 |
| USER_SCH_5 | other | 61 | 0 | 77433 16; 77449 10; 77429 8; 77269-2003 3 |
| USER_SCH_6 | other | 101 | 0 | 10330 PRAIRIELAND CROSSIN 1; 17501 CYPRESS N HOUSTON R 1; 21211 TUCKERTON RD 1; 20220 CLAY RD 1 |
| USER_SCH_7 | category | 4 | 0 | HOUSTON 51; CYPRESS 34; KATY 14; CYRESS 1 |
| USER_SCH_8 | other | 1 | 0 | TX 100 |
| USER_SCH_9 | who | 60 | 0 | 77433 19; 77449 10; 77429 8; 77041 3 |
| USER_SCH10 | other | 98 | 2 | (281) 213-1550 2; (936) 931-3685 1; (281) 373-2303 1; (281) 897-4077 1 |
| USER_SCH11 | other | 93 | 5 | (281) 897-4125 2; (281) 213-1551 2; (281) 444-1555 2; (281) 373-2304 1 |
| USER_SCH12 | other | 98 | 0 | superintendent.office@har 3; martin.drayton@cfisd.net 2; kcottrell@wallerisd.net 1; susan.brenz@cfisd.net 1 |
| USER_SCH13 | category | 7 | 16 | www.cfisd.net 79; HARMONYTX.ORG 1; hsacypress.harmonytx.org/ 1; hsdharmonytx.org/ 1 |
| USER_SCH14 | other | 99 | 2 | SUSAN BRENZ 1; LAURA NOVACINSKI 1; MS MICHELLE RICE 1; MS KATIE HERRERA 1 |
| USER_GRADE | category | 12 | 0 | EE-05 39; 06-08 20; PK-05 13; 09-12 12 |
| USER_SCH15 | other | 94 | 0 | 0 5; 1056 2; 1103 2; 930 2 |
| USER_SCH16 | category | 2 | 0 | Active 97; Under Construction 3 |
| USER_SCH17 | amount | 43 | 0 | nan 31; 1214784000000.0 4; 1151366400000.0 4; 1120176000000.0 4 |
| USER_UPDAT | date | 4 | 0 | 4/20/2023 5:41:29 AM 93; 4/20/2023 5:41:28 AM 4; 4/20/2023 5:41:27 AM 2; 4/20/2023 5:41:53 AM 1 |
| PRECINCT | category | 2 | 74 | 4 26 |
| GEOMETRY | other | 99 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:19:28.03604 100 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5eab5f5e-fc76-4d83-9326-e 100 |
| SRC_SHA256 | who | 1 | 0 | 171c2bc5c058aa990dfc07f09 100 |
