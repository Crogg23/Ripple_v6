# PORTAL_ARC_TUCSON_OPEN_DATA_CDFFE1002A

rows 43  columns 78  scan 6.6s

roles: amount 9, audit 2, category 43, date 6, empty 6, other 3, who 10

## when

LASTCHANGE
  2005        25  ##############################
  2008         4  #####
  2011         2  ##
  2013         2  ##
  2014         3  ####
  2015         1  #
  2017         1  #
  2018         1  #
  2020         1  #
  2023         3  ####

RECORDDATE
  1971         3  ##############################
  1972         2  ####################
  1974         1  ##########
  1975         1  ##########
  1977         2  ####################
  1978         1  ##########
  1979         1  ##########
  1980         1  ##########
  1981         1  ##########
  1982         1  ##########
  1984         1  ##########
  1988         1  ##########
  1993         1  ##########
  1994         1  ##########
  1997         1  ##########
  1998         1  ##########
  1999         2  ####################
  2005         1  ##########
  2014         1  ##########
  2015         1  ##########

LAST_EDITED_DATE
  2020        36  ##############################
  2021         3  ##
  2022         1  #
  2023         3  ##

CREATED_DATE_COT
  2023        43  ##############################

LAST_EDITED_DATE_COT
  2023        43  ##############################

INGESTED_AT
  2026        43  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 43 | 20.3K | 54.6K | 488.2K | 526.5K | 4.32M |
| GISACRES | 43 | 0.47 | 1.25 | 11.21 | 12.09 | 99.09 |
| X_HPGN | 43 | 975.2K | 991.9K | 1.05M | 1.05M | 43.09M |
| Y_HPGN | 43 | 401.2K | 436.3K | 465.3K | 468.2K | 18.67M |
| LANDMEAS | 43 | 0.10 | 36.0K | 481.2K | 517.1K | 3.36M |
| PAGE | 28 | 0 | 597 | 5.1K | 5.2K | 28.6K |

## who

JURIS_OL by rows
        43  TUCSON

JURIS_OL by dollars
       4.32M       43 rows  TUCSON

MAIL1 by rows
        43  CITY OF TUCSON

MAIL1 by dollars
       4.32M       43 rows  CITY OF TUCSON

USE_DESC by rows
        43  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
       4.32M       43 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
        43  MISC REL/GVT/IN     

SPT_DESC by dollars
       4.32M       43 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:2.84M 2021:640.4K 2022:526.5K 2023:309.0K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:2.84M 2021:640.4K 2022:526.5K 2023:309.0K

## what

OBJECTID: 43 8%, 42 8%, 41 8%, 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%

PARCEL: 141203980 8%, 141196620 8%, 140214160 8%, 140162520 8%, 13815008C 8%, 138133130 8%, 138120210 8%, 13811015A 8%, 137336890 8%, 137335750 8%, 13732259A 8%, 137118730 8%

LON: -110.7868851 8%, -110.77953539 8%, -110.94684233 8%, -110.9508511 8%, -110.9661708 8%, -110.97230453 8%, -110.96859035 8%, -110.96566408 8%, -111.00791397 8%, -110.99724674 8%, -110.99542777 8%, -110.99529589 8%

LAT: 32.10011922 8%, 32.0979829 8%, 32.1517865 8%, 32.15665957 8%, 32.13229028 8%, 32.14503177 8%, 32.14285059 8%, 32.14056535 8%, 32.13943926 8%, 32.14810115 8%, 32.15336278 8%, 32.15616552 8%

LOT_R: nan 57%, 1 13%, 50 3%, 8 3%, 3 3%, 2 3%, 14 3%, 13 3%, B 3%, C 3%, 87 3%

LINK: HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 8%

TRS_OL: 141314E 20%, 151312E 10%, 151301E 10%, 141311E 10%, 151526E 7%, 151406E 7%, 151310E 7%, 151303E 7%, 141511E 7%, 141336E 7%, 141303E 7%, 151313E 3%

