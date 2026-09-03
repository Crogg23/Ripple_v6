# PORTAL_ARC_TUCSON_OPEN_DATA_B44EAD49D6

rows 66  columns 78  scan 4.8s

roles: amount 8, audit 2, category 34, date 6, empty 4, other 16, who 9

## when

LASTCHANGE
  2005        19  ##############################
  2006         1  ##
  2008         7  ###########
  2009         1  ##
  2010         3  #####
  2017         3  #####
  2018         7  ###########
  2019         2  ###
  2020         6  #########
  2021         7  ###########
  2022         7  ###########
  2023         3  #####

RECORDDATE
  1966         2  #####
  1967         1  ###
  1968         1  ###
  1969         1  ###
  1970         3  ########
  1972         1  ###
  1974         3  ########
  1980         1  ###
  1981         1  ###
  1983         3  ########
  1987         4  ###########
  1989         1  ###
  1991         2  #####
  1994         3  ########
  2002         2  #####
  2003         1  ###
  2006         1  ###
  2010         1  ###
  2011         1  ###
  2016         1  ###
  2017         4  ###########
  2018         6  ################
  2019        11  ##############################
  2020         4  ###########
  2021         5  ##############

LAST_EDITED_DATE
  2020        40  ##############################
  2021        12  #########
  2022         8  ######
  2023         6  ####

CREATED_DATE_COT
  2023        66  ##############################

LAST_EDITED_DATE_COT
  2023        66  ##############################

INGESTED_AT
  2026        66  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 66 | 188.55 | 6.5K | 31.4K | 32.5K | 546.3K |
| GISACRES | 66 | 0 | 0.15 | 0.72 | 0.75 | 12.50 |
| X_HPGN | 66 | 979.7K | 1.00M | 1.05M | 1.05M | 66.62M |
| Y_HPGN | 66 | 408.8K | 447.4K | 463.9K | 464.1K | 29.46M |
| LANDMEAS | 66 | 0.10 | 5.0K | 28.5K | 32.3K | 448.4K |
| PAGE | 65 | 0 | 24 | 6.7K | 13.2K | 44.0K |

## who

JURIS_OL by rows
        66  TUCSON

JURIS_OL by dollars
      546.3K       66 rows  TUCSON

USE_DESC by rows
        66  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
      546.3K       66 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        66  MISC REL/GVT/IN     

SPT_DESC by dollars
      546.3K       66 rows  MISC REL/GVT/IN     

PPT_DESC by rows
        66  Miscellaneous            

PPT_DESC by dollars
      546.3K       66 rows  Miscellaneous            

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:322.7K 2021:75.2K 2022:86.5K 2023:61.9K

USE_DESC by LAST_EDITED_DATE, dollars = GISAREA
  MUNICIPAL VACANT LAND                     2020:322.7K 2021:75.2K 2022:86.5K 2023:61.9K

## what

LOT_R: 4 23%, nan 19%, 1 15%, 5 10%, 3 6%, 2 6%, 15 6%, 7 4%, 13 4%, 10 4%, 26 2%

TRS_OL: 141408E 24%, 141403E 22%, 141420E 8%, 141404E 8%, 141407E 6%, 141311E 6%, 151407E 4%, 151313E 4%, 141528E 4%, 141508E 4%, 141506E 4%, 141505E 4%

MP_OL: nan 20%, 05038 14%, 07067 14%, 03010 11%, 05078 9%, 09025 5%, 44081 5%, 56084 5%, 64060 5%, 04005 5%, 03081 5%, 06007 5%

SEQ_NUM_S: nan 53%, 93060446 12%, 20030070610 12%, 20090940484 12%, 95040957 6%, 20050340091 6%

ADDRESS_OL: nan 78%, 2432 E 22ND ST 2%, 2438 E 22ND ST 2%, 2402 E 22ND ST 2%, 2302 E 22ND ST 2%, 1001 E 26TH ST 2%, 2043 E BROADWAY BL 2%, 2021 E BROADWAY BL 2%, 2009 E BROADWAY BL 2%, 2005 E BROADWAY BL 2%, 2445 E BROADWAY BL 2%, 2419 E BROADWAY BL 2%

SEQ_NUM_D: 0.0 48%, 20190160184.0 14%, nan 9%, 20170870297.0 5%, 20192400261.0 5%, 20181560584.0 5%, 20213010886.0 5%, 94036571.0 2%, 94058631.0 2%, 20022292337.0 2%, 20022150182.0 2%, 91069523.0 2%

LANDUNIT: F 83%, S 15%, A 2%

