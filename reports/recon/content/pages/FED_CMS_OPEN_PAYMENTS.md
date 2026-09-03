# FED_CMS_OPEN_PAYMENTS

rows 15.39M  columns 94  scan 25.6s

roles: amount 1, audit 2, category 29, date 2, empty 4, id 1, other 6, state 8, who 41

## when

DATE_OF_PAYMENT
  2002        73  
  2024    15.38M  ##############################

PAYMENT_PUBLICATION_DATE
  2026    15.39M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS | 15.39M | 0.01 | 20.37 | 3.1K | 91.08M | 3.31B |

## who

COVERED_RECIPIENT_LAST_NAME by rows
    106.8K  PATEL
     74.0K  SMITH
     56.5K  LEE
     52.5K  JOHNSON
     49.9K  NGUYEN
     45.6K  MILLER
     44.5K  BROWN
     41.8K  JONES
     40.2K  WILLIAMS
     38.1K  DAVIS
     37.8K  KIM
     37.8K  SHAH
     28.4K  THOMAS
     27.5K  ANDERSON
     27.4K  SINGH
     25.8K  WILSON
     25.8K  KHAN
     24.5K  CHEN
     23.7K  MOORE
     23.6K  MARTIN

COVERED_RECIPIENT_LAST_NAME by dollars
      91.09M       14 rows  GOODIS
      26.75M       81 rows  MEDOFF
      25.32M     2.4K rows  GOYAL
      17.81M      720 rows  OSORIO
      17.41M      556 rows  BURKHART
      16.74M     2.8K rows  FOLEY
      13.60M   106.8K rows  PATEL
      13.07M    18.4K rows  JACKSON
      10.72M    74.0K rows  SMITH
       9.62M     8.4K rows  SCHWARTZ
       7.54M    56.5K rows  LEE
       7.49M      219 rows  KUBIAK
       7.49M      529 rows  BINDER
       7.42M     2.2K rows  MAXWELL
       7.33M      157 rows  FRANKLE
       7.29M    37.8K rows  SHAH
       6.85M       23 rows  ELATTRACHE
       6.82M    16.5K rows  COHEN
       6.78M    37.8K rows  KIM
       6.35M    44.5K rows  BROWN

COVERED_RECIPIENT_FIRST_NAME by rows
    242.8K  MICHAEL
    208.7K  DAVID
    184.8K  JOHN
    151.6K  ROBERT
    148.4K  JENNIFER
    133.0K  JAMES
    110.0K  CHRISTOPHER
    105.2K  DANIEL
    103.7K  WILLIAM
    101.8K  MATTHEW
    100.1K  MARK
     91.2K  JESSICA
     90.3K  JOSEPH
     86.4K  ANDREW
     84.0K  SARAH
     81.8K  RICHARD
     81.5K  JEFFREY
     78.5K  THOMAS
     76.9K  BRIAN
     75.8K  STEVEN

COVERED_RECIPIENT_FIRST_NAME by dollars
     102.80M    55.2K rows  CHARLES
      72.91M   151.6K rows  ROBERT
      59.30M   242.8K rows  MICHAEL
      55.08M   184.8K rows  JOHN
      48.22M   208.7K rows  DAVID
      36.28M   103.7K rows  WILLIAM
      35.71M    58.3K rows  STEPHEN
      35.34M   100.1K rows  MARK
      31.28M   105.2K rows  DANIEL
      28.99M   133.0K rows  JAMES
      26.02M    78.5K rows  THOMAS
      25.83M     2.7K rows  NITIN
      25.42M    66.0K rows  PAUL
      25.37M    57.5K rows  KEVIN
      23.27M   110.0K rows  CHRISTOPHER
      22.57M    81.8K rows  RICHARD
      21.95M    47.0K rows  PETER
      21.40M    75.8K rows  STEVEN
      21.34M    81.5K rows  JEFFREY
      20.16M    90.3K rows  JOSEPH

