# PORTAL_ARC_TUCSON_OPEN_DATA_7044E0923D

rows 13  columns 78  scan 5.8s

roles: amount 8, audit 2, category 43, date 6, empty 5, other 5, who 10

## when

LASTCHANGE
  2005         5  ##############################
  2008         2  ############
  2009         2  ############
  2012         1  ######
  2013         1  ######
  2016         1  ######
  2019         1  ######

RECORDDATE
  1972         1  ##############################
  1975         1  ##############################
  1986         1  ##############################
  1989         1  ##############################
  1998         1  ##############################
  1999         1  ##############################

LAST_EDITED_DATE
  2020         9  ##############################
  2021         2  #######
  2022         1  ###
  2023         1  ###

CREATED_DATE_COT
  2023        13  ##############################

LAST_EDITED_DATE_COT
  2023        13  ##############################

INGESTED_AT
  2026        13  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 13 | 21.1K | 64.2K | 259.3K | 271.6K | 1.14M |
| GISACRES | 13 | 0.48 | 1.47 | 5.95 | 6.23 | 26.16 |
| X_HPGN | 13 | 983.4K | 994.3K | 1.04M | 1.04M | 13.04M |
| Y_HPGN | 13 | 415.6K | 439.2K | 471.0K | 471.0K | 5.72M |
| LANDMEAS | 13 | 0.10 | 6.52 | 156.4K | 162.0K | 367.6K |
| PAGE | 8 | 11 | 974.50 | 2.6K | 2.7K | 8.9K |

## who

JURIS_OL by rows
        13  TUCSON

JURIS_OL by dollars
       1.14M       13 rows  TUCSON

MAIL1 by rows
        13  CITY OF TUCSON

MAIL1 by dollars
       1.14M       13 rows  CITY OF TUCSON

USE_DESC by rows
        13  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
       1.14M       13 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        13  MISC REL/GVT/IN     

SPT_DESC by dollars
       1.14M       13 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:837.5K 2021:173.1K 2022:35.1K 2023:93.9K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:837.5K 2021:173.1K 2022:35.1K 2023:93.9K

## what

OBJECTID: 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%, 3 8%, 2 8%

PARCEL: 14032145A 8%, 14032002F 8%, 140105280 8%, 137335740 8%, 13414016C 8%, 133301130 8%, 12914164A 8%, 118200750 8%, 118072710 8%, 116163030 8%, 106042440 8%, 105097360 8%

LON: -110.90369909 8%, -110.90202353 8%, -110.93062949 8%, -111.00107297 8%, -110.83070929 8%, -110.80282709 8%, -110.95931055 8%, -110.97537308 8%, -111.00000809 8%, -110.9801251 8%, -110.96938297 8%, -110.96435894 8%

LAT: 32.1384074 8%, 32.139884 8%, 32.15507216 8%, 32.14539179 8%, 32.21190024 8%, 32.22198196 8%, 32.18895765 8%, 32.20407586 8%, 32.19462578 8%, 32.2306624 8%, 32.26683867 8%, 32.29079324 8%

LOT_R: nan 71%, 1 14%, 6 14%

LINK: HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%

TRS_OL: 151410E 15%, 131324E 15%, 151405E 8%, 151310E 8%, 141517E 8%, 141510E 8%, 141430E 8%, 141324E 8%, 141322E 8%, 141311E 8%, 131325E 8%

MP_OL: nan 23%, 60049 15%, 50009 8%, 53051 8%, 46039 8%, 58099 8%, 02039 8%, 34020 8%, 03026 8%, 06041 8%

SEQ_NUM_S: nan 50%, 20052270612 33%, 97155305 17%

ADDRESS_OL: nan 77%, 6184 S COLUMBUS BL 8%, 744 E 39TH ST 8%, 201 E NAVAJO RD 8%

SEQ_NUM_D: 0.0 54%, nan 31%, 19991360588.0 8%, 19981380939.0 8%

LANDUNIT: F 38%, A 38%, S 23%

