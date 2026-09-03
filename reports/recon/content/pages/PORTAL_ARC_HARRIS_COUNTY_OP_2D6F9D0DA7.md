# PORTAL_ARC_HARRIS_COUNTY_OP_2D6F9D0DA7

rows 2.0K  columns 40  scan 5.4s

roles: amount 9, audit 2, category 9, date 3, empty 1, id 3, other 4, who 10

## when

CREATIONDATE
  2025      2.0K  ##############################

EDITDATE
  2025      2.0K  ##############################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ZIP_4_EXTENSION | 1.9K | 126 | 3.9K | 8.4K | 9.5K | 8.02M |
| SQUARE_FOOT_MINIMUM | 1.7K | 1 | 2.5K | 100.0K | 100.0K | 15.66M |
| SQUARE_FOOT_MAXIMUM | 1.7K | 1.5K | 5.0K | 100.0K | 100.0K | 23.76M |
| EMPLOYEE_COUNT | 2.0K | 1 | 7 | 112.90 | 300 | 29.5K |
| SALES_VOLUME | 1.9K | 64.0K | 637.0K | 10.75M | 32.25M | 2.40B |
| LATITUDE | 2.0K | 29.64 | 29.74 | 30.08 | 30.09 | 59.5K |

## who

COMPANY_BUSINESS_NAME by rows
        41  McDonald's
        29  Jack in the Box
        25  Burger King
        20  Chick-fil-A
        15  Chipotle Mexican Grill
        11  Denny's
        11  Laredo Taco Company
        11  Jimmy John's
         9  IHOP
         9  KFC
         9  Charleys Philly Steaks
         8  Extended Stay America
         7  Church's Texas Chicken
         7  Chili's
         6  First Watch
         6  Becks Prime
         5  Buffalo Wild Wings
         5  Murphy's Deli
         5  Firehouse Subs
         5  Jersey Mike's Subs

COMPANY_BUSINESS_NAME by dollars
        1.2K       41 rows  McDonald's
      863.36       29 rows  Jack in the Box
         744       25 rows  Burger King
      595.95       20 rows  Chick-fil-A
      446.83       15 rows  Chipotle Mexican Grill
      328.34       11 rows  Laredo Taco Company
      327.78       11 rows  Jimmy John's
      327.69       11 rows  Denny's
      267.92        9 rows  Charleys Philly Steaks
      267.84        9 rows  KFC
      267.83        9 rows  IHOP
      238.15        8 rows  Extended Stay America
      208.73        7 rows  Chili's
      208.45        7 rows  Church's Texas Chicken
         179        6 rows  First Watch
      178.55        6 rows  Becks Prime
      149.29        5 rows  Jersey Mike's Subs
      149.21        5 rows  Buffalo Wild Wings
      148.85        5 rows  Jason's Deli
      148.78        5 rows  Murphy's Deli

HEADQUARTERS_NAME by rows
      1.5K  nan
        41  McDonald's USA, LLC
        29  Different Rules, LLC
        27  Hilton Worldwide Inc
        25  Burger King Corporation
        20  Chick-fil-A, Inc
        15  Chipotle Mexican Grill, Inc
        13  Marriott International, Inc
        13  Choice Hotels International, Inc
        11  Denny's Inc
        11  Jimmy John's Franchise, LLC
        11  7-Eleven, Inc
         9  Gosh Enterprises, Inc
         9  Holiday Hospitality Franchising, LLC
         9  IHOP LLC
         9  KFC Corporation
         9  Extended Stay America, Inc
         7  Cajun Global LLC
         7  La Quinta Holdings Inc
         7  Chili's Grill & Bar

HEADQUARTERS_NAME by dollars
       43.9K     1.5K rows  nan
        1.2K       41 rows  McDonald's USA, LLC
      863.36       29 rows  Different Rules, LLC
      803.92       27 rows  Hilton Worldwide Inc
         744       25 rows  Burger King Corporation
      595.95       20 rows  Chick-fil-A, Inc
      446.83       15 rows  Chipotle Mexican Grill, Inc
      387.30       13 rows  Choice Hotels International, Inc
      386.91       13 rows  Marriott International, Inc
      328.34       11 rows  7-Eleven, Inc
      327.78       11 rows  Jimmy John's Franchise, LLC
      327.69       11 rows  Denny's Inc
      268.30        9 rows  Holiday Hospitality Franchising, LLC
      267.92        9 rows  Gosh Enterprises, Inc
      267.88        9 rows  Extended Stay America, Inc
      267.84        9 rows  KFC Corporation
      267.83        9 rows  IHOP LLC
      208.73        7 rows  Chili's Grill & Bar
      208.60        7 rows  La Quinta Holdings Inc
      208.45        7 rows  Cajun Global LLC