COVERED_RECIPIENT_MIDDLE_NAME by rows
    357.7K  M
    343.2K  A
    272.7K  L
    218.4K  J
    175.3K  R
    163.0K  S
    162.3K  E
    156.7K  D
    144.7K  C
    112.5K  MARIE
    108.2K  K
    100.2K  B
     83.3K  N
     80.9K  P
     75.8K  ANN
     74.1K  G
     73.2K  T
     72.5K  H
     65.5K  W
     63.4K  LYNN

COVERED_RECIPIENT_MIDDLE_NAME by dollars
      43.28M   343.2K rows  A
      37.36M   357.7K rows  M
      34.59M   218.4K rows  J
      27.40M   163.0K rows  S
      23.70M   272.7K rows  L
      23.08M   156.7K rows  D
      19.92M   162.3K rows  E
      19.28M   175.3K rows  R
      16.90M   144.7K rows  C
      13.97M   108.2K rows  K
      13.89M   100.2K rows  B
      13.17M    80.9K rows  P
      12.85M    65.5K rows  W
      11.31M    73.2K rows  T
      10.40M    74.1K rows  G
       9.75M    72.5K rows  H
       7.63M    54.6K rows  F
       7.53M    83.3K rows  N
       7.30M    34.9K rows  MICHAEL
       6.71M   112.5K rows  MARIE

NAME_OF_THIRD_PARTY_ENTITY_RECEIVING_PAYMENT_OR_TRANSFER_OF_VALUE by rows
      1.2K  UATP UNITED
       750  Ashfield Healthcare, LLC
       568  I RIDE TRANSPORTATION
       550  Wink Productions
       509  EXPERT OPINION MD
       341  HCA Group
       238  THE GERCH GROUP LLC
       176  BRASS LANTERN CONSULTING LLC
       168  RESONANT RESPIRATORY LLC
       168  Vector Health Inc
       165  Purdie Pascoe
       158  ETC Consultants Inc
       154  Facilitation of International Dermatology Educatio
       154  Rebecca Roma Evaluation and Consulting LLC
       153  ALILA MAREA BEACH RESORT
       150  PARISER DERMATOLOGY ASSOC
       148  Edge Aesthetics, LLC
       145  Egencia LLC
       144  PNW Dermatology Education LLC
       144  Jva Medcl

NAME_OF_THIRD_PARTY_ENTITY_RECEIVING_PAYMENT_OR_TRANSFER_OF_VALUE by dollars
      26.75M        1 rows  Amp'd International
      17.46M        5 rows  Flint hill
      17.33M        3 rows  BURKHART RESOURCE LIMITED
       7.42M        4 rows  Miotox, LLC
       5.68M       63 rows  MAYO FOUNDATION
       4.84M       31 rows  ANTHONY A ROMEO, M.D, S.C
       4.04M       28 rows  Lgl Spine Llc
       3.32M       17 rows  DSD#1 LLC
       3.20M        1 rows  The Poole Family Trust
       3.08M        1 rows  Previse Medical
       2.81M       15 rows  JEFFREY R. DUGAS, MD PC
       2.76M        2 rows  Clph Llc
       2.34M       77 rows  UPP Pathology
       2.15M        7 rows  SMS Trust
       2.12M        7 rows  PKC NO 1 LLC
       2.09M        7 rows  THOMAS KEITH FEHRING SPOUSAL LIFETI ME ACCESS TRUS
       2.04M       41 rows  KYLEX VENTURES LLC
       2.02M       29 rows  PRIMO MC LLC
       2.01M       14 rows  SANDERS FAMILY LIMITED PARTNERSHIP
       1.77M        4 rows  SURGIVISION CONSULTANTS INC

## who x when

