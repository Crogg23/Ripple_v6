# FED_FEC_COMMITTEES

rows 60.0K  columns 18  scan 3.4s

roles: audit 2, category 4, date 1, other 5, state 1, who 6

## when

_INGESTED_AT
  2026     60.0K  ##############################

## who

C4 by rows
       471  PO BOX 30844
       327  PO BOX 26141
       322  PO BOX 183
       300  824 S MILLEDGE AVE STE 101
       282  PO BOX 9891
       235  918 PENNSYLVANIA AVE SE
       220  611 PENNSYLVANIA AVE SE
       183  228 S. WASHINGTON ST.
       176  PO BOX 15320
       157  600 PENNSYLVANIA AVE SE
       134  1742 WOODBEND DR
       127  C/O BULLDOG COMPLIANCE
       113  610 S. BOULEVARD
       109  C/O RED CURVE SOLUTIONS
       108  122 C STREET NW
       107  600 PENNSYLVANIA AVE SE #15180
       107  228 S WASHINGTON ST STE 115
       101  PO BOX 97275
        98  PO BOX 65322
        96  PO BOX 33079

C3 by rows
       660  DATWYLER, THOMAS
       609  KILGORE, PAUL
       452  LISKER, LISA
       385  MARTIN, STEVEN
       367  MARSTON, CHRIS
       311  PETTERSON, JAY
       310  HOBBS, CABELL
       301  MAY, JENNIFER
       266  ZAMORE, JUDITH
       251  KYRIACOPOULOS, JANICA
       210  CURTIS, ELIZABETH
       184  JACKSON, SUE
       182  SATTERFIELD, DAVID
       164  GLAZE, KAYLA
       162  MELE, STEVEN
       161  WILLIAMSON, LES
       156  PHILLIPS, ROBERT III
       154  GANTT, CHARLES
       148  WATKINS, NANCY H.
       143  OTTENHOFF, BENJAMIN

C14 by rows
     16.8K  NONE
        89  TAKE BACK THE HOUSE 2022
        42  DOLLARS FOR DEMOCRATS
        39  TAKE BACK THE HOUSE 2020
        33  SERVE AMERICA VICTORY FUND
        30  CALIFORNIA REPUBLICAN PARTY
        24  REPUBLICAN PARTY OF TEXAS
        22  DEMOCRATIC GRASSROOTS VICTORY FUND
        21  DEMOCRATIC PARTY OF VIRGINIA
        20  CALIFORNIA REPUBLICAN PARTY (FEDERAL)
        18  TRUMP VICTORY
        16  GROW THE MAJORITY
        15  REPUBLICAN NATIONAL COMMITTEE
        14  REPUBLICANS INSPIRING SUCCESS & EMPOWERMENT PROJECT (RISE PROJECT)
        14  CRUZ 20 FOR 20 VICTORY FUND
        13  FRESHMAN AGRICULTURAL REPUBLICAN MEMBERS TRUST AKA FARM TRUST
        13  REPUBLICAN PARTY OF VIRGINIA INC
        11  NRSC TARGETED STATE VICTORY
        11  ENGINEERS POLITICAL EDUCATION COMMITTEE (EPEC)/INTERNATIONAL UNION OF 
        11  DNC STATE PARTY VICTORY FUND

C6 by rows
      6.2K  WASHINGTON
      1.8K  ALEXANDRIA
       933  NEW YORK
       780  ARLINGTON
       629  HOUSTON
       629  LOS ANGELES
       570  CHICAGO
       556  BETHESDA
       530  SACRAMENTO
       484  AUSTIN
       473  LAS VEGAS
       472  ATHENS
       470  COLUMBUS
       428  PHOENIX
       403  HUDSON
       390  DALLAS
       386  RALEIGH
       376  ATLANTA
       350  SEATTLE
       338  DENVER

## who x when

C4 by _INGESTED_AT  LOAD STAMP, not an event date
  122 C STREET NW                           2026:108
  1742 WOODBEND DR                          2026:134
  228 S WASHINGTON ST STE 115               2026:107
  228 S. WASHINGTON ST.                     2026:183
  600 PENNSYLVANIA AVE SE                   2026:157
  600 PENNSYLVANIA AVE SE #15180            2026:107
  610 S. BOULEVARD                          2026:113
  611 PENNSYLVANIA AVE SE                   2026:220
  824 S MILLEDGE AVE STE 101                2026:300
  918 PENNSYLVANIA AVE SE                   2026:235
  C/O BULLDOG COMPLIANCE                    2026:127
  C/O RED CURVE SOLUTIONS                   2026:109
  PO BOX 15320                              2026:176
  PO BOX 183                                2026:322
  PO BOX 26141                              2026:327
  PO BOX 30844                              2026:471
  PO BOX 33079                              2026:96
  PO BOX 65322                              2026:98
  PO BOX 97275                              2026:101
  PO BOX 9891                               2026:282

