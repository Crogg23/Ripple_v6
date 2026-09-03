# FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER

rows 3.0K  columns 59  scan 5.5s

roles: amount 30, audit 2, category 1, date 1, id 4, other 20, state 1, who 2

## when

_INGESTED_AT
  2026      3.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RNDRNG_PRVDR_RUCA | 3.0K | 1 | 1 | 10 | 99 | 7.8K |
| TOT_PYMT_AMT | 3.0K | 109.8K | 20.90M | 316.17M | 1.09B | 129.31B |
| TOT_MDCR_PYMT_AMT | 3.0K | 84.9K | 17.27M | 240.48M | 865.43M | 107.02B |
| BENE_AVG_AGE | 3.0K | 34.25 | 75.80 | 80.19 | 81.88 | 229.4K |
| BENE_CC_BH_ADHD_OTHCD_V1_PCT | 3.0K | 0 | 0.02 | 0.11 | 0.42 | 64.77 |
| BENE_CC_BH_ALCOHOL_DRUG_V1_PCT | 3.0K | 0 | 0.13 | 0.40 | 0.75 | 426.51 |

## who

RNDRNG_PRVDR_ORG_NAME by rows
         6  Memorial Hospital
         4  St Mary's Medical Center
         4  Mercy Medical Center
         4  Good Samaritan Hospital
         4  St Joseph Medical Center
         3  Marion General Hospital
         3  Memorial Medical Center
         3  Northwest Medical Center
         3  Grady Memorial Hospital
         3  St Lukes Hospital
         3  St Joseph Hospital
         3  Saint Francis Medical Center
         3  St Mary Medical Center
         3  St Josephs Hospital
         3  Doctors Hospital
         3  Mercy Hospital
         3  Holy Cross Hospital
         2  Community Hospital
         2  Good Samaritan Medical Center
         2  South Shore Hospital

RNDRNG_PRVDR_ORG_NAME by dollars
       1.09B        1 rows  New York-Presbyterian Hospital
     900.72M        1 rows  Nyu Langone Hospitals
     683.84M        1 rows  Stanford Health Care
     628.34M        1 rows  Mayo Clinic Hospital Rochester
     620.28M        1 rows  Cedars-Sinai Medical Center
     582.90M        1 rows  Adventhealth Orlando
     549.86M        1 rows  Massachusetts General Hospital
     522.16M        1 rows  Ucsf Medical Center
     475.85M        1 rows  Mount Sinai Hospital
     469.15M        1 rows  Johns Hopkins Hospital, The
     455.46M        1 rows  Brigham And Women's Hospital
     453.32M        1 rows  Cleveland Clinic
     412.56M        1 rows  University Of Maryland Medical Center
     406.06M        1 rows  Barnes Jewish Hospital
     399.27M        2 rows  Methodist Hospital
     386.80M        1 rows  Stony Brook University Hospital
     379.07M        1 rows  Hospital Of Univ Of Pennsylvania
     367.82M        1 rows  University Of California Davis Medical Center
     365.26M        1 rows  Beth Israel Deaconess Medical Center
     358.35M        1 rows  Northwestern Memorial Hospital

RNDRNG_PRVDR_CITY by rows
        27  Chicago
        19  Houston
        15  Oklahoma City
        15  Los Angeles
        14  Dallas
        14  Phoenix
        13  Philadelphia
        13  Baltimore
        12  Columbia
        12  Greenville
        12  Columbus
        11  Springfield
        10  Austin
        10  Jackson
        10  New York
        10  Washington
        10  San Antonio
        10  San Francisco
         9  Indianapolis
         9  Miami

RNDRNG_PRVDR_CITY by dollars
       3.17B       10 rows  New York
       1.80B       13 rows  Baltimore
       1.76B        9 rows  Boston
       1.62B       15 rows  Los Angeles
       1.42B       27 rows  Chicago
       1.33B       19 rows  Houston
       1.20B       13 rows  Philadelphia
       1.04B        8 rows  Rochester
     943.39M       10 rows  San Francisco
     940.11M       14 rows  Dallas
     823.38M        3 rows  Orlando
     822.74M       14 rows  Phoenix
     820.82M       11 rows  Springfield
     795.29M        6 rows  Atlanta
     786.70M        9 rows  Jacksonville
     786.36M       10 rows  San Antonio
     767.11M        7 rows  Cleveland
     757.17M       12 rows  Columbus
     751.43M        6 rows  Saint Louis
     740.86M       10 rows  Washington

