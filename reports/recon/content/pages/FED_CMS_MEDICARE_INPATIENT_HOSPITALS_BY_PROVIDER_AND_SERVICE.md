# FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE

rows 145.9K  columns 17  scan 5.7s

roles: amount 4, audit 2, category 1, date 1, id 1, other 4, state 1, who 5

## when

_INGESTED_AT
  2026    145.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RNDRNG_PRVDR_RUCA | 145.9K | 1 | 1 | 7 | 99 | 254.7K |
| AVG_SUBMTD_CVRD_CHRG | 145.9K | 2.1K | 61.6K | 561.8K | 7.20M | 14.06B |
| AVG_TOT_PYMT_AMT | 145.9K | 1.8K | 13.2K | 91.4K | 1.44M | 2.79B |
| AVG_MDCR_PYMT_AMT | 145.9K | 386.80 | 10.9K | 76.4K | 1.44M | 2.30B |

## who

RNDRNG_PRVDR_ORG_NAME by rows
       423  Methodist Hospital
       387  Adventhealth Orlando
       373  New York-Presbyterian Hospital
       356  Nyu Langone Hospitals
       309  Memorial Medical Center
       309  Mayo Clinic Hospital Rochester
       298  Massachusetts General Hospital
       287  Sarasota Memorial Hospital
       286  Saint Francis Medical Center
       284  Christianacare
       279  Stanford Health Care
       277  Barnes Jewish Hospital
       272  Lehigh Valley Hospital
       271  Cedars-Sinai Medical Center
       270  Brigham And Women's Hospital
       266  St Lukes Hospital
       257  Vanderbilt University Medical Center
       257  Huntington Hospital
       255  Stony Brook University Hospital
       255  Morristown Medical Center

RNDRNG_PRVDR_ORG_NAME by dollars
      15.14M      373 rows  New York-Presbyterian Hospital
      14.92M      279 rows  Stanford Health Care
      13.66M      356 rows  Nyu Langone Hospitals
      13.44M      231 rows  Ucsf Medical Center
      13.15M      309 rows  Mayo Clinic Hospital Rochester
      11.65M      242 rows  Johns Hopkins Hospital, The
      10.95M      298 rows  Massachusetts General Hospital
      10.70M      164 rows  University Of Maryland Medical Center
      10.58M      271 rows  Cedars-Sinai Medical Center
      10.12M      219 rows  Mount Sinai Hospital
      10.09M      270 rows  Brigham And Women's Hospital
       9.89M      277 rows  Barnes Jewish Hospital
       9.66M      211 rows  Hospital Of Univ Of Pennsylvania
       9.49M      199 rows  University Of California Davis Medical Center
       8.98M      185 rows  Uc San Diego Health Hillcrest - Hillcrest Med Ctr
       8.70M      387 rows  Adventhealth Orlando
       8.58M      226 rows  Northwestern Memorial Hospital
       8.56M      257 rows  Vanderbilt University Medical Center
       8.55M      247 rows  Cleveland Clinic
       8.51M      132 rows  Ronald Reagan Ucla Medical Center

RNDRNG_PRVDR_CCN by rows
       387  100007
       373  330101
       356  330214
       309  240010
       298  220071
       287  100087
       284  080001
       279  450388
       279  050441
       277  260032
       272  390133
       271  050625
       270  220110
       257  440039
       255  330393
       255  310015
       254  180088
       252  170040
       251  340030
       249  100088

RNDRNG_PRVDR_CCN by dollars
      15.14M      373 rows  330101
      14.92M      279 rows  050441
      13.66M      356 rows  330214
      13.44M      231 rows  050454
      13.15M      309 rows  240010
      11.65M      242 rows  210009
      10.95M      298 rows  220071
      10.70M      164 rows  210002
      10.58M      271 rows  050625
      10.12M      219 rows  330024
      10.09M      270 rows  220110
       9.89M      277 rows  260032
       9.66M      211 rows  390111
       9.49M      199 rows  050599
       8.98M      185 rows  050025
       8.70M      387 rows  100007
       8.58M      226 rows  140281
       8.56M      257 rows  440039
       8.55M      247 rows  360180
       8.51M      132 rows  050262

