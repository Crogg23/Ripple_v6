# PORTAL_ARC_TUCSON_OPEN_DATA_28F95EBB76

rows 23  columns 78  scan 5.1s

roles: amount 7, audit 2, category 45, date 6, empty 4, other 5, who 10

## when

LASTCHANGE
  2005        10  ##############################
  2007         2  ######
  2008         4  ############
  2010         1  ###
  2017         5  ###############
  2020         1  ###

RECORDDATE
  1966         2  ####################
  1969         2  ####################
  1986         1  ##########
  1991         1  ##########
  1995         3  ##############################
  1997         2  ####################
  1999         1  ##########
  2000         1  ##########
  2001         3  ##############################
  2015         1  ##########
  2017         2  ####################

LAST_EDITED_DATE
  2020        19  ##############################
  2021         4  ######

CREATED_DATE_COT
  2023        23  ##############################

LAST_EDITED_DATE_COT
  2023        23  ##############################

INGESTED_AT
  2026        23  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 23 | 1.2K | 6.0K | 78.9K | 97.6K | 225.3K |
| GISACRES | 23 | 0.03 | 0.14 | 1.81 | 2.24 | 5.17 |
| X_HPGN | 23 | 987.6K | 992.6K | 1.01M | 1.01M | 22.84M |
| Y_HPGN | 23 | 421.7K | 445.7K | 468.5K | 470.1K | 10.25M |
| LANDMEAS | 23 | 0.10 | 5.9K | 90.1K | 112.1K | 236.5K |
| SHAPE__AREA | 23 | 155.12 | 787.71 | 10.3K | 12.7K | 29.3K |

## who

JURIS_OL by rows
        23  TUCSON

JURIS_OL by dollars
      225.3K       23 rows  TUCSON

MAIL1 by rows
        23  CITY OF TUCSON

MAIL1 by dollars
      225.3K       23 rows  CITY OF TUCSON

USE_DESC by rows
        23  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
      225.3K       23 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        23  MISC REL/GVT/IN     

SPT_DESC by dollars
      225.3K       23 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:113.0K 2021:112.3K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:113.0K 2021:112.3K

## what

OBJECTID: 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%

PARCEL: 13705509A 8%, 13705507A 8%, 124171920 8%, 124062390 8%, 124062380 8%, 124062350 8%, 117091960 8%, 117091550 8%, 117091510 8%, 117072040 8%, 117042280 8%, 11704225B 8%

LON: -110.98693839 8%, -110.9872525 8%, -110.95359341 8%, -110.95567135 8%, -110.95587629 8%, -110.95599387 8%, -110.96894415 8%, -110.9680454 8%, -110.96804663 8%, -110.96917334 8%, -110.97047562 8%, -110.97077546 8%

LAT: 32.1559454 8%, 32.15653249 8%, 32.21327468 8%, 32.2216471 8%, 32.22152898 8%, 32.22173443 8%, 32.20725806 8%, 32.20703426 8%, 32.20728149 8%, 32.21243852 8%, 32.22790604 8%, 32.22808754 8%

LOT_R: 9 19%, 1 14%, 12 14%, 11 10%, nan 10%, 7 5%, 16 5%, 4 5%, 2 5%, 15 5%, 8 5%, 22 5%

LINK: HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%

TRS_OL: 141312E 30%, 141313E 17%, 141407E 13%, 151302E 9%, 141314E 9%, 141311E 9%, 141418E 4%, 131428E 4%, 131324E 4%

MP_OL: 03071 23%, 01004 14%, 63054 9%, 02004 9%, 01003 9%, 01023 9%, 04081 5%, 02024 5%, 05055 5%, 04037 5%, nan 5%, 05046 5%

SEQ_NUM_S: 20080560074 67%, nan 33%

ADDRESS_OL: nan 52%, 1025 E BROADWAY BL 4%, 1003 E BROADWAY BL 4%, 10 N PARK AV 4%, 1128 S 6TH AV 4%, 1133 S 6TH AV 4%, 41 E 6TH ST 4%, 512 N ECHOLS AV 4%, 25 E 6TH ST 4%, 509 N 7TH AV 4%, 503 N STONE AV 4%, 523 W SPEEDWAY BL 4%

SEQ_NUM_D: 0 39%, 20011600631 13%, 97064010 9%, 20171020456 9%, 95145751 4%, 95018114 4%, 95022288 4%, 20151270557 4%, 20001380419 4%, 19991360588 4%, 91033626 4%

LANDUNIT: F 91%, A 9%

