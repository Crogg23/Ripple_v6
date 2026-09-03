# PORTAL_ARC_HARRIS_COUNTY_OP_3E3BFD2059

rows 254  columns 126  scan 6.3s

roles: amount 14, audit 2, category 50, date 2, empty 19, other 35, who 5

## when

USER_UPDAT
  2023       254  ##############################

INGESTED_AT
  2026       254  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 254 | 86 | 100 | 100 | 100 | 25.2K |
| RANK | 254 | 4.50 | 20 | 20 | 20 | 5.1K |
| DISTANCE | 254 | 0 | 0 | 300.0K | 304.4K | 1.86M |
| X | 254 | -95.92 | -95.60 | -95.43 | -95.42 | -24.3K |
| Y | 254 | 29.64 | 29.74 | 30.07 | 30.08 | 7.6K |
| DISPLAYX | 254 | -95.92 | -95.60 | -95.43 | -95.42 | -24.3K |

## who

STNAME by rows
         7  Bissonnet
         7  Bellaire
         6  Clay
         6  Westpark
         6  Greenhouse
         6  Gulfton
         5  Katyland
         5  Kieth Harrow
         5  Franz
         4  Briar Forest
         4  Sam Houston
         4  Cook
         3  Rookin
         3  Kipp Way
         3  Richmond
         3  Braeswood
         3  Ridgecrest
         3  Synott
         3  High Star
         3  Little York

STNAME by dollars
         692        7 rows  Bissonnet
      688.63        7 rows  Bellaire
         600        6 rows  Greenhouse
      598.53        6 rows  Clay
      598.35        6 rows  Gulfton
      593.07        6 rows  Westpark
      498.59        5 rows  Kieth Harrow
      497.22        5 rows  Katyland
      490.94        5 rows  Franz
         400        4 rows  Sam Houston
      398.61        4 rows  Cook
         397        4 rows  Briar Forest
         300        3 rows  Synott
      299.01        3 rows  Braeswood
      298.02        3 rows  Little York
      297.03        3 rows  Rookin
         297        3 rows  Ridgecrest
         297        3 rows  High Star
      296.93        3 rows  Richmond
      296.34        3 rows  Fern

USER_SCH13 by rows
        54  www.houstonisd.org
        44  www.aliefisd.net
        36  www.katyisd.org/
        20  www.cfisd.net
         7  www.kipptexas.org
         4  www.wallerisd.net
         4  www.swschools.org
         3  www.tomballisd.net
         2  westparkk8.iltexas.org
         2  katyk8.iltexas.org
         2  www.cnchs.net
         1  hse.springbranchisd.com
         1  gulfton.yesprep.org
         1  hsacypress.harmonytx.org/
         1  www.hcde-texas.org
         1  sbai.springbranchisd.com
         1  bce.springbranchisd.com
         1  wais.springbranchisd.com
         1  sfm.springbranchisd.com
         1  lls.springbranchisd.com

USER_SCH13 by dollars
        5.4K       54 rows  www.houstonisd.org
        4.4K       44 rows  www.aliefisd.net
        3.6K       36 rows  www.katyisd.org/
        2.0K       20 rows  www.cfisd.net
      672.66        7 rows  www.kipptexas.org
         400        4 rows  www.swschools.org
      390.40        4 rows  www.wallerisd.net
         299        3 rows  www.tomballisd.net
         200        2 rows  www.cnchs.net
      194.05        2 rows  westparkk8.iltexas.org
      190.94        2 rows  katyk8.iltexas.org
         100        1 rows  mwe.springbranchisd.com
         100        1 rows  www.alief.isd.net
         100        1 rows  amcsmontessori.org
         100        1 rows  houstonclassical.org
         100        1 rows  hehouston.harmonytx.org/
         100        1 rows  hsahouston.harmonytx.org
         100        1 rows  ewe.springbranchisd.com
         100        1 rows  www.aristoiclassical.org
         100        1 rows  hsshouston.harmonytx.org

SUBREGION by rows
       254  Harris County

