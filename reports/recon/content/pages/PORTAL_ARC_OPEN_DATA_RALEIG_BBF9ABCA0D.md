# PORTAL_ARC_OPEN_DATA_RALEIG_BBF9ABCA0D

rows 1.9K  columns 15  scan 3.5s

roles: audit 2, category 3, date 1, id 2, other 4, who 4

## when

INGESTED_AT
  2026      1.9K  ##############################

## who

BUSINESS_NAME by rows
         6  WAKE COUNTY GOVERNMENT
         4  SUBWAY
         4  WESTERN UNION AGENT LOCATION
         3  FIRST BAPTIST CHURCH
         3  CVS PHARMACY
         2  MC DONALD'S
         2  WELLS FARGO
         2  AUTOZONE
         2  APPLETREE DAY CARE
         2  COUNTY COMMISSIONERS
         2  CITY OF RALEIGH
         2  WALGREENS
         2  STATE EMPLOYEES' CREDIT UNION
         2  DEBNAM CLINIC
         2  WAKE SPECIALTY PHYSICIANS LLC
         2  DOLLAR TREE
         2  NEWS & OBSERVER
         2  WAKE COUNTY GEOGRAPHIC INFO
         2  FOX ROTHSCHILD
         2  NORTH CAROLINA SOLAR CTR

SICGROUP by rows
       151  Legal Services
       142  Executive, Legislative, And General Government, Except Finance
       123  Business Services
       123  Eating And Drinking Places
       121  Engineering, Accounting, Research, Management, And Related Services
       117  Membership Organizations
        94  Health Services
        93  Real Estate
        81  Social Services
        77  Personal Services
        57  Miscellaneous Retail
        50  Construction Special Trade Contractors
        44  Building Construction General Contractors And Operative Builders
        42  Automotive Repair, Services, And Parking
        30  Food Stores
        29  Security And Commodity Brokers, Dealers, Exchanges, And Services
        27  Educational Services
        27  Depository Institutions
        25  Nonclassifiable Establishments
        25  Agricultural Services

STREET by rows
       423  FAYETTEVILLE ST
       350  NEW BERN AVE
       186  nan
        88  W HARGETT ST
        79  S WILMINGTON ST
        60  S SALISBURY ST
        52  E HARGETT ST
        31  W MORGAN ST
        30  S BLOUNT ST
        26  E MARTIN ST
        24  E EDENTON ST
        22  CORPORATION PKWY
        19  E JONES ST
        18  W MARTIN ST
        17  POOLE RD
        17  N PERSON ST
        17  SUNNYBROOK RD
        15  S MCDOWELL ST
        15  W EDENTON ST
        14  W JONES ST

SRC_SHA256 by rows
      1.9K  e5329a82af576ac1a9e40961348c017972dbcdeff6215fa71a0a111843f3df29

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date
  APPLETREE DAY CARE                        2026:2
  AUTOZONE                                  2026:2
  CITY OF RALEIGH                           2026:2
  COUNTY COMMISSIONERS                      2026:2
  CVS PHARMACY                              2026:3
  DEBNAM CLINIC                             2026:2
  DOLLAR TREE                               2026:2
  FIRST BAPTIST CHURCH                      2026:3
  FOX ROTHSCHILD                            2026:2
  MC DONALD'S                               2026:2
  NEWS & OBSERVER                           2026:2
  NORTH CAROLINA SOLAR CTR                  2026:2
  STATE EMPLOYEES' CREDIT UNION             2026:2
  SUBWAY                                    2026:4
  WAKE COUNTY GEOGRAPHIC INFO               2026:2
  WAKE COUNTY GOVERNMENT                    2026:6
  WAKE SPECIALTY PHYSICIANS LLC             2026:2
  WALGREENS                                 2026:2
  WELLS FARGO                               2026:2
  WESTERN UNION AGENT LOCATION              2026:4

SICGROUP by INGESTED_AT  LOAD STAMP, not an event date
  Agricultural Services                     2026:25
  Automotive Repair, Services, And Parking  2026:42
  Building Construction General Contractor  2026:44
  Business Services                         2026:123
  Construction Special Trade Contractors    2026:50
  Depository Institutions                   2026:27
  Eating And Drinking Places                2026:123
  Educational Services                      2026:27
  Engineering, Accounting, Research, Manag  2026:121
  Executive, Legislative, And General Gove  2026:142
  Food Stores                               2026:30
  Health Services                           2026:94
  Legal Services                            2026:151
  Membership Organizations                  2026:117
  Miscellaneous Retail                      2026:57
  Nonclassifiable Establishments            2026:25
  Personal Services                         2026:77
  Real Estate                               2026:93
  Security And Commodity Brokers, Dealers,  2026:29
  Social Services                           2026:81

## what

SUBAREA: 529F 14%, 254 13%, 529C 11%, 34B 10%, 529H 10%, 529E 8%, 597 6%, 529D 6%, 569 5%, 123 5%, 337 5%, 498 5%

CITY: RALEIGH, NC 27601 65%, RALEIGH, NC 27610 26%, RALEIGH, NC 27604 2%, RALEIGH, NC 27611 2%, RALEIGH, NC 27602 2%, RALEIGH, NC 27603 1%, RALEIGH, NC 27697 0%, RALEIGH, NC 27615 0%, RALEIGH, NC 27612 0%, RALEIGH, NC 27609 0%

SICDIVISION: Services 49%, Retail Trade 15%, Public Administration 12%, Finance, Insurance, And Real E 11%, Construction 5%, Transportation, Communications 3%, Agriculture, Forestry, And Fis 2%, Wholesale Trade 1%, Manufacturing 1%, Mining 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.8K | 0 | 1877 10; 1876 10; 1875 10; 1874 10 |
| ID | id | 1.8K | 0 | 1877 10; 1876 10; 1875 10; 1874 10 |
| SUBAREA | category | 24 | 0 | 529F 198; 254 189; 529C 165; 34B 150 |
| BUSINESS_NAME | who | 1.8K | 0 | JEFFRIES RIDGE APARTMENTS 10; IN & OUT MARKET LLC 10; FIVE BIG BROTHERS LLC 10; HARRIS AUTOMOTIVE & CAR 10 |
| STREET | who | 181 | 0 | FAYETTEVILLE ST 423; NEW BERN AVE 350; nan 186; W HARGETT ST 88 |
| CITY | category | 10 | 0 | RALEIGH, NC 27601 1.2K; RALEIGH, NC 27610 494; RALEIGH, NC 27604 45; RALEIGH, NC 27611 40 |
| EMPLOYEES | other | 94 | 0 | 3 316; 4 248; 2 223; 5 156 |
| SIC_CODE | other | 545 | 0 | 811103 149; 581208 91; 912103 51; 912102 50 |
| SALES | other | 558 | 0 | 0 497; 669 63; 481 34; 431 30 |
| SICNO | other | 62 | 0 | 81 151; 91 142; 73 123; 58 123 |
| SICGROUP | who | 62 | 0 | Legal Services 151; Executive, Legislative, A 142; Business Services 123; Eating And Drinking Place 123 |
| SICDIVISION | category | 10 | 0 | Services 923; Retail Trade 282; Public Administration 221; Finance, Insurance, And R 201 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:31:27.30544 1.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | bdc059f8-d38d-4dda-9576-a 1.9K |
| SRC_SHA256 | who | 1 | 0 | e5329a82af576ac1a9e409613 1.9K |