MP_OL: nan 46%, 40058 8%, 03043 8%, 56057 4%, 40012 4%, 24014 4%, 04041 4%, 05014 4%, 52058 4%, 40019 4%, 39073 4%, 53013 4%

SEQ_NUM_S: nan 58%, 86175010 11%, 20022250738 5%, 86124884 5%, 20000050083 5%, 96078470 5%, 97145981 5%, 20061890684 5%

ADDRESS_OL: nan 84%, 6220 S HEADLEY RD 2%, 5101 S NOGALES HY 2%, 5500 S NOGALES HY 2%, 4050 S APACHE WELL DR 2%, 357 W PENNSYLVANIA DR 2%, 455 W 5TH ST 2%, 4255 N 4TH AV 2%

SEQ_NUM_D: 0.0 49%, nan 33%, 94065783.0 2%, 20223620514.0 2%, 20221740178.0 2%, 20052051165.0 2%, 20152580666.0 2%, 97078237.0 2%, 20141630049.0 2%, 19990470328.0 2%

LANDUNIT: F 67%, S 28%, A 5%

LEGAL1: HACIENDA DEL ORO 15%, ARROYO VISTA RODEO WASH 8%, AMHERST SOUTH RODEO WASH DRGWY 8%, VACATED LERDO RD IN NW4 NE4 .6 8%, MISSION HEIGHTS NO 5 PUBLIC PA 8%, MISSIONDALE LOT 1 BLK 4 8%, EMERY PARK UNIT NO 2 IRR PORT  8%, CAMBRIE AT MIDVALE PARK DRAINA 8%, 60' DRAINAGEWAY IN NE4 NE4 LYG 8%, WOODBRIDGE AT MIDVALE PARK PUB 8%, WOODBRIDGE III DRAINAGEWAY 8%, RODEO W PT OF BLK 2 8%

LEGAL2: DRAINAGEWAYS 17%, SEC 13-15-13 8%, (9539/1435) 8%, LYG SWLY OF DRAINAGEWAY 8%, MIDVALE PARK RD & S OF DREXEL  8%, DRAINAGEWAY EXC BETWEEN LOTS 1 8%, DWY IN NE4 SE4 EXC N75' FOR RD 8%, W LINE OF NOGALES HWY 2.75 AC  8%, LOTS 177 & 202 8%, TO 49/45 8%, BLK 57 8%

LEGAL3: (RD 8600/613) 20%, SEC 10-15-13 20%, 206, 229 & 230, 241 & 242 20%, NELY COR LOT 1 3.48 AC SEC 1-1 20%, 1.91 AC SEC 14-14-13E 20%

LOT: nan 57%, 00001 13%, 00050 3%, 00008 3%, 00003 3%, 00002 3%, 00014 3%, 00013 3%, 0000B 3%, 0000C 3%, 00087 3%

MAIL2: . 74%, REAL ESTATE DIVISION 19%, PO BOX 27210 7%

MAIL3: . 72%, ATTN: PROPERTY MANAGMENT 12%, TUCSON AZ 5%, ATTN: PROPERTY MANAGEMENT 5%, .. 2%, ATTN:  PROPERTY MANAGEMENT 2%, TUCSON  AZ 2%

MAIL4: PO BOX 27210 80%, . 20%

MAIL5: TUCSON AZ 80%, . 20%

MP: nan 50%, 40058 8%, 03043 8%, 56057 4%, 40012 4%, 24014 4%, 04041 4%, 05014 4%, 52058 4%, 53013 4%, 09026 4%, 39043 4%

DOCKET: nan 54%, 5539 7%, 0 7%, 4879 4%, 4351 4%, 6675 4%, 3999 4%, 8327 4%, 9761 4%, 10849 4%, 7320 4%, 4224 4%

SECTMODIF: nan 100%

