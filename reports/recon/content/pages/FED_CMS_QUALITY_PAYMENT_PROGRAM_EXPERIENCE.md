# FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE

rows 503.9K  columns 214  scan 9.7s

roles: amount 54, audit 2, category 116, date 1, empty 6, id 1, other 30, state 1, who 5

## when

_INGESTED_AT
  2026    503.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ALLOWED_CHARGES | 503.9K | 5.9K | 10.34M | 329.27M | 385.17M | 17319.90B |
| DUAL_ELIGIBILITY_RATIO | 503.9K | 0 | 0.16 | 0.80 | 1 | 100.9K |
| FINAL_SCORE | 503.9K | 0 | 87.53 | 100 | 100 | 42.89M |
| PAYMENT_ADJUSTMENT_PERCENTAGE | 503.9K | -9 | 0.53 | 1.05 | 1.05 | 122.6K |
| COMPLEX_PATIENT_BONUS | 503.9K | 0 | 0.87 | 10.00 | 10 | 1.25M |
| QUALITY_CATEGORY_SCORE | 503.9K | 0 | 77.02 | 100 | 100 | 34.75M |

## who

PROVIDER_KEY by rows
         1  000022109
         1  000017349
         1  000020248
         1  000022728
         1  000022433
         1  000023480
         1  000023849
         1  000026771
         1  000023927
         1  000026821
         1  000024954
         1  000027352
         1  000025387
         1  000021778
         1  000017500
         1  000017271
         1  000023301
         1  000021313
         1  000019946
         1  000019781

PROVIDER_KEY by dollars
        1.05        1 rows  000017513
        1.05        1 rows  000001613
        1.05        1 rows  000001028
        1.05        1 rows  000070667
        1.05        1 rows  000056555
        1.05        1 rows  000003510
        1.05        1 rows  000053072
        1.05        1 rows  000001577
        1.05        1 rows  000029495
        1.05        1 rows  000030438
        1.05        1 rows  000047118
        1.05        1 rows  000035326
        1.05        1 rows  000077691
        1.05        1 rows  000072866
        1.05        1 rows  000067725
        1.05        1 rows  000039431
        1.05        1 rows  000023340
        1.05        1 rows  000023289
        1.05        1 rows  000038007
        1.05        1 rows  000026856

SERVICES by rows
      5.4K  3081473
      4.6K  3477198
      3.9K  935212
      3.3K  2054550
      3.0K  800968
      2.8K  970284
      2.7K  1451251
      2.7K  1078560
      2.7K  813339
      2.5K  1183394
      2.4K  1633627
      2.4K  894157
      2.4K  750380
      2.3K  384645
      2.3K  741021
      2.2K  1357017
      2.2K  949467
      2.1K  508925
      2.1K  942619
      2.0K  2566473

SERVICES by dollars
        4.1K     5.4K rows  3081473
        3.1K     4.6K rows  3477198
        2.7K     3.3K rows  2054550
        2.4K     2.3K rows  741021
        2.3K     3.0K rows  800968
        2.3K     2.8K rows  970284
        2.1K     2.0K rows  884962
        2.0K     2.1K rows  508925
        1.7K     1.6K rows  826354
        1.7K     1.9K rows  802715
        1.6K     1.7K rows  928516
        1.6K     2.0K rows  791299
        1.5K     1.5K rows  911848
        1.5K     1.8K rows  506009
        1.4K     2.5K rows  1183394
        1.4K     2.3K rows  384645
        1.3K     1.6K rows  601987
        1.3K     1.4K rows  412103
        1.3K     1.2K rows  485922
        1.2K     2.4K rows  750380

CLINICIAN_SPECIALTY by rows
     72.8K  Nurse Practitioner
     50.6K  Physician Assistant
     32.0K  Physician/Internal Medicine
     26.4K  Physician/Emergency Medicine
     26.2K  Physician/Diagnostic Radiology
     22.5K  Physician/Family Practice
     17.7K  Physical Therapist in Private Practice
     17.5K  Certified Registered Nurse Anesthetist (CRNA)
     15.3K  Physician/Anesthesiology
     13.4K  Physician/Ophthalmology
     13.0K  Physician/Orthopedic Surgery
     11.4K  Physician/Cardiovascular Disease (Cardiology)
     10.8K  Physician/Obstetrics/Gynecology
      9.9K  Physician/Hospitalist 
      9.8K  Physician/General Surgery
      9.4K  Physician/Dermatology
      8.7K  Physician/Neurology
      8.1K  Physician/Gastroenterology
      7.9K  Podiatry
      7.6K  Optometry

CLINICIAN_SPECIALTY by dollars
       24.8K    72.8K rows  Nurse Practitioner
       22.2K    50.6K rows  Physician Assistant
       14.0K    26.4K rows  Physician/Emergency Medicine
        6.7K    26.2K rows  Physician/Diagnostic Radiology
        6.0K    32.0K rows  Physician/Internal Medicine
        5.0K    17.5K rows  Certified Registered Nurse Anesthetist (CRNA)
        4.9K    22.5K rows  Physician/Family Practice
        4.7K     9.9K rows  Physician/Hospitalist 
        4.1K    10.8K rows  Physician/Obstetrics/Gynecology
        3.6K    15.3K rows  Physician/Anesthesiology
        3.5K     9.8K rows  Physician/General Surgery
        3.3K    17.7K rows  Physical Therapist in Private Practice
        3.0K    13.4K rows  Physician/Ophthalmology
        2.9K    11.4K rows  Physician/Cardiovascular Disease (Cardiology)
        2.7K     7.6K rows  Physician/Pathology
        2.2K     5.8K rows  Physician/Hematology-Oncology
        2.2K     8.1K rows  Physician/Gastroenterology
        1.8K     7.3K rows  Physician/Psychiatry
        1.4K     3.3K rows  Physician/Pediatric Medicine
        1.4K     4.0K rows  Licensed Clinical Social Worker

PI_MEASURE_TYPE_19 by rows
     20.0K  Required

PI_MEASURE_TYPE_19 by dollars
        8.4K    20.0K rows  Required

## who x when

PROVIDER_KEY by _INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYMENT_ADJUSTMENT_PERCENTAGE
  000001028                                 2026:1.05
  000001577                                 2026:1.05
  000001613                                 2026:1.05
  000003510                                 2026:1.05
  000017271                                 2026:0.59
  000017349                                 2026:0.87
  000017500                                 2026:0.97
  000017513                                 2026:1.05
  000019781                                 2026:0.44
  000019946                                 2026:0.67
  000020248                                 2026:0.75
  000021313                                 2026:0.22
  000021778                                 2026:-3.79
  000022109                                 2026:0.46
  000022433                                 2026:0.85
  000022728                                 2026:0.51
  000023301                                 2026:0.99
  000023480                                 2026:0.67
  000023849                                 2026:1.01
  000023927                                 2026:1.05
  000024954                                 2026:0.55
  000025387                                 2026:0.76
  000026771                                 2026:0.43
  000026821                                 2026:0.51
  000027352                                 2026:0.98
  000029495                                 2026:1.05
  000030438                                 2026:1.05
  000053072                                 2026:1.05
  000056555                                 2026:1.05
  000070667                                 2026:1.05

SERVICES by _INGESTED_AT  LOAD STAMP, not an event date, dollars = PAYMENT_ADJUSTMENT_PERCENTAGE
  1078560                                   2026:1.0K
  1183394                                   2026:1.4K
  1357017                                   2026:936.60
  1451251                                   2026:961.80
  1633627                                   2026:1.0K
  2054550                                   2026:2.7K
  2566473                                   2026:973.44
  3081473                                   2026:4.1K
  3477198                                   2026:3.1K
  384645                                    2026:1.4K
  412103                                    2026:1.3K
  485922                                    2026:1.3K
  506009                                    2026:1.5K
  508925                                    2026:2.0K
  601987                                    2026:1.3K
  741021                                    2026:2.4K
  750380                                    2026:1.2K
  791299                                    2026:1.6K
  800968                                    2026:2.3K
  802715                                    2026:1.7K
  813339                                    2026:880.44
  826354                                    2026:1.7K
  884962                                    2026:2.1K
  894157                                    2026:937.17
  911848                                    2026:1.5K
  928516                                    2026:1.6K
  935212                                    2026:976.75
  942619                                    2026:734.65
  949467                                    2026:1.0K
  970284                                    2026:2.3K

## where

PRACTICE_STATE_OR_US_TERRITORY: CA 47.7K, FL 40.7K, NY 36.4K, TX 33.3K, PA 26.7K, IL 20.5K, GA 18.2K, NC 18.1K, OH 16.6K, NJ 15.8K, MD 13.9K, VA 13.6K

## what

CLINICIAN_TYPE: Doctor of Medicine 64%, Nurse Practitioner 15%, Physician Assistant 10%, Physical Therapist  4%, Certified Registered Nurse Ane 3%, Doctor of Optometry 2%, Clinical Social Worker  1%, Clinical Psychologist 1%, Occupational Therapist 0%, Qualified Audiologist 0%, Certified Nurse-Midwife 0%, Anesthesiologist Assistant 0%

YEARS_IN_MEDICARE: 21 13%, 15 11%, 20 10%, 9 9%, 6 8%, 10 7%, 7 7%, 11 7%, 2 7%, 14 7%, 17 7%, 4 7%

NON_REPORTING: False 94%, True 6%

