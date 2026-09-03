# PORTAL_SOC_PA_OPEN_DATA_POR_CD66682741

rows 2.0K  columns 110  scan 6.7s

roles: amount 42, audit 2, category 40, date 2, other 17, who 8

## when

COLLECTION_WEEK
  2020       497  ##############################
  2021       438  ##########################
  2022       416  #########################
  2023       489  ##############################
  2024       160  ##########

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_BEDS_7_DAY_COVERAGE | 2.0K | 0 | 1 | 7 | 7 | 6.5K |
| TOTAL_ADULT_PATIENTS_4 | 2.0K | 0 | 7 | 7 | 7 | 11.2K |
| TOTAL_ADULT_PATIENTS_5 | 2.0K | 0 | 7 | 7 | 7 | 11.8K |
| TOTAL_PEDIATRIC_PATIENTS_4 | 2.0K | 0 | 7 | 7 | 7 | 11.2K |
| TOTAL_PEDIATRIC_PATIENTS_5 | 2.0K | 0 | 7 | 7 | 7 | 11.8K |
| TOTAL_ICU_BEDS_7_DAY_COVERAGE | 2.0K | 0 | 7 | 7 | 7 | 13.4K |

## who

HOSPITAL_NAME by rows
        18  UPMC CHILDREN'S HOSPITAL OF PITTSBURGH
        18  SUBURBAN COMMUNITY HOSPITAL
        18  TROY COMMUNITY HOSPITAL
        17  GEISINGER-BLOOMSBURG HOSPITAL
        17  SELECT SPECIALTY HOSPITAL - ERIE
        17  PAM HEALTH SPECIALITY HOSPITAL AT HERITAGE VALLEY
        17  UPMC PINNACLE HOSPITALS
        17  WARREN GENERAL HOSPITAL
        17  EXCELA HEALTH WESTMORELAND HOSPITAL
        17  PENN HIGHLANDS BROOKVILLE
        17  UPMC KANE
        16  UPMC MEMORIAL
        16  WELLSPAN CHAMBERSBURG HOSPITAL
        16  HERITAGE VALLEY KENNEDY
        16  TEMPLE HEALTH - CHESTNUT HILL HOSPITAL
        16  WELLSPAN SURGERY AND REHABILITATION HOSPITAL
        16  GEISINGER COMMUNITY MEDICAL CENTER
        16  UPMC LITITZ
        16  ST LUKE'S HOSPITAL - EASTON CAMPUS
        16  ADVANCED SURGICAL HOSPITAL

HOSPITAL_NAME by dollars
         126       18 rows  SUBURBAN COMMUNITY HOSPITAL
         102       15 rows  KINDRED HOSPITAL PHILADELPHIA
          94       16 rows  HERITAGE VALLEY KENNEDY
          90       13 rows  PAM SPECIALTY HOSPITAL OF WILKES-BARRE
          78       18 rows  UPMC CHILDREN'S HOSPITAL OF PITTSBURGH
          76       11 rows  LOWER BUCKS HOSPITAL
          73       12 rows  SHARON REGIONAL HEALTH SYSTEM
          71       12 rows  MERCY CATHOLIC MEDICAL CENTER- MERCY FITZGERALD
          70       14 rows  SELECT SPECIALTY HOSPITAL - PITTSBURGH/UPMC
          70       16 rows  WELLSPAN SURGERY AND REHABILITATION HOSPITAL
          70       15 rows  UPMC HANOVER
          70       13 rows  LECOM HEALTH CORRY MEMORIAL HOSPITAL
          68       18 rows  TROY COMMUNITY HOSPITAL
          63       17 rows  SELECT SPECIALTY HOSPITAL - ERIE
          63       15 rows  GETTYSBURG HOSPITAL
          63        9 rows  ROXBOROUGH MEMORIAL HOSPITAL
          62       14 rows  FULTON COUNTY MEDICAL CENTER
          62       16 rows  GEISINGER COMMUNITY MEDICAL CENTER
          60       13 rows  HERITAGE VALLEY BEAVER
          58       17 rows  UPMC PINNACLE HOSPITALS

HOSPITAL_PK by rows
        18  390116
        18  391305
        18  393302
        17  390003
        17  390146
        17  390067
        17  392037
        17  390104
        17  390145
        17  391312
        17  392043
        16  390327
        16  390026
        16  390162
        16  390157
        16  390001
        16  390151
        16  390068
        16  390101
        16  390323

HOSPITAL_PK by dollars
         126       18 rows  390116
         102       15 rows  392027
          94       16 rows  390157
          90       13 rows  392025
          78       18 rows  393302
          76       11 rows  390070
          73       12 rows  390211
          71       12 rows  390156
          70       16 rows  390327
          70       14 rows  392044
          70       15 rows  390233
          70       13 rows  391308
          68       18 rows  391305
          63       17 rows  392037
          63       15 rows  390065
          63        9 rows  390304
          62       16 rows  390001
          62       14 rows  391303
          60       13 rows  390036
          58       17 rows  390067

