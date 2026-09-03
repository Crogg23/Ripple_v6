# PORTAL_ARC_WISCONSIN_OPEN_D_5206358BDD

rows 604  columns 45  scan 2.6s

roles: audit 2, category 5, date 2, empty 20, other 12, state 1, who 4

## when

LAST_EDITED_DATE
  2017       604  ##############################

INGESTED_AT
  2026       604  ##############################

## who

FACILITY_NAME by rows
         6  PRESENCE HOSPITALS PRV
         3  ADVOCATE HEALTH AND HOSPITALS CORP
         3  MERCY HOSPITAL
         3  THC-CHICAGO, INC.
         3  ST. MARY'S HOSPITAL
         2  WAUKEGAN ILLINOIS HOSPITAL COMPANY, LLC
         2  FRANCISCAN ALLIANCE, INC.
         2  COMMUNITY MEMORIAL HOSPITAL
         2  UHS OF HARTGROVE, INC.
         2  PRESENCE SAINTS MARY AND ELIZABETH
         2  RML HEALTH PROVIDERS LIMITED PARTNERSHIP
         2  MEMORIAL HOSPITAL
         2  ST. JOSEPH'S HOSPITAL
         1  MCLAREN MACOMB
         1  MCLAREN LAPEER REGION
         1  TAWAS ST JOSEPH HOSPITAL
         1  SANFORD BEMIDJI MEDICAL CENTER
         1  HENRY FORD MACOMB HOSPITAL
         1  STURGIS HOSPITAL
         1  COMMUNITY HEALTH CENTER OF BRANCH COUNTY

TYPE_DESC by rows
       604  HOSPITAL

COUNTY by rows
        69  COOK
        18  WAYNE
        12  OAKLAND
        12  HENNEPIN
         9  DUPAGE
         8  SAINT LOUIS
         8  LAKE
         7  MADISON
         7  POLK
         6  RAMSEY
         5  JACKSON
         5  STEARNS
         5  KANE
         4  SIOUX
         4  WASHTENAW
         4  WRIGHT
         4  MACOMB
         4  MC HENRY
         4  CALHOUN
         4  MARION

SRC_SHA256 by rows
       604  03ccd265749ab7c2e5dced4ddc691b49bd5213f917e4f206eab83c651fa1cce9

## who x when

FACILITY_NAME by LAST_EDITED_DATE
  ADVOCATE HEALTH AND HOSPITALS CORP        2017:3
  COMMUNITY HEALTH CENTER OF BRANCH COUNTY  2017:1
  COMMUNITY MEMORIAL HOSPITAL               2017:2
  FRANCISCAN ALLIANCE, INC.                 2017:2
  HENRY FORD MACOMB HOSPITAL                2017:1
  MCLAREN LAPEER REGION                     2017:1
  MCLAREN MACOMB                            2017:1
  MEMORIAL HOSPITAL                         2017:2
  MERCY HOSPITAL                            2017:3
  PRESENCE HOSPITALS PRV                    2017:6
  PRESENCE SAINTS MARY AND ELIZABETH        2017:2
  RML HEALTH PROVIDERS LIMITED PARTNERSHIP  2017:2
  SANFORD BEMIDJI MEDICAL CENTER            2017:1
  ST. JOSEPH'S HOSPITAL                     2017:2
  ST. MARY'S HOSPITAL                       2017:3
  STURGIS HOSPITAL                          2017:1
  TAWAS ST JOSEPH HOSPITAL                  2017:1
  THC-CHICAGO, INC.                         2017:3
  UHS OF HARTGROVE, INC.                    2017:2
  WAUKEGAN ILLINOIS HOSPITAL COMPANY, LLC   2017:2

TYPE_DESC by LAST_EDITED_DATE
  HOSPITAL                                  2017:604

## where

STATE: IL 214, MI 136, MN 136, IA 118

## what

ADDRESS_2: nan 98%, P. O. BOX 372 0%, P.O. BOX 850 0%, 200 BERTEAU AVENUE 0%, (M/C 693) 0%, MC1112 0%, P. O. BOX 297 0%, 129 NORTH EIGHTH STREET 0%, P.O. BOX 747 0%, P.O. BOX 267 0%, 7TH STREET CAMPUS 0%, P. O. BOX 530 0%

SUB_TYPE_DESC: nan 66%, GENERAL HOSPITAL 27%, CRITICAL ACCESS HOSP 5%, PSYCH. HOSPITAL 1%, REHABILITATION HOSP 1%, PEDIATRIC HOSPITAL 0%, CHILDRENS 0%

FED_TYPE_DESC: nan 58%, Acute Care Hospitals 21%, Critical Access Hospitals 19%, ACUTE CARE - VETERANS ADMINIST 1%, Critical Access Hospital 0%, Childrens 0%

