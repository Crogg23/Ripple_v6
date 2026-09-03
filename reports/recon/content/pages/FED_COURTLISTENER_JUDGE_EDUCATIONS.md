# FED_COURTLISTENER_JUDGE_EDUCATIONS

rows 12.8K  columns 11  scan 3.5s

roles: audit 2, category 1, date 3, id 1, other 3, who 2

## when

DATE_CREATED
  2016      6.6K  ##############################
  2017         7  
  2018         1  
  2019       307  #
  2020        17  
  2021        28  
  2022      5.8K  ###########################
  2023        12  

DATE_MODIFIED
  2016      6.6K  ##############################
  2017         7  
  2018         1  
  2019       305  #
  2020        19  
  2021        28  
  2022      5.8K  ###########################
  2023        12  

_INGESTED_AT
  2026     12.8K  ##############################

## who

DEGREE_DETAIL by rows
      1.0K  B.A.
       547  J.D.
       538  A.B.
       410  LL.B.
       261  B.S.
       110  Political Science
       100  cum laude
        93  Business Administration
        89  magna cum laude
        81  M.A.
        43  B.B.A.
        42  Economics
        37  summa cum laude
        36  with honors
        35  A.M.
        32  LL.M.
        29  History
        26  Criminal Justice
        26  English
        25  Ph.B.

_SRC_SHA256 by rows
     12.8K  e84c16d8a0e975cd6b70101aecf2a1338e5efebd7ce60f90c785b7e25156f69d

## who x when

DEGREE_DETAIL by DATE_CREATED
  A.B.                                      2016:529 2019:7 2021:1 2022:1
  A.M.                                      2016:35
  B.A.                                      2016:918 2019:83 2021:13
  B.B.A.                                    2016:36 2019:7
  B.S.                                      2016:238 2019:23
  Business Administration                   2022:93
  Criminal Justice                          2022:26
  Economics                                 2022:42
  English                                   2022:26
  History                                   2022:29
  J.D.                                      2016:413 2018:1 2019:124 2021:9
  LL.B.                                     2016:409 2022:1
  LL.M.                                     2016:28 2019:4
  M.A.                                      2016:78 2019:3
  Ph.B.                                     2016:25
  Political Science                         2016:3 2019:1 2022:106
  cum laude                                 2016:3 2019:1 2022:96
  magna cum laude                           2016:2 2022:87
  summa cum laude                           2022:37
  with honors                               2022:36

_SRC_SHA256 by DATE_CREATED
  e84c16d8a0e975cd6b70101aecf2a1338e5efebd  2016:6.6K 2017:7 2018:1 2019:307 2020:17 2021:28 2022:5.8K 2023:12

## what

DEGREE_LEVEL: ba 51%, jd 41%, llb 4%, ma 3%, llm 1%, aa 0%, mba 0%, cert 0%, phd 0%, jsd 0%, md 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 12.8K | 0 | 12855 64; 12854 64; 12853 64; 12852 64 |
| DATE_CREATED | date | 12.7K | 0 | 2022-08-09 23:34:19.35043 64; 2022-08-09 23:34:19.34557 64; 2022-08-09 23:26:50.40318 64; 2022-08-09 23:13:44.67699 64 |
| DATE_MODIFIED | date | 12.9K | 0 | 2022-08-09 23:34:19.35045 64; 2022-08-09 23:34:19.34558 64; 2022-08-09 23:26:50.40319 64; 2022-08-09 23:13:44.67700 64 |
| DEGREE_LEVEL | category | 11 | 263 | ba 6.4K; jd 5.2K; llb 444; ma 340 |
| DEGREE_DETAIL | who | 525 | 8.3K | B.A. 1.0K; J.D. 547; A.B. 538; LL.B. 410 |
| DEGREE_YEAR | other | 230 | 4.9K | 1981 225; 1982 223; 1979 221; 1986 218 |
| PERSON_ID | other | 7.3K | 31 | 16202 66; 16198 66; 16197 66; 8392 66 |
| SCHOOL_ID | other | 906 | 0 | 860 833; 3832 479; 3094 294; 5618 272 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:07.435 12.8K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 93fcdc89-26d2-4929-acde-8 12.8K |
| _SRC_SHA256 | who | 1 | 0 | e84c16d8a0e975cd6b70101ae 12.8K |