PARTICIPATION_OPTION: Group 72%, APM Entity 20%, Individual 9%, Subgroup 0%, Virtual Group 0%

REPORTING_OPTION: Traditional MIPS 78%, APM Performance Pathway 19%, MIPS Value Pathways 2%

MIPS_VALUE_PATHWAY_ID: G0058 30%, M0005 18%, G0059 16%, M0001 13%, M0004 7%, G0057 4%, M1367 4%, G0055 3%, M1366 2%, M1370 1%, M1368 1%, M0002 1%

MIPS_VALUE_PATHWAY_TITLE: Improving Care for Lower Extre 30%, Value in Primary Care 18%, Patient Safety and Support of  16%, Advancing Cancer Care 13%, Supportive Care for Neurodegen 7%, Adopting Best Practices and Pr 4%, Quality Care for the Treatment 4%, Advancing Care for Heart Disea 3%, Focusing on Womenâs Health 2%, Rehabilitative Support for Mus 1%, Prevention and Treatment of In 1%, Optimal Care for Kidney Health 1%

OPTED_INTO_MIPS: False 99%, True 1%

SMALL_PRACTICE_STATUS: False 86%, True 14%

RURAL_STATUS: False 89%, True 11%

HEALTH_PROFESSIONAL_SHORTAGE_AREA_STATUS: False 83%, True 17%

AMBULATORY_SURGICAL_CENTER_BASED_STATUS: False 100%, True 0%

HOSPITAL_BASED_STATUS: False 68%, True 32%

NON_PATIENT_FACING_STATUS: False 84%, True 16%

FACILITY_BASED_STATUS: False 88%, True 12%

RECEIVED_FACILITY_SCORE: False 96%, True 4%

SAFETY_NET_STATUS: False 79%, True 21%

EXTREME_UNCONTROLLABLE_CIRCUMSTANCE_EUC: False 84%, True 16%

QUALITY_REWEIGHTING_EUC: False 90%, True 10%

QUALITY_MEASURE_COLLECTION_TYPE_1: eCQM 42%, CMS Web Interface Measure 19%, MIPS CQM 17%, Administrative Claims Measure 14%, QCDR Measure 6%, Medicare Part B Claims Measure 1%, CAHPS Measure 0%

QUALITY_MEASURE_COLLECTION_TYPE_2: eCQM 43%, CMS Web Interface Measure 20%, MIPS CQM 17%, Administrative Claims Measure 13%, QCDR Measure 7%, Medicare Part B Claims Measure 1%, CAHPS Measure 1%

QUALITY_MEASURE_COLLECTION_TYPE_3: eCQM 42%, CMS Web Interface Measure 18%, MIPS CQM 16%, Administrative Claims Measure 14%, QCDR Measure 7%, CAHPS Measure 1%, Medicare Part B Claims Measure 0%

QUALITY_MEASURE_COLLECTION_TYPE_4: eCQM 42%, CMS Web Interface Measure 20%, MIPS CQM 18%, Administrative Claims Measure 12%, QCDR Measure 8%, CAHPS Measure 1%, Medicare Part B Claims Measure 0%

QUALITY_MEASURE_COLLECTION_TYPE_5: eCQM 46%, CMS Web Interface Measure 20%, MIPS CQM 17%, Administrative Claims Measure 9%, QCDR Measure 7%, CAHPS Measure 1%, Medicare Part B Claims Measure 0%

QUALITY_MEASURE_COLLECTION_TYPE_6: eCQM 37%, CMS Web Interface Measure 20%, Administrative Claims Measure 16%, MIPS CQM 16%, QCDR Measure 9%, CAHPS Measure 2%, Medicare Part B Claims Measure 0%

QUALITY_MEASURE_COLLECTION_TYPE_7: Administrative Claims Measure 36%, eCQM 29%, CMS Web Interface Measure 26%, MIPS CQM 6%, QCDR Measure 3%, CAHPS Measure 1%, Medicare Part B Claims Measure 0%

QUALITY_MEASURE_COLLECTION_TYPE_8: Administrative Claims Measure 52%, CMS Web Interface Measure 24%, eCQM 17%, CAHPS Measure 4%, MIPS CQM 3%, QCDR Measure 0%, Medicare Part B Claims Measure 0%

QUALITY_MEASURE_ID_9: 479 17%, 492 16%, 321 16%, 484 13%, 480 10%, 110 7%, 488 7%, 226 6%, 134 3%, 379 2%, 236 1%, 001 1%

QUALITY_MEASURE_COLLECTION_TYPE_9: Administrative Claims Measure 55%, CAHPS Measure 16%, CMS Web Interface Measure 16%, eCQM 13%, MIPS CQM 1%

QUALITY_MEASURE_ID_10: 484 32%, 488 23%, 479 18%, 492 8%, 321 8%, 480 5%, 226 3%, 110 1%, 236 1%, 001 1%, 134 0%, 007 0%

QUALITY_MEASURE_COLLECTION_TYPE_10: Administrative Claims Measure 63%, eCQM 24%, CAHPS Measure 8%, CMS Web Interface Measure 5%, MIPS CQM 0%

QUALITY_MEASURE_ID_11: 484 49%, 479 29%, 321 18%, 226 3%, 110 2%, 113 0%

QUALITY_MEASURE_COLLECTION_TYPE_11: Administrative Claims Measure 77%, CAHPS Measure 18%, CMS Web Interface Measure 5%

PI_REWEIGHTING_EUC: False 91%, True 9%

PI_REWEIGHTING_HARDSHIP_EXCEPTION: False 97%, True 3%

PI_REWEIGHTING_SPECIAL_STATUS_OR_CLINICIAN_TYPE: True 56%, False 44%

PI_MEASURE_ID_1: PI_HIE_5 76%, PI_PEA_1 17%, PI_HIE_6 5%, PI_PHCDRR_3 1%, PI_EP_1 1%, PI_HIE_1 0%, PI_PHCDRR_1 0%, PI_INFBLO_1 0%, PI_EP_2 0%, PI_HIE_4 0%, PI_EP_2_EX_2 0%, PI_EP_2_EX_1 0%

PI_MEASURE_TYPE_1: Required 100%, Exclusion 0%

PI_MEASURE_ID_2: PI_PEA_1 76%, PI_PHCDRR_1 8%, PI_HIE_5 5%, PI_PHCDRR_3 4%, PI_EP_1 2%, PI_HIE_4 2%, PI_HIE_1 1%, PI_EP_2 1%, PI_EP_2_EX_2 1%, PI_EP_2_EX_1 0%, PI_ONCACB_1 0%, PI_HIE_6 0%

PI_MEASURE_TYPE_2: Required 99%, Exclusion 1%, Bonus 0%

PI_MEASURE_SCORE_2: 25 44%, 24 24%, 23 9%, 12 5%, 30 5%, 22 4%, 15 2%, 20 2%, 10 2%, 0 1%, 21 1%, 49 1%

PI_MEASURE_ID_3: PI_PHCDRR_1 73%, PI_EP_1 7%, PI_PEA_1 6%, PI_PHCDRR_3 6%, PI_HIE_4 2%, PI_EP_2 2%, PI_HIE_1 1%, PI_EP_2_EX_1 1%, PI_LVITC_2 1%, PI_HIE_5 0%, PI_PHCDRR_5 0%, PI_EP_2_EX_2 0%

PI_MEASURE_TYPE_3: Required 98%, Exclusion 2%, Bonus 0%

PI_MEASURE_SCORE_3: 12 78%, 10 7%, 0 3%, 15 2%, 24 2%, 25 2%, 20 2%, 23 2%, 22 1%, 19 1%, 21 1%, 13 0%

PI_MEASURE_ID_4: PI_PHCDRR_3 73%, PI_EP_1 13%, PI_EP_2 7%, PI_HIE_4 2%, PI_LVPP_1 1%, PI_HIE_1 1%, PI_PHCDRR_5 1%, PI_LVOTC_1 1%, PI_LVITC_2 1%, PI_EP_2_EX_2 1%, PI_PHCDRR_1 1%, PI_INFBLO_1 0%

PI_MEASURE_TYPE_4: Required 95%, Exclusion 3%, Bonus 1%

PI_MEASURE_SCORE_4: 12 74%, 10 19%, 0 4%, 5 1%, 11 1%, 9 1%, 15 1%, 14 0%, 13 0%, 20 0%, 19 0%, 1 0%

PI_MEASURE_ID_5: PI_EP_1 69%, PI_EP_2 18%, PI_PHCDRR_5 3%, PI_ONCACB_1 2%, PI_PHCDRR_1_EX_1 2%, PI_PHCDRR_4 1%, PI_HIE_1 1%, PI_LVOTC_1 1%, PI_LVITC_2 1%, PI_LVPP_1 1%, PI_EP_2_EX_2 1%, PI_PHCDRR_3 1%

PI_MEASURE_TYPE_5: Required 90%, Exclusion 6%, Bonus 4%

PI_MEASURE_SCORE_5: 10 85%, 0 8%, 5 4%, 9 1%, 12 1%, 8 0%, 1 0%, 3 0%, 7 0%, 2 0%, 15 0%, 14 0%

PI_MEASURE_ID_6: PI_EP_2 69%, PI_ONCACB_1 7%, PI_EP_1 6%, PI_PHCDRR_4 3%, PI_PHCDRR_2 3%, PI_PHCDRR_1_EX_1 3%, PI_PHCDRR_5 3%, PI_PHCDRR_3_EX_1 2%, PI_HIE_4 1%, PI_LVOTC_1 1%, PI_HIE_1 1%, PI_LVITC_2 1%

