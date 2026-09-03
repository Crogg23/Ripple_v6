# PORTAL_CKA_CALIFORNIA_OPEN_22F6B7DB0F

rows 1.5K  columns 24  scan 6.3s

roles: amount 4, audit 2, category 8, date 1, id 2, other 5, who 3

## when

INGESTED_AT
  2026      1.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FAC_LATITUDE | 1.5K | 32.96 | 38.03 | 41.74 | 41.93 | 57.5K |
| FAC_LONGITUDE | 1.5K | -124.27 | -122.54 | -121.94 | -115.54 | -184.0K |
| X | 1.5K | -13.83M | -13.64M | -13.57M | -12.86M | -20.48B |
| Y | 1.5K | 3.89M | 4.58M | 5.12M | 5.15M | 6.94B |

## who

NAME by rows
         5  POMEROY RECREATION & REHABILITATION CEN
         4  KINDERCARE LEARNING CENTER
         4  POTRERO HILL MONTESSORI SCHOOL
         3  BRIGHT HORIZONS SAN FRANCISCO CALIFORNI
         3  L'ACADEMY PRESCHOOL SF SOMA
         3  STRATFORD SCHOOL
         3  CRISTINA'S CARE HOME
         3  CENTRO PRIMEROS PASOS
         3  BRIGHT STARS CHILDREN'S CENTER
         3  DAMENIK'S HOME
         3  OLD FIREHOUSE SCHOOL
         3  BUILDING KIDZ
         2  CAL POLY HUMBOLDT CHILDREN'S CENTER RM#
         2  TEACHER'S PET SCHOOL
         2  LANGUAGE IN ACTION - SF
         2  ROSEBAY BEHAVIORAL HEALTH
         2  SUNNY INFANT AND PRESCHOOL CENTER
         2  LAUREL HEIGHTS CHILD DEVELOPMENT CENTER
         2  LIL FISHER LEARNING CENTER
         2  OUR HOUSE

NAME by dollars
      188.73        5 rows  POMEROY RECREATION & REHABILITATION CEN
      153.26        4 rows  KINDERCARE LEARNING CENTER
      151.04        4 rows  POTRERO HILL MONTESSORI SCHOOL
      113.98        3 rows  BRIGHT STARS CHILDREN'S CENTER
      113.92        3 rows  OLD FIREHOUSE SCHOOL
      113.37        3 rows  BRIGHT HORIZONS SAN FRANCISCO CALIFORNI
      113.31        3 rows  L'ACADEMY PRESCHOOL SF SOMA
      113.21        3 rows  CENTRO PRIMEROS PASOS
      113.13        3 rows  DAMENIK'S HOME
      113.08        3 rows  STRATFORD SCHOOL
      112.89        3 rows  CRISTINA'S CARE HOME
      112.83        3 rows  BUILDING KIDZ
       81.88        2 rows  LIL FISHER LEARNING CENTER
       81.80        2 rows  LITTLE LEARNERS CENTER
       81.74        2 rows  CAL POLY HUMBOLDT CHILDREN'S CENTER RM#
       81.56        2 rows  TEACHER'S PET SCHOOL
       81.16        2 rows  EARLY FOUNDATIONS CHILDREN'S ACADEMY
       79.04        2 rows  OUR HOUSE
       78.88        2 rows  OCEANSIDE CARE HOME LLC
       77.25        2 rows  MILA'S PRESCHOOL AND CHILDCARE CENTER-I

RES_CITY by rows
       335  SAN FRANCISCO
       224  SANTA ROSA
        99  SAN RAFAEL
        75  NOVATO
        59  SOUTH SAN FRA
        57  DALY CITY
        47  SAN BRUNO
        44  ROHNERT PARK
        44  EUREKA
        41  PETALUMA
        29  UKIAH
        25  PACIFICA
        25  WINDSOR
        24  SONOMA
        21  MILL VALLEY
        16  SEBASTOPOL
        14  CORTE MADERA
        13  FORTUNA
        13  FORT BRAGG
        12  COTATI

