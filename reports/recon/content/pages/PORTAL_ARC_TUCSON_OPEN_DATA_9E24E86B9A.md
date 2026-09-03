# PORTAL_ARC_TUCSON_OPEN_DATA_9E24E86B9A

rows 2  columns 78  scan 4.8s

roles: amount 7, audit 2, category 38, date 5, empty 8, other 8, who 11

## when

LASTCHANGE
  2005         1  ##############################
  2023         1  ##############################

LAST_EDITED_DATE
  2020         1  ##############################
  2023         1  ##############################

CREATED_DATE_COT
  2023         2  ##############################

LAST_EDITED_DATE_COT
  2023         2  ##############################

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| GISAREA | 2 | 73.7K | 290.6K | 503.3K | 507.6K | 581.3K |
| GISACRES | 2 | 1.69 | 6.67 | 11.55 | 11.65 | 13.34 |
| X_HPGN | 2 | 973.8K | 981.3K | 988.7K | 988.8K | 1.96M |
| Y_HPGN | 2 | 445.8K | 446.0K | 446.1K | 446.1K | 891.9K |
| LANDMEAS | 2 | 0.10 | 20.3K | 40.1K | 40.5K | 40.5K |
| SHAPE__AREA | 2 | 9.6K | 37.8K | 65.5K | 66.1K | 75.7K |

## who

JURIS_OL by rows
         2  TUCSON

JURIS_OL by dollars
      581.3K        2 rows  TUCSON

MAIL1 by rows
         2  CITY OF TUCSON

MAIL1 by dollars
      581.3K        2 rows  CITY OF TUCSON

USE_DESC by rows
         2  MUNICIPAL VACANT LAND                       

USE_DESC by dollars
      581.3K        2 rows  MUNICIPAL VACANT LAND                       

SPT_DESC by rows
         2  MISC REL/GVT/IN     

SPT_DESC by dollars
      581.3K        2 rows  MISC REL/GVT/IN     

## who x when

JURIS_OL by LAST_EDITED_DATE, dollars = GISAREA
  TUCSON                                    2020:507.6K 2023:73.7K

MAIL1 by LAST_EDITED_DATE, dollars = GISAREA
  CITY OF TUCSON                            2020:507.6K 2023:73.7K

## what

OBJECTID: 2 50%, 1 50%

PARCEL: 11619222A 50%, 116112820 50%

LON: -110.98262282 50%, -111.03126817 50%

LAT: 32.22213056 50%, 32.2234235 50%

LOT_R: nan 100%

LINK: HTTPS://GIS.PIMA.GOV/D.HTM?P=1 50%, HTTPS://GIS.PIMA.GOV/D.HTM?P=1 50%

TRS_OL: 141311E 50%, 141308E 50%

MP_OL: 36017 50%, 52063 50%

SEQ_NUM_S: 19991480300 100%

ADDRESS_OL: 660 W ALAMEDA ST 50%, 2901 W ANKLAM RD 50%

SEQ_NUM_D: 0.0 50%, nan 50%

LANDUNIT: F 50%, S 50%

LEGAL1: WLY PTN RIO NUEVO NORTH BLK I 50%, DESERT STAR DRAINAGE 50%

LOT: nan 100%

MAIL2: REAL ESTATE DIVISION 50%, . 50%

MAIL3: ATTN: PROPERTY MANAGEMENT 50%, . 50%

MAIL4: PO BOX 27210 100%

MAIL5: TUCSON AZ 100%

MP: 36017 50%, 52063 50%

PAGE: 944.0 50%, nan 50%

RECORDDATE: 19800813 50%, nan 50%

DOCKET: 6342 50%, nan 50%

SECTMODIF: nan 100%

ZIP: 85726 50%, 00000 50%

ZIP4: 7210 50%, 0000 50%

FCV: 82306 50%, 500 50%

ADDRESSEE: CITY OF TUCSON
REAL ESTATE DI 50%, CITY OF TUCSON 50%