STATE_FIPS: 17 35%, 26 23%, 27 23%, 19 20%

WCRS_ID: nan 100%, 0000004408 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 589 | 0 | 769 4; 768 4; 767 4; 766 4 |
| NAME | empty | 1 | 604 |  |
| FACILITY_NAME | who | 589 | 0 | PRESENCE HOSPITALS PRV 8; ADVOCATE HEALTH AND HOSPI 4; ST. MARY'S HOSPITAL 4; FRANCISCAN ALLIANCE, INC. 4 |
| LABEL | other | 587 | 0 | PRESENCE HOSPITALS PRV 8; ADVOCATE HEALTH AND HOSPI 4; ST. MARY'S HOSPITAL 4; FRANCISCAN ALLIANCE, INC. 4 |
| ADDRESS | other | 604 | 0 | 118 NORTH 7TH AVENUE 4; 920 SOUTH OAK STREET 4; 1229 C AVENUE EAST 4; 1111 3RD STREET SW 4 |
| ADDRESS_2 | category | 16 | 0 | nan 589; P. O. BOX 372 1; P.O. BOX 850 1; 200 BERTEAU AVENUE 1 |
| CITY | other | 469 | 0 | CHICAGO 40; DETROIT 8; DES MOINES 6; MINNEAPOLIS 6 |
| STATE | state | 4 | 0 | IL 214; MI 136; MN 136; IA 118 |
| ZIP | other | 554 | 0 | 48201 5; 52001 4; 50314 4; 51503 4 |
| ZIP_4 | empty | 1 | 604 |  |
| TYPE_DESC | who | 1 | 0 | HOSPITAL 604 |
| SUB_TYPE_DESC | category | 7 | 0 | nan 396; GENERAL HOSPITAL 164; CRITICAL ACCESS HOSP 28; PSYCH. HOSPITAL 8 |
| FED_TYPE_DESC | category | 6 | 0 | nan 350; Acute Care Hospitals 129; Critical Access Hospitals 116; ACUTE CARE - VETERANS ADM 7 |
| WI_LICENSE_NUM | empty | 1 | 604 |  |
| STATE_FIPS | category | 4 | 0 | 17 214; 26 136; 27 136; 19 118 |
| COUNTY | who | 274 | 0 | COOK 69; WAYNE 18; OAKLAND 12; HENNEPIN 12 |
| COUNTY_FIPS | other | 102 | 0 | 31 69; 185 18; 125 15; 53 15 |
| LAT | other | 604 | 0 | 43.186912 4; 42.506702 4; 41.298557 4; 42.476052 4 |
| LON | other | 606 | 0 | -95.846246 4; -93.262374 4; -92.630641 4; -91.130638 4 |
| USNG | other | 600 | 0 | 15TTH6870585504 4; 15TVH7844406070 4; 15TWF3092371966 4; 15TXH5365904326 4 |
| GIS_ID | other | 616 | 0 | IAHosp_0093 4; IAHosp_0092 4; IAHosp_0091 4; IAHosp_0090 4 |
| ASPEN_FACILITY_ID | empty | 1 | 604 |  |
| FACILITY_INTERNAL_ID | empty | 1 | 604 |  |
| MEDICARE_ID | other | 252 | 0 | nan 356; 161381 2; 161380 2; 161379 2 |
| MEDICAID_ID | empty | 1 | 604 |  |
| HSIP_ID | empty | 1 | 604 |  |
| NPI_ID | empty | 1 | 604 |  |
| AHA_ID | empty | 1 | 604 |  |
| TYPE_CODE | empty | 1 | 604 |  |
| FACILITY_TYPE_CODE | empty | 1 | 604 |  |
| WCRS_ID | category | 2 | 0 | nan 603; 0000004408 1 |
| PHONE_NUMBER | empty | 1 | 604 |  |
| BED_COUNT | empty | 1 | 604 |  |
| TRAUMA | empty | 1 | 604 |  |
| TRAUMA_CLASS | empty | 1 | 604 |  |
| HCC_REGION | empty | 1 | 604 |  |
| WITRAC_NAME | empty | 1 | 604 |  |
| EMRESOURCE_ID | empty | 1 | 604 |  |
| URL | empty | 1 | 604 |  |
| LAST_EDITED_DATE | date | 1 | 0 | 1507210747000 604 |
| TRAUMA_CLASS_TEXT | empty | 1 | 604 |  |
| GEOMETRY | other | 614 | 0 | {"type": "Point", "coordi 4; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:33:25.51790 604 |
| SOURCE_RUN_ID | audit | 1 | 0 | f1b04b7c-8cf2-4f5a-81f4-4 604 |
| SRC_SHA256 | who | 1 | 0 | 03ccd265749ab7c2e5dced4dd 604 |