SOURCE by rows
      2.0K  Data Axle

SOURCE by dollars
       59.5K     2.0K rows  Data Axle

CREATOR by rows
      2.0K  Pjohnson1906

CREATOR by dollars
       59.5K     2.0K rows  Pjohnson1906

## who x when

COMPANY_BUSINESS_NAME by CREATIONDATE, dollars = LATITUDE
  Becks Prime                               2025:178.55
  Buffalo Wild Wings                        2025:149.21
  Burger King                               2025:744
  Charleys Philly Steaks                    2025:267.92
  Chick-fil-A                               2025:595.95
  Chili's                                   2025:208.73
  Chipotle Mexican Grill                    2025:446.83
  Church's Texas Chicken                    2025:208.45
  Denny's                                   2025:327.69
  Extended Stay America                     2025:238.15
  Firehouse Subs                            2025:148.70
  First Watch                               2025:179
  IHOP                                      2025:267.83
  Jack in the Box                           2025:863.36
  Jason's Deli                              2025:148.85
  Jersey Mike's Subs                        2025:149.29
  Jimmy John's                              2025:327.78
  KFC                                       2025:267.84
  Laredo Taco Company                       2025:328.34
  McDonald's                                2025:1.2K
  Murphy's Deli                             2025:148.78

HEADQUARTERS_NAME by CREATIONDATE, dollars = LATITUDE
  7-Eleven, Inc                             2025:328.34
  Burger King Corporation                   2025:744
  Cajun Global LLC                          2025:208.45
  Chick-fil-A, Inc                          2025:595.95
  Chili's Grill & Bar                       2025:208.73
  Chipotle Mexican Grill, Inc               2025:446.83
  Choice Hotels International, Inc          2025:387.30
  Denny's Inc                               2025:327.69
  Different Rules, LLC                      2025:863.36
  Extended Stay America, Inc                2025:267.88
  Gosh Enterprises, Inc                     2025:267.92
  Hilton Worldwide Inc                      2025:803.92
  Holiday Hospitality Franchising, LLC      2025:268.30
  IHOP LLC                                  2025:267.83
  Jimmy John's Franchise, LLC               2025:327.78
  KFC Corporation                           2025:267.84
  La Quinta Holdings Inc                    2025:208.60
  Marriott International, Inc               2025:386.91
  McDonald's USA, LLC                       2025:1.2K
  nan                                       2025:43.9K

## what

CITY: Houston 81%, Katy 15%, Tomball 2%, Cypress 1%, Waller 1%, Hockley 0%, Stafford 0%

ZIP_CODE: 77036 14%, 77449 11%, 77077 9%, 77084 9%, 77072 9%, 77057 8%, 77079 7%, 77056 7%, 77450 7%, 77042 7%, 77081 5%, 77063 5%

PRIMARY_NAICS: 72251117 86%, 72111002 9%, 71131004 3%, 72251301 2%, 71131003 1%, 71131005 0%

PRIMARY_SIC: 581208 86%, 701101 9%, 738944 3%, 581206 2%, 794104 1%, 651211 0%

AFFILIATED_ORGS: nan 100%, Five Star Alliance 0%

LOCATION_CONFIDENCE: High 94%, Medium 5%, Low 1%

NAICS_INDUSTRY_SECTOR: Accommodation & Food Services 96%, Arts, Entertainment & Recreati 4%

BUSINESS_CATEGORY: Independent 74%, Branch 26%, Headquarters 0%

