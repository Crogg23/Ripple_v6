# PORTAL_CKA_ISRAEL_NATIONAL_EE52E94997

rows 864  columns 24  scan 3.8s

roles: amount 3, audit 2, category 8, date 2, other 8, who 2

## when

DATE
  2006         8  ##
  2007        15  ####
  2008         7  ##
  2009        85  #########################
  2010        54  ################
  2011        31  #########
  2012        24  #######
  2013        28  ########
  2014        13  ####
  2015        26  ########
  2016        29  #########
  2017        74  ######################
  2018        61  ##################
  2019        17  #####
  2020        46  ##############
  2021        40  ############
  2022        29  #########
  2023        45  #############
  2024        57  #################
  2025       102  ##############################
  2026        72  #####################

INGESTED_AT
  2026       864  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EVENT | 864 | 1 | 25 | 122.85 | 2.0K | 28.3K |
| X | 863 | 3.87M | 3.95M | 3.99M | 3.99M | 3.41B |
| Y | 863 | 3.48M | 3.89M | 3.93M | 3.93M | 3.34B |

## who

SETTLEMENTENG by rows
        15  Yardena
        15  Menahemya
        15  Alma
        15  Majdal Shams
        13  Dan
        13  Zefat
        13  Gan Ner
        12  Ayyelet Hashahar
        12  Newe Etan
        11  Hamadya
        10  Ortal
        10  Fassuta
        10  Nir Dawid (Tel Amal)
        10  Kefar Szold
        10  Mas'Ade
         9  Buq'Ata
         9  Bet She'An
         9  Dalton
         9  Metula
         9  Shetula

SETTLEMENTENG by dollars
        2.1K        5 rows  Newe Ur
         668       15 rows  Alma
         588       12 rows  Ayyelet Hashahar
         561       13 rows  Gan Ner
         512       15 rows  Yardena
         462        6 rows  Sha'Al
         457       15 rows  Menahemya
         404        8 rows  Kefar Yehoshua
         398       10 rows  Nir Dawid (Tel Amal)
         383        4 rows  Qidmat Zevi
         374        9 rows  Merom Golan
         366       13 rows  Zefat
         339       15 rows  Majdal Shams
         327        9 rows  Dalton
         302        8 rows  Tirat Zevi
         289       13 rows  Dan
         284        9 rows  Shetula
         281       10 rows  Ortal
         279        5 rows  Yoqne'Am(Moshava)
         277       11 rows  Hamadya

SRC_SHA256 by rows
       864  564c12babbd14d3c14dd610d0abc9ecefe943fee11b9dd4526d9c2ae4bdd4d8f

SRC_SHA256 by dollars
       28.3K      864 rows  564c12babbd14d3c14dd610d0abc9ecefe943fee11b9dd4526d9c2ae4bdd

## who x when

SETTLEMENTENG by DATE, dollars = EVENT
  Alma                                      2020:17 2024:45 2025:578 2026:28
  Ayyelet Hashahar                          2008:11 2021:36 2022:5 2025:482 2026:54
  Bet She'An                                2009:106 2010:61 2017:66 2023:10 2024:2
  Buq'Ata                                   2006:9 2009:34 2014:11 2022:14 2025:23
  Dalton                                    2010:32 2020:44 2023:39 2024:28 2025:143 2026:12
  Dan                                       2007:3 2009:38 2013:18 2014:8 2017:35 2018:119 2019:15 2020:53
  Fassuta                                   2010:44 2016:14 2020:85 2022:12 2024:46 2025:1
  Gan Ner                                   2009:474 2017:82 2019:5
  Hamadya                                   2009:58 2010:89 2016:15 2017:33 2022:59 2023:23
  Kefar Szold                               2007:6 2009:108 2012:8 2015:62 2018:34 2020:17
  Kefar Yehoshua                            2013:256 2017:67 2018:81
  Majdal Shams                              2007:36 2009:49 2010:22 2011:41 2012:13 2013:117 2019:14 2024:8 2025:39
  Mas'Ade                                   2007:9 2009:71 2012:11 2013:11 2014:10 2015:60
  Menahemya                                 2009:316 2011:4 2017:2 2018:50 2024:74 2026:11
  Merom Golan                               2006:4 2007:12 2009:84 2011:28 2013:241 2014:5
  Metula                                    2009:2 2015:2 2016:54 2020:70 2023:21 2024:22
  Newe Etan                                 2010:12 2011:121 2017:46 2019:6 2023:43 2024:10
  Newe Ur                                   2009:78 2013:16 2023:26 2026:2.0K
  Nir Dawid (Tel Amal)                      2010:6 2017:72 2018:195 2024:37 2025:88
  Ortal                                     2009:62 2013:21 2021:37 2024:161
  Qidmat Zevi                               2013:383
  Sha'Al                                    2010:31 2012:18 2013:399 2014:14
  Shetula                                   2007:2 2015:65 2020:84 2021:39 2023:45 2025:49
  Tirat Zevi                                2009:215 2010:40 2018:6 2026:41
  Yardena                                   2009:77 2017:315 2018:40 2024:43 2026:37
  Yoqne'Am(Moshava)                         2017:279
  Zefat                                     2009:71 2010:168 2018:38 2025:89

SRC_SHA256 by DATE, dollars = EVENT
  564c12babbd14d3c14dd610d0abc9ecefe943fee  2006:39 2007:120 2008:41 2009:2.9K 2010:1.5K 2011:527 2012:300 2013:2.2K 2014:104 2015:377 2016:455 2017:2.8K 2018:1.8K 2019:153 2020:1.1K 2021:820 2022:435 2023:1.0K 2024:1.7K 2025:5.3K 2026:4.7K

