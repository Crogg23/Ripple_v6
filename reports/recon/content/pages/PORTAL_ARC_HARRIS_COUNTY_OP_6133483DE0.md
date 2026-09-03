# PORTAL_ARC_HARRIS_COUNTY_OP_6133483DE0

rows 67  columns 126  scan 5.5s

roles: amount 4, audit 2, category 26, date 1, empty 84, other 7, who 3

## when

INGESTED_AT
  2026        67  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 67 | -95.82 | -95.47 | 0 | 0 | -5.9K |
| Y | 67 | 0 | 29.83 | 30 | 30 | 1.8K |
| DISPLAYX | 67 | -95.82 | 0 | 0 | 0 | -574.92 |
| DISPLAYY | 67 | 0 | 0 | 29.79 | 29.79 | 178.74 |

## who

USER_M_F by rows
        67  <Null>

USER_M_F by dollars
       -5.9K       67 rows  <Null>

USER_INSURANCE by rows
        67  Uninsured, All Insurance

USER_INSURANCE by dollars
       -5.9K       67 rows  Uninsured, All Insurance

SRC_SHA256 by rows
        67  0bca9168ba6cb98632220ffe6be07a8f551834b01976379b344b28bb7c4b8083

SRC_SHA256 by dollars
       -5.9K       67 rows  0bca9168ba6cb98632220ffe6be07a8f551834b01976379b344b28bb7c4b

## who x when

USER_M_F by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  <Null>                                    2026:-5.9K

USER_INSURANCE by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Uninsured, All Insurance                  2026:-5.9K

## what

LOC_NAME: HGAC_Address_P 90%, HGAC_StarMap_R 10%

SCORE: 100 93%, 0 7%

MATCH_ADDR: 5502 FIRST ST, KATY, TX, 77493 10%, 7777 WESTGREEN BLVD, CYPRESS,  10%, 15555 KUYKENDAHL RD, HOUSTON,  10%, 8575 PITNER RD, HOUSTON, TX, 7 10%, 19333 CLAY RD, KATY, TX, 77449 10%, 3737 RED BLUFF RD, PASADENA, T 10%, 8540 C E KING PKWY, HOUSTON, T 10%, 5815 ANTOINE DR, HOUSTON, TX,  10%, 7340 SPENCER HWY, PASADENA, TX 8%, 6400 BISSONNET ST, HOUSTON, TX 8%, 9401 SOUTHWEST FWY, HOUSTON, T 6%

ADDR_TYPE: PointAddress 90%, StreetAddress 10%

ADDNUM: 5502 10%, 7777 10%, 15555 10%, 8575 10%, 19333 10%, 3737 10%, 8540 10%, 5815 10%, 7340 8%, 6400 8%, 9401 6%

SIDE: R 100%

STNAME: FIRST 10%, WESTGREEN 10%, KUYKENDAHL 10%, PITNER 10%, CLAY 10%, RED BLUFF 10%, C E KING 10%, ANTOINE 10%, SPENCER 8%, BISSONNET 8%, SOUTHWEST 6%

STTYPE: RD 39%, ST 18%, BLVD 10%, PKWY 10%, DR 10%, HWY 8%, FWY 6%

STADDR: 5502 FIRST ST 10%, 7777 WESTGREEN BLVD 10%, 15555 KUYKENDAHL RD 10%, 8575 PITNER RD 10%, 19333 CLAY RD 10%, 3737 RED BLUFF RD 10%, 8540 C E KING PKWY 10%, 5815 ANTOINE DR 10%, 7340 SPENCER HWY 8%, 6400 BISSONNET ST 8%, 9401 SOUTHWEST FWY 6%

CITY: HOUSTON 53%, KATY 19%, PASADENA 18%, CYPRESS 10%

COUNTY: HARRIS COUNTY 100%

STATE: TX 100%

STATEABBR: TX 100%

ZIP: 77074 15%, 77493 10%, 77433 10%, 77090 10%, 77080 10%, 77449 10%, 77503 10%, 77044 10%, 77091 10%, 77505 8%

ADDNUMFROM: 5500 100%

ADDNUMTO: 5570 100%

COUNTRY: USA 100%

STATUS: M 84%, T 9%, U 7%

