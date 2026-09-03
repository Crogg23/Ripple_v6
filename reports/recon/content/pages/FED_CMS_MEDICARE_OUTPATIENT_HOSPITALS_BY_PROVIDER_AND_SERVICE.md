# FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE

rows 116.2K  columns 20  scan 5.5s

roles: amount 5, audit 2, category 2, date 1, id 1, other 5, state 1, who 5

## when

_INGESTED_AT
  2026    116.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RNDRNG_PRVDR_RUCA | 116.2K | 1 | 1 | 10 | 99 | 249.0K |
| AVG_TOT_SBMTD_CHRGS | 63.5K | 173.11 | 26.2K | 222.9K | 736.7K | 2.63B |
| AVG_MDCR_ALOWD_AMT | 63.5K | 216.14 | 3.6K | 29.9K | 58.5K | 390.95M |
| AVG_MDCR_PYMT_AMT | 63.5K | 70.61 | 2.8K | 28.3K | 56.8K | 332.45M |
| AVG_MDCR_OUTLIER_AMT | 47.5K | 0 | 0 | 4.7K | 31.9K | 9.70M |

## who

RNDRNG_PRVDR_ORG_NAME by rows
       181  Mercy Medical Center
       180  Memorial Hospital
       177  St Joseph Medical Center
       174  Memorial Medical Center
       172  St Lukes Hospital
       162  Good Samaritan Hospital
       146  Mercy Hospital
       142  St Mary's Medical Center
       135  Saint Francis Medical Center
       131  Northwest Medical Center
       123  Methodist Hospital
       118  Doctors Hospital
       118  St Mary Medical Center
       117  Community Hospital
       115  St Joseph Hospital
       112  Huntington Hospital
       112  Covenant Medical Center
       111  University Medical Center
       110  Wakemed
       109  Grady Memorial Hospital

RNDRNG_PRVDR_ORG_NAME by dollars
      917.7K      174 rows  Memorial Medical Center
      817.9K      172 rows  St Lukes Hospital
      765.8K      162 rows  Good Samaritan Hospital
      728.1K      123 rows  Methodist Hospital
      699.7K       68 rows  Ucsf Medical Center
      696.0K       67 rows  Stanford Health Care
      645.8K       68 rows  Nyu Langone Hospitals
      634.8K      112 rows  Huntington Hospital
      630.3K      146 rows  Mercy Hospital
      599.3K       66 rows  New York-Presbyterian Hospital
      595.9K      135 rows  Saint Francis Medical Center
      581.1K      177 rows  St Joseph Medical Center
      579.3K       67 rows  Uc San Diego Health Hillcrest - Hillcrest Med Ctr
      565.4K       66 rows  Cedars-Sinai Medical Center
      561.4K       71 rows  Ronald Reagan Ucla Medical Center
      560.5K      117 rows  Community Hospital
      559.4K       67 rows  University Of California Davis Medical Center
      534.8K       66 rows  Yale-New Haven Hospital
      526.3K       65 rows  Stony Brook University Hospital
      524.3K       61 rows  El Camino Hospital

RNDRNG_PRVDR_ST by rows
       173  1 Medical Center Drive
       123  One Hospital Drive
        95  100 Hospital Drive
        77  100 Medical Center Drive
        71  757 Westwood Plaza
        69  1216 Second Street Southwest
        69  2301  Erwin Rd
        69  9500 Euclid Avenue
        68  1 Tampa General Cir
        68  1500 E Medical Center Drive, Spc 5474
        68  550 First Avenue
        68  11100 Euclid Avenue
        68  5841 South Maryland
        68  200 Hawkins Drive
        68  169 Ashley Ave
        68  505 Parnassus Ave, Box 0296
        67  9200 W Wisconsin Ave
        67  80 Seymour Street
        67  2315 Stockton Boulevard
        67  200 West Arbor Drive

