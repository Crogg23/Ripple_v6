# PORTAL_ARC_TUCSON_OPEN_DATA_080C2334EE

rows 17  columns 78  scan 4.5s

roles: amount 7, audit 2, category 45, date 6, empty 4, other 5, who 10

## when

LASTCHANGE
  2005         9  ##############################
  2007         2  #######
  2008         4  #############
  2010         1  ###
  2020         1  ###

RECORDDATE
  1966         2  ####################
  1969         2  ####################
  1986         1  ##########
  1991         1  ##########
  1995         3  ##############################
  2000         1  ##########
  2001         3  ##############################

LAST_EDITED_DATE
  2020        13  ##############################
  2021         4  #########

CREATED_DATE_COT
  2023        17  ##############################

LAST_EDITED_DATE_COT
  2023        17  ##############################

INGESTED_AT
  2026        17  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 17 | 1.2K | 5.5K | 83.9K | 97.6K | 184.9K |
| GISACRES | 17 | 0.03 | 0.13 | 1.92 | 2.24 | 4.25 |
| X_HPGN | 17 | 987.6K | 993.1K | 1.01M | 1.01M | 16.89M |
| Y_HPGN | 17 | 421.7K | 445.7K | 469.0K | 470.1K | 7.56M |
| LANDMEAS | 17 | 0.10 | 5.5K | 96.0K | 112.1K | 194.1K |
| SHAPE__AREA | 17 | 155.12 | 721.77 | 10.9K | 12.7K | 24.1K |

## who

JURIS_OL by rows
        17  TUCSON

JURIS_OL by dollars
      184.9K       17 rows  TUCSON

MAIL1 by rows
        17  CITY OF TUCSON

MAIL1 by dollars
      184.9K       17 rows  CITY OF TUCSON

USE_DESC by rows
        17  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
      184.9K       17 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        17  MISC REL/GVT/IN     

SPT_DESC by dollars
      184.9K       17 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:72.6K 2021:112.3K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:72.6K 2021:112.3K

## what

OBJECTID: 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%

PARCEL: 13705509A 8%, 13705507A 8%, 124171920 8%, 124062390 8%, 124062380 8%, 124062350 8%, 117091960 8%, 117091550 8%, 117091510 8%, 117072040 8%, 11704181D 8%, 11704181C 8%

LON: -110.98693839 8%, -110.9872525 8%, -110.95359341 8%, -110.95567135 8%, -110.95587629 8%, -110.95599387 8%, -110.96894415 8%, -110.9680454 8%, -110.96804663 8%, -110.96917334 8%, -110.97765585 8%, -110.97767853 8%

LAT: 32.1559454 8%, 32.15653249 8%, 32.21327468 8%, 32.2216471 8%, 32.22152898 8%, 32.22173443 8%, 32.20725806 8%, 32.20703426 8%, 32.20728149 8%, 32.21243852 8%, 32.22950858 8%, 32.22963057 8%

LOT_R: 1 19%, 11 12%, nan 12%, 9 6%, 7 6%, 16 6%, 4 6%, 2 6%, 15 6%, 8 6%, 22 6%, 5 6%

LINK: HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%

TRS_OL: 141313E 24%, 141407E 18%, 151302E 12%, 141312E 12%, 141311E 12%, 141418E 6%, 141314E 6%, 131428E 6%, 131324E 6%

MP_OL: 01004 18%, 63054 12%, 02004 12%, 01003 12%, 01023 12%, 04081 6%, 02024 6%, 05055 6%, 04037 6%, 05046 6%, 03008 6%

SEQ_NUM_S: 20080560074 100%

ADDRESS_OL: nan 65%, 1025 E BROADWAY BL 6%, 1003 E BROADWAY BL 6%, 10 N PARK AV 6%, 1128 S 6TH AV 6%, 1133 S 6TH AV 6%, 523 W SPEEDWAY BL 6%

SEQ_NUM_D: 0 53%, 20011600631 18%, 95145751 6%, 95018114 6%, 95022288 6%, 20001380419 6%, 91033626 6%

LANDUNIT: F 88%, A 12%