IN_SINGLELINE: 5502 1st St, Katy, TX 77493 9%, 7777 Westgreen Blvd, Cypress,  9%, 15555 Kuykendahl Rd. Ste #319, 9%, 8575 Pitner Rd, Houston, TX 77 9%, 19333 Clay Road, Katy, TX 7744 9%, 3737 Red Bluff Rd, Pasadena, T 9%, 8540 C E King Pkwy, Houston, T 9%, 5815 Antoine Dr, Houston, TX 7 9%, 10918 1/2 Bentley, Houston, TX 7%, 7340 Spencer Hwy, Pasadena, TX 7%, 6400 Bissonnet St, Houston, TX 7%, 9401 Southwest Fwy, Houston, T 6%

USER_COMPANY_BUSINESS_NAME: Spring Branch Community Health 9%, Spring Branch Community Health 9%, Spring Branch Community Health 9%, Spring Branch Community Health 9%, Spring Branch Community Health 9%, Harris County Public Health -  9%, Harris County Public Health -  9%, Harris County Public Health -  9%, Precinct 2 Access2Health Pod - 7%, Precinct 2 Access2Health Pod - 7%, Bayland Teen Health Clinic 7%, The Harris Center for Mental H 6%

USER_ADDRESS_1: 5502 1st St, Katy, TX 77493 9%, 7777 Westgreen Blvd, Cypress,  9%, 15555 Kuykendahl Rd. Ste #319, 9%, 8575 Pitner Rd, Houston, TX 77 9%, 19333 Clay Road, Katy, TX 7744 9%, 3737 Red Bluff Rd, Pasadena, T 9%, 8540 C E King Pkwy, Houston, T 9%, 5815 Antoine Dr, Houston, TX 7 9%, 10918 1/2 Bentley, Houston, TX 7%, 7340 Spencer Hwy, Pasadena, TX 7%, 6400 Bissonnet St, Houston, TX 7%, 9401 Southwest Fwy, Houston, T 6%

USER_PHONE: (832) 927-7350 42%, (713) 231-5757 9%, (713) 387-7180 9%, (281) 885-4630 9%, (713) 462-6545 9%, (713) 462-6555 9%, (713) 274-4353 7%, (713) 970-7000 6%

USER_LANGUAGE: English, Spanish 60%, English, Spanish, Translators  40%

USER_SPECIALTY: Workshops 14%, Family 14%, Couples 14%, Group 14%, Individual 14%, Counseling 14%, medication management 3%, psychiatric evaluations 3%, individual therapy 3%, family counseling 3%, Wellness 3%, and IDD Services 2%

USER_OFFER_VIRTUAL: Check with Provider 67%, Yes 33%

