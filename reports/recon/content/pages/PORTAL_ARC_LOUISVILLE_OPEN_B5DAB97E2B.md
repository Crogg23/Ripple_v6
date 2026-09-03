# PORTAL_ARC_LOUISVILLE_OPEN_B5DAB97E2B

rows 2.0K  columns 21  scan 2.9s

roles: audit 2, category 5, date 1, empty 1, id 2, other 6, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

COMPANY_NAME by rows
         7  Edward Jones
         4  Mortenson Family Dental
         3  Ken Towery's Tire & Autocare
         3  Louisville Ky
         3  Mc Donald's
         3  Thorntons
         3  Autozone
         3  Burger King
         3  El Nopal
         3  H&R Block
         3  Meineke
         3  Chipotle Mexican Grill
         3  Enterprise Rent-A-Car
         3  Chick-Fil-A
         3  Hanger Clinic
         2  Little Caesars
         2  Jet's Pizza
         2  Cellular Sales-Verizon Auth
         2  Bistro
         2  ACF Services Co

EXECUTIVE_LAST_NAME by rows
       614  nan
        11  Miller
        11  Smith
         8  Martin
         8  Thomas
         7  Brown
         7  Mattingly
         5  Woods
         5  Wilson
         5  Dunn
         5  Adams
         5  Brooks
         4  Lancaster
         4  Wagner
         4  Baker
         4  Johnson
         4  Gray
         4  Cox
         4  Morris
         4  Butler

EXECUTIVE_FIRST_NAME by rows
       614  nan
        19  John
        18  Michael
        17  Brian
        17  David
        14  Scott
        14  James
        13  Mike
        12  Mark
        11  Steve
        10  Jeff
        10  Chris
        10  Robert
         9  Kevin
         8  Greg
         7  William
         7  Paul
         7  Susan
         7  Matthew
         6  Keith

PRIMARY_SIC_DESCRIPTION by rows
       116  Nonclassified Establishments
       114  Restaurants
        59  Physicians & Surgeons
        48  Attorneys
        39  Dentists
        37  Real Estate
        37  Insurance
        35  Real Estate Management
        31  Nurses-Practitioners
        23  Beauty Salons
        22  Financial Advisory Services
        22  Apartments
        21  Construction Companies
        20  Physical Therapists
        16  Home Builders
        16  Chiropractors DC
        16  Social Workers
        15  Automobile Repairing & Service
        14  Services NEC
        13  Electric Contractors

## who x when

COMPANY_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ACF Services Co                           2026:2
  Autozone                                  2026:3
  Bistro                                    2026:2
  Burger King                               2026:3
  Cellular Sales-Verizon Auth               2026:2
  Chick-Fil-A                               2026:3
  Chipotle Mexican Grill                    2026:3
  Edward Jones                              2026:7
  El Nopal                                  2026:3
  Enterprise Rent-A-Car                     2026:3
  H&R Block                                 2026:3
  Hanger Clinic                             2026:3
  Jet's Pizza                               2026:2
  Ken Towery's Tire & Autocare              2026:3
  Little Caesars                            2026:2
  Louisville Ky                             2026:3
  Mc Donald's                               2026:3
  Meineke                                   2026:3
  Mortenson Family Dental                   2026:4
  Thorntons                                 2026:3

EXECUTIVE_LAST_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Adams                                     2026:5
  Baker                                     2026:4
  Brooks                                    2026:5
  Brown                                     2026:7
  Butler                                    2026:4
  Cox                                       2026:4
  Dunn                                      2026:5
  Gray                                      2026:4
  Johnson                                   2026:4
  Lancaster                                 2026:4
  Martin                                    2026:8
  Mattingly                                 2026:7
  Miller                                    2026:11
  Morris                                    2026:4
  Smith                                     2026:11
  Thomas                                    2026:8
  Wagner                                    2026:4
  Wilson                                    2026:5
  Woods                                     2026:5
  nan                                       2026:614

## what