SUBREGION by dollars
       25.2K      254 rows  Harris County

BUFF_DIST by rows
       254  1319.9973599999996

BUFF_DIST by dollars
       25.2K      254 rows  1319.9973599999996

## who x when

STNAME by USER_UPDAT, dollars = SCORE
  Bellaire                                  2023:688.63
  Bissonnet                                 2023:692
  Braeswood                                 2023:299.01
  Briar Forest                              2023:397
  Clay                                      2023:598.53
  Cook                                      2023:398.61
  Fern                                      2023:296.34
  Franz                                     2023:490.94
  Greenhouse                                2023:600
  Gulfton                                   2023:598.35
  High Star                                 2023:297
  Katyland                                  2023:497.22
  Kieth Harrow                              2023:498.59
  Kipp Way                                  2023:285.72
  Little York                               2023:298.02
  Richmond                                  2023:296.93
  Ridgecrest                                2023:297
  Rookin                                    2023:297.03
  Sam Houston                               2023:400
  Synott                                    2023:300
  Westpark                                  2023:593.07

USER_SCH13 by USER_UPDAT, dollars = SCORE
  amcsmontessori.org                        2023:100
  bce.springbranchisd.com                   2023:100
  ewe.springbranchisd.com                   2023:100
  gulfton.yesprep.org                       2023:100
  hehouston.harmonytx.org/                  2023:100
  houstonclassical.org                      2023:100
  hsacypress.harmonytx.org/                 2023:100
  hsahouston.harmonytx.org                  2023:100
  hse.springbranchisd.com                   2023:100
  hsshouston.harmonytx.org                  2023:100
  katyk8.iltexas.org                        2023:190.94
  lls.springbranchisd.com                   2023:99
  mwe.springbranchisd.com                   2023:100
  sbai.springbranchisd.com                  2023:99
  sfm.springbranchisd.com                   2023:99
  wais.springbranchisd.com                  2023:99
  westparkk8.iltexas.org                    2023:194.05
  www.alief.isd.net                         2023:100
  www.aliefisd.net                          2023:4.4K
  www.aristoiclassical.org                  2023:100
  www.cfisd.net                             2023:2.0K
  www.cnchs.net                             2023:200
  www.hcde-texas.org                        2023:99
  www.houstonisd.org                        2023:5.4K
  www.katyisd.org/                          2023:3.6K
  www.kipptexas.org                         2023:672.66
  www.swschools.org                         2023:400
  www.tomballisd.net                        2023:299
  www.wallerisd.net                         2023:390.40

## what

STATUS: M 99%, T 1%

ADDR_TYPE: PointAddress 82%, StreetAddress 15%, StreetName 1%, Subaddress 1%, StreetAddressExt 1%, Postal 0%, PostalLoc 0%

PLACENAME: 77493 50%, 77494 50%

ADDNUMFROM: 1726 29%, 25749 12%, 24398 12%, 31237 6%, 20944 6%, 19409 6%, 2124 6%, 17986 6%, 20125 6%, 2500 6%, 5364 6%

ADDNUMTO: 1752 29%, 25569 12%, 24348 12%, 31189 6%, 20964 6%, 19499 6%, 2298 6%, 17932 6%, 20361 6%, 2572 6%, 5360 6%

ADDRANGE: 1726-1752 29%, 25569-25749 12%, 24348-24398 12%, 31189-31237 6%, 20944-20964 6%, 19409-19499 6%, 2124-2298 6%, 17932-17986 6%, 20125-20361 6%, 2500-2572 6%, 5360-5364 6%

SIDE: R 57%, L 43%

STPREDIR: W 43%, S 38%, N 14%, E 5%

STTYPE: Dr 33%, Rd 31%, St 15%, Blvd 10%, Ln 6%, Pkwy 3%, Ave 1%, Trl 1%, Way 0%, Fwy 0%

STDIR: S 80%, W 20%

UNITTYPE: Ste 100%

UNITNAME: 200 100%

SUBADDR: Ste 200 100%

