# PORTAL_CKA_ANALYZE_BOSTON_9FE0838E9F

rows 968  columns 33  scan 3.1s

roles: audit 2, category 9, date 1, other 8, who 14

## when

INGESTED_AT
  2026       968  ##############################

## who

COMPANY_NAME by rows
         2  CDW Consultants, Inc.
         2  Kripper Architecture Studio, Inc.
         1  Urban Edge Housing Corporation
         1  City Sealcoating, Inc.
         1  Highland Development Group, LLC
         1  Synergy Contracting, Inc.
         1  Choo & Company, Inc.
         1  Dorchester Bay Economic Development Corporation
         1  ImEx Cargo
         1  Linea 5, Inc.
         1  JaMa Professional Cleaning, Inc.
         1  Outkast Electrical Contractors, Inc.
         1  JEWN Enterprise, Inc.
         1  LGAPPAREL, LLC dba LMI Textiles
         1  Kambrian Corporation
         1  Communication via Design, Ltd.
         1  Supplier Diversity Experts, LLC
         1  Casablanca Services, Inc.
         1  Self Esteem Boston Educational Institute, Inc.
         1  Cross Country Painting Company, Inc.

CONTACT_NAME by rows
         3  Rokeya Begum
         3  Nhung Lam
         2  Stephanie O'Mahony
         2  Kristen Pope
         2  Shonte Davidson
         2  Micah Logan
         2  Tricia Young
         2  Gretchen Lundgren
         2  Ann Sullivan
         2  Anel Bellevue
         2  david console
         2  Jeff Rogers
         2  Kevin Chin
         2  Duane Edward Osborn
         2  Jacqueline Lawlor
         2  Shari Betty
         2  Francois Exilhomme
         2  Maria Gonzalez
         2  Peter Smith
         2  Jennifer Ha

DATE_BUSINESS_ESTABLISHED by rows
        55  2022
        55  2023
        43  2024
        43  2021
        42  2019
        41  2020
        32  2015
        28  2017
        25  2018
        23  2012
        23  2016
        17  2025
        16  2013
        11  2010
        11  01/01/2017
        11  2011
        10  01/01/2018
         9  01/01/2016
         9  01/01/2014
         8  01/01/2015

NAICS_CODES1 by rows
        71  541611 - Administrative Management and General Management Consulting S
        41  541310 - Architectural Services
        30  561720 - Janitorial Services 
        29  541330 - Engineering Services
        27  541511 - Custom Computer Programming Services 
        25  541613 - Marketing Consulting Services 
        20  541618 - Other Management Consulting Services 
        18  611710 - Educational Support Services
        18  541430 - Graphic Design Services
        17  722511 - Full-Service Restaurants 
        15  238320 - Painting and Wall Covering Contractors
        13  531390 - Other Activities Related to Real Estate 
        13  722320 - Caterers
        13  541320 - Landscape Architectural Services
        13  541512 - Computer Systems Design Services 
        13  541690 - Other Scientific and Technical Consulting Services
        13  238210 - Electrical Contractors and Other Wiring Installation Contract
        11  611430 - Professional and Management Development Training 
        11  238990 - All Other Specialty Trade Contractors
        11  236220 - Commercial and Institutional Building Construction 

## who x when

COMPANY_NAME by INGESTED_AT  LOAD STAMP, not an event date
  CDW Consultants, Inc.                     2026:2
  Casablanca Services, Inc.                 2026:1
  Choo & Company, Inc.                      2026:1
  City Sealcoating, Inc.                    2026:1
  Communication via Design, Ltd.            2026:1
  Cross Country Painting Company, Inc.      2026:1
  Dorchester Bay Economic Development Corp  2026:1
  Highland Development Group, LLC           2026:1
  ImEx Cargo                                2026:1
  JEWN Enterprise, Inc.                     2026:1
  JaMa Professional Cleaning, Inc.          2026:1
  Kambrian Corporation                      2026:1
  Kripper Architecture Studio, Inc.         2026:2
  LGAPPAREL, LLC dba LMI Textiles           2026:1
  Linea 5, Inc.                             2026:1
  Outkast Electrical Contractors, Inc.      2026:1
  Self Esteem Boston Educational Institute  2026:1
  Supplier Diversity Experts, LLC           2026:1
  Synergy Contracting, Inc.                 2026:1
  Urban Edge Housing Corporation            2026:1

CONTACT_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Anel Bellevue                             2026:2
  Ann Sullivan                              2026:2
  Duane Edward Osborn                       2026:2
  Francois Exilhomme                        2026:2
  Gretchen Lundgren                         2026:2
  Jacqueline Lawlor                         2026:2
  Jeff Rogers                               2026:2
  Jennifer Ha                               2026:2
  Kevin Chin                                2026:2
  Kristen Pope                              2026:2
  Maria Gonzalez                            2026:2
  Micah Logan                               2026:2
  Nhung Lam                                 2026:3
  Peter Smith                               2026:2
  Rokeya Begum                              2026:3
  Shari Betty                               2026:2
  Shonte Davidson                           2026:2
  Stephanie O'Mahony                        2026:2
  Tricia Young                              2026:2
  david console                             2026:2

## what

MBE_WBE_CERT: MBE 39%, WBE 31%, MWBE 30%

SMALL_LOCAL_CERT: SLBE 60%, SBE 40%, SBE, SLBE 0%

VETERAN_CERT: SVOB 47%, SVOB, SDVOB 29%, SDVOB 24%

SDO_CERTIFIED: No 58%, Yes 42%

CITY_REGISTERED: Yes 51%, No 49%

