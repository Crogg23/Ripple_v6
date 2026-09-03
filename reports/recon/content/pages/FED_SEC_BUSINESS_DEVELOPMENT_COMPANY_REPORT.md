# FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT

rows 212  columns 13  scan 2.9s

roles: audit 2, category 1, date 1, other 5, state 1, who 3

## when

FILING_DATE
  2000         4  #
  2001         2  
  2003         1  
  2004         5  #
  2006         2  
  2007         2  
  2009         2  
  2013         1  
  2014         2  
  2015         6  #
  2016         3  #
  2017         3  #
  2018         2  
  2019         1  
  2020         1  
  2022         2  
  2023         3  #
  2024         2  
  2025         4  #
  2026       163  ##############################

## who

REGISTRANT_NAME by rows
         1  T Series BDC LLC
         1  RAND CAPITAL CORP
         1  CION Investment Corp
         1  Goldman Sachs BDC, Inc.
         1  Superior Community Capital CORP
         1  Silver Capital Holdings LLC
         1  Morgan Stanley Direct Lending Fund
         1  Chicago Atlantic BDC, Inc.
         1  Barings Capital Investment Corp
         1  Kayne DL 2021, Inc.
         1  OHA Senior Private Lending Fund (U) LLC
         1  Altmore BDC, Inc.
         1  Stone Point Credit Corp
         1  Muzinich BDC, Inc.
         1  TRIANGLE MEZZANINE FUND LLLP
         1  WESTFORD TECHNOLOGY VENTURES LP
         1  TPG Twin Brook Capital Income Fund
         1  Hercules Energy Technology & Resource Management, Inc.
         1  BlackRock TCP Capital Corp.
         1  Oaktree Specialty Lending Corp

CITY by rows
        95  NEW YORK
        11  LOS ANGELES
        10  BOSTON
        10  CHICAGO
         9  HOUSTON
         5  CHARLOTTE
         5  GREENWICH
         4  DALLAS
         3  SANTA MONICA
         3  PORTOLA VALLEY
         3  SAN FRANCISCO
         2  NEWARK
         2  WEST PALM BEACH
         2  MARION
         2  Miami
         2  MCLEAN
         2  MENLO PARK
         2  FAIRHOPE
         2  MAITLAND
         2  AUSTIN

_SRC_SHA256 by rows
       212  e90392f2182482392d8145a3fdceeb74f3c4fc8c9d46bee671df5ac113161e51

## who x when

REGISTRANT_NAME by FILING_DATE
  Altmore BDC, Inc.                         2022:1
  Barings Capital Investment Corp           2026:1
  BlackRock TCP Capital Corp.               2026:1
  CION Investment Corp                      2026:1
  Chicago Atlantic BDC, Inc.                2026:1
  Goldman Sachs BDC, Inc.                   2026:1
  Hercules Energy Technology & Resource Ma  2014:1
  Kayne DL 2021, Inc.                       2026:1
  Morgan Stanley Direct Lending Fund        2026:1
  Muzinich BDC, Inc.                        2026:1
  OHA Senior Private Lending Fund (U) LLC   2026:1
  Oaktree Specialty Lending Corp            2026:1
  RAND CAPITAL CORP                         2026:1
  Silver Capital Holdings LLC               2026:1
  Stone Point Credit Corp                   2026:1
  Superior Community Capital CORP           2006:1
  T Series BDC LLC                          2026:1
  TPG Twin Brook Capital Income Fund        2026:1
  TRIANGLE MEZZANINE FUND LLLP              2018:1
  WESTFORD TECHNOLOGY VENTURES LP           2004:1

CITY by FILING_DATE
  AUSTIN                                    2026:2
  BOSTON                                    2004:1 2017:1 2018:1 2026:7
  CHARLOTTE                                 2016:2 2026:3
  CHICAGO                                   2025:1 2026:9
  DALLAS                                    2020:1 2026:3
  FAIRHOPE                                  2023:1 2026:1
  GREENWICH                                 2026:5
  HOUSTON                                   2000:1 2015:1 2026:7
  LOS ANGELES                               2019:1 2026:10
  MAITLAND                                  2025:1 2026:1
  MARION                                    2001:1 2009:1
  MCLEAN                                    2022:1 2026:1
  MENLO PARK                                2026:2
  Miami                                     2026:2
  NEW YORK                                  2000:2 2004:2 2006:1 2009:1 2015:1 2017:1 2022:1 2023:2 2024:1 2025:1 2026:82
  NEWARK                                    2004:1 2026:1
  PORTOLA VALLEY                            2026:3
  SAN FRANCISCO                             2000:1 2026:2
  SANTA MONICA                              2004:1 2026:2
  WEST PALM BEACH                           2026:2

## where

STATE: NY 98, CA 27, TX 17, IL 11, MA 11, FL 7, CT 6, NC 6, NJ 5, AL 3, PA 2, VA 2

## what

FILING_TYPE: 8-K 42%, 10-Q 28%, N-2/A 6%, 40-17G 6%, RW 5%, N-54A 3%, SC TO-I 2%, SCHEDULE 13G/A 2%, N-6F 2%, 424B3 1%, 15-12G 1%, POS EX 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FILE_NO | other | 213 | 0 | 814-01979 2; 814-01977 2; 814-01966 2; 814-01953 2 |
| CIK | other | 211 | 0 | 0002122354 2; 0002107577 2; 0002066811 2; 0002083477 2 |
| REGISTRANT_NAME | who | 210 | 0 | Third Point Private Capit 2; CAPQ BDC 2; TCW SPECIALTY LENDING LLC 2; APS BDC, LLC 2 |
| ADDRESS_1 | other | 154 | 0 | 1585 BROADWAY 6; 375 PARK AVENUE 5; 200 WEST STREET 5; 399 PARK AVENUE 5 |
| ADDRESS_2 | other | 77 | 98 | 48TH FLOOR 5; 9TH FLOOR 4; 25TH FLOOR 4; 51ST FLOOR 3 |
| CITY | who | 54 | 0 | NEW YORK 95; LOS ANGELES 11; CHICAGO 10; BOSTON 10 |
| STATE | state | 27 | 0 | NY 98; CA 27; TX 17; IL 11 |
| ZIP_CODE | other | 94 | 2 | 10022 26; 10019 16; 10017 11; 90071 7 |
| FILING_DATE | date | 67 | 0 | 05/29/26 20; 05/28/26 17; 05/27/26 17; 05/12/26 15 |
| FILING_TYPE | category | 40 | 0 | 8-K 74; 10-Q 49; N-2/A 11; 40-17G 10 |
| _INGESTED_AT | audit | 1 | 0 | 1785096119712663 212 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 6d3d8105-b8fa-4b30-84c2-2 212 |
| _SRC_SHA256 | who | 1 | 0 | e90392f2182482392d8145a3f 212 |