RNDRNG_PRVDR_ST by dollars
      839.5K      173 rows  1 Medical Center Drive
      699.7K       68 rows  505 Parnassus Ave, Box 0296
      696.0K       67 rows  300 Pasteur Drive
      645.8K       68 rows  550 First Avenue
      599.3K       66 rows  525 East 68th Street
      579.3K       67 rows  200 West Arbor Drive
      565.4K       66 rows  8700 Beverly Blvd
      561.4K       71 rows  757 Westwood Plaza
      559.4K       67 rows  2315 Stockton Boulevard
      534.8K       66 rows  20 York St
      526.3K       65 rows  Health Sciences Center Suny
      524.3K       61 rows  2500 Grant Road
      523.1K       69 rows  1216 Second Street Southwest
      511.7K       65 rows  4755 Ogletown-Stanton Road
      501.9K       66 rows  251 E Huron St
      499.2K       67 rows  6565 Fannin
      489.9K      123 rows  One Hospital Drive
      489.0K       67 rows  41 & 45 Mall Road
      483.6K       65 rows  3181 Sw Sam Jackson Park Road
      478.5K       61 rows  2825 Capitol Avenue

RNDRNG_PRVDR_CCN by rows
        71  050262
        69  340030
        69  360180
        69  240010
        68  160058
        68  140088
        68  330214
        68  420004
        68  230046
        68  100128
        68  050454
        67  050025
        67  490032
        67  100007
        67  510001
        67  450358
        67  030103
        67  460009
        67  170040
        67  220171

RNDRNG_PRVDR_CCN by dollars
      699.7K       68 rows  050454
      696.0K       67 rows  050441
      645.8K       68 rows  330214
      599.3K       66 rows  330101
      579.3K       67 rows  050025
      565.4K       66 rows  050625
      561.4K       71 rows  050262
      559.4K       67 rows  050599
      534.8K       66 rows  070022
      526.3K       65 rows  330393
      524.3K       61 rows  050308
      523.1K       69 rows  240010
      511.7K       65 rows  080001
      501.9K       66 rows  140281
      499.2K       67 rows  450358
      489.0K       67 rows  220171
      483.6K       65 rows  380009
      478.5K       61 rows  050108
      476.2K       64 rows  220163
      475.9K       63 rows  050696

APC_DESC by rows
      2.9K  Comprehensive Observation Services
      2.9K  Level 2 Excision/ Biopsy/ Incision and Drainage
      2.8K  Level 3 Vascular Procedures
      2.8K  Level 2 Musculoskeletal Procedures
      2.8K  Level 3 Excision/ Biopsy/ Incision and Drainage
      2.8K  Level 3 Musculoskeletal Procedures
      2.8K  Level 1 Laparoscopy and Related Services
      2.7K  Level 4 Musculoskeletal Procedures
      2.7K  Level 2 Upper GI Procedures
      2.7K  Level 1 Abdominal/Peritoneal/Biliary and Related Procedures
      2.7K  Level 2 Vascular Procedures
      2.6K  Level 5 Musculoskeletal Procedures
      2.6K  Level 1 Nerve Procedures
      2.5K  Level 3 Urology and Related Services
      2.4K  Level 4 Urology and Related Services
      2.4K  Level 4 Gynecologic Procedures
      2.4K  Level 1 Breast/Lymphatic Surgery and Related Procedures
      2.3K  Level 6 Musculoskeletal Procedures
      2.3K  Level 3 Lower GI Procedures
      2.3K  Level 5 Urology and Related Services

APC_DESC by dollars
      27.33M     2.6K rows  Level 5 Musculoskeletal Procedures
      25.82M     2.3K rows  Level 6 Musculoskeletal Procedures
      24.41M     1.5K rows  Level 2 ICD and Similar Procedures
      21.47M     1.1K rows  Level 3 Electrophysiologic Procedures
      17.78M     1.8K rows  Level 4 Endovascular Procedures
      17.41M     1.6K rows  Level 5 Neurostimulator and Related Procedures
      16.17M     2.0K rows  Level 3 Endovascular Procedures
      15.01M     2.7K rows  Level 4 Musculoskeletal Procedures
      13.20M     1.8K rows  Level 3 Pacemaker and Similar Procedures
      12.34M     2.3K rows  Level 2 Laparoscopy and Related Services
      12.17M     2.8K rows  Level 1 Laparoscopy and Related Services
      10.24M     1.3K rows  Level 4 Pacemaker and Similar Procedures
       9.45M     1.6K rows  Level 4 Neurostimulator and Related Procedures
       9.41M     2.3K rows  Level 5 Urology and Related Services
       7.57M     2.2K rows  Level 2 Breast/Lymphatic Surgery and Related Procedures
       7.47M     1.8K rows  Level 2 Pacemaker and Similar Procedures
       7.13M     2.9K rows  Comprehensive Observation Services
       6.95M     2.0K rows  Level 2 Endovascular Procedures
       6.55M     2.4K rows  Level 4 Urology and Related Services
       6.42M     2.8K rows  Level 3 Vascular Procedures

