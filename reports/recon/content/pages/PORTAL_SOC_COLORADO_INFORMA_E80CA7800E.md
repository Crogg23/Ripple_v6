# PORTAL_SOC_COLORADO_INFORMA_E80CA7800E

rows 2.0K  columns 77  scan 6.7s

roles: amount 6, audit 2, category 41, date 3, id 2, other 13, who 11

## when

EXIT_DATE
  2012         2  
  2013        12  ##
  2014        92  #############
  2015       150  #####################
  2016       142  ###################
  2017       219  ##############################
  2018       162  ######################
  2019       114  ################
  2020       117  ################
  2021       210  #############################
  2022       180  #########################
  2023       199  ###########################
  2024       168  #######################
  2025        19  ###

FISCAL_YEAR
  2013       134  #################
  2014       107  ##############
  2015       232  ##############################
  2016       159  #####################
  2017       183  ########################
  2018       113  ###############
  2019       205  ###########################
  2020       179  #######################
  2021       123  ################
  2022       157  ####################
  2023       165  #####################
  2024       121  ################
  2025       122  ################

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| EXIT_WAGE | 362 | 0 | 22 | 624.08 | 42.0K | 94.1K |
| MEDIANWAGE | 277 | 0.12 | 17.54 | 38.77 | 66 | 4.9K |
| START_WAGE_ADJUST | 1.8K | 0 | 0 | 31.37 | 66 | 4.8K |
| STARTING_WAGE | 322 | 0 | 15.87 | 38.29 | 66 | 4.9K |
| EXIT_WAGE_ADJUST | 237 | 0 | 22 | 50.61 | 56.70 | 5.3K |
| AVGWAGE | 238 | 7.50 | 18.65 | 39.21 | 66 | 4.8K |

## who

APPR_COUNTY_NAME by rows
      1.6K  nan
        11  Los Angeles County
        11  Bond County
         9  Harris County
         7  Marion County
         6  San Diego County
         5  Jefferson County
         5  Miami-Dade County
         5  Bowie County
         5  Cook County
         4  Broward County
         4  Aiken County
         4  Tarrant County
         4  Franklin County
         3  Cobb County
         3  St. Louis County
         3  Riverside County
         3  Wayne County
         3  Ada County
         3  Union County

APPR_COUNTY_NAME by dollars
      273.68     1.6K rows  nan
      131.82       11 rows  Los Angeles County
          95        5 rows  Miami-Dade County
          91        4 rows  Broward County
       82.83        5 rows  Jefferson County
       79.09        6 rows  San Diego County
       69.95        3 rows  Riverside County
       67.89        3 rows  Honolulu County
          66        3 rows  Ada County
       65.74        5 rows  Cook County
          65        9 rows  Harris County
       64.51        3 rows  Kent County
       62.50        3 rows  Wayne County
       59.56        3 rows  Clark County
       59.52        3 rows  Middlesex County
       55.12        2 rows  Box Elder County
       53.15        2 rows  Howard County
       50.94        1 rows  Ward County
       45.67        2 rows  Livingston County
       45.30        2 rows  Summit County

COUNTY_NAME_COPY by rows
      1.4K  nan
        37  Los Angeles County
        32  Suffolk County
        31  Sacramento County
        20  San Bernardino County
        19  San Diego County
        18  San Joaquin County
        17  Westchester County
        12  Clark County
        11  Middlesex County
        11  Bond County
        10  Fulton County
         9  Marion County
         9  Harris County
         9  Jackson County
         7  Broward County
         7  Worcester County
         7  Greene County
         6  Philadelphia County
         6  Aiken County

COUNTY_NAME_COPY by dollars
      218.06       12 rows  Clark County
      130.55       20 rows  San Bernardino County
         128        7 rows  Broward County
      111.08       37 rows  Los Angeles County
      109.03        6 rows  Kent County
      106.86        9 rows  Jackson County
      102.50       10 rows  Fulton County
       90.08       19 rows  San Diego County
       90.04        4 rows  Palm Beach County
       87.40        4 rows  Oakland County
       87.24        9 rows  Marion County
       86.14        5 rows  Cook County
       84.66       31 rows  Sacramento County
       82.09        5 rows  Jefferson County
       81.63        6 rows  Wayne County
       80.27        5 rows  Franklin County
       75.71        4 rows  Arapahoe County
       74.33        6 rows  Philadelphia County
       67.89        3 rows  Honolulu County
       67.70        9 rows  Harris County

