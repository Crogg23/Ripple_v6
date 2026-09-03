# PORTAL_CKA_CALIFORNIA_OPEN_B36AD1F596

rows 10.0K  columns 16  scan 4.9s

roles: amount 2, audit 2, category 5, date 1, other 3, who 4

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MEDIAN_OOP_AMT | 7.9K | 0 | 19.25 | 1.9K | 2.8K | 1.47M |
| PERCENT_ZERO_OOP | 7.9K | 0 | 0.24 | 1 | 1 | 2.8K |

## who

VISIT_TYPE_NAME by rows
       198  Sleeve Gastrectomy: Laparoscopic
       198  Knee Arthroscopy
       198  Drain/Injection Joint with Ultrasound Guidance
       198  Breast Biopsy Including Ultrasound Guidance
       198  Mastectomy (Partial): Outpatient
       198  Diagnostic Colonoscopy - All Service Settings
       198  Drain/Injection Joint without Ultrasound Guidance
       198  Upper Endoscopy of Esophagus, Stomach and Duodenum (EGD) - All Service
       198  Gastric Bypass: Laparoscopic
       166  Colonoscopy and Biopsy - All Service Settings
       132  Coronary Angioplasty: Outpatient
       132  Preventive Visit Ages 12-17
       132  Preventive Visit Ages 5-11
       132  Brief Emotional/Behavioral Health Assessment
       132  Psychotherapy (Group)
       132  Total Hysterectomy: Inpatient
       132  Physical Therapy Evaluation and Treatment Plan
       132  Coronary Artery Angiogram
       132  Office Visit Existing Patient: 30 Minutes
       132  Office Visit: Evening, Weekend, Holiday

VISIT_TYPE_NAME by dollars
      176.5K      132 rows  Total Hip or Knee Replacement
      124.6K      132 rows  Spinal Fusion
       83.7K      132 rows  Cesarean Section
       78.1K      132 rows  Coronary Artery Angiogram
       72.3K      132 rows  Coronary Bypass
       65.7K      132 rows  Coronary Angioplasty: Outpatient
       63.9K      132 rows  Total Hysterectomy: Inpatient
       63.7K      132 rows  Laminectomy
       62.3K      132 rows  Vaginal Delivery
       50.0K      132 rows  Cataract Removal with Implant of Lens – All Service Settings
       48.1K      198 rows  Knee Arthroscopy
       47.8K      132 rows  Discectomy
       46.5K      132 rows  Total Knee Replacement: Outpatient
       41.3K      198 rows  Mastectomy (Partial): Outpatient
       38.7K      132 rows  Bariatric (Weight loss) Surgery
       37.2K      132 rows  Prostatectomy (TURP)
       28.6K      198 rows  Upper Endoscopy of Esophagus, Stomach and Duodenum (EGD) - A
       28.5K      132 rows  Total Hysterectomy: Laparoscopic
       27.7K      132 rows  Hysteroscopy with Biopsy
       27.5K      132 rows  Prostatectomy

MEMBER_MONTHS by rows
       141  42306011
       140  8831470
       140  7632101
       139  8347941
       139  14571632
       139  8873879
       139  3584658
       138  10039097
       138  6822496
       138  9368115
       138  13886556
       138  10413565
       136  6288068
       136  4639752
       135  4011804
       135  5935477
       134  2851393
       134  3437937
       133  3105592
       132  3047738

MEMBER_MONTHS by dollars
       62.6K      134 rows  3437937
       53.1K      118 rows  1199030
       52.5K      123 rows  1189422
       52.1K      139 rows  3584658
       47.9K      121 rows  1482066
       47.3K      113 rows  564592
       44.5K      118 rows  674961
       40.0K      132 rows  3047738
       38.4K      127 rows  1300685
       36.1K      138 rows  9368115
       32.9K      122 rows  1146945
       32.3K      139 rows  14571632
       30.9K      113 rows  832307
       30.2K      129 rows  3921118
       30.2K      129 rows  2013642
       29.9K      106 rows  425928
       29.0K      128 rows  2085027
       28.7K      134 rows  2851393
       28.3K      138 rows  10039097
       26.7K      118 rows  890375

GEO_VALUE by rows
       152  Los Angeles
       152  Butte
       152  Calaveras
       152  Mono
       152  Kings
       152  Imperial
       152  Lassen
       152  Madera
       152  Marin
       152  Mendocino
       152  Placer
       152  Colusa
       152  Napa
       152  Plumas
       152  Merced
       152  Alpine
       152  Nevada
       152  Sacramento
       152  Humboldt
       152  Amador

GEO_VALUE by dollars
       62.6K      151 rows  West
       53.1K      152 rows  Monterey
       52.5K      151 rows  San Luis Obispo
       52.1K      151 rows  Ventura
       47.9K      151 rows  Santa Barbara
       47.3K      151 rows  Shasta
       44.5K      152 rows  Butte
       40.0K      152 rows  Fresno
       38.4K      151 rows  Tulare
       36.1K      151 rows  San Fernando Valley
       32.9K      151 rows  Santa Cruz
       32.3K      152 rows  Orange
       30.9K      152 rows  Merced
       30.2K      151 rows  Metro
       30.2K      151 rows  Stanislaus
       29.9K      152 rows  Humboldt
       29.0K      152 rows  Placer
       28.7K      152 rows  Kern
       28.3K      151 rows  Santa Clara
       26.7K      152 rows  El Dorado

SRC_SHA256 by rows
     10.0K  39297be0d1d1254b1496e29f6c764164fa4d2bffe8ba4445a9f8d6c6dd5c2c9b

SRC_SHA256 by dollars
       1.47M    10.0K rows  39297be0d1d1254b1496e29f6c764164fa4d2bffe8ba4445a9f8d6c6dd5c