LEGAL1: VALENCIA ALVERNON COMMERCE CEN 8%, W410' OF E667.12' OF N420' OF  8%, RANCHO REYES II 8%, DRAINAGEWAY IN CTRL NLY PTN W2 8%, S10' OF N659.83 M/L OF LOT 5 E 8%, CENTENNIAL TERRACES DRAINAGEWA 8%, GRAND VIEW LOTS 1 2 15 & 16 BL 8%, N150' S406' W364.45' E784.4' E 8%, 36TH & MISSION PTN DRGWY/MAINT 8%, R/W 1480' VARIABLE WIDTH IN M/ 8%, GARDEN HOMES LOT 6 BLK 12 8%, MIRAMONTE AT THE RIVER RACETRA 8%

LEGAL2: LYG SLY OF ANTRIM LOOP 9%, 3.95 AC SEC 10-15-14 9%, PUBLIC DRAINAGE 9%, & ADJ TO 40/20 6.52 AC SEC 10- 9%, FOR RD .23 AC SEC 17-14-15 9%, PTN ABAND EUCLID AVE 9%, E64.35' THEREOF 1.19 AC SEC 24 9%, EXTENSION EAST LINE LOT 97 & M 9%, NE4 SEC 11 T14S R13E 2.85 AC 9%, SLY PTN NORTHMANOR WASH (DRAIN 9%, (DRAINAGEWAY) 9%

LEGAL3: (DRE 251/570 RD 862/284) 100%

LOT: nan 71%, 00001 14%, 00006 14%

MAIL2: . 69%, REAL ESTATE DIVISION 23%, ATTN: HOUSING AND COMMUNITY DE 8%

MAIL3: . 75%, ATTN: PROPERTY MANAGEMENT 17%, ATTN: PROPERTY MANAGMENT 8%

MAIL4: PO BOX 27210 100%

MAIL5: TUCSON AZ 100%

MP: nan 38%, 60049 15%, 47004 8%, 53051 8%, 58099 8%, 02039 8%, 34020 8%, 06041 8%

DOCKET: nan 38%, 8447 8%, 7827 8%, 4182 8%, 3136 8%, 4958 8%, 107 8%, 11090 8%, 10861 8%

SECTMODIF: nan 100%

TAXAREA: 0150 54%, 1250 23%, 1050 23%

ZIP: 00000 69%, 85726 31%

ZIP4: 0000 69%, 7210 31%

FCV: 500 31%, 260000 8%, 25000 8%, 72000 8%, 230000 8%, 509 8%, 366700 8%, 45000 8%, 213000 8%, 48000 8%

ADDRESSEE: CITY OF TUCSON 69%, CITY OF TUCSON
REAL ESTATE DI 15%, CITY OF TUCSON
REAL ESTATE DI 8%, CITY OF TUCSON
ATTN: HOUSING  8%

ADDRESS: nan 69%, PO BOX 27210 31%

CITY: nan 69%, TUCSON 31%

STATE_PROVINCE: nan 69%, AZ 31%

POSTAL_CODE: nan 69%, 85726-7210 31%

SITE_ADDRESS: nan 77%, 6184 S COLUMBUS BL 8%, 744 E 39TH ST 8%, 201 E NAVAJO RD 8%

SITE_ZIP: 85706 33%, 85713 33%, 85705 33%

SITE_ZIPCITY: TUCSON 100%

URL: https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%

URL2: http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%

ADR_STATUS: NONE 77%, ONE 23%

LEGAL_DESC: VALENCIA ALVERNON COMMERCE CEN 8%, W410' OF E667.12' OF N420' OF  8%, RANCHO REYES II; PUBLIC DRAINA 8%, DRAINAGEWAY IN CTRL NLY PTN W2 8%, S10' OF N659.83 M/L OF LOT 5 E 8%, CENTENNIAL TERRACES DRAINAGEWA 8%, GRAND VIEW LOTS 1 2 15 & 16 BL 8%, N150' S406' W364.45' E784.4' E 8%, 36TH & MISSION PTN DRGWY/MAINT 8%, R/W 1480' VARIABLE WIDTH IN M/ 8%, GARDEN HOMES LOT 6 BLK 12 8%, MIRAMONTE AT THE RIVER RACETRA 8%

YEARBUILT: nan 92%, 1969 8%

LAST_EDITED_USER: GISPARFAB 69%, u142832@CENTRAL 15%, u116448@CENTRAL 8%, JArechederra2@CENTRAL 8%