## who x when

RNDRNG_PRVDR_ORG_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = AVG_MDCR_ALOWD_AMT
  Cedars-Sinai Medical Center               2026:565.4K
  Community Hospital                        2026:560.5K
  Covenant Medical Center                   2026:442.7K
  Doctors Hospital                          2026:226.8K
  Good Samaritan Hospital                   2026:765.8K
  Grady Memorial Hospital                   2026:157.7K
  Huntington Hospital                       2026:634.8K
  Memorial Hospital                         2026:391.7K
  Memorial Medical Center                   2026:917.7K
  Mercy Hospital                            2026:630.3K
  Mercy Medical Center                      2026:486.9K
  Methodist Hospital                        2026:728.1K
  New York-Presbyterian Hospital            2026:599.3K
  Northwest Medical Center                  2026:462.9K
  Nyu Langone Hospitals                     2026:645.8K
  Ronald Reagan Ucla Medical Center         2026:561.4K
  Saint Francis Medical Center              2026:595.9K
  St Joseph Hospital                        2026:278.4K
  St Joseph Medical Center                  2026:581.1K
  St Lukes Hospital                         2026:817.9K
  St Mary Medical Center                    2026:330.3K
  St Mary's Medical Center                  2026:409.4K
  Stanford Health Care                      2026:696.0K
  Stony Brook University Hospital           2026:526.3K
  Uc San Diego Health Hillcrest - Hillcres  2026:579.3K
  Ucsf Medical Center                       2026:699.7K
  University Medical Center                 2026:360.6K
  University Of California Davis Medical C  2026:559.4K
  Wakemed                                   2026:436.6K
  Yale-New Haven Hospital                   2026:534.8K

RNDRNG_PRVDR_ST by _INGESTED_AT  LOAD STAMP, not an event date, dollars = AVG_MDCR_ALOWD_AMT
  1 Medical Center Drive                    2026:839.5K
  1 Tampa General Cir                       2026:405.0K
  100 Hospital Drive                        2026:236.0K
  100 Medical Center Drive                  2026:153.3K
  11100 Euclid Avenue                       2026:300.3K
  1216 Second Street Southwest              2026:523.1K
  1500 E Medical Center Drive, Spc 5474     2026:442.8K
  169 Ashley Ave                            2026:418.1K
  20 York St                                2026:534.8K
  200 Hawkins Drive                         2026:436.9K
  200 West Arbor Drive                      2026:579.3K
  2301  Erwin Rd                            2026:464.4K
  2315 Stockton Boulevard                   2026:559.4K
  2500 Grant Road                           2026:524.3K
  251 E Huron St                            2026:501.9K
  300 Pasteur Drive                         2026:696.0K
  41 & 45 Mall Road                         2026:489.0K
  4755 Ogletown-Stanton Road                2026:511.7K
  505 Parnassus Ave, Box 0296               2026:699.7K
  525 East 68th Street                      2026:599.3K
  550 First Avenue                          2026:645.8K
  5841 South Maryland                       2026:393.2K
  6565 Fannin                               2026:499.2K
  757 Westwood Plaza                        2026:561.4K
  80 Seymour Street                         2026:467.8K
  8700 Beverly Blvd                         2026:565.4K
  9200 W Wisconsin Ave                      2026:370.7K
  9500 Euclid Avenue                        2026:455.3K
  Health Sciences Center Suny               2026:526.3K
  One Hospital Drive                        2026:489.9K

## where

RNDRNG_PRVDR_STATE_ABRVTN: CA 10.2K, TX 9.6K, FL 7.2K, PA 5.4K, NY 5.3K, OH 5.1K, IL 4.8K, GA 3.7K, MI 3.7K, NC 3.4K, IN 3.1K, VA 2.8K

## what

