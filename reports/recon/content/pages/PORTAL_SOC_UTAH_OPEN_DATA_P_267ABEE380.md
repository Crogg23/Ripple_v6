# PORTAL_SOC_UTAH_OPEN_DATA_P_267ABEE380

rows 1.1K  columns 14  scan 2.5s

roles: audit 2, category 6, date 1, other 3, who 3

## when

INGESTED_AT
  2026      1.1K  ##############################

## who

EMPLOYER by rows
        10  INTERMOUNTAIN HEALTHCARE
         8  NITYA SOFTWARE SOLUTIONS INC
         8  USANA HEALTH SCIENCES INC
         7  ALTIUS TECHNOLOGIES INC
         7  ANCESTRY COM OPERATIONS INC
         7  BOART LONGYEAR
         6  UNIVERSITY OF UTAH
         6  QUALTRICS LLC
         6  SONUS SOFTWARE SOLUTIONS INC
         5  DAVIS SCHOOL DISTRICT
         5  WORKFRONT INC
         5  CONNVERTEX TECHNOLOGIES INC
         5  CONSULTNET LLC
         5  INMOMENT INC
         5  UTAH VALLEY UNIVERSITY
         5  INCONTACT INC
         5  VIVINT INC
         4  ZB NA DBA ZIONS BANK
         4  GALILEO PROCESSING INC
         4  FATPIPE TECHNOLOGIES INC

CITY by rows
       431  SALT LAKE CITY
        88  PROVO
        73  LEHI
        72  SOUTH JORDAN
        55  SANDY
        49  DRAPER
        43  OREM
        31  MIDVALE
        28  OGDEN
        24  WEST VALLEY CITY
        19  MURRAY
        18  AMERICAN FORK
        17  PARK CITY
        15  PLEASANT GROVE
        15  LINDON
        15  LOGAN
        12  SAINT GEORGE
        10  WEST JORDAN
        10  FARMINGTON
         9  CEDAR CITY

SRC_SHA256 by rows
      1.1K  6bbde358aa5151e034db32e9cdb957ede676de2eda695cd62a7f6ec60fbd8455

## who x when

EMPLOYER by INGESTED_AT  LOAD STAMP, not an event date
  ALTIUS TECHNOLOGIES INC                   2026:7
  ANCESTRY COM OPERATIONS INC               2026:7
  BOART LONGYEAR                            2026:7
  CONNVERTEX TECHNOLOGIES INC               2026:5
  CONSULTNET LLC                            2026:5
  DAVIS SCHOOL DISTRICT                     2026:5
  FATPIPE TECHNOLOGIES INC                  2026:4
  GALILEO PROCESSING INC                    2026:4
  INCONTACT INC                             2026:5
  INMOMENT INC                              2026:5
  INTERMOUNTAIN HEALTHCARE                  2026:10
  NITYA SOFTWARE SOLUTIONS INC              2026:8
  QUALTRICS LLC                             2026:6
  SONUS SOFTWARE SOLUTIONS INC              2026:6
  UNIVERSITY OF UTAH                        2026:6
  USANA HEALTH SCIENCES INC                 2026:8
  UTAH VALLEY UNIVERSITY                    2026:5
  VIVINT INC                                2026:5
  WORKFRONT INC                             2026:5
  ZB NA DBA ZIONS BANK                      2026:4

CITY by INGESTED_AT  LOAD STAMP, not an event date
  AMERICAN FORK                             2026:18
  CEDAR CITY                                2026:9
  DRAPER                                    2026:49
  FARMINGTON                                2026:10
  LEHI                                      2026:73
  LINDON                                    2026:15
  LOGAN                                     2026:15
  MIDVALE                                   2026:31
  MURRAY                                    2026:19
  OGDEN                                     2026:28
  OREM                                      2026:43
  PARK CITY                                 2026:17
  PLEASANT GROVE                            2026:15
  PROVO                                     2026:88
  SAINT GEORGE                              2026:12
  SALT LAKE CITY                            2026:431
  SANDY                                     2026:55
  SOUTH JORDAN                              2026:72
  WEST JORDAN                               2026:10
  WEST VALLEY CITY                          2026:24

## what

FISCAL_YEAR: 2018 27%, 2016 25%, 2019 25%, 2017 23%

INITIAL_APPROVALS: 0 52%, 1 36%, 2 6%, 3 2%, 4 2%, 5 1%, 6 1%, 8 0%, 12 0%, 13 0%, 9 0%, 11 0%

INITIAL_DENIALS: 0 90%, 1 9%, 2 1%, 4 0%, 6 0%, 8 0%, 3 0%, 12 0%, 10 0%

CONTINUING_APPROVALS: 1 43%, 0 39%, 2 8%, 3 4%, 4 2%, 6 1%, 5 1%, 10 1%, 14 0%, 7 0%, 8 0%, 18 0%

CONTINUING_DENIALS: 0 92%, 1 6%, 2 1%, 3 0%, 4 0%, 6 0%, 10 0%, 8 0%

NAICS: Scientific & Technical Svcs 38%, Education 13%, Industrial, Mining, Metal Manu 11%, Information 9%, Finance & Insurance 7%, Health Care 6%, Other Services 4%, Retail Trade 4%, Management of Companies 2%, Utilities 2%, Wholesale Trade 2%, Ag Manufacturing 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | category | 4 | 0 | 2018 305; 2016 287; 2019 280; 2017 267 |
| EMPLOYER | who | 756 | 0 | INTERMOUNTAIN HEALTHCARE 13; UNIVERSITY OF UTAH 10; NITYA SOFTWARE SOLUTIONS  10; UTAH VALLEY UNIVERSITY 9 |
| INITIAL_APPROVALS | category | 24 | 0 | 0 585; 1 401; 2 63; 3 21 |
| INITIAL_DENIALS | category | 9 | 0 | 0 1.0K; 1 97; 2 6; 4 2 |
| CONTINUING_APPROVALS | category | 32 | 0 | 1 480; 0 431; 2 88; 3 41 |
| CONTINUING_DENIALS | category | 8 | 0 | 0 1.0K; 1 70; 2 10; 3 4 |
| NAICS | category | 21 | 0 | Scientific & Technical Sv 393; Education 131; Industrial, Mining, Metal 114; Information 89 |
| TAX_ID | other | 625 | 2 | 4057 13; 525 13; 9820 9; 3206 9 |
| STATE | other | 1 | 0 | UT 1.1K |
| CITY | who | 66 | 0 | SALT LAKE CITY 431; PROVO 88; LEHI 73; SOUTH JORDAN 72 |
| ZIP | other | 102 | 0 | 84043 72; 84095 62; 84101 59; 84111 52 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-27 03:48:53.49069 1.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3b216ac0-ebb8-4318-b0f3-4 1.1K |
| SRC_SHA256 | who | 1 | 0 | 6bbde358aa5151e034db32e9c 1.1K |