CCN by rows
        18  393302
        18  390116
        18  391305
        17  392037
        17  392043
        17  390003
        17  390067
        17  391312
        17  390145
        17  390104
        17  390146
        16  390068
        16  390101
        16  390151
        16  390162
        16  390001
        16  390323
        16  390327
        16  390026
        16  390157

CCN by dollars
         126       18 rows  390116
         102       15 rows  392027
          94       16 rows  390157
          90       13 rows  392025
          78       18 rows  393302
          76       11 rows  390070
          73       12 rows  390211
          71       12 rows  390156
          70       14 rows  392044
          70       16 rows  390327
          70       15 rows  390233
          70       13 rows  391308
          68       18 rows  391305
          63       15 rows  390065
          63        9 rows  390304
          63       17 rows  392037
          62       16 rows  390001
          62       14 rows  391303
          60       13 rows  390036
          58       17 rows  390067

HHS_IDS by rows
        40  nan
        18  [C393302-A]
        18  [C390116-A]
        18  [C391305-A]
        17  [C390067-C, C390067-B, C390067-A]
        17  [C390146-A]
        17  [C391312-A]
        17  [C390145-A]
        17  [C392043-A]
        17  [C392037-A]
        17  [C390104-A]
        17  [C390003-A]
        16  [C390026-A]
        16  [C390068-A]
        16  [C390162-A]
        16  [C390323-A]
        16  [C390101-A]
        16  [C390157-A]
        16  [C390001-A]
        16  [C390151-A]

HHS_IDS by dollars
         126       18 rows  [C390116-A]
         121       40 rows  nan
         102       15 rows  [C392027-B, C392027-A]
          94       16 rows  [C390157-A]
          90       13 rows  [C392025-A]
          78       18 rows  [C393302-A]
          76       11 rows  [C390070-A]
          73       12 rows  [C390211-A]
          71       12 rows  [C390156-A, C390156-B]
          70       13 rows  [C391308-A]
          70       14 rows  [C392044-B, C392044-A]
          70       15 rows  [C390233-A]
          70       16 rows  [C390327-A]
          68       18 rows  [C391305-A]
          63        9 rows  [C390304-A]
          63       17 rows  [C392037-A]
          63       15 rows  [C390065-A]
          62       14 rows  [C391303-A]
          62       16 rows  [C390001-A]
          60       13 rows  [C390036-A]

## who x when

HOSPITAL_NAME by COLLECTION_WEEK, dollars = TOTAL_BEDS_7_DAY_COVERAGE
  ADVANCED SURGICAL HOSPITAL                2020:31 2021:21 2022:1 2023:0
  EXCELA HEALTH WESTMORELAND HOSPITAL       2020:7 2021:28 2022:7 2023:0
  GEISINGER COMMUNITY MEDICAL CENTER        2020:18 2021:21 2022:22 2023:1 2024:0
  GEISINGER-BLOOMSBURG HOSPITAL             2020:7 2021:28 2022:16 2023:1 2024:0
  GETTYSBURG HOSPITAL                       2020:21 2021:35 2022:7 2023:0 2024:0
  HERITAGE VALLEY KENNEDY                   2020:31 2021:21 2022:21 2023:21
  KINDRED HOSPITAL PHILADELPHIA             2020:32 2021:14 2022:28 2023:14 2024:14
  LECOM HEALTH CORRY MEMORIAL HOSPITAL      2020:48 2021:14 2022:7 2023:0 2024:1
  LOWER BUCKS HOSPITAL                      2020:27 2021:42 2022:7
  MERCY CATHOLIC MEDICAL CENTER- MERCY FIT  2020:35 2021:21 2022:15 2024:0
  PAM HEALTH SPECIALITY HOSPITAL AT HERITA  2021:14 2022:1 2023:0 2024:0
  PAM SPECIALTY HOSPITAL OF WILKES-BARRE    2020:48 2021:14 2022:14 2024:14
  PENN HIGHLANDS BROOKVILLE                 2020:17 2021:14 2022:7 2023:0 2024:0
  ROXBOROUGH MEMORIAL HOSPITAL              2021:14 2022:21 2023:28
  SELECT SPECIALTY HOSPITAL - ERIE          2020:7 2021:28 2022:7 2023:21 2024:0
  SELECT SPECIALTY HOSPITAL - PITTSBURGH/U  2020:7 2021:35 2022:14 2023:14 2024:0
  SHARON REGIONAL HEALTH SYSTEM             2020:17 2021:28 2022:7 2023:21
  ST LUKE'S HOSPITAL - EASTON CAMPUS        2020:11 2021:14 2022:0 2023:0
  SUBURBAN COMMUNITY HOSPITAL               2020:21 2021:49 2022:21 2023:21 2024:14
  TEMPLE HEALTH - CHESTNUT HILL HOSPITAL    2020:8 2021:21 2022:0 2023:0
  TROY COMMUNITY HOSPITAL                   2020:12 2021:49 2022:7 2023:0 2024:0
  UPMC CHILDREN'S HOSPITAL OF PITTSBURGH    2020:21 2021:35 2022:22 2023:0 2024:0
  UPMC HANOVER                              2021:63 2022:7 2023:0
  UPMC KANE                                 2020:24 2021:7 2022:5 2023:0 2024:0
  UPMC LITITZ                               2020:12 2021:21 2022:13 2023:0 2024:0
  UPMC MEMORIAL                             2020:14 2021:42 2022:0 2023:0
  UPMC PINNACLE HOSPITALS                   2020:30 2021:28 2022:0 2023:0 2024:0
  WARREN GENERAL HOSPITAL                   2020:27 2021:28 2022:0 2023:1
  WELLSPAN CHAMBERSBURG HOSPITAL            2020:21 2021:21 2022:14 2023:0 2024:0
  WELLSPAN SURGERY AND REHABILITATION HOSP  2020:21 2021:28 2022:21 2023:0 2024:0