COUNTY_NAME by rows
      1.4K  nan
        37  Los Angeles County
        32  Suffolk County
        31  Sacramento County
        20  San Bernardino County
        19  San Diego County
        18  San Joaquin County
        17  Westchester County
        12  Clark County
        11  Bond County
        11  Middlesex County
        10  Fulton County
         9  Jackson County
         9  Marion County
         9  Harris County
         7  Broward County
         7  Greene County
         7  Worcester County
         6  Kent County
         6  Wayne County

COUNTY_NAME by dollars
      218.06       12 rows  Clark County
      130.55       20 rows  San Bernardino County
         128        7 rows  Broward County
      111.08       37 rows  Los Angeles County
      109.03        6 rows  Kent County
      106.86        9 rows  Jackson County
      102.50       10 rows  Fulton County
       90.08       19 rows  San Diego County
       90.04        4 rows  Palm Beach County
       87.40        4 rows  Oakland County
       87.24        9 rows  Marion County
       86.14        5 rows  Cook County
       84.66       31 rows  Sacramento County
       82.09        5 rows  Jefferson County
       81.63        6 rows  Wayne County
       80.27        5 rows  Franklin County
       75.71        4 rows  Arapahoe County
       74.33        6 rows  Philadelphia County
       67.89        3 rows  Honolulu County
       67.70        9 rows  Harris County

OCCUPATION by rows
      1.0K  Not Provided
       366  COMPUTER OPERATOR
        51  ELECTRICIAN (Alternate Title: Interior Electrician)
        28  Airframe Mechanic
        27  ELECTRONICS MECHANIC
        24  ELECTRONICS TECHNICIAN
        16  Electrician
        14  MEDICAL SECRETARY
        13  CONSTRUCTION CRAFT LABORER
        13  Aviation Safety Equipment Technician
        13  PIPE FITTER (Construction)
        12  PLUMBER
        10  SHEET METAL WORKER
        10  ELECTRICIAN, AIRCRAFT
        10  Application Developer
         9  Medical Assistant
         9  CORRECTION OFFICER
         9  Armory Technician
         8  DIESEL MECHANIC
         8  TRUCK DRIVER, HEAVY