## who x when

RNDRNG_PRVDR_ORG_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = TOT_PYMT_AMT
  Adventhealth Orlando                      2026:582.90M
  Cedars-Sinai Medical Center               2026:620.28M
  Community Hospital                        2026:100.54M
  Doctors Hospital                          2026:88.38M
  Good Samaritan Hospital                   2026:191.84M
  Good Samaritan Medical Center             2026:82.16M
  Grady Memorial Hospital                   2026:143.76M
  Holy Cross Hospital                       2026:158.69M
  Johns Hopkins Hospital, The               2026:469.15M
  Marion General Hospital                   2026:40.90M
  Massachusetts General Hospital            2026:549.86M
  Mayo Clinic Hospital Rochester            2026:628.34M
  Memorial Hospital                         2026:70.63M
  Memorial Medical Center                   2026:252.56M
  Mercy Hospital                            2026:147.15M
  Mercy Medical Center                      2026:155.50M
  Mount Sinai Hospital                      2026:475.85M
  New York-Presbyterian Hospital            2026:1.09B
  Northwest Medical Center                  2026:76.03M
  Nyu Langone Hospitals                     2026:900.72M
  Saint Francis Medical Center              2026:271.51M
  South Shore Hospital                      2026:161.34M
  St Joseph Hospital                        2026:82.64M
  St Joseph Medical Center                  2026:151.45M
  St Josephs Hospital                       2026:147.13M
  St Lukes Hospital                         2026:166.34M
  St Mary Medical Center                    2026:133.36M
  St Mary's Medical Center                  2026:138.26M
  Stanford Health Care                      2026:683.84M
  Ucsf Medical Center                       2026:522.16M

RNDRNG_PRVDR_CITY by _INGESTED_AT  LOAD STAMP, not an event date, dollars = TOT_PYMT_AMT
  Atlanta                                   2026:795.29M
  Austin                                    2026:387.99M
  Baltimore                                 2026:1.80B
  Boston                                    2026:1.76B
  Chicago                                   2026:1.42B
  Cleveland                                 2026:767.11M
  Columbia                                  2026:531.40M
  Columbus                                  2026:757.17M
  Dallas                                    2026:940.11M
  Greenville                                2026:491.76M
  Houston                                   2026:1.33B
  Indianapolis                              2026:655.69M
  Jackson                                   2026:514.21M
  Jacksonville                              2026:786.70M
  Los Angeles                               2026:1.62B
  Miami                                     2026:422.62M
  New York                                  2026:3.17B
  Oklahoma City                             2026:618.48M
  Orlando                                   2026:823.38M
  Philadelphia                              2026:1.20B
  Phoenix                                   2026:822.74M
  Rochester                                 2026:1.04B
  Saint Louis                               2026:751.43M
  San Antonio                               2026:786.36M
  San Francisco                             2026:943.39M
  Springfield                               2026:820.82M
  Washington                                2026:740.86M

## where

RNDRNG_PRVDR_STATE_ABRVTN: CA 276, TX 272, FL 168, PA 133, NY 128, OH 118, IL 116, GA 94, MI 89, NC 82, IN 82, LA 81

## what