ADDRESS: PO BOX 27210 50%, nan 50%

CITY: TUCSON 50%, nan 50%

STATE_PROVINCE: AZ 50%, nan 50%

POSTAL_CODE: 85726-7210 50%, nan 50%

SITE_ADDRESS: 660 W ALAMEDA ST 50%, 2901 W ANKLAM RD 50%

URL: https://pro.tucsonaz.gov/parce 50%, https://pro.tucsonaz.gov/parce 50%

URL2: http://gis.pima.gov/maps/detai 50%, http://gis.pima.gov/maps/detai 50%

LEGAL_DESC: WLY PTN RIO NUEVO NORTH BLK I 50%, DESERT STAR DRAINAGE 50%

LAST_EDITED_USER: KChristensen2@CENTRAL 50%, GISPARFAB 50%

GLOBALID: 5e5c06ed-ad3e-47d0-826b-015b00 50%, 9ee5e63a-16ec-495e-8777-6269c2 50%

GEOMETRY: {"type": "Polygon", "coordinat 50%, {"type": "MultiPolygon", "coor 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 2 1; 1 1 |
| PARCEL | category | 2 | 0 | 11619222A 1; 116112820 1 |
| GISAREA | amount | 2 | 0 | 73652.72486412 1; 507629.36193241 1 |
| GISACRES | amount | 2 | 0 | 1.69077195 1; 11.65313963 1 |
| X_HPGN | amount | 2 | 0 | 988845.72818034 1; 973798.12611525 1 |
| Y_HPGN | amount | 2 | 0 | 445797.25795069 1; 446140.2395775 1 |
| LON | category | 2 | 0 | -110.98262282 1; -111.03126817 1 |
| LAT | category | 2 | 0 | 32.22213056 1; 32.2234235 1 |
| LOT_R | category | 2 | 1 | nan 1 |
| LINK | category | 2 | 0 | HTTPS://GIS.PIMA.GOV/D.HT 1; HTTPS://GIS.PIMA.GOV/D.HT 1 |
| TRS_OL | category | 2 | 0 | 141311E 1; 141308E 1 |
| MP_OL | category | 2 | 0 | 36017 1; 52063 1 |
| SEQ_NUM_S | category | 2 | 1 | 19991480300 1 |
| JURIS_OL | who | 1 | 0 | TUCSON 2 |
| CURZONE_OL | other | 1 | 0 | O-3 2 |
| ADDRESS_OL | category | 2 | 0 | 660 W ALAMEDA ST 1; 2901 W ANKLAM RD 1 |
| SEQ_NUM_D | category | 2 | 0 | 0.0 1; nan 1 |
| PARCEL_USE | other | 1 | 0 | 9700 2 |
| LANDMEAS | amount | 2 | 0 | 40545.0 1; 0.1 1 |
| LANDUNIT | category | 2 | 0 | F 1; S 1 |
| LASTCHANGE | date | 2 | 0 | 1677673409000 1; 1121126400000 1 |
| LEGAL1 | category | 2 | 0 | WLY PTN RIO NUEVO NORTH B 1; DESERT STAR DRAINAGE 1 |
| LEGAL2 | empty | 1 | 2 |  |
| LEGAL3 | empty | 1 | 2 |  |
| LEGAL4 | empty | 1 | 2 |  |
| LEGAL5 | empty | 1 | 2 |  |
| LOT | category | 2 | 1 | nan 1 |
| MAIL1 | who | 1 | 0 | CITY OF TUCSON 2 |
| MAIL2 | category | 2 | 0 | REAL ESTATE DIVISION 1; . 1 |
| MAIL3 | category | 2 | 0 | ATTN: PROPERTY MANAGEMENT 1; . 1 |
| MAIL4 | category | 2 | 1 | PO BOX 27210 1 |
| MAIL5 | category | 2 | 1 | TUCSON AZ 1 |
| MP | category | 2 | 0 | 36017 1; 52063 1 |
| PAGE | category | 2 | 0 | 944.0 1; nan 1 |
| RECORDDATE | category | 2 | 0 | 19800813 1; nan 1 |
| DOCKET | category | 2 | 0 | 6342 1; nan 1 |
| RECTRACT | empty | 1 | 2 |  |
| SECTMODIF | category | 2 | 1 | nan 1 |
| TAXAREA | other | 1 | 0 | 0150 2 |
| ZIP | category | 2 | 0 | 85726 1; 00000 1 |
| ZIP4 | category | 2 | 0 | 7210 1; 0000 1 |
| TAXYR | other | 1 | 0 | 2023 2 |
| LIMNET | other | 1 | 0 | 0 2 |
| FCV | category | 2 | 0 | 82306 1; 500 1 |
| SHAPE_LENG | empty | 1 | 2 |  |
| ADDRESSEE | category | 2 | 0 | CITY OF TUCSON
REAL ESTA 1; CITY OF TUCSON 1 |
| ADDRESS | category | 2 | 0 | PO BOX 27210 1; nan 1 |
| CITY | category | 2 | 0 | TUCSON 1; nan 1 |
| STATE_PROVINCE | category | 2 | 0 | AZ 1; nan 1 |
| COUNTRY | empty | 1 | 2 |  |
| POSTAL_CODE | category | 2 | 0 | 85726-7210 1; nan 1 |
| SITE_ADDRESS | category | 2 | 0 | 660 W ALAMEDA ST 1; 2901 W ANKLAM RD 1 |
| SITE_ZIP | other | 1 | 0 | 85745 2 |
| SITE_ZIPCITY | who | 1 | 0 | TUCSON 2 |
| USE_DESC | who | 1 | 0 | MUNICIPAL VACANT LAND     2 |
| SPT_DESC | who | 1 | 0 | MISC REL/GVT/IN      2 |
| PPT_DESC | who | 1 | 0 | Miscellaneous             2 |
| DATASOURCE | who | 1 | 0 | PAREGION 2 |
| URL | category | 2 | 0 | https://pro.tucsonaz.gov/ 1; https://pro.tucsonaz.gov/ 1 |
| URL2 | category | 2 | 0 | http://gis.pima.gov/maps/ 1; http://gis.pima.gov/maps/ 1 |
| ADR_STATUS | other | 1 | 0 | ONE 2 |
| LEGAL_DESC | category | 2 | 0 | WLY PTN RIO NUEVO NORTH B 1; DESERT STAR DRAINAGE 1 |
| OWN | other | 1 | 0 | City 2 |
| VAN | who | 1 | 0 | not_van 2 |
| YEARBUILT | empty | 1 | 2 |  |
| LAST_EDITED_USER | category | 2 | 0 | KChristensen2@CENTRAL 1; GISPARFAB 1 |
| LAST_EDITED_DATE | date | 2 | 0 | 1679515111000 1; 1603158602000 1 |
| GLOBALID | category | 2 | 0 | 5e5c06ed-ad3e-47d0-826b-0 1; 9ee5e63a-16ec-495e-8777-6 1 |
| CREATED_USER_COT | who | 1 | 0 | GISDATA 2 |
| CREATED_DATE_COT | date | 1 | 0 | 1697082847000 2 |
| LAST_EDITED_USER_COT | who | 1 | 0 | GISDATA 2 |
| LAST_EDITED_DATE_COT | date | 1 | 0 | 1697082847000 2 |
| SHAPE__AREA | amount | 2 | 0 | 9585.04296875 1; 66089.98046875 1 |
| SHAPE__LENGTH | amount | 2 | 0 | 605.8404524504465 1; 2205.252482061971 1 |
| GEOMETRY | category | 2 | 0 | {"type": "Polygon", "coor 1; {"type": "MultiPolygon",  1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:46:13.64270 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | 080ba39c-4009-4269-9fd4-0 2 |
| SRC_SHA256 | who | 1 | 0 | f87905583e7ccb09fc5963377 2 |
