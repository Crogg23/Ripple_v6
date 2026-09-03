# PORTAL_ARC_LA_COUNTY_OPEN_D_E85041E063

rows 1.8K  columns 28  scan 5.0s

roles: amount 1, audit 2, category 10, date 1, empty 1, id 2, other 4, who 8

## when

INGESTED_AT
  2026      1.8K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 1.8K | 85 | 100 | 100 | 100 | 181.6K |

## who

CONAME by rows
       235  T-MOBILE
       120  SPRINT
        98  CRICKET WIRELESS AUTH RETAILER
        82  METRO BY T-MOBILE
        71  AT&T STORE
        59  PRIME COMMUNICATIONS-AT&T AUTH
        39  VICTRA-VERIZON AUTH RETAILER
        38  VERIZON WIRELESS
        29  BOOST MOBILE
        24  GO WIRELESS-VERIZON AUTH RTLR
        23  WIRELESS ADVOCATES
        15  IMOBILE-SPRINT AUTH RETAILER
        14  WIRELESS PLUS-VERIZON AUTH
        13  ARCH TELECOM-SPRINT AUTH RTLR
        10  MY WIRELESS-AT&T AUTH RETAILER
        10  WIRELESS LIFESTYLE-SPRINT AUTH
         8  VERITY WIRELESS-SPRINT AUTH
         8  ULTIMATE WIRELESS-VERIZON AUTH
         6  DF WIRELESS
         4  BOOST MOBILE PREMIER

CONAME by dollars
       23.5K      235 rows  T-MOBILE
       12.0K      120 rows  SPRINT
        9.8K       98 rows  CRICKET WIRELESS AUTH RETAILER
        8.2K       82 rows  METRO BY T-MOBILE
        7.1K       71 rows  AT&T STORE
        5.9K       59 rows  PRIME COMMUNICATIONS-AT&T AUTH
        3.9K       39 rows  VICTRA-VERIZON AUTH RETAILER
        3.8K       38 rows  VERIZON WIRELESS
        2.9K       29 rows  BOOST MOBILE
        2.4K       24 rows  GO WIRELESS-VERIZON AUTH RTLR
        2.3K       23 rows  WIRELESS ADVOCATES
        1.5K       15 rows  IMOBILE-SPRINT AUTH RETAILER
        1.4K       14 rows  WIRELESS PLUS-VERIZON AUTH
        1.3K       13 rows  ARCH TELECOM-SPRINT AUTH RTLR
        1.0K       10 rows  WIRELESS LIFESTYLE-SPRINT AUTH
      999.52       10 rows  MY WIRELESS-AT&T AUTH RETAILER
         800        8 rows  VERITY WIRELESS-SPRINT AUTH
         800        8 rows  ULTIMATE WIRELESS-VERIZON AUTH
         586        6 rows  DF WIRELESS
         400        4 rows  EXPERTS CHOICE-SPRINT AUTH

STATE_NAME by rows
      1.8K  California

STATE_NAME by dollars
      181.6K     1.8K rows  California

NAICS by rows
      1.8K  51731214

NAICS by dollars
      181.6K     1.8K rows  51731214

SIC by rows
      1.8K  481207

SIC by dollars
      181.6K     1.8K rows  481207

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  ARCH TELECOM-SPRINT AUTH RTLR             2026:1.3K
  AT&T STORE                                2026:7.1K
  BOOST MOBILE                              2026:2.9K
  BOOST MOBILE PREMIER                      2026:400
  CRICKET WIRELESS AUTH RETAILER            2026:9.8K
  DF WIRELESS                               2026:586
  EXPERTS CHOICE-SPRINT AUTH                2026:400
  GO WIRELESS-VERIZON AUTH RTLR             2026:2.4K
  IMOBILE-SPRINT AUTH RETAILER              2026:1.5K
  METRO BY T-MOBILE                         2026:8.2K
  MY WIRELESS-AT&T AUTH RETAILER            2026:999.52
  PRIME COMMUNICATIONS-AT&T AUTH            2026:5.9K
  SPRINT                                    2026:12.0K
  T-MOBILE                                  2026:23.5K
  ULTIMATE WIRELESS-VERIZON AUTH            2026:800
  VERITY WIRELESS-SPRINT AUTH               2026:800
  VERIZON WIRELESS                          2026:3.8K
  VICTRA-VERIZON AUTH RETAILER              2026:3.9K
  WIRELESS ADVOCATES                        2026:2.3K
  WIRELESS LIFESTYLE-SPRINT AUTH            2026:1.0K
  WIRELESS PLUS-VERIZON AUTH                2026:1.4K

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:181.6K