STATE: MA 89%, NY 3%, Massachusetts 2%, NH 1%, GA 1%, CT 1%, IL 1%, DC 1%, CA 1%, NJ 1%, PA 1%, MD 1%

BUSINESS_TYPE: Limited Liability Company (LLC 42%, Corporation 39%, Sole Proprietorship 10%, Limited Liability Company 6%, Non Profit 3%, Partnership 1%

CONSTRUCTION: No 84%, Yes 16%

NUMBER_EMPLOYEES: Less than 10 73%, 11 - 20 12%, 21 - 40 6%, 41 - 100 5%, Greater than 100 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMPANY_NAME | who | 953 | 0 | Leone Marketing Solutions 5; Prep Work Consulting 5; The Social Butterflies Ev 5; Helco Safety Equipment Co 5 |
| SERVICES_PROVIDED | other | 975 | 0 | Real Estate Development 6; Promotional Products and  5; Education Consultant Serv 5; Event Planning, Coordinat 5 |
| MBE_WBE_CERT | category | 4 | 39 | MBE 360; WBE 286; MWBE 283 |
| SMALL_LOCAL_CERT | category | 4 | 513 | SLBE 272; SBE 182; SBE, SLBE 1 |
| VETERAN_CERT | category | 4 | 951 | SVOB 8; SVOB, SDVOB 5; SDVOB 4 |
| SDO_CERTIFIED | category | 2 | 0 | No 566; Yes 402 |
| CITY_REGISTERED | category | 2 | 0 | Yes 491; No 477 |
| ADDRESS | other | 949 | 0 | 867 Boylston Street, Bost 6; 6 Baker Hill Drive, Hingh 5; 4580 Watch Hill Court, Do 5; 93 Saint Gregory Street,  5 |
| CITY | who | 246 | 0 | Boston 352; Dorchester 44; Roxbury 15; Hyde Park 14 |
| STATE | category | 35 | 0 | MA 818; NY 27; Massachusetts 17; NH 8 |
| ZIPCODE | other | 348 | 0 | 02119 40; 02124 34; 02136 33; 02121 29 |
| CONTACT_NAME | who | 939 | 0 | Rachel Leone 5; Shauntice Wheeler 5; Paige Pasley 5; Arthur Hellender 5 |
| CONTACT_TITLE | other | 821 | 97 | President 18; Owner 14; CEO 8; Rachel Leone 5 |
| PHONE | other | 958 | 0 | (781) 740-3171 5; (404) 955-7082 5; (617) 594-5868 5; (617) 846-4210 5 |
| FAX | other | 136 | 830 | (000) 000-0000 2; (617) 296-5134 2; (178) 418-468 1; (978) 452-3796 1 |
| EMAIL | other | 955 | 0 | rachel@leonemarketing.com 5; support@prepwork.org 5; info@tsb.events 5; ahellender@helcosafety.co 5 |
| WEBSITE | other | 791 | 181 | N/A 6; leonemarketing.com 4; www.prepwork.org 4; tsb.events 4 |
| BUSINESS_TYPE | category | 7 | 99 | Limited Liability Company 364; Corporation 336; Sole Proprietorship 83; Limited Liability Company 48 |
| CONSTRUCTION | category | 3 | 90 | No 737; Yes 141 |
| DATE_BUSINESS_ESTABLISHED | who | 141 | 154 | 2022 55; 2023 55; 2021 43; 2024 43 |
| NUMBER_EMPLOYEES | category | 6 | 6 | Less than 10 700; 11 - 20 116; 21 - 40 62; 41 - 100 48 |
| COB_CATEGORY_CODES1 | who | 98 | 0 | COM - Consultants: Manage 54; FD - Food Products, Servi 51; AE - Architects/Engineers 51; AD - Advertising/Audovisu 44 |
| COB_CATEGORY_CODES2 | who | 90 | 392 | COM - Consultants: Manage 41; TA - Training (see also E 26; COA - Consultants: Archit 22; COD - Consultants: Design 22 |
| COB_CATEGORY_CODES3 | who | 83 | 596 | TA - Training (see also E 23; MK - Marketing 17; COA - Consultants: Archit 16; COM - Consultants: Manage 15 |
| NAICS_CODES1 | who | 254 | 0 | 541611 - Administrative M 71; 541310 - Architectural Se 41; 561720 - Janitorial Servi 30; 541330 - Engineering Serv 29 |
| NAICS_CODES2 | who | 217 | 360 | 541618 - Other Management 34; 541613 - Marketing Consul 21; 541611 - Administrative M 20; 541512 - Computer Systems 18 |
| NAICS_CODES3 | who | 157 | 573 | 611430 - Professional and 21; 541611 - Administrative M 17; 541618 - Other Management 14; 541519 - Other Computer R 13 |
| UNSPSC_CODE1 | who | 153 | 0 | 81100000 - Professional e 65; 80100000 - Management adv 59; 72110000 - Residential bu 44; 90100000 - Restaurants an 34 |
| UNSPSC_CODE2 | who | 138 | 529 | 72120000 - Nonresidential 24; 80100000 - Management adv 19; 80160000 - Business admin 17; 81160000 - Information Te 12 |
| UNSPSC_CODE3 | who | 108 | 708 | 80100000 - Management adv 13; 72120000 - Nonresidential 10; 43230000 - Software 9; 72150000 - Specialized tr 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:01:22.88393 968 |
| SOURCE_RUN_ID | audit | 1 | 0 | 24c994cb-004a-4a46-9f5c-e 968 |
| SRC_SHA256 | who | 1 | 0 | a611d778723f2da0e6d14ec17 968 |