## who x when

VISIT_TYPE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = MEDIAN_OOP_AMT
  Bariatric (Weight loss) Surgery           2026:38.7K
  Breast Biopsy Including Ultrasound Guida  2026:24.1K
  Brief Emotional/Behavioral Health Assess  2026:19.64
  Cataract Removal with Implant of Lens –   2026:50.0K
  Cesarean Section                          2026:83.7K
  Colonoscopy and Biopsy - All Service Set  2026:15.9K
  Coronary Angioplasty: Outpatient          2026:65.7K
  Coronary Artery Angiogram                 2026:78.1K
  Coronary Bypass                           2026:72.3K
  Diagnostic Colonoscopy - All Service Set  2026:5.1K
  Discectomy                                2026:47.8K
  Drain/Injection Joint with Ultrasound Gu  2026:2.2K
  Drain/Injection Joint without Ultrasound  2026:1.6K
  Gastric Bypass: Laparoscopic              2026:0
  Knee Arthroscopy                          2026:48.1K
  Laminectomy                               2026:63.7K
  Mastectomy (Partial): Outpatient          2026:41.3K
  Office Visit Existing Patient: 30 Minute  2026:2.7K
  Office Visit: Evening, Weekend, Holiday   2026:0
  Physical Therapy Evaluation and Treatmen  2026:1.8K
  Preventive Visit Ages 12-17               2026:0
  Preventive Visit Ages 5-11                2026:0
  Psychotherapy (Group)                     2026:827.47
  Sleeve Gastrectomy: Laparoscopic          2026:53.05
  Spinal Fusion                             2026:124.6K
  Total Hip or Knee Replacement             2026:176.5K
  Total Hysterectomy: Inpatient             2026:63.9K
  Total Knee Replacement: Outpatient        2026:46.5K
  Upper Endoscopy of Esophagus, Stomach an  2026:28.6K
  Vaginal Delivery                          2026:62.3K

MEMBER_MONTHS by INGESTED_AT  LOAD STAMP, not an event date, dollars = MEDIAN_OOP_AMT
  10039097                                  2026:28.3K
  10413565                                  2026:19.1K
  1146945                                   2026:32.9K
  1189422                                   2026:52.5K
  1199030                                   2026:53.1K
  1300685                                   2026:38.4K
  13886556                                  2026:24.4K
  14571632                                  2026:32.3K
  1482066                                   2026:47.9K
  2013642                                   2026:30.2K
  2851393                                   2026:28.7K
  3047738                                   2026:40.0K
  3105592                                   2026:25.5K
  3437937                                   2026:62.6K
  3584658                                   2026:52.1K
  3921118                                   2026:30.2K
  4011804                                   2026:25.3K
  42306011                                  2026:25.5K
  4639752                                   2026:19.5K
  564592                                    2026:47.3K
  5935477                                   2026:18.7K
  6288068                                   2026:12.7K
  674961                                    2026:44.5K
  6822496                                   2026:24.5K
  7632101                                   2026:10.9K
  832307                                    2026:30.9K
  8347941                                   2026:15.0K
  8831470                                   2026:18.9K
  8873879                                   2026:21.3K
  9368115                                   2026:36.1K

## what

PAYER_TYPE: Commercial + Medicare 47%, Commercial 47%, Medi-Cal 6%

VISIT_CATEGORY_ID: 2 41%, 4 25%, 3 22%, 5 12%

VISIT_CATEGORY_NAME: Outpatient Surgery 41%, Professional 25%, Outpatient Diagnostic 22%, Inpatient 12%

GEO_TYPE: County 88%, LA SPA 12%

SUPPRESSION_IND: N 79%, Y 21%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORTING_YEAR | other | 1 | 0 | 2018 10.0K |
| PAYER_TYPE | category | 3 | 0 | Commercial + Medicare 4.7K; Commercial 4.7K; Medi-Cal 628 |
| VISIT_TYPE_ID | other | 72 | 0 | 28 198; 27 198; 26 198; 25 198 |
| VISIT_TYPE_NAME | who | 71 | 0 | Diagnostic Colonoscopy -  198; Sleeve Gastrectomy: Lapar 198; Gastric Bypass: Laparosco 198; Upper Endoscopy of Esopha 198 |
| VISIT_CATEGORY_ID | category | 4 | 0 | 2 4.1K; 4 2.5K; 3 2.2K; 5 1.2K |
| VISIT_CATEGORY_NAME | category | 4 | 0 | Outpatient Surgery 4.1K; Professional 2.5K; Outpatient Diagnostic 2.2K; Inpatient 1.2K |
| GEO_TYPE | category | 2 | 0 | County 8.8K; LA SPA 1.2K |
| GEO_VALUE | who | 67 | 0 | Sacramento 152; Riverside 152; Plumas 152; Placer 152 |
| MEMBER_MONTHS | who | 139 | 2.1K | 42306011 141; 7632101 140; 8831470 140; 3584658 139 |
| VISIT_COUNT | other | 3.7K | 2.1K | 0 554; 33 45; 35 43; 37 43 |
| MEDIAN_OOP_AMT | amount | 4.2K | 2.1K | 0.0 2.1K; 20.0 123; 250.0 80; 15.0 49 |
| PERCENT_ZERO_OOP | amount | 4.1K | 2.1K | 0.0 576; 1.0 331; 0.9998 42; 0.9996 40 |
| SUPPRESSION_IND | category | 2 | 0 | N 7.9K; Y 2.1K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:57:53.38926 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 795ad875-62d6-4530-b963-8 10.0K |
| SRC_SHA256 | who | 1 | 0 | 39297be0d1d1254b1496e29f6 10.0K |