HOSPITAL_PK by COLLECTION_WEEK, dollars = TOTAL_BEDS_7_DAY_COVERAGE
  390001                                    2020:18 2021:21 2022:22 2023:1 2024:0
  390003                                    2020:7 2021:28 2022:16 2023:1 2024:0
  390026                                    2020:8 2021:21 2022:0 2023:0
  390065                                    2020:21 2021:35 2022:7 2023:0 2024:0
  390067                                    2020:30 2021:28 2022:0 2023:0 2024:0
  390068                                    2020:12 2021:21 2022:13 2023:0 2024:0
  390070                                    2020:27 2021:42 2022:7
  390101                                    2020:14 2021:42 2022:0 2023:0
  390104                                    2020:24 2021:7 2022:5 2023:0 2024:0
  390116                                    2020:21 2021:49 2022:21 2023:21 2024:14
  390145                                    2020:7 2021:28 2022:7 2023:0
  390146                                    2020:27 2021:28 2022:0 2023:1
  390151                                    2020:21 2021:21 2022:14 2023:0 2024:0
  390156                                    2020:35 2021:21 2022:15 2024:0
  390157                                    2020:31 2021:21 2022:21 2023:21
  390162                                    2020:11 2021:14 2022:0 2023:0
  390211                                    2020:17 2021:28 2022:7 2023:21
  390233                                    2021:63 2022:7 2023:0
  390304                                    2021:14 2022:21 2023:28
  390323                                    2020:31 2021:21 2022:1 2023:0
  390327                                    2020:21 2021:28 2022:21 2023:0 2024:0
  391305                                    2020:12 2021:49 2022:7 2023:0 2024:0
  391308                                    2020:48 2021:14 2022:7 2023:0 2024:1
  391312                                    2020:17 2021:14 2022:7 2023:0 2024:0
  392025                                    2020:48 2021:14 2022:14 2024:14
  392027                                    2020:32 2021:14 2022:28 2023:14 2024:14
  392037                                    2020:7 2021:28 2022:7 2023:21 2024:0
  392043                                    2021:14 2022:1 2023:0 2024:0
  392044                                    2020:7 2021:35 2022:14 2023:14 2024:0
  393302                                    2020:21 2021:35 2022:22 2023:0 2024:0

## what

HOSPITAL_SUBTYPE: Short Term 79%, Critical Access Hospitals 10%, Long Term 8%, Childrens Hospitals 3%

IS_METRO_MICRO: true 94%, false 6%

ALL_ADULT_HOSPITAL_BEDS_7_2: 0 56%, 7 37%, 6 2%, 1 1%, 4 1%, 5 1%, 3 1%, 2 1%

ALL_ADULT_HOSPITAL_INPATIENT_4: 7 81%, 0 16%, 6 1%, 4 1%, 5 1%, 3 0%, 2 0%, 1 0%

INPATIENT_BEDS_USED_7_DAY_2: 7 84%, 0 8%, 6 3%, 5 1%, 4 1%, 1 1%, 3 1%, 2 1%

ALL_ADULT_HOSPITAL_INPATIENT_5: 7 81%, 0 15%, 6 2%, 4 1%, 5 1%, 3 0%, 2 0%, 1 0%

INPATIENT_BEDS_7_DAY_COVERAGE: 7 84%, 0 8%, 6 3%, 5 1%, 4 1%, 1 1%, 3 1%, 2 1%

ICU_BEDS_USED_7_DAY_COVERAGE: 7 79%, 0 16%, 6 2%, 4 1%, 5 1%, 3 0%, 2 0%, 1 0%