TAXAREA: 0150 72%, 1250 21%, 2050 5%, 1050 2%

ZIP: 00000 74%, 85726 26%

ZIP4: 0000 74%, 7210 26%

TAXYR: 2023 98%, nan 2%

LIMNET: 0.0 98%, nan 2%

ADDRESSEE: CITY OF TUCSON 81%, CITY OF TUCSON
REAL ESTATE DI 12%, CITY OF TUCSON
REAL ESTATE DI 5%, CITY OF TUCSON
REAL ESTATE DI 2%

ADDRESS: nan 74%, PO BOX 27210 26%

CITY: nan 74%, TUCSON 23%, TUCSON  2%

STATE_PROVINCE: nan 74%, AZ 26%

POSTAL_CODE: nan 74%, 85726-7210 26%

SITE_ADDRESS: nan 84%, 5901 S FIESTA AV 2%, 6220 S HEADLEY RD 2%, 5101 S NOGALES HY 2%, 4050 S APACHE WELL DR 2%, 357 W PENNSYLVANIA DR 2%, 455 W 5TH ST 2%, 4255 N 4TH AV 2%

SITE_ZIP: 85706 29%, 85705 29%, 85746 14%, 85730 14%, 85714 14%

SITE_ZIPCITY: TUCSON 100%

URL: https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%, https://pro.tucsonaz.gov/parce 8%

URL2: http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%, http://gis.pima.gov/maps/detai 8%

ADR_STATUS: NONE 81%, ONE 16%, MULTIPLE 2%

LEGAL_DESC: HACIENDA DEL ORO; DRAINAGEWAYS 15%, ARROYO VISTA RODEO WASH 8%, AMHERST SOUTH RODEO WASH DRGWY 8%, VACATED LERDO RD IN NW4 NE4 .6 8%, MISSION HEIGHTS NO 5 PUBLIC PA 8%, MISSIONDALE LOT 1 BLK 4 8%, EMERY PARK UNIT NO 2 IRR PORT  8%, CAMBRIE AT MIDVALE PARK DRAINA 8%, 60' DRAINAGEWAY IN NE4 NE4 LYG 8%, WOODBRIDGE AT MIDVALE PARK PUB 8%, WOODBRIDGE III DRAINAGEWAY 8%, RODEO W PT OF BLK 2 8%

LAST_EDITED_USER: GISPARFAB 84%, u142832@CENTRAL 7%, KChristensen2@CENTRAL 5%, u116448@CENTRAL 2%, SGilpin2@CENTRAL 2%

GLOBALID: b2acaacd-a641-4c5a-8f8c-dbb1f3 8%, 5694fcc8-60f2-4491-8880-5d0785 8%, c0e0dd58-0327-4cc8-95e7-f2e716 8%, 51bbce80-8f44-4c88-ba31-839f7f 8%, 4560273d-cff3-435f-b0b3-68e224 8%, 67badecd-1b98-4bcd-9328-f740a2 8%, e791331e-d393-4d93-8cc5-59fa91 8%, 978f08b0-59a7-4c8e-b82b-fdee32 8%, 2c2e97fe-8ded-4fa5-b1db-6bbb61 8%, 14e7c91c-8af4-4d1c-962a-76e2e1 8%, 2f3f007b-e771-4440-b3b9-87dcc4 8%, 4fe3d16c-4990-4add-9421-a12d2b 8%

