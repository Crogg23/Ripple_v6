# PORTAL_ARC_TN_DATA_TENNESSE_B3E1127384

rows 2.0K  columns 27  scan 4.2s

roles: audit 2, category 5, date 1, empty 3, id 1, other 11, who 5

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

DISTRICT by rows
       206  SHELBY COUNTY
       163  DAVIDSON COUNTY
        92  KNOX COUNTY
        81  HAMILTON COUNTY
        49  RUTHERFORD COUNTY
        49  SUMNER COUNTY
        47  WILLIAMSON COUNTY
        41  MONTGOMERY COUNTY
        31  SEVIER COUNTY
        30  ACHIEVEMENT SCHOOL DISTRICT
        25  MADISON COUNTY
        24  WILSON COUNTY
        23  BLOUNT COUNTY
        23  PUTNAM COUNTY
        23  ROBERTSON COUNTY
        23  SULLIVAN COUNTY
        21  MAURY COUNTY
        20  HAMBLEN COUNTY
        20  HAWKINS COUNTY
        19  ROANE COUNTY

GRADE_LEVELS by rows
       312  9,10,11,12
       259  PK,K,1,2,3,4,5
       209  6,7,8
       194  K,1,2,3,4,5
       176  K,1,2,3,4,5,6,7,8,9,10,11,12
        99  PK,K,1,2,3,4
        90  5,6,7,8
        79  PK,K,1,2,3,4,5,6,7,8
        56  K,1,2,3,4,5,6,7,8
        44  K,1,2,3,4
        37  6,7,8,9,10,11,12
        30  P4,P3,K,1,2,3,4,5
        23  P4,K,1,2,3,4,5,6,7,8
        22  K,1,2,3,4,5,6
        22  P4,P3,K,1,2,3,4,5,6,7,8
        21  PK,K,1,2,3,4,5,6
        20  3,4,5
        19  PK,K,1,2
        18  PK,K,1,2,3,4,5,6,7,8,9,10,11,12
        18  7,8,9,10,11,12

CITY by rows
       218  Memphis
       122  Nashville
        80  Knoxville
        49  Chattanooga
        38  Clarksville
        33  Murfreesboro
        28  Cleveland
        25  Maryville
        24  Jackson
        24  Kingsport
        22  Franklin
        21  Antioch
        17  Lebanon
        17  Morristown
        17  Hendersonville
        17  Sevierville
        17  Johnson City
        17  Elizabethton
        16  Greeneville
        16  Cookeville

ZIPCODE by rows
      1.8K  nan
         4  38001.0
         4  38242.0
         4  37321.0
         4  37857.0
         4  37303.0
         4  37821.0
         4  37803.0
         4  37643.0
         4  38351.0
         3  37716.0
         2  37110.0
         2  38382.0
         2  38583.0
         2  37040.0
         2  37087.0
         2  37620.0
         2  38324.0
         2  37841.0
         2  38551.0

## who x when

DISTRICT by INGESTED_AT  LOAD STAMP, not an event date
  ACHIEVEMENT SCHOOL DISTRICT               2026:30
  BLOUNT COUNTY                             2026:23
  DAVIDSON COUNTY                           2026:163
  HAMBLEN COUNTY                            2026:20
  HAMILTON COUNTY                           2026:81
  HAWKINS COUNTY                            2026:20
  KNOX COUNTY                               2026:92
  MADISON COUNTY                            2026:25
  MAURY COUNTY                              2026:21
  MONTGOMERY COUNTY                         2026:41
  PUTNAM COUNTY                             2026:23
  ROANE COUNTY                              2026:19
  ROBERTSON COUNTY                          2026:23
  RUTHERFORD COUNTY                         2026:49
  SEVIER COUNTY                             2026:31
  SHELBY COUNTY                             2026:206
  SULLIVAN COUNTY                           2026:23
  SUMNER COUNTY                             2026:49
  WILLIAMSON COUNTY                         2026:47
  WILSON COUNTY                             2026:24

GRADE_LEVELS by INGESTED_AT  LOAD STAMP, not an event date
  3,4,5                                     2026:20
  5,6,7,8                                   2026:90
  6,7,8                                     2026:209
  6,7,8,9,10,11,12                          2026:37
  7,8,9,10,11,12                            2026:18
  9,10,11,12                                2026:312
  K,1,2,3,4                                 2026:44
  K,1,2,3,4,5                               2026:194
  K,1,2,3,4,5,6                             2026:22
  K,1,2,3,4,5,6,7,8                         2026:56
  K,1,2,3,4,5,6,7,8,9,10,11,12              2026:176
  P4,K,1,2,3,4,5,6,7,8                      2026:23
  P4,P3,K,1,2,3,4,5                         2026:30
  P4,P3,K,1,2,3,4,5,6,7,8                   2026:22
  PK,K,1,2                                  2026:19
  PK,K,1,2,3,4                              2026:99
  PK,K,1,2,3,4,5                            2026:259
  PK,K,1,2,3,4,5,6                          2026:21
  PK,K,1,2,3,4,5,6,7,8                      2026:79
  PK,K,1,2,3,4,5,6,7,8,9,10,11,12           2026:18