STAFFED_ADULT_ICU_BED_2: 7 79%, 0 16%, 6 2%, 4 1%, 5 1%, 3 0%, 2 0%, 1 0%

STAFFED_ICU_ADULT_PATIENTS_4: 7 75%, 0 17%, 6 3%, 5 2%, 4 1%, 3 1%, 1 1%, 2 1%

STAFFED_ICU_ADULT_PATIENTS_5: 7 79%, 0 16%, 6 2%, 4 1%, 5 1%, 3 0%, 2 0%, 1 0%

ICU_PATIENTS_CONFIRMED_2: 7 75%, 0 21%, 6 2%, 5 1%, 4 1%, 3 0%, 1 0%, 2 0%

PREVIOUS_DAY_ADMISSION_ADULT_COVID_CONFIRMED_7_DAY_COVERAGE: 7 82%, 0 14%, 6 2%, 5 1%, 4 1%, 3 0%, 2 0%, 1 0%

PREVIOUS_DAY_ADMISSION_PEDIATRIC_COVID_CONFIRMED_7_DAY_COVERAGE: 7 81%, 0 15%, 6 1%, 4 1%, 5 1%, 1 0%, 3 0%, 2 0%

PREVIOUS_DAY_ADMISSION_ADULT_COVID_SUSPECTED_7_DAY_COVERAGE: 7 75%, 0 17%, 6 3%, 5 2%, 4 1%, 3 1%, 2 1%, 1 1%

PREVIOUS_DAY_ADMISSION_PEDIATRIC_COVID_SUSPECTED_7_DAY_COVERAGE: 7 74%, 0 18%, 6 2%, 5 2%, 4 1%, 1 1%, 3 1%, 2 1%

IS_CORRECTED: False 96%, True 4%

ICU_PATIENTS_CONFIRMED_1: 0 74%, nan 21%, -999999 3%, 4 1%, 5 1%, 7 0%, 6 0%, 9 0%, 13 0%, 10 0%, 21 0%, 12 0%

PREVIOUS_DAY_ADMISSION_ADULT_1: 0 81%, nan 17%, -999999 2%, 4 0%

PREVIOUS_DAY_ADMISSION_ADULT_2: 0 70%, nan 18%, -999999 11%, 4 0%, 6 0%, 7 0%, 5 0%, 13 0%, 15 0%, 8 0%

PREVIOUS_DAY_ADMISSION_ADULT_3: 0 66%, nan 18%, -999999 14%, 4 1%, 6 0%, 5 0%, 8 0%, 7 0%, 12 0%, 10 0%, 15 0%

PREVIOUS_DAY_ADMISSION_ADULT_4: 0 64%, nan 18%, -999999 15%, 4 2%, 5 1%, 7 0%, 6 0%, 8 0%, 10 0%, 9 0%, 11 0%, 13 0%

PREVIOUS_DAY_ADMISSION_ADULT_5: 0 57%, -999999 20%, nan 18%, 4 2%, 5 1%, 6 1%, 7 1%, 8 1%, 9 0%, 10 0%, 12 0%, 11 0%

PREVIOUS_DAY_ADMISSION_ADULT_6: 0 52%, -999999 21%, nan 17%, 4 3%, 5 2%, 6 1%, 9 1%, 7 1%, 8 1%, 11 0%, 10 0%, 13 0%

PREVIOUS_DAY_ADMISSION_ADULT_7: 0 49%, -999999 23%, nan 17%, 4 4%, 5 2%, 6 1%, 7 1%, 9 1%, 8 1%, 10 1%, 11 0%, 12 0%

PREVIOUS_DAY_ADMISSION_ADULT_8: 0 47%, -999999 23%, nan 18%, 4 4%, 5 2%, 6 2%, 7 1%, 8 1%, 10 1%, 9 1%, 12 1%, 15 0%

PREVIOUS_DAY_ADMISSION_ADULT_9: 0 80%, nan 16%, -999999 3%, 5 0%, 11 0%, 7 0%, 4 0%, 6 0%, 18 0%, 12 0%, 37 0%, 8 0%

PREVIOUS_DAY_ADMISSION: 0 80%, nan 15%, -999999 4%, 7 0%, 4 0%, 8 0%, 5 0%, 6 0%, 9 0%, 13 0%, 64 0%, 14 0%

PREVIOUS_DAY_ADMISSION_ADULT_11: 0 74%, nan 20%, -999999 5%, 4 0%, 7 0%

PREVIOUS_DAY_ADMISSION_ADULT_12: 0 63%, nan 21%, -999999 11%, 4 1%, 5 1%, 6 1%, 7 1%, 10 0%, 9 0%, 8 0%, 13 0%, 14 0%

PREVIOUS_DAY_ADMISSION_ADULT_13: 0 63%, nan 21%, -999999 10%, 4 2%, 5 1%, 6 1%, 7 1%, 8 1%, 12 0%, 11 0%, 10 0%, 9 0%

