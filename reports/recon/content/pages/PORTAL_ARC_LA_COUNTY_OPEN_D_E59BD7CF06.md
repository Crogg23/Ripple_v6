# PORTAL_ARC_LA_COUNTY_OPEN_D_E59BD7CF06

rows 659  columns 28  scan 4.9s

roles: amount 1, audit 2, category 10, date 1, empty 1, other 6, who 8

## when

INGESTED_AT
  2026       659  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 659 | 85 | 100 | 100 | 100 | 65.9K |

## who

CONAME by rows
        73  T-MOBILE
        52  CRICKET WIRELESS AUTH RETAILER
        47  METRO BY T-MOBILE
        33  SPRINT
        19  BOOST MOBILE
        18  AT&T STORE
        10  PRIME COMMUNICATIONS-AT&T AUTH
         8  VERIZON WIRELESS
         7  VICTRA-VERIZON AUTH RETAILER
         6  WIRELESS ADVOCATES
         4  ALL STAR WIRELESS
         4  ARCH TELECOM-SPRINT AUTH RTLR
         3  IMOBILE-SPRINT AUTH RETAILER
         3  WIRELESS PLUS-VERIZON AUTH
         3  CELL ZONE
         3  AVE WIRELESS
         3  ULTIMATE WIRELESS-VERIZON AUTH
         3  MY WIRELESS-AT&T AUTH RETAILER
         3  GOT WIRELESS
         2  C & J WIRELESS INC

CONAME by dollars
        7.3K       73 rows  T-MOBILE
        5.2K       52 rows  CRICKET WIRELESS AUTH RETAILER
        4.7K       47 rows  METRO BY T-MOBILE
        3.3K       33 rows  SPRINT
        1.9K       19 rows  BOOST MOBILE
        1.8K       18 rows  AT&T STORE
      999.78       10 rows  PRIME COMMUNICATIONS-AT&T AUTH
         800        8 rows  VERIZON WIRELESS
         700        7 rows  VICTRA-VERIZON AUTH RETAILER
         600        6 rows  WIRELESS ADVOCATES
         400        4 rows  ARCH TELECOM-SPRINT AUTH RTLR
         400        4 rows  ALL STAR WIRELESS
         300        3 rows  AVE WIRELESS
         300        3 rows  MY WIRELESS-AT&T AUTH RETAILER
         300        3 rows  IMOBILE-SPRINT AUTH RETAILER
         300        3 rows  WIRELESS PLUS-VERIZON AUTH
         300        3 rows  GOT WIRELESS
         300        3 rows  ULTIMATE WIRELESS-VERIZON AUTH
         300        3 rows  CELL ZONE
         200        2 rows  SINALOA 2000 INC

STATE_NAME by rows
       659  California

STATE_NAME by dollars
       65.9K      659 rows  California

NAICS by rows
       659  51731214

NAICS by dollars
       65.9K      659 rows  51731214

SIC by rows
       659  481207

SIC by dollars
       65.9K      659 rows  481207

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  ALL STAR WIRELESS                         2026:400
  ARCH TELECOM-SPRINT AUTH RTLR             2026:400
  AT&T STORE                                2026:1.8K
  AVE WIRELESS                              2026:300
  BOOST MOBILE                              2026:1.9K
  C & J WIRELESS INC                        2026:200
  CELL ZONE                                 2026:300
  CRICKET WIRELESS AUTH RETAILER            2026:5.2K
  GOT WIRELESS                              2026:300
  IMOBILE-SPRINT AUTH RETAILER              2026:300
  METRO BY T-MOBILE                         2026:4.7K
  MY WIRELESS-AT&T AUTH RETAILER            2026:300
  PRIME COMMUNICATIONS-AT&T AUTH            2026:999.78
  SINALOA 2000 INC                          2026:200
  SPRINT                                    2026:3.3K
  T-MOBILE                                  2026:7.3K
  ULTIMATE WIRELESS-VERIZON AUTH            2026:300
  VERIZON WIRELESS                          2026:800
  VICTRA-VERIZON AUTH RETAILER              2026:700
  WIRELESS ADVOCATES                        2026:600
  WIRELESS PLUS-VERIZON AUTH                2026:300

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:65.9K