RNDRNG_PRVDR_ST by rows
       387  601 E Rollins St
       379  1 Medical Center Drive
       373  525 East 68th Street
       356  550 First Avenue
       309  1216 Second Street Southwest
       298  55 Fruit Street
       287  1700 S Tamiami Trl
       284  4755 Ogletown-Stanton Road
       279  7700 Floyd Curl Dr
       279  300 Pasteur Drive
       277  One Barnes-Jewish Hospital Plaza
       272  1200 South Cedar Crest Boulevard
       271  8700 Beverly Blvd
       270  75 Francis Street
       257  1211 Medical Center Drive
       255  Health Sciences Center Suny
       255  100 Madison Ave
       254  200 East Chestnut Street
       252  4000 Cambridge Street
       251  2301  Erwin Rd

RNDRNG_PRVDR_ST by dollars
      15.14M      373 rows  525 East 68th Street
      14.92M      279 rows  300 Pasteur Drive
      13.66M      356 rows  550 First Avenue
      13.44M      231 rows  505 Parnassus Ave, Box 0296
      13.15M      309 rows  1216 Second Street Southwest
      11.65M      242 rows  600 North  Wolfe Street
      10.95M      298 rows  55 Fruit Street
      10.70M      164 rows  22 South  Greene Street
      10.58M      271 rows  8700 Beverly Blvd
      10.48M      379 rows  1 Medical Center Drive
      10.12M      219 rows  One Gustave L Levy Place
      10.09M      270 rows  75 Francis Street
       9.89M      277 rows  One Barnes-Jewish Hospital Plaza
       9.66M      211 rows  34th & Spruce Sts
       9.49M      199 rows  2315 Stockton Boulevard
       8.98M      185 rows  200 West Arbor Drive
       8.70M      387 rows  601 E Rollins St
       8.58M      226 rows  251 E Huron St
       8.56M      257 rows  1211 Medical Center Drive
       8.55M      247 rows  9500 Euclid Avenue

DRG_DESC by rows
      2.7K  SEPTICEMIA OR SEVERE SEPSIS WITHOUT MV >96 HOURS WITH MCC
      2.6K  HEART FAILURE AND SHOCK WITH MCC
      2.4K  SIMPLE PNEUMONIA AND PLEURISY WITH MCC
      2.3K  RESPIRATORY INFECTIONS AND INFLAMMATIONS WITH MCC
      2.2K  SEPTICEMIA OR SEVERE SEPSIS WITHOUT MV >96 HOURS WITHOUT MCC
      2.1K  KIDNEY AND URINARY TRACT INFECTIONS WITHOUT MCC
      2.1K  PULMONARY EDEMA AND RESPIRATORY FAILURE
      2.0K  RENAL FAILURE WITH CC
      2.0K  ESOPHAGITIS, GASTROENTERITIS AND MISCELLANEOUS DIGESTIVE DISORDERS WIT
      1.9K  KIDNEY AND URINARY TRACT INFECTIONS WITH MCC
      1.9K  MISCELLANEOUS DISORDERS OF NUTRITION, METABOLISM, FLUIDS AND ELECTROLY
      1.9K  RENAL FAILURE WITH MCC
      1.9K  MISCELLANEOUS DISORDERS OF NUTRITION, METABOLISM, FLUIDS AND ELECTROLY
      1.8K  ACUTE MYOCARDIAL INFARCTION, DISCHARGED ALIVE WITH MCC
      1.8K  OTHER KIDNEY AND URINARY TRACT DIAGNOSES WITH MCC
      1.8K  GASTROINTESTINAL HEMORRHAGE WITH CC
      1.8K  INFECTIOUS AND PARASITIC DISEASES WITH O.R. PROCEDURES WITH MCC
      1.7K  INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION WITH CC OR TPA IN 24 HO
      1.7K  HIP AND FEMUR PROCEDURES EXCEPT MAJOR JOINT WITH CC
      1.7K  CELLULITIS WITHOUT MCC