PI_MEASURE_TYPE_6: Required 82%, Bonus 10%, Exclusion 8%

PI_MEASURE_SCORE_6: 10 68%, 0 15%, 5 9%, 9 5%, 6 1%, 8 1%, 7 0%, 1 0%, 3 0%, 2 0%, 4 0%, 12 0%

PI_MEASURE_ID_7: PI_PHCDRR_2 39%, PI_ONCACB_1 19%, PI_PHCDRR_4 12%, PI_PHCDRR_5 7%, PI_PHCDRR_1_PROD 7%, PI_PHCDRR_1_EX_1 6%, PI_HIE_1 3%, PI_PHCDRR_3_EX_1 2%, PI_INFBLO_1 2%, PI_HIE_4 2%, PI_LVOTC_1 1%, PI_EP_2_EX_2 1%

PI_MEASURE_TYPE_7: Bonus 69%, Required 18%, Exclusion 13%

PI_MEASURE_SCORE_7: 5 57%, 0 38%, 1 2%, 3 1%, 2 0%, 4 0%, 10 0%, 9 0%, 6 0%, 8 0%, 7 0%

PI_MEASURE_ID_8: PI_ONCACB_1 51%, PI_PHCDRR_1_PROD 23%, PI_PHCDRR_1_EX_1 5%, PI_PHCDRR_3_EX_1 5%, PI_PHCDRR_2 4%, PI_INFBLO_1 2%, PI_HIE_1 2%, PI_PHCDRR_3_PROD 2%, PI_ONCDIR_1 2%, PI_PHCDRR_3_PRE 2%, PI_HIE_4 2%, PI_PHCDRR_1_PRE 1%

PI_MEASURE_TYPE_8: Required 66%, Exclusion 23%, Bonus 11%

PI_MEASURE_SCORE_8: 0 96%, 1 3%, 5 1%, 2 0%, 3 0%, 4 0%

PI_MEASURE_ID_9: PI_PHCDRR_1_PROD 51%, PI_PHCDRR_3_PROD 9%, PI_PHCDRR_3_PRE 9%, PI_PHCDRR_2 7%, PI_INFBLO_1 6%, PI_PHCDRR_2_PROD 5%, PI_ONCACB_1 3%, PI_PHCDRR_1_PRE 2%, PI_ONCDIR_1 2%, PI_PPHI_1 2%, PI_PHCDRR_3_EX_1 2%, PI_PHCDRR_5_PROD 2%

PI_MEASURE_TYPE_9: Required 79%, Bonus 17%, Exclusion 5%

PI_MEASURE_ID_10: PI_PHCDRR_2_PROD 36%, PI_PHCDRR_3_PROD 14%, PI_INFBLO_1 11%, PI_PHCDRR_3_PRE 9%, PI_PHCDRR_4 7%, PI_ONCDIR_1 6%, PI_PHCDRR_2 5%, PI_PHCDRR_1_PROD 3%, PI_PHCDRR_5_PROD 3%, PI_PHCDRR_4_PRE 3%, PI_PPHI_1 2%, PI_PPHI_2 2%

PI_MEASURE_TYPE_10: Bonus 54%, Required 44%, Exclusion 1%

PI_MEASURE_ID_11: PI_PHCDRR_3_PROD 33%, PI_ONCDIR_1 11%, PI_PHCDRR_4 11%, PI_INFBLO_1 9%, PI_PHCDRR_3_PRE 8%, PI_PHCDRR_5 6%, PI_PPHI_1 5%, PI_PHCDRR_4_PRE 4%, PI_PHCDRR_5_PROD 4%, PI_PHCDRR_4_PROD 3%, PI_PPHI_2 2%, PI_PHCDRR_2_PROD 2%

PI_MEASURE_TYPE_11: Required 68%, Bonus 32%, Exclusion 0%

PI_MEASURE_ID_12: PI_PHCDRR_4 26%, PI_INFBLO_1 26%, PI_PHCDRR_5 12%, PI_PPHI_1 11%, PI_ONCDIR_1 9%, PI_PPHI_2 5%, PI_PHCDRR_4_PROD 4%, PI_PHCDRR_5_PROD 1%, PI_PHCDRR_4_PRE 1%, PI_PHCDRR_3_PROD 1%, PI_PHCDRR_3_PRE 1%, PI_PHCDRR_3 0%

PI_MEASURE_TYPE_12: Required 55%, Bonus 45%

PI_MEASURE_ID_13: PI_ONCDIR_1 28%, PI_PHCDRR_5 18%, PI_PHCDRR_4_PROD 14%, PI_INFBLO_1 12%, PI_PPHI_2 12%, PI_PPHI_1 10%, PI_PHCDRR_5_PROD 4%, PI_PHCDRR_4 2%, PI_PHCDRR_4_PRE 1%, PI_PHCDRR_3_PROD 0%, PI_PHCDRR_5_PRE 0%, PI_PHCDRR_3_PRE 0%

PI_MEASURE_TYPE_13: Required 62%, Bonus 38%

PI_MEASURE_ID_14: PI_PPHI_1 31%, PI_INFBLO_1 21%, PI_PHCDRR_5 16%, PI_ONCDIR_1 14%, PI_PPHI_2 11%, PI_PHCDRR_5_PROD 5%, PI_PHCDRR_4_PROD 2%, PI_PHCDRR_4 0%, PI_PHCDRR_5_PRE 0%, PI_PHCDRR_4_PRE 0%, PI_PHCDRR_3_PROD 0%, PI_PHCDRR_3_PRE 0%

PI_MEASURE_TYPE_14: Required 77%, Bonus 23%

PI_MEASURE_ID_15: PI_PPHI_2 35%, PI_ONCDIR_1 23%, PI_PPHI_1 16%, PI_INFBLO_1 15%, PI_PHCDRR_5_PROD 8%, PI_PHCDRR_5 2%, PI_PHCDRR_4_PROD 0%, PI_PHCDRR_5_PRE 0%, PI_PHCDRR_4_PRE 0%, PI_PHCDRR_4 0%

PI_MEASURE_TYPE_15: Required 89%, Bonus 11%

PI_MEASURE_ID_16: PI_PPHI_1 36%, PI_PPHI_2 24%, PI_ONCDIR_1 24%, PI_INFBLO_1 13%, PI_PHCDRR_5_PROD 2%, PI_PHCDRR_5 1%, PI_PHCDRR_5_PRE 0%, PI_PHCDRR_4_PRE 0%

PI_MEASURE_TYPE_16: Required 97%, Bonus 3%

PI_MEASURE_ID_17: PI_PPHI_2 47%, PI_PPHI_1 31%, PI_ONCDIR_1 18%, PI_INFBLO_1 3%, PI_PHCDRR_5_PROD 1%, PI_PHCDRR_5_PRE 0%, PI_PHCDRR_5 0%

PI_MEASURE_TYPE_17: Required 99%, Bonus 1%

PI_MEASURE_ID_18: PI_PPHI_2 59%, PI_PPHI_1 35%, PI_ONCDIR_1 6%, PI_PHCDRR_5_PRE 0%

PI_MEASURE_TYPE_18: Required 100%, Bonus 0%

PI_MEASURE_ID_19: PI_PPHI_2 86%, PI_PPHI_1 14%

IMPROVEMENT_ACTIVITIES_IA_CATEGORY_SCORE: 40 91%, 0 8%, 20 0%, 30 0%, 10 0%

IA_REWEIGHTING_EUC: False 92%, True 8%

IA_CREDIT: False 56%, True 44%

IA_MEASURE_SCORE_1: 20 51%, 40 34%, 10 15%

IA_MEASURE_SCORE_2: 10 51%, 20 48%, 40 0%

IA_MEASURE_SCORE_3: 10 99%, 20 1%, 40 0%

IA_MEASURE_SCORE_4: 10 98%, 20 2%, 40 0%

COST_REWEIGHTING_EUC: False 88%, True 12%

COST_MEASURE_ID_1: COST_S_1 24%, MSPB_1 15%, TPCC_1 13%, COST_LBP_1 8%, COST_EDV_1 8%, COST_IOL_1 7%, COST_IHCI_1 5%, COST_NECABG_1 5%, COST_MR_1 4%, COST_PRC_1 4%, COST_KA_1 3%, COST_EOPCI_1 3%

COST_MEASURE_ID_2: COST_S_1 22%, MSPB_1 17%, TPCC_1 12%, COST_EDV_1 8%, COST_RUSST_1 7%, COST_COPDE_1 6%, COST_LBP_1 6%, COST_D_1 5%, COST_KA_1 5%, COST_PRC_1 4%, COST_LGH_1 4%, COST_IHCI_1 3%

COST_MEASURE_ID_3: COST_S_1 20%, MSPB_1 15%, TPCC_1 11%, COST_RUSST_1 9%, COST_EDV_1 7%, COST_LBP_1 7%, COST_D_1 6%, COST_COPDE_1 5%, COST_SSC_1 5%, COST_DEP_1 5%, COST_LSFDD_1 5%, COST_CCLI_1 4%