## what

SALESVOL: 1927 56%, 5781 9%, 3854 9%, 6744 7%, 2891 6%, 4817 4%, 964 3%, 8671 2%, 9634 2%, 7707 1%, 11561 1%, 10598 1%

HDBRCH: 2 100%, 1 0%, 3 0%

ULTNUM: 000000000 51%, 507958353 17%, 800138737 9%, 460637358 9%, 566623054 3%, 007564776 2%, 603864331 2%, 358565984 2%, 720755608 1%, 524037314 1%, 425850924 1%, 440024295 1%

PUBPRV: 2 100%, 1 0%

EMPNUM: 2 56%, 6 9%, 4 9%, 7 7%, 3 6%, 5 4%, 1 3%, 9 2%, 10 2%, 8 1%, 12 1%, 11 1%

FRNCOD: d 16%, S 15%, T 13%, z 12%, M 10%, D 9%, 02 7%, HO 5%, B 5%, GO 3%, O 3%

SQFTCODE: 2 53%, 3 30%, 4 8%, 1 6%, 5 1%, 6 1%, 7 0%, 8 0%

LOC_NAME: PointAddress 50%, StreetAddress 31%, Subaddress 16%, Postal 2%, PostalExt 1%, StreetName 0%, StreetAddressExt 0%

STATUS: M 99%, T 1%

REC_TYPE: 0 99%, 1 1%, 2 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.8K | 0 | 1818 10; 1817 10; 1816 10; 1815 10 |
| LOCNUM | id | 1.8K | 0 | 995867942 10; 992928978 10; 992928747 10; 989369673 10 |
| CONAME | who | 846 | 0 | T-MOBILE 235; SPRINT 120; CRICKET WIRELESS AUTH RET 99; METRO BY T-MOBILE 82 |
| STREET | who | 530 | 24 | VENTURA BLVD 31; VAN NUYS BLVD 29; HAWTHORNE BLVD 28; WILSHIRE BLVD 27 |
| CITY | who | 127 | 0 | LOS ANGELES 417; LONG BEACH 83; VAN NUYS 35; HUNTINGTON PARK 35 |
| STATE | other | 1 | 0 | CA 1.8K |
| STATE_NAME | who | 1 | 0 | California 1.8K |
| ZIP | other | 261 | 0 | 90255 35; 90006 27; 91748 25; 91402 22 |
| ZIP4 | other | 1.3K | 55 | 3711 10; 1945 10; 4021 10; 1502 10 |
| NAICS | who | 1 | 0 | 51731214 1.8K |
| SIC | who | 1 | 0 | 481207 1.8K |
| SALESVOL | category | 32 | 0 | 1927 978; 5781 165; 3854 163; 6744 117 |
| HDBRCH | category | 4 | 912 | 2 902; 1 3; 3 1 |
| ULTNUM | category | 25 | 0 | 000000000 912; 507958353 304; 800138737 166; 460637358 164 |
| PUBPRV | category | 3 | 1.1K | 2 674; 1 1 |
| EMPNUM | category | 30 | 0 | 2 982; 6 165; 4 162; 7 116 |
| FRNCOD | category | 24 | 955 | d 126; S 120; T 104; z 98 |
| ISCODE | empty | 1 | 1.8K |  |
| SQFTCODE | category | 9 | 2 | 2 958; 3 550; 4 146; 1 116 |
| LOC_NAME | category | 7 | 0 | PointAddress 917; StreetAddress 558; Subaddress 299; Postal 28 |
| STATUS | category | 2 | 0 | M 1.8K; T 14 |
| SCORE | amount | 26 | 0 | 100.0 1.8K; 99.890625 27; 86.0 7; 98.0 4 |
| SOURCE | who | 1 | 0 | INFOGROUP 1.8K |
| REC_TYPE | category | 3 | 0 | 0 1.8K; 1 24; 2 3 |
| GEOMETRY | other | 1.6K | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:31:22.08627 1.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4c0b436f-72a9-47b7-b363-2 1.8K |
| SRC_SHA256 | who | 1 | 0 | 42c0c2bdfbf1c525c582f56d0 1.8K |