## what

YEAR: 2025 15%, 2009 12%, 2017 11%, 2026 10%, 2018 9%, 2024 8%, 2010 8%, 2020 7%, 2023 6%, 2021 6%, 2011 4%, 2016 4%

SPECIESNAMEENG: Dog 37%, Jackal 36%, Cattle 16%, Fox 3%, Wolf 2%, Sheep 2%, Cat 2%, Badger 1%, Horse 1%, Mongoose 0%, Cow 0%

REGIONENG: Galil Golan 53%, Amakim 28%, Galil Maaravi 9%, Hasharon 6%, Shfela Vahar 2%, Negev 1%

REGIONHEB: גליל גולן 52%, עמקים 28%, גליל מערבי 10%, השרון 6%, השפלה וההר 3%, הנגב 1%

SPECIESNAMEHEB: כלב 37%, תן 35%, בקר 16%, שועל 3%, צאן 2%, זאב 2%, חתול 2%, גירית 2%, סוס 1%, נמיה 0%, חמור 0%, דלק 0%

SPECIES: VIIA 37%, VII 26%, VIIB 22%, I 4%, VII B 4%, V7 3%, VII A 2%, III 1%, V 0%, V1 0%, IV 0%

LOCATIONNOTSETTLEMENTENG: Ramat Sirin 24%, Matsok Orvim 12%, Akhuzat Shoshana 12%, Sirin 12%, Ein Hogea 6%, Beit Ha'Meches 6%, snir 6%, עין חרדלית 6%, מבואות החרמון 6%,   Ein HaNetziv 6%, Tayasir checkpoint 6%

LOCATIONNOTSETTLEMENTHEB: רמת סירין 22%, מצוק עורבים 11%, אחוזת שושנה 11%, סירין 11%, גני חוגה 11%, עין חוגע  6%, צומת בית המכס 6%, ספסופה 6%, עין חרדלית 6%, מבואות החרמון 6%, מחסום תיאסיר 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 847 | 0 | 821 5; 188 5; 204 5; 242 5 |
| ANIMAL_LAB_ID | other | 850 | 1 | A00554281 5; 503563 5;  509069 5; 509455 5 |
| EVENT | amount | 119 | 0 | 2.0 21; 7.0 21; 8.0 21; 4.0 20 |
| DATE | date | 691 | 1 | 2017-10-23 9; 2009-09-22 7; 2009-10-21 7; 2009-11-13 7 |
| LINKTOTEST | other | 548 | 314 | https://www.gov.il/files/ 4; https://www.gov.il/files/ 4; https://www.gov.il/files/ 4; https://moag.maps.arcgis. 4 |
| OPENLINK | other | 540 | 0 | <a href="<NA>" target="_b 314; <a href="https://www.gov. 4; <a href="https://www.gov. 4; <a href="https://www.gov. 4 |
| LINKTOMRE | other | 542 | 295 | https://www.gov.il/files/ 5; https://www.gov.il/files/ 4; https://www.gov.il/files/ 4; https://www.gov.il/files/ 4 |
| LINKMOREOPEN | other | 544 | 0 | <a href="<NA>" target="_b 295; <a href="https://www.gov. 5; <a href="https://www.gov. 4; <a href="https://www.gov. 4 |
| YEAR | category | 21 | 0 | 2025 102; 2009 85; 2017 74; 2026 72 |
| SPECIESNAMEENG | category | 15 | 4 | Dog 317; Jackal 304; Cattle 133; Fox 28 |
| REGIONENG | category | 7 | 2 | Galil Golan 456; Amakim 243; Galil Maaravi 80; Hasharon 50 |
| REGIONHEB | category | 7 | 3 | גליל גולן 451; עמקים 242; גליל מערבי 83; השרון 50 |
| SPECIESNAMEHEB | category | 13 | 0 | כלב 320; תן 305; בקר 134; שועל 28 |
| SPECIES | category | 12 | 18 | VIIA 310; VII 219; VIIB 188; I 38 |
| SETTLEMENTHEB | other | 270 | 16 | מג'דל שמס 15; ירדנה 15; מנחמיה 15; עלמה 15 |
| SETTLEMENTENG | who | 272 | 16 | Majdal Shams 15; Yardena 15; Menahemya 15; Alma 15 |
| LOCATIONNOTSETTLEMENTENG | category | 12 | 847 | Ramat Sirin 4; Matsok Orvim 2; Akhuzat Shoshana 2; Sirin 2 |
| LOCATIONNOTSETTLEMENTHEB | category | 12 | 846 | רמת סירין 4; מצוק עורבים 2; אחוזת שושנה 2; סירין 2 |
| GLOBALID | other | 850 | 0 | 0499a8c5-ecc2-47b1-9879-a 5; adde1e8d-ea05-457d-90c5-5 5; 2bea341e-b30d-4177-a435-e 5; fa774526-70e4-4b09-a2c4-2 5 |
| X | amount | 695 | 1 | 3981879.4062999436 15; 3951302.6175203538 14; 3933369.476578877 13; 3982616.464337035 11 |
| Y | amount | 708 | 1 | 3931025.170399642 15; 3891363.4127191687 14; 3832680.0248219124 13; 3912788.9838301153 11 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:23:35.57778 864 |
| SOURCE_RUN_ID | audit | 1 | 0 | 67963efc-6fcd-4d9d-9018-d 864 |
| SRC_SHA256 | who | 1 | 0 | 564c12babbd14d3c14dd610d0 864 |