## what

REGION: MID CUMBERLAND CORE REGIONAL O 24%, SOUTHWEST CORE REGIONAL OFFICE 19%, EAST TENNESSEE CORE REGIONAL O 17%, FIRST TENNESSEE CORE REGIONAL  10%, SOUTHEAST TENNESSEE CORE REGIO 8%, UPPER CUMBERLAND CORE REGIONAL 7%, SOUTH CENTRAL CORE REGIONAL OF 7%, NORTHWEST TENNESSEE CORE REGIO 6%, SOUTH EAST TENNESSEE CORE REGI 1%, SOUTH WEST/MEMPHIS CORE REGION 1%, STATE AGENCIES/SPECIAL SCHOOLS 0%

STATUS: M 88%, A 8%, T 4%, U 0%

ADDRESS2: nan 99%, Suite A 0%, Suite 300 0%, Suite 505 0%, Po Box 4819 0%, Po Box 37 0%, Po Box 445 0%, Box 10 0%, Po Box 469 0%, Box 488 0%, Po Box 220 0%, Po Box 1507 0%

STATE: TN 100%, nan 0%

CATEGORIES: nan 99%, 4 0%, 1 0%, 2 0%, 3,4 0%, 1,3,4 0%, 2,3 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| REGION | category | 11 | 0 | MID CUMBERLAND CORE REGIO 479; SOUTHWEST CORE REGIONAL O 377; EAST TENNESSEE CORE REGIO 331; FIRST TENNESSEE CORE REGI 203 |
| DISTRICT_NO | other | 155 | 0 | 00792 206; 00190 163; 00470 92; 00330 81 |
| DISTRICT | who | 155 | 0 | SHELBY COUNTY 206; DAVIDSON COUNTY 163; KNOX COUNTY 92; HAMILTON COUNTY 81 |
| SCHOOL_NO | other | 514 | 0 | 0981 82; 0975 80; 0005 79; 0015 75 |
| NCES_SCHOOL_NUMBER | other | 1.8K | 39 | nan 162; 470140000423 10; 470123000383 10; 470042000138 10 |
| SCHOOL | other | 1.8K | 0 | Home School 82; Homebound 80; Woodland Elementary 12; Westside Elementary 12 |
| EMAIL | other | 1.8K | 0 | nan 164; evefirstclass@earthlink.n 11; henry.johnson@mnps.org 11; agathosschool@bellsouth.n 10 |
| TITLE | other | 1.9K | 0 | Principal:  148; Principal: Henry Johnson 11; Principal: Walter Turner 10; Principal: Dr. Robert J.  10 |
| STATUS | category | 4 | 0 | M 1.8K; A 162; T 87; U 1 |
| ADDRESS | other | 1.9K | 0 | 1224 Chelsea AVE 10; 809 Percy Warner BLVD 10; 1201 Mapleash AVE 10; 2921 Sevierville RD 10 |
| ADDRESS2 | category | 27 | 0 | nan 2.0K; Suite A 3; Suite 300 2; Suite 505 2 |
| ADDRESS3 | empty | 1 | 2.0K |  |
| ADDRESS4 | empty | 1 | 2.0K |  |
| CITY | who | 386 | 0 | Memphis 218; Nashville 122; Knoxville 80; Chattanooga 49 |
| STATE | category | 2 | 0 | TN 2.0K; nan 1 |
| ZIPCODE | who | 73 | 0 | nan 1.8K; 37857.0 4; 37643.0 4; 37821.0 4 |
| ZIP_4 | other | 185 | 0 | nan 1.8K; 5020 4; 4207 4; 5611 3 |
| PHONE1 | other | 1.8K | 0 | nan 240; (901) 775-3960 9; (615) 356-1880 9; (931) 388-0556 9 |
| PHONE2 | empty | 1 | 2.0K |  |
| FAX | other | 1.3K | 0 | nan 652; (423) 510-1428 7; (731) 643-6635 7; (931) 879-2739 7 |
| GRADE_LEVELS | who | 119 | 0 | 9,10,11,12 312; PK,K,1,2,3,4,5 259; 6,7,8 209; K,1,2,3,4,5 194 |
| CATEGORIES | category | 7 | 0 | nan 2.0K; 4 4; 1 3; 2 2 |
| GEOMETRY | other | 1.9K | 0 | {"type": "Point", "coordi 11; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:33:04.83161 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b6eca0e8-bf41-498a-8496-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | 86bf1261bf6edd9df735f47d0 2.0K |