## what

SALESVOL: 1927 57%, 3854 11%, 5781 9%, 2891 6%, 964 6%, 6744 5%, 4817 2%, 11561 1%, 9634 1%, 10598 1%, 19268 1%, 14451 1%

HDBRCH: 2 100%, 1 0%

ULTNUM: 000000000 56%, 507958353 17%, 460637358 10%, 800138737 9%, 566623054 2%, 007564776 1%, 603864331 1%, 720755608 1%, 440024295 1%, 435142912 0%, 524037314 0%, 425850924 0%

PUBPRV: 2 100%

EMPNUM: 2 57%, 4 11%, 6 9%, 3 6%, 1 6%, 7 5%, 5 2%, 12 1%, 10 1%, 11 1%, 20 1%, 15 1%

FRNCOD: z 20%, M 18%, d 17%, S 13%, T 11%, D 7%, 02 4%, B 3%, HO 3%, O 2%, I3 2%

SQFTCODE: 2 59%, 3 24%, 1 9%, 4 5%, 5 1%, 6 1%, 7 0%, 8 0%

LOC_NAME: PointAddress 55%, StreetAddress 30%, Subaddress 14%, Postal 0%, PostalExt 0%

STATUS: M 99%, T 1%

REC_TYPE: 0 100%, 1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 645 | 0 | 659 4; 658 4; 657 4; 656 4 |
| LOCNUM | other | 651 | 0 | 992928978 4; 987795309 4; 987621877 4; 978209658 4 |
| CONAME | who | 360 | 0 | T-MOBILE 73; CRICKET WIRELESS AUTH RET 52; METRO BY T-MOBILE 47; SPRINT 33 |
| STREET | who | 222 | 2 | VAN NUYS BLVD 24; PACIFIC BLVD 17; S VERMONT AVE 16; WHITTIER BLVD 14 |
| CITY | who | 58 | 0 | LOS ANGELES 253; LONG BEACH 34; HUNTINGTON PARK 27; GLENDALE 21 |
| STATE | other | 1 | 0 | CA 659 |
| STATE_NAME | who | 1 | 0 | California 659 |
| ZIP | other | 121 | 0 | 90255 27; 90006 23; 91402 21; 90201 19 |
| ZIP4 | other | 532 | 13 | 3711 5; 2409 5; 4104 5; 2564 5 |
| NAICS | who | 1 | 0 | 51731214 659 |
| SIC | who | 1 | 0 | 481207 659 |
| SALESVOL | category | 23 | 0 | 1927 367; 3854 69; 5781 55; 2891 37 |
| HDBRCH | category | 3 | 365 | 2 293; 1 1 |
| ULTNUM | category | 20 | 0 | 000000000 365; 507958353 113; 460637358 65; 800138737 61 |
| PUBPRV | category | 2 | 411 | 2 248 |
| EMPNUM | category | 21 | 0 | 2 368; 4 69; 6 55; 3 37 |
| FRNCOD | category | 19 | 388 | z 52; M 47; d 44; S 33 |
| ISCODE | empty | 1 | 659 |  |
| SQFTCODE | category | 8 | 0 | 2 392; 3 160; 1 59; 4 34 |
| LOC_NAME | category | 5 | 0 | PointAddress 364; StreetAddress 198; Subaddress 93; Postal 3 |
| STATUS | category | 2 | 0 | M 654; T 5 |
| SCORE | amount | 11 | 0 | 100.0 639; 99.890625 10; 98.59375 2; 85.0 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 659 |
| REC_TYPE | category | 2 | 0 | 0 657; 1 2 |
| GEOMETRY | other | 603 | 0 | {"type": "Point", "coordi 6; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4; {"type": "Point", "coordi 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:25:24.14133 659 |
| SOURCE_RUN_ID | audit | 1 | 0 | ebac1552-5f48-4fbf-80ce-3 659 |
| SRC_SHA256 | who | 1 | 0 | 8cae9d7bb0ba77f9fb207b9c7 659 |
