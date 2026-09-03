# PORTAL_SOC_CHICAGO_DATA_POR_1CA267A903

rows 2.0K  columns 21  scan 4.0s

roles: audit 2, category 3, date 1, id 2, other 9, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

DBA_NAME by rows
         8  YBUY FINANCIAL LLC
         5  STARBUCKS CORP
         5  REDBOX AUTOMATED RETAIL LLC
         4  BOND DRUG COMPANY OF ILLINOIS LLC
         4  COMPASS ONE LLC
         3  CHIPOTLE MEXICAN GRILL INC
         3  GAMESTOP INC
         3  JEWEL FOOD STORES INC
         3  LORI'S GIFTS, INC.
         3  GLC VENDING, CORP
         3  JACKSON AVENUE SUBS INC
         2  POTBELLY SANDWICH WORKS LLC
         2  NEW CINGULAR WIRELESS PCS LLC
         2  SODEXO AMERICA LLC
         2  CREATIVE HAIRDRESSERS INC
         2  FAMILY DOLLAR INC
         2  FASHION GALLERY INC
         2  T-MOBILE CENTRAL LLC
         2  BLUE KANGAROO MANAGEMENT LLC
         2  CAR OUTLET AC LLC

ILLINOIS_BUSINESS_TAX_NUMBER by rows
         8  4115-4584
         5  2004-2851
         5  3624-7960
         4  3271-9299
         4  0586-2061
         3  2309-4729
         3  0097-1316
         3  4003-0172
         3  3929-6172
         3  2947-2946
         3  2378-9778
         2  2086-3578
         2  3920-8885
         2  1687-0174
         2  2526-8317
         2  3115-8110
         2  3984-4935
         2  3693-3007
         2  2678-3320
         2  3985-1818

OWNING_ENTITY by rows
       999  nan
         9  SUBWAY
         8  YBUY
         3  SURPRISE PARTIES
         2  SHELL OIL PRODUCTS US
         2  LOUIS VUITTON
         2  CITGO FUEL & MINI MART
         2  RAINBOW SHOP
         2  MCDONALDS
         2  JIMMY JOHNS
         2  THE BLUE KANGAROO
         2  J & J FISH
         2  EL DORADO
         2  AT&T MOBILITY
         1  DA CONNECTION
         1  LOS NUEVOS CHEFS DEL SABOR
         1  QUAD CITY CHIMNEY SWEEP
         1  CHEF SARA'S CAFE
         1  BRITTANYS FASHION BOUTIQUE
         1  LUIS'S GROCERY STORE

CITY by rows
      1.8K  CHICAGO
        25  nan
         4  CICERO
         4  FOREST PARK
         3  AURORA
         3  KANSAS CITY
         3  NAPERVILLE
         3  SAINT LOUIS
         3  SKOKIE
         3  PLANO
         2  WILMETTE
         2  OAK PARK
         2  CATHEDRAL CITY
         2  WILMINGTON
         2  NEW YORK
         2  DAVENPORT
         2  EVANSTON
         2  SAN DIEGO
         2  WHEATON
         2  DALLAS

## who x when

DBA_NAME by INGESTED_AT  LOAD STAMP, not an event date
  BLUE KANGAROO MANAGEMENT LLC              2026:2
  BOND DRUG COMPANY OF ILLINOIS LLC         2026:4
  CAR OUTLET AC LLC                         2026:2
  CHIPOTLE MEXICAN GRILL INC                2026:3
  COMPASS ONE LLC                           2026:4
  CREATIVE HAIRDRESSERS INC                 2026:2
  FAMILY DOLLAR INC                         2026:2
  FASHION GALLERY INC                       2026:2
  GAMESTOP INC                              2026:3
  GLC VENDING, CORP                         2026:3
  JACKSON AVENUE SUBS INC                   2026:3
  JEWEL FOOD STORES INC                     2026:3
  LORI'S GIFTS, INC.                        2026:3
  NEW CINGULAR WIRELESS PCS LLC             2026:2
  POTBELLY SANDWICH WORKS LLC               2026:2
  REDBOX AUTOMATED RETAIL LLC               2026:5
  SODEXO AMERICA LLC                        2026:2
  STARBUCKS CORP                            2026:5
  T-MOBILE CENTRAL LLC                      2026:2
  YBUY FINANCIAL LLC                        2026:8

