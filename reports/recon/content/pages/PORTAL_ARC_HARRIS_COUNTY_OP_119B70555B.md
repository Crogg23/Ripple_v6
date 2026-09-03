# PORTAL_ARC_HARRIS_COUNTY_OP_119B70555B

rows 74  columns 60  scan 3.1s

roles: audit 2, category 10, date 5, empty 1, other 25, who 18

## when

USER_SCH17
  1976         1  ##
  1984         1  ##
  1987         1  ##
  1990         1  ##
  1993         1  ##
  1995         1  ##
  1997         3  #######
  1999         1  ##
  2001         1  ##
  2002         1  ##
  2005         2  #####
  2006         1  ##
  2007         1  ##
  2008         3  #######
  2009         1  ##
  2010         2  #####
  2012         1  ##
  2015         1  ##
  2016         1  ##
  2018        13  ##############################
  2019         1  ##
  2021         2  #####
  2022         1  ##

USER_UPDAT
  2024        74  ##############################

CREATIONDATE
  2026        74  ##############################

EDITDATE
  2026        74  ##############################

INGESTED_AT
  2026        74  ##############################

## who

USER_COU_1 by rows
        74  HARRIS COUNTY

USER_DISTR by rows
        74  101902

USER_DIS_1 by rows
        74  ALDINE ISD

USER_DIS_2 by rows
        74  INDEPENDENT

## who x when

USER_COU_1 by USER_UPDAT
  HARRIS COUNTY                             2024:74

USER_DISTR by USER_UPDAT
  101902                                    2024:74

## what

USER_INSTR: REGULAR INSTRUCTIONAL 96%, ALTERNATIVE INSTRUCTIONAL 3%, DAEP INSTRUCTIONAL 1%

USER_AEA: N 97%, Y 3%

USER_MAGNE: N 80%, Y 20%

USER_SCH_3: HOUSTON 92%, HUMBLE 8%

USER_SCH_5: 77088 17%, 77338 14%, 77039 11%, 77060 8%, 77067 8%, 77032 8%, 77073 6%, 77073-3301 6%, 77396 6%, 77032-3097 6%, 77086 6%, 77038-1905 6%

USER_SCH_7: HOUSTON 91%, HUMBLE 9%

USER_SCH_9: 77088 17%, 77338 14%, 77039 11%, 77060 8%, 77067 8%, 77032 8%, 77073 6%, 77073-3301 6%, 77396 6%, 77032-3097 6%, 77086 6%, 77038-1905 6%

USER_SCH13: www.aldineisd.org 97%, www.aldine.k12.tx.us 1%, www.aldine.org 1%

USER_GRADE: 01-05 47%, 06-08 15%, EE-KG 15%, 09-12 12%, 06-12 1%, 08-12 1%, EE KG-12 1%, 03-12 1%, 01-08 1%, 05-06 1%, PK-KG 1%, 01-04 1%