GEOMETRY: {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, {"type": "Point", "coordinates 9%, nan 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 68 | 0 | 67 1; 66 1; 65 1; 64 1 |
| LOC_NAME | category | 3 | 5 | HGAC_Address_P 56; HGAC_StarMap_R 6 |
| SCORE | category | 2 | 0 | 100 62; 0 5 |
| MATCH_TYPE | other | 1 | 0 | A 67 |
| MATCH_ADDR | category | 12 | 5 | 5502 FIRST ST, KATY, TX,  6; 7777 WESTGREEN BLVD, CYPR 6; 15555 KUYKENDAHL RD, HOUS 6; 8575 PITNER RD, HOUSTON,  6 |
| ADDR_TYPE | category | 3 | 5 | PointAddress 56; StreetAddress 6 |
| ADDNUM | category | 12 | 5 | 5502 6; 7777 6; 15555 6; 8575 6 |
| SIDE | category | 2 | 61 | R 6 |
| STPREDIR | empty | 1 | 67 |  |
| STPRETYPE | empty | 1 | 67 |  |
| STNAME | category | 12 | 5 | FIRST 6; WESTGREEN 6; KUYKENDAHL 6; PITNER 6 |
| STTYPE | category | 8 | 5 | RD 24; ST 11; BLVD 6; PKWY 6 |
| STDIR | empty | 1 | 67 |  |
| STADDR | category | 12 | 5 | 5502 FIRST ST 6; 7777 WESTGREEN BLVD 6; 15555 KUYKENDAHL RD 6; 8575 PITNER RD 6 |
| CITY | category | 5 | 5 | HOUSTON 33; KATY 12; PASADENA 11; CYPRESS 6 |
| COUNTY | category | 2 | 5 | HARRIS COUNTY 62 |
| STATE | category | 2 | 5 | TX 62 |
| STATEABBR | category | 2 | 11 | TX 56 |
| ZIP | category | 11 | 5 | 77074 9; 77493 6; 77433 6; 77090 6 |
| ZIP4 | empty | 1 | 67 |  |
| X | amount | 11 | 0 | -95.820092 6; -95.743863 6; -95.461956 6; -95.501614 6 |
| Y | amount | 12 | 0 | 29.786399 6; 29.889947 6; 30.003773 6; 29.828367 6 |
| DISPLAYX | amount | 2 | 0 | 0.0 61; -95.820092 6 |
| DISPLAYY | amount | 2 | 0 | 0.0 61; 29.786399 6 |
| XMIN | other | 1 | 0 | 0 67 |
| XMAX | other | 1 | 0 | 0 67 |
| YMIN | other | 1 | 0 | 0 67 |
| YMAX | other | 1 | 0 | 0 67 |
| ADDNUMFROM | category | 2 | 61 | 5500 6 |
| ADDNUMTO | category | 2 | 61 | 5570 6 |
| COUNTRY | category | 2 | 61 | USA 6 |
| LANGCODE | empty | 1 | 67 |  |
| DISTANCE | other | 1 | 0 | 0 67 |
| STATUS | category | 3 | 0 | M 56; T 6; U 5 |
| IN_SINGLELINE | category | 12 | 0 | 5502 1st St, Katy, TX 774 6; 7777 Westgreen Blvd, Cypr 6; 15555 Kuykendahl Rd. Ste  6; 8575 Pitner Rd, Houston,  6 |
| USER_OBJECTID | empty | 1 | 67 |  |
| USER_OBJECT_ID | empty | 1 | 67 |  |
| USER_COMPANY_BUSINESS_NAME | category | 12 | 0 | Spring Branch Community H 6; Spring Branch Community H 6; Spring Branch Community H 6; Spring Branch Community H 6 |
| USER_ADDRESS | empty | 1 | 67 |  |
| USER_ADDRESS_1 | category | 12 | 0 | 5502 1st St, Katy, TX 774 6; 7777 Westgreen Blvd, Cypr 6; 15555 Kuykendahl Rd. Ste  6; 8575 Pitner Rd, Houston,  6 |
| USER_PHONE | category | 8 | 0 | (832) 927-7350 28; (713) 231-5757 6; (713) 387-7180 6; (281) 885-4630 6 |
| USER_M_F | who | 1 | 0 | <Null> 67 |
| USER_LANGUAGE | category | 2 | 0 | English, Spanish 40; English, Spanish, Transla 27 |
| USER_INSURANCE | who | 1 | 0 | Uninsured, All Insurance 67 |
| USER_SPECIALTY | category | 20 | 0 | Workshops 8; Family 8; Couples 8; Group 8 |
| USER_OFFER_VIRTUAL | category | 2 | 0 | Check with Provider 45; Yes 22 |
| USER_PHONE_1 | empty | 1 | 67 |  |
| USER_ADDRESS_12 | empty | 1 | 67 |  |
| USER_CITY | empty | 1 | 67 |  |
| USER_STATE_NAME | empty | 1 | 67 |  |
| USER_STATE_ABBREVIATION | empty | 1 | 67 |  |
| USER_ZIP_CODE | empty | 1 | 67 |  |
| USER_ZIP_4_EXTENSION | empty | 1 | 67 |  |
| USER_PRIMARY_NAICS | empty | 1 | 67 |  |
| USER_ALL_NAICS_CODES | empty | 1 | 67 |  |
| USER_PRIMARY_SIC | empty | 1 | 67 |  |
| USER_ALL_SIC_CODES | empty | 1 | 67 |  |
| USER_INDUSTRY_DESCRIPTION | empty | 1 | 67 |  |
| USER_AFFILIATED_ORGS | empty | 1 | 67 |  |
| USER_BRANDS | empty | 1 | 67 |  |
| USER_HEADQUARTERS_NAME | empty | 1 | 67 |  |
| USER_LOCATION_CONFIDENCE | empty | 1 | 67 |  |
| USER_NAICS_INDUSTRY_SECTOR | empty | 1 | 67 |  |
| USER_BUSINESS_CATEGORY | empty | 1 | 67 |  |
| USER_SQUARE_FOOTAGE | empty | 1 | 67 |  |
| USER_SQUARE_FOOT_MINIMUM | empty | 1 | 67 |  |
| USER_SQUARE_FOOT_MAXIMUM | empty | 1 | 67 |  |
| USER_EMPLOYEE_COUNT | empty | 1 | 67 |  |
| USER_SALES_VOLUME | empty | 1 | 67 |  |
| USER_CORPORATE_PARENT_NAME | empty | 1 | 67 |  |
| USER_SOURCE | empty | 1 | 67 |  |
| USER_ESRI_PID | empty | 1 | 67 |  |
| USER_DESCRIPTION | empty | 1 | 67 |  |
| USER_LATITUDE | empty | 1 | 67 |  |
| USER_LONGITUDE | empty | 1 | 67 |  |
| USER_LOC_NAME | empty | 1 | 67 |  |
| USER_SCORE | empty | 1 | 67 |  |
| USER_MATCH_TYPE | empty | 1 | 67 |  |
| USER_MATCH_ADDR | empty | 1 | 67 |  |
| USER_ADDR_TYPE | empty | 1 | 67 |  |
| USER_ADDNUM | empty | 1 | 67 |  |
| USER_SIDE | empty | 1 | 67 |  |
| USER_STPREDIR | empty | 1 | 67 |  |
| USER_STPRETYPE | empty | 1 | 67 |  |
| USER_STNAME | empty | 1 | 67 |  |
| USER_STTYPE | empty | 1 | 67 |  |
| USER_STDIR | empty | 1 | 67 |  |
| USER_STADDR | empty | 1 | 67 |  |
| USER_COUNTY | empty | 1 | 67 |  |
| USER_STATEABBR | empty | 1 | 67 |  |
| USER_X | empty | 1 | 67 |  |
| USER_Y | empty | 1 | 67 |  |
| USER_DISPLAYX | empty | 1 | 67 |  |
| USER_DISPLAYY | empty | 1 | 67 |  |
| USER_XMIN | empty | 1 | 67 |  |
| USER_XMAX | empty | 1 | 67 |  |
| USER_YMIN | empty | 1 | 67 |  |
| USER_YMAX | empty | 1 | 67 |  |
| USER_ADDNUMFROM | empty | 1 | 67 |  |
| USER_ADDNUMTO | empty | 1 | 67 |  |
| USER_COUNTRY | empty | 1 | 67 |  |
| USER_LANGCODE | empty | 1 | 67 |  |
| USER_DISTANCE | empty | 1 | 67 |  |
| USER_STATUS | empty | 1 | 67 |  |
| USER_IN_SINGLEL | empty | 1 | 67 |  |
| USER_USER_ZIP_C | empty | 1 | 67 |  |
| USER_USER_NAME | empty | 1 | 67 |  |
| USER_USER_ADDRE | empty | 1 | 67 |  |
| USER_USER_MD | empty | 1 | 67 |  |
| USER_USER_LPC | empty | 1 | 67 |  |
| USER_USER_PHD_E | empty | 1 | 67 |  |
| USER_USER_MSW_L | empty | 1 | 67 |  |
| USER_USER_LMFT | empty | 1 | 67 |  |
| USER_USER_LCDC | empty | 1 | 67 |  |
| USER_USER_OTHER | empty | 1 | 67 |  |
| USER_NAME | empty | 1 | 67 |  |
| USER_NAME_1 | empty | 1 | 67 |  |
| USER_ZIP_CODE_1 | empty | 1 | 67 |  |
| USER_NAME_2 | empty | 1 | 67 |  |
| USER_ADDRESS_2 | empty | 1 | 67 |  |
| USER_PHONE_NUMBER | empty | 1 | 67 |  |
| USER_SHAPE | empty | 1 | 67 |  |
| GEOMETRY | category | 12 | 0 | {"type": "Point", "coordi 6; {"type": "Point", "coordi 6; {"type": "Point", "coordi 6; {"type": "Point", "coordi 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:13.89415 67 |
| SOURCE_RUN_ID | audit | 1 | 0 | a8e31e40-46e2-408c-82f2-b 67 |
| SRC_SHA256 | who | 1 | 0 | 0bca9168ba6cb98632220ffe6 67 |
