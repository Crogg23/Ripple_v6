# PORTAL_ARC_LOUISVILLE_OPEN_4654B3D9BA

rows 2.0K  columns 20  scan 4.1s

roles: audit 2, category 5, date 1, empty 1, id 1, other 5, who 6

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

COMPANY_NAME by rows
      1.2K  nan
         2  Advocates For Women's Health
         2  GE Co
         2  Mountjoy Chilton Medley LLP
         1  Jefferson Audio Video Systems
         1  Generator Supercenter-Lsvll
         1  Meijer Bakery
         1  First Care Realty LLC
         1  Bittys Baked Goods
         1  Hans Management LLC
         1  All Trucking Logistics LLC
         1  Dollar Tree
         1  D B S Oldham LLC
         1  Falco Drilling
         1  Bluegrass Hydronics
         1  Diamond Cut Lawn & Landscaping
         1  Barrow Brown Carrington PLLC
         1  Abbotts Window Tinting
         1  Leaf Home Stair Lift
         1  Choose Russell Inc

EXECUTIVE_LAST_NAME by rows
      1.5K  nan
         4  Johnson
         4  Howell
         4  Brown
         4  Moore
         4  Hill
         4  Smith
         3  Ryan
         3  Anderson
         3  Adams
         3  Jones
         3  Cook
         3  Hall
         3  Baker
         2  Vaughn
         2  Daily
         2  Francis
         2  Barrett
         2  Crawford
         2  Petty

EXECUTIVE_FIRST_NAME by rows
      1.5K  nan
         7  David
         6  Mark
         6  John
         5  Jim
         5  Robert
         5  Jeff
         4  Justin
         4  Christopher
         4  James
         4  Gary
         4  Kathy
         4  Melissa
         4  Joseph
         3  Brian
         3  Greg
         3  Doug
         3  Steve
         3  Tom
         3  Kevin

ADDRESS by rows
      1.2K  nan
         1  13100 Mddltwn Ind Blvd
         1  201 A Flexner Way # 600
         1  1538 Wyltle St
         1  2601 S Gault Pkwy # 101
         1  2600 S Gault Pkwy # 201
         1  201 A Flexner Way # 902
         1  13015 Mddltwn Ind Blvd
         1  455 S Main # 382
         1  3700 Johnson Hall Dr
         1  13117 Mddltwn Ind Blvd
         1  7313 Ralph Ave
         1  201 A Flexner Way # 1105
         1  3050 Hunsinger Ln
         1  13050 Eastgt Park Way # 108
         1  1553 KY-44
         1  201 A Flexner Way # 1101
         1  1850 S Hurstbrn Pkwy # 166
         1  1850 S Hurstbrn Pkwy # 189
         1  4915 Nortn Hlthcr Blvd # 507

## who x when

COMPANY_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Abbotts Window Tinting                    2026:1
  Advocates For Women's Health              2026:2
  All Trucking Logistics LLC                2026:1
  Barrow Brown Carrington PLLC              2026:1
  Bittys Baked Goods                        2026:1
  Bluegrass Hydronics                       2026:1
  Choose Russell Inc                        2026:1
  D B S Oldham LLC                          2026:1
  Diamond Cut Lawn & Landscaping            2026:1
  Dollar Tree                               2026:1
  Falco Drilling                            2026:1
  First Care Realty LLC                     2026:1
  GE Co                                     2026:2
  Generator Supercenter-Lsvll               2026:1
  Hans Management LLC                       2026:1
  Jefferson Audio Video Systems             2026:1
  Leaf Home Stair Lift                      2026:1
  Meijer Bakery                             2026:1
  Mountjoy Chilton Medley LLP               2026:2
  nan                                       2026:1.2K