SCHOOL_TYP: Elementary School 65%, Middle School 16%, High School 14%, Elementary/Secondary 4%, Junior High School 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | other | 74 | 0 | 140 1; 139 1; 138 1; 137 1 |
| USER_COUNT | other | 1 | 0 | '101 74 |
| USER_COU_1 | who | 1 | 0 | HARRIS COUNTY 74 |
| USER_ESC_R | other | 1 | 0 | 04 74 |
| USER_ESC_1 | other | 1 | 0 | 04 74 |
| USER_ESC_2 | other | 1 | 0 | 04 74 |
| USER_DISTR | who | 1 | 0 | 101902 74 |
| USER_DIS_1 | who | 1 | 0 | ALDINE ISD 74 |
| USER_DIS_2 | who | 1 | 0 | INDEPENDENT 74 |
| USER_NCES | who | 1 | 0 | 4807710 74 |
| USER_DIS_3 | who | 1 | 0 | 2520 W W THORNE DR 74 |
| USER_DIS_4 | who | 1 | 0 | HOUSTON 74 |
| USER_DIS_5 | other | 1 | 0 | TX 74 |
| USER_DIS_6 | other | 1 | 0 | 77073 74 |
| USER_DIS_7 | who | 1 | 0 | 2520 W W THORNE DR 74 |
| USER_DIS_8 | who | 1 | 0 | HOUSTON 74 |
| USER_DIS_9 | other | 1 | 0 | TX 74 |
| USER_DIS10 | other | 1 | 0 | 77073 74 |
| USER_DIS11 | who | 1 | 0 | (281) 449-1011 74 |
| USER_DIS12 | who | 1 | 0 | (281) 449-4911 74 |
| USER_DIS13 | who | 1 | 0 | lmgoffney@aldineisd.org 74 |
| USER_DIS14 | who | 1 | 0 | www.aldineisd.org 74 |
| USER_DIS15 | who | 1 | 0 | DR LATONYA GOFFNEY 74 |
| USER_DIS16 | other | 1 | 0 | 57844 74 |
| USER_SCHOO | other | 75 | 0 | 101902146 1; 101902136 1; 101902045 1; 101902162 1 |
| USER_SCH_1 | other | 75 | 0 | OGDEN EL 1; CYPRESSWOOD EL 1; TEAGUE MIDDLE 1; MAGRILL EC/PK/K 1 |
| USER_INSTR | category | 3 | 0 | REGULAR INSTRUCTIONAL 71; ALTERNATIVE INSTRUCTIONAL 2; DAEP INSTRUCTIONAL 1 |
| USER_CHART | empty | 1 | 74 |  |
| USER_AEA | category | 2 | 0 | N 72; Y 2 |
| USER_MAGNE | category | 2 | 0 | N 59; Y 15 |
| USER_RESID | other | 1 | 0 | N 74 |
| USER_NCE_1 | other | 74 | 0 | 480771013692 1; 480771012216 1; 480771000087 1; 480771013786 1 |
| USER_SCH_2 | other | 74 | 0 | 11101 AIRLINE DR 2; 21919 RAYFORD RD 1; 6901 CYPRESSWOOD POINT AV 1; 21700 RAYFORD RD 1 |
| USER_SCH_3 | category | 2 | 0 | HOUSTON 68; HUMBLE 6 |
| USER_SCH_4 | other | 1 | 0 | TX 74 |
| USER_SCH_5 | category | 48 | 0 | 77088 6; 77338 5; 77039 4; 77060 3 |
| USER_SCH_6 | other | 74 | 0 | 11101 AIRLINE DR 2; 21919 RAYFORD RD 1; 6901 CYPRESSWOOD POINT AV 1; 21700 RAYFORD RD 1 |
| USER_SCH_7 | category | 2 | 0 | HOUSTON 67; HUMBLE 7 |
| USER_SCH_8 | other | 1 | 0 | TX 74 |
| USER_SCH_9 | category | 48 | 0 | 77088 6; 77338 5; 77039 4; 77060 3 |
| USER_SCH10 | other | 74 | 0 | (281) 233-8901 1; (281) 227-3370 1; (281) 233-4310 1; (281) 233-4300 1 |
| USER_SCH11 | other | 67 | 3 | (281) 985-7139 3; (281) 878-1536 2; (555) 555-1212 2; (281) 233-8907 1 |
| USER_SCH12 | other | 74 | 0 | jfwhite@aldineisd.org 1; GTJohnson@aldineisd.org 1; gwschattle@aldineisd.org 1; MKMalo@aldineisd.org 1 |
| USER_SCH13 | category | 4 | 3 | www.aldineisd.org 69; www.aldine.k12.tx.us 1; www.aldine.org 1 |
| USER_SCH14 | other | 75 | 0 | JOYELLE WHITE 1; GUY TRENT JOHNSON 1; GERALD SCHATTLE 1; MARK K MALO 1 |
| USER_GRADE | category | 13 | 0 | 01-05 34; 06-08 11; EE-KG 11; 09-12 9 |
| USER_SCH15 | other | 70 | 0 | 571 2; 747 2; 531 2; 518 2 |
| USER_SCH16 | who | 1 | 0 | Active 74 |
| USER_SCH17 | date | 27 | 32 | 07/03/2018 8; 08/16/2018 4; 08/18/2008 3; 04/07/1997 3 |
| USER_UPDAT | date | 1 | 0 | 3/14/2024 5:38:21 AM 74 |
| SCHOOL_TYP | category | 5 | 0 | Elementary School 48; Middle School 12; High School 10; Elementary/Secondary 3 |
| GLOBALID | other | 75 | 0 | 93bdd182-bd16-4e5c-8743-d 1; 3c77f09c-65cb-475c-ba5c-d 1; 7bbb775e-5db3-4b3f-a0aa-3 1; b88197a0-8430-4294-bbe3-c 1 |
| CREATIONDATE | date | 1 | 0 | 1775741499678 74 |
| CREATOR | who | 1 | 0 | JGuerraPct2 74 |
| EDITDATE | date | 1 | 0 | 1775741499678 74 |
| EDITOR | who | 1 | 0 | JGuerraPct2 74 |
| GEOMETRY | other | 74 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:42.60750 74 |
| SOURCE_RUN_ID | audit | 1 | 0 | a5af21da-0cac-44ec-af77-e 74 |
| SRC_SHA256 | who | 1 | 0 | 1f51552eedb4f979a13c6d8e3 74 |
