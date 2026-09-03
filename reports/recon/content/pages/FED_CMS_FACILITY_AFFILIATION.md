# FED_CMS_FACILITY_AFFILIATION

rows 2.26M  columns 12  scan 4.0s

roles: audit 2, category 3, other 2, who 5

## who

PROVIDER_LAST_NAME by rows
     15.5K  PATEL
     11.5K  SMITH
      8.6K  LEE
      8.5K  JOHNSON
      7.1K  MILLER
      6.3K  BROWN
      6.1K  SHAH
      5.8K  WILLIAMS
      5.7K  JONES
      5.7K  NGUYEN
      5.5K  KHAN
      5.3K  KIM
      4.7K  DAVIS
      4.7K  ANDERSON
      4.7K  SINGH
      4.5K  THOMAS
      3.8K  WILSON
      3.8K  CHEN
      3.7K  MARTIN
      3.4K  WANG

PROVIDER_FIRST_NAME by rows
     41.2K  MICHAEL
     33.9K  DAVID
     31.7K  JOHN
     23.5K  JAMES
     23.5K  ROBERT
     20.5K  CHRISTOPHER
     20.0K  MATTHEW
     19.6K  JENNIFER
     19.2K  DANIEL
     17.9K  WILLIAM
     16.4K  MARK
     16.1K  JOSEPH
     15.9K  ANDREW
     14.6K  THOMAS
     13.8K  BRIAN
     13.8K  JEFFREY
     13.2K  SARAH
     12.8K  RICHARD
     12.4K  JESSICA
     12.2K  STEVEN

PROVIDER_MIDDLE_NAME by rows
    120.8K  A
    119.8K  M
     90.0K  J
     80.0K  L
     64.4K  R
     60.8K  S
     56.4K  E
     53.9K  D
     53.4K  C
     40.0K  K
     35.4K  B
     33.7K  P
     30.1K  T
     28.3K  W
     27.6K  G
     27.3K  H
     25.4K  N
     20.7K  F
     16.5K  MARIE
     11.9K  V

FACILITY_TYPE_CERTIFICATION_NUMBER by rows
       228  330214
        67  450388
        50  490122
        36  330246
        34  330259
        30  220074
        29  390049
        29  100017
        27  051334
        26  100212
        25  282003
        24  050782
        24  100038
        23  050145
        23  100006
        23  022001
        22  390160
        22  100032
        22  450184
        21  050485

## what

SUFF: JR. 56%, III 25%, II 12%, IV 5%, SR. 2%, I 0%, V 0%, VI 0%, IX 0%, VII 0%

FACILITY_TYPE: Hospital 85%, Home health agency 9%, Hospice 2%, Nursing home 2%, Dialysis facility 1%, Inpatient rehabilitation facil 1%, Long-term care hospital 0%

_SRC_SHA256: 7373e9b183c2aa77429f3e7960f8ae 11%, 570d60238af9fd7abea078c3fe383b 11%, e42585609657bc5ac70c7b3203f036 11%, 8eefe02e9ac530b58d5f2afed86c52 11%, 107e9d41e02ed77a9156b82a4a6484 11%, 50c2ff0574ea1fdec88b0361df1624 11%, 4b82763f049354bf8189e1d5cbb014 11%, 75740c0398b613cb2a611ea22a6c4a 11%, 55c84c5de7c2cbc4f616a4e098649a 11%, ba22ebb75f5171c0214ac79a8dc2e3 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | other | 919.2K | 0 | 1225011836 2.5K; 1225016256 2.5K; 1225014046 2.5K; 1114013927 2.5K |
| IND_PAC_ID | other | 917.0K | 0 | 6507807708 2.5K; 4688653892 2.5K; 7012922644 2.5K; 2466558754 2.5K |
| PROVIDER_LAST_NAME | who | 228.6K | 22 | PATEL 15.6K; SMITH 11.9K; MILLER 10.0K; THOMAS 8.7K |
| PROVIDER_FIRST_NAME | who | 76.7K | 62 | MICHAEL 41.2K; DAVID 33.9K; JOHN 31.7K; JAMES 23.5K |
| PROVIDER_MIDDLE_NAME | who | 36.2K | 771.4K | A 120.8K; M 119.8K; J 90.0K; L 80.0K |
| SUFF | category | 11 | 2.22M | JR. 19.7K; III 8.9K; II 4.3K; IV 1.6K |
| FACILITY_TYPE | category | 7 | 0 | Hospital 1.92M; Home health agency 213.1K; Hospice 42.0K; Nursing home 40.8K |
| CCN | who | 41.3K | 0 | 360180 6.3K; 340030 6.3K; 390046 6.2K; 100087 5.1K |
| FACILITY_TYPE_CERTIFICATION_NUMBER | who | 2.1K | 2.25M | 330214 228; 450388 67; 490122 48; 050145 41 |
| _INGESTED_AT | audit | 1 | 0 | 1783783392626274 2.26M |
| _SOURCE_RUN_ID | audit | 1 | 0 | e9e3f1a8-f13f-430a-8348-e 2.26M |
| _SRC_SHA256 | category | 10 | 0 | 7373e9b183c2aa77429f3e796 250.0K; 570d60238af9fd7abea078c3f 250.0K; e42585609657bc5ac70c7b320 250.0K; 8eefe02e9ac530b58d5f2afed 250.0K |