NBRHD: Sharpstown 19%, Gulfton 19%, Mid-West 19%, Alief 12%, Spring Branch East 6%, West Memorial 6%, Briar Forest 6%, Westwood 6%, Eldridge/West Oaks 6%

CITY: Houston 72%, Katy 24%, Tomball 2%, Waller 1%, Hockley 1%, Cypress 0%

METROAREA: Houston-Galveston Metro Area 100%

POSTAL: 77449 16%, 77493 11%, 77074 10%, 77099 10%, 77081 9%, 77072 9%, 77084 8%, 77083 6%, 77079 5%, 77450 5%, 77082 5%, 77063 4%

EXINFO: TRAVIS COUNTY 33%, DALLAS COUNTY 17%, WALLER COUNTY 12%, 0159 8%, 31502 | WALLER COUNTY 4%, COUNTY 4%, TAYLOR COUNTY 4%, 77449 4%, 7400 INNOVATION DR 4%, 77494 4%, 27500 FULSHEAR BEND DR 4%

IN_CITY: HOUSTON 72%, KATY 24%, TOMBALL 2%, WALLER 1%, HOCKLEY 1%, CYPRESS 0%

IN_SUBREGI: HARRIS COUNTY 92%, TRAVIS COUNTY 3%, WALLER COUNTY 2%, DALLAS COUNTY 2%, TAYLOR COUNTY 0%, ERATH COUNTY 0%, BEXAR COUNTY 0%

USER_COUNT: 101 92%, 227 3%, 237 2%, 57 2%, 221 0%, 72 0%, 15 0%

USER_COU_1: HARRIS COUNTY 92%, TRAVIS COUNTY 3%, WALLER COUNTY 2%, DALLAS COUNTY 2%, TAYLOR COUNTY 0%, ERATH COUNTY 0%, BEXAR COUNTY 0%

USER_ESC_R: 4 97%, 10 2%, 14 0%, 11 0%, 20 0%

USER_ESC_1: 4 97%, 10 2%, 14 0%, 11 0%, 20 0%

USER_ESC_2: 4 94%, 13 3%, 10 2%, 14 0%, 11 0%, 20 0%

USER_DISTR: 101912 24%, 101903 21%, 101914 20%, 101907 10%, 101920 10%, 227820 4%, 237904 2%, 101846 2%, 101921 2%, 101858 2%, 101838 2%, 101802 2%

USER_DIS_1: HOUSTON ISD 24%, ALIEF ISD 21%, KATY ISD 20%, CYPRESS-FAIRBANKS ISD 10%, SPRING BRANCH ISD 10%, KIPP TEXAS PUBLIC SCHOOLS 4%, WALLER ISD 2%, HARMONY PUBLIC SCHOOLS - HOUST 2%, TOMBALL ISD 2%, HARMONY PUBLIC SCHOOLS - HOUST 2%, SOUTHWEST PUBLIC SCHOOLS 2%, SER-NINOS CHARTER SCHOOL 2%

USER_DIS_2: INDEPENDENT 80%, CHARTER 20%

USER_NCES: 4823640 24%, 4807830 21%, 4825170 20%, 4816110 10%, 4841100 10%, 4800264 4%, 4844430 2%, 4800210 2%, 4842960 2%, 4800274 2%, 4800125 2%, 4800018 2%

USER_DIS_3: 4400 W 18TH ST 24%, P O BOX 68 21%, P O BOX 159 20%, P O BOX 692003 10%, 955 CAMPBELL RD 10%, 10711 KIPP WAY 4%, 2214 WALLER ST 2%, 13522 W AIRPORT BLVD 2%, 310 S CHERRY ST 2%, 9321 W SAM HOUSTON PKWY S 2%, 3333 BERING DR STE 200 2%, 5815 ALDER DR 2%

USER_DIS_4: HOUSTON 52%, KATY 20%, ALIEF 19%, WALLER 2%, SUGAR LAND 2%, TOMBALL 2%, RICHARDSON 2%, BELLAIRE 1%, LEWISVILLE 1%, SAN ANTONIO 0%