C3 by _INGESTED_AT  LOAD STAMP, not an event date
  CURTIS, ELIZABETH                         2026:210
  DATWYLER, THOMAS                          2026:660
  GANTT, CHARLES                            2026:154
  GLAZE, KAYLA                              2026:164
  HOBBS, CABELL                             2026:310
  JACKSON, SUE                              2026:184
  KILGORE, PAUL                             2026:609
  KYRIACOPOULOS, JANICA                     2026:251
  LISKER, LISA                              2026:452
  MARSTON, CHRIS                            2026:367
  MARTIN, STEVEN                            2026:385
  MAY, JENNIFER                             2026:301
  MELE, STEVEN                              2026:162
  OTTENHOFF, BENJAMIN                       2026:143
  PETTERSON, JAY                            2026:311
  PHILLIPS, ROBERT III                      2026:156
  SATTERFIELD, DAVID                        2026:182
  WATKINS, NANCY H.                         2026:148
  WILLIAMSON, LES                           2026:161
  ZAMORE, JUDITH                            2026:266

## where

C7: DC 6.3K, CA 6.3K, VA 4.4K, TX 3.8K, NY 3.1K, FL 3.1K, OH 1.9K, GA 1.9K, PA 1.9K, IL 1.7K, MD 1.7K, NC 1.6K

## what

C9: U 43%, P 38%, J 7%, B 6%, D 4%, A 2%, H 0%

C10: H 30%, N 19%, Q 14%, O 13%, S 6%, P 6%, I 3%, V 3%, X 2%, Y 1%, C 1%, U 1%

C12: Q 49%, T 23%, A 19%, M 9%, D 0%

C13: C 53%, T 21%, M 11%, L 10%, W 3%, V 1%, I 0%, H 0%, NONE 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C1 | other | 37.9K | 0 | C00658310 301; C00730127 301; C00891747 301; C00165324 301 |
| C2 | other | 38.3K | 11 | ROBERT BARR FOR CONGRESS 301; MATT CONNOLLY FOR PA-07 301; WIN WITH BLACK MEN CIVIC  301; PHILADELPHIA JOINT BOARD  301 |
| C3 | who | 30.4K | 2.1K | DATWYLER, THOMAS 660; KILGORE, PAUL 609; LISKER, LISA 452; MARTIN, STEVEN 389 |
| C4 | who | 30.8K | 38 | PO BOX 30844 475; PO BOX 183 332; PO BOX 26141 328; 824 S MILLEDGE AVE STE 10 305 |
| C5 | who | 4.7K | 45.4K | SUITE 300 246; STE. 115 224; SUITE 200 216; SUITE 600 203 |
| C6 | who | 5.6K | 33 | WASHINGTON 6.2K; ALEXANDRIA 1.8K; NEW YORK 933; ARLINGTON 780 |
| C7 | state | 68 | 31 | DC 6.3K; CA 6.3K; VA 4.4K; TX 3.8K |
| C8 | other | 13.6K | 50 | 20003 1.7K; 22314 1.1K; 20005 816; 20001 677 |
| C9 | category | 8 | 32 | U 25.7K; P 22.9K; J 4.0K; B 3.9K |
| C10 | category | 17 | 28 | H 17.7K; N 11.3K; Q 8.2K; O 8.0K |
| C11 | other | 180 | 33.0K | REP 10.7K; DEM 10.4K; IND 1.7K; LIB 756 |
| C12 | category | 6 | 2 | Q 29.6K; T 13.6K; A 11.1K; M 5.7K |
| C13 | category | 10 | 51.6K | C 4.5K; T 1.8K; M 893; L 863 |
| C14 | who | 5.9K | 34.2K | NONE 16.8K; TAKE BACK THE HOUSE 2022 89; CALIFORNIA REPUBLICAN PAR 48; DOLLARS FOR DEMOCRATS 47 |
| C15 | other | 14.5K | 36.1K | H4PA17141 121; H2UT01292 121; P40002214 121; H4AZ03117 121 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-24 02:10:52.000 60.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | d6dc3557-b6c2-48b0-b2d9-e 60.0K |
| _SRC_SHA256 | who | 1 | 0 | manifest:4:cm24.zip 60.0K |