COVERED_RECIPIENT_LAST_NAME by DATE_OF_PAYMENT, dollars = TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS
  ANDERSON                                  2024:5.00M
  BINDER                                    2024:7.49M
  BROWN                                     2024:6.35M
  BURKHART                                  2024:17.41M
  CHEN                                      2024:3.74M
  DAVIS                                     2024:3.77M
  FOLEY                                     2024:16.74M
  GOODIS                                    2024:91.09M
  GOYAL                                     2024:25.32M
  JACKSON                                   2024:13.07M
  JOHNSON                                   2024:5.40M
  JONES                                     2024:4.58M
  KHAN                                      2024:2.78M
  KIM                                       2024:6.78M
  KUBIAK                                    2024:7.49M
  LEE                                       2024:7.54M
  MARTIN                                    2024:2.89M
  MEDOFF                                    2024:26.75M
  MILLER                                    2024:5.58M
  MOORE                                     2024:2.17M
  NGUYEN                                    2024:5.58M
  OSORIO                                    2024:17.81M
  PATEL                                     2024:13.60M
  SCHWARTZ                                  2024:9.62M
  SHAH                                      2024:7.29M
  SINGH                                     2024:5.61M
  SMITH                                     2024:10.72M
  THOMAS                                    2024:2.93M
  WILLIAMS                                  2024:3.91M
  WILSON                                    2024:1.75M

COVERED_RECIPIENT_FIRST_NAME by DATE_OF_PAYMENT, dollars = TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS
  ANDREW                                    2002:411.94 2024:17.69M
  BRIAN                                     2024:18.94M
  CHARLES                                   2024:102.80M
  CHRISTOPHER                               2024:23.27M
  DANIEL                                    2024:31.28M
  DAVID                                     2024:48.22M
  JAMES                                     2024:28.99M
  JEFFREY                                   2024:21.34M
  JENNIFER                                  2024:13.10M
  JESSICA                                   2024:5.59M
  JOHN                                      2002:6.8K 2024:55.08M
  JOSEPH                                    2024:20.16M
  KEVIN                                     2024:25.37M
  MARK                                      2024:35.34M
  MATTHEW                                   2024:18.47M
  MICHAEL                                   2024:59.30M
  NITIN                                     2024:25.83M
  PAUL                                      2024:25.42M
  PETER                                     2024:21.95M
  RICHARD                                   2024:22.57M
  ROBERT                                    2024:72.91M
  SARAH                                     2024:5.47M
  STEPHEN                                   2024:35.71M
  STEVEN                                    2024:21.40M
  THOMAS                                    2024:26.02M
  WILLIAM                                   2024:36.28M

## where

RECIPIENT_STATE: TX 1.45M, CA 1.37M, FL 1.35M, NY 1.03M, PA 666.0K, OH 602.9K, GA 591.6K, NC 534.8K, IL 523.0K, NJ 515.9K, TN 499.8K, MI 474.6K

COVERED_RECIPIENT_LICENSE_STATE_CODE1: CA 1.53M, FL 1.43M, TX 1.22M, NY 945.6K, GA 608.3K, IL 598.5K, PA 586.1K, OH 563.7K, NJ 553.7K, NC 535.9K, MI 490.5K, AZ 441.4K

COVERED_RECIPIENT_LICENSE_STATE_CODE2: CA 25.9K, TX 13.2K, FL 12.4K, NY 12.1K, OH 10.5K, PA 8.3K, NC 7.1K, TN 6.9K, IN 6.7K, IL 6.3K, MD 5.8K

COVERED_RECIPIENT_LICENSE_STATE_CODE3: TX 4.8K, CA 3.8K, PA 3.7K, NY 3.7K, OH 3.6K, TN 2.5K, VA 2.4K, NC 2.3K, FL 2.1K, MO 2.1K, IL 2.0K

COVERED_RECIPIENT_LICENSE_STATE_CODE4: TX 1.6K, CA 1.4K, VA 1.3K, OH 1.2K, PA 1.1K, NY 918, WA 801, WI 760, TN 756, NC 741, MO 670

COVERED_RECIPIENT_LICENSE_STATE_CODE5: CA 673, TX 479, VA 443, PA 415, WI 342, OH 341, NY 340, IL 314, TN 281, WA 265, SC 253

APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE: NJ 3.22M, IL 2.38M, CA 1.88M, MA 1.66M, PA 1.05M, NY 895.3K, DE 719.4K, IN 624.1K, MN 524.9K, MD 292.8K, TX 234.3K, FL 222.1K

STATE_OF_TRAVEL: TX 76.2K, CA 67.5K, FL 66.2K, IL 33.0K, GA 26.8K, MN 22.0K, CO 21.5K, NY 20.2K, TN 18.6K, AZ 18.1K, NV 16.7K

