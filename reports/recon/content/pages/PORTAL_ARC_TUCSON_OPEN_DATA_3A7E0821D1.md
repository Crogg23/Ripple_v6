# PORTAL_ARC_TUCSON_OPEN_DATA_3A7E0821D1

rows 61  columns 80  scan 4.7s

roles: amount 9, audit 2, category 34, date 6, empty 6, other 14, who 10

## when

LASTCHANGE
  2005        34  ##############################
  2006         1  #
  2008         6  #####
  2009         1  #
  2011         1  #
  2012         1  #
  2014         3  ###
  2015         2  ##
  2016         1  #
  2017         1  #
  2018         1  #
  2019         2  ##
  2020         4  ####
  2023         3  ###

RECORDDATE
  1964         1  ##########
  1966         1  ##########
  1971         3  ##############################
  1972         3  ##############################
  1973         1  ##########
  1974         1  ##########
  1975         2  ####################
  1979         3  ##############################
  1980         1  ##########
  1981         1  ##########
  1982         1  ##########
  1983         1  ##########
  1984         1  ##########
  1988         1  ##########
  1989         1  ##########
  1991         1  ##########
  1992         1  ##########
  1993         3  ##############################
  1994         2  ####################
  1995         1  ##########
  1997         2  ####################
  1998         2  ####################
  1999         3  ##############################
  2000         3  ##############################
  2005         1  ##########
  2009         1  ##########
  2014         1  ##########
  2015         2  ####################
  2019         1  ##########

LAST_EDITED_DATE
  2020        55  ##############################
  2021         1  #
  2022         2  #
  2023         3  ##

CREATED_DATE_COT
  2023        61  ##############################

LAST_EDITED_DATE_COT
  2023        61  ##############################

INGESTED_AT
  2026        61  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 61 | 424.18 | 24.8K | 471.8K | 526.5K | 3.72M |
| GISACRES | 61 | 0.01 | 0.57 | 10.83 | 12.09 | 85.35 |
| X_HPGN | 61 | 975.2K | 991.4K | 1.05M | 1.05M | 60.93M |
| Y_HPGN | 61 | 413.2K | 441.3K | 460.2K | 462.1K | 26.85M |
| LANDMEAS | 61 | 0.10 | 10.0K | 465.8K | 517.1K | 2.89M |
| PAGE | 55 | 0 | 691 | 5.0K | 5.2K | 61.3K |

## who

JURIS_OL by rows
        61  TUCSON

JURIS_OL by dollars
       3.72M       61 rows  TUCSON

MAIL1 by rows
        61  CITY OF TUCSON

MAIL1 by dollars
       3.72M       61 rows  CITY OF TUCSON

USE_DESC by rows
        61  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
       3.72M       61 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        61  MISC REL/GVT/IN     

SPT_DESC by dollars
       3.72M       61 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:2.84M 2021:6.7K 2022:561.7K 2023:309.0K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:2.84M 2021:6.7K 2022:561.7K 2023:309.0K

## what

LOT_R: nan 48%, 1 21%, 8 7%, 3 5%, 5 5%, 50 2%, 14 2%, 13 2%, B 2%, C 2%, 87 2%

TRS_OL: 141311E 23%, 141324E 19%, 141314E 13%, 141313E 11%, 151301E 9%, 151312E 6%, 141303E 4%, 151410E 4%, 141515E 4%, 151313E 2%, 141535E 2%, 141522E 2%

MP_OL: nan 42%, 03026 16%, 02004 9%, 02020 9%, 03043 5%, 16090 5%, 04041 2%, 05014 2%, 09026 2%, 39043 2%, 24075 2%, 48038 2%

SEQ_NUM_S: nan 86%, 96078470 5%, 20061890684 5%, 97145981 5%

CURZONE_OL: R-3 51%, R-2 49%

ADDRESS_OL: nan 84%, 5101 S NOGALES HY 2%, 455 W 5TH ST 2%, 6184 S COLUMBUS BL 2%, 744 E 39TH ST 2%, 201 E NAVAJO RD 2%, 5500 S NOGALES HY 2%, 937 S OSBORNE AV 2%, 628 N ANITA AV 2%, 1073 N CONTZEN AV 2%, 526 W DAVIS ST 2%

