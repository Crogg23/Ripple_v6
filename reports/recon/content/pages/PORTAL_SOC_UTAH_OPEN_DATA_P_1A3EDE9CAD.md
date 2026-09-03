# PORTAL_SOC_UTAH_OPEN_DATA_P_1A3EDE9CAD

rows 643  columns 12  scan 4.0s

roles: amount 4, audit 2, category 2, date 1, other 2, who 2

## when

INGESTED_AT
  2026       643  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_PROVIDER_PAYMENT_25 | 643 | 775.80 | 9.2K | 72.1K | 145.4K | 8.84M |
| TOTAL_PROVIDER_PAYMENT_50 | 643 | 775.80 | 10.8K | 114.0K | 347.4K | 11.79M |
| TOTAL_PROVIDER_PAYMENT_75 | 643 | 775.80 | 13.5K | 188.3K | 590.2K | 16.01M |
| CLAIM_CNT_TOTAL | 643 | 11 | 22 | 691.96 | 1.2K | 40.2K |

## who

DESCRIPTION by rows
        38  Vaginal Delivery w/o Complicating Diagnoses
        36  Normal Newborn
        30  Major Joint Replacement or Reattachment of Lower Extremity w/o MCC
        29  Cesarean Section w/o CC/MCC
        26  Neonate w Other Significant Problems
        22  Vaginal Delivery w Complicating Diagnoses
        19  Cesarean Section w CC/MCC
        18  Full Term Neonate w Major Problems
        15  Psychoses
        14  Septicemia or Severe Sepsis w/o MV 96+ Hours w MCC
        14  Spinal Fusion except Cervical w/o MCC
        10  Prematurity w/o Major Problems
        10  Septicemia or Severe Sepsis w/o MV 96+ Hours w/o MCC
        10  Extreme Immaturity or Respiratory Distress Syndrome, Neonate
        10  Vaginal Delivery w Sterilization &/or D&C
        10  Uterine & Adnexa Proc for Non-Malignancy w/o CC/MCC
         9  Esophagitis, Gastroent & Misc Digest Disorders w/o MCC
         8  Major Small & Large Bowel Procedures w CC
         7  Perc Cardiovasc Proc w Drug-Eluting Stent w/o MCC
         7  Cervical Spinal Fusion w/o CC/MCC

DESCRIPTION by dollars
      718.7K       30 rows  Major Joint Replacement or Reattachment of Lower Extremity w
      511.1K       14 rows  Spinal Fusion except Cervical w/o MCC
      438.0K       10 rows  Extreme Immaturity or Respiratory Distress Syndrome, Neonate
      229.2K       29 rows  Cesarean Section w/o CC/MCC
      211.6K        8 rows  Major Small & Large Bowel Procedures w CC
      207.6K        7 rows  Perc Cardiovasc Proc w Drug-Eluting Stent w/o MCC
      191.8K       38 rows  Vaginal Delivery w/o Complicating Diagnoses
      178.4K       14 rows  Septicemia or Severe Sepsis w/o MV 96+ Hours w MCC
      171.4K       19 rows  Cesarean Section w CC/MCC
      145.4K        1 rows  Acute Leukemia w/o Major O.R. Procedure w MCC
      145.4K        7 rows  Cervical Spinal Fusion w/o CC/MCC
      135.1K        4 rows  Infectious & Parasitic Diseases w O.R. Procedure w MCC
      125.5K        4 rows  Major Joint/limb Reattachment Procedure of Upper Extremities
      122.8K       22 rows  Vaginal Delivery w Complicating Diagnoses
      119.5K        1 rows  Other Cardiothoracic Procedures w MCC
      117.3K        2 rows  Kidney Transplant
      115.9K        6 rows  Lower Extrem & Humer Proc except Hip,Foot,Femur w/o CC/MCC
      112.8K        1 rows  Cardiac Valve & Oth Maj Cardiothoracic Proc w/o Card Cath w 
      109.6K        2 rows  Other Cardiothoracic Procedures w CC
      108.2K        4 rows  Craniotomy & Endovascular Intracranial Procedures w/o CC/MCC

SRC_SHA256 by rows
       643  3834699b796d08e2243b7b0eb79e9e3516b63887cde22bbececc2a57693f291b

SRC_SHA256 by dollars
       8.84M      643 rows  3834699b796d08e2243b7b0eb79e9e3516b63887cde22bbececc2a57693f

## who x when

