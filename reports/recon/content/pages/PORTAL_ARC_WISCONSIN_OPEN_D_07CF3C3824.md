# PORTAL_ARC_WISCONSIN_OPEN_D_07CF3C3824

rows 2  columns 45  scan 4.0s

roles: audit 2, category 32, date 2, empty 2, other 6, who 2

## when

LAST_EDITED_DATE
  2017         2  ##############################

INGESTED_AT
  2026         2  ##############################

## who

TYPE_DESC by rows
         2  HOSPITAL

SRC_SHA256 by rows
         2  b2a6285b65d1c287c8a8df70bb5e1ca9cd885e2081a0cff2a73a9a62227f92d1

## who x when

TYPE_DESC by LAST_EDITED_DATE
  HOSPITAL                                  2017:2

SRC_SHA256 by LAST_EDITED_DATE
  b2a6285b65d1c287c8a8df70bb5e1ca9cd885e20  2017:2

## what

OBJECTID: 151 50%, 86 50%

NAME: CHILDREN'S HOSPITAL OF WISCONS 50%, UNIVERSITY HOSPITAL 50%

FACILITY_NAME: CHILDRENS HOSPITAL OF WISCONSI 50%, UNIVERSITY OF WI HOSPITALS & C 50%

LABEL: CHILDRENS HOSPITAL OF WISCONSI 50%, U.W. HOSPITAL 50%

ADDRESS: 9000 W WISCONSIN AVE 50%, 600 HIGHLAND AVENUE 50%

CITY: MILWAUKEE 50%, MADISON 50%

ZIP: 53226 50%, 53792 50%

SUB_TYPE_DESC: CHILDRENS 50%, SHORT TERM 50%

FED_TYPE_DESC: nan 50%, ACUTE CARE HOSPITALS 50%

WI_LICENSE_NUM: 135 50%, 125 50%

COUNTY: MILWAUKEE 50%, DANE 50%

COUNTY_FIPS: 79 50%, 25 50%

LAT: 43.042252 50%, 43.076378 50%

LON: -88.023442 50%, -89.431784 50%

USNG: 16TDN1663766015 50%, 16TCN0203072166 50%

GIS_ID: WIHosp_0140 50%, WIHosp_0081 50%

ASPEN_FACILITY_ID: HSPLACU19 50%, HSPLACU127 50%

FACILITY_INTERNAL_ID: 6054 50%, 6149 50%

MEDICARE_ID: nan 50%, 520098 50%

MEDICAID_ID: nan 50%, 11022000 50%

HSIP_ID: 111553226 50%, 113853792 50%

NPI_ID: <Null> 50%, nan 50%

AHA_ID: 6451030 50%, 6450820 50%

FACILITY_TYPE_CODE: 16 50%, 11 50%

WCRS_ID: 0000004019 50%, 0000001304 50%

PHONE_NUMBER: 4142662000 50%, 6082638991 50%

BED_COUNT: 306 50%, 648 50%

HCC_REGION: 7 50%, 5 50%

WITRAC_NAME: Children's Hospital of WI - Mi 50%, University of Wisconsin Hospit 50%

EMRESOURCE_ID: 90801 50%, 90770 50%

URL: http://www.chw.org/location-di 50%, http://www.uwhealth.org/locati 50%

GEOMETRY: {"type": "Point", "coordinates 50%, {"type": "Point", "coordinates 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 151 1; 86 1 |
| NAME | category | 2 | 0 | CHILDREN'S HOSPITAL OF WI 1; UNIVERSITY HOSPITAL 1 |
| FACILITY_NAME | category | 2 | 0 | CHILDRENS HOSPITAL OF WIS 1; UNIVERSITY OF WI HOSPITAL 1 |
| LABEL | category | 2 | 0 | CHILDRENS HOSPITAL OF WIS 1; U.W. HOSPITAL 1 |
| ADDRESS | category | 2 | 0 | 9000 W WISCONSIN AVE 1; 600 HIGHLAND AVENUE 1 |
| ADDRESS_2 | empty | 1 | 2 |  |
| CITY | category | 2 | 0 | MILWAUKEE 1; MADISON 1 |
| STATE | other | 1 | 0 | WI 2 |
| ZIP | category | 2 | 0 | 53226 1; 53792 1 |
| ZIP_4 | empty | 1 | 2 |  |
| TYPE_DESC | who | 1 | 0 | HOSPITAL 2 |
| SUB_TYPE_DESC | category | 2 | 0 | CHILDRENS 1; SHORT TERM 1 |
| FED_TYPE_DESC | category | 2 | 0 | nan 1; ACUTE CARE HOSPITALS 1 |
| WI_LICENSE_NUM | category | 2 | 0 | 135 1; 125 1 |
| STATE_FIPS | other | 1 | 0 | 55 2 |
| COUNTY | category | 2 | 0 | MILWAUKEE 1; DANE 1 |
| COUNTY_FIPS | category | 2 | 0 | 79 1; 25 1 |
| LAT | category | 2 | 0 | 43.042252 1; 43.076378 1 |
| LON | category | 2 | 0 | -88.023442 1; -89.431784 1 |
| USNG | category | 2 | 0 | 16TDN1663766015 1; 16TCN0203072166 1 |
| GIS_ID | category | 2 | 0 | WIHosp_0140 1; WIHosp_0081 1 |
| ASPEN_FACILITY_ID | category | 2 | 0 | HSPLACU19 1; HSPLACU127 1 |
| FACILITY_INTERNAL_ID | category | 2 | 0 | 6054 1; 6149 1 |
| MEDICARE_ID | category | 2 | 0 | nan 1; 520098 1 |
| MEDICAID_ID | category | 2 | 0 | nan 1; 11022000 1 |
| HSIP_ID | category | 2 | 0 | 111553226 1; 113853792 1 |
| NPI_ID | category | 2 | 0 | <Null> 1; nan 1 |
| AHA_ID | category | 2 | 0 | 6451030 1; 6450820 1 |
| TYPE_CODE | other | 1 | 0 | 1 2 |
| FACILITY_TYPE_CODE | category | 2 | 0 | 16 1; 11 1 |
| WCRS_ID | category | 2 | 0 | 0000004019 1; 0000001304 1 |
| PHONE_NUMBER | category | 2 | 0 | 4142662000 1; 6082638991 1 |
| BED_COUNT | category | 2 | 0 | 306 1; 648 1 |
| TRAUMA | other | 1 | 0 | TRUE 2 |
| TRAUMA_CLASS | other | 1 | 0 | 1 2 |
| HCC_REGION | category | 2 | 0 | 7 1; 5 1 |
| WITRAC_NAME | category | 2 | 0 | Children's Hospital of WI 1; University of Wisconsin H 1 |
| EMRESOURCE_ID | category | 2 | 0 | 90801 1; 90770 1 |
| URL | category | 2 | 0 | http://www.chw.org/locati 1; http://www.uwhealth.org/l 1 |
| LAST_EDITED_DATE | date | 1 | 0 | 1507210747000 2 |
| TRAUMA_CLASS_TEXT | other | 1 | 0 | 1 2 |
| GEOMETRY | category | 2 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:30:07.94295 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | e7ee1bd0-4e70-479e-8540-3 2 |
| SRC_SHA256 | who | 1 | 0 | b2a6285b65d1c287c8a8df70b 2 |