ILLINOIS_BUSINESS_TAX_NUMBER by INGESTED_AT  LOAD STAMP, not an event date
  0097-1316                                 2026:3
  0586-2061                                 2026:4
  1687-0174                                 2026:2
  2004-2851                                 2026:5
  2086-3578                                 2026:2
  2309-4729                                 2026:3
  2378-9778                                 2026:3
  2526-8317                                 2026:2
  2678-3320                                 2026:2
  2947-2946                                 2026:3
  3115-8110                                 2026:2
  3271-9299                                 2026:4
  3624-7960                                 2026:5
  3693-3007                                 2026:2
  3920-8885                                 2026:2
  3929-6172                                 2026:3
  3984-4935                                 2026:2
  3985-1818                                 2026:2
  4003-0172                                 2026:3
  4115-4584                                 2026:8

## what

TYPE_OF_FILER: PL 83%, CL 17%, TL 0%

STATE: IL 95%, nan 1%, MO 1%, CA 1%, WI 1%, MN 0%, MI 0%, TX 0%, NY 0%, OH 0%, IN 0%, FL 0%

ADDRESS_SECONDARY: nan 99%, PO BOX 9149 0%, N16085 HAROLD ST 0%, BANK OF AMERICA BLDG 0%, STE 280 0%, 10302 E 55TH PL 0%, MUSEUM OF SCIENCE& INDUSTRY 0%, C/O TAX DEPT TEN SOUTH 0%, UNIT 301 0%, CHICAGO O'HARE AIRPORT 0%, 12TH FLOOR 0%, PO BOX 10483 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ILLINOIS_BUSINESS_TAX_NUMBER | who | 2.0K | 0 | 4115-4584 13; 2766-4899 10; 3996-4183 10; 2136-7582 10 |
| SEQUENCE_NUMBER | other | 73 | 0 | 1 1.3K; 0 272; 2 204; 3 57 |
| TYPE_OF_FILER | category | 3 | 0 | PL 1.7K; CL 331; TL 7 |
| SIC | other | 244 | 0 | 5812 299; 5999 188; 5947 117; 7299 93 |
| DBA_NAME | who | 1.9K | 0 | YBUY FINANCIAL LLC 13; MARIAN NIXON 10; OSCAR AGUILAR 10; JABCA INC 10 |
| OWNING_ENTITY | who | 953 | 0 | nan 999; SUBWAY 9; YBUY 9; MARIAN NIXON PAINTINGS 5 |
| ADDRESS | id | 1.9K | 0 | nan 25; 2139 W BERWYN AVE 10; 6551 S KILBOURN AVE 10; 2026 W WEBSTER AVE 10 |
| CITY | who | 179 | 0 | CHICAGO 1.8K; nan 25; CICERO 4; FOREST PARK 4 |
| STATE | category | 31 | 0 | IL 1.8K; nan 27; MO 11; CA 11 |
| ZIP | other | 1.9K | 0 | nan 28; 60634-2520 11; 60642-2502 11; 60619 11 |
| LOCATION | id | 1.9K | 0 | nan 25; {"latitude": "41.97776312 10; {"latitude": "41.77337252 10; {"latitude": "41.92140580 10 |
| COMPUTED_REGION_6MKV_F3DW | other | 254 | 0 | 21538 79; 21190 73; 22535 67; 22616 58 |
| COMPUTED_REGION_RPCA_8UM6 | other | 59 | 0 | nan 241; 39 76; 16 70; 1 62 |
| COMPUTED_REGION_VRXF_VC4K | other | 78 | 0 | nan 241; 37 152; 38 127; 29 96 |
| COMPUTED_REGION_BDYS_3D7I | other | 574 | 0 | nan 241; 92 71; 580 27; 652 27 |
| COMPUTED_REGION_43WA_7QMU | other | 51 | 0 | nan 241; 36 226; 46 72; 11 67 |
| COMPUTED_REGION_AWAF_S7UX | other | 52 | 0 | nan 239; 22 221; 48 98; 51 67 |
| ADDRESS_SECONDARY | category | 15 | 0 | nan 2.0K; PO BOX 9149 1; N16085 HAROLD ST 1; BANK OF AMERICA BLDG 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:44:22.45506 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2b84bb2f-f7e4-4280-8cf4-3 2.0K |
| SRC_SHA256 | who | 1 | 0 | e77db4670d380645b24e556b5 2.0K |