LEGAL1: PARQUE DE SANTA CRUZ RESUB 15%, BRUCKNERS N30'  LOT 16 BLK 32 8%, BUELLS PT L 4 & E 10' OF L 3 L 8%, BUELLS S 65' OF N 150' OF E 28 8%, BUELLS N85' LOTS 1 & 2 & N85'  8%, ROSENFELDS RESUB TUCSON BLK 16 8%, TUCSON LOT 15 BLK 166 8%, TUCSON LOT 11 BLK 166 8%, TUCSON PT L 8 & 9 LYG W OF STO 8%, TUCSON E2 OF LOT 12 BLK 58 8%, TUCSON N44' W2 OF LOT 9 BLK 58 8%, TUCSON W2 OF LOT 9 & 12 EXC N4 8%

LEGAL2: BLK 2 18%, ELY PTN LOT 9 9%, ELY PTN LOT 7 9%, BLK 42 9%, N150' OF W40' OF LOT 3 BLK 42 9%, BLK 121 9%, ST & S48' M/L OF BLK 7 MT VIEW 9%, OF MAIN ST & PART OF BLK 7 MT  9%, OF LOT 12 BLK 1 EXC RD 9%, LOT 1 EXC RILLITO RIVER & PT O 9%

LEGAL3: PART FOR RDS 25%, WLY PT FOR RD 25%, (PROC 2177 BK 17 PG 43 D R E B 25%, LOT 4 25%

LEGAL4: (DRNGWY 6590/805) 100%

LOT: 00009 19%, 00001 14%, 00012 14%, 00011 10%, nan 10%, 00007 5%, 00016 5%, 00004 5%, 00002 5%, 00015 5%, 00008 5%, 00022 5%

MAIL2: . 65%, REAL ESTATE DIVISION 35%

MAIL3: . 65%, ATTN: PROPERTY MANAGMENT 22%, ATTN: PROPERTY MANAGEMENT 13%

MAIL4: PO BOX 27210 100%

MAIL5: TUCSON AZ 75%, TUCSON  AZ 25%

MP: 03071 22%, 03069 13%, 02004 13%, 32038 9%, 02003 9%, 01023 9%, 04081 4%, 02024 4%, 04037 4%, nan 4%, 05046 4%, 03008 4%

PAGE: 3027 16%, 0 16%, 527 11%, 1271 11%, 51 11%, 404 5%, 2194 5%, 1213 5%, 1194 5%, 598 5%, 419 5%, 343 5%

DOCKET: 11615 16%, 0 16%, 31 11%, 10533 11%, 2683 11%, 76 5%, 10135 5%, 9976 5%, 9982 5%, 26 5%, 3576 5%, 3586 5%

SECTMODIF: nan 100%

TAXAREA: 0150 87%, 1250 9%, 1050 4%

ZIP: 00000 65%, 85726 35%

ZIP4: 0000 65%, 7210 35%

FCV: 4356 8%, 8276 8%, 16816 8%, 80737 8%, 39813 8%, 107457 8%, 78032 8%, 78817 8%, 77239 8%, 61870 8%, 48967 8%, 24437 8%

ADDRESSEE: CITY OF TUCSON 65%, CITY OF TUCSON
REAL ESTATE DI 22%, CITY OF TUCSON
REAL ESTATE DI 13%

ADDRESS: nan 43%, PO BOX 27210 35%, 1128 S 6TH AV 4%, 1133 S 6TH AV 4%, 41 E 6TH ST 4%, 509 N 7TH AV 4%, 523 W SPEEDWAY BL 4%

CITY: nan 65%, TUCSON 26%, TUCSON  9%

STATE_PROVINCE: nan 65%, AZ 35%

POSTAL_CODE: nan 65%, 85726-7210 35%

SITE_ADDRESS: nan 50%, 1025 E BROADWAY BL 5%, 1003 E BROADWAY BL 5%, 10 N PARK AV 5%, 1128 S 6TH AV 5%, 1149 S 6TH AV 5%, 1133 S 6TH AV 5%, 41 E 6TH ST 5%, 512 N ECHOLS AV 5%, 25 E 6TH ST 5%, 509 N 7TH AV 5%, 503 N STONE AV 5%

SITE_ZIP: 85705 50%, 85719 25%, 85701 25%

SITE_ZIPCITY: TUCSON 100%

URL: https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%

URL2: http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%

ADR_STATUS: NONE 48%, ONE 48%, MULTIPLE 4%

LEGAL_DESC: PARQUE DE SANTA CRUZ RESUB; EL 8%, PARQUE DE SANTA CRUZ RESUB; EL 8%, BRUCKNERS N30'  LOT 16 BLK 32 8%, BUELLS PT L 4 & E 10' OF L 3 L 8%, BUELLS S 65' OF N 150' OF E 28 8%, BUELLS N85' LOTS 1 & 2 & N85'  8%, ROSENFELDS RESUB TUCSON BLK 16 8%, TUCSON LOT 15 BLK 166 8%, TUCSON LOT 11 BLK 166 8%, TUCSON PT L 8 & 9 LYG W OF STO 8%, TUCSON E2 OF LOT 12 BLK 58 8%, TUCSON N44' W2 OF LOT 9 BLK 58 8%

YEARBUILT: nan 65%, 1965 4%, 1935 4%, 1957 4%, 1969 4%, 1954 4%, 1910 4%, 1961 4%, 1930 4%

LAST_EDITED_USER: GISPARFAB 83%, u142832@CENTRAL 13%, u152243@CENTRAL 4%

GLOBALID: 51ad829c-fb4d-4b8b-820a-26da30 8%, 374f4130-b4a5-4454-aba6-eb5c0f 8%, 04cb1ac1-2505-4643-af97-5e0cb2 8%, 2c535f67-0301-44de-a6c6-469be2 8%, a21482ad-1022-4999-92f8-ec6800 8%, 1c22b961-0897-463c-9f44-a99e53 8%, 24e50e88-30ff-4747-a454-b4413e 8%, a401024c-795d-48f1-ae8b-4bee12 8%, 9d830bff-2bae-4af8-b654-8f534b 8%, 8be2d03d-9c2b-4678-bf2d-62a731 8%, ff61cc50-d134-4080-82bf-b5d46f 8%, 5e34fc6d-0a0e-4292-91bc-92989f 8%

GEOMETRY: {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 23 | 0 | 23 1; 22 1; 21 1; 20 1 |
| PARCEL | category | 23 | 0 | 13705509A 1; 13705507A 1; 124171920 1; 124062390 1 |
| GISAREA | amount | 23 | 0 | 2460.7034045 1; 7321.3639024 1; 5545.16812642 1; 9000.97954141 1 |
| GISACRES | amount | 23 | 0 | 0.05648791 1; 0.16806923 1; 0.12729488 1; 0.20662649 1 |
| X_HPGN | amount | 23 | 0 | 987719.2798393 1; 987620.24007875 1; 997852.08703027 1; 997182.17206585 1 |
| Y_HPGN | amount | 23 | 0 | 421707.69198019 1; 421920.39668397 1; 442654.72564936 1; 445694.86113545 1 |
| LON | category | 23 | 0 | -110.98693839 1; -110.9872525 1; -110.95359341 1; -110.95567135 1 |
| LAT | category | 23 | 0 | 32.1559454 1; 32.15653249 1; 32.21327468 1; 32.2216471 1 |
| LOT_R | category | 14 | 1 | 9 4; 1 3; 12 3; 11 2 |
| LINK | category | 23 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 9 | 0 | 141312E 7; 141313E 4; 141407E 3; 151302E 2 |
| MP_OL | category | 13 | 0 | 03071 5; 01004 3; 63054 2; 02004 2 |
| SEQ_NUM_S | category | 3 | 20 | 20080560074 2; nan 1 |
| JURIS_OL | who | 1 | 0 | TUCSON 23 |
| CURZONE_OL | other | 1 | 0 | C-3 23 |
| ADDRESS_OL | category | 12 | 0 | nan 12; 1025 E BROADWAY BL 1; 1003 E BROADWAY BL 1; 10 N PARK AV 1 |
| SEQ_NUM_D | category | 11 | 0 | 0 9; 20011600631 3; 97064010 2; 20171020456 2 |
| PARCEL_USE | other | 1 | 0 | 9700 23 |
| LANDMEAS | amount | 22 | 0 | 6098.0 2; 0.1 1; 0.19 1; 5550.0 1 |
| LANDUNIT | category | 2 | 0 | F 21; A 2 |
| LASTCHANGE | date | 11 | 0 | 1121126400000 10; 1215388800000 4; 1178532350000 1; 1178533065000 1 |
| LEGAL1 | category | 22 | 0 | PARQUE DE SANTA CRUZ RESU 2; BRUCKNERS N30'  LOT 16 BL 1; BUELLS PT L 4 & E 10' OF  1; BUELLS S 65' OF N 150' OF 1 |
| LEGAL2 | category | 11 | 12 | BLK 2 2; ELY PTN LOT 9 1; ELY PTN LOT 7 1; BLK 42 1 |
| LEGAL3 | category | 5 | 19 | PART FOR RDS 1; WLY PT FOR RD 1; (PROC 2177 BK 17 PG 43 D  1; LOT 4 1 |
| LEGAL4 | category | 2 | 22 | (DRNGWY 6590/805) 1 |
| LEGAL5 | empty | 1 | 23 |  |
| LOT | category | 14 | 1 | 00009 4; 00001 3; 00012 3; 00011 2 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 23 |
| MAIL2 | category | 2 | 0 | . 15; REAL ESTATE DIVISION 8 |
| MAIL3 | category | 3 | 0 | . 15; ATTN: PROPERTY MANAGMENT 5; ATTN: PROPERTY MANAGEMENT 3 |
| MAIL4 | category | 2 | 15 | PO BOX 27210 8 |
| MAIL5 | category | 3 | 15 | TUCSON AZ 6; TUCSON  AZ 2 |
| MP | category | 12 | 0 | 03071 5; 03069 3; 02004 3; 32038 2 |
| PAGE | category | 16 | 0 | 3027 3; 0 3; 527 2; 1271 2 |
| RECORDDATE | date | 15 | 0 | nan 4; 20010817 3; 19970428 2; 20170412 2 |
| DOCKET | category | 16 | 0 | 11615 3; 0 3; 31 2; 10533 2 |
| RECTRACT | empty | 1 | 23 |  |
| SECTMODIF | category | 2 | 4 | nan 19 |
| TAXAREA | category | 3 | 0 | 0150 20; 1250 2; 1050 1 |
| ZIP | category | 2 | 0 | 00000 15; 85726 8 |
| ZIP4 | category | 2 | 0 | 0000 15; 7210 8 |
| TAXYR | other | 1 | 0 | 2023 23 |
| LIMNET | other | 1 | 0 | 0 23 |
| FCV | category | 23 | 0 | 4356 1; 8276 1; 16816 1; 80737 1 |
| SHAPE_LENG | empty | 1 | 23 |  |
| ADDRESSEE | category | 3 | 0 | CITY OF TUCSON 15; CITY OF TUCSON
REAL ESTA 5; CITY OF TUCSON
REAL ESTA 3 |
| ADDRESS | category | 7 | 0 | nan 10; PO BOX 27210 8; 1128 S 6TH AV 1; 1133 S 6TH AV 1 |
| CITY | category | 3 | 0 | nan 15; TUCSON 6; TUCSON  2 |
| STATE_PROVINCE | category | 2 | 0 | nan 15; AZ 8 |
| COUNTRY | empty | 1 | 23 |  |
| POSTAL_CODE | category | 2 | 0 | nan 15; 85726-7210 8 |
| SITE_ADDRESS | category | 13 | 0 | nan 11; 1025 E BROADWAY BL 1; 1003 E BROADWAY BL 1; 10 N PARK AV 1 |
| SITE_ZIP | category | 4 | 11 | 85705 6; 85719 3; 85701 3 |
| SITE_ZIPCITY | category | 2 | 11 | TUCSON 12 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     23 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      23 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             23 |
| DATASOURCE | who | 1 | 0 | PAREGION 23 |
| URL | category | 22 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | category | 23 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 3 | 0 | NONE 11; ONE 11; MULTIPLE 1 |
| LEGAL_DESC | category | 23 | 0 | PARQUE DE SANTA CRUZ RESU 1; PARQUE DE SANTA CRUZ RESU 1; BRUCKNERS N30'  LOT 16 BL 1; BUELLS PT L 4 & E 10' OF  1 |
| OWN | other | 1 | 0 | City 23 |
| VAN | who | 1 | 0 | not_van 23 |
| YEARBUILT | category | 9 | 0 | nan 15; 1965 1; 1935 1; 1957 1 |
| LAST_EDITED_USER | category | 3 | 0 | GISPARFAB 19; u142832@CENTRAL 3; u152243@CENTRAL 1 |
| LAST_EDITED_DATE | date | 19 | 0 | 1611163938000 2; 1603172077000 2; 1603165972000 2; 1603158685000 2 |
| GLOBALID | category | 23 | 0 | 51ad829c-fb4d-4b8b-820a-2 1; 374f4130-b4a5-4454-aba6-e 1; 04cb1ac1-2505-4643-af97-5 1; 2c535f67-0301-44de-a6c6-4 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 23 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 23 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 23 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 23 |
| SHAPE__AREA | amount | 23 | 0 | 319.8984375 1; 946.984375 1; 721.765625 1; 1171.7890625 1 |
| SHAPE__LENGTH | amount | 23 | 0 | 140.6922066103407 1; 246.56390743221505 1; 154.75074704515924 1; 151.71345544967102 1 |
| GEOMETRY | category | 23 | 0 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:47:12.24856 23 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5c1a9d09-6caf-4143-99c5-3 23 |
| SRC_SHA256 | who | 1 | 0 | 07b969ecb94acb3fa37633a00 23 |