PREVIOUS_DAY_ADMISSION_ADULT_14: 0 61%, nan 21%, -999999 10%, 4 2%, 5 1%, 6 1%, 7 1%, 8 1%, 9 1%, 12 0%, 11 0%, 10 0%

PREVIOUS_DAY_ADMISSION_ADULT_15: 0 59%, nan 21%, -999999 11%, 4 2%, 5 1%, 6 1%, 7 1%, 8 1%, 9 1%, 12 1%, 10 1%, 11 1%

PREVIOUS_DAY_ADMISSION_ADULT_16: 0 58%, nan 21%, -999999 11%, 5 2%, 11 1%, 4 1%, 8 1%, 14 1%, 6 1%, 7 1%, 9 1%, 10 1%

PREVIOUS_DAY_ADMISSION_ADULT_17: 0 58%, nan 22%, -999999 11%, 5 1%, 4 1%, 7 1%, 16 1%, 9 1%, 8 1%, 6 1%, 10 1%, 15 1%

PREVIOUS_DAY_ADMISSION_ADULT_18: 0 58%, nan 21%, -999999 11%, 4 2%, 6 1%, 7 1%, 5 1%, 13 1%, 9 1%, 8 1%, 21 1%, 10 1%

PREVIOUS_DAY_ADMISSION_ADULT_19: 0 77%, nan 19%, -999999 3%, 9 0%, 6 0%, 4 0%, 5 0%, 7 0%, 8 0%, 35 0%, 28 0%, 18 0%

PREVIOUS_DAY_ADMISSION_1: 0 73%, nan 18%, -999999 5%, 9 1%, 5 1%, 6 0%, 7 0%, 4 0%, 8 0%, 10 0%, 12 0%, 16 0%

PREVIOUS_DAY_ADMISSION_2: 0 67%, nan 21%, -999999 8%, 6 1%, 7 1%, 4 1%, 5 1%, 8 0%, 12 0%, 10 0%, 26 0%, 9 0%