SQUARE_FOOTAGE: 2500 - 4999 33%, 5000 - 9999 16%, nan 15%, 10000 - 19999 10%, 1500 - 2499 9%, 1 - 1499 6%, 20000 - 39999 5%, 40000 - 99999 4%, 100000+ 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| OBJECT_ID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| COMPANY_BUSINESS_NAME | who | 1.7K | 0 | McDonald's 45; Jack in the Box 37; Burger King 28; Chick-fil-A 20 |
| ADDRESS | who | 323 | 0 | Westheimer Rd 207; Bellaire Blvd 160; Katy Fwy 115; Richmond Ave 80 |
| CITY | category | 7 | 0 | Houston 1.6K; Katy 296; Tomball 31; Cypress 29 |
| STATE_NAME | other | 1 | 0 | Texas 2.0K |
| STATE_ABBREVIATION | other | 1 | 0 | TX 2.0K |
| ZIP_CODE | category | 44 | 0 | 77036 176; 77449 141; 77077 117; 77084 115 |
| ZIP_4_EXTENSION | amount | 1.3K | 0 | nan 72; 3202.0 12; 5552.0 11; 4990.0 11 |
| PRIMARY_NAICS | category | 6 | 0 | 72251117 1.7K; 72111002 172; 71131004 57; 72251301 32 |
| ALL_NAICS_CODES | who | 208 | 0 | 72251117 1.1K; 72251117, 72251301 274; 72111002 71; 71131004 48 |
| PRIMARY_SIC | category | 6 | 0 | 581208 1.7K; 701101 172; 738944 57; 581206 32 |
| ALL_SIC_CODES | who | 215 | 0 | 581208 1.1K; 581208, 581206 274; 701101 71; 738944 48 |
| INDUSTRY_DESCRIPTION | who | 216 | 0 | Restaurants 1.1K; Restaurants, Foods-Carry  274; Hotels & Motels 71; Events-Special 48 |
| AFFILIATED_ORGS | category | 2 | 0 | nan 2.0K; Five Star Alliance 2 |
| BRANDS | empty | 1 | 2.0K |  |
| HEADQUARTERS_NAME | who | 147 | 0 | nan 1.5K; McDonald's USA, LLC 41; Different Rules, LLC 29; Hilton Worldwide Inc 27 |
| LOCATION_CONFIDENCE | category | 3 | 0 | High 1.9K; Medium 93; Low 23 |
| NAICS_INDUSTRY_SECTOR | category | 2 | 0 | Accommodation & Food Serv 1.9K; Arts, Entertainment & Rec 73 |
| BUSINESS_CATEGORY | category | 3 | 0 | Independent 1.5K; Branch 524; Headquarters 1 |
| SQUARE_FOOTAGE | category | 9 | 0 | 2500 - 4999 658; 5000 - 9999 314; nan 296; 10000 - 19999 207 |
| SQUARE_FOOT_MINIMUM | amount | 9 | 0 | 2500.0 658; 5000.0 314; nan 296; 10000.0 207 |
| SQUARE_FOOT_MAXIMUM | amount | 8 | 0 | 4999.0 658; nan 343; 9999.0 314; 19999.0 207 |
| EMPLOYEE_COUNT | amount | 82 | 0 | 6.0 236; 7.0 228; 5.0 159; 8.0 153 |
| SALES_VOLUME | amount | 155 | 0 | 1639000.0 263; 382000.0 185; 446000.0 165; nan 129 |
| SOURCE | who | 1 | 0 | Data Axle 2.0K |
| ESRI_PID | id | 2.0K | 0 | 3842f588b05eedaaa5a565e6f 10; 33cd5ee3e2d4b996300301570 10; 2db662f177eca3d25fe7abd7d 10; 238269230de700abcc54389b9 10 |
| DESCRIPTION | other | 1.7K | 0 | McDonald's, Houston, Texa 36; Jack in the Box, Houston, 31; Burger King, Houston, Tex 22; KFC, Houston, Texas 16 |
| LATITUDE | amount | 1.5K | 0 | 29.702523 17; 29.706306 13; 29.879646 12; 29.74905 11 |
| LONGITUDE | amount | 1.5K | 0 | -95.554229 17; -95.54388 13; -95.720602 12; -95.643676 11 |
| CREATIONDATE | date | 1 | 0 | 1759952460000 2.0K |
| CREATOR | who | 1 | 0 | Pjohnson1906 2.0K |
| EDITDATE | date | 1 | 0 | 1759952460000 2.0K |
| EDITOR | who | 1 | 0 | Pjohnson1906 2.0K |
| X | amount | 1.5K | 0 | -95.554229 17; -95.54388 13; -95.720602 12; -95.643676 11 |
| Y | amount | 1.5K | 0 | 29.702523 17; 29.706306 13; 29.879646 12; 29.74905 11 |
| GEOMETRY | other | 1.5K | 0 | {"type": "Point", "coordi 17; {"type": "Point", "coordi 13; {"type": "Point", "coordi 12; {"type": "Point", "coordi 11 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:33:15.76364 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | a68694c4-b3f0-4d52-9795-2 2.0K |
| SRC_SHA256 | who | 1 | 0 | 7e94b508bec71421978c4c942 2.0K |