EXECUTIVE_LAST_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Adams                                     2026:3
  Anderson                                  2026:3
  Baker                                     2026:3
  Barrett                                   2026:2
  Brown                                     2026:4
  Cook                                      2026:3
  Crawford                                  2026:2
  Daily                                     2026:2
  Francis                                   2026:2
  Hall                                      2026:3
  Hill                                      2026:4
  Howell                                    2026:4
  Johnson                                   2026:4
  Jones                                     2026:3
  Moore                                     2026:4
  Petty                                     2026:2
  Ryan                                      2026:3
  Smith                                     2026:4
  Vaughn                                    2026:2
  nan                                       2026:1.5K

## what

CITY: nan 62%, Louisville 35%, Prospect 1%, St Matthews 0%, Glenview 0%, Eastwood 0%, Fairdale 0%, Middletown 0%, Anchorage 0%, Jeffersontown 0%, Fisherville 0%, Lyndon 0%

STATE: nan 62%, KY 38%

EXECUTIVE_TITLE: nan 82%, Owner 9%, Manager 6%, President 1%, Other 1%, Director 1%, CEO 0%, Vice President 0%, Exec Officer 0%, Site Manager 0%, Senior VP 0%, Regional Mgr 0%

LOCATION_EMPLOYEE_SIZE_RANGE: nan 69%, 1 to 4 22%, 5 to 9 5%, 10 to 19 2%, 20 to 49 1%, 100 to 249 0%, 50 to 99 0%

LOCATION_SALES_VOLUME_RANGE: nan 72%, Less Than $500,000 16%, $500,000-1 Million 6%, $1-2.5 Million 3%, $2.5-5 Million 2%, $20-50 Million 1%, $5-10 Million 1%, $10-20 Million 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMPANY_NAME | who | 758 | 0 | nan 1.2K; Lansing, Peter Scott MD 4; Neikirk, E Bruce Aty 4; Carewise Health Inc 4 |
| EXECUTIVE_FIRST_NAME | who | 340 | 0 | nan 1.5K; David 7; Mark 6; Robert 6 |
| EXECUTIVE_LAST_NAME | who | 394 | 0 | nan 1.5K; Jones 4; Baker 4; Ryan 4 |
| ADDRESS | who | 747 | 0 | nan 1.2K; Williams & Wagner Psc 4; Westport Vlg 4; Vertex House Styal Rd Gre 4 |
| CITY | category | 17 | 0 | nan 1.2K; Louisville 690; Prospect 27; St Matthews 7 |
| STATE | category | 2 | 0 | nan 1.2K; KY 755 |
| ZIP_CODE | other | 53 | 0 | nan 1.2K; 40223.0 113; 40202.0 65; 40232.0 45 |
| EXECUTIVE_TITLE | category | 25 | 0 | nan 1.6K; Owner 174; Manager 112; President 20 |
| LOCATION_EMPLOYEE_SIZE_RANGE | category | 7 | 0 | nan 1.4K; 1 to 4 450; 5 to 9 91; 10 to 19 32 |
| LOCATION_SALES_VOLUME_RANGE | category | 8 | 0 | nan 1.4K; Less Than $500,000 318; $500,000-1 Million 112; $1-2.5 Million 68 |
| PHONE_NUMBER_COMBINED | other | 412 | 0 | nan 1.2K; Not Available 333; (502) 498-8379 3; (502) 426-4888 3 |
| PRIMARY_SIC_CODE | other | 319 | 0 | nan 1.2K; 999977.0 137; 801101.0 39; 811103.0 25 |
| PRIMARY_SIC_DESCRIPTION | who | 319 | 0 | nan 1.2K; Nonclassified Establishme 137; Physicians & Surgeons 39; Attorneys 25 |
| SIC_CODE_1 | other | 319 | 0 | nan 1.2K; 999977.0 137; 801101.0 39; 811103.0 25 |
| SIC_CODE_1_DESCRIPTION | other | 319 | 0 | nan 1.2K; Nonclassified Establishme 137; Physicians & Surgeons 39; Attorneys 25 |
| COLUMN15 | empty | 1 | 2.0K |  |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:35:56.45887 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 14568bfd-3250-493d-8c2e-3 2.0K |
| SRC_SHA256 | who | 1 | 0 | 93fa0d23e46d0067b2d778b67 2.0K |