GEOMETRY: {"type": "MultiPolygon", "coor 8%, {"type": "MultiPolygon", "coor 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "MultiPolygon", "coor 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 43 | 0 | 43 1; 42 1; 41 1; 40 1 |
| PARCEL | category | 43 | 0 | 141203980 1; 141196620 1; 140214160 1; 140162520 1 |
| GISAREA | amount | 43 | 0 | 112111.49353356 1; 243280.11559792 1; 73712.62301184 1; 45675.49359393 1 |
| GISACRES | amount | 41 | 0 | 2.57363145 1; 5.58473833 1; 1.69214697 1; 1.04852663 1 |
| X_HPGN | amount | 43 | 0 | 1049845.20002437 1; 1052129.39492404 1; 1000141.65442341 1; 998885.19336623 1 |
| Y_HPGN | amount | 42 | 0 | 401990.20038818 1; 401236.91853525 1; 420303.79863803 1; 422065.83847035 1 |
| LON | category | 43 | 0 | -110.7868851 1; -110.77953539 1; -110.94684233 1; -110.9508511 1 |
| LAT | category | 43 | 0 | 32.10011922 1; 32.0979829 1; 32.1517865 1; 32.15665957 1 |
| LOT_R | category | 13 | 12 | nan 17; 1 4; 50 1; 8 1 |
| LINK | category | 43 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 25 | 0 | 141314E 6; 151312E 3; 151301E 3; 141311E 3 |
| MP_OL | category | 31 | 0 | nan 11; 40058 2; 03043 2; 56057 1 |
| SEQ_NUM_S | category | 9 | 24 | nan 11; 86175010 2; 20022250738 1; 86124884 1 |
| JURIS_OL | who | 1 | 0 | TUCSON 43 |
| CURZONE_OL | other | 1 | 0 | R-2 43 |
| ADDRESS_OL | category | 8 | 0 | nan 36; 6220 S HEADLEY RD 1; 5101 S NOGALES HY 1; 5500 S NOGALES HY 1 |
| SEQ_NUM_D | category | 10 | 0 | 0.0 21; nan 14; 94065783.0 1; 20223620514.0 1 |
| PARCEL_USE | other | 1 | 0 | 9700 43 |
| LANDMEAS | amount | 34 | 0 | 0.1 7; 1.0 2; 6.0 2; 115779.0 1 |
| LANDUNIT | category | 3 | 0 | F 29; S 12; A 2 |
| LASTCHANGE | date | 17 | 0 | 1121126400000 25; 1215388800000 3; 1359645568000 1; 1359645321000 1 |
| LEGAL1 | category | 42 | 0 | HACIENDA DEL ORO 2; ARROYO VISTA RODEO WASH 1; AMHERST SOUTH RODEO WASH  1; VACATED LERDO RD IN NW4 N 1 |
| LEGAL2 | category | 23 | 20 | DRAINAGEWAYS 2; SEC 13-15-13 1; (9539/1435) 1; LYG SWLY OF DRAINAGEWAY 1 |
| LEGAL3 | category | 6 | 38 | (RD 8600/613) 1; SEC 10-15-13 1; 206, 229 & 230, 241 & 242 1; NELY COR LOT 1 3.48 AC SE 1 |
| LEGAL4 | empty | 1 | 43 |  |
| LEGAL5 | empty | 1 | 43 |  |
| LOT | category | 13 | 12 | nan 17; 00001 4; 00050 1; 00008 1 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 43 |
| MAIL2 | category | 3 | 0 | . 32; REAL ESTATE DIVISION 8; PO BOX 27210 3 |
| MAIL3 | category | 7 | 0 | . 31; ATTN: PROPERTY MANAGMENT 5; TUCSON AZ 2; ATTN: PROPERTY MANAGEMENT 2 |
| MAIL4 | category | 3 | 33 | PO BOX 27210 8; . 2 |
| MAIL5 | category | 3 | 33 | TUCSON AZ 8; . 2 |
| MP | category | 29 | 0 | nan 13; 40058 2; 03043 2; 56057 1 |
| PAGE | amount | 26 | 0 | nan 15; 1017.0 2; 962.0 2; 0.0 2 |
| RECORDDATE | date | 25 | 0 | nan 18; 19770603 2; 19741024 1; 19721005 1 |
| DOCKET | category | 27 | 0 | nan 15; 5539 2; 0 2; 4879 1 |
| RECTRACT | empty | 2 | 43 |  |
| SECTMODIF | category | 2 | 16 | nan 27 |
| TAXAREA | category | 4 | 0 | 0150 31; 1250 9; 2050 2; 1050 1 |
| ZIP | category | 2 | 0 | 00000 32; 85726 11 |
| ZIP4 | category | 2 | 0 | 0000 32; 7210 11 |
| TAXYR | category | 2 | 0 | 2023 42; nan 1 |
| LIMNET | category | 2 | 0 | 0.0 42; nan 1 |
| FCV | amount | 31 | 0 | 500.0 12; 53000.0 2; 72000.0 1; 114000.0 1 |
| SHAPE_LENG | empty | 1 | 43 |  |
| ADDRESSEE | category | 4 | 0 | CITY OF TUCSON 35; CITY OF TUCSON
REAL ESTA 5; CITY OF TUCSON
REAL ESTA 2; CITY OF TUCSON
REAL ESTA 1 |
| ADDRESS | category | 2 | 0 | nan 32; PO BOX 27210 11 |
| CITY | category | 3 | 0 | nan 32; TUCSON 10; TUCSON  1 |
| STATE_PROVINCE | category | 2 | 0 | nan 32; AZ 11 |
| COUNTRY | empty | 1 | 43 |  |
| POSTAL_CODE | category | 2 | 0 | nan 32; 85726-7210 11 |
| SITE_ADDRESS | category | 8 | 0 | nan 36; 5901 S FIESTA AV 1; 6220 S HEADLEY RD 1; 5101 S NOGALES HY 1 |
| SITE_ZIP | category | 6 | 36 | 85706 2; 85705 2; 85746 1; 85730 1 |
| SITE_ZIPCITY | category | 2 | 36 | TUCSON 7 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     43 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      43 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             43 |
| DATASOURCE | who | 1 | 0 | PAREGION 43 |
| URL | category | 41 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | category | 42 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | category | 3 | 0 | NONE 35; ONE 7; MULTIPLE 1 |
| LEGAL_DESC | category | 42 | 0 | HACIENDA DEL ORO; DRAINAG 2; ARROYO VISTA RODEO WASH 1; AMHERST SOUTH RODEO WASH  1; VACATED LERDO RD IN NW4 N 1 |
| OWN | other | 1 | 0 | City 43 |
| VAN | who | 1 | 0 | not_van 43 |
| YEARBUILT | empty | 1 | 43 |  |
| LAST_EDITED_USER | category | 5 | 0 | GISPARFAB 36; u142832@CENTRAL 3; KChristensen2@CENTRAL 2; u116448@CENTRAL 1 |
| LAST_EDITED_DATE | date | 42 | 0 | 1603200631000 2; 1610391444000 1; 1610391414000 1; 1603152561000 1 |
| GLOBALID | category | 43 | 0 | b2acaacd-a641-4c5a-8f8c-d 1; 5694fcc8-60f2-4491-8880-5 1; c0e0dd58-0327-4cc8-95e7-f 1; 51bbce80-8f44-4c88-ba31-8 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 43 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 43 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 43 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 43 |
| SHAPE__AREA | amount | 43 | 0 | 14555.51953125 1; 31583.7109375 1; 9581.48828125 1; 5937.796875 1 |
| SHAPE__LENGTH | amount | 43 | 0 | 2398.526423393987 1; 3855.4743000597045 1; 1580.0853315093962 1; 599.132749416292 1 |
| GEOMETRY | category | 42 | 0 | {"type": "MultiPolygon",  1; {"type": "MultiPolygon",  1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:48:08.64767 43 |
| SOURCE_RUN_ID | audit | 1 | 0 | 18b1e922-89b6-4a3d-8c99-2 43 |
| SRC_SHA256 | who | 1 | 0 | a9a57f8f40232814bfac409e5 43 |