SEQ_NUM_D: 0.0 63%, nan 10%, 20000220283.0 6%, 94065783.0 4%, 19991360588.0 4%, 20152580666.0 2%, 97078237.0 2%, 20141630049.0 2%, 19981380939.0 2%, 20223620514.0 2%, 20221740178.0 2%, 20052051165.0 2%

LANDUNIT: F 69%, S 28%, A 3%

LEGAL2: DWY IN NE4 SE4 EXC N75' FOR RD 15%, ABAND ALLEY BLK 138 15%, SEC 13-15-13 8%, LYG SWLY OF DRAINAGEWAY 8%, LOTS 177 & 202 8%, .64 AC SEC 26-14-13E 8%, RONALD RD 8%, OF STREETS (RD 245/532) 8%, MANOR 2.24 AC SEC 14-14-13 8%, & W GRANADA AVE 8%, LINE OF PALOMAS AV EXTENDED .7 8%

LEGAL3: (AB 9472/1390) 27%, NELY COR LOT 1 3.48 AC SEC 1-1 18%, (DRE 251/570 RD 862/284) 18%, (RD 8600/613) 9%, 1.91 AC SEC 14-14-13E 9%, (RD 854/213 RD 3418/153) 9%, (DRE 251/570 & 325/181 & RD 86 9%

LOT: nan 49%, 00001 20%, 00008 7%, 00003 5%, 00005 5%, 00050 2%, 00014 2%, 00013 2%, 0000B 2%, 0000C 2%, 00087 2%

MAIL2: . 72%, REAL ESTATE DIVISION 18%, PO BOX 27210 5%, ATTN: HOUSING AND COMMUNITY DE 5%

MAIL3: . 73%, ATTN: PROPERTY MANAGMENT 8%, ATTN: PROPERTY MANAGEMENT 8%, TUCSON AZ 3%, PO BOX 27210 3%, TUCSON  AZ 2%, ATTN:  PROPERTY MANAGEMENT 2%

MAIL4: PO BOX 27210 86%, TUCSON AZ 14%

MAIL5: TUCSON AZ 100%

MP: nan 45%, 03026 16%, 02020 9%, 02004 7%, 03043 5%, 16090 5%, 04041 2%, 05014 2%, 09026 2%, 39043 2%, 48038 2%, 04044 2%

DOCKET: nan 22%, 0 15%, 11226 11%, 9761 7%, 4224 7%, 107 7%, 6180 7%, 11090 7%, 4879 4%, 6675 4%, 3999 4%, 8327 4%

SECTMODIF: nan 100%

TAXAREA: 0150 80%, 1250 16%, 1050 3%

ZIP: 00000 72%, 85726 28%

ZIP4: 0000 72%, 7210 28%

TAXYR: 2023 98%, nan 2%

LIMNET: 0.0 98%, nan 2%

ADDRESSEE: CITY OF TUCSON 77%, CITY OF TUCSON
REAL ESTATE DI 8%, CITY OF TUCSON
REAL ESTATE DI 8%, CITY OF TUCSON
ATTN: HOUSING  3%, CITY OF TUCSON
ATTN: HOUSING  2%, CITY OF TUCSON
REAL ESTATE DI 2%

ADDRESS: nan 72%, PO BOX 27210 28%

CITY: nan 72%, TUCSON 26%, TUCSON  2%

STATE_PROVINCE: nan 72%, AZ 28%

POSTAL_CODE: nan 72%, 85726-7210 28%

SITE_ADDRESS: nan 82%, 5101 S NOGALES HY 2%, 455 W 5TH ST 2%, 6184 S COLUMBUS BL 2%, 744 E 39TH ST 2%, 201 E NAVAJO RD 2%, 5901 S FIESTA AV 2%, 1415 S 10TH AV 2%, 937 S OSBORNE AV 2%, 628 N ANITA AV 2%, 1073 N CONTZEN AV 2%, 526 W DAVIS ST 2%

SITE_ZIP: 85705 45%, 85706 27%, 85713 18%, 85701 9%

SITE_ZIPCITY: TUCSON 100%

ADR_STATUS: NONE 80%, ONE 16%, MULTIPLE 3%

YEARBUILT: nan 98%, 1969 2%

LAST_EDITED_USER: GISPARFAB 90%, u116448@CENTRAL 3%, KChristensen2@CENTRAL 3%, SGilpin2@CENTRAL 2%, Ajanson2@CENTRAL 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 61 | 0 | 78 1; 76 1; 75 1; 74 1 |
| PARCEL | other | 59 | 0 | 13701008E 2; 13815008C 1; 138120210 1; 13811015A 1 |
| GISAREA | amount | 60 | 0 | 144551.0398092 2; 22424.13690458 1; 40615.15655206 1; 25167.61730295 1 |
| GISACRES | amount | 57 | 0 | 3.31831367 2; 0.51476849 1; 0.93236153 1; 0.57774782 1 |
| X_HPGN | amount | 60 | 0 | 995798.82317899 2; 994222.3637409 1; 993439.54971491 1; 994352.6791529 1 |
| Y_HPGN | amount | 58 | 0 | 422620.45155166 2; 413158.194957 1; 416993.38255378 1; 416169.97278063 1 |
| LON | other | 60 | 0 | -110.96080726 2; -110.9661708 1; -110.96859035 1; -110.96566408 1 |
| LAT | other | 60 | 0 | 32.15825974 2; 32.13229028 1; 32.14285059 1; 32.14056535 1 |
| LOT_R | category | 21 | 10 | nan 20; 1 9; 8 3; 3 2 |
| LINK | other | 60 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 2; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 26 | 0 | 141311E 11; 141324E 9; 141314E 6; 141313E 5 |
| MP_OL | category | 30 | 0 | nan 18; 03026 7; 02004 4; 02020 4 |
| SEQ_NUM_S | category | 5 | 40 | nan 18; 96078470 1; 20061890684 1; 97145981 1 |
| JURIS_OL | who | 1 | 0 | TUCSON 61 |
| CURZONE_OL | category | 2 | 0 | R-3 31; R-2 30 |
| ADDRESS_OL | category | 11 | 0 | nan 51; 5101 S NOGALES HY 1; 455 W 5TH ST 1; 6184 S COLUMBUS BL 1 |
| SEQ_NUM_D | category | 21 | 0 | 0.0 33; nan 5; 20000220283.0 3; 94065783.0 2 |
| PARCEL_USE | other | 1 | 0 | 9700 61 |
| LANDMEAS | amount | 50 | 0 | 0.1 8; 1.0 4; 151644.0 2; 26771.0 1 |
| LANDUNIT | category | 3 | 0 | F 42; S 17; A 2 |
| LASTCHANGE | date | 22 | 0 | 1121126400000 34; 1215388800000 5; 1418802546000 2; 1580342400000 2 |
| LEGAL1 | other | 60 | 0 | 50' PCL LYG ELY & ADJ TO  2; VACATED LERDO RD IN NW4 N 1; MISSIONDALE LOT 1 BLK 4 1; EMERY PARK UNIT NO 2 IRR  1 |
| LEGAL2 | category | 39 | 21 | DWY IN NE4 SE4 EXC N75' F 2; ABAND ALLEY BLK 138 2; SEC 13-15-13 1; LYG SWLY OF DRAINAGEWAY 1 |
| LEGAL3 | category | 8 | 50 | (AB 9472/1390) 3; NELY COR LOT 1 3.48 AC SE 2; (DRE 251/570 RD 862/284) 2; (RD 8600/613) 1 |
| LEGAL4 | empty | 1 | 61 |  |
| LEGAL5 | empty | 1 | 61 |  |
| LOT | category | 22 | 10 | nan 20; 00001 8; 00008 3; 00003 2 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 61 |
| MAIL2 | category | 4 | 0 | . 44; REAL ESTATE DIVISION 11; PO BOX 27210 3; ATTN: HOUSING AND COMMUNI 3 |
| MAIL3 | category | 8 | 1 | . 44; ATTN: PROPERTY MANAGMENT 5; ATTN: PROPERTY MANAGEMENT 5; TUCSON AZ 2 |
| MAIL4 | category | 3 | 47 | PO BOX 27210 12; TUCSON AZ 2 |
| MAIL5 | category | 2 | 49 | TUCSON AZ 12 |
| MP | category | 29 | 0 | nan 20; 03026 7; 02020 4; 02004 3 |
| PAGE | amount | 45 | 0 | nan 6; 0.0 4; 691.0 3; 4774.0 2 |
| RECORDDATE | date | 41 | 0 | nan 15; 20000202 3; 19940331 2; 19720406 2 |
| DOCKET | category | 46 | 0 | nan 6; 0 4; 11226 3; 9761 2 |
| RECTRACT | empty | 2 | 61 |  |
| SECTMODIF | category | 2 | 18 | nan 43 |
| TAXAREA | category | 3 | 0 | 0150 49; 1250 10; 1050 2 |
| ZIP | category | 2 | 0 | 00000 44; 85726 17 |
| ZIP4 | category | 2 | 0 | 0000 44; 7210 17 |
| TAXYR | category | 2 | 0 | 2023 60; nan 1 |
| LIMNET | category | 2 | 0 | 0.0 60; nan 1 |
| FCV | amount | 46 | 0 | 500.0 10; 53000.0 2; 148000.0 2; 122000.0 2 |
| SHAPE_LENG | empty | 1 | 61 |  |
| ADDRESSEE | category | 6 | 0 | CITY OF TUCSON 47; CITY OF TUCSON
REAL ESTA 5; CITY OF TUCSON
REAL ESTA 5; CITY OF TUCSON
ATTN: HOU 2 |
| ADDRESS | category | 2 | 0 | nan 44; PO BOX 27210 17 |
| CITY | category | 3 | 0 | nan 44; TUCSON 16; TUCSON  1 |
| STATE_PROVINCE | category | 2 | 0 | nan 44; AZ 17 |
| COUNTRY | empty | 1 | 61 |  |
| POSTAL_CODE | category | 2 | 0 | nan 44; 85726-7210 17 |
| SITE_ADDRESS | category | 12 | 0 | nan 50; 5101 S NOGALES HY 1; 455 W 5TH ST 1; 6184 S COLUMBUS BL 1 |
| SITE_ZIP | category | 5 | 50 | 85705 5; 85706 3; 85713 2; 85701 1 |
| SITE_ZIPCITY | category | 2 | 50 | TUCSON 11 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     61 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      61 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             61 |
| DATASOURCE | who | 1 | 0 | PAREGION 61 |
| URL | other | 59 | 0 | https://pro.tucsonaz.gov/ 2; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | other | 59 | 0 | http://gis.pima.gov/maps/ 2; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 3 | 0 | NONE 49; ONE 10; MULTIPLE 2 |
| LEGAL_DESC | other | 60 | 0 | 50' PCL LYG ELY & ADJ TO  2; VACATED LERDO RD IN NW4 N 1; MISSIONDALE LOT 1 BLK 4 1; EMERY PARK UNIT NO 2 IRR  1 |
| OWN | other | 1 | 0 | City 61 |
| VAN | who | 1 | 0 | not_van 61 |
| YEARBUILT | category | 2 | 0 | nan 60; 1969 1 |
| LAST_EDITED_USER | category | 5 | 0 | GISPARFAB 55; u116448@CENTRAL 2; KChristensen2@CENTRAL 2; SGilpin2@CENTRAL 1 |
| LAST_EDITED_DATE | date | 53 | 0 | 1603188132000 2; 1603158433000 2; 1603200631000 2; 1648074242000 2 |
| GLOBALID | other | 61 | 0 | 869a222a-bebb-49b6-b326-7 1; ec380ed0-d827-43db-9b19-3 1; fe36c346-a59c-4329-96d5-6 1; 0c5704da-61c9-4e8e-b04b-b 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 61 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 61 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 61 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 61 |
| PARCELSIZE | other | 60 | 0 | 144550 2; 22424 1; 40615 1; 25168 1 |
| PARCELSIZECLASS | empty | 1 | 61 |  |
| SHAPE__AREA | amount | 58 | 0 | 18792.2890625 2; 2913.48046875 1; 5278.4296875 1; 3270.6743978857994 1 |
| SHAPE__LENGTH | amount | 60 | 0 | 2158.586204073842 2; 631.3842357679291 1; 320.0522619255216 1; 290.32496174466166 1 |
| GEOMETRY | other | 58 | 0 | {"type": "Polygon", "coor 2; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:48:20.92747 61 |
| SOURCE_RUN_ID | audit | 1 | 0 | 62f3f521-09d4-4878-8ed5-a 61 |
| SRC_SHA256 | who | 1 | 0 | 9152cba702c3aced084742966 61 |
