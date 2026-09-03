# PORTAL_ARC_TUCSON_OPEN_DATA_1073539FE2

rows 41  columns 78  scan 5.2s

roles: amount 8, audit 2, category 43, date 6, empty 5, other 5, who 10

## when

LASTCHANGE
  2005        21  ##############################
  2006         1  #
  2008         6  #########
  2009         3  ####
  2012         2  ###
  2013         1  #
  2015         1  #
  2016         1  #
  2019         2  ###
  2020         3  ####

RECORDDATE
  1964         1  ##########
  1966         1  ##########
  1972         2  ####################
  1973         1  ##########
  1975         1  ##########
  1979         2  ####################
  1983         1  ##########
  1986         1  ##########
  1989         1  ##########
  1991         1  ##########
  1992         1  ##########
  1993         2  ####################
  1995         1  ##########
  1997         1  ##########
  1998         1  ##########
  1999         3  ##############################
  2000         3  ##############################
  2009         1  ##########
  2015         1  ##########
  2019         1  ##########

LAST_EDITED_DATE
  2020        36  ##############################
  2021         3  ##
  2022         1  #
  2023         1  #

CREATED_DATE_COT
  2023        41  ##############################

LAST_EDITED_DATE_COT
  2023        41  ##############################

INGESTED_AT
  2026        41  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 41 | 424.18 | 10.1K | 230.7K | 271.6K | 1.35M |
| GISACRES | 41 | 0.01 | 0.23 | 5.29 | 6.23 | 30.92 |
| X_HPGN | 41 | 983.4K | 992.0K | 1.05M | 1.05M | 41.06M |
| Y_HPGN | 41 | 406.6K | 441.3K | 470.9K | 471.0K | 18.09M |
| LANDMEAS | 41 | 0.10 | 1.2K | 143.2K | 162.0K | 497.6K |
| PAGE | 34 | 0 | 692 | 3.8K | 4.1K | 36.8K |

## who

JURIS_OL by rows
        41  TUCSON

JURIS_OL by dollars
       1.35M       41 rows  TUCSON

MAIL1 by rows
        41  CITY OF TUCSON

MAIL1 by dollars
       1.35M       41 rows  CITY OF TUCSON

USE_DESC by rows
        41  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
       1.35M       41 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        41  MISC REL/GVT/IN     

SPT_DESC by dollars
       1.35M       41 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:1.04M 2021:179.9K 2022:35.1K 2023:93.9K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:1.04M 2021:179.9K 2022:35.1K 2023:93.9K

## what

OBJECTID: 41 8%, 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%

PARCEL: 14113834A 8%, 14032145A 8%, 14032002J 8%, 14032002F 8%, 140105280 8%, 137335780 8%, 137335740 8%, 13414016C 8%, 133311580 8%, 133311570 8%, 133301130 8%, 13312070B 8%

LON: -110.80022587 8%, -110.90369909 8%, -110.90129792 8%, -110.90202353 8%, -110.93062949 8%, -111.00025918 8%, -111.00107297 8%, -110.83070929 8%, -110.8021311 8%, -110.80227623 8%, -110.80282709 8%, -110.82809557 8%

LAT: 32.1129105 8%, 32.1384074 8%, 32.13988837 8%, 32.139884 8%, 32.15507216 8%, 32.13997225 8%, 32.14539179 8%, 32.21190024 8%, 32.2188668 8%, 32.21894204 8%, 32.22198196 8%, 32.24882636 8%

LOT_R: nan 40%, 1 20%, 3 7%, 8 7%, 5 7%, 2 3%, 12 3%, 9 3%, 27 3%, 10 3%, 11 3%

LINK: HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%

TRS_OL: 141324E 26%, 141311E 23%, 141313E 11%, 151410E 9%, 151310E 6%, 141515E 6%, 131324E 6%, 151522E 3%, 151405E 3%, 141517E 3%, 141510E 3%, 141505E 3%

MP_OL: nan 27%, 03026 21%, 02020 12%, 02004 9%, 16090 6%, 60049 6%, 46037 3%, 50009 3%, 53051 3%, 46039 3%, 58099 3%, 38041 3%

SEQ_NUM_S: nan 75%, 20052270612 17%, 97155305 8%

ADDRESS_OL: nan 83%, 6184 S COLUMBUS BL 2%, 744 E 39TH ST 2%, 937 S OSBORNE AV 2%, 628 N ANITA AV 2%, 1073 N CONTZEN AV 2%, 526 W DAVIS ST 2%, 201 E NAVAJO RD 2%

SEQ_NUM_D: 0.0 50%, nan 16%, 20000220283.0 8%, 19991360588.0 5%, 20152230528.0 3%, 19991710971.0 3%, 97130768.0 3%, 95145751.0 3%, 93124933.0 3%, 91087145.0 3%, 20190850415.0 3%, 92110690.0 3%