## what

CHANGE_TYPE: UNCHANGED 99%, CHANGED 1%, ADD 0%

COVERED_RECIPIENT_TYPE: Covered Recipient Physician 64%, Covered Recipient Non-Physicia 36%, Covered Recipient Teaching Hos 0%

RECIPIENT_COUNTRY: United States 100%, United States Minor Outlying I 0%, Canada 0%, Japan 0%, Great Britain (UK) 0%, United Arab Emirates 0%, Argentina 0%, Germany 0%, Lebanon 0%, Italy 0%, Pakistan 0%, Israel 0%

COVERED_RECIPIENT_PRIMARY_TYPE_1: Medical Doctor 53%, Nurse Practitioner 23%, Physician Assistant 12%, Doctor of Osteopathy 6%, Doctor of Dentistry 2%, Doctor of Optometry 2%, Doctor of Podiatric Medicine 1%, Certified Registered Nurse Ane 0%, Clinical Nurse Specialist 0%, Certified Nurse-Midwife 0%, Chiropractor 0%

COVERED_RECIPIENT_PRIMARY_TYPE_2: Nurse Practitioner 48%, Clinical Nurse Specialist 18%, Certified Registered Nurse Ane 15%, Certified Nurse-Midwife 15%, Physician Assistant 4%, Anesthesiologist Assistant 0%

COVERED_RECIPIENT_PRIMARY_TYPE_3: Clinical Nurse Specialist 100%

COVERED_RECIPIENT_PRIMARY_TYPE_4: Certified Registered Nurse Ane 100%

COVERED_RECIPIENT_PRIMARY_TYPE_5: Certified Nurse-Midwife 100%

COVERED_RECIPIENT_PRIMARY_TYPE_6: Anesthesiologist Assistant 100%

COVERED_RECIPIENT_SPECIALTY_2: Physician Assistants & Advance 40%, Nursing Service Providers|Regi 20%, Physician Assistants & Advance 20%, Physician Assistants & Advance 20%

APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_COUNTRY: United States 100%, Great Britain (UK) 0%, Iceland 0%, Switzerland 0%, Canada 0%, Germany 0%, Denmark 0%, Ireland 0%, Japan 0%, Israel 0%, Belgium 0%, United Arab Emirates 0%

FORM_OF_PAYMENT_OR_TRANSFER_OF_VALUE: In-kind items and services 87%, Cash or cash equivalent 13%, Stock, stock option, or any ot 0%, Dividend, profit or other retu 0%, Stock option 0%, Stock 0%

NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE: Food and Beverage 92%, Travel and Lodging 4%, Compensation for services othe 2%, Consulting Fee 1%, Education 1%, Gift 0%, Long term medical supply or de 0%, Honoraria 0%, Royalty or License 0%, Compensation for serving as fa 0%, Debt forgiveness 0%, Space rental or facility fees  0%

PHYSICIAN_OWNERSHIP_INDICATOR: No 100%, Yes 0%

THIRD_PARTY_PAYMENT_RECIPIENT_INDICATOR: No Third Party Payment 99%, Entity 1%, Individual 0%

CHARITY_INDICATOR: No 100%, Yes 0%

THIRD_PARTY_EQUALS_COVERED_RECIPIENT_INDICATOR: No 78%, Yes 22%

DISPUTE_STATUS_FOR_PUBLICATION: No 100%, Yes 0%

RELATED_PRODUCT_INDICATOR: Yes 94%, No 6%

COVERED_OR_NONCOVERED_INDICATOR_1: Covered 97%, Non-Covered 3%

INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1: Drug 60%, Device 22%, Biological 17%, Medical Supply 1%

COVERED_OR_NONCOVERED_INDICATOR_2: Covered 97%, Non-Covered 3%

INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_2: Drug 66%, Biological 21%, Device 13%, Medical Supply 0%

COVERED_OR_NONCOVERED_INDICATOR_3: Covered 96%, Non-Covered 4%

INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_3: Drug 44%, Device 28%, Biological 28%, Medical Supply 0%