OCCUPATION by dollars
      787.29       51 rows  ELECTRICIAN (Alternate Title: Interior Electrician)
      238.81       13 rows  PIPE FITTER (Construction)
      174.46       10 rows  SHEET METAL WORKER
      168.22        8 rows  LINE MAINTAINER (Alternate Title:  High Voltage Electrician)
      159.46        7 rows  ELEVATOR CONSTRUCTOR (Alternate Title: Elevator Constructor 
      152.68       13 rows  CONSTRUCTION CRAFT LABORER
      148.16        7 rows  LINE ERECTOR (POWER-LINE DISTRIBUTION ERECTOR)
      146.07       12 rows  PLUMBER
         135     1.0K rows  Not Provided
      117.58        5 rows  MILLWRIGHT
      112.88        7 rows  CARPENTER
          74        5 rows  Registered Nurse Resident
          66        2 rows  Educator and Trainer
       62.33        4 rows  HEATING & AIR-CONDITIONER INSTALL/SER
       61.37        3 rows  FLOOR LAYER
       55.64        3 rows  ROOFER
       51.59        4 rows  CHILD CARE DEVELOPMENT SPECIALIST
          51        2 rows  Registered Nurse
       50.94        2 rows  ELECTRIC METER REPAIRER
       48.36        4 rows  LINE INSTALLER-REPAIRER

## who x when

APPR_COUNTY_NAME by EXIT_DATE, dollars = START_WAGE_ADJUST
  Ada County                                2023:2
  Aiken County                              2023:2 2024:1
  Bond County                               2023:0
  Box Elder County                          2020:20.26
  Clark County                              2022:1 2024:59.56
  Cobb County                               2024:1
  Cook County                               2019:17.74 2024:48
  Franklin County                           2023:15.86
  Harris County                             2023:3 2024:1
  Jefferson County                          2023:2
  Los Angeles County                        2015:1 2024:20.22
  Marion County                             2015:1 2023:1 2024:9.50
  Miami-Dade County                         2022:1 2024:29
  Middlesex County                          2023:28
  San Diego County                          2020:1 2021:1 2023:18.97 2024:1
  St. Louis County                          2023:2
  Tarrant County                            2023:1
  Union County                              2013:1 2021:15
  Wayne County                              2023:41.50
  nan                                       2012:0 2013:0 2014:0 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:64.23 2023:62.78 2024:0 2025:0

COUNTY_NAME_COPY by EXIT_DATE, dollars = START_WAGE_ADJUST
  Aiken County                              2023:2 2024:25.13
  Arapahoe County                           2023:1
  Bond County                               2023:0
  Broward County                            2022:1
  Clark County                              2022:1 2024:59.56 2025:15
  Cook County                               2019:17.74 2024:48
  Fulton County                             2016:18.75 2020:2 2021:2 2025:1
  Greene County                             2023:5 2024:0
  Harris County                             2023:27.50 2024:2
  Jackson County                            2022:15 2023:26.50 2024:20.25
  Jefferson County                          2023:1 2024:1
  Los Angeles County                        2013:1 2014:3 2015:1 2016:2 2017:7 2018:3 2020:1 2021:2 2022:6 2023:3 2024:20.22
  Marion County                             2015:1 2023:1 2024:1
  Middlesex County                          2015:1 2018:0 2019:0 2020:0 2021:0 2022:1
  Philadelphia County                       2022:2 2023:1
  Sacramento County                         2013:1 2014:3 2015:7 2018:1 2020:3 2021:6 2022:5 2023:15
  San Bernardino County                     2020:3 2021:1 2022:6 2023:4
  San Diego County                          2019:4 2020:1 2021:2 2023:33.97 2024:3
  San Joaquin County                        2015:1 2016:2 2017:1 2018:1 2019:1 2020:2 2021:3 2022:1 2023:6
  Suffolk County                            2013:1 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0
  Wayne County                              2022:1 2023:15
  Westchester County                        2022:3 2023:35.23 2024:2 2025:1
  Worcester County                          2013:1 2018:1 2020:0 2024:0
  nan                                       2012:0 2013:0 2014:0 2015:0 2016:0 2017:0 2018:0 2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0

## what

AGE_COHORT: Ages 25-54 98%, Ages 55+ 1%, Ages 24 and Under 0%, Participant Did Not Self-Ident 0%

APPR_STATE_APPRENTICE_LOCATION: USMAP 78%, CA 8%, MA 3%, TX 2%, MI 1%, IL 1%, NC 1%, FL 1%, PA 1%, IN 1%, MO 1%, GA 1%

APPRENTICE_STATUS_CODE: CA 74%, CO 15%, RE 10%, RI 0%, SU 0%

EDUCATION: Bachelor's degree 50%, High School graduate (includin 34%, Participant Did Not Self-Ident 7%, Some College or Associate's de 6%, Doctorate or Prof. degree 1%, Master's degree 1%, Not High School graduate 0%

ETHNICITY: Non-Hispanic or Latino 82%, Hispanic or Latino 9%, Participant Did Not Self-Ident 9%

HUD_STATE_PROGRAM_LOCATION: USMAP 78%, CA 8%, MA 3%, TX 2%, MI 1%, MO 1%, IL 1%, NY 1%, FL 1%, IN 1%, SC 1%, NC 1%

INDIVIDUALS_WITH_DISABILITIES: Participant Did Not Self-Ident 85%, No 14%, Yes 0%

INDUSTRY: Public Administration (not cov 75%, Construction 6%, Other Services (except Public  5%, Not Provided 4%, Educational Services 3%, Health Care and Social Assista 2%, Professional, Scientific, and  2%, Manufacturing 2%, Utilities 1%, Transportation and Warehousing 1%, Administrative and Support and 0%, Wholesale Trade 0%

ISUNION: Non-Union 84%, Not Specified 10%, Union 6%

PROGRAM_VIEW: National 74%, State 26%

RACE: White 66%, Participant Did Not Self-Ident 32%, Black or African American 2%, American Indian or Alaska Nati 0%, Multiracial 0%, Native Hawaiian or Pacific Isl 0%, Asian 0%

RACE_AND_ETHNICITY: White 65%, Participant Did Not Self-Ident 24%, Hispanic or Latino 9%, Black or African American 2%, American Indian or Alaska Nati 0%, Multiracial 0%, Asian 0%, Native Hawaiian or Pacific Isl 0%

SELECTED_OPTION: White 66%, Participant Did Not Self-Ident 32%, Black or African American 2%, American Indian or Alaska Nati 0%, Multiracial 0%, Native Hawaiian or Pacific Isl 0%, Asian 0%

SELECTGEO: USMAP 78%, CA 8%, MA 3%, TX 2%, MI 1%, MO 1%, IL 1%, NY 1%, FL 1%, IN 1%, SC 1%, NC 1%

SELECTGEO_LOCATION: USMAP 78%, California 8%, Massachusetts 3%, National Programs 2%, Texas 2%, Michigan 1%, Missouri 1%, North Carolina 1%, New York 1%, Pennsylvania 1%, Florida 1%, Indiana 1%

SEX: Male 75%, Participant Did Not Self-Ident 18%, Female 7%

STATE_STATE_WORKLOAD: USMAP 78%, California 8%, Massachusetts 3%, National Programs 2%, Texas 2%, Michigan 1%, Missouri 1%, North Carolina 1%, New York 1%, Pennsylvania 1%, Florida 1%, Indiana 1%

STATE_ID: USMAP 78%, CA 8%, MA 3%, TX 2%, MI 1%, MO 1%, IL 1%, NY 1%, FL 1%, IN 1%, SC 1%, NC 1%

STATE_ID_COPY: USMAP 78%, CA 8%, MA 3%, TX 2%, MI 1%, MO 1%, IL 1%, NY 1%, FL 1%, IN 1%, SC 1%, NC 1%

TABLE_NAME: V_OA_APPRENTICE_ACTIVE_V1 63%, V_OA_APPRENTICE_NEW_V1 25%, V_OA_APPRENTICE_EXITER_V1 12%

UNDERREPRESENTED: nan 59%, 0 29%, 1 8%, UnderRepresented 4%

VETERAN_STATUS: Participant Did Not Self-Ident 79%, Non Veteran 19%, Veteran 1%, Non Veteran, Other Eligible In 0%

FBOP_PROGRAM: 0 98%, 1 2%

FBOP_NUM: 0 98%, 1 2%

FEMALE: 0 93%, 1 7%

MALE: 1 75%, 0 25%

NATIONAL_PROGRAM: 0 100%, 1 0%

NATIONAL_OFFICE_NUM: 0 100%, 1 0%

NATIONALPROGAMS: 0 98%, 1 2%

NEW_ADJUST: nan 75%, 0 25%

NEW_APPR: nan 75%, 1 25%

REGION: 8 74%, 6 8%, 5 5%, 1 5%, 3 3%, 4 3%, 2 2%

UNION_Y_N: 0 84%, nan 10%, 1 6%

USMAP_PROGRAM: 1 72%, 0 28%

USMAP_NUM_NO_NULLS: 0 98%, 1 2%

YOUTH: 0 100%, 1 0%

SEX_ADJUST: Male 75%, Participant Did Not Self-Ident 16%, Female 6%, nan 2%

ACTIVE_ADJUST: 0 51%, nan 37%, 1 12%

ACTIVE_APPR: 1 63%, nan 37%

COMPLETER: nan 88%, 1 12%

COMPLETER_ADJUST: nan 88%, 1 11%, 0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGE_COHORT | category | 4 | 0 | Ages 25-54 2.0K; Ages 55+ 23; Ages 24 and Under 10; Participant Did Not Self- 7 |
| APPR_COUNTY_FIPS | other | 247 | 0 | nan 1.6K; 6037 11; 17005 11; 48201 9 |
| APPR_COUNTY_NAME | who | 230 | 0 | nan 1.6K; Los Angeles County 11; Bond County 11; Harris County 9 |
| APPR_STATE_APPRENTICE_LOCATION | category | 48 | 0 | USMAP 1.4K; CA 152; MA 58; TX 46 |
| APPRENTICE_STATUS_CODE | category | 5 | 0 | CA 1.5K; CO 309; RE 205; RI 7 |
| APPRENTICE_NUMBER | id | 1.9K | 0 | USMAP_1080737 10; USMAP_1076118 10; USMAP_514723 10; USMAP_1034262 10 |
| COUNTY_FIPS | other | 190 | 0 | nan 1.4K; 6037 37; 25025 32; 6067 31 |
| COUNTY_NAME | who | 175 | 0 | nan 1.4K; Los Angeles County 37; Suffolk County 32; Sacramento County 31 |
| COUNTY_NAME_COPY | who | 176 | 0 | nan 1.4K; Los Angeles County 37; Suffolk County 32; Sacramento County 31 |
| DISPLAY_TEST | who | 1 | 0 | States&County 2.0K |
| EDUCATION | category | 7 | 0 | Bachelor's degree 1.0K; High School graduate (inc 688; Participant Did Not Self- 138; Some College or Associate 122 |
| ETHNICITY | category | 3 | 0 | Non-Hispanic or Latino 1.6K; Hispanic or Latino 188; Participant Did Not Self- 175 |
| EXIT_DATE | date | 1.2K | 0 | nan 214; 2017-08-01T00:00:00.000 104; 2017-07-31T00:00:00.000 38; 2020-01-30T00:00:00.000 12 |
| FISCAL_YEAR | date | 13 | 0 | 2015-01-01T00:00:00.000 232; 2019-01-01T00:00:00.000 205; 2017-01-01T00:00:00.000 183; 2020-01-01T00:00:00.000 179 |
| HUD_STATE_PROGRAM_LOCATION | category | 48 | 0 | USMAP 1.4K; CA 150; MA 57; TX 40 |
| HUD_ZIPCODE | other | 320 | 0 | nan 1.4K; 95826 25; 90240 24; 95205 19 |
| INDIVIDUALS_WITH_DISABILITIES | category | 3 | 0 | Participant Did Not Self- 1.7K; No 288; Yes 7 |
| INDUSTRY | category | 13 | 0 | Public Administration (no 1.5K; Construction 115; Other Services (except Pu 99; Not Provided 72 |
| ISUNION | category | 3 | 0 | Non-Union 1.7K; Not Specified 191; Union 129 |
| NAICS_CD | other | 104 | 0 | 928110 1.4K; 812320 86; nan 60; 922140 48 |
| OCCUPATION | who | 185 | 0 | Not Provided 1.0K; COMPUTER OPERATOR 366; ELECTRICIAN (Alternate Ti 51; Airframe Mechanic 28 |
| ONE | other | 1 | 0 | 1 2.0K |
| PROGRAM_NUMBER | other | 327 | 0 | XD098680001 1.4K; 2018-ZA-71003 33; CA_10230-925 23; CA_5083-5278 22 |
| PROGRAM_VIEW | category | 2 | 0 | National 1.5K; State 525 |
| RACE | category | 7 | 0 | White 1.3K; Participant Did Not Self- 634; Black or African American 37; American Indian or Alaska 5 |
| RACE_AND_ETHNICITY | category | 8 | 0 | White 1.3K; Participant Did Not Self- 473; Hispanic or Latino 188; Black or African American 37 |
| SELECTED_MAP | who | 1 | 0 | States 2.0K |
| SELECTED_OPTION | category | 7 | 0 | White 1.3K; Participant Did Not Self- 634; Black or African American 37; American Indian or Alaska 5 |
| SELECTGEO | category | 48 | 0 | USMAP 1.4K; CA 150; MA 57; TX 40 |
| SELECTGEO_LOCATION | category | 48 | 0 | USMAP 1.4K; California 148; Massachusetts 57; National Programs 35 |
| SEX | category | 3 | 0 | Male 1.5K; Participant Did Not Self- 368; Female 135 |
| START_DATE | other | 1.5K | 0 | 09 19 2018 00:00:00 14; 09 30 2019 00:00:00 13; 08 28 2019 00:00:00 12; 07 31 2019 00:00:00 11 |
| STATE_STATE_WORKLOAD | category | 48 | 0 | USMAP 1.4K; California 148; Massachusetts 57; National Programs 35 |
| STATE_BAR | who | 1 | 0 | States&County 2.0K |
| STATE_ID | category | 48 | 0 | USMAP 1.4K; CA 150; MA 57; TX 40 |
| STATE_ID_COPY | category | 48 | 0 | USMAP 1.4K; CA 150; MA 57; TX 40 |
| STATE_COUNTY_BAR | who | 1 | 0 | State&County Bar 2.0K |
| STATE_COUNTY_TOGGLE | who | 1 | 0 | Not Specified 2.0K |
| TABLE_NAME | category | 3 | 0 | V_OA_APPRENTICE_ACTIVE_V1 1.3K; V_OA_APPRENTICE_NEW_V1 506; V_OA_APPRENTICE_EXITER_V1 237 |
| UNDERREPRESENTED | category | 4 | 0 | nan 1.2K; 0 588; 1 155; UnderRepresented 85 |
| VETERAN_STATUS | category | 4 | 0 | Participant Did Not Self- 1.6K; Non Veteran 386; Veteran 25; Non Veteran, Other Eligib 5 |
| WORKLOAD_COUNTY | who | 1 | 0 | Not Specified 2.0K |
| ZERO | other | 1 | 0 | 0 2.0K |
| AGGREGATE_APPRENTICE_COUNT | other | 1 | 0 | 1 2.0K |
| APPRENTICE_ID | id | 2.0K | 0 | 4702303 10; 4575105 10; 3575166 10; 4410686 10 |
| EXIT_WAGE | amount | 150 | 0 | nan 1.6K; 22 118; 0 57; 0.12 4 |
| FBOP_PROGRAM | category | 2 | 0 | 0 2.0K; 1 33 |
| FBOP_NUM | category | 2 | 0 | 0 2.0K; 1 33 |
| FEMALE | category | 2 | 0 | 0 1.9K; 1 135 |
| MALE | category | 2 | 0 | 1 1.5K; 0 503 |
| MEDIANWAGE | amount | 173 | 0 | nan 1.7K; 15 27; 0.12 20; 12 9 |
| NATIONAL_PROGRAM | category | 2 | 0 | 0 2.0K; 1 2 |
| NATIONAL_OFFICE_NUM | category | 2 | 0 | 0 2.0K; 1 2 |
| NATIONALPROGAMS | category | 2 | 0 | 0 2.0K; 1 35 |
| NEW_ADJUST | category | 2 | 0 | nan 1.5K; 0 506 |
| NEW_APPR | category | 2 | 0 | nan 1.5K; 1 506 |
| PDNSI | other | 1 | 0 | 0 2.0K |
| PROGRAM_ID | other | 322 | 0 | 33538 1.4K; 71003 33; 102844 23; 102960 22 |
| REGION | category | 7 | 0 | 8 1.5K; 6 169; 5 102; 1 91 |
| START_WAGE_ADJUST | amount | 164 | 0 | 0 1.5K; nan 237; 15 26; 12 9 |
| STARTING_WAGE | amount | 174 | 0 | nan 1.7K; 0 45; 15 27; 0.12 20 |
| TOTAL_APPRENTICE_NUM | other | 1 | 0 | 1 2.0K |
| UNION_Y_N | category | 3 | 0 | 0 1.7K; nan 191; 1 129 |
| USMAP_PROGRAM | category | 2 | 0 | 1 1.4K; 0 560 |
| USMAP_NUM | other | 1 | 0 | 0 2.0K |
| USMAP_NUM_NO_NULLS | category | 2 | 0 | 0 2.0K; 1 35 |
| YOUTH | category | 2 | 0 | 0 2.0K; 1 10 |
| SEX_ADJUST | category | 4 | 0 | Male 1.5K; Participant Did Not Self- 328; Female 128; nan 48 |
| ACTIVE_ADJUST | category | 3 | 0 | 0 1.0K; nan 743; 1 238 |
| ACTIVE_APPR | category | 2 | 0 | 1 1.3K; nan 743 |
| COMPLETER | category | 2 | 0 | nan 1.8K; 1 237 |
| COMPLETER_ADJUST | category | 3 | 0 | nan 1.8K; 1 213; 0 24 |
| EXIT_WAGE_ADJUST | amount | 94 | 0 | nan 1.8K; 22 105; 0 24; 25 3 |
| AVGWAGE | amount | 163 | 0 | nan 1.8K; 15 26; 12 9; 16 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:45:03.89010 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 10223234-e567-4f09-8deb-7 2.0K |
| SRC_SHA256 | who | 1 | 0 | 007118564074c43f480597e52 2.0K |
