# PORTAL_CKA_IRELAND_NATIONAL_7B813F1D72

rows 3.1K  columns 14  scan 5.9s

roles: amount 5, audit 2, category 3, date 1, id 1, who 3

## when

INGESTED_AT
  2026      3.1K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SET_HOURS_26_27 | 3.1K | 5 | 57.50 | 310 | 525 | 247.1K |
| SET_POSTS__26_27 | 3.1K | 0.20 | 2.30 | 12.40 | 21 | 9.9K |
| MAINSTREAM_SNA_ALLOCATION__26_27 | 3.1K | 0 | 2.83 | 12.80 | 22 | 10.5K |
| SPECIAL_CLASS_SNAS__26_27 | 1.5K | 0 | 3.83 | 10.13 | 20.16 | 5.5K |
| TOTAL_SNA_ALLOCATION_26_27 | 3.1K | 0 | 4 | 19 | 42.16 | 16.0K |

## who

SCHOOL_NAME by rows
        49  Scoil Mhuire
        17  Scoil Bhride
        12  SN Mhuire
        10  St Patricks NS
         9  S N Mhuire
         8  Scoil Naomh Mhuire
         7  Scoil Iosagain
         7  St Josephs NS
         7  St Marys NS
         6  St Brigid's NS
         6  S N Muire Gan Smal
         6  St Mary's NS
         6  SN Naomh Padraig
         6  St. Patrick's NS
         6  Scoil Bhríde
         6  St. Joseph's NS
         5  S N Naomh Padraig
         5  S N Padraig Naofa
         5  Scoil Eoin
         5  St Marys N S

SCHOOL_NAME by dollars
      213.26       49 rows  Scoil Mhuire
      102.14        7 rows  Scoil Iosagain
      101.43       17 rows  Scoil Bhride
       57.98        5 rows  Scoil Na Mbraithre
       52.28       12 rows  SN Mhuire
       46.49        4 rows  Holy Family NS
       45.56        6 rows  St Brigid's NS
       44.16        8 rows  Scoil Naomh Mhuire
       43.90        2 rows  Scoil Naomh Pádraig
       43.46       10 rows  St Patricks NS
       40.07        5 rows  Scoil Eoin
       38.41        9 rows  S N Mhuire
       38.23        7 rows  St Josephs NS
       36.64        6 rows  Scoil Bhríde
       36.13        1 rows  Trinity Primary School
       35.15        6 rows  St Mary's NS
       35.15        2 rows  Sacred Heart N S
       34.70        2 rows  Holy Family Primary School
       33.82        4 rows  St Josephs N S
       33.79        3 rows  Presentation Primary

SCHOOL_TYPE by rows
      3.1K  Primary

SCHOOL_TYPE by dollars
       16.0K     3.1K rows  Primary

SRC_SHA256 by rows
      3.1K  2a4618d3ae0a64c3a848e725c497d389d08b84bcb222dbe422334bec847406e0

SRC_SHA256 by dollars
       16.0K     3.1K rows  2a4618d3ae0a64c3a848e725c497d389d08b84bcb222dbe422334bec8474

## who x when

SCHOOL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_SNA_ALLOCATION_26_27
  Holy Family NS                            2026:46.49
  Holy Family Primary School                2026:34.70
  Presentation Primary                      2026:33.79
  S N Mhuire                                2026:38.41
  S N Muire Gan Smal                        2026:9.83
  S N Naomh Padraig                         2026:7.50
  S N Padraig Naofa                         2026:16.99
  SN Mhuire                                 2026:52.28
  SN Naomh Padraig                          2026:16.98
  Sacred Heart N S                          2026:35.15
  Scoil Bhride                              2026:101.43
  Scoil Bhríde                              2026:36.64
  Scoil Eoin                                2026:40.07
  Scoil Iosagain                            2026:102.14
  Scoil Mhuire                              2026:213.26
  Scoil Na Mbraithre                        2026:57.98
  Scoil Naomh Mhuire                        2026:44.16
  Scoil Naomh Pádraig                       2026:43.90
  St Brigid's NS                            2026:45.56
  St Josephs N S                            2026:33.82
  St Josephs NS                             2026:38.23
  St Mary's NS                              2026:35.15
  St Marys N S                              2026:25.99
  St Marys NS                               2026:30.81
  St Patricks NS                            2026:43.46
  St. Joseph's NS                           2026:17.74
  St. Patrick's NS                          2026:24.66
  Trinity Primary School                    2026:36.13

SCHOOL_TYPE by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_SNA_ALLOCATION_26_27
  Primary                                   2026:16.0K

## what

COUNTY: Dublin 21%, Cork 15%, Galway 10%, Donegal 8%, Tipperary 7%, Mayo 7%, Limerick 6%, Kerry 6%, Meath 5%, Clare 5%, Wexford 5%, Kildare 5%

DUBLIN_AREA_CODES: Dublin County 34%, Dublin 24 11%, Dublin 15 9%, Dublin 5 8%, Dublin 9 6%, Dublin 11 6%, Dublin 7 6%, Dublin 22 5%, Dublin 13 5%, Dublin 12 5%, Dublin 16 5%

SPECIAL_CLASS_TEACHING_POSTS__26_27: 2 43%, 1 34%, 3 12%, 4 4%, 5 4%, 0 2%, 6 1%, 7 0%, 10 0%, 9 0%, 11 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTY | category | 26 | 0 | Dublin 459; Cork 332; Galway 216; Donegal 169 |
| DUBLIN_AREA_CODES | category | 24 | 2.6K | Dublin County 119; Dublin 24 37; Dublin 15 32; Dublin 5 26 |
| ROLL_NUMBER | id | 3.1K | 0 | 20606B 16; 20605W 16; 20604U 16; 20603S 16 |
| SCHOOL_TYPE | who | 1 | 0 | Primary 3.1K |
| SCHOOL_NAME | who | 2.8K | 0 | Scoil Mhuire 50; Scoil Bhride 17; Scoil Náisiúnta Chill Dá  16; Scoil Naomh Pádraig 16 |
| SET_HOURS_26_27 | amount | 142 | 1 | 25.0 133; 20.0 105; 30.0 101; 32.5 93 |
| SET_POSTS__26_27 | amount | 140 | 1 | 1.0 133; 0.8 105; 1.2 101; 1.3 93 |
| SPECIAL_CLASS_TEACHING_POSTS__26_27 | category | 13 | 1.6K | 2 635; 1 514; 3 176; 4 59 |
| MAINSTREAM_SNA_ALLOCATION__26_27 | amount | 216 | 0 | 1.0 429; 2.0 287; 1.5 172; 1.83 160 |
| SPECIAL_CLASS_SNAS__26_27 | amount | 96 | 1.6K | 4.0 379; 2.0 338; 3.66 86; 3.83 85 |
| TOTAL_SNA_ALLOCATION_26_27 | amount | 310 | 0 | 1.0 380; 2.0 201; 1.5 138; 1.83 111 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:29:36.94303 3.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | e82aa6a2-8e3c-4ec2-bbd0-4 3.1K |
| SRC_SHA256 | who | 1 | 0 | 2a4618d3ae0a64c3a848e725c 3.1K |