RNDRNG_PRVDR_STATE_FIPS: 06 16%, 48 15%, 12 11%, 42 8%, 36 8%, 39 8%, 17 7%, 13 6%, 26 6%, 37 5%, 18 5%, 51 4%

RNDRNG_PRVDR_RUCA_DESC: Metropolitan area core: primar 76%, Micropolitan area core: primar 14%, Small town core: primary flow  3%, Metropolitan area high commuti 2%, Secondary flow 30% to <50% to  2%, Secondary flow 30% to <50% to  1%, Rural areas: primary flow to a 1%, Micropolitan high commuting: p 1%, Unknown 0%, Small town high commuting: pri 0%, Metropolitan area low commutin 0%, Secondary flow 30% to <50% to  0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RNDRNG_PRVDR_CCN | who | 3.1K | 0 | 670122 614; 670088 613; 670260 610; 670077 608 |
| RNDRNG_PRVDR_ORG_NAME | who | 3.1K | 0 | Houston Methodist The Woo 614; Baylor Scott & White Medi 613; Texas Health Hospital Fri 610; Houston Methodist West Ho 608 |
| RNDRNG_PRVDR_ST | who | 3.1K | 0 | 17201 Interstate 45 South 614; 700 Scott & White Drive 613; 12400 N Dallas Parkway 611; 18500 Katy Freeway 608 |
| RNDRNG_PRVDR_CITY | who | 1.8K | 0 | Houston 1.3K; Chicago 980; Dallas 974; Philadelphia 945 |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 50 | 0 | CA 10.2K; TX 9.6K; FL 7.2K; PA 5.4K |
| RNDRNG_PRVDR_STATE_FIPS | category | 50 | 0 | 06 10.2K; 48 9.6K; 12 7.2K; 42 5.4K |
| RNDRNG_PRVDR_ZIP5 | other | 2.9K | 0 | 77030 793; 76104 684; 54601 645; 78664 643 |
| RNDRNG_PRVDR_RUCA | amount | 18 | 0 | 1 88.2K; 4 16.0K; 7 3.8K; 2 2.6K |
| RNDRNG_PRVDR_RUCA_DESC | category | 14 | 0 | Metropolitan area core: p 88.2K; Micropolitan area core: p 16.0K; Small town core: primary  3.8K; Metropolitan area high co 2.6K |
| APC_CD | other | 72 | 0 | 8011 2.9K; 5072 2.9K; 5183 2.8K; 5112 2.8K |
| APC_DESC | who | 72 | 0 | Comprehensive Observation 2.9K; Level 2 Excision/ Biopsy/ 2.9K; Level 3 Vascular Procedur 2.8K; Level 2 Musculoskeletal P 2.8K |
| BENE_CNT | other | 978 | 53.8K | 11 2.2K; 12 2.1K; 13 2.0K; 14 1.7K |
| CAPC_SRVCS | other | 1.1K | 52.7K | 11 2.2K; 12 2.0K; 13 1.9K; 14 1.7K |
| AVG_TOT_SBMTD_CHRGS | amount | 63.5K | 52.7K | 7430.03590163932 318; 235634.210869564 318; 329630.442857142 318; 357081.683636363 318 |
| AVG_MDCR_ALOWD_AMT | amount | 53.7K | 52.7K | 27863.37 319; 11865.9799999999 319; 5209.03999999999 319; 1755.58 319 |
| AVG_MDCR_PYMT_AMT | amount | 54.4K | 52.7K | 26231.37 319; 10233.9799999999 319; 1398.75 319; 2444.75 319 |
| OUTLIER_SRVCS | other | 174 | 68.7K | 0 44.8K; 12 224; 11 212; 13 189 |
| AVG_MDCR_OUTLIER_AMT | amount | 2.6K | 68.7K | 0 44.8K; 15146.0487818181 14; 4909.91010588235 14; 15682.2051749999 14 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 12:22:30.034 116.2K |
| _SOURCE_RUN_ID | audit id | 116.4K | 0 | 4c51bcf2-dd36-4c67-9526-a 581; 5a355436-47a5-4e17-82a9-3 581; a52b7f7e-fff8-40a7-8f2e-1 581; 89ca0485-1791-4bda-9738-e 581 |