COST_MEASURE_ID_4: MSPB_1 22%, COST_COPDE_1 11%, TPCC_1 11%, COST_EDV_1 9%, COST_S_1 9%, COST_D_1 6%, COST_DEP_1 6%, COST_LPMSM_1 6%, COST_IHCI_1 5%, COST_CRR_1 5%, COST_ACOPD_1 5%, COST_HAC_1 5%

COST_MEASURE_ID_5: MSPB_1 15%, TPCC_1 12%, COST_IHCI_1 9%, COST_EDV_1 9%, COST_COPDE_1 8%, COST_LPMSM_1 8%, COST_DEP_1 8%, COST_LBP_1 7%, COST_CRR_1 6%, COST_D_1 6%, COST_PHA_1 6%, COST_SSC_1 6%

COST_MEASURE_ID_6: MSPB_1 14%, COST_COPDE_1 13%, TPCC_1 12%, COST_EDV_1 9%, COST_LSFDD_1 8%, COST_CRR_1 8%, COST_LGH_1 7%, COST_LBP_1 6%, COST_DEP_1 6%, COST_D_1 6%, COST_FIHR_1 5%, COST_HF_1 5%

COST_MEASURE_ID_7: MSPB_1 15%, TPCC_1 12%, COST_EDV_1 12%, COST_D_1 9%, COST_HAC_1 9%, COST_PHA_1 8%, COST_DEP_1 6%, COST_SSC_1 6%, COST_NECABG_1 6%, COST_LBP_1 6%, COST_HF_1 5%, COST_FIHR_1 5%

COST_MEASURE_ID_8: COST_FIHR_1 11%, COST_D_1 10%, TPCC_1 10%, COST_LBP_1 9%, MSPB_1 9%, COST_DEP_1 9%, COST_HF_1 9%, COST_KA_1 8%, COST_LGH_1 7%, COST_PRC_1 6%, COST_PHA_1 6%, COST_EOPCI_1 6%

COST_MEASURE_ID_9: COST_KA_1 13%, COST_DEP_1 12%, COST_D_1 9%, COST_EDV_1 8%, COST_PHA_1 8%, COST_HF_1 8%, COST_ACOPD_1 8%, COST_FIHR_1 7%, COST_COPDE_1 7%, COST_LBP_1 7%, TPCC_1 6%, COST_SSC_1 6%

COST_MEASURE_ID_10: COST_IHCI_1 12%, COST_DEP_1 11%, COST_MR_1 10%, COST_D_1 9%, COST_COPDE_1 9%, COST_EDV_1 9%, COST_HF_1 8%, COST_FIHR_1 8%, COST_EOPCI_1 7%, COST_SSC_1 7%, COST_ACOPD_1 7%, COST_CCLI_1 6%

COST_MEASURE_ID_11: COST_HF_1 10%, COST_SSC_1 10%, COST_LBP_1 10%, COST_ACOPD_1 9%, COST_EDV_1 9%, COST_DEP_1 9%, COST_IHCI_1 8%, MSPB_1 8%, COST_CCLI_1 7%, COST_FIHR_1 7%, COST_D_1 7%, COST_LPMSM_1 7%

COST_MEASURE_ID_12: TPCC_1 13%, COST_D_1 13%, COST_FIHR_1 11%, COST_DEP_1 10%, COST_LBP_1 9%, COST_HF_1 9%, COST_EDV_1 8%, COST_LGH_1 6%, COST_ACOPD_1 6%, COST_MR_1 5%, COST_EOPCI_1 5%, COST_IOL_1 4%

COST_MEASURE_ID_13: COST_LBP_1 13%, COST_SSC_1 13%, COST_FIHR_1 10%, COST_EOPCI_1 9%, TPCC_1 9%, COST_HF_1 8%, COST_EDV_1 7%, COST_CCLI_1 7%, COST_IHCI_1 6%, COST_ACOPD_1 6%, COST_HAC_1 6%, COST_LPMSM_1 6%

COST_MEASURE_ID_14: COST_LBP_1 13%, COST_CCLI_1 12%, COST_FIHR_1 11%, COST_SSC_1 10%, COST_D_1 9%, COST_DEP_1 9%, TPCC_1 9%, COST_HF_1 6%, COST_NECABG_1 6%, COST_LGH_1 5%, COST_EOPCI_1 5%, COST_IOL_1 4%

COST_MEASURE_ID_15: COST_D_1 20%, COST_LBP_1 16%, COST_DEP_1 9%, COST_CCLI_1 9%, COST_HF_1 8%, COST_IHCI_1 7%, COST_FIHR_1 7%, COST_KA_1 5%, COST_ACOPD_1 5%, TPCC_1 5%, COST_EOPCI_1 5%, COST_LPMSM_1 5%

COST_MEASURE_ID_16: COST_ACOPD_1 16%, COST_RUSST_1 11%, COST_HF_1 10%, COST_DEP_1 10%, COST_D_1 9%, COST_LPMSM_1 7%, COST_MR_1 7%, COST_NECABG_1 6%, COST_IOL_1 6%, COST_COPDE_1 6%, COST_LGH_1 5%, TPCC_1 5%

COST_MEASURE_ID_17: COST_LPMSM_1 12%, COST_HF_1 12%, COST_KA_1 11%, COST_SSC_1 10%, COST_LBP_1 10%, COST_ACOPD_1 8%, COST_LSFDD_1 7%, COST_D_1 7%, TPCC_1 7%, COST_IOL_1 6%, COST_LGH_1 5%, COST_CCLI_1 5%

COST_MEASURE_ID_18: COST_D_1 14%, TPCC_1 12%, COST_FIHR_1 11%, COST_ACOPD_1 11%, COST_EOPCI_1 11%, COST_HF_1 9%, COST_DEP_1 7%, COST_LBP_1 6%, COST_IHCI_1 5%, COST_SSC_1 5%, COST_PHA_1 4%, COST_STEMI_1 4%

COST_MEASURE_ID_19: COST_DEP_1 19%, COST_ACOPD_1 16%, COST_SSC_1 11%, COST_D_1 10%, COST_CRR_1 10%, TPCC_1 5%, COST_EDV_1 5%, COST_PHA_1 5%, COST_NECABG_1 5%, COST_LBP_1 5%, COST_KA_1 5%, COST_HAC_1 4%

COST_MEASURE_ID_20: TPCC_1 14%, COST_LBP_1 12%, COST_ACOPD_1 10%, COST_PHA_1 9%, COST_D_1 9%, COST_HAC_1 8%, COST_HF_1 8%, COST_IHCI_1 8%, COST_EOPCI_1 6%, COST_PRC_1 6%, COST_MR_1 5%, COST_LPMSM_1 5%

COST_MEASURE_ID_21: COST_HF_1 20%, TPCC_1 12%, COST_EOPCI_1 9%, COST_IHCI_1 8%, COST_LBP_1 8%, COST_ACOPD_1 8%, COST_COPDE_1 6%, COST_KA_1 6%, COST_DEP_1 6%, COST_EDV_1 6%, COST_D_1 6%, COST_CRR_1 6%

COST_MEASURE_ID_22: COST_ACOPD_1 13%, COST_HF_1 11%, COST_PHA_1 11%, COST_MR_1 9%, COST_RUSST_1 8%, COST_LSFDD_1 8%, COST_KA_1 8%, COST_CRR_1 7%, COST_HAC_1 7%, COST_LGH_1 6%, COST_IHCI_1 5%, TPCC_1 5%

COST_MEASURE_ID_23: COST_PHA_1 15%, COST_RUSST_1 11%, COST_SSC_1 10%, COST_MR_1 10%, TPCC_1 10%, COST_HF_1 10%, COST_PRC_1 7%, COST_D_1 6%, COST_NECABG_1 6%, COST_ACOPD_1 6%, COST_IHCI_1 6%, COST_KA_1 4%

COST_MEASURE_ID_24: COST_LPMSM_1 16%, COST_SSC_1 11%, COST_IOL_1 10%, COST_ACOPD_1 10%, COST_HF_1 9%, COST_KA_1 8%, COST_LSFDD_1 7%, COST_PHA_1 6%, COST_LGH_1 6%, COST_EOPCI_1 6%, COST_CCLI_1 6%, COST_PRC_1 5%

COST_MEASURE_ID_25: COST_PHA_1 13%, COST_EOPCI_1 12%, COST_IOL_1 12%, COST_RUSST_1 11%, COST_LPMSM_1 8%, COST_LSFDD_1 7%, COST_CCLI_1 7%, COST_DEP_1 7%, COST_PRC_1 6%, COST_KA_1 6%, COST_ACOPD_1 6%, COST_LBP_1 5%

COST_MEASURE_ID_26: COST_KA_1 14%, COST_CRR_1 12%, COST_LSFDD_1 12%, COST_IHCI_1 8%, COST_HF_1 8%, COST_ACOPD_1 8%, COST_MR_1 8%, COST_SSC_1 7%, TPCC_1 7%, COST_NECABG_1 7%, COST_HAC_1 5%, COST_IOL_1 4%

COST_MEASURE_ID_27: COST_PRC_1 29%, COST_HAC_1 18%, COST_MR_1 8%, COST_NECABG_1 8%, COST_STEMI_1 8%, COST_EDV_1 6%, COST_PHA_1 5%, TPCC_1 5%, COST_LBP_1 5%, COST_LPMSM_1 4%, COST_KA_1 3%, COST_RUSST_1 2%

