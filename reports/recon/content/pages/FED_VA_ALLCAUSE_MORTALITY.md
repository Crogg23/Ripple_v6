# FED_VA_ALLCAUSE_MORTALITY

rows 2.8K  columns 15  scan 3.8s

roles: amount 7, audit 2, category 3, other 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RANK | 2.8K | 0 | 24 | 44 | 45 | 63.2K |
| PERCENT | 1.8K | 0 | 1.07 | 100 | 100 | 10.8K |
| UNADJUSTED_RATE | 250 | 0 | 5.10 | 2.5K | 2.8K | 30.4K |
| AGE_ADJUSTED_RATE | 963 | 0.10 | 24.50 | 1.4K | 1.6K | 107.3K |
| YPLL | 1.8K | 20 | 2.9K | 1.01M | 2.00M | 83.59M |
| YPLL_2 | 1.8K | 0 | 0.46 | 100 | 100 | 10.8K |

## who

CAUSE_OF_DEATH by rows
        54  Complications of medical and surgical care
        54  In situ neoplasms, benign neoplasms, and neoplasms of
uncertain or unk
        54  Septicemia
        54  Shigellosis and amebiasis
        54  Inflammatory diseases of female pelvic organs
        54  Influenza and pneumonia
        54  Parkinson disease
        54  Hernia
        54  Essential hypertension and hypertensive renal disease
(hypertension)
        54  Legal intervention
        54  Diseases of appendix
        54  Arthropod-borne viral encephalitis
        54  Atherosclerosis
        54  Enterocolitis due to clostridium difficile
        54  Pregnancy, childbirth, and the puerperium
        54  Nephritis, nephrotic syndrome, and nephrosis (kidney
disease)
        54  Scarlet fever and erysipelas
        54  Operations of war and their sequelae
        54  Diabetes mellitus (diabetes)
        54  Malaria

CAUSE_OF_DEATH by dollars
        2.1K       54 rows  Scarlet fever and erysipelas
        2.1K       54 rows  Whooping cough
        2.1K       54 rows  Shigellosis and amebiasis
        2.1K       54 rows  Certain conditions originating in the perinatal period
        2.1K       54 rows  Malaria
        2.1K       54 rows  Meningococcal infection
        2.0K       54 rows  Inflammatory diseases of female pelvic organs
        2.0K       54 rows  Arthropod-borne viral encephalitis
        2.0K       54 rows  Syphilis
        2.0K       54 rows  Salmonella infections
        2.0K       54 rows  Operations of war and their sequelae
        1.9K       54 rows  Pregnancy, childbirth, and the puerperium
        1.9K       54 rows  Acute bronchitis and bronchiolitis
        1.8K       54 rows  Legal intervention
        1.8K       54 rows  Tuberculosis
        1.8K       54 rows  Meningitis
        1.8K       54 rows  Diseases of appendix
        1.7K       54 rows  Infections of kidney
        1.7K       54 rows  Pneumoconioses and chemical effects
        1.6K       54 rows  Hyperplasia of prostate

_SRC_SHA256 by rows
      2.8K  0e20bef1c6ba086a1e3a992b0bcc53e6ceedb309da47ffd8d14003b5aba0bf74

_SRC_SHA256 by dollars
       63.2K     2.8K rows  0e20bef1c6ba086a1e3a992b0bcc53e6ceedb309da47ffd8d14003b5aba0

## what

YEAR: 2023 17%, 2022 17%, 2021 17%, 2020 17%, 2019 17%, 2018 17%

COHORT: Other Veteran 33%, Recent-VHA Veteran 33%, Veteran 33%

SEX: Male 33%, Female 33%, All 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RANK | amount | 46 | 0 | . 108; 31 107; 28 105; 42 96 |
| CAUSE_OF_DEATH | who | 52 | 0 | Shigellosis and amebiasis 54; Whooping cough 54; Scarlet fever and erysipe 54; Arthropod-borne viral enc 54 |
| NUMBER | other | 1.3K | 0 | <10 849; 10-19 28; 30-39 28; 20-29 26 |
| PERCENT | amount | 432 | 0 | -- 1.1K; 0.1 185; 0.2 112; 0.0 97 |
| UNADJUSTED_RATE | amount | 165 | 2.5K | -- 62; 0.3 19; 0.1 17; 1.3 6 |
| AGE_ADJUSTED_RATE | amount | 769 | 0 | -- 1.8K; 1.9 8; 1.5 8; 1.4 7 |
| YPLL | amount | 1.6K | 0 | -- 1.1K; 676.00 10; 105.00 10; 241.00 10 |
| YPLL_2 | amount | 409 | 0 | -- 1.1K; 0.1 190; 0.3 127; 0.0 115 |
| YEAR | category | 6 | 0 | 2023 468; 2022 468; 2021 468; 2020 468 |
| COHORT | category | 3 | 0 | Other Veteran 936; Recent-VHA Veteran 936; Veteran 936 |
| SEX | category | 3 | 0 | Male 936; Female 936; All 936 |
| CRUDE_RATE | amount | 1.1K | 312 | -- 995; 0.4 13; 1.6 11; 0.5 11 |
| _INGESTED_AT | audit | 1 | 0 | 1786325075964258 2.8K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 07d15db6-4fe6-488d-93c3-3 2.8K |
| _SRC_SHA256 | who | 1 | 0 | 0e20bef1c6ba086a1e3a992b0 2.8K |
