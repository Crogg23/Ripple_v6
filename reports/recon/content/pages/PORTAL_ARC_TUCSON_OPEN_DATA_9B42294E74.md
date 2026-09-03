# PORTAL_ARC_TUCSON_OPEN_DATA_9B42294E74

rows 38  columns 34  scan 4.2s

roles: amount 5, audit 2, category 10, date 4, empty 9, who 5

## when

R_DATE
  1954         1  #####
  1980         1  #####
  1981         1  #####
  1982         1  #####
  1983         1  #####
  1984         6  ##############################
  1985         3  ###############
  1986         1  #####
  1987         4  ####################
  1988         1  #####
  1989         3  ###############
  1990         3  ###############
  1993         2  ##########
  1997         1  #####
  1998         1  #####
  1999         1  #####
  2001         1  #####
  2002         2  ##########
  2003         1  #####
  2004         1  #####
  2006         1  #####
  2009         1  #####

CREATIONDATE
  2025        38  ##############################

EDITDATE
  2025        38  ##############################

INGESTED_AT
  2026        38  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X_COORD | 38 | -112.87 | -111.03 | -110.84 | -110.84 | -4.2K |
| Y_COORD | 38 | 31.89 | 32.32 | 32.46 | 32.49 | 1.2K |
| AREA_SQFT | 38 | 8.8K | 133.4K | 9.58M | 10.06M | 34.66M |
| SHAPE__AREA | 38 | 8.8K | 133.4K | 9.58M | 10.06M | 34.66M |
| SHAPE__LENGTH | 38 | 398.32 | 1.9K | 17.6K | 19.0K | 137.3K |

## who

DATASOURCE by rows
        38  BASINPUB

DATASOURCE by dollars
       -4.2K       38 rows  BASINPUB

CREATOR by rows
        38  vberg2_cotgis

CREATOR by dollars
       -4.2K       38 rows  vberg2_cotgis

EDITOR by rows
        38  vberg2_cotgis

EDITOR by dollars
       -4.2K       38 rows  vberg2_cotgis

CLASSCODE by rows
        38  PUBLIC BASIN

CLASSCODE by dollars
       -4.2K       38 rows  PUBLIC BASIN

## who x when

DATASOURCE by R_DATE, dollars = X_COORD
  BASINPUB                                  1954:-110.93 1980:-111.06 1981:-111.03 1982:-111 1983:-111.05 1984:-666.22 1985:-332.92 1986:-111.02 1987:-444.15 1988:-111.05 1989:-332.92 1990:-332.95 1993:-222.05 1997:-111.10 1998:-111.21 1999:-110.84 2001:-110.91 2002:-222.21 2003:-111.14 2004:-111 2006:-112.87 2009:-110.95

CREATOR by R_DATE, dollars = X_COORD
  vberg2_cotgis                             1954:-110.93 1980:-111.06 1981:-111.03 1982:-111 1983:-111.05 1984:-666.22 1985:-332.92 1986:-111.02 1987:-444.15 1988:-111.05 1989:-332.92 1990:-332.95 1993:-222.05 1997:-111.10 1998:-111.21 1999:-110.84 2001:-110.91 2002:-222.21 2003:-111.14 2004:-111 2006:-112.87 2009:-110.95

## what

OBJECTID: 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%

GRANTOR: PIONEER TRUST COMPANY OF ARIZO 13%, I.C.M. MORTGAGE COMPANY 13%, FIRST AMERICAN TITLE INSURANCE 13%, US LIFE TITLE COMPANY OF AMERI 7%, TUCSON RETAIL 7%, TRANSAMERICA TITLE INSURANCE C 7%, TRANSAMERICA TITLE INSURANCE C 7%, TITLE INSURANCE COMPANY OF MIN 7%, TITLE GUARANTY AGENCY OF AZ, I 7%, TITLE GUARANTY AGENCY OF AZ IN 7%, TITLE GUARANTY AGENCY OF AZ IN 7%, TITLE GUARANTY AGENCY OF ARIZO 7%

GRANTEE: PC 79%, PCFCD 18%, PCPR 3%

DOCKET: nan 79%, 12894 3%, 07337 3%, 11474 3%, 11176 3%, 08554 3%, 00776 3%, 12218 3%, 10878 3%

