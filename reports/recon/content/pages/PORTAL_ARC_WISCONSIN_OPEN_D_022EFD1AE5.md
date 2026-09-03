# PORTAL_ARC_WISCONSIN_OPEN_D_022EFD1AE5

rows 2  columns 45  scan 3.2s

roles: audit 2, category 28, date 2, empty 3, other 7, who 4

## when

LAST_EDITED_DATE
  2017         2  ##############################

INGESTED_AT
  2026         2  ##############################

## who

TYPE_DESC by rows
         2  HOSPITAL

SUB_TYPE_DESC by rows
         2  SHORT TERM

FED_TYPE_DESC by rows
         2  ACUTE CARE HOSPITALS

SRC_SHA256 by rows
         2  4935e95acfb7a39e5727ad6e839de2d2a122026683e786e88480d3164d5905f7

## who x when

TYPE_DESC by LAST_EDITED_DATE
  HOSPITAL                                  2017:2

SUB_TYPE_DESC by LAST_EDITED_DATE
  SHORT TERM                                2017:2

## what

OBJECTID: 124 50%, 86 50%

NAME: FROEDTERT HOSPITAL 50%, UNIVERSITY HOSPITAL 50%

FACILITY_NAME: FROEDTERT MEMORIAL LUTHERAN HS 50%, UNIVERSITY OF WI HOSPITALS & C 50%

LABEL: MEMORIAL LUTHERAN 50%, U.W. HOSPITAL 50%

ADDRESS: 9200 W WISCONSIN AVE 50%, 600 HIGHLAND AVENUE 50%

CITY: MILWAUKEE 50%, MADISON 50%

ZIP: 53226 50%, 53792 50%

WI_LICENSE_NUM: 232 50%, 125 50%

COUNTY: MILWAUKEE 50%, DANE 50%

COUNTY_FIPS: 79 50%, 25 50%

LAT: 43.040833 50%, 43.076378 50%

LON: -88.024544 50%, -89.431784 50%

USNG: 16TDN1654665858 50%, 16TCN0203072166 50%

GIS_ID: WIHosp_0058 50%, WIHosp_0081 50%

ASPEN_FACILITY_ID: HSPLACU35 50%, HSPLACU127 50%

FACILITY_INTERNAL_ID: 6013 50%, 6149 50%

MEDICARE_ID: 520177 50%, 520098 50%

MEDICAID_ID: 11000400 50%, 11022000 50%

HSIP_ID: 110553226 50%, 113853792 50%

AHA_ID: 6452115 50%, 6450820 50%

WCRS_ID: nan 50%, 0000001304 50%

PHONE_NUMBER: 4148053000 50%, 6082638991 50%

BED_COUNT: 596 50%, 648 50%

HCC_REGION: 7 50%, 5 50%

WITRAC_NAME: Froedtert Hospital - Froedtert 50%, University of Wisconsin Hospit 50%

EMRESOURCE_ID: 90806 50%, 90770 50%

URL: http://www.froedtert.com/froed 50%, http://www.uwhealth.org/locati 50%

GEOMETRY: {"type": "Point", "coordinates 50%, {"type": "Point", "coordinates 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 2 | 0 | 124 1; 86 1 |
| NAME | category | 2 | 0 | FROEDTERT HOSPITAL 1; UNIVERSITY HOSPITAL 1 |
| FACILITY_NAME | category | 2 | 0 | FROEDTERT MEMORIAL LUTHER 1; UNIVERSITY OF WI HOSPITAL 1 |
| LABEL | category | 2 | 0 | MEMORIAL LUTHERAN 1; U.W. HOSPITAL 1 |
| ADDRESS | category | 2 | 0 | 9200 W WISCONSIN AVE 1; 600 HIGHLAND AVENUE 1 |
| ADDRESS_2 | empty | 1 | 2 |  |
| CITY | category | 2 | 0 | MILWAUKEE 1; MADISON 1 |
| STATE | other | 1 | 0 | WI 2 |
| ZIP | category | 2 | 0 | 53226 1; 53792 1 |
| ZIP_4 | empty | 1 | 2 |  |
| TYPE_DESC | who | 1 | 0 | HOSPITAL 2 |
| SUB_TYPE_DESC | who | 1 | 0 | SHORT TERM 2 |
| FED_TYPE_DESC | who | 1 | 0 | ACUTE CARE HOSPITALS 2 |
| WI_LICENSE_NUM | category | 2 | 0 | 232 1; 125 1 |
| STATE_FIPS | other | 1 | 0 | 55 2 |
| COUNTY | category | 2 | 0 | MILWAUKEE 1; DANE 1 |
| COUNTY_FIPS | category | 2 | 0 | 79 1; 25 1 |
| LAT | category | 2 | 0 | 43.040833 1; 43.076378 1 |
| LON | category | 2 | 0 | -88.024544 1; -89.431784 1 |
| USNG | category | 2 | 0 | 16TDN1654665858 1; 16TCN0203072166 1 |
| GIS_ID | category | 2 | 0 | WIHosp_0058 1; WIHosp_0081 1 |
| ASPEN_FACILITY_ID | category | 2 | 0 | HSPLACU35 1; HSPLACU127 1 |
| FACILITY_INTERNAL_ID | category | 2 | 0 | 6013 1; 6149 1 |
| MEDICARE_ID | category | 2 | 0 | 520177 1; 520098 1 |
| MEDICAID_ID | category | 2 | 0 | 11000400 1; 11022000 1 |
| HSIP_ID | category | 2 | 0 | 110553226 1; 113853792 1 |
| NPI_ID | empty | 1 | 2 |  |
| AHA_ID | category | 2 | 0 | 6452115 1; 6450820 1 |
| TYPE_CODE | other | 1 | 0 | 1 2 |
| FACILITY_TYPE_CODE | other | 1 | 0 | 11 2 |
| WCRS_ID | category | 2 | 0 | nan 1; 0000001304 1 |
| PHONE_NUMBER | category | 2 | 0 | 4148053000 1; 6082638991 1 |
| BED_COUNT | category | 2 | 0 | 596 1; 648 1 |
| TRAUMA | other | 1 | 0 | TRUE 2 |
| TRAUMA_CLASS | other | 1 | 0 | 1 2 |
| HCC_REGION | category | 2 | 0 | 7 1; 5 1 |
| WITRAC_NAME | category | 2 | 0 | Froedtert Hospital - Froe 1; University of Wisconsin H 1 |
| EMRESOURCE_ID | category | 2 | 0 | 90806 1; 90770 1 |
| URL | category | 2 | 0 | http://www.froedtert.com/ 1; http://www.uwhealth.org/l 1 |
| LAST_EDITED_DATE | date | 1 | 0 | 1507210747000 2 |
| TRAUMA_CLASS_TEXT | other | 1 | 0 | 1 2 |
| GEOMETRY | category | 2 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:30:26.02550 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | 44570456-415c-4bd2-9a5b-4 2 |
| SRC_SHA256 | who | 1 | 0 | 4935e95acfb7a39e5727ad6e8 2 |