COST_MEASURE_ID_28: COST_SSC_1 29%, COST_ACOPD_1 29%, COST_LGH_1 16%, COST_RUSST_1 11%, COST_EOPCI_1 6%, COST_HAC_1 5%, COST_KA_1 2%, COST_NECABG_1 1%, COST_STEMI_1 0%, COST_LSFDD_1 0%, COST_EDV_1 0%, COST_PRC_1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROVIDER_KEY | who | 507.7K | 0 | 000312545 410; 000312538 410; 000312531 410; 000312523 410 |
| PRACTICE_STATE_OR_US_TERRITORY | state | 55 | 24 | CA 47.7K; FL 40.7K; NY 36.4K; TX 33.3K |
| PRACTICE_SIZE | other | 822 | 0 | 1 14.6K; 2 7.1K; 3 6.1K; 4 5.5K |
| CLINICIAN_TYPE | category | 19 | 0 | Doctor of Medicine 319.7K; Nurse Practitioner 72.8K; Physician Assistant 50.6K; Physical Therapist  17.7K |
| CLINICIAN_SPECIALTY | who | 85 | 0 | Nurse Practitioner 72.8K; Physician Assistant 50.6K; Physician/Internal Medici 32.0K; Physician/Emergency Medic 26.4K |
| YEARS_IN_MEDICARE | category | 21 | 0 | 21 43.8K; 15 37.2K; 20 32.1K; 9 30.3K |
| NPI | other | 452.6K | 0 | 1831419829 410; 1487952446 410; 1366647646 410; 1891885661 410 |
| NON_REPORTING | category | 2 | 0 | False 473.2K; True 30.7K |
| PARTICIPATION_OPTION | category | 5 | 0 | Group 360.8K; APM Entity 99.3K; Individual 43.1K; Subgroup 569 |
| REPORTING_OPTION | category | 3 | 0 | Traditional MIPS 394.2K; APM Performance Pathway 98.2K; MIPS Value Pathways 11.4K |
| MIPS_VALUE_PATHWAY_ID | category | 16 | 492.5K | G0058 3.4K; M0005 2.0K; G0059 1.8K; M0001 1.5K |
| MIPS_VALUE_PATHWAY_TITLE | category | 16 | 492.5K | Improving Care for Lower  3.4K; Value in Primary Care 2.0K; Patient Safety and Suppor 1.8K; Advancing Cancer Care 1.5K |
| MEDICARE_PATIENTS | other | 7.4K | 0 | 300342 5.4K; 307061 4.7K; 92381 3.9K; 174003 3.3K |
| ALLOWED_CHARGES | amount | 57.0K | 0 | 329265077.00 5.4K; 385171391.00 4.7K; 84074214.00 3.9K; 202251737.00 3.3K |
| SERVICES | who | 14.8K | 0 | 3081473 5.4K; 3477198 4.7K; 935212 3.9K; 2054550 3.3K |
| OPTED_INTO_MIPS | category | 2 | 0 | False 500.5K; True 3.4K |
| SMALL_PRACTICE_STATUS | category | 2 | 0 | False 433.1K; True 70.8K |
| RURAL_STATUS | category | 2 | 0 | False 447.3K; True 56.6K |
| HEALTH_PROFESSIONAL_SHORTAGE_AREA_STATUS | category | 2 | 0 | False 419.5K; True 84.4K |
| AMBULATORY_SURGICAL_CENTER_BASED_STATUS | category | 2 | 0 | False 503.4K; True 515 |
| HOSPITAL_BASED_STATUS | category | 2 | 0 | False 341.9K; True 162.1K |
| NON_PATIENT_FACING_STATUS | category | 2 | 0 | False 422.8K; True 81.1K |
| FACILITY_BASED_STATUS | category | 2 | 0 | False 443.1K; True 60.8K |
| RECEIVED_FACILITY_SCORE | category | 2 | 0 | False 485.1K; True 18.8K |
| DUAL_ELIGIBILITY_RATIO | amount | 101 | 0 | 0.14 25.9K; 0.13 25.5K; 0.12 22.4K; 0.11 20.0K |
| SAFETY_NET_STATUS | category | 2 | 0 | False 397.5K; True 106.4K |
| EXTREME_UNCONTROLLABLE_CIRCUMSTANCE_EUC | category | 2 | 0 | False 424.3K; True 79.6K |
| FINAL_SCORE | amount | 6.8K | 0 | 100.00 32.1K; 75.00 25.6K; 93.07 6.3K; 0.00 5.5K |
| PAYMENT_ADJUSTMENT_PERCENTAGE | amount | 779 | 0 | 1.05 32.4K; 0.00 26.0K; 0.80 11.3K; 0.76 11.3K |
| COMPLEX_PATIENT_BONUS | amount | 948 | 0 | 0.00 237.2K; 5.00 16.3K; 10.00 15.9K; 6.55 9.3K |
| QUALITY_CATEGORY_SCORE | amount | 6.5K | 0 | 0.00 39.7K; 100.00 14.3K; 79.77 6.3K; 91.79 4.7K |
| QUALITY_IMPROVEMENT_SCORE | amount | 797 | 0 | 0.00 292.5K; 0.22 7.5K; 0.60 6.7K; 0.04 6.5K |
| QUALITY_CATEGORY_WEIGHT | amount | 9 | 0 | 0.30 224.2K; 0.50 112.6K; 0.55 67.7K; 0.00 45.7K |
| QUALITY_REWEIGHTING_EUC | category | 2 | 0 | False 453.4K; True 50.5K |
| SMALL_PRACTICE_BONUS | amount | 2 | 0 | 0.00 456.6K; 6.00 47.4K |
| QUALITY_MEASURE_ID_1 | other | 243 | 35.7K | 001 90.1K; 066 40.4K; 479 24.8K; 475 24.5K |
| QUALITY_MEASURE_COLLECTION_TYPE_1 | category | 7 | 35.7K | eCQM 197.9K; CMS Web Interface Measure 90.8K; MIPS CQM 81.8K; Administrative Claims Mea 65.0K |
| QUALITY_MEASURE_SCORE_1 | amount | 91 | 35.7K | 10.0 332.7K; 9.7 12.3K; 9.8 11.0K; 7.0 9.5K |
| QUALITY_MEASURE_ID_2 | other | 283 | 44.6K | 318 41.4K; 001 32.1K; 226 32.0K; 475 30.4K |
| QUALITY_MEASURE_COLLECTION_TYPE_2 | category | 7 | 44.6K | eCQM 195.6K; CMS Web Interface Measure 89.7K; MIPS CQM 76.6K; Administrative Claims Mea 61.7K |
| QUALITY_MEASURE_SCORE_2 | amount | 91 | 44.6K | 10.0 213.4K; 9.9 22.7K; 7.0 17.9K; 9.7 14.3K |
| QUALITY_MEASURE_ID_3 | other | 289 | 54.5K | 226 37.3K; 318 33.9K; 309 27.1K; 479 24.4K |
| QUALITY_MEASURE_COLLECTION_TYPE_3 | category | 7 | 54.5K | eCQM 189.2K; CMS Web Interface Measure 83.1K; MIPS CQM 70.9K; Administrative Claims Mea 64.4K |
| QUALITY_MEASURE_SCORE_3 | amount | 91 | 54.5K | 10.0 122.5K; 7.0 27.2K; 9.7 17.9K; 9.6 16.9K |
| QUALITY_MEASURE_ID_4 | other | 304 | 60.6K | 001 31.5K; 318 30.2K; 112 29.5K; 236 25.3K |
| QUALITY_MEASURE_COLLECTION_TYPE_4 | category | 7 | 60.6K | eCQM 185.4K; CMS Web Interface Measure 87.4K; MIPS CQM 77.8K; Administrative Claims Mea 53.2K |
| QUALITY_MEASURE_SCORE_4 | amount | 91 | 60.6K | 10.0 55.2K; 7.0 42.8K; 9.2 20.5K; 9.5 20.4K |
| QUALITY_MEASURE_ID_5 | other | 312 | 69.4K | 001 31.2K; 134 27.7K; 317 25.2K; 113 23.8K |
| QUALITY_MEASURE_COLLECTION_TYPE_5 | category | 7 | 69.4K | eCQM 198.5K; CMS Web Interface Measure 86.3K; MIPS CQM 72.5K; Administrative Claims Mea 40.5K |
| QUALITY_MEASURE_SCORE_5 | amount | 91 | 69.4K | 7.0 55.1K; 8.4 22.4K; 8.9 16.1K; 9.2 15.7K |
| QUALITY_MEASURE_ID_6 | other | 315 | 79.9K | 236 42.5K; 479 29.7K; 001 25.5K; 113 22.3K |
| QUALITY_MEASURE_COLLECTION_TYPE_6 | category | 7 | 79.9K | eCQM 157.6K; CMS Web Interface Measure 85.0K; Administrative Claims Mea 68.0K; MIPS CQM 66.5K |
| QUALITY_MEASURE_SCORE_6 | amount | 91 | 79.9K | 7.0 47.9K; 8.4 22.5K; 9.1 14.2K; 8.5 14.0K |
| QUALITY_MEASURE_ID_7 | other | 138 | 184.6K | 484 42.7K; 479 40.5K; 113 25.5K; 236 23.4K |
| QUALITY_MEASURE_COLLECTION_TYPE_7 | category | 7 | 184.6K | Administrative Claims Mea 113.8K; eCQM 92.7K; CMS Web Interface Measure 83.6K; MIPS CQM 17.9K |
| QUALITY_MEASURE_SCORE_7 | amount | 90 | 184.6K | 7.0 14.3K; 7.9 13.3K; 8.6 13.2K; 8.2 13.2K |
| QUALITY_MEASURE_ID_8 | other | 62 | 222.3K | 484 51.0K; 479 49.7K; 110 30.8K; 492 27.6K |
| QUALITY_MEASURE_COLLECTION_TYPE_8 | category | 7 | 222.3K | Administrative Claims Mea 145.9K; CMS Web Interface Measure 67.3K; eCQM 48.9K; CAHPS Measure 11.9K |
| QUALITY_MEASURE_SCORE_8 | amount | 88 | 222.3K | 7.8 14.0K; 7.3 13.8K; 8.5 10.9K; 0.0 9.7K |
| QUALITY_MEASURE_ID_9 | category | 42 | 257.7K | 479 41.0K; 492 39.0K; 321 38.9K; 484 30.5K |
| QUALITY_MEASURE_COLLECTION_TYPE_9 | category | 5 | 257.7K | Administrative Claims Mea 135.1K; CAHPS Measure 38.9K; CMS Web Interface Measure 38.8K; eCQM 31.2K |
| QUALITY_MEASURE_SCORE_9 | amount | 84 | 257.7K | 0.0 16.9K; 6.0 9.6K; 1.6 9.3K; 7.0 7.7K |
| QUALITY_MEASURE_ID_10 | category | 14 | 311.9K | 484 60.6K; 488 43.9K; 479 34.2K; 492 16.1K |
| QUALITY_MEASURE_COLLECTION_TYPE_10 | category | 5 | 311.9K | Administrative Claims Mea 120.6K; eCQM 46.7K; CAHPS Measure 14.4K; CMS Web Interface Measure 10.1K |
| QUALITY_MEASURE_SCORE_10 | amount | 71 | 311.9K | 0.0 43.9K; 5.2 9.1K; 5.7 8.8K; 7.2 8.0K |
| QUALITY_MEASURE_ID_11 | category | 6 | 413.7K | 484 44.0K; 479 26.0K; 321 16.0K; 226 2.7K |
| QUALITY_MEASURE_COLLECTION_TYPE_11 | category | 3 | 413.7K | Administrative Claims Mea 69.9K; CAHPS Measure 16.0K; CMS Web Interface Measure 4.4K |
| QUALITY_MEASURE_SCORE_11 | amount | 54 | 413.7K | 4.9 12.6K; 4.6 5.4K; 3.8 4.9K; 3.9 4.2K |
| QUALITY_MEASURE_ID_12 | empty | 0 | 503.9K |  |
| QUALITY_MEASURE_COLLECTION_TYPE_12 | empty | 0 | 503.9K |  |
| QUALITY_MEASURE_SCORE_12 | empty | 0 | 503.9K |  |
| PROMOTING_INTEROPERABILITY_PI_CATEGORY_SCORE | amount | 118 | 0 | 100.00 259.0K; 0.00 150.5K; 99.00 26.6K; 98.00 12.6K |
| PROMOTING_INTEROPERABILITY_PI_CATEGORY_WEIGHT | amount | 5 | 0 | 0.25 224.2K; 0.00 142.6K; 0.30 118.5K; 0.85 18.1K |
| PI_REWEIGHTING_EUC | category | 2 | 0 | False 458.5K; True 45.4K |
| PI_REWEIGHTING_HARDSHIP_EXCEPTION | category | 2 | 0 | False 490.9K; True 13.1K |
| PI_REWEIGHTING_SPECIAL_STATUS_OR_CLINICIAN_TYPE | category | 2 | 0 | True 281.1K; False 222.8K |
| CEHRT_ID | other | 697 | 235.3K | 0015CWF2A39FFN1 19.1K; 0015C2XAQ9DS7BM 15.0K; 0015CYC5RFV7B8K 14.2K; 0015CTA26NFD57N 9.8K |
| PI_MEASURE_ID_1 | category | 12 | 235.3K | PI_HIE_5 204.2K; PI_PEA_1 44.5K; PI_HIE_6 12.9K; PI_PHCDRR_3 3.9K |
| PI_MEASURE_TYPE_1 | category | 2 | 235.3K | Required 268.6K; Exclusion 79 |
| PI_MEASURE_SCORE_1 | other | 85 | 235.3K | 30 213.6K; 25 10.1K; 50 7.5K; 24 4.4K |
| PI_MEASURE_ID_2 | category | 18 | 235.3K | PI_PEA_1 203.6K; PI_PHCDRR_1 22.5K; PI_HIE_5 13.1K; PI_PHCDRR_3 11.1K |
| PI_MEASURE_TYPE_2 | category | 3 | 235.4K | Required 266.6K; Exclusion 1.9K; Bonus 19 |
| PI_MEASURE_SCORE_2 | category | 48 | 235.3K | 25 114.6K; 24 63.1K; 23 22.4K; 12 13.3K |
| PI_MEASURE_ID_3 | category | 21 | 235.3K | PI_PHCDRR_1 195.4K; PI_EP_1 19.8K; PI_PEA_1 17.0K; PI_PHCDRR_3 15.8K |
| PI_MEASURE_TYPE_3 | category | 3 | 235.3K | Required 262.7K; Exclusion 5.2K; Bonus 783 |
| PI_MEASURE_SCORE_3 | category | 26 | 235.3K | 12 206.9K; 10 19.7K; 0 7.0K; 15 5.0K |
| PI_MEASURE_ID_4 | category | 20 | 235.4K | PI_PHCDRR_3 193.9K; PI_EP_1 34.1K; PI_EP_2 17.7K; PI_HIE_4 4.3K |
| PI_MEASURE_TYPE_4 | category | 3 | 235.5K | Required 256.0K; Exclusion 9.1K; Bonus 3.3K |
| PI_MEASURE_SCORE_4 | category | 21 | 235.4K | 12 196.9K; 10 50.4K; 0 10.6K; 5 3.4K |
| PI_MEASURE_ID_5 | category | 23 | 235.5K | PI_EP_1 183.9K; PI_EP_2 48.0K; PI_PHCDRR_5 6.8K; PI_ONCACB_1 5.0K |
| PI_MEASURE_TYPE_5 | category | 3 | 240.5K | Required 237.6K; Exclusion 14.7K; Bonus 11.0K |
| PI_MEASURE_SCORE_5 | category | 16 | 235.5K | 10 229.2K; 0 20.1K; 5 11.2K; 9 3.1K |
| PI_MEASURE_ID_6 | category | 27 | 235.5K | PI_EP_2 180.9K; PI_ONCACB_1 18.5K; PI_EP_1 16.2K; PI_PHCDRR_4 8.6K |
| PI_MEASURE_TYPE_6 | category | 3 | 254.0K | Required 205.5K; Bonus 23.8K; Exclusion 20.6K |
| PI_MEASURE_SCORE_6 | category | 12 | 235.5K | 10 182.1K; 0 40.8K; 5 24.7K; 9 13.9K |
| PI_MEASURE_ID_7 | category | 31 | 235.5K | PI_PHCDRR_2 102.1K; PI_ONCACB_1 49.4K; PI_PHCDRR_4 30.8K; PI_PHCDRR_5 18.2K |
| PI_MEASURE_TYPE_7 | category | 3 | 284.9K | Bonus 151.1K; Required 38.8K; Exclusion 29.2K |
| PI_MEASURE_SCORE_7 | category | 11 | 240.1K | 5 150.3K; 0 100.6K; 1 4.9K; 3 3.1K |
| PI_MEASURE_ID_8 | category | 34 | 235.5K | PI_ONCACB_1 131.6K; PI_PHCDRR_1_PROD 58.0K; PI_PHCDRR_1_EX_1 13.6K; PI_PHCDRR_3_EX_1 11.6K |
| PI_MEASURE_TYPE_8 | category | 3 | 367.1K | Required 90.3K; Exclusion 31.1K; Bonus 15.4K |
| PI_MEASURE_SCORE_8 | category | 6 | 245.7K | 0 247.6K; 1 7.1K; 5 1.5K; 2 854 |
| PI_MEASURE_ID_9 | category | 25 | 235.5K | PI_PHCDRR_1_PROD 127.2K; PI_PHCDRR_3_PROD 23.7K; PI_PHCDRR_3_PRE 23.1K; PI_PHCDRR_2 17.9K |
| PI_MEASURE_TYPE_9 | category | 3 | 243.5K | Required 204.8K; Bonus 43.4K; Exclusion 12.2K |
| PI_MEASURE_SCORE_9 | other | 1 | 259.8K | 0 244.1K |
| PI_MEASURE_ID_10 | category | 21 | 235.6K | PI_PHCDRR_2_PROD 89.6K; PI_PHCDRR_3_PROD 35.1K; PI_INFBLO_1 28.6K; PI_PHCDRR_3_PRE 22.1K |
| PI_MEASURE_TYPE_10 | category | 3 | 235.6K | Bonus 145.8K; Required 118.5K; Exclusion 4.0K |
| PI_MEASURE_SCORE_10 | other | 1 | 288.5K | 0 215.4K |
| PI_MEASURE_ID_11 | category | 19 | 240.3K | PI_PHCDRR_3_PROD 86.5K; PI_ONCDIR_1 28.6K; PI_PHCDRR_4 28.0K; PI_INFBLO_1 24.3K |
| PI_MEASURE_TYPE_11 | category | 3 | 240.3K | Required 179.5K; Bonus 83.9K; Exclusion 146 |
| PI_MEASURE_SCORE_11 | other | 1 | 312.9K | 0 191.1K |
| PI_MEASURE_ID_12 | category | 15 | 246.1K | PI_PHCDRR_4 68.2K; PI_INFBLO_1 67.4K; PI_PHCDRR_5 31.6K; PI_PPHI_1 28.7K |
| PI_MEASURE_TYPE_12 | category | 2 | 246.1K | Required 141.2K; Bonus 116.6K |
| PI_MEASURE_SCORE_12 | other | 1 | 380.5K | 0 123.5K |
| PI_MEASURE_ID_13 | category | 13 | 260.2K | PI_ONCDIR_1 67.4K; PI_PHCDRR_5 43.0K; PI_PHCDRR_4_PROD 33.0K; PI_INFBLO_1 29.6K |
| PI_MEASURE_TYPE_13 | category | 2 | 260.2K | Required 150.9K; Bonus 92.8K |
| PI_MEASURE_SCORE_13 | other | 1 | 410.1K | 0 93.8K |
| PI_MEASURE_ID_14 | category | 12 | 288.9K | PI_PPHI_1 67.5K; PI_INFBLO_1 44.3K; PI_PHCDRR_5 34.2K; PI_ONCDIR_1 29.6K |
| PI_MEASURE_TYPE_14 | category | 2 | 288.9K | Required 165.8K; Bonus 49.2K |
| PI_MEASURE_SCORE_14 | other | 1 | 454.4K | 0 49.5K |
| PI_MEASURE_ID_15 | category | 10 | 313.3K | PI_PPHI_2 67.5K; PI_ONCDIR_1 44.3K; PI_PPHI_1 29.7K; PI_INFBLO_1 29.1K |
| PI_MEASURE_TYPE_15 | category | 2 | 313.3K | Required 170.6K; Bonus 20.1K |
| PI_MEASURE_SCORE_15 | other | 1 | 483.7K | 0 20.2K |
| PI_MEASURE_ID_16 | category | 8 | 380.8K | PI_PPHI_1 44.3K; PI_PPHI_2 29.7K; PI_ONCDIR_1 29.1K; PI_INFBLO_1 16.5K |
| PI_MEASURE_TYPE_16 | category | 2 | 380.8K | Required 119.5K; Bonus 3.6K |
| PI_MEASURE_SCORE_16 | other | 1 | 500.2K | 0 3.7K |
| PI_MEASURE_ID_17 | category | 7 | 410.5K | PI_PPHI_2 44.3K; PI_PPHI_1 29.2K; PI_ONCDIR_1 16.5K; PI_INFBLO_1 2.8K |
| PI_MEASURE_TYPE_17 | category | 2 | 410.5K | Required 92.7K; Bonus 714 |
| PI_MEASURE_SCORE_17 | other | 1 | 503.1K | 0 825 |
| PI_MEASURE_ID_18 | category | 4 | 454.8K | PI_PPHI_2 29.2K; PI_PPHI_1 17.2K; PI_ONCDIR_1 2.8K; PI_PHCDRR_5_PRE 1 |
| PI_MEASURE_TYPE_18 | category | 2 | 454.8K | Required 49.1K; Bonus 1 |
| PI_MEASURE_SCORE_18 | other | 1 | 503.1K | 0 783 |
| PI_MEASURE_ID_19 | category | 2 | 483.9K | PI_PPHI_2 17.2K; PI_PPHI_1 2.8K |
| PI_MEASURE_TYPE_19 | who | 1 | 483.9K | Required 20.0K |
| PI_MEASURE_SCORE_19 | other | 1 | 503.2K | 0 714 |
| PI_MEASURE_ID_20 | other | 1 | 501.1K | PI_PPHI_2 2.8K |
| PI_MEASURE_TYPE_20 | who | 1 | 501.1K | Required 2.8K |
| PI_MEASURE_SCORE_20 | other | 1 | 503.9K | 0 1 |
| PI_MEASURE_ID_21 | empty | 0 | 503.9K |  |
| PI_MEASURE_TYPE_21 | empty | 0 | 503.9K |  |
| PI_MEASURE_SCORE_21 | empty | 0 | 503.9K |  |
| IMPROVEMENT_ACTIVITIES_IA_CATEGORY_SCORE | category | 5 | 0 | 40 460.3K; 0 41.9K; 20 1.2K; 30 531 |
| IMPROVEMENT_ACTIVITIES_IA_CATEGORY_WEIGHT | amount | 6 | 0 | 0.15 334.6K; 0.20 97.9K; 0.30 29.2K; 0.00 25.8K |
| IA_REWEIGHTING_EUC | category | 2 | 0 | False 463.0K; True 40.9K |
| IA_CREDIT | category | 2 | 0 | False 281.9K; True 222.0K |
| IA_MEASURE_ID_1 | other | 93 | 133.8K | IA_BE_6 84.3K; IA_EPA_1 74.3K; IA_BE_4 48.9K; IA_AHE_3 22.6K |
| IA_MEASURE_SCORE_1 | category | 3 | 133.8K | 20 188.5K; 40 126.0K; 10 55.6K |
| IA_MEASURE_ID_2 | other | 100 | 248.8K | IA_BE_4 39.0K; IA_EPA_1 32.7K; IA_CC_13 27.0K; IA_BMH_2 14.3K |
| IA_MEASURE_SCORE_2 | category | 3 | 248.8K | 10 131.1K; 20 123.5K; 40 636 |
| IA_MEASURE_ID_3 | other | 79 | 372.9K | IA_EPA_2 20.2K; IA_PSPA_16 11.1K; IA_BE_4 10.4K; IA_CC_2 9.3K |
| IA_MEASURE_SCORE_3 | category | 3 | 372.9K | 10 129.1K; 20 1.5K; 40 307 |
| IA_MEASURE_ID_4 | other | 54 | 452.1K | IA_PSPA_16 14.5K; IA_PM_16 6.3K; IA_PSPA_21 6.3K; IA_EPA_2 3.9K |
| IA_MEASURE_SCORE_4 | category | 3 | 452.1K | 10 50.5K; 20 1.2K; 40 100 |
| COST_CATEGORY_SCORE | amount | 27.1K | 0 | 0.0000 152.6K; 75.1821 4.6K; 74.5758 3.9K; 79.0490 2.8K |
| COST_IMPROVEMENT_SCORE | amount | 101 | 0 | 0.00 208.9K; 1.00 16.7K; 0.27 11.6K; 0.29 9.9K |
| COST_CATEGORY_WEIGHT | amount | 3 | 0 | 0.3000 301.3K; 0.0000 201.3K; 0.5000 1.4K |
| COST_REWEIGHTING_EUC | category | 2 | 0 | False 444.4K; True 59.6K |
| COST_MEASURE_ID_1 | category | 28 | 150.6K | COST_S_1 62.6K; MSPB_1 39.4K; TPCC_1 34.5K; COST_LBP_1 21.5K |
| COST_MEASURE_ACHIEVEMENT_POINTS_1 | amount | 90 | 150.6K | 10.0 75.6K; 9.1 13.4K; 9.0 12.5K; 8.0 12.4K |
| COST_MEASURE_ID_2 | category | 28 | 217.1K | COST_S_1 45.7K; MSPB_1 36.2K; TPCC_1 25.4K; COST_EDV_1 15.8K |
| COST_MEASURE_ACHIEVEMENT_POINTS_2 | amount | 90 | 217.1K | 10.0 19.0K; 8.7 18.1K; 7.9 16.0K; 8.0 14.3K |
| COST_MEASURE_ID_3 | category | 28 | 251.6K | COST_S_1 36.2K; MSPB_1 27.5K; TPCC_1 20.2K; COST_RUSST_1 15.6K |
| COST_MEASURE_ACHIEVEMENT_POINTS_3 | amount | 90 | 251.6K | 7.9 24.4K; 8.0 18.8K; 8.4 18.6K; 7.8 16.0K |
| COST_MEASURE_ID_4 | category | 28 | 267.8K | MSPB_1 33.4K; COST_COPDE_1 17.3K; TPCC_1 16.4K; COST_EDV_1 13.6K |
| COST_MEASURE_ACHIEVEMENT_POINTS_4 | amount | 90 | 267.8K | 7.9 29.0K; 7.8 25.9K; 8.0 25.0K; 8.1 14.2K |
| COST_MEASURE_ID_5 | category | 28 | 279.4K | MSPB_1 22.1K; TPCC_1 17.1K; COST_IHCI_1 13.5K; COST_EDV_1 13.0K |
| COST_MEASURE_ACHIEVEMENT_POINTS_5 | amount | 87 | 279.4K | 7.8 32.9K; 7.9 31.1K; 7.7 19.9K; 8.0 16.2K |
| COST_MEASURE_ID_6 | category | 28 | 294.3K | MSPB_1 19.3K; COST_COPDE_1 18.5K; TPCC_1 16.9K; COST_EDV_1 12.4K |
| COST_MEASURE_ACHIEVEMENT_POINTS_6 | amount | 78 | 294.3K | 7.8 32.9K; 7.9 26.2K; 8.0 21.0K; 7.6 20.9K |
| COST_MEASURE_ID_7 | category | 28 | 309.3K | MSPB_1 18.0K; TPCC_1 14.8K; COST_EDV_1 14.6K; COST_D_1 10.7K |
| COST_MEASURE_ACHIEVEMENT_POINTS_7 | amount | 67 | 309.3K | 7.8 43.9K; 7.5 19.9K; 7.9 19.6K; 7.6 17.8K |
| COST_MEASURE_ID_8 | category | 28 | 320.4K | COST_FIHR_1 12.9K; COST_D_1 12.6K; TPCC_1 12.2K; COST_LBP_1 11.2K |
| COST_MEASURE_ACHIEVEMENT_POINTS_8 | amount | 61 | 320.4K | 7.8 30.0K; 7.7 28.5K; 7.6 18.0K; 7.5 17.8K |
| COST_MEASURE_ID_9 | category | 28 | 327.4K | COST_KA_1 14.3K; COST_DEP_1 13.7K; COST_D_1 10.0K; COST_EDV_1 9.3K |
| COST_MEASURE_ACHIEVEMENT_POINTS_9 | amount | 57 | 327.4K | 7.6 32.9K; 7.8 23.4K; 7.7 22.9K; 7.5 19.3K |
| COST_MEASURE_ID_10 | category | 28 | 333.9K | COST_IHCI_1 13.0K; COST_DEP_1 11.5K; COST_MR_1 10.5K; COST_D_1 9.4K |
| COST_MEASURE_ACHIEVEMENT_POINTS_10 | amount | 53 | 333.9K | 7.6 35.9K; 7.7 24.5K; 7.5 15.6K; 7.3 15.0K |
| COST_MEASURE_ID_11 | category | 28 | 338.3K | COST_HF_1 10.8K; COST_SSC_1 10.6K; COST_LBP_1 10.2K; COST_ACOPD_1 9.9K |
| COST_MEASURE_ACHIEVEMENT_POINTS_11 | amount | 47 | 338.3K | 7.6 35.7K; 7.5 18.7K; 7.7 18.6K; 7.4 18.0K |
| COST_MEASURE_ID_12 | category | 28 | 345.6K | TPCC_1 15.8K; COST_D_1 15.5K; COST_FIHR_1 12.8K; COST_DEP_1 12.3K |
| COST_MEASURE_ACHIEVEMENT_POINTS_12 | amount | 45 | 345.6K | 7.5 35.9K; 7.6 23.0K; 7.3 15.9K; 7.4 13.0K |
| COST_MEASURE_ID_13 | category | 28 | 352.1K | COST_LBP_1 13.2K; COST_SSC_1 13.2K; COST_FIHR_1 9.8K; COST_EOPCI_1 9.6K |
| COST_MEASURE_ACHIEVEMENT_POINTS_13 | amount | 41 | 352.1K | 7.4 28.9K; 7.5 27.8K; 7.6 19.4K; 7.2 13.1K |
| COST_MEASURE_ID_14 | category | 28 | 360.3K | COST_LBP_1 12.7K; COST_CCLI_1 12.2K; COST_FIHR_1 10.5K; COST_SSC_1 9.7K |
| COST_MEASURE_ACHIEVEMENT_POINTS_14 | amount | 46 | 360.3K | 7.4 33.9K; 7.5 22.1K; 7.3 15.6K; 7.1 15.1K |
| COST_MEASURE_ID_15 | category | 27 | 367.4K | COST_D_1 20.4K; COST_LBP_1 16.1K; COST_DEP_1 9.3K; COST_CCLI_1 8.9K |
| COST_MEASURE_ACHIEVEMENT_POINTS_15 | amount | 42 | 367.4K | 7.4 29.2K; 7.5 18.5K; 7.3 18.4K; 7.2 13.5K |
| COST_MEASURE_ID_16 | category | 27 | 372.5K | COST_ACOPD_1 15.5K; COST_RUSST_1 10.2K; COST_HF_1 9.8K; COST_DEP_1 9.7K |
| COST_MEASURE_ACHIEVEMENT_POINTS_16 | amount | 41 | 372.5K | 7.4 26.1K; 7.3 18.4K; 7.1 15.9K; 7.5 15.3K |
| COST_MEASURE_ID_17 | category | 27 | 377.3K | COST_LPMSM_1 10.5K; COST_HF_1 10.1K; COST_KA_1 9.3K; COST_SSC_1 9.1K |
| COST_MEASURE_ACHIEVEMENT_POINTS_17 | amount | 46 | 377.3K | 7.2 21.0K; 7.3 19.6K; 7.4 16.4K; 7.0 12.9K |
| COST_MEASURE_ID_18 | category | 27 | 382.4K | COST_D_1 11.7K; TPCC_1 10.4K; COST_FIHR_1 9.8K; COST_ACOPD_1 9.8K |
| COST_MEASURE_ACHIEVEMENT_POINTS_18 | amount | 43 | 382.4K | 7.3 21.8K; 7.4 17.3K; 7.1 15.5K; 7.0 14.4K |
| COST_MEASURE_ID_19 | category | 27 | 388.8K | COST_DEP_1 16.8K; COST_ACOPD_1 14.4K; COST_SSC_1 9.5K; COST_D_1 8.6K |
| COST_MEASURE_ACHIEVEMENT_POINTS_19 | amount | 38 | 388.8K | 7.1 25.2K; 7.4 14.9K; 7.3 13.5K; 7.2 11.3K |
| COST_MEASURE_ID_20 | category | 27 | 393.7K | TPCC_1 11.0K; COST_LBP_1 9.7K; COST_ACOPD_1 7.8K; COST_PHA_1 7.5K |
| COST_MEASURE_ACHIEVEMENT_POINTS_20 | amount | 40 | 393.7K | 7.1 17.5K; 7.3 15.4K; 7.0 13.4K; 7.2 13.3K |
| COST_MEASURE_ID_21 | category | 26 | 399.0K | COST_HF_1 15.6K; TPCC_1 9.4K; COST_EOPCI_1 7.4K; COST_IHCI_1 6.6K |
| COST_MEASURE_ACHIEVEMENT_POINTS_21 | amount | 36 | 399.0K | 7.1 16.8K; 7.0 16.5K; 7.3 10.2K; 6.6 9.8K |
| COST_MEASURE_ID_22 | category | 26 | 402.5K | COST_ACOPD_1 10.2K; COST_HF_1 8.8K; COST_PHA_1 8.7K; COST_MR_1 7.2K |
| COST_MEASURE_ACHIEVEMENT_POINTS_22 | amount | 39 | 402.5K | 7.0 12.5K; 7.1 11.7K; 7.2 11.5K; 6.4 9.0K |
| COST_MEASURE_ID_23 | category | 26 | 407.6K | COST_PHA_1 11.1K; COST_RUSST_1 8.4K; COST_SSC_1 7.8K; COST_MR_1 7.5K |
| COST_MEASURE_ACHIEVEMENT_POINTS_23 | amount | 37 | 407.6K | 7.0 14.7K; 7.2 9.5K; 6.3 8.6K; 6.8 8.5K |
| COST_MEASURE_ID_24 | category | 24 | 411.6K | COST_LPMSM_1 11.2K; COST_SSC_1 8.0K; COST_IOL_1 7.3K; COST_ACOPD_1 7.3K |
| COST_MEASURE_ACHIEVEMENT_POINTS_24 | amount | 39 | 411.6K | 6.6 11.6K; 6.8 9.1K; 6.3 8.0K; 7.1 6.7K |
| COST_MEASURE_ID_25 | category | 26 | 419.8K | COST_PHA_1 7.7K; COST_EOPCI_1 7.6K; COST_IOL_1 7.2K; COST_RUSST_1 6.8K |
| COST_MEASURE_ACHIEVEMENT_POINTS_25 | amount | 36 | 419.8K | 6.5 8.3K; 6.9 7.1K; 6.8 6.7K; 5.7 6.0K |
| COST_MEASURE_ID_26 | category | 23 | 430.2K | COST_KA_1 7.9K; COST_CRR_1 7.2K; COST_LSFDD_1 6.8K; COST_IHCI_1 4.9K |
| COST_MEASURE_ACHIEVEMENT_POINTS_26 | amount | 33 | 430.2K | 6.8 6.7K; 5.4 5.2K; 6.5 5.0K; 4.9 4.8K |
| COST_MEASURE_ID_27 | category | 20 | 449.7K | COST_PRC_1 15.2K; COST_HAC_1 9.4K; COST_MR_1 4.5K; COST_NECABG_1 4.2K |
| COST_MEASURE_ACHIEVEMENT_POINTS_27 | amount | 33 | 449.7K | 6.4 8.6K; 6.2 5.6K; 5.9 5.4K; 1.0 4.1K |
| COST_MEASURE_ID_28 | category | 15 | 479.6K | COST_SSC_1 7.1K; COST_ACOPD_1 7.0K; COST_LGH_1 4.0K; COST_RUSST_1 2.6K |
| COST_MEASURE_ACHIEVEMENT_POINTS_28 | amount | 21 | 479.6K | 5.7 6.3K; 5.8 4.6K; 6.0 2.4K; 7.0 2.2K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 15:07:05.524 503.9K |
| _SOURCE_RUN_ID | audit id | 497.0K | 0 | 92e304fb-8519-4dea-86ac-9 349; 9d6e0226-62c3-42cc-b4b8-9 349; c1206f81-1d39-4d18-95b8-5 349; c7d0b439-54b1-46d6-93aa-6 349 |
