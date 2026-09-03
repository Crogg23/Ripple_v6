# PORTAL_ARC_HARRIS_COUNTY_OP_86AE12CFC0

rows 1.1K  columns 23  scan 3.5s

roles: amount 2, audit 2, category 3, date 3, empty 1, id 6, other 3, who 4

## when

CREATIONDATE
  2026      1.1K  ##############################

EDITDATE
  2026      1.1K  ##############################

INGESTED_AT
  2026      1.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 1.1K | 27.72 | 29.76 | 30.11 | 32.58 | 33.6K |
| LONGITUDE | 1.1K | -98.68 | -95.47 | -94.98 | -94.92 | -107.7K |

## who

NAME by rows
       151  WALGREEN CO
       148  CVS Pharmacy Inc
        51  KROGER TEXAS L P
        47  Wal-Mart Stores Texas, LLC
        38  H-E-B LP
        15  HARRIS COUNTY HOSPITAL DISTRICT
        12  Walgreen Co
        12  KS Pharm, LLC
        11  RANDALLS FOOD & DRUGS LP
         9  Sam's East, Inc.
         8  Baylor College of Medicine
         5  COSTCO WHOLESALE CORPORATION
         4  Texas Children's Hospital
         4  KROGER TEXAS LP
         4  The HARRIS CENTER for Mental Health and IDD
         3  ExperienceCare Pharmacy LLC
         3  Family Biocare LLC
         3  Kroger Texas LP
         3  Ngozi A Anaduaka
         2  Harris County Hospital District

NAME by dollars
        4.5K      151 rows  WALGREEN CO
        4.4K      148 rows  CVS Pharmacy Inc
        1.5K       51 rows  KROGER TEXAS L P
        1.4K       47 rows  Wal-Mart Stores Texas, LLC
        1.1K       38 rows  H-E-B LP
      446.68       15 rows  HARRIS COUNTY HOSPITAL DISTRICT
      357.81       12 rows  Walgreen Co
      357.42       12 rows  KS Pharm, LLC
      327.46       11 rows  RANDALLS FOOD & DRUGS LP
      268.56        9 rows  Sam's East, Inc.
      237.98        8 rows  Baylor College of Medicine
      149.27        5 rows  COSTCO WHOLESALE CORPORATION
      119.55        4 rows  KROGER TEXAS LP
      119.12        4 rows  Texas Children's Hospital
      118.98        4 rows  The HARRIS CENTER for Mental Health and IDD
       90.16        3 rows  Kroger Texas LP
       89.19        3 rows  ExperienceCare Pharmacy LLC
       89.07        3 rows  Ngozi A Anaduaka
       88.94        3 rows  Family Biocare LLC
       60.18        2 rows  Yousenasna Group LLC

CREATOR by rows
      1.1K  JGuerraPct2

CREATOR by dollars
       33.6K     1.1K rows  JGuerraPct2

EDITOR by rows
      1.1K  JGuerraPct2

EDITOR by dollars
       33.6K     1.1K rows  JGuerraPct2

SRC_SHA256 by rows
      1.1K  6c4f2dd50af19235f002d0ede68f6b77bfa5f82a422d36ee97f6b26d7d5c9fe6

SRC_SHA256 by dollars
       33.6K     1.1K rows  6c4f2dd50af19235f002d0ede68f6b77bfa5f82a422d36ee97f6b26d7d5c

## who x when

NAME by CREATIONDATE, dollars = LATITUDE
  Baylor College of Medicine                2026:237.98
  COSTCO WHOLESALE CORPORATION              2026:149.27
  CVS Pharmacy Inc                          2026:4.4K
  ExperienceCare Pharmacy LLC               2026:89.19
  Family Biocare LLC                        2026:88.94
  H-E-B LP                                  2026:1.1K
  HARRIS COUNTY HOSPITAL DISTRICT           2026:446.68
  Harris County Hospital District           2026:59.36
  KROGER TEXAS L P                          2026:1.5K
  KROGER TEXAS LP                           2026:119.55
  KS Pharm, LLC                             2026:357.42
  Kroger Texas LP                           2026:90.16
  Ngozi A Anaduaka                          2026:89.07
  RANDALLS FOOD & DRUGS LP                  2026:327.46
  Sam's East, Inc.                          2026:268.56
  Texas Children's Hospital                 2026:119.12
  The HARRIS CENTER for Mental Health and   2026:118.98
  WALGREEN CO                               2026:4.5K
  Wal-Mart Stores Texas, LLC                2026:1.4K
  Walgreen Co                               2026:357.81
  Yousenasna Group LLC                      2026:60.18

CREATOR by CREATIONDATE, dollars = LATITUDE
  JGuerraPct2                               2026:33.6K

## what

STATUS: nan 80%, UNKNOWN 20%

CITY: Houston 72%, Spring 5%, Katy 4%, Pasadena 4%, Cypress 4%, Humble 3%, Tomball 3%, Baytown 2%, Bellaire 1%, Kingwood 1%, Webster 1%, Crosby 0%

PCT: nan 80%, 2.0 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.1K | 0 | 1128 6; 1127 6; 1126 6; 1125 6 |
| STATUS | category | 2 | 0 | nan 899; UNKNOWN 229 |
| NAME | who | 584 | 0 | WALGREEN CO 151; CVS Pharmacy Inc 148; KROGER TEXAS L P 51; Wal-Mart Stores Texas, LL 47 |
| NPI | id | 1.1K | 0 | 1740387141 6; 1093378366 6; 1104251149 6; 1043233422 6 |
| PHONE | id | 1.1K | 0 | 7136608888 7; 7135243330 7; 2814804410 6; 2817244828 6 |
| ADDRESS | id | 1.1K | 0 | 6330 West Loop South 7; 980 Clearlake City Blvd 6; 600 N. Kobayashi Ste 112  6; 500 N Kobayashi Ste E 6 |
| CITY | category | 24 | 0 | Houston 790; Spring 52; Katy 47; Pasadena 44 |
| STATE | other | 1 | 0 | TX 1.1K |
| ZIP | other | 697 | 0 | 77055 16; 77036 16; 77375 15; 77449 14 |
| LATITUDE | amount | 1.1K | 0 | 29.702361 7; 29.696827 7; 29.733022 7; 29.578724 6 |
| LONGITUDE | amount | 1.1K | 0 | -95.760883 7; -95.413074 7; -95.419335 7; -95.158622 6 |
| COUNTY_CODE | other | 1 | 0 | 48201 1.1K |
| PCT | category | 2 | 0 | nan 899; 2.0 229 |
| ICON | empty | 1 | 1.1K |  |
| GLOBALID | id | 1.1K | 0 | 27a7aee3-ec75-41d7-be15-f 6; d0d171d8-c642-4e5b-8b0e-1 6; b2ff2642-aa2d-4089-92d9-3 6; 5a6f98d7-ef61-4444-8d93-1 6 |
| CREATIONDATE | date | 1 | 0 | 1768918781519 1.1K |
| CREATOR | who | 1 | 0 | JGuerraPct2 1.1K |
| EDITDATE | date | 1 | 0 | 1768918781519 1.1K |
| EDITOR | who | 1 | 0 | JGuerraPct2 1.1K |
| GEOMETRY | id | 1.1K | 0 | {"type": "Point", "coordi 7; {"type": "Point", "coordi 7; {"type": "Point", "coordi 7; {"type": "Point", "coordi 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:33:58.63985 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | e23545b2-64d3-49b0-9b8f-4 1.1K |
| SRC_SHA256 | who | 1 | 0 | 6c4f2dd50af19235f002d0ede 1.1K |