RES_CITY by dollars
       12.6K      335 rows  SAN FRANCISCO
        8.6K      224 rows  SANTA ROSA
        3.8K       99 rows  SAN RAFAEL
        2.9K       75 rows  NOVATO
        2.2K       59 rows  SOUTH SAN FRA
        2.1K       57 rows  DALY CITY
        1.8K       44 rows  EUREKA
        1.8K       47 rows  SAN BRUNO
        1.7K       44 rows  ROHNERT PARK
        1.6K       41 rows  PETALUMA
        1.1K       29 rows  UKIAH
      963.43       25 rows  WINDSOR
      940.60       25 rows  PACIFICA
      919.20       24 rows  SONOMA
      795.86       21 rows  MILL VALLEY
      614.31       16 rows  SEBASTOPOL
      530.93       14 rows  CORTE MADERA
      527.64       13 rows  FORTUNA
      512.72       13 rows  FORT BRAGG
      487.01       12 rows  REDDING

SRC_SHA256 by rows
      1.5K  9e8421ebab9a1c7f6a900abc886e9b52692cbed81add63f5165047fa6fc2b63f

SRC_SHA256 by dollars
       57.5K     1.5K rows  9e8421ebab9a1c7f6a900abc886e9b52692cbed81add63f5165047fa6fc2

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = FAC_LATITUDE
  BRIGHT HORIZONS SAN FRANCISCO CALIFORNI   2026:113.37
  BRIGHT STARS CHILDREN'S CENTER            2026:113.98
  BUILDING KIDZ                             2026:112.83
  CAL POLY HUMBOLDT CHILDREN'S CENTER RM#   2026:81.74
  CENTRO PRIMEROS PASOS                     2026:113.21
  CRISTINA'S CARE HOME                      2026:112.89
  DAMENIK'S HOME                            2026:113.13
  EARLY FOUNDATIONS CHILDREN'S ACADEMY      2026:81.16
  KINDERCARE LEARNING CENTER                2026:153.26
  L'ACADEMY PRESCHOOL SF SOMA               2026:113.31
  LANGUAGE IN ACTION - SF                   2026:75.58
  LAUREL HEIGHTS CHILD DEVELOPMENT CENTER   2026:75.56
  LIL FISHER LEARNING CENTER                2026:81.88
  LITTLE LEARNERS CENTER                    2026:81.80
  MILA'S PRESCHOOL AND CHILDCARE CENTER-I   2026:77.25
  OCEANSIDE CARE HOME LLC                   2026:78.88
  OLD FIREHOUSE SCHOOL                      2026:113.92
  OUR HOUSE                                 2026:79.04
  POMEROY RECREATION & REHABILITATION CEN   2026:188.73
  POTRERO HILL MONTESSORI SCHOOL            2026:151.04
  ROSEBAY BEHAVIORAL HEALTH                 2026:75.97
  STRATFORD SCHOOL                          2026:113.08
  SUNNY INFANT AND PRESCHOOL CENTER         2026:75.56
  TEACHER'S PET SCHOOL                      2026:81.56

RES_CITY by INGESTED_AT  LOAD STAMP, not an event date, dollars = FAC_LATITUDE
  CORTE MADERA                              2026:530.93
  COTATI                                    2026:459.93
  DALY CITY                                 2026:2.1K
  EUREKA                                    2026:1.8K
  FORT BRAGG                                2026:512.72
  FORTUNA                                   2026:527.64
  MILL VALLEY                               2026:795.86
  NOVATO                                    2026:2.9K
  PACIFICA                                  2026:940.60
  PETALUMA                                  2026:1.6K
  REDDING                                   2026:487.01
  ROHNERT PARK                              2026:1.7K
  SAN BRUNO                                 2026:1.8K
  SAN FRANCISCO                             2026:12.6K
  SAN RAFAEL                                2026:3.8K
  SANTA ROSA                                2026:8.6K
  SEBASTOPOL                                2026:614.31
  SONOMA                                    2026:919.20
  SOUTH SAN FRA                             2026:2.2K
  UKIAH                                     2026:1.1K
  WINDSOR                                   2026:963.43

## what

TYPE: 850 37%, 740 24%, 735 13%, 860 7%, 830 6%, 840 4%, 775 4%, 772 2%, 734 1%, 741 1%, 737 1%, 736 0%

PROGRAM_TYPE: CHILD CARE 55%, ADULT AND SENIOR 45%

STATUS: 3 97%, 4 2%, 6 1%, 5 0%

CLIENT_SERVED: 950 42%, 983 13%, 910 12%, 955 9%, 935 8%, 940 4%, 957 3%, 985 3%, 915 2%, 945 2%, 956 2%, 960 1%

FAC_CO_NBR: 49 28%, 38 23%, 21 18%, 41 15%, 12 6%, 23 5%, 17 2%, 28 1%, 47 1%, 45 1%, 8 1%, 53 0%