USER_DIS_6: 77092-8501 23%, 77411-0068 20%, 77492-0159 20%, 77269-2003 10%, 77024-2803 9%, 77099 6%, 77081 3%, 77484 2%, 77478 2%, 77375-6668 2%, 77057 2%, 75082 2%

USER_DIS_7: 4400 W 18TH ST 24%, 4250 COOK RD 21%, 6301 S STADIUM LN 20%, 10300 JONES RD 10%, 955 CAMPBELL RD 10%, 10711 KIPP WAY 4%, 2214 WALLER ST 2%, 13522 W AIRPORT BLVD 2%, 310 S CHERRY ST 2%, 3203 N SAM HOUSTON PKWY W 2%, 3333 BERING DR STE 200 2%, 5815 ALDER DR 2%

USER_DIS_8: HOUSTON 71%, KATY 20%, WALLER 2%, SUGAR LAND 2%, TOMBALL 2%, RICHARDSON 2%, BELLAIRE 1%, LEWISVILLE 1%, SAN ANTONIO 0%

USER_DIS10: 77092-8501 24%, 77072-1115 20%, 77494-1057 20%, 77065-4208 10%, 77024-2803 10%, 77099 4%, 77081 3%, 77484 2%, 77478 2%, 77375-6668 2%, 77038 2%, 77057 2%

USER_DIS11: (713) 556-6005 24%, (281) 498-8110 20%, (281) 396-6000 20%, (281) 897-4000 10%, (713) 464-1511 10%, (713) 343-3333 4%, (832) 328-1051 3%, (936) 931-3685 2%, (281) 357-3100 2%, (713) 784-6345 2%, (713) 667-6145 2%, (972) 479-9078 2%

USER_DIS12: (713) 556-6006 24%, (281) 575-1923 20%, (281) 644-1800 20%, (281) 897-4125 10%, (713) 251-9186 10%, (713) 777-8555 4%, (832) 328-1051 3%, (936) 310-6589 2%, (281) 357-3128 2%, (713) 974-3137 2%, (713) 667-0645 2%, (972) 479-9129 2%

USER_DIS13: HISDSuperintendent@houstonisd. 24%, ilene.avila@aliefisd.net 20%, kennethgregorski@katyisd.org 20%, holly.reichert@cfisd.net 10%, cheryl.jeffers@springbranchisd 10%, superintendent.office@harmonyt 4%, Sehba.Ali@KIPPTexas.org 3%, kmoran@wallerisd.net 2%, marthasalazarzamora@tomballisd 2%, fadams@swschools.org 2%, Charmconst@aol.com 2%, econger@iltexas.org 2%

USER_DIS14: www.houstonisd.org 24%, www.aliefisd.net 20%, www.katyisd.org/ 20%, www.cfisd.net 10%, www.springbranchisd.com 10%, www.harmonytx.org 4%, www.kipptexas.org 3%, www.wallerisd.net 2%, www.tomballisd.net 2%, www.swschools.org 2%, www.serninos.org/ 2%, www.iltexas.org/ 2%

USER_DIS15: MR MILLARD L HOUSE II 24%, DR ANTHONY MAYS 20%, DR KENNETH GREGORSKI 20%, DR MARK HENRY 10%, DR JENNIFER BLAINE 10%, MR FATIH AY 4%, MS SEHBA ALI 3%, KEVIN MORAN 2%, DR MARTHA SALAZAR-ZAMORA 2%, DR FELICIA ADAMS 2%, MS CHARMAINE CONSTANTINE 2%, MR EDWARD CONGER 2%

USER_DIS16: 189934 24%, 40329 21%, 92667 20%, 118010 10%, 33649 10%, 33068 4%, 8834 2%, 3501 2%, 21426 2%, 6731 2%, 1578 2%, 1113 2%

USER_INSTR: REGULAR INSTRUCTIONAL 92%, ALTERNATIVE INSTRUCTIONAL 6%, DAEP INSTRUCTIONAL 2%, JJAEP INSTRUCTIONAL 1%