GLOBALID: c684de50-f1a0-46a2-9668-85d1a6 8%, 500287fc-6a05-484d-b071-5c99c1 8%, d04aa97f-b55d-4b31-a213-8ffc15 8%, 3519942b-ad12-4e06-b749-6b29e7 8%, 6a864c04-3883-4f7f-9b9b-05a7c3 8%, 84ca19b2-ea85-4202-b6ef-e671cf 8%, bfcabdc6-e229-48c4-b83e-2b4833 8%, 00761f30-4ace-4cb8-bc4d-c294fd 8%, 33d7aa94-4653-410b-9e23-382f45 8%, 30c5dead-1f60-4c2c-99f7-5bfbee 8%, 292c7a58-9cc7-48bc-9822-6ee0f5 8%, 9e41d29c-f227-4ea2-86ee-c70ea2 8%

GEOMETRY: {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "MultiPolygon", "coor 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 13 | 0 | 13 1; 12 1; 11 1; 10 1 |
| PARCEL | category | 13 | 0 | 14032145A 1; 14032002F 1; 140105280 1; 137335740 1 |
| GISAREA | amount | 13 | 0 | 114412.61334092 1; 169389.15971171 1; 64211.16529013 1; 271562.76309218 1 |
| GISACRES | amount | 13 | 0 | 2.62645595 1; 3.88849755 1; 1.47403151 1; 6.23399479 1 |
| X_HPGN | amount | 13 | 0 | 1013540.16776118 1; 1014053.75856458 1; 1005148.61763913 1; 983377.59086297 1 |
| Y_HPGN | amount | 13 | 0 | 415559.85225139 1; 416101.9142924 1; 421545.07486436 1; 417830.81470949 1 |
| LON | category | 13 | 0 | -110.90369909 1; -110.90202353 1; -110.93062949 1; -111.00107297 1 |
| LAT | category | 13 | 0 | 32.1384074 1; 32.139884 1; 32.15507216 1; 32.14539179 1 |
| LOT_R | category | 4 | 6 | nan 5; 1 1; 6 1 |
| LINK | category | 13 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 11 | 0 | 151410E 2; 131324E 2; 151405E 1; 151310E 1 |
| MP_OL | category | 10 | 0 | nan 3; 60049 2; 50009 1; 53051 1 |
| SEQ_NUM_S | category | 4 | 7 | nan 3; 20052270612 2; 97155305 1 |
| JURIS_OL | who | 1 | 0 | TUCSON 13 |
| CURZONE_OL | other | 1 | 0 | R-3 13 |
| ADDRESS_OL | category | 4 | 0 | nan 10; 6184 S COLUMBUS BL 1; 744 E 39TH ST 1; 201 E NAVAJO RD 1 |
| SEQ_NUM_D | category | 4 | 0 | 0.0 7; nan 4; 19991360588.0 1; 19981380939.0 1 |
| PARCEL_USE | other | 1 | 0 | 9700 13 |
| LANDMEAS | amount | 12 | 0 | 0.1 2; 115131.0 1; 9.0 1; 6.52 1 |
| LANDUNIT | category | 3 | 0 | F 5; A 5; S 3 |
| LASTCHANGE | date | 8 | 0 | 1121126400000 5; 1256774400000 2; 1337782138000 1; 1360195200000 1 |
| LEGAL1 | category | 13 | 0 | VALENCIA ALVERNON COMMERC 1; W410' OF E667.12' OF N420 1; RANCHO REYES II 1; DRAINAGEWAY IN CTRL NLY P 1 |
| LEGAL2 | category | 12 | 2 | LYG SLY OF ANTRIM LOOP 1; 3.95 AC SEC 10-15-14 1; PUBLIC DRAINAGE 1; & ADJ TO 40/20 6.52 AC SE 1 |
| LEGAL3 | category | 2 | 12 | (DRE 251/570 RD 862/284) 1 |
| LEGAL4 | empty | 1 | 13 |  |
| LEGAL5 | empty | 1 | 13 |  |
| LOT | category | 4 | 6 | nan 5; 00001 1; 00006 1 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 13 |
| MAIL2 | category | 3 | 0 | . 9; REAL ESTATE DIVISION 3; ATTN: HOUSING AND COMMUNI 1 |
| MAIL3 | category | 4 | 1 | . 9; ATTN: PROPERTY MANAGEMENT 2; ATTN: PROPERTY MANAGMENT 1 |
| MAIL4 | category | 2 | 9 | PO BOX 27210 4 |
| MAIL5 | category | 2 | 9 | TUCSON AZ 4 |
| MP | category | 8 | 0 | nan 5; 60049 2; 47004 1; 53051 1 |
| PAGE | amount | 9 | 0 | nan 5; 1455.0 1; 1645.0 1; 494.0 1 |
| RECORDDATE | date | 7 | 0 | nan 7; 19890105 1; 19860716 1; 19720207 1 |
| DOCKET | category | 9 | 0 | nan 5; 8447 1; 7827 1; 4182 1 |
| RECTRACT | empty | 2 | 13 |  |
| SECTMODIF | category | 2 | 7 | nan 6 |
| TAXAREA | category | 3 | 0 | 0150 7; 1250 3; 1050 3 |
| ZIP | category | 2 | 0 | 00000 9; 85726 4 |
| ZIP4 | category | 2 | 0 | 0000 9; 7210 4 |
| TAXYR | other | 1 | 0 | 2023 13 |
| LIMNET | other | 1 | 0 | 0 13 |
| FCV | category | 10 | 0 | 500 4; 260000 1; 25000 1; 72000 1 |
| SHAPE_LENG | empty | 1 | 13 |  |
| ADDRESSEE | category | 4 | 0 | CITY OF TUCSON 9; CITY OF TUCSON
REAL ESTA 2; CITY OF TUCSON
REAL ESTA 1; CITY OF TUCSON
ATTN: HOU 1 |
| ADDRESS | category | 2 | 0 | nan 9; PO BOX 27210 4 |
| CITY | category | 2 | 0 | nan 9; TUCSON 4 |
| STATE_PROVINCE | category | 2 | 0 | nan 9; AZ 4 |
| COUNTRY | empty | 1 | 13 |  |
| POSTAL_CODE | category | 2 | 0 | nan 9; 85726-7210 4 |
| SITE_ADDRESS | category | 4 | 0 | nan 10; 6184 S COLUMBUS BL 1; 744 E 39TH ST 1; 201 E NAVAJO RD 1 |
| SITE_ZIP | category | 4 | 10 | 85706 1; 85713 1; 85705 1 |
| SITE_ZIPCITY | category | 2 | 10 | TUCSON 3 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     13 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      13 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             13 |
| DATASOURCE | who | 1 | 0 | PAREGION 13 |
| URL | category | 13 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | category | 13 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 2 | 0 | NONE 10; ONE 3 |
| LEGAL_DESC | category | 13 | 0 | VALENCIA ALVERNON COMMERC 1; W410' OF E667.12' OF N420 1; RANCHO REYES II; PUBLIC D 1; DRAINAGEWAY IN CTRL NLY P 1 |
| OWN | other | 1 | 0 | City 13 |
| VAN | who | 1 | 0 | not_van 13 |
| YEARBUILT | category | 2 | 0 | nan 12; 1969 1 |
| LAST_EDITED_USER | category | 4 | 0 | GISPARFAB 9; u142832@CENTRAL 2; u116448@CENTRAL 1; JArechederra2@CENTRAL 1 |
| LAST_EDITED_DATE | date | 12 | 0 | 1611163968000 2; 1603152841000 1; 1603202425000 1; 1603152909000 1 |
| GLOBALID | category | 13 | 0 | c684de50-f1a0-46a2-9668-8 1; 500287fc-6a05-484d-b071-5 1; d04aa97f-b55d-4b31-a213-8 1; 3519942b-ad12-4e06-b749-6 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 13 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 13 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 13 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 13 |
| SHAPE__AREA | amount | 13 | 0 | 14867.48828125 1; 22012.109375 1; 8346.35546875 1; 35293.4921875 1 |
| SHAPE__LENGTH | amount | 13 | 0 | 1233.98363538931 1; 593.5906669261035 1; 1260.8733474553817 1; 3024.660105371295 1 |
| GEOMETRY | category | 13 | 0 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:46:44.29252 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1d20bde2-cda6-45e3-ac45-a 13 |
| SRC_SHA256 | who | 1 | 0 | c8c393060d1da5ee572ff12b8 13 |