DRG_DESC by dollars
      79.95M     1.8K rows  INFECTIOUS AND PARASITIC DISEASES WITH O.R. PROCEDURES WITH 
      60.08M      272 rows  ECMO OR TRACHEOSTOMY WITH MV >96 HOURS OR PRINCIPAL DIAGNOSI
      55.68M      878 rows  SEPTICEMIA OR SEVERE SEPSIS WITH MV >96 HOURS
      47.36M     2.7K rows  SEPTICEMIA OR SEVERE SEPSIS WITHOUT MV >96 HOURS WITH MCC
      43.47M      653 rows  CARDIAC VALVE AND OTHER MAJOR CARDIOTHORACIC PROCEDURES WITH
      41.69M      988 rows  MAJOR SMALL AND LARGE BOWEL PROCEDURES WITH MCC
      34.66M     2.3K rows  RESPIRATORY INFECTIONS AND INFLAMMATIONS WITH MCC
      31.25M     2.6K rows  HEART FAILURE AND SHOCK WITH MCC
      31.05M     1.7K rows  HIP AND FEMUR PROCEDURES EXCEPT MAJOR JOINT WITH CC
      30.51M      680 rows  EXTENSIVE O.R. PROCEDURES UNRELATED TO PRINCIPAL DIAGNOSIS W
      30.09M     1.1K rows  PERCUTANEOUS CARDIOVASCULAR PROCEDURES WITH INTRALUMINAL DEV
      29.77M      533 rows  ENDOVASCULAR CARDIAC VALVE REPLACEMENT AND SUPPLEMENT PROCED
      29.69M     2.4K rows  SIMPLE PNEUMONIA AND PLEURISY WITH MCC
      29.67M       87 rows  HEART TRANSPLANT OR IMPLANT OF HEART ASSIST SYSTEM WITH MCC
      29.15M      690 rows  ENDOVASCULAR CARDIAC VALVE REPLACEMENT AND SUPPLEMENT PROCED
      28.50M      212 rows  TRACHEOSTOMY WITH MV >96 HOURS OR PRINCIPAL DIAGNOSIS EXCEPT
      28.12M      491 rows  COMBINED ANTERIOR AND POSTERIOR SPINAL FUSION WITH CC
      27.00M      541 rows  OTHER MAJOR CARDIOVASCULAR PROCEDURES WITH MCC
      27.00M     1.5K rows  INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION WITH MCC
      26.69M     1.8K rows  ACUTE MYOCARDIAL INFARCTION, DISCHARGED ALIVE WITH MCC

## who x when

RNDRNG_PRVDR_ORG_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = AVG_TOT_PYMT_AMT
  Adventhealth Orlando                      2026:8.70M
  Barnes Jewish Hospital                    2026:9.89M
  Brigham And Women's Hospital              2026:10.09M
  Cedars-Sinai Medical Center               2026:10.58M
  Christianacare                            2026:6.34M
  Cleveland Clinic                          2026:8.55M
  Hospital Of Univ Of Pennsylvania          2026:9.66M
  Huntington Hospital                       2026:4.79M
  Johns Hopkins Hospital, The               2026:11.65M
  Lehigh Valley Hospital                    2026:5.78M
  Massachusetts General Hospital            2026:10.95M
  Mayo Clinic Hospital Rochester            2026:13.15M
  Memorial Medical Center                   2026:5.83M
  Methodist Hospital                        2026:7.55M
  Morristown Medical Center                 2026:6.86M
  Mount Sinai Hospital                      2026:10.12M
  New York-Presbyterian Hospital            2026:15.14M
  Northwestern Memorial Hospital            2026:8.58M
  Nyu Langone Hospitals                     2026:13.66M
  Ronald Reagan Ucla Medical Center         2026:8.51M
  Saint Francis Medical Center              2026:5.99M
  Sarasota Memorial Hospital                2026:4.54M
  St Lukes Hospital                         2026:3.61M
  Stanford Health Care                      2026:14.92M
  Stony Brook University Hospital           2026:7.67M
  Uc San Diego Health Hillcrest - Hillcres  2026:8.98M
  Ucsf Medical Center                       2026:13.44M
  University Of California Davis Medical C  2026:9.49M
  University Of Maryland Medical Center     2026:10.70M
  Vanderbilt University Medical Center      2026:8.56M

RNDRNG_PRVDR_CCN by _INGESTED_AT  LOAD STAMP, not an event date, dollars = AVG_TOT_PYMT_AMT
  050025                                    2026:8.98M
  050262                                    2026:8.51M
  050441                                    2026:14.92M
  050454                                    2026:13.44M
  050599                                    2026:9.49M
  050625                                    2026:10.58M
  080001                                    2026:6.34M
  100007                                    2026:8.70M
  100087                                    2026:4.54M
  100088                                    2026:4.66M
  140281                                    2026:8.58M
  170040                                    2026:6.57M
  180088                                    2026:4.49M
  210002                                    2026:10.70M
  210009                                    2026:11.65M
  220071                                    2026:10.95M
  220110                                    2026:10.09M
  240010                                    2026:13.15M
  260032                                    2026:9.89M
  310015                                    2026:6.86M
  330024                                    2026:10.12M
  330101                                    2026:15.14M
  330214                                    2026:13.66M
  330393                                    2026:7.67M
  340030                                    2026:8.14M
  360180                                    2026:8.55M
  390111                                    2026:9.66M
  390133                                    2026:5.78M
  440039                                    2026:8.56M
  450388                                    2026:5.36M