PAGE: nan 79%, 04970 3%, 00706 3%, 01764 3%, 01495 3%, 00761 3%, 00416 3%, 00224 3%, 03200 3%

SUBBOOK: nan 24%, 37 9%, 38 9%, 39 9%, 43 9%, 33 6%, 36 6%, 40 6%, 41 6%, 56 6%, 42 6%, 65 3%

SUBPAGE: nan 32%, 17 8%, 57 8%, 55 8%, 51 8%, 72 8%, 49 8%, 2 4%, 58 4%, 84 4%, 7 4%, 81 4%

LEASE_NO: nan 97%, 016-086066 3%

MAINTAIN: nan 79%, PIMA COUNTY - RFCD 21%

GEOMETRY: {"type": "Polygon", "coordinat 8%, {"type": "MultiPolygon", "coor 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "MultiPolygon", "coor 8%, {"type": "MultiPolygon", "coor 8%, {"type": "MultiPolygon", "coor 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 38 | 0 | 38 1; 37 1; 36 1; 35 1 |
| BB_NO | empty | 1 | 38 |  |
| BR_NO | empty | 1 | 38 |  |
| LAYER | empty | 1 | 38 |  |
| BB_NO_1 | empty | 1 | 38 |  |
| BR_NO_1 | empty | 1 | 38 |  |
| GRANTOR | category | 35 | 0 | PIONEER TRUST COMPANY OF  2; I.C.M. MORTGAGE COMPANY 2; FIRST AMERICAN TITLE INSU 2; US LIFE TITLE COMPANY OF  1 |
| GRANTEE | category | 3 | 0 | PC 30; PCFCD 7; PCPR 1 |
| R_DATE | date | 37 | 0 | 04/24/1990 2; 09/23/1980 1; 12/18/2009 1; 08/31/1989 1 |
| DOCKET | category | 9 | 0 | nan 30; 12894 1; 07337 1; 11474 1 |
| PAGE | category | 9 | 0 | nan 30; 04970 1; 00706 1; 01764 1 |
| SUBDIVISIO | empty | 1 | 38 |  |
| SUBBOOK | category | 17 | 0 | nan 8; 37 3; 38 3; 39 3 |
| SUBPAGE | category | 25 | 0 | nan 8; 17 2; 57 2; 55 2 |
| CLASSCODE | who | 1 | 0 | PUBLIC BASIN 38 |
| LEASE_NO | category | 3 | 7 | nan 30; 016-086066 1 |
| REFERENCE | empty | 1 | 38 |  |
| EXP_DATE | empty | 1 | 38 |  |
| WIDTH | empty | 1 | 38 |  |
| X_COORD | amount | 38 | 0 | -111.06125048 1; -110.95028209 1; -111.00168157 1; -111.00256378 1 |
| Y_COORD | amount | 38 | 0 | 32.34569357 1; 32.18638367 1; 32.15237271 1; 32.1527149 1 |
| AREA_SQFT | amount | 38 | 0 | 692622.4937525 1; 1481651.27033797 1; 197812.48102866 1; 124780.05232716 1 |
| MAINTAIN | category | 2 | 0 | nan 30; PIMA COUNTY - RFCD 8 |
| DATASOURCE | who | 1 | 0 | BASINPUB 38 |
| CREATIONDATE | date | 1 | 0 | 1761695587858 38 |
| CREATOR | who | 1 | 0 | vberg2_cotgis 38 |
| EDITDATE | date | 1 | 0 | 1761695587858 38 |
| EDITOR | who | 1 | 0 | vberg2_cotgis 38 |
| SHAPE__AREA | amount | 38 | 0 | 692625.2642211914 1; 1481657.1970214844 1; 197813.27239990234 1; 124780.55151367188 1 |
| SHAPE__LENGTH | amount | 38 | 0 | 3461.6905887933863 1; 12058.613167758313 1; 2221.8767181232747 1; 1575.409848096071 1 |
| GEOMETRY | category | 38 | 0 | {"type": "Polygon", "coor 1; {"type": "MultiPolygon",  1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:47:21.28854 38 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6d0365b8-a470-4c3d-b7c4-d 38 |
| SRC_SHA256 | who | 1 | 0 | 1b2e8664b283447ed6ed9ab6e 38 |