RNDRNG_PRVDR_RUCA_DESC: Metropolitan area core: primar 68%, Micropolitan area core: primar 16%, Small town core: primary flow  7%, Metropolitan area high commuti 3%, Secondary flow 30% to <50% to  2%, Secondary flow 30% to <50% to  1%, Rural areas: primary flow to a 1%, Micropolitan high commuting: p 1%, Unknown 0%, Small town high commuting: pri 0%, Metropolitan area low commutin 0%, Secondary flow 30% to <50% to  0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RNDRNG_PRVDR_CCN | id | 3.0K | 0 | 670333 16; 670322 16; 670321 16; 670320 16 |
| RNDRNG_PRVDR_ORG_NAME | who | 3.0K | 0 | Westover Hills Baptist Ho 16; Legent Surgical Hospital  16; Advanced Dallas Hospitals 16; East Houston Medical Cent 16 |
| RNDRNG_PRVDR_ST | id | 3.0K | 0 | 3011 W Loop 1604 N 16; 4100 Mapleshade Lane 16; 7502 Greenville Avenue 16; 15149 Wallisville Road 16 |
| RNDRNG_PRVDR_CITY | who | 1.8K | 0 | Chicago 30; Houston 29; Dallas 25; Oklahoma City 24 |
| RNDRNG_PRVDR_ZIP5 | other | 2.9K | 0 | 75231 17; 75093 17; 25301 17; 77030 17 |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 51 | 0 | CA 276; TX 272; FL 168; PA 133 |
| RNDRNG_PRVDR_STATE_FIPS | other | 51 | 0 | 06 276; 48 272; 12 168; 42 133 |
| RNDRNG_PRVDR_RUCA | amount | 19 | 0 | 1 2.1K; 4 482; 7 198; 2 100 |
| RNDRNG_PRVDR_RUCA_DESC | category | 15 | 0 | Metropolitan area core: p 2.1K; Micropolitan area core: p 482; Small town core: primary  198; Metropolitan area high co 100 |
| TOT_BENES | other | 2.0K | 0 | 128 17; 17 17; 33 17; 366 17 |
| TOT_SUBMTD_CVRD_CHRG | id | 3.1K | 0 | 17963181 16; 5450252 16; 5929691 16; 1177892 16 |
| TOT_PYMT_AMT | amount | 3.1K | 0 | 1510417 16; 637794 16; 567032 16; 113380 16 |
| TOT_MDCR_PYMT_AMT | amount | 3.0K | 0 | 1245187 16; 600258 16; 487237 16; 90532 16 |
| TOT_DSCHRGS | other | 2.2K | 0 | 20 17; 35 17; 135 16; 30 16 |
| TOT_CVRD_DAYS | other | 2.7K | 0 | 44 17; 507 16; 47 16; 389 16 |
| TOT_DAYS | other | 2.8K | 0 | 48 17; 525 16; 47 16; 393 16 |
| BENE_AVG_AGE | amount | 3.0K | 0 | 76.7109375 16; 71.333333333 16; 72.701754386 16; 75.2 16 |
| BENE_AGE_LT_65_CNT | other | 632 | 283 | 24 32; 34 26; 14 24; 20 22 |
| BENE_AGE_65_74_CNT | other | 1.2K | 46 | 53 18; 45 17; 12 17; 14 16 |
| BENE_AGE_75_84_CNT | other | 1.3K | 63 | 41 18; 42 17; 22 17; 51 17 |
| BENE_AGE_GT_84_CNT | other | 972 | 291 | 67 16; 46 16; 11 15; 161 15 |
| BENE_FEML_CNT | other | 1.6K | 46 | 52 17; 64 17; 78 16; 19 16 |
| BENE_MALE_CNT | other | 1.5K | 46 | 14 17; 37 17; 50 16; 34 16 |
| BENE_RACE_WHT_CNT | other | 1.9K | 31 | 324 17; 74 16; 22 16; 15 16 |
| BENE_RACE_BLACK_CNT | other | 606 | 881 | 13 37; 14 37; 11 36; 21 31 |
| BENE_RACE_API_CNT | other | 269 | 1.7K | 11 57; 12 47; 14 46; 13 44 |
| BENE_RACE_HSPNC_CNT | other | 473 | 1.0K | 11 44; 17 43; 19 41; 12 40 |
| BENE_RACE_NATIND_CNT | other | 121 | 2.7K | 11 26; 13 16; 18 13; 12 12 |
| BENE_RACE_OTHR_CNT | other | 147 | 2.1K | 13 54; 15 45; 12 42; 11 40 |
| BENE_DUAL_CNT | other | 1.0K | 145 | 20 19; 54 18; 168 17; 41 17 |
| BENE_NDUAL_CNT | other | 1.8K | 145 | 320 16; 113 16; 706 16; 107 15 |
| BENE_CC_BH_ADHD_OTHCD_V1_PCT | amount | 2.5K | 0 | 0 133; 0.0078125 16; 0.0117647059 16; 0.0163934426 16 |
| BENE_CC_BH_ALCOHOL_DRUG_V1_PCT | amount | 2.8K | 0 | 0.0588235294 17; 0.1515151515 17; 0 17; 0.0703125 16 |
| BENE_CC_BH_TOBACCO_V1_PCT | amount | 2.8K | 0 | 0.1111111111 17; 0.125 16; 0.1481481481 16; 0.298245614 16 |
| BENE_CC_BH_ALZ_NONALZDEM_V2_PCT | amount | 2.9K | 0 | 0 18; 0.0588235294 17; 0.2734375 16; 0.0740740741 16 |
| BENE_CC_BH_ANXIETY_V1_PCT | amount | 2.8K | 0 | 0.75 19; 0.34375 16; 0.4814814815 16; 0.701754386 16 |
| BENE_CC_BH_BIPOLAR_V1_PCT | amount | 2.8K | 0 | 0 21; 0.0588235294 17; 0.078125 16; 0.037037037 16 |
| BENE_CC_BH_MOOD_V2_PCT | amount | 2.9K | 0 | 0.75 21; 0.3333333333 17; 0.2 17; 0.3529411765 17 |
| BENE_CC_BH_DEPRESS_V1_PCT | amount | 2.8K | 0 | 0.3529411765 17; 0.3125 16; 0.2962962963 16; 0.5614035088 16 |
| BENE_CC_BH_PD_V1_PCT | amount | 2.5K | 0 | 0 134; 0.023255814 16; 0.0081967213 16; 0.015625 15 |
| BENE_CC_BH_PTSD_V1_PCT | amount | 2.6K | 0 | 0 86; 0.0298507463 16; 0.0303030303 16; 0.0253164557 16 |
| BENE_CC_BH_SCHIZO_OTHPSY_V1_PCT | amount | 2.7K | 0 | 0 57; 0.0078125 16; 0.037037037 16; 0.0303030303 16 |
| BENE_CC_PH_ASTHMA_V2_PCT | amount | 2.8K | 0 | 0.1328125 16; 0.0740740741 16; 0.1403508772 16; 0.0666666667 16 |
| BENE_CC_PH_AFIB_V2_PCT | amount | 2.9K | 0 | 0.4 17; 0.3333333333 17; 0.3828125 16; 0.1111111111 16 |
| BENE_CC_PH_CANCER6_V2_PCT | amount | 2.8K | 0 | 0.1875 16; 0.2222222222 16; 0.1228070175 16; 0.0666666667 16 |
| BENE_CC_PH_CKD_V2_PCT | amount | 2.9K | 0 | 0.2 17; 0.5151515152 17; 0.4609375 16; 0.1851851852 16 |
| BENE_CC_PH_COPD_V2_PCT | amount | 2.8K | 0 | 0.2265625 16; 0.037037037 16; 0.4035087719 16; 0.4666666667 16 |
| BENE_CC_PH_DIABETES_V2_PCT | amount | 2.9K | 0 | 0.4921875 16; 0.2222222222 16; 0.6666666667 16; 0.2666666667 16 |
| BENE_CC_PH_HF_NONIHD_V2_PCT | amount | 3.0K | 0 | 0.5 17; 0.4609375 16; 0.1111111111 16; 0.5438596491 16 |
| BENE_CC_PH_HYPERLIPIDEMIA_V2_PCT | amount | 536 | 0 | 0.75 2.5K; 0.6666666667 6; 0.6842105263 6; 0.7272727273 5 |
| BENE_CC_PH_HYPERTENSION_V2_PCT | amount | 48 | 0 | 0.75 3.0K; 0.6842105263 3; 0.6617647059 2; 0.6785714286 1 |
| BENE_CC_PH_ISCHEMICHEART_V2_PCT | amount | 2.8K | 0 | 0.5 20; 0.3333333333 18; 0.75 17; 0.4285714286 17 |
| BENE_CC_PH_OSTEOPOROSIS_V2_PCT | amount | 2.8K | 0 | 0.1666666667 17; 0.171875 16; 0.1851851852 16; 0.1754385965 16 |
| BENE_CC_PH_PARKINSON_V2_PCT | amount | 2.6K | 0 | 0 55; 0.0588235294 17; 0.0434782609 17; 0.0303030303 16 |
| BENE_CC_PH_ARTHRITIS_V2_PCT | amount | 2.8K | 0 | 0.75 134; 0.5 17; 0.5703125 15; 0.5614035088 15 |
| BENE_CC_PH_STROKE_TIA_V2_PCT | amount | 2.8K | 0 | 0.1176470588 18; 0.1052631579 17; 0 17; 0.1640625 16 |
| BENE_AVG_RISK_SCRE | amount | 3.0K | 0 | 1.9036354167 16; 1.1055925926 16; 3.1085861111 16; 1.3080722222 16 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 12:06:20.940 3.0K |
| _SOURCE_RUN_ID | audit id | 3.0K | 0 | 055a82a3-26de-4519-888f-7 16; 18f46be4-864a-4664-a003-0 16; 2cfa0858-6431-4fbe-8d32-6 16; d6bce9ed-ae8e-4f01-b308-e 16 |