## where

RNDRNG_PRVDR_STATE_ABRVTN: CA 13.3K, FL 12.0K, TX 10.0K, NY 8.3K, PA 6.9K, IL 6.4K, OH 5.5K, NJ 4.8K, MA 4.5K, NC 4.5K, VA 4.3K, MI 4.1K

## what

RNDRNG_PRVDR_RUCA_DESC: Metropolitan area core: primar 87%, Micropolitan area core: primar 7%, Secondary flow 30% to <50% to  2%, Metropolitan area high commuti 2%, Small town core: primary flow  1%, Secondary flow 30% to <50% to  0%, Micropolitan high commuting: p 0%, Unknown 0%, Rural areas: primary flow to a 0%, Secondary flow 30% to <50% to  0%, Small town high commuting: pri 0%, Metropolitan area low commutin 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RNDRNG_PRVDR_CCN | who | 2.9K | 0 | 520098 887; 450388 868; 490063 860; 520177 857 |
| RNDRNG_PRVDR_ORG_NAME | who | 2.8K | 0 | University Of Wi  Hospita 888; Methodist Hospital 868; Inova Fairfax Hospital 860; Froedtert Memorial Luther 858 |
| RNDRNG_PRVDR_CITY | who | 1.7K | 0 | New York 1.7K; Houston 1.5K; Philadelphia 1.4K; Baltimore 1.3K |
| RNDRNG_PRVDR_ST | who | 2.8K | 0 | 600 Highland Avenue 887; 7700 Floyd Curl Dr 868; 3300 Gallows Road 860; 9200 W Wisconsin Ave 857 |
| RNDRNG_PRVDR_STATE_FIPS | other | 51 | 0 | 06 13.3K; 12 12.0K; 48 10.0K; 36 8.3K |
| RNDRNG_PRVDR_ZIP5 | other | 2.8K | 0 | 78229 1.1K; 77030 1.1K; 76104 967; 53715 888 |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 51 | 0 | CA 13.3K; FL 12.0K; TX 10.0K; NY 8.3K |
| RNDRNG_PRVDR_RUCA | amount | 19 | 0 | 1 127.0K; 4 10.3K; 1.1 2.4K; 2 2.2K |
| RNDRNG_PRVDR_RUCA_DESC | category | 15 | 0 | Metropolitan area core: p 127.0K; Micropolitan area core: p 10.3K; Secondary flow 30% to <50 2.4K; Metropolitan area high co 2.2K |
| DRG_CD | other | 538 | 0 | 871 2.7K; 291 2.6K; 193 2.4K; 177 2.3K |
| DRG_DESC | who | 531 | 0 | SEPTICEMIA OR SEVERE SEPS 2.7K; HEART FAILURE AND SHOCK W 2.6K; SIMPLE PNEUMONIA AND PLEU 2.4K; RESPIRATORY INFECTIONS AN 2.3K |
| TOT_DSCHRGS | other | 657 | 0 | 11 12.0K; 12 10.5K; 13 9.2K; 14 8.1K |
| AVG_SUBMTD_CVRD_CHRG | amount | 147.6K | 0 | 120397.45455 730; 56832.1 730; 44871.153846 730; 64812.782609 730 |
| AVG_TOT_PYMT_AMT | amount | 141.8K | 0 | 12540.909091 730; 13823.966667 730; 6666.6923077 730; 13463.681159 730 |
| AVG_MDCR_PYMT_AMT | amount | 144.5K | 0 | 8500.5454545 730; 10110.666667 730; 5152.2307692 730; 11372.26087 730 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 12:22:20.271 145.9K |
| _SOURCE_RUN_ID | audit id | 146.4K | 0 | 06844fb3-a9c8-45eb-a8a5-d 730; bae9693d-68fd-44c7-a833-a 730; f687c26a-5bc9-46f8-828a-5 730; 6bd897b0-ef69-4fa4-9a30-2 730 |