LEGAL1: PARQUE DE SANTA CRUZ RESUB 15%, BRUCKNERS N30'  LOT 16 BLK 32 8%, BUELLS PT L 4 & E 10' OF L 3 L 8%, BUELLS S 65' OF N 150' OF E 28 8%, BUELLS N85' LOTS 1 & 2 & N85'  8%, ROSENFELDS RESUB TUCSON BLK 16 8%, TUCSON LOT 15 BLK 166 8%, TUCSON LOT 11 BLK 166 8%, TUCSON PT L 8 & 9 LYG W OF STO 8%, TUCSON S48' M/L OF THAT PART O 8%, TUCSON N2 M/L OF 596.3' OF THA 8%, COTTONWOOD LOT 22 EXC E10' BLK 8%

LEGAL2: BLK 2 18%, ELY PTN LOT 9 9%, ELY PTN LOT 7 9%, BLK 42 9%, N150' OF W40' OF LOT 3 BLK 42 9%, BLK 121 9%, ST & S48' M/L OF BLK 7 MT VIEW 9%, OF MAIN ST & PART OF BLK 7 MT  9%, OF LOT 12 BLK 1 EXC RD 9%, LOT 1 EXC RILLITO RIVER & PT O 9%

LEGAL3: PART FOR RDS 25%, WLY PT FOR RD 25%, (PROC 2177 BK 17 PG 43 D R E B 25%, LOT 4 25%

LEGAL4: (DRNGWY 6590/805) 100%

LOT: 00001 19%, 00011 12%, nan 12%, 00009 6%, 00007 6%, 00016 6%, 00004 6%, 00002 6%, 00015 6%, 00008 6%, 00022 6%, 00005 6%

MAIL2: . 71%, REAL ESTATE DIVISION 29%

MAIL3: . 71%, ATTN: PROPERTY MANAGMENT 29%

MAIL4: PO BOX 27210 100%

MAIL5: TUCSON AZ 100%

MP: 03069 18%, 02004 18%, 32038 12%, 02003 12%, 01023 12%, 04081 6%, 02024 6%, 04037 6%, 05046 6%, 03008 6%

PAGE: 3027 19%, 527 12%, 51 12%, 404 6%, 2194 6%, 1213 6%, 1194 6%, 598 6%, 419 6%, 343 6%, 817 6%, 1700 6%

DOCKET: 11615 19%, 31 12%, 2683 12%, 76 6%, 10135 6%, 9976 6%, 9982 6%, 26 6%, 3576 6%, 3586 6%, 11342 6%, 7836 6%

SECTMODIF: nan 100%

TAXAREA: 0150 82%, 1250 12%, 1050 6%

ZIP: 00000 71%, 85726 29%

ZIP4: 0000 71%, 7210 29%

FCV: 4356 8%, 8276 8%, 16816 8%, 80737 8%, 39813 8%, 107457 8%, 78032 8%, 78817 8%, 77239 8%, 61870 8%, 12181 8%, 8641 8%

ADDRESSEE: CITY OF TUCSON 71%, CITY OF TUCSON
REAL ESTATE DI 29%

ADDRESS: nan 53%, PO BOX 27210 29%, 1128 S 6TH AV 6%, 1133 S 6TH AV 6%, 523 W SPEEDWAY BL 6%

CITY: nan 71%, TUCSON 29%

STATE_PROVINCE: nan 71%, AZ 29%

POSTAL_CODE: nan 71%, 85726-7210 29%

SITE_ADDRESS: nan 59%, 1025 E BROADWAY BL 6%, 1003 E BROADWAY BL 6%, 10 N PARK AV 6%, 1128 S 6TH AV 6%, 1149 S 6TH AV 6%, 1133 S 6TH AV 6%, 523 W SPEEDWAY BL 6%

SITE_ZIP: 85719 43%, 85701 43%, 85705 14%

SITE_ZIPCITY: TUCSON 100%

URL: https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%

URL2: http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%

ADR_STATUS: NONE 59%, ONE 35%, MULTIPLE 6%

LEGAL_DESC: PARQUE DE SANTA CRUZ RESUB; EL 8%, PARQUE DE SANTA CRUZ RESUB; EL 8%, BRUCKNERS N30'  LOT 16 BLK 32 8%, BUELLS PT L 4 & E 10' OF L 3 L 8%, BUELLS S 65' OF N 150' OF E 28 8%, BUELLS N85' LOTS 1 & 2 & N85'  8%, ROSENFELDS RESUB TUCSON BLK 16 8%, TUCSON LOT 15 BLK 166 8%, TUCSON LOT 11 BLK 166 8%, TUCSON PT L 8 & 9 LYG W OF STO 8%, TUCSON S48' M/L OF THAT PART O 8%, TUCSON N2 M/L OF 596.3' OF THA 8%

YEARBUILT: nan 82%, 1965 6%, 1935 6%, 1957 6%

LAST_EDITED_USER: GISPARFAB 76%, u142832@CENTRAL 18%, u152243@CENTRAL 6%

GLOBALID: b1703340-beee-4b0e-9713-a23548 8%, 9852f785-9645-48be-81b0-c647d2 8%, 6d66e6a1-9d4f-400d-9090-1f30c3 8%, b0438ac2-71ac-441b-bcf8-569d86 8%, 8fc269b1-085c-4a4f-8c00-416b93 8%, e4052fdd-05ee-4466-ab66-135483 8%, d1ae5ade-01c9-41a9-8efa-8650b8 8%, 2f2963bf-664e-4452-959d-11287d 8%, 0c35f073-df9b-46ae-ad53-1c4eac 8%, 8e7903c0-a0d1-4aa6-a078-9e3a10 8%, 5c02177f-664e-4398-8f1b-b3663e 8%, 94920607-797d-4dad-9473-8c5921 8%

GEOMETRY: {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 17 | 0 | 17 1; 16 1; 15 1; 14 1 |
| PARCEL | category | 17 | 0 | 13705509A 1; 13705507A 1; 124171920 1; 124062390 1 |
| GISAREA | amount | 17 | 0 | 2460.7034045 1; 7321.3639024 1; 5545.16812642 1; 9000.97954141 1 |
| GISACRES | amount | 17 | 0 | 0.05648791 1; 0.16806923 1; 0.12729488 1; 0.20662649 1 |
| X_HPGN | amount | 17 | 0 | 987719.2798393 1; 987620.24007875 1; 997852.08703027 1; 997182.17206585 1 |
| Y_HPGN | amount | 17 | 0 | 421707.69198019 1; 421920.39668397 1; 442654.72564936 1; 445694.86113545 1 |
| LON | category | 17 | 0 | -110.98693839 1; -110.9872525 1; -110.95359341 1; -110.95567135 1 |
| LAT | category | 17 | 0 | 32.1559454 1; 32.15653249 1; 32.21327468 1; 32.2216471 1 |
| LOT_R | category | 13 | 0 | 1 3; 11 2; nan 2; 9 1 |
| LINK | category | 17 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 9 | 0 | 141313E 4; 141407E 3; 151302E 2; 141312E 2 |
| MP_OL | category | 11 | 0 | 01004 3; 63054 2; 02004 2; 01003 2 |
| SEQ_NUM_S | category | 2 | 15 | 20080560074 2 |
| JURIS_OL | who | 1 | 0 | TUCSON 17 |
| CURZONE_OL | other | 1 | 0 | C-3 17 |
| ADDRESS_OL | category | 7 | 0 | nan 11; 1025 E BROADWAY BL 1; 1003 E BROADWAY BL 1; 10 N PARK AV 1 |
| SEQ_NUM_D | category | 7 | 0 | 0 9; 20011600631 3; 95145751 1; 95018114 1 |
| PARCEL_USE | other | 1 | 0 | 9700 17 |
| LANDMEAS | amount | 17 | 0 | 0.1 1; 0.19 1; 5550.0 1; 8941.0 1 |
| LANDUNIT | category | 2 | 0 | F 15; A 2 |
| LASTCHANGE | date | 6 | 0 | 1121126400000 9; 1215388800000 4; 1178532350000 1; 1178533065000 1 |
| LEGAL1 | category | 16 | 0 | PARQUE DE SANTA CRUZ RESU 2; BRUCKNERS N30'  LOT 16 BL 1; BUELLS PT L 4 & E 10' OF  1; BUELLS S 65' OF N 150' OF 1 |
| LEGAL2 | category | 11 | 6 | BLK 2 2; ELY PTN LOT 9 1; ELY PTN LOT 7 1; BLK 42 1 |
| LEGAL3 | category | 5 | 13 | PART FOR RDS 1; WLY PT FOR RD 1; (PROC 2177 BK 17 PG 43 D  1; LOT 4 1 |
| LEGAL4 | category | 2 | 16 | (DRNGWY 6590/805) 1 |
| LEGAL5 | empty | 1 | 17 |  |
| LOT | category | 13 | 0 | 00001 3; 00011 2; nan 2; 00009 1 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 17 |
| MAIL2 | category | 2 | 0 | . 12; REAL ESTATE DIVISION 5 |
| MAIL3 | category | 2 | 0 | . 12; ATTN: PROPERTY MANAGMENT 5 |
| MAIL4 | category | 2 | 12 | PO BOX 27210 5 |
| MAIL5 | category | 2 | 12 | TUCSON AZ 5 |
| MP | category | 10 | 0 | 03069 3; 02004 3; 32038 2; 02003 2 |
| PAGE | category | 13 | 0 | 3027 3; 527 2; 51 2; 404 1 |
| RECORDDATE | date | 11 | 0 | nan 4; 20010817 3; 19660216 2; 19950925 1 |
| DOCKET | category | 13 | 0 | 11615 3; 31 2; 2683 2; 76 1 |
| RECTRACT | empty | 1 | 17 |  |
| SECTMODIF | category | 2 | 2 | nan 15 |
| TAXAREA | category | 3 | 0 | 0150 14; 1250 2; 1050 1 |
| ZIP | category | 2 | 0 | 00000 12; 85726 5 |
| ZIP4 | category | 2 | 0 | 0000 12; 7210 5 |
| TAXYR | other | 1 | 0 | 2023 17 |
| LIMNET | other | 1 | 0 | 0 17 |
| FCV | category | 17 | 0 | 4356 1; 8276 1; 16816 1; 80737 1 |
| SHAPE_LENG | empty | 1 | 17 |  |
| ADDRESSEE | category | 2 | 0 | CITY OF TUCSON 12; CITY OF TUCSON
REAL ESTA 5 |
| ADDRESS | category | 5 | 0 | nan 9; PO BOX 27210 5; 1128 S 6TH AV 1; 1133 S 6TH AV 1 |
| CITY | category | 2 | 0 | nan 12; TUCSON 5 |
| STATE_PROVINCE | category | 2 | 0 | nan 12; AZ 5 |
| COUNTRY | empty | 1 | 17 |  |
| POSTAL_CODE | category | 2 | 0 | nan 12; 85726-7210 5 |
| SITE_ADDRESS | category | 8 | 0 | nan 10; 1025 E BROADWAY BL 1; 1003 E BROADWAY BL 1; 10 N PARK AV 1 |
| SITE_ZIP | category | 4 | 10 | 85719 3; 85701 3; 85705 1 |
| SITE_ZIPCITY | category | 2 | 10 | TUCSON 7 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     17 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      17 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             17 |
| DATASOURCE | who | 1 | 0 | PAREGION 17 |
| URL | category | 17 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | category | 17 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 3 | 0 | NONE 10; ONE 6; MULTIPLE 1 |
| LEGAL_DESC | category | 17 | 0 | PARQUE DE SANTA CRUZ RESU 1; PARQUE DE SANTA CRUZ RESU 1; BRUCKNERS N30'  LOT 16 BL 1; BUELLS PT L 4 & E 10' OF  1 |
| OWN | other | 1 | 0 | City 17 |
| VAN | who | 1 | 0 | not_van 17 |
| YEARBUILT | category | 4 | 0 | nan 14; 1965 1; 1935 1; 1957 1 |
| LAST_EDITED_USER | category | 3 | 0 | GISPARFAB 13; u142832@CENTRAL 3; u152243@CENTRAL 1 |
| LAST_EDITED_DATE | date | 15 | 0 | 1611163938000 2; 1603172077000 2; 1603170427000 1; 1603180645000 1 |
| GLOBALID | category | 17 | 0 | b1703340-beee-4b0e-9713-a 1; 9852f785-9645-48be-81b0-c 1; 6d66e6a1-9d4f-400d-9090-1 1; b0438ac2-71ac-441b-bcf8-5 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 17 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 17 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 17 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 17 |
| SHAPE__AREA | amount | 17 | 0 | 319.8984375 1; 946.984375 1; 721.765625 1; 1171.7890625 1 |
| SHAPE__LENGTH | amount | 17 | 0 | 140.6922066103407 1; 246.56390743221505 1; 154.75074704515924 1; 151.71345544967102 1 |
| GEOMETRY | category | 17 | 0 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:46:55.93190 17 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6f63ac42-1cb4-4a6c-8186-9 17 |
| SRC_SHA256 | who | 1 | 0 | 4d9e6bffd8d7412309ec894d8 17 |