CITY: Louisville 90%, Jeffersontown 2%, Fairdale 2%, Prospect 2%, St Matthews 1%, Middletown 1%, Valley Station 0%, Anchorage 0%, Lyndon 0%, Okolona 0%, Douglass Hills 0%, Hills And Dales 0%

ZIP_CODE: 40299 26%, 40223 16%, 40241 8%, 40243 8%, 40272 7%, 40204 6%, 40207 6%, 40202 5%, 40203 5%, 40217 5%, 40229 4%, 40291 4%

EXECUTIVE_TITLE: nan 43%, Owner 26%, Manager 17%, President 3%, Other 3%, Director 2%, CEO 2%, Vice President 2%, Site Manager 1%, Administrator 1%, Regional Mgr 1%, Office Manager 1%

LOCATION_EMPLOYEE_SIZE_RANGE: 1 to 4 58%, 5 to 9 16%, 10 to 19 9%, 20 to 49 7%, nan 6%, 50 to 99 2%, 100 to 249 1%, 250 to 499 0%, 500 to 999 0%, 1000 to 4999 0%

LOCATION_SALES_VOLUME_RANGE: Less Than $500,000 45%, $500,000-1 Million 17%, $1-2.5 Million 14%, nan 10%, $2.5-5 Million 6%, $5-10 Million 4%, $10-20 Million 1%, $20-50 Million 1%, $50-100 Million 0%, $100-500 Million 0%, Over $1 Billion 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMPANY_NAME | who | 1.9K | 0 | Century Belmont Station 10; Homesweet Homes 10; Got 2 Dance LLC 10; Middletown City 10 |
| EXECUTIVE_FIRST_NAME | who | 863 | 0 | nan 614; John 19; Michael 18; Brian 17 |
| EXECUTIVE_LAST_NAME | who | 1.1K | 0 | nan 614; Miller 12; Smith 11; Thomas 9 |
| ADDRESS | id | 2.0K | 0 | 11950 Victory Knoll Cir 10; 1195 Lincoln Ave 10; 119 Norwood Dr 10; 11803 Old Shelbyville Rd 10 |
| CITY | category | 14 | 0 | Louisville 1.8K; Jeffersontown 49; Fairdale 46; Prospect 45 |
| STATE | other | 1 | 0 | KY 2.0K |
| ZIP_CODE | category | 32 | 0 | 40299 421; 40223 267; 40241 130; 40243 124 |
| EXECUTIVE_TITLE | category | 34 | 0 | nan 821; Owner 493; Manager 325; President 64 |
| LOCATION_EMPLOYEE_SIZE_RANGE | category | 10 | 0 | 1 to 4 1.2K; 5 to 9 324; 10 to 19 182; 20 to 49 134 |
| LOCATION_SALES_VOLUME_RANGE | category | 11 | 0 | Less Than $500,000 906; $500,000-1 Million 347; $1-2.5 Million 287; nan 206 |
| PHONE_NUMBER_COMBINED | other | 1.6K | 0 | Not Available 388; (502) 754-6303 9; (502) 594-9111 9; (502) 245-2762 9 |
| PRIMARY_SIC_CODE | other | 668 | 0 | 999977 116; 581208 114; 801101 59; 811103 48 |
| PRIMARY_SIC_DESCRIPTION | who | 665 | 0 | Nonclassified Establishme 116; Restaurants 114; Physicians & Surgeons 59; Attorneys 48 |
| SIC_CODE_1 | other | 668 | 0 | 999977 116; 581208 114; 801101 59; 811103 48 |
| SIC_CODE_1_DESCRIPTION | other | 665 | 0 | Nonclassified Establishme 116; Restaurants 114; Physicians & Surgeons 59; Attorneys 48 |
| COLUMN15 | empty | 1 | 2.0K |  |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| GEOMETRY | other | 1.6K | 0 | {"type": "Point", "coordi 48; {"type": "Point", "coordi 18; {"type": "Point", "coordi 17; {"type": "Point", "coordi 15 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:36:03.95905 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | e569a913-c97b-4457-a8a6-b 2.0K |
| SRC_SHA256 | who | 1 | 0 | 85febb8bea7c3acc38573f1ff 2.0K |