COVERED_OR_NONCOVERED_INDICATOR_4: Covered 97%, Non-Covered 3%

INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_4: Device 44%, Drug 33%, Biological 22%, Medical Supply 0%

COVERED_OR_NONCOVERED_INDICATOR_5: Covered 97%, Non-Covered 3%

INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_5: Device 48%, Drug 39%, Biological 12%, Medical Supply 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CHANGE_TYPE | category | 3 | 0 | UNCHANGED 15.29M; CHANGED 97.3K; ADD 1.3K |
| COVERED_RECIPIENT_TYPE | category | 3 | 0 | Covered Recipient Physici 9.88M; Covered Recipient Non-Phy 5.47M; Covered Recipient Teachin 34.4K |
| CCN | who | 1.3K | 15.35M | 090004 861; 390111 670; 220071 610; 330393 597 |
| TEACHING_HOSPITAL_ID | other | 1.2K | 15.35M | 14335 861; 15218 670; 14674 610; 15017 597 |
| TEACHING_HOSPITAL_NAME | who | 2.1K | 15.35M | Georgetown University Hos 862; Stony Brook University Ho 598; Hospital Of The Univ Of P 559; University Of Washington  425 |
| COVERED_RECIPIENT_PROFILE_ID | who | 966.6K | 34.4K | 119282 20.0K; 213832 20.0K; 859782 10.1K; 50597 10.1K |
| NPI | other | 974.6K | 48.1K | 1629175195 20.0K; 1720170053 20.0K; 1447541206 10.1K; 1114174729 10.1K |
| COVERED_RECIPIENT_FIRST_NAME | who | 99.8K | 34.4K | MICHAEL 243.4K; DAVID 209.8K; JOHN 185.9K; ROBERT 153.1K |
| COVERED_RECIPIENT_MIDDLE_NAME | who | 75.9K | 9.20M | M 357.7K; A 343.2K; L 272.7K; J 218.4K |
| COVERED_RECIPIENT_LAST_NAME | who | 292.8K | 34.4K | PATEL 112.2K; SMITH 78.1K; NGUYEN 77.6K; LEE 59.2K |
| COVERED_RECIPIENT_NAME_SUFFIX | who | 380 | 15.25M | JR. 36.0K; JR 30.5K; III 26.9K; II 15.0K |
| RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE1 | who | 746.7K | 0 | 100 E LANCASTER AVE 28.9K; 1515 HOLCOMBE BLVD 28.1K; 300 PASTEUR DR 28.0K; 3400 SPRUCE ST 19.9K |
| RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE2 | who | 74.1K | 12.38M | SUITE 200 86.8K; SUITE 100 74.9K; STE 100 55.2K; STE 200 53.8K |
| RECIPIENT_CITY | who | 22.8K | 0 | HOUSTON 188.6K; NEW YORK 182.2K; SAN ANTONIO 111.4K; DALLAS 109.1K |
| RECIPIENT_STATE | state | 60 | 464 | TX 1.45M; CA 1.37M; FL 1.35M; NY 1.03M |
| RECIPIENT_ZIP_CODE | who | 268.9K | 464 | 77030 59.9K; 10021 39.0K; 32308 30.0K; 32207 30.0K |
| RECIPIENT_COUNTRY | category | 33 | 0 | United States 15.38M; United States Minor Outly 123; Canada 110; Japan 44 |
| RECIPIENT_PROVINCE | who | 92 | 15.38M | ONTARIO 53; MD 22; CAPITAL FEDERAL 17; PUERTO RICO 16 |
| RECIPIENT_POSTAL_CODE | who | 165 | 15.38M | 20817 22; M3B 20; L2H0K4 15; W1G 7LA 14 |
| COVERED_RECIPIENT_PRIMARY_TYPE_1 | category | 13 | 34.4K | Medical Doctor 8.15M; Nurse Practitioner 3.56M; Physician Assistant 1.80M; Doctor of Osteopathy 958.4K |
| COVERED_RECIPIENT_PRIMARY_TYPE_2 | category | 7 | 15.38M | Nurse Practitioner 593; Clinical Nurse Specialist 220; Certified Registered Nurs 191; Certified Nurse-Midwife 180 |
| COVERED_RECIPIENT_PRIMARY_TYPE_3 | category | 2 | 15.38M | Clinical Nurse Specialist 499 |
| COVERED_RECIPIENT_PRIMARY_TYPE_4 | category | 2 | 15.38M | Certified Registered Nurs 499 |
| COVERED_RECIPIENT_PRIMARY_TYPE_5 | category | 2 | 15.38M | Certified Nurse-Midwife 499 |
| COVERED_RECIPIENT_PRIMARY_TYPE_6 | category | 2 | 15.38M | Anesthesiologist Assistan 499 |
| COVERED_RECIPIENT_SPECIALTY_1 | who | 386 | 34.4K | Physician Assistants & Ad 1.49M; Physician Assistants & Ad 1.39M; Allopathic & Osteopathic  1.18M; Physician Assistants & Ad 1.12M |
| COVERED_RECIPIENT_SPECIALTY_2 | category | 5 | 15.39M | Physician Assistants & Ad 2; Nursing Service Providers 1; Physician Assistants & Ad 1; Physician Assistants & Ad 1 |
| COVERED_RECIPIENT_SPECIALTY_3 | empty | 1 | 15.39M |  |
| COVERED_RECIPIENT_SPECIALTY_4 | empty | 1 | 15.39M |  |
| COVERED_RECIPIENT_SPECIALTY_5 | empty | 1 | 15.39M |  |
| COVERED_RECIPIENT_SPECIALTY_6 | empty | 1 | 15.39M |  |
| COVERED_RECIPIENT_LICENSE_STATE_CODE1 | state | 60 | 34.4K | CA 1.53M; FL 1.43M; TX 1.22M; NY 945.6K |
| COVERED_RECIPIENT_LICENSE_STATE_CODE2 | state | 56 | 15.19M | CA 25.9K; TX 13.2K; FL 12.4K; NY 12.1K |
| COVERED_RECIPIENT_LICENSE_STATE_CODE3 | state | 57 | 15.32M | TX 4.8K; CA 3.8K; PA 3.7K; NY 3.7K |
| COVERED_RECIPIENT_LICENSE_STATE_CODE4 | state | 56 | 15.36M | TX 1.6K; CA 1.4K; VA 1.3K; OH 1.2K |
| COVERED_RECIPIENT_LICENSE_STATE_CODE5 | state | 54 | 15.38M | CA 673; TX 479; VA 443; PA 415 |
| SUBMITTING_APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_NAME | who | 1.8K | 0 | ABBVIE INC. 1.72M; AstraZeneca Pharmaceutica 658.1K; Pfizer Inc. 581.2K; Eli Lilly and Company 542.4K |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID | who | 1.8K | 0 | 100000000204 1.72M; 100000000146 610.0K; 100000000286 568.3K; 100000000066 534.8K |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME | who | 1.8K | 0 | ABBVIE INC. 1.72M; AstraZeneca Pharmaceutica 610.0K; PFIZER INC. 568.3K; Lilly USA, LLC 534.8K |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | 50 | 66.8K | NJ 3.22M; IL 2.38M; CA 1.88M; MA 1.66M |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_COUNTRY | category | 33 | 0 | United States 15.32M; Great Britain (UK) 32.3K; Iceland 15.4K; Switzerland 4.4K |
| TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS | amount | 129.7K | 0 | 23.70 39.0K; 20.21 38.9K; 17.58 37.9K; 20.00 30.3K |
| DATE_OF_PAYMENT | date | 364 | 0 | 04/24/2024 83.6K; 09/26/2024 83.0K; 11/14/2024 81.5K; 10/23/2024 81.3K |
| NUMBER_OF_PAYMENTS_INCLUDED_IN_TOTAL_AMOUNT | other | 87 | 0 | 1 15.32M; 2 24.6K; 3 7.9K; 4 5.0K |
| FORM_OF_PAYMENT_OR_TRANSFER_OF_VALUE | category | 6 | 0 | In-kind items and service 13.33M; Cash or cash equivalent 2.05M; Stock, stock option, or a 310; Dividend, profit or other 186 |
| NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE | category | 16 | 0 | Food and Beverage 14.10M; Travel and Lodging 588.8K; Compensation for services 238.7K; Consulting Fee 185.9K |
| CITY_OF_TRAVEL | who | 10.0K | 14.80M | Dallas 15.5K; Minneapolis 14.2K; Naples 13.3K; ATLANTA 12.8K |
| STATE_OF_TRAVEL | state | 110 | 14.81M | TX 76.2K; CA 67.5K; FL 66.2K; IL 33.0K |
| COUNTRY_OF_TRAVEL | who | 98 | 14.80M | United States 570.8K; Germany 2.0K; Canada 1.7K; Ireland 1.7K |
| PHYSICIAN_OWNERSHIP_INDICATOR | category | 3 | 2.20M | No 13.19M; Yes 3.8K |
| THIRD_PARTY_PAYMENT_RECIPIENT_INDICATOR | category | 3 | 0 | No Third Party Payment 15.25M; Entity 107.5K; Individual 31.2K |
| NAME_OF_THIRD_PARTY_ENTITY_RECEIVING_PAYMENT_OR_TRANSFER_OF_VALUE | who | 14.8K | 15.28M | UATP UNITED 1.2K; Ashfield Healthcare, LLC 761; Wink Productions 606; I RIDE TRANSPORTATION 568 |
| CHARITY_INDICATOR | category | 3 | 11.28M | No 4.10M; Yes 739 |
| THIRD_PARTY_EQUALS_COVERED_RECIPIENT_INDICATOR | category | 3 | 15.25M | No 108.2K; Yes 30.6K |
| CONTEXTUAL_INFORMATION | who | 131.6K | 14.44M | Informational Meal 537.2K; Educational Program 62.5K; Transfer of value related 29.6K; Sponsorship of Attendee ( 28.9K |
| DELAY_IN_PUBLICATION_INDICATOR | other | 1 | 0 | No 15.39M |
| RECORD_ID | id | 15.92M | 0 | 1134630681 10.0K; 1134629283 10.0K; 1134629281 10.0K; 1134629279 10.0K |
| DISPUTE_STATUS_FOR_PUBLICATION | category | 2 | 0 | No 15.38M; Yes 662 |
| RELATED_PRODUCT_INDICATOR | category | 2 | 0 | Yes 14.44M; No 940.8K |
| COVERED_OR_NONCOVERED_INDICATOR_1 | category | 3 | 940.8K | Covered 14.04M; Non-Covered 405.2K |
| INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1 | category | 5 | 1.22M | Drug 8.53M; Device 3.16M; Biological 2.39M; Medical Supply 86.7K |
| PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_1 | who | 2.4K | 1.23M | NEUROSCIENCE 839.8K; Immunology 759.3K; Diabetes 659.3K; IMMUNOLOGY 630.0K |
| NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1 | who | 9.2K | 1.33M | VRAYLAR 395.9K; DUPIXENT 285.3K; RINVOQ 245.1K; JARDIANCE 236.4K |
| ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_1 | who | 1.3K | 4.58M | 61874-115-31 395.8K; 0024-5914-01 282.9K; 0074-2306-30 245.0K; 0002-1506-80 229.8K |
| ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1 | who | 5.2K | 13.07M | 00858637005017 107.8K; 00357599819002 74.3K; 00386270000385 53.4K; 00850291007000 43.8K |
| COVERED_OR_NONCOVERED_INDICATOR_2 | category | 3 | 12.61M | Covered 2.70M; Non-Covered 79.1K |
| INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_2 | category | 5 | 12.68M | Drug 1.79M; Biological 566.3K; Device 347.2K; Medical Supply 6.4K |
| PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_2 | who | 699 | 12.68M | Diabetes 263.7K; NEUROSCIENCE 236.2K; PAIN 180.2K; Obesity 138.0K |
| NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_2 | who | 2.9K | 12.68M | Rybelsus 174.3K; ZAVZPRET 135.8K; ZEPBOUND 132.7K; UBRELVY 128.7K |
| ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_2 | who | 598 | 13.03M | 0169-4303-13 174.2K; 0069-3500-02 135.6K; 0002-2457-80 132.6K; 0023-6501-10 128.7K |
| ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_2 | who | 2.1K | 15.08M | 00850291007154 43.8K; 05694310962391 10.8K; 00816305023701 10.6K; 10381780032434 9.7K |
| COVERED_OR_NONCOVERED_INDICATOR_3 | category | 3 | 14.76M | Covered 597.1K; Non-Covered 25.5K |
| INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_3 | category | 5 | 14.78M | Drug 269.9K; Device 168.2K; Biological 167.5K; Medical Supply 2.7K |
| PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_3 | who | 525 | 14.78M | CNS 73.4K; VACCINES 61.6K; VACCINE 43.1K; IMMUNOLOGY 40.0K |
| NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_3 | who | 2.0K | 14.78M | ARISTADA 56.5K; ABRYSVO 43.4K; GARDASIL 9 33.6K; NURTEC ODT 30.0K |
| ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_3 | who | 402 | 14.95M | 65757-403-03 56.5K; 0069-0344-01 43.3K; 0006-4119-03 33.6K; 72618-3000-2 29.9K |
| ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_3 | who | 1.6K | 15.25M | 05694310960052 10.8K; 10381780032472 9.2K; 00850050080022 6.5K; 00818806020005 6.3K |
| COVERED_OR_NONCOVERED_INDICATOR_4 | category | 3 | 15.11M | Covered 272.4K; Non-Covered 7.3K |
| INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_4 | category | 5 | 15.11M | Device 122.5K; Drug 91.4K; Biological 60.5K; Medical Supply 978 |
| PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_4 | who | 369 | 15.11M | CNS 73.4K; VACCINE 26.2K; Immunology 20.3K; Wound Care 16.1K |
| NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_4 | who | 1.2K | 15.11M | ARISTADA 56.5K; STELARA 20.2K; LYBALVI 17.0K; Kerecis Omega3 Marigen 15.4K |
| ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_4 | who | 198 | 15.23M | 65757-404-03 56.5K; 57894-060-03 20.2K; 65757-651-42 17.0K; 63361-243-10 15.0K |
| ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_4 | who | 1.1K | 15.29M | 05694310961592 10.7K; 10381780000617 9.2K; 00818806020029 6.3K; 05694310962414 4.7K |
| COVERED_OR_NONCOVERED_INDICATOR_5 | category | 3 | 15.22M | Covered 160.9K; Non-Covered 5.4K |
| INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_5 | category | 5 | 15.22M | Device 78.2K; Drug 63.3K; Biological 19.4K; Medical Supply 842 |
| PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_5 | who | 284 | 15.22M | CNS 56.5K; VACCINE 17.6K; Wound Care 16.0K; Recon-Skin and Wound 11.7K |
| NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_5 | who | 723 | 15.22M | LYBALVI 54.1K; Kerecis Omega3 Marigen 15.4K; BIOHORIZONS 9.6K; PRIMATRIX 9.2K |
| ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_5 | who | 116 | 15.30M | 65757-652-42 54.1K; 0006-4681-00 5.3K; 72245-682-10 5.1K; 63361-243-10 3.2K |
| ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_5 | who | 694 | 15.32M | 05694310960151 10.7K; 10381780113744 9.2K; 00818806021583 6.3K; 05694310962391 4.7K |
| PROGRAM_YEAR | other | 1 | 0 | 2024 15.39M |
| PAYMENT_PUBLICATION_DATE | date | 1 | 0 | 01/23/2026 15.39M |
| _INGESTED_AT | audit | 1 | 0 | 1782514748097395 15.39M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 528e772d-620a-48b4-bba9-b 15.39M |
| _SRC_SHA256 | other | 78 | 0 | 8bbda39681eedf961273d87cd 200.0K; f3100c07e18f881841040bf1c 200.0K; 085d85ca50073152ee41a4b73 200.0K; 3894066ddb86930e9dadc688f 200.0K |