LEGAL2: 10 BLK 9 17%, EXC E10' /PAR 5 BLK H/ 8%, EXC E10' /PAR 3 BLK H/ 8%, DRAINAGEWAY EXC S250' THEREOF 8%, .04 AC SEC 13-15-13 8%, WASH DRAINAGEWAY EXC E5' & W5' 8%, OF LOT B EXC THAT PT LYG IN AL 8%, OF BLOCK 2 8%, SE4 SE4 H .18 AC SEC 28-14-15 8%, LOT 49 8%, WELLSITE 8%

LEGAL3: (RESOLUTION-ORD #5632 8/3/82) 29%, (DEED: D 7006 P 880 4-8-83) 14%, (DEED: D 7006 P 880 4-18-83) 14%, (M&P 44/81) 14%, SUBJECT TO ANY MINERAL RIGHTS 14%, EXC ALLEY BLK 1 14%

LEGAL5: (FORMERLY 139-21-4240) 50%, (FORMERLY 139-21-4220) 50%

LOT: 00004 23%, nan 19%, 00001 15%, 00005 10%, 00003 6%, 00002 6%, 00015 6%, 00007 4%, 00013 4%, 00010 4%, 00026 2%

MAIL1: CITY OF TUCSON 95%, CITY OF TUCSON REAL ESTATE DIV 3%, INDUSTRIAL DEVELOPMENT AUTHORI 2%

MAIL2: REAL ESTATE DIVISION 46%, . 35%, REAL ESTATES DIVISION 9%, ATTN: PROPERTY MANAGEMENT 3%, PO BOX 27210 3%, REAL ESTATE DIVISION  ATTN: PR 2%, CITY OF TUCSON 2%

MAIL3: . 35%, ATTN: PROPERTY MANAGEMENT 23%, PO BOX 27210 22%, ATTN: PROPERTY MANAGMENT 12%, TUCSON AZ 3%, FBO: SCF RC FUNDING IV LLC 2%, 376 S STONE AVE 2%, FBO STROMIGA 68% & ROLL-IT LLC 2%

MAIL4: PO BOX 27210 62%, TUCSON AZ 35%, TUCSON  AZ 2%

MAIL5: TUCSON AZ 100%

MP: nan 25%, 05038 14%, 07067 14%, 03010 11%, 05078 9%, 09025 5%, 44081 5%, 04005 5%, 03081 5%, 06007 5%, 04040 2%, 04041 2%

DOCKET: 0 67%, 4771 6%, 3801 4%, 6948 4%, 8166 4%, 3870 2%, 6351 2%, 3206 2%, 3511 2%, 6631 2%, 9735 2%, 9756 2%

SECTMODIF: nan 100%

TAXAREA: 0150 89%, 1250 9%, 0113 2%

ZIP: 85726 62%, 00000 36%, 85701 2%

ZIP4: 7210 62%, 0000 35%, nan 2%, 2318 2%

FCV: 500 59%, 28805 7%, 15300 3%, 39586 3%, 32931 3%, 3788 3%, 80000 3%, 58344 3%, 22297 3%, 75248 3%, 31268 3%, 28602 3%

ADDRESSEE: CITY OF TUCSON 39%, CITY OF TUCSON
REAL ESTATE DI 23%, CITY OF TUCSON
REAL ESTATE DI 12%, CITY OF TUCSON
REAL ESTATE DI 9%, CITY OF TUCSON
REAL ESTATES D 9%, CITY OF TUCSON REAL ESTATE DIV 3%, CITY OF TUCSON
REAL ESTATE DI 2%, INDUSTRIAL DEVELOPMENT AUTHORI 2%, CITY OF TUCSON
REAL ESTATE DI 2%

ADDRESS: PO BOX 27210 63%, nan 35%, 376 S STONE AVE 2%

CITY: TUCSON 63%, nan 35%, TUCSON  2%

STATE_PROVINCE: AZ 64%, nan 36%

POSTAL_CODE: 85726-7210 62%, nan 36%, 85701-2318 2%

SITE_ADDRESS: nan 78%, 2432 E 22ND ST 2%, 2438 E 22ND ST 2%, 2402 E 22ND ST 2%, 2302 E 22ND ST 2%, 1001 E 26TH ST 2%, 2043 E BROADWAY BL 2%, 2021 E BROADWAY BL 2%, 2009 E BROADWAY BL 2%, 2005 E BROADWAY BL 2%, 2445 E BROADWAY BL 2%, 2419 E BROADWAY BL 2%

SITE_ZIP: 85719 32%, 85712 29%, 85713 18%, 85716 11%, 85745 7%, 85701 4%

SITE_ZIPCITY: TUCSON 100%

ADR_STATUS: NONE 58%, ONE 41%, MULTIPLE 2%

YEARBUILT: nan 73%, 1948 5%, 1969 3%, 1990 3%, 1947 3%, 1998 2%, 1985 2%, 1960 2%, 1962 2%, 1952 2%, 1927 2%, 1953 2%

LAST_EDITED_USER: GISPARFAB 61%, JArechederra2@CENTRAL 29%, u142832@CENTRAL 8%, u153886@CENTRAL 2%, SGilpin2@CENTRAL 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 67 | 0 | 66 1; 65 1; 64 1; 63 1 |
| PARCEL | other | 67 | 0 | 140234240 1; 140234220 1; 13821030B 1; 138150110 1 |
| GISAREA | amount | 67 | 0 | 8221.80749254 1; 8220.48291489 1; 17108.12053565 1; 3139.76371219 1 |
| GISACRES | amount | 66 | 0 | 0.18873981 1; 0.18870941 1; 0.39273402 1; 0.07207642 1 |
| X_HPGN | amount | 67 | 0 | 997195.90076481 1; 997195.45776898 1; 991130.08902012 1; 993467.68736208 1 |
| Y_HPGN | amount | 66 | 0 | 414597.12524365 1; 414767.13166522 1; 408810.07174103 1; 413587.71172548 1 |
| LON | other | 67 | 0 | -110.95652439 1; -110.95652093 1; -110.97628194 1; -110.9685963 1 |
| LAT | other | 67 | 0 | 32.13617281 1; 32.1366401 1; 32.12041365 1; 32.13348913 1 |
| LOT_R | category | 23 | 7 | 4 11; nan 9; 1 7; 5 5 |
| LINK | other | 67 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 28 | 0 | 141408E 12; 141403E 11; 141420E 4; 141404E 4 |
| MP_OL | category | 34 | 0 | nan 9; 05038 6; 07067 6; 03010 5 |
| SEQ_NUM_S | category | 7 | 49 | nan 9; 93060446 2; 20030070610 2; 20090940484 2 |
| JURIS_OL | who | 1 | 0 | TUCSON 66 |
| CURZONE_OL | other | 1 | 0 | C-1 66 |
| ADDRESS_OL | category | 25 | 0 | nan 39; 2432 E 22ND ST 1; 2438 E 22ND ST 1; 2402 E 22ND ST 1 |
| SEQ_NUM_D | category | 34 | 0 | 0.0 21; 20190160184.0 6; nan 4; 20170870297.0 2 |
| PARCEL_USE | other | 1 | 0 | 9700 66 |
| LANDMEAS | amount | 55 | 0 | 0.1 8; 1.0 3; 8160.0 2; 15300.0 1 |
| LANDUNIT | category | 3 | 0 | F 55; S 10; A 1 |
| LASTCHANGE | date | 32 | 0 | 1121126400000 19; 1215388800000 6; 1635465600000 6; 1529366400000 2 |
| LEGAL1 | other | 65 | 0 | COUNTRY CLUB HOMESITES SL 2; SOUTHLAND PARK RESUB OF B 1; SOUTHLAND PARK RESUB OF B 1; VALENCIA THAT PT OF LOT 2 1 |
| LEGAL2 | category | 46 | 20 | 10 BLK 9 2; EXC E10' /PAR 5 BLK H/ 1; EXC E10' /PAR 3 BLK H/ 1; DRAINAGEWAY EXC S250' THE 1 |
| LEGAL3 | category | 7 | 59 | (RESOLUTION-ORD #5632 8/3 2; (DEED: D 7006 P 880 4-8-8 1; (DEED: D 7006 P 880 4-18- 1; (M&P 44/81) 1 |
| LEGAL4 | empty | 1 | 66 |  |
| LEGAL5 | category | 3 | 64 | (FORMERLY 139-21-4240) 1; (FORMERLY 139-21-4220) 1 |
| LOT | category | 24 | 6 | 00004 11; nan 9; 00001 7; 00005 5 |
| MAIL1 | category | 3 | 0 | CITY OF TUCSON 63; CITY OF TUCSON REAL ESTAT 2; INDUSTRIAL DEVELOPMENT AU 1 |
| MAIL2 | category | 8 | 1 | REAL ESTATE DIVISION 30; . 23; REAL ESTATES DIVISION 6; ATTN: PROPERTY MANAGEMENT 2 |
| MAIL3 | category | 9 | 1 | . 23; ATTN: PROPERTY MANAGEMENT 15; PO BOX 27210 14; ATTN: PROPERTY MANAGMENT 8 |
| MAIL4 | category | 4 | 26 | PO BOX 27210 25; TUCSON AZ 14; TUCSON  AZ 1 |
| MAIL5 | category | 2 | 41 | TUCSON AZ 25 |
| MP | category | 34 | 0 | nan 11; 05038 6; 07067 6; 03010 5 |
| PAGE | amount | 31 | 0 | 0.0 32; 399.0 3; 1001.0 2; 1978.0 2 |
| RECORDDATE | date | 49 | 0 | 20190116 6; 19740521 3; 19700803 2; 19830114 2 |
| DOCKET | category | 30 | 0 | 0 32; 4771 3; 3801 2; 6948 2 |
| RECTRACT | empty | 1 | 66 |  |
| SECTMODIF | category | 2 | 32 | nan 34 |
| TAXAREA | category | 3 | 0 | 0150 59; 1250 6; 0113 1 |
| ZIP | category | 3 | 0 | 85726 41; 00000 24; 85701 1 |
| ZIP4 | category | 4 | 0 | 7210 41; 0000 23; nan 1; 2318 1 |
| TAXYR | other | 1 | 0 | 2023 66 |
| LIMNET | other | 1 | 0 | 0 66 |
| FCV | category | 49 | 0 | 500 17; 28805 2; 15300 1; 39586 1 |
| SHAPE_LENG | empty | 1 | 66 |  |
| ADDRESSEE | category | 9 | 0 | CITY OF TUCSON 26; CITY OF TUCSON
REAL ESTA 15; CITY OF TUCSON
REAL ESTA 8; CITY OF TUCSON
REAL ESTA 6 |
| ADDRESS | category | 4 | 1 | PO BOX 27210 41; nan 23; 376 S STONE AVE 1 |
| CITY | category | 4 | 1 | TUCSON 41; nan 23; TUCSON  1 |
| STATE_PROVINCE | category | 2 | 0 | AZ 42; nan 24 |
| COUNTRY | empty | 1 | 66 |  |
| POSTAL_CODE | category | 3 | 0 | 85726-7210 41; nan 24; 85701-2318 1 |
| SITE_ADDRESS | category | 26 | 0 | nan 38; 2432 E 22ND ST 1; 2438 E 22ND ST 1; 2402 E 22ND ST 1 |
| SITE_ZIP | category | 7 | 38 | 85719 9; 85712 8; 85713 5; 85716 3 |
| SITE_ZIPCITY | category | 2 | 38 | TUCSON 28 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     66 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      66 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             66 |
| DATASOURCE | who | 1 | 0 | PAREGION 66 |
| URL | other | 67 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | other | 67 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 3 | 0 | NONE 38; ONE 27; MULTIPLE 1 |
| LEGAL_DESC | other | 66 | 0 | COUNTRY CLUB HOMESITES SL 2; SOUTHLAND PARK RESUB OF B 1; SOUTHLAND PARK RESUB OF B 1; VALENCIA THAT PT OF LOT 2 1 |
| OWN | other | 1 | 0 | City 66 |
| VAN | who | 1 | 0 | not_van 66 |
| YEARBUILT | category | 18 | 0 | nan 44; 1948 3; 1969 2; 1990 2 |
| LAST_EDITED_USER | category | 5 | 0 | GISPARFAB 40; JArechederra2@CENTRAL 19; u142832@CENTRAL 5; u153886@CENTRAL 1 |
| LAST_EDITED_DATE | date | 47 | 0 | 1648585028000 6; 1638305320000 5; 1611164013000 4; 1684191150000 4 |
| GLOBALID | other | 67 | 0 | 1b3c1c8f-441a-429b-becd-a 1; bbf5a439-46df-498f-836f-3 1; fea576b4-6bc7-415e-8c11-0 1; 30b23388-18fa-498b-bcf3-c 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 66 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 66 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 66 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 66 |
| SHAPE__AREA | amount | 67 | 0 | 1068.36328125 1; 1068.203125 1; 2222.328125 1; 407.96875 1 |
| SHAPE__LENGTH | amount | 67 | 0 | 130.9989155505193 1; 130.98837049665613 1; 227.41237036230848 1; 244.35977366233993 1 |
| GEOMETRY | other | 67 | 0 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:48:27.96061 66 |
| SOURCE_RUN_ID | audit | 1 | 0 | 74867818-5fcb-425b-94c8-2 66 |
| SRC_SHA256 | who | 1 | 0 | 1c25447930f5dc05fd8b207e3 66 |