COUNTY: Sonoma 23%, San Francisco 20%, Marin 16%, San Mateo 12%, Sonoma County 7%, Humboldt 5%, Mendocino 4%, San Francisco County 3%, San Mateo County 3%, Marin County 3%, Lake 2%, Humboldt County 1%

FAC_DO_DESC: PENINSULA CHILD CARE 28%, NO. CAL AC/SC 22%, SANTA ROSA RO 14%, SF COASTAL AC/SC 11%, REDWOOD EMPIRE CC 8%, SAN BRUNO CC RO 5%, CHICO-DAY CARE 4%, SANTA ROSA CC RO 3%, SAN BRUNO RO 2%, CHICO CC RO 2%, CHICO - RESIDENTIAL 1%, SANTA ROSA ASC 0%

FAC_TYPE_DESC: DAY CARE CENTER 37%, RESIDENTIAL-ELDERLY 24%, ADULT RESIDENTIAL 13%, SINGLE CHILD CARE CE 7%, INFANT CENTER 6%, SCHOOL-AGE DC CENTER 4%, ADULT DAY CARE 4%, SOCIAL REHABILITATIO 2%, ARFPSHN 1%, RESIDENTIAL ELDERLY- 1%, ARF-ENHANCED BEHAVIO 1%, RESID FAC CHRON ILL 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FAC_LATITUDE | amount | 1.4K | 0 | 37.764877 11; 37.79267 10; 37.774055 9; 37.46335 9 |
| FAC_LONGITUDE | amount | 1.4K | 0 | -122.40073 11; -122.404144 10; -122.422615 9; -122.436554 9 |
| FAC_NBR | id | 1.5K | 0 | 384004644 9; 384004643 9; 455002677 8; 380540091 8 |
| TYPE | category | 12 | 0 | 850 557; 740 357; 735 201; 860 104 |
| PROGRAM_TYPE | category | 2 | 0 | CHILD CARE 822; ADULT AND SENIOR 678 |
| STATUS | category | 4 | 0 | 3 1.5K; 4 32; 6 13; 5 2 |
| CLIENT_SERVED | category | 20 | 0 | 950 607; 983 191; 910 182; 955 128 |
| CAPACITY | other | 148 | 0 | 6 311; 4 94; 30 91; 24 74 |
| NAME | who | 1.4K | 0 | POTRERO HILL MONTESSORI S 11; BRIGHT HORIZONS SAN FRANC 10; L'ACADEMY PRESCHOOL SF SO 9; L'ACADEMY PRESCHOOL SF NO 9 |
| RES_STREET_ADDR | other | 1.4K | 0 | 1701 17TH STREET 11; 555 CALIFORNIA STREET 10; 111 PAGE STREET 9; 494 MIRAMONTES AVENUE 9 |
| RES_CITY | who | 114 | 0 | SAN FRANCISCO 335; SANTA ROSA 224; SAN RAFAEL 99; NOVATO 75 |
| RES_STATE | other | 1 | 0 | CA 1.5K |
| RES_ZIP_CODE | other | 142 | 0 | 94903 68; 94080 64; 95403 57; 94066 46 |
| FAC_PHONE_NBR | other | 1.3K | 0 | 4159217019 11; 6504763015 11; 4153927531 10; 4152307508 10 |
| FAC_CO_NBR | category | 20 | 0 | 49 419; 38 337; 21 267; 41 215 |
| COUNTY | category | 33 | 0 | Sonoma 327; San Francisco 286; Marin 230; San Mateo 173 |
| FAC_DO_DESC | category | 26 | 0 | PENINSULA CHILD CARE 413; NO. CAL AC/SC 319; SANTA ROSA RO 202; SF COASTAL AC/SC 168 |
| FAC_TYPE_DESC | category | 12 | 0 | DAY CARE CENTER 557; RESIDENTIAL-ELDERLY 357; ADULT RESIDENTIAL 201; SINGLE CHILD CARE CE 104 |
| OBJECTID | id | 1.5K | 0 | 3399 8; 3395 8; 3389 8; 3388 8 |
| X | amount | 1.4K | 0 | -13625586.936325 11; -13625966.9810665 10; -13628023.163381 9; -13629574.8457631 9 |
| Y | amount | 1.4K | 0 | 4546263.85819268 11; 4550178.2977718 10; 4547556.34922542 9; 4503890.10422634 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:55:04.96623 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 27b571e8-f5f0-4e27-b93a-c 1.5K |
| SRC_SHA256 | who | 1 | 0 | 9e8421ebab9a1c7f6a900abc8 1.5K |
