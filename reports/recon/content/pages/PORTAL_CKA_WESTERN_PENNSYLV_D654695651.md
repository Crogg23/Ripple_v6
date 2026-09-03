# PORTAL_CKA_WESTERN_PENNSYLV_D654695651

rows 6.6K  columns 13  scan 4.4s

roles: audit 2, category 5, date 2, id 1, other 1, who 3

## when

REQUEST_DATE
  2025      3.0K  #########################
  2026      3.6K  ##############################

INGESTED_AT
  2026      6.6K  ##############################

## who

ADDRESS by rows
        22  180 GAMMA DR
        15  1000 5TH AVE
        15  516 SINCLAIR ST
        12  211 BEECHAM DR
        11  2729 MOSSIDE BLVD
        11  820 E OHIO ST
        10  700 2ND AVE
         8  111 TECUMSEH ST
         8  12 D VALLEY ST
         8  1 BIGELOW SQ
         8  301 3RD AVE
         7  110 BARTLEY RD
         7  744 N NEGLEY AVE
         7  14 S 7TH ST
         7  2915 BEDFORD AVE
         7  2650 CENTRE AVE
         6  1808 CONCORDIA ST
         6  426 EUCLID AVE
         6  112 WASHINGTON PL
         6  755 MARY ST

CITY by rows
      3.7K  PITTSBURGH
       397  MCKEESPORT
       327  MC KEES ROCKS
       214  BRADDOCK
       151  HOMESTEAD
       100  CLAIRTON
        99  WEST MIFFLIN
        99  CORAOPOLIS
        86  CARNEGIE
        84  DUQUESNE
        80  MONROEVILLE
        73  GLASSPORT
        72  NORTH VERSAILLES
        68  VERONA
        67  TURTLE CREEK
        49  EAST PITTSBURGH
        48  TARENTUM
        39  PITCAIRN
        38  ELIZABETH
        33  BRIDGEVILLE

SRC_SHA256 by rows
      6.6K  64c0644004bce81c88434ea04eb6c86f0d6994615c6f4cfb5095598f284e6023

## who x when

ADDRESS by REQUEST_DATE
  1 BIGELOW SQ                              2025:6 2026:2
  1000 5TH AVE                              2025:4 2026:11
  110 BARTLEY RD                            2025:3 2026:4
  111 TECUMSEH ST                           2025:4 2026:4
  112 WASHINGTON PL                         2025:2 2026:4
  12 D VALLEY ST                            2025:5 2026:3
  14 S 7TH ST                               2025:3 2026:4
  180 GAMMA DR                              2025:7 2026:15
  1808 CONCORDIA ST                         2025:5 2026:1
  211 BEECHAM DR                            2025:8 2026:4
  2650 CENTRE AVE                           2025:6 2026:1
  2729 MOSSIDE BLVD                         2025:2 2026:9
  2915 BEDFORD AVE                          2025:2 2026:5
  301 3RD AVE                               2025:5 2026:3
  426 EUCLID AVE                            2026:6
  516 SINCLAIR ST                           2025:9 2026:6
  700 2ND AVE                               2025:1 2026:9
  744 N NEGLEY AVE                          2026:7
  755 MARY ST                               2025:3 2026:3
  820 E OHIO ST                             2025:8 2026:3

CITY by REQUEST_DATE
  BRADDOCK                                  2025:110 2026:104
  BRIDGEVILLE                               2025:13 2026:20
  CARNEGIE                                  2025:45 2026:41
  CLAIRTON                                  2025:36 2026:64
  CORAOPOLIS                                2025:32 2026:67
  DUQUESNE                                  2025:30 2026:54
  EAST PITTSBURGH                           2025:27 2026:22
  ELIZABETH                                 2025:13 2026:25
  GLASSPORT                                 2025:29 2026:44
  HOMESTEAD                                 2025:69 2026:82
  MC KEES ROCKS                             2025:176 2026:151
  MCKEESPORT                                2025:191 2026:206
  MONROEVILLE                               2025:33 2026:47
  NORTH VERSAILLES                          2025:25 2026:47
  PITCAIRN                                  2025:21 2026:18
  PITTSBURGH                                2025:1.7K 2026:2.0K
  TARENTUM                                  2025:22 2026:26
  TURTLE CREEK                              2025:37 2026:30
  VERONA                                    2025:25 2026:43
  WEST MIFFLIN                              2025:48 2026:51

## what

ADDRESS_2: BLDG A 56%, 5TH - 7TH FLS 12%, 2ND FL / 3RD FL 6%, 5TH FLOOR 6%, AKA 124 JOHNSTON AVENUE 6%, AKA 700 -940 CHATHAM PARK DR 6%, AKA 12-16 BELL AVENUE 6%

REQUEST_TYPE: Complaint Housing 63%, Community Environment 21%, LBP Investigation EBL 8%, West Nile 4%, Rooming Houses (Non Priority) 2%, Boarding Homes 0%, Nursing Homes 0%, Rooming Houses (Priority) 0%, Pools 0%, Pool Contamination 0%, School Buildings 0%

PROPERTY_TYPE: Multi 66%, Single 31%, N/A 2%, Vacant Lot 1%

EMERGENCY_INSPECTION_TYPE: No Heat 53%, Sewage 22%, No Water 17%, NON EMERGENCY 7%, Major Rat Infestation 1%, Other 0%, Utility Termination 0%, SEWAGE 0%, NO WATER 0%

UNITS: 2 39%, 41 11%, 0 10%, 3 10%, 4 9%, 1 7%, 19 6%, 39 6%, 6 1%, 5 1%, 24 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REQUEST_DATE | date | 304 | 0 | 2025-09-10 77; 2026-01-30 70; 2025-08-12 62; 2026-06-10 61 |
| SERVICE_REQUEST_NUMBER | id | 6.5K | 0 | HCE-SR-25-00844 53; HCE-SR-25-00178 38; HCE-SR-25-00696 36; REC25-00000-00CFI 34 |
| ADDRESS | who | 3.7K | 499 | 619 3RD ST 33; 180 GAMMA DR 33; 516 SINCLAIR ST 32; 834 ORANMORE ST 32 |
| ADDRESS_2 | category | 8 | 6.6K | BLDG A 9; 5TH - 7TH FLS 2; 2ND FL / 3RD FL 1; 5TH FLOOR 1 |
| CITY | who | 58 | 395 | PITTSBURGH 3.7K; MCKEESPORT 397; MC KEES ROCKS 327; BRADDOCK 214 |
| ZIP_CODE | other | 99 | 345 | 15132 345; 15136 331; 15212 301; 15210 287 |
| REQUEST_TYPE | category | 17 | 2.0K | Complaint Housing 2.9K; Community Environment 973; LBP Investigation EBL 388; West Nile 166 |
| PROPERTY_TYPE | category | 5 | 2.7K | Multi 2.6K; Single 1.2K; N/A 83; Vacant Lot 24 |
| EMERGENCY_INSPECTION_TYPE | category | 10 | 5.7K | No Heat 481; Sewage 200; No Water 156; NON EMERGENCY 60 |
| UNITS | category | 13 | 6.1K | 2 224; 41 66; 0 59; 3 55 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:09:27.80279 6.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | ba2a65f7-c9f8-42f2-9474-2 6.6K |
| SRC_SHA256 | who | 1 | 0 | 64c0644004bce81c88434ea04 6.6K |