USER_CHART: OPEN ENROLLMENT CHARTER 88%, CAMPUS CHARTER 12%

USER_AEA: N 97%, Y 3%

USER_MAGNE: N 94%, Y 6%

USER_RESID: N 98%, Y 2%

USER_SCH_3: HOUSTON 69%, KATY 24%, WALLER 2%, TOMBALL 2%, BELLAIRE 1%, LEWISVILLE 1%, ALIEF 1%, HOCKLEY 0%, CYPRESS 0%, SAN ANTONIO 0%

USER_SCH_7: HOUSTON 72%, KATY 24%, TOMBALL 2%, WALLER 1%, HOCKLEY 1%, CYPRESS 0%

USER_GRADE: EE-05 37%, 06-08 15%, 09-12 13%, EE-04 12%, PK-05 5%, 06-12 4%, 07-08 3%, KG-05 3%, 05-06 3%, KG-12 2%, EE-12 2%, PK-08 1%

USER_SCH16: Active 99%, Under Construction 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | other | 253 | 0 | 254 2; 253 2; 252 2; 251 2 |
| OBJECTID | other | 247 | 0 | 9214 2; 9212 2; 9207 2; 9206 2 |
| STATUS | category | 2 | 0 | M 252; T 2 |
| SCORE | amount | 36 | 0 | 100.0 145; 99.0 58; 99.01 7; 97.14 3 |
| MATCH_TYPE | other | 1 | 0 | A 254 |
| MATCH_ADDR | other | 234 | 0 | 6700 Bellaire Blvd, Houst 4; 10711 Kipp Way Dr, Housto 4; 14400 Fern Dr, Houston, T 3; 1732 Katyland Dr, Katy, T 3 |
| LONGLABEL | other | 232 | 0 | 6700 Bellaire Blvd, Houst 4; 10711 Kipp Way Dr, Housto 4; 14400 Fern Dr, Houston, T 3; 1732 Katyland Dr, Katy, T 3 |
| SHORTLABEL | other | 240 | 0 | 6700 Bellaire Blvd 4; 10711 Kipp Way Dr 4; 14400 Fern Dr 3; 1732 Katyland Dr 3 |
| ADDR_TYPE | category | 7 | 0 | PointAddress 208; StreetAddress 38; StreetName 2; Subaddress 2 |
| TYPE | empty | 1 | 254 |  |
| PLACENAME | category | 3 | 252 | 77493 1; 77494 1 |
| PLACE_ADDR | other | 234 | 0 | 6700 Bellaire Blvd, Houst 4; 10711 Kipp Way Dr, Housto 4; 14400 Fern Dr, Houston, T 3; 1732 Katyland Dr, Katy, T 3 |
| PHONE | empty | 1 | 254 |  |
| URL | empty | 1 | 254 |  |
| RANK | amount | 3 | 0 | 20.0 252; 4.5 1; 6.5 1 |
| ADDBLDG | empty | 1 | 254 |  |
| ADDNUM | other | 230 | 4 | 6700 4; 10711 4; 1732 3; 5610 3 |
| ADDNUMFROM | category | 35 | 214 | 1726 5; 25749 2; 24398 2; 31237 1 |
| ADDNUMTO | category | 35 | 214 | 1752 5; 25569 2; 24348 2; 31189 1 |
| ADDRANGE | category | 35 | 214 | 1726-1752 5; 25569-25749 2; 24348-24398 2; 31189-31237 1 |
| SIDE | category | 3 | 208 | R 26; L 20 |
| STPREDIR | category | 5 | 233 | W 9; S 8; N 3; E 1 |
| STPRETYPE | empty | 1 | 254 |  |
| STNAME | who | 159 | 2 | Bellaire 7; Bissonnet 7; Westpark 6; Clay 6 |
| STTYPE | category | 11 | 3 | Dr 83; Rd 77; St 38; Blvd 24 |
| STDIR | category | 3 | 249 | S 4; W 1 |
| BLDGTYPE | empty | 1 | 254 |  |
| BLDGNAME | empty | 1 | 254 |  |
| LEVELTYPE | empty | 1 | 254 |  |
| LEVELNAME | empty | 1 | 254 |  |
| UNITTYPE | category | 2 | 252 | Ste 2 |
| UNITNAME | category | 2 | 252 | 200 2 |
| SUBADDR | category | 2 | 252 | Ste 200 2 |
| STADDR | other | 239 | 2 | 6700 Bellaire Blvd 4; 10711 Kipp Way Dr 4; 14400 Fern Dr 3; 1732 Katyland Dr 3 |
| BLOCK | empty | 1 | 254 |  |
| SECTOR | empty | 1 | 254 |  |
| NBRHD | category | 10 | 238 | Sharpstown 3; Gulfton 3; Mid-West 3; Alief 2 |
| DISTRICT | empty | 1 | 254 |  |
| CITY | category | 6 | 0 | Houston 183; Katy 61; Tomball 4; Waller 3 |
| METROAREA | category | 2 | 209 | Houston-Galveston Metro A 45 |
| SUBREGION | who | 1 | 0 | Harris County 254 |
| REGION | other | 1 | 0 | Texas 254 |
| REGIONABBR | other | 1 | 0 | TX 254 |
| TERRITORY | empty | 1 | 254 |  |
| ZONE | empty | 1 | 254 |  |
| POSTAL | category | 34 | 0 | 77449 29; 77493 21; 77074 19; 77099 18 |
| POSTALEXT | other | 170 | 63 | 1751 5; 4906 3; 2675 3; 5943 2 |
| COUNTRY | other | 1 | 0 | USA 254 |
| LANGCODE | other | 1 | 0 | ENG 254 |
| DISTANCE | amount | 8 | 0 | 0.0 247; 304428.01099611 1; 299151.11551188 1; 300883.59311344 1 |
| X | amount | 234 | 0 | -95.8109727 5; -95.50234354 4; -95.565375 4; -95.60080272 3 |
| Y | amount | 237 | 0 | 29.70547759 4; 29.67095048 4; 29.77557551 3; 29.79599647 3 |
| DISPLAYX | amount | 234 | 0 | -95.8109727 5; -95.502366 4; -95.565375 4; -95.600592 3 |
| DISPLAYY | amount | 237 | 0 | 29.705778 4; 29.669976 4; 29.776221 3; 29.79599647 3 |
| XMIN | amount | 232 | 0 | -95.8119727 5; -95.503366 4; -95.566375 4; -95.601592 3 |
| XMAX | amount | 229 | 0 | -95.8099727 5; -95.501366 4; -95.564375 4; -95.599592 3 |
| YMIN | amount | 237 | 0 | 29.704778 4; 29.668976 4; 29.775221 3; 29.79499647 3 |
| YMAX | amount | 237 | 0 | 29.706778 4; 29.670976 4; 29.777221 3; 29.79699647 3 |
| EXINFO | category | 19 | 223 | TRAVIS COUNTY 8; DALLAS COUNTY 4; WALLER COUNTY 3; 0159 2 |
| IN_ADDRESS | other | 240 | 0 | 6700 BELLAIRE BLVD 4; 10711 KIPP WAY ST 3; 14400 FERN 3; 1732 KATYLAND DR 3 |
| IN_ADDRE_1 | empty | 1 | 254 |  |
| IN_ADDRE_2 | empty | 1 | 254 |  |
| IN_NEIGHBO | empty | 1 | 254 |  |
| IN_CITY | category | 6 | 0 | HOUSTON 183; KATY 61; TOMBALL 4; WALLER 3 |
| IN_SUBREGI | category | 7 | 0 | HARRIS COUNTY 234; TRAVIS COUNTY 8; WALLER COUNTY 5; DALLAS COUNTY 4 |
| IN_REGION | other | 1 | 0 | TX 254 |
| IN_POSTAL | other | 160 | 0 | 77449 20; 77099 13; 77493 13; 77074 10 |
| IN_POSTALE | empty | 1 | 254 |  |
| IN_COUNTRY | empty | 1 | 254 |  |
| USER_COUNT | category | 7 | 0 | 101 234; 227 8; 237 5; 57 4 |
| USER_COU_1 | category | 7 | 0 | HARRIS COUNTY 234; TRAVIS COUNTY 8; WALLER COUNTY 5; DALLAS COUNTY 4 |
| USER_ESC_R | category | 5 | 0 | 4 247; 10 4; 14 1; 11 1 |
| USER_ESC_1 | category | 5 | 0 | 4 247; 10 4; 14 1; 11 1 |
| USER_ESC_2 | category | 6 | 0 | 4 239; 13 8; 10 4; 14 1 |
| USER_DISTR | category | 28 | 0 | 101912 55; 101903 47; 101914 46; 101907 23 |
| USER_DIS_1 | category | 28 | 0 | HOUSTON ISD 55; ALIEF ISD 47; KATY ISD 46; CYPRESS-FAIRBANKS ISD 23 |
| USER_DIS_2 | category | 2 | 0 | INDEPENDENT 203; CHARTER 51 |
| USER_NCES | category | 28 | 0 | 4823640 55; 4807830 47; 4825170 46; 4816110 23 |
| USER_DIS_3 | category | 26 | 0 | 4400 W 18TH ST 55; P O BOX 68 47; P O BOX 159 46; P O BOX 692003 23 |
| USER_DIS_4 | category | 10 | 0 | HOUSTON 133; KATY 50; ALIEF 47; WALLER 5 |
| USER_DIS_5 | other | 1 | 0 | TX 254 |
| USER_DIS_6 | category | 24 | 0 | 77092-8501 55; 77411-0068 47; 77492-0159 46; 77269-2003 23 |
| USER_DIS_7 | category | 27 | 0 | 4400 W 18TH ST 55; 4250 COOK RD 47; 6301 S STADIUM LN 46; 10300 JONES RD 23 |
| USER_DIS_8 | category | 9 | 0 | HOUSTON 180; KATY 50; WALLER 5; SUGAR LAND 5 |
| USER_DIS_9 | other | 1 | 0 | TX 254 |
| USER_DIS10 | category | 25 | 0 | 77092-8501 55; 77072-1115 47; 77494-1057 46; 77065-4208 23 |
| USER_DIS11 | category | 26 | 0 | (713) 556-6005 55; (281) 498-8110 47; (281) 396-6000 46; (281) 897-4000 23 |
| USER_DIS12 | category | 26 | 0 | (713) 556-6006 55; (281) 575-1923 47; (281) 644-1800 46; (281) 897-4125 23 |
| USER_DIS13 | category | 26 | 0 | HISDSuperintendent@housto 55; ilene.avila@aliefisd.net 47; kennethgregorski@katyisd. 46; holly.reichert@cfisd.net 23 |
| USER_DIS14 | category | 26 | 0 | www.houstonisd.org 55; www.aliefisd.net 47; www.katyisd.org/ 46; www.cfisd.net 23 |
| USER_DIS15 | category | 26 | 0 | MR MILLARD L HOUSE II 55; DR ANTHONY MAYS 47; DR KENNETH GREGORSKI 46; DR MARK HENRY 23 |
| USER_DIS16 | category | 28 | 0 | 189934 55; 40329 47; 92667 46; 118010 23 |
| USER_SCHOO | other | 254 | 0 | 237904108 2; 237904002 2; 237904043 2; 237904102 2 |
| USER_SCH_1 | other | 255 | 0 | NEW EL 2; WALLER H S 2; SCHULTZ J H 2; I T HOLLEMAN EL 2 |
| USER_INSTR | category | 4 | 0 | REGULAR INSTRUCTIONAL 233; ALTERNATIVE INSTRUCTIONAL 14; DAEP INSTRUCTIONAL 5; JJAEP INSTRUCTIONAL 2 |
| USER_CHART | category | 3 | 196 | OPEN ENROLLMENT CHARTER 51; CAMPUS CHARTER 7 |
| USER_AEA | category | 2 | 0 | N 247; Y 7 |
| USER_MAGNE | category | 2 | 0 | N 238; Y 16 |
| USER_RESID | category | 2 | 0 | N 250; Y 4 |
| USER_NCE_1 | other | 248 | 0 | 0 7; 484443005073 2; 484443012000 2; 484443005072 2 |
| USER_SCH_2 | other | 230 | 0 | 6700 BELLAIRE BLVD 4; 5815 ALDER DR 4; 10711 KIPP WAY ST 3; 1732 KATYLAND DR 3 |
| USER_SCH_3 | category | 10 | 0 | HOUSTON 176; KATY 60; WALLER 4; TOMBALL 4 |
| USER_SCH_4 | other | 1 | 0 | TX 254 |
| USER_SCH_5 | other | 159 | 0 | 77449 20; 77099 14; 77493 11; 77081 9 |
| USER_SCH_6 | other | 240 | 0 | 6700 BELLAIRE BLVD 4; 10711 KIPP WAY ST 3; 14400 FERN 3; 1732 KATYLAND DR 3 |
| USER_SCH_7 | category | 6 | 0 | HOUSTON 183; KATY 61; TOMBALL 4; WALLER 3 |
| USER_SCH_8 | other | 1 | 0 | TX 254 |
| USER_SCH_9 | other | 160 | 0 | 77449 20; 77099 13; 77493 13; 77074 10 |
| USER_SCH10 | other | 241 | 2 | (281) 879-3023 4; (832) 328-1051 3; (281) 237-6350 3; (713) 773-3600 3 |
| USER_SCH11 | other | 223 | 7 | (281) 396-6000 5; (832) 328-0178 4; (713) 667-0645 4; (713) 774-0410 3 |
| USER_SCH12 | other | 239 | 0 | superintendent.office@har 7; kcottrell@wallerisd.net 2; sfletcher@wallerisd.net 2; hgates@wallerisd.net 2 |
| USER_SCH13 | who | 55 | 32 | www.houstonisd.org 54; www.aliefisd.net 44; www.katyisd.org/ 36; www.cfisd.net 20 |
| USER_SCH14 | other | 238 | 8 | CHARMAINE CONSTANTINE 3; STEPHANIE FLETCHER 2; MRS HANNAH GATES 2; MRS MICHELLE SCIBA 2 |
| USER_GRADE | category | 37 | 0 | EE-05 82; 06-08 33; 09-12 29; EE-04 26 |
| USER_SCH15 | other | 216 | 0 | 0 10; 829 3; 489 3; 676 3 |
| USER_SCH16 | category | 2 | 0 | Active 251; Under Construction 3 |
| USER_SCH17 | amount | 118 | 0 | nan 82; 1530230400000.0 8; 804556800000.0 5; 741484800000.0 4 |
| USER_UPDAT | date | 12 | 0 | 4/20/2023 5:41:29 AM 87; 4/20/2023 5:41:30 AM 55; 4/20/2023 5:41:31 AM 29; 4/20/2023 5:41:32 AM 26 |
| BUFF_DIST | who | 1 | 0 | 1319.9973599999996 254 |
| ORIG_FID | other | 253 | 0 | 254 2; 253 2; 252 2; 251 2 |
| SHAPE__AREA | amount | 239 | 0 | 680000.6535148621 4; 679529.1107959747 4; 680930.6667804718 3; 681192.6953601837 3 |
| SHAPE__LENGTH | amount | 240 | 0 | 2923.2071822008315 4; 2922.193465448022 4; 2925.2054836265643 3; 2925.7682529026306 3 |
| GEOMETRY | other | 237 | 0 | {"type": "Polygon", "coor 4; {"type": "Polygon", "coor 4; {"type": "Polygon", "coor 3; {"type": "Polygon", "coor 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:21:26.08201 254 |
| SOURCE_RUN_ID | audit | 1 | 0 | ab710b2f-2cac-4380-bfe6-0 254 |
| SRC_SHA256 | who | 1 | 0 | c142d99136606f8ad2f06462b 254 |