DESCRIPTION by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_PROVIDER_PAYMENT_25
  Acute Leukemia w/o Major O.R. Procedure   2026:145.4K
  Cardiac Valve & Oth Maj Cardiothoracic P  2026:112.8K
  Cervical Spinal Fusion w/o CC/MCC         2026:145.4K
  Cesarean Section w CC/MCC                 2026:171.4K
  Cesarean Section w/o CC/MCC               2026:229.2K
  Craniotomy & Endovascular Intracranial P  2026:108.2K
  Esophagitis, Gastroent & Misc Digest Dis  2026:76.8K
  Extreme Immaturity or Respiratory Distre  2026:438.0K
  Full Term Neonate w Major Problems        2026:88.9K
  Infectious & Parasitic Diseases w O.R. P  2026:135.1K
  Kidney Transplant                         2026:117.3K
  Lower Extrem & Humer Proc except Hip,Foo  2026:115.9K
  Major Joint Replacement or Reattachment   2026:718.7K
  Major Joint/limb Reattachment Procedure   2026:125.5K
  Major Small & Large Bowel Procedures w C  2026:211.6K
  Neonate w Other Significant Problems      2026:61.9K
  Normal Newborn                            2026:63.7K
  Other Cardiothoracic Procedures w CC      2026:109.6K
  Other Cardiothoracic Procedures w MCC     2026:119.5K
  Perc Cardiovasc Proc w Drug-Eluting Sten  2026:207.6K
  Prematurity w/o Major Problems            2026:35.2K
  Psychoses                                 2026:75.5K
  Septicemia or Severe Sepsis w/o MV 96+ H  2026:178.4K
  Septicemia or Severe Sepsis w/o MV 96+ H  2026:102.1K
  Spinal Fusion except Cervical w/o MCC     2026:511.1K
  Uterine & Adnexa Proc for Non-Malignancy  2026:95.4K
  Vaginal Delivery w Complicating Diagnose  2026:122.8K
  Vaginal Delivery w Sterilization &/or D&  2026:64.7K
  Vaginal Delivery w/o Complicating Diagno  2026:191.8K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_PROVIDER_PAYMENT_25
  3834699b796d08e2243b7b0eb79e9e3516b63887  2026:8.84M

## what

PROVIDER_ORGANIZATION_NAME: IHC HEALTH SERVICES INC 37%, IHC HEALTH SERVICES INC. 28%, UNIVERSITY OF UTAH 11%, IHC HEALTH SERVICES, INC. 8%, NORTHERN UTAH HEALTH CARE CORP 3%, JORDAN VALLEY MEDICAL CENTER L 3%, COLUMBIA OGDEN MEDICAL CENTER, 2%, DAVIS HOSPITAL & MEDICAL CENTE 2%, TIMPANOGOS REGIONAL MEDICAL SE 2%, MOUNTAIN VIEW HOSPITAL, INC. 2%, SALT LAKE REGIONAL MEDICAL CEN 2%, UINTAH BASIN MEDICAL CENTER 1%

PROVIDER_OTHER_ORGANIZATION: INTERMOUNTAIN MEDICAL CENTER 18%, PRIMARY CHILDRENS HOSPITAL 14%, UTAH VALLEY HOSPITAL 12%, UNIVERSITY HEALTH CARE HOSPITA 12%, nan 11%, MCKAY DEE HOSPITAL 8%, DIXIE REGIONAL MEDICAL CENTER 6%, LDS HOSPITAL 5%, RIVERTON HOSPITAL 5%, ST. MARK'S HOSPITAL 4%, AMERICAN FORK HOSPITAL 3%, OGDEN REGIONAL MEDICAL CENTER 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | other | 52 | 0 | 1043220650 92; 1235148594 70; 1114025491 63; 1588656870 61 |
| PROVIDER_ORGANIZATION_NAME | category | 32 | 0 | IHC HEALTH SERVICES INC 214; IHC HEALTH SERVICES INC. 161; UNIVERSITY OF UTAH 63; IHC HEALTH SERVICES, INC. 48 |
| MSDRG | other | 168 | 0 | 775 38; 795 36; 470 30; 766 29 |
| DESCRIPTION | who | 168 | 0 | Vaginal Delivery w/o Comp 38; Normal Newborn 36; Major Joint Replacement o 30; Cesarean Section w/o CC/M 29 |
| TOTAL_PROVIDER_PAYMENT_25 | amount | 585 | 0 | 1774.60 8; 28051.52 8; 4810.10 6; 2178.52 4 |
| TOTAL_PROVIDER_PAYMENT_50 | amount | 548 | 0 | 1778.10 8; 2271.75 8; 4819.58 8; 7728.87 8 |
| TOTAL_PROVIDER_PAYMENT_75 | amount | 598 | 0 | 7728.87 5; 9226.21 5; 3636.78 4; 8309.94 4 |
| CLAIM_CNT_TOTAL | amount | 151 | 0 | 11 55; 13 48; 12 43; 15 29 |
| PROVIDER_OTHER_ORGANIZATION | category | 43 | 0 | INTERMOUNTAIN MEDICAL CEN 92; PRIMARY CHILDRENS HOSPITA 70; UTAH VALLEY HOSPITAL 63; UNIVERSITY HEALTH CARE HO 61 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:44:17.95733 643 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7957536b-c922-4fe5-92e5-4 643 |
| SRC_SHA256 | who | 1 | 0 | 3834699b796d08e2243b7b0eb 643 |