LANDUNIT: F 51%, S 37%, A 12%

LEGAL1: SILVER PASS DRAINAGEWAYS 8%, VALENCIA ALVERNON COMMERCE CEN 8%, W45' E257.12' N420' S2240.9' E 8%, W410' OF E667.12' OF N420' OF  8%, RANCHO REYES II 8%, N36' M/L S2286' W580.50' E680. 8%, DRAINAGEWAY IN CTRL NLY PTN W2 8%, S10' OF N659.83 M/L OF LOT 5 E 8%, CENTENNIAL PARK NO 3 WELLSITE  8%, CENTENNIAL PARK NO 3 PARCEL AP 8%, CENTENNIAL TERRACES DRAINAGEWA 8%, TANQUE VERDE TERRACE S 30' OF  8%

LEGAL2: ABAND ALLEY BLK 138 17%, LYG SLY OF ANTRIM LOOP 8%, SEC 10-15-14 8%, 3.95 AC SEC 10-15-14 8%, PUBLIC DRAINAGE 8%, LYG W & ADJ MIDVALE PK RD .50  8%, & ADJ TO 40/20 6.52 AC SEC 10- 8%, FOR RD .23 AC SEC 17-14-15 8%, IN PART OF ABANDONED ALLEY 8%, SELY PORT OF BLK 1 8%, (RESOLUTION-ORD #5632 8/3/82) 8%

LEGAL3: (AB 9472/1390) 43%, (DRE 251/570 RD 862/284) 29%, (RD 854/213 RD 3418/153) 14%, (DRE 251/570 & 325/181 & RD 86 14%

LOT: nan 41%, 00001 17%, 00003 7%, 00008 7%, 00005 7%, 001 3%, 00002 3%, 00012 3%, 00009 3%, 00027 3%, 00010 3%

MAIL2: . 71%, REAL ESTATE DIVISION 22%, ATTN: HOUSING AND COMMUNITY DE 7%

MAIL3: . 72%, ATTN: PROPERTY MANAGEMENT 12%, ATTN: PROPERTY MANAGMENT 10%, PO BOX 27210 5%

MAIL4: PO BOX 27210 83%, TUCSON AZ 17%

MAIL5: TUCSON AZ 100%

MP: nan 31%, 03026 20%, 02020 11%, 02004 9%, 16090 6%, 60049 6%, 46037 3%, 47004 3%, 53051 3%, 58099 3%, 20080 3%, 02039 3%

DOCKET: nan 29%, 11226 12%, 0 8%, 6180 8%, 107 8%, 11090 8%, 8447 4%, 11125 4%, 7827 4%, 4182 4%, 3136 4%, 6948 4%

SECTMODIF: nan 100%

TAXAREA: 0150 78%, 1250 10%, 1050 10%, 2050 2%

ZIP: 00000 71%, 85726 29%

ZIP4: 0000 71%, 7210 29%

FCV: 500 44%, 29000 8%, 39000 8%, 11200 8%, 260000 4%, 25000 4%, 72000 4%, 22000 4%, 1003 4%, 5250 4%, 9100 4%, 12400 4%

ADDRESSEE: CITY OF TUCSON 71%, CITY OF TUCSON
REAL ESTATE DI 12%, CITY OF TUCSON
REAL ESTATE DI 10%, CITY OF TUCSON
ATTN: HOUSING  5%, CITY OF TUCSON
ATTN: HOUSING  2%

ADDRESS: nan 71%, PO BOX 27210 29%

CITY: nan 71%, TUCSON 29%

STATE_PROVINCE: nan 71%, AZ 29%

POSTAL_CODE: nan 71%, 85726-7210 29%

SITE_ADDRESS: nan 80%, 6184 S COLUMBUS BL 2%, 744 E 39TH ST 2%, 1415 S 10TH AV 2%, 937 S OSBORNE AV 2%, 628 N ANITA AV 2%, 1073 N CONTZEN AV 2%, 526 W DAVIS ST 2%, 201 E NAVAJO RD 2%

SITE_ZIP: 85705 50%, 85713 25%, 85706 12%, 85701 12%

SITE_ZIPCITY: TUCSON 100%

URL: https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%

URL2: http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%

ADR_STATUS: NONE 80%, ONE 17%, MULTIPLE 2%

LEGAL_DESC: SILVER PASS DRAINAGEWAYS 8%, VALENCIA ALVERNON COMMERCE CEN 8%, W45' E257.12' N420' S2240.9' E 8%, W410' OF E667.12' OF N420' OF  8%, RANCHO REYES II; PUBLIC DRAINA 8%, N36' M/L S2286' W580.50' E680. 8%, DRAINAGEWAY IN CTRL NLY PTN W2 8%, S10' OF N659.83 M/L OF LOT 5 E 8%, CENTENNIAL PARK NO 3 WELLSITE  8%, CENTENNIAL PARK NO 3 PARCEL AP 8%, CENTENNIAL TERRACES DRAINAGEWA 8%, TANQUE VERDE TERRACE S 30' OF  8%

YEARBUILT: nan 98%, 1969 2%

LAST_EDITED_USER: GISPARFAB 88%, u142832@CENTRAL 5%, u116448@CENTRAL 2%, Ajanson2@CENTRAL 2%, JArechederra2@CENTRAL 2%

GLOBALID: 397026ff-139f-42b2-a441-c0f4e6 8%, 6a9a93dd-92a6-440c-ab1c-8e9b79 8%, f7efaf59-adff-4bc2-89dd-6a97e4 8%, 460f9e83-6a76-48d5-b932-d4ecca 8%, 9dfa823b-205d-4ddd-b705-0b07cd 8%, d1ad63ba-851e-4dc3-a859-5dac68 8%, 7364aa0c-07e8-46fd-ba88-a6cccd 8%, 2ec99b3d-4e86-45bb-9bee-fbb898 8%, e70e16d6-c27c-4ad3-88aa-261dce 8%, b4335f37-77df-414c-81c9-a9e33c 8%, ada87719-0c83-4d38-812a-d28a4c 8%, 8a0c4244-2774-4900-8cc0-c4b051 8%

GEOMETRY: {"type": "MultiPolygon", "coor 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 41 | 0 | 41 1; 40 1; 39 1; 38 1 |
| PARCEL | category | 41 | 0 | 14113834A 1; 14032145A 1; 14032002J 1; 14032002F 1 |
| GISAREA | amount | 41 | 0 | 10771.37417251 1; 114412.61334092 1; 18830.9196303 1; 169389.15971171 1 |
| GISACRES | amount | 40 | 0 | 0.24726767 1; 2.62645595 1; 0.43228259 1; 3.88849755 1 |
| X_HPGN | amount | 41 | 0 | 1045665.66411197 1; 1013540.16776118 1; 1014278.3460622 1; 1014053.75856458 1 |
| Y_HPGN | amount | 41 | 0 | 406600.65356368 1; 415559.85225139 1; 416105.62333069 1; 416101.9142924 1 |
| LON | category | 41 | 0 | -110.80022587 1; -110.90369909 1; -110.90129792 1; -110.90202353 1 |
| LAT | category | 41 | 0 | 32.1129105 1; 32.1384074 1; 32.13988837 1; 32.139884 1 |
| LOT_R | category | 15 | 8 | nan 12; 1 6; 3 2; 8 2 |
| LINK | category | 41 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 18 | 0 | 141324E 9; 141311E 8; 141313E 4; 151410E 3 |
| MP_OL | category | 20 | 0 | nan 9; 03026 7; 02020 4; 02004 3 |
| SEQ_NUM_S | category | 4 | 29 | nan 9; 20052270612 2; 97155305 1 |
| JURIS_OL | who | 1 | 0 | TUCSON 41 |
| CURZONE_OL | other | 1 | 0 | R-3 41 |
| ADDRESS_OL | category | 8 | 0 | nan 34; 6184 S COLUMBUS BL 1; 744 E 39TH ST 1; 937 S OSBORNE AV 1 |
| SEQ_NUM_D | category | 15 | 0 | 0.0 19; nan 6; 20000220283.0 3; 19991360588.0 2 |
| PARCEL_USE | other | 1 | 0 | 9700 41 |
| LANDMEAS | amount | 32 | 0 | 0.1 9; 1.0 2; 115131.0 1; 9.0 1 |
| LANDUNIT | category | 3 | 0 | F 21; S 15; A 5 |
| LASTCHANGE | date | 16 | 0 | 1121126400000 21; 1215388800000 4; 1580342400000 2; 1256774400000 2 |
| LEGAL1 | category | 41 | 0 | SILVER PASS DRAINAGEWAYS 1; VALENCIA ALVERNON COMMERC 1; W45' E257.12' N420' S2240 1; W410' OF E667.12' OF N420 1 |
| LEGAL2 | category | 32 | 9 | ABAND ALLEY BLK 138 2; LYG SLY OF ANTRIM LOOP 1; SEC 10-15-14 1; 3.95 AC SEC 10-15-14 1 |
| LEGAL3 | category | 5 | 34 | (AB 9472/1390) 3; (DRE 251/570 RD 862/284) 2; (RD 854/213 RD 3418/153) 1; (DRE 251/570 & 325/181 &  1 |
| LEGAL4 | empty | 1 | 41 |  |
| LEGAL5 | empty | 1 | 41 |  |
| LOT | category | 16 | 8 | nan 12; 00001 5; 00003 2; 00008 2 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 41 |
| MAIL2 | category | 3 | 0 | . 29; REAL ESTATE DIVISION 9; ATTN: HOUSING AND COMMUNI 3 |
| MAIL3 | category | 5 | 1 | . 29; ATTN: PROPERTY MANAGEMENT 5; ATTN: PROPERTY MANAGMENT 4; PO BOX 27210 2 |
| MAIL4 | category | 3 | 29 | PO BOX 27210 10; TUCSON AZ 2 |
| MAIL5 | category | 2 | 31 | TUCSON AZ 10 |
| MP | category | 18 | 0 | nan 11; 03026 7; 02020 4; 02004 3 |
| PAGE | amount | 29 | 0 | nan 7; 691.0 3; 0.0 2; 1336.0 2 |
| RECORDDATE | date | 24 | 0 | nan 14; 20000202 3; 19791221 2; 19990716 2 |
| DOCKET | category | 29 | 0 | nan 7; 11226 3; 0 2; 6180 2 |
| RECTRACT | empty | 2 | 41 |  |
| SECTMODIF | category | 2 | 13 | nan 28 |
| TAXAREA | category | 4 | 0 | 0150 32; 1250 4; 1050 4; 2050 1 |
| ZIP | category | 2 | 0 | 00000 29; 85726 12 |
| ZIP4 | category | 2 | 0 | 0000 29; 7210 12 |
| TAXYR | other | 1 | 0 | 2023 41 |
| LIMNET | other | 1 | 0 | 0 41 |
| FCV | category | 28 | 0 | 500 11; 29000 2; 39000 2; 11200 2 |
| SHAPE_LENG | empty | 1 | 41 |  |
| ADDRESSEE | category | 5 | 0 | CITY OF TUCSON 29; CITY OF TUCSON
REAL ESTA 5; CITY OF TUCSON
REAL ESTA 4; CITY OF TUCSON
ATTN: HOU 2 |
| ADDRESS | category | 2 | 0 | nan 29; PO BOX 27210 12 |
| CITY | category | 2 | 0 | nan 29; TUCSON 12 |
| STATE_PROVINCE | category | 2 | 0 | nan 29; AZ 12 |
| COUNTRY | empty | 1 | 41 |  |
| POSTAL_CODE | category | 2 | 0 | nan 29; 85726-7210 12 |
| SITE_ADDRESS | category | 9 | 0 | nan 33; 6184 S COLUMBUS BL 1; 744 E 39TH ST 1; 1415 S 10TH AV 1 |
| SITE_ZIP | category | 5 | 33 | 85705 4; 85713 2; 85706 1; 85701 1 |
| SITE_ZIPCITY | category | 2 | 33 | TUCSON 8 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     41 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      41 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             41 |
| DATASOURCE | who | 1 | 0 | PAREGION 41 |
| URL | category | 41 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | category | 41 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 3 | 0 | NONE 33; ONE 7; MULTIPLE 1 |
| LEGAL_DESC | category | 41 | 0 | SILVER PASS DRAINAGEWAYS 1; VALENCIA ALVERNON COMMERC 1; W45' E257.12' N420' S2240 1; W410' OF E667.12' OF N420 1 |
| OWN | other | 1 | 0 | City 41 |
| VAN | who | 1 | 0 | not_van 41 |
| YEARBUILT | category | 2 | 0 | nan 40; 1969 1 |
| LAST_EDITED_USER | category | 5 | 0 | GISPARFAB 36; u142832@CENTRAL 2; u116448@CENTRAL 1; Ajanson2@CENTRAL 1 |
| LAST_EDITED_DATE | date | 35 | 0 | 1603156969000 2; 1603185741000 2; 1603158355000 2; 1603158765000 2 |
| GLOBALID | category | 40 | 0 | 397026ff-139f-42b2-a441-c 1; 6a9a93dd-92a6-440c-ab1c-8 1; f7efaf59-adff-4bc2-89dd-6 1; 460f9e83-6a76-48d5-b932-d 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 41 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 41 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 41 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 41 |
| SHAPE__AREA | amount | 39 | 0 | 1398.86328125 1; 14867.48828125 1; 2447.07421875 1; 22012.109375 1 |
| SHAPE__LENGTH | amount | 41 | 0 | 253.18782568409614 1; 1233.98363538931 1; 334.7951761840708 1; 593.5906669261035 1 |
| GEOMETRY | category | 41 | 0 | {"type": "MultiPolygon",  1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:48:02.60584 41 |
| SOURCE_RUN_ID | audit | 1 | 0 | dac305d0-761e-4f35-bc32-5 41 |
| SRC_SHA256 | who | 1 | 0 | 38cc1b93b165f8af2e85037ff 41 |