TOTAL_PATIENTS_HOSPITALIZED_1: nan 63%, 0.0 36%, -999999.0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HOSPITAL_PK | who | 189 | 0 | 393302 18; 390116 18; 391305 18; 390104 17 |
| COLLECTION_WEEK | date | 212 | 0 | 2020-05-10T00:00:00.000 27; 2020-05-31T00:00:00.000 24; 2020-04-19T00:00:00.000 24; 2020-07-12T00:00:00.000 23 |
| STATE | other | 1 | 0 | PA 2.0K |
| CCN | who | 189 | 0 | 393302 18; 390116 18; 391305 18; 390104 17 |
| HOSPITAL_NAME | who | 184 | 0 | UPMC CHILDREN'S HOSPITAL  18; SUBURBAN COMMUNITY HOSPIT 18; TROY COMMUNITY HOSPITAL 18; UPMC KANE 17 |
| ADDRESS | who | 182 | 0 | 1000 DUTCH RIDGE ROAD 30; 1500 FIFTH AVENUE 22; ONE HOSPITAL DRIVE 21; ONE MELLON WAY 21 |
| CITY | who | 131 | 0 | PHILADELPHIA 198; PITTSBURGH 133; ERIE 56; YORK 53 |
| ZIP | other | 159 | 0 | 19104 45; 15224 42; 19107 36; 15213 31 |
| HOSPITAL_SUBTYPE | category | 4 | 0 | Short Term 1.6K; Critical Access Hospitals 199; Long Term 157; Childrens Hospitals 59 |
| FIPS_CODE | other | 60 | 0 | 42003 240; 42101 218; 42091 121; 42049 69 |
| IS_METRO_MICRO | category | 2 | 0 | true 1.9K; false 130 |
| TOTAL_BEDS_7_DAY_COVERAGE | amount | 8 | 0 | 0 972; 7 806; 6 59; 1 47 |
| ALL_ADULT_HOSPITAL_BEDS_7_2 | category | 8 | 0 | 0 1.1K; 7 738; 6 34; 1 28 |
| ALL_ADULT_HOSPITAL_INPATIENT_4 | category | 8 | 0 | 7 1.6K; 0 313; 6 28; 4 16 |
| INPATIENT_BEDS_USED_7_DAY_2 | category | 8 | 0 | 7 1.7K; 0 151; 6 57; 5 29 |
| ALL_ADULT_HOSPITAL_INPATIENT_5 | category | 8 | 0 | 7 1.6K; 0 291; 6 32; 4 20 |
| TOTAL_ADULT_PATIENTS_4 | amount | 8 | 0 | 7 1.5K; 0 341; 6 56; 5 40 |
| TOTAL_ADULT_PATIENTS_5 | amount | 8 | 0 | 7 1.6K; 0 278; 6 36; 5 19 |
| TOTAL_PEDIATRIC_PATIENTS_4 | amount | 8 | 0 | 7 1.5K; 0 341; 6 58; 5 40 |
| TOTAL_PEDIATRIC_PATIENTS_5 | amount | 8 | 0 | 7 1.6K; 0 279; 6 35; 5 20 |
| INPATIENT_BEDS_7_DAY_COVERAGE | category | 8 | 0 | 7 1.7K; 0 151; 6 57; 5 29 |
| TOTAL_ICU_BEDS_7_DAY_COVERAGE | amount | 8 | 0 | 7 1.8K; 6 87; 0 37; 4 28 |
| TOTAL_STAFFED_ADULT_ICU_BEDS_2 | amount | 8 | 0 | 7 1.6K; 0 324; 6 38; 4 17 |
| ICU_BEDS_USED_7_DAY_COVERAGE | category | 8 | 0 | 7 1.6K; 0 324; 6 38; 4 17 |
| STAFFED_ADULT_ICU_BED_2 | category | 8 | 0 | 7 1.6K; 0 324; 6 38; 4 17 |
| STAFFED_ICU_ADULT_PATIENTS_4 | category | 8 | 0 | 7 1.5K; 0 349; 6 54; 5 40 |
| STAFFED_ICU_ADULT_PATIENTS_5 | category | 8 | 0 | 7 1.6K; 0 324; 6 38; 4 17 |
| TOTAL_PATIENTS_HOSPITALIZED_4 | amount | 8 | 0 | 7 1.5K; 0 416; 6 34; 5 19 |
| ICU_PATIENTS_CONFIRMED_2 | category | 8 | 0 | 7 1.5K; 0 416; 6 34; 5 19 |
| TOTAL_PATIENTS_HOSPITALIZED_5 | amount | 8 | 0 | 0 1.3K; 7 616; 6 34; 1 23 |
| HHS_IDS | who | 181 | 0 | nan 40; [C393302-A] 18; [C390116-A] 18; [C391305-A] 18 |
| PREVIOUS_DAY_ADMISSION_ADULT_COVID_CONFIRMED_7_DAY_COVERAGE | category | 8 | 0 | 7 1.6K; 0 271; 6 37; 5 17 |
| PREVIOUS_DAY_ADMISSION_PEDIATRIC_COVID_CONFIRMED_7_DAY_COVERAGE | category | 8 | 0 | 7 1.6K; 0 299; 6 27; 4 14 |
| PREVIOUS_DAY_ADMISSION_ADULT_COVID_SUSPECTED_7_DAY_COVERAGE | category | 8 | 0 | 7 1.5K; 0 336; 6 58; 5 38 |
| PREVIOUS_DAY_ADMISSION_PEDIATRIC_COVID_SUSPECTED_7_DAY_COVERAGE | category | 8 | 0 | 7 1.5K; 0 361; 6 47; 5 34 |
| IS_CORRECTED | category | 2 | 0 | False 1.9K; True 88 |
| GEOCODED_HOSPITAL_ADDRESS | who | 176 | 0 | {"type": "Point", "coordi 30; {"type": "Point", "coordi 24; {"type": "Point", "coordi 24; {"type": "Point", "coordi 22 |
| COMPUTED_REGION_NMSQ_HQVV | other | 59 | 0 | 40 241; 13 213; 57 134; 30 69 |
| ALL_ADULT_HOSPITAL_INPATIENT | amount | 707 | 0 | nan 313; 0.0 60; 14.0 46; 25.0 43 |
| INPATIENT_BEDS_USED_7_DAY | amount | 1.1K | 0 | nan 151; -999999.0 58; 0.0 23; 18.0 11 |
| ALL_ADULT_HOSPITAL_INPATIENT_1 | amount | 1.0K | 0 | nan 291; 0.0 62; -999999.0 46; 15.7 10 |
| TOTAL_ADULT_PATIENTS | amount | 295 | 0 | -999999.0 550; 0.0 343; nan 341; 4.0 18 |
| TOTAL_ADULT_PATIENTS_1 | amount | 254 | 0 | -999999.0 589; 0.0 432; nan 278; 4.0 17 |
| TOTAL_PEDIATRIC_PATIENTS | amount | 37 | 0 | 0.0 1.4K; nan 341; -999999.0 196; 4.6 3 |
| TOTAL_PEDIATRIC_PATIENTS_1 | amount | 20 | 0 | 0.0 1.6K; nan 279; -999999.0 128; 5.4 1 |
| INPATIENT_BEDS_7_DAY_AVG | amount | 753 | 0 | nan 151; 25.0 57; 14.0 50; 20.0 42 |
| TOTAL_ICU_BEDS_7_DAY_AVG | amount | 395 | 0 | 0.0 522; 6.0 87; 12.0 70; 10.0 69 |
| TOTAL_STAFFED_ADULT_ICU_BEDS | amount | 289 | 0 | 0.0 518; nan 324; 6.0 84; 10.0 67 |
| ICU_BEDS_USED_7_DAY_AVG | amount | 404 | 0 | 0.0 491; nan 324; -999999.0 152; 6.0 18 |
| STAFFED_ADULT_ICU_BED | amount | 349 | 0 | 0.0 540; nan 324; -999999.0 142; 5.7 18 |
| STAFFED_ICU_ADULT_PATIENTS | amount | 90 | 0 | 0.0 828; -999999.0 602; nan 349; 5.7 9 |
| STAFFED_ICU_ADULT_PATIENTS_1 | amount | 89 | 0 | 0.0 926; -999999.0 556; nan 324; 4.7 9 |
| TOTAL_PATIENTS_HOSPITALIZED | amount | 38 | 0 | 0.0 1.2K; nan 416; -999999.0 292; 6.0 4 |
| ICU_PATIENTS_CONFIRMED | amount | 5 | 0 | 0.0 1.5K; nan 416; -999999.0 119; 4.7 1 |
| ALL_ADULT_HOSPITAL_INPATIENT_2 | other | 733 | 0 | nan 313; 0 60; 98 45; 175 44 |
| INPATIENT_BEDS_USED_7_DAY_1 | other | 1.1K | 0 | nan 151; 0 23; 37 12; 66 11 |
| ALL_ADULT_HOSPITAL_INPATIENT_3 | other | 1.0K | 0 | nan 291; 0 62; 66 10; 33 10 |
| TOTAL_ADULT_PATIENTS_2 | amount | 301 | 0 | 0 343; nan 341; -999999 100; 5 43 |
| TOTAL_ADULT_PATIENTS_3 | amount | 272 | 0 | 0 432; nan 278; -999999 118; 4 42 |
| TOTAL_PEDIATRIC_PATIENTS_2 | amount | 57 | 0 | 0 1.4K; nan 341; -999999 108; 4 14 |
| TOTAL_PEDIATRIC_PATIENTS_3 | amount | 39 | 0 | 0 1.6K; nan 279; -999999 66; 7 10 |
| INPATIENT_BEDS_7_DAY_SUM | amount | 802 | 0 | nan 151; 175 53; 98 49; 140 42 |
| TOTAL_ICU_BEDS_7_DAY_SUM | amount | 414 | 0 | 0 522; 42 84; 84 68; 70 68 |
| TOTAL_STAFFED_ADULT_ICU_BEDS_1 | amount | 298 | 0 | 0 518; nan 324; 42 81; 70 67 |
| ICU_BEDS_USED_7_DAY_SUM | amount | 424 | 0 | 0 491; nan 324; 40 17; 42 17 |
| STAFFED_ADULT_ICU_BED_1 | other | 370 | 0 | 0 540; nan 324; 40 19; 42 18 |
| STAFFED_ICU_ADULT_PATIENTS_2 | other | 112 | 0 | 0 828; nan 349; -999999 160; 7 44 |
| STAFFED_ICU_ADULT_PATIENTS_3 | other | 109 | 0 | 0 926; nan 324; -999999 142; 5 51 |
| TOTAL_PATIENTS_HOSPITALIZED_2 | amount | 60 | 0 | 0 1.2K; nan 416; -999999 113; 7 27 |
| ICU_PATIENTS_CONFIRMED_1 | category | 23 | 0 | 0 1.5K; nan 416; -999999 56; 4 11 |
| PREVIOUS_DAY_ADMISSION_ADULT | other | 68 | 0 | 0 643; -999999 396; nan 271; 4 78 |
| PREVIOUS_DAY_ADMISSION_ADULT_1 | category | 4 | 0 | 0 1.6K; nan 345; -999999 42; 4 1 |
| PREVIOUS_DAY_ADMISSION_ADULT_2 | category | 10 | 0 | 0 1.4K; nan 360; -999999 220; 4 9 |
| PREVIOUS_DAY_ADMISSION_ADULT_3 | category | 11 | 0 | 0 1.3K; nan 359; -999999 280; 4 19 |
| PREVIOUS_DAY_ADMISSION_ADULT_4 | category | 13 | 0 | 0 1.3K; nan 354; -999999 295; 4 30 |
| PREVIOUS_DAY_ADMISSION_ADULT_5 | category | 21 | 0 | 0 1.1K; -999999 391; nan 350; 4 36 |
| PREVIOUS_DAY_ADMISSION_ADULT_6 | category | 27 | 0 | 0 1.0K; -999999 423; nan 342; 4 59 |
| PREVIOUS_DAY_ADMISSION_ADULT_7 | category | 28 | 0 | 0 960; -999999 462; nan 345; 4 76 |
| PREVIOUS_DAY_ADMISSION_ADULT_8 | category | 28 | 0 | 0 931; -999999 462; nan 348; 4 70 |
| PREVIOUS_DAY_ADMISSION_ADULT_9 | category | 22 | 0 | 0 1.6K; nan 318; -999999 58; 5 5 |
| PREVIOUS_DAY_ADMISSION | category | 17 | 0 | 0 1.6K; nan 299; -999999 76; 7 8 |
| PREVIOUS_DAY_COVID_ED_VISITS | other | 327 | 0 | 0 370; nan 367; -999999 66; 6 22 |
| PREVIOUS_DAY_ADMISSION_ADULT_10 | other | 138 | 0 | 0 943; nan 336; -999999 219; 8 25 |
| PREVIOUS_DAY_ADMISSION_ADULT_11 | category | 5 | 0 | 0 1.5K; nan 408; -999999 98; 4 8 |
| PREVIOUS_DAY_ADMISSION_ADULT_12 | category | 25 | 0 | 0 1.3K; nan 421; -999999 209; 4 27 |
| PREVIOUS_DAY_ADMISSION_ADULT_13 | category | 26 | 0 | 0 1.2K; nan 417; -999999 195; 4 30 |
| PREVIOUS_DAY_ADMISSION_ADULT_14 | category | 23 | 0 | 0 1.2K; nan 412; -999999 205; 4 32 |
| PREVIOUS_DAY_ADMISSION_ADULT_15 | category | 35 | 0 | 0 1.1K; nan 409; -999999 207; 4 35 |
| PREVIOUS_DAY_ADMISSION_ADULT_16 | category | 47 | 0 | 0 1.1K; nan 406; -999999 210; 5 31 |
| PREVIOUS_DAY_ADMISSION_ADULT_17 | category | 46 | 0 | 0 1.1K; nan 405; -999999 206; 5 28 |
| PREVIOUS_DAY_ADMISSION_ADULT_18 | category | 47 | 0 | 0 1.1K; nan 402; -999999 204; 4 40 |
| PREVIOUS_DAY_ADMISSION_ADULT_19 | category | 18 | 0 | 0 1.5K; nan 382; -999999 57; 9 5 |
| PREVIOUS_DAY_ADMISSION_1 | category | 36 | 0 | 0 1.4K; nan 361; -999999 104; 9 11 |
| PREVIOUS_DAY_TOTAL_ED_VISITS | amount | 871 | 0 | nan 360; 0 290; 157 9; 544 8 |
| PREVIOUS_DAY_ADMISSION_2 | category | 24 | 0 | 0 1.3K; nan 416; -999999 167; 6 16 |
| TOTAL_BEDS_7_DAY_AVG | amount | 414 | 0 | nan 972; 25.0 37; 30.0 35; 0.0 20 |
| TOTAL_BEDS_7_DAY_SUM | amount | 501 | 0 | nan 972; 210 31; 175 26; 0 20 |
| ALL_ADULT_HOSPITAL_BEDS_7 | amount | 364 | 0 | nan 1.1K; 0.0 36; 25.0 33; 30.0 29 |
| ALL_ADULT_HOSPITAL_BEDS_7_1 | other | 424 | 0 | nan 1.1K; 0 36; 175 27; 210 26 |
| TOTAL_PATIENTS_HOSPITALIZED_1 | category | 3 | 0 | nan 1.3K; 0.0 716; -999999.0 20 |
| TOTAL_PATIENTS_HOSPITALIZED_3 | amount | 6 | 0 | nan 1.3K; 0 716; -999999 16; 4 2 |
| PREVIOUS_WEEK_PERSONNEL_COVID_VACCINATED_DOSES_ADMINISTERED_7_DAY | other | 90 | 0 | nan 1.5K; 0 357; -999999 39; 8 7 |
| TOTAL_PERSONNEL_COVID_VACCINATED_DOSES_NONE_7_DAY | amount | 236 | 0 | nan 1.5K; 0 158; 39 13; -999999 10 |
| TOTAL_PERSONNEL_COVID_VACCINATED_DOSES_ONE_7_DAY | amount | 203 | 0 | nan 1.5K; 0 199; -999999 38; 18 7 |
| TOTAL_PERSONNEL_COVID_VACCINATED_DOSES_ALL_7_DAY | amount | 296 | 0 | nan 1.5K; 0 156; 259 6; 284 4 |
| PREVIOUS_WEEK_PATIENTS_COVID_VACCINATED_DOSES_ONE_7_DAY | other | 90 | 0 | nan 1.4K; 0 419; -999999 35; 5 5 |
| PREVIOUS_WEEK_PATIENTS_COVID_VACCINATED_DOSES_ALL_7_DAY | other | 80 | 0 | nan 1.4K; 0 444; -999999 26; 4 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:45:57.78554 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9e42df68-0046-4a17-90d7-f 2.0K |
| SRC_SHA256 | who | 1 | 0 | 4567b45a6e6d6b23675842912 2.0K |
