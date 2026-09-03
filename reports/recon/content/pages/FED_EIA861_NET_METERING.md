# FED_EIA861_NET_METERING

rows 1.0K  columns 119  scan 7.7s

roles: amount 77, audit 2, category 35, date 1, state 1, who 4

## when

_INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| UNNAMED_6 | 1.0K | -286.60 | 1.25 | 627.94 | 5.5K | 34.2K |
| UNNAMED_7 | 1.0K | -147.48 | 0.17 | 317.28 | 1.8K | 13.8K |
| UNNAMED_8 | 1.0K | -20.01 | 0 | 29.84 | 1.3K | 2.6K |
| UNNAMED_10 | 1.0K | -351.38 | 1.69 | 901.88 | 8.5K | 50.6K |
| INSTALLATIONS | 1.0K | 0 | 137.50 | 88.4K | 861.2K | 5.08M |
| UNNAMED_12 | 1.0K | 0 | 5 | 2.6K | 17.3K | 138.5K |

## who

UNNAMED_2 by rows
        83  99999
         6  14354
         4  5860
         3  27058
         3  12377
         3  17671
         3  19160
         3  14232
         3  6169
         2  12199
         2  5574
         2  40165
         2  17561
         2  14063
         2  8319
         2  10000
         2  16740
         2  15270
         2  15263
         2  14289

UNNAMED_2 by dollars
        5.5K        1 rows  14328
        4.2K        1 rows  17609
        1.8K        1 rows  16609
        1.6K        1 rows  803
      982.76        1 rows  6452
      907.30        1 rows  13407
      834.71        1 rows  6455
      767.97        6 rows  14354
      685.65        1 rows  11804
      666.92        1 rows  15466
      650.50        1 rows  4176
      629.43        1 rows  11171
      579.85        1 rows  54913
      577.83        1 rows  15477
      541.84        1 rows  11208
      479.24        1 rows  4110
      455.18        1 rows  9726
      427.29        1 rows  963
      405.16        2 rows  15270
      397.34        1 rows  4226

UNNAMED_3 by rows
        83  Adjustment 2024
         6  PacifiCorp
         4  Empire District Electric Co
         3  Midwest Energy Cooperative - (MI)
         3  High West Energy, Inc
         3  Fall River Rural Elec Coop Inc
         3  Otter Tail Power Co
         3  Southwest Arkansas E C C
         3  Tri-County Electric Coop, Inc (OK)
         2  Lower Valley Energy Inc
         2  Rock Energy Cooperative
         2  Empire Electric Assn, Inc
         2  Duke Energy Progress - (NC)
         2  Duke Energy Carolinas, LLC
         2  Delmarva Power
         2  Avista Corp
         2  MidAmerican Energy Co
         2  Inland Power & Light Company
         2  Evergy Metro
         2  El Paso Electric Co

UNNAMED_3 by dollars
        5.5K        1 rows  Pacific Gas & Electric Co.
        4.2K        1 rows  Southern California Edison Co
        1.8K        1 rows  San Diego Gas & Electric Co
        1.6K        1 rows  Arizona Public Service Co
      982.76        1 rows  Florida Power & Light Co
      907.30        1 rows  Nevada Power Co
      834.71        1 rows  Duke Energy Florida, LLC
      767.97        6 rows  PacifiCorp
      685.65        1 rows  Massachusetts Electric Co
      666.92        1 rows  Public Service Co of Colorado
      650.50        1 rows  Connecticut Light & Power Co
      629.43        1 rows  Long Island Power Authority
      579.85        1 rows  NSTAR Electric Company
      577.83        1 rows  Public Service Elec & Gas Co
      541.84        1 rows  Los Angeles Department of Water & Power
      479.24        1 rows  Commonwealth Edison Co
      455.18        1 rows  Jersey Central Power & Lt Co
      427.29        1 rows  Atlantic City Electric Co
      405.16        2 rows  Potomac Electric Power Co
      397.34        1 rows  Consolidated Edison Co-NY Inc

UNNAMED_4 by rows
       258  MISO
       116  PJM
       109  SWPP
        54  SOCO
        53  BPAT
        49  ERCO
        37  WACM
        35  AECI
        35  ISNE
        20  CISO
        19  PACE
        18  DUK
        14  CPLE
        14  SC
        11  WALC
        11  PSCO
        10  NYIS
        10  SEC
         9  PACW
         9  PNM

UNNAMED_4 by dollars
       11.6K       20 rows  CISO
        4.5K      116 rows  PJM
        2.6K       35 rows  ISNE
        1.6K       10 rows  NYIS
        1.4K      258 rows  MISO
        1.4K        4 rows  AZPS
        1.1K        6 rows  FPL
        1.0K        6 rows  NEVP
      843.76        6 rows  FPC
      795.71       49 rows  ERCO
      722.58       11 rows  PSCO
      570.84        3 rows  LDWP
      510.26       19 rows  PACE
      456.67      109 rows  SWPP
      433.91        4 rows  TEPC
      393.22        1 rows  SRP
      372.48        6 rows  BANC
      336.34        1 rows  HECO
      318.46       18 rows  DUK
      278.71        2 rows  TEC

_SRC_FILE by rows
      1.0K  Net_Metering_2024.xlsx

_SRC_FILE by dollars
       34.2K     1.0K rows  Net_Metering_2024.xlsx

## who x when

UNNAMED_2 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = UNNAMED_6
  10000                                     2026:43.60
  11804                                     2026:685.65
  12199                                     2026:1.34
  12377                                     2026:2.08
  13407                                     2026:907.30
  14063                                     2026:68.36
  14232                                     2026:0.94
  14289                                     2026:16.58
  14328                                     2026:5.5K
  14354                                     2026:767.97
  15263                                     2026:84.04
  15270                                     2026:405.16
  15466                                     2026:666.92
  16609                                     2026:1.8K
  16740                                     2026:2.14
  17561                                     2026:1.06
  17609                                     2026:4.2K
  17671                                     2026:1.28
  19160                                     2026:0.45
  27058                                     2026:0.50
  40165                                     2026:1.82
  4176                                      2026:650.50
  5574                                      2026:8.16
  5860                                      2026:66.04
  6169                                      2026:1.81
  6452                                      2026:982.76
  6455                                      2026:834.71
  803                                       2026:1.6K
  8319                                      2026:0.05
  99999                                     2026:-1.3K

UNNAMED_3 by _INGESTED_AT  LOAD STAMP, not an event date, dollars = UNNAMED_6
  Adjustment 2024                           2026:-1.3K
  Arizona Public Service Co                 2026:1.6K
  Avista Corp                               2026:32.10
  Connecticut Light & Power Co              2026:650.50
  Delmarva Power                            2026:139.60
  Duke Energy Carolinas, LLC                2026:278.98
  Duke Energy Florida, LLC                  2026:834.71
  Duke Energy Progress - (NC)               2026:198.65
  El Paso Electric Co                       2026:186.71
  Empire District Electric Co               2026:66.04
  Empire Electric Assn, Inc                 2026:3.64
  Evergy Metro                              2026:43.60
  Fall River Rural Elec Coop Inc            2026:1.81
  Florida Power & Light Co                  2026:982.76
  High West Energy, Inc                     2026:0.50
  Inland Power & Light Company              2026:5.44
  Lower Valley Energy Inc                   2026:1
  Massachusetts Electric Co                 2026:685.65
  MidAmerican Energy Co                     2026:41.07
  Midwest Energy Cooperative - (MI)         2026:2.08
  Nevada Power Co                           2026:907.30
  Otter Tail Power Co                       2026:0.94
  PacifiCorp                                2026:767.97
  Pacific Gas & Electric Co.                2026:5.5K
  Public Service Co of Colorado             2026:666.92
  Rock Energy Cooperative                   2026:1
  San Diego Gas & Electric Co               2026:1.8K
  Southern California Edison Co             2026:4.2K
  Southwest Arkansas E C C                  2026:1.28
  Tri-County Electric Coop, Inc (OK)        2026:0.45

## where

UNNAMED_1: TX 65, WI 60, MO 46, FL 46, MN 45, WA 42, GA 41, IN 36, CA 34, CO 31, MI 30, OK 28

## what

UNNAMED_0: 2024 100%, Note: Data is reported as coll 0%, Year 0%

CAPACITY_MW: AC 75%, DC 25%, Type 0%

UNNAMED_9: . 79%, 0 21%, Transportation 0%

UNNAMED_14: . 82%, 0 18%, Transportation 0%

UNNAMED_19: . 87%, 0 13%, 130.883 0%, Transportation 0%

UNNAMED_24: . 87%, 0 13%, Transportation 0%

UNNAMED_28: . 87%, 0 12%, 3 0%, 1 0%, 19 0%, 2 0%, Industrial 0%

UNNAMED_29: . 88%, 0 12%, Transportation 0%

UNNAMED_34: . 87%, 0 13%, Transportation 0%

UNNAMED_38: . 87%, 0 12%, 1 0%, 3 0%, 2 0%, 10 0%, 6 0%, 4 0%, Industrial 0%

UNNAMED_39: . 87%, 0 12%, Transportation 0%

UNNAMED_44: . 92%, 0 8%, Transportation 0%

UNNAMED_48: . 91%, 0 8%, 1 1%, 19 0%, 7 0%, 166 0%, 8 0%, Industrial 0%

UNNAMED_49: . 93%, 0 7%, Transportation 0%

UNNAMED_53: . 92%, 0 8%, 1.001 0%, 0.84 0%, 0.01 0%, 0.038 0%, 20.128 0%, 57.05 0%, Industrial 0%

UNNAMED_54: . 93%, 0 7%, Transportation 0%

UNNAMED_58: . 93%, 0 7%, 0.245 0%, 1.341 0%, Industrial 0%

UNNAMED_59: . 93%, 0 7%, Transportation 0%

UNNAMED_62: . 92%, 0 6%, 1 1%, 4 0%, 2 0%, 21 0%, 6 0%, 7 0%, Commercial 0%

UNNAMED_63: . 93%, 0 6%, 2 0%, 1 0%, Industrial 0%

UNNAMED_64: . 94%, 0 6%, Transportation 0%

UNNAMED_68: . 94%, 0 6%, Industrial 0%

UNNAMED_69: . 94%, 0 6%, Transportation 0%

UNNAMED_74: . 86%, 0 14%, Transportation 0%

UNNAMED_78: . 83%, 0 13%, 1 2%, 2 0%, 7 0%, 3 0%, 4 0%, 42 0%, Industrial 0%

UNNAMED_79: . 86%, 0 14%, Transportation 0%

UNNAMED_83: . 88%, 0 12%, 6571.7 0%, 4.56 0%, Industrial 0%

UNNAMED_84: . 89%, 0 11%, Transportation 0%

UNNAMED_89: . 88%, 0 12%, Transportation 0%

UNNAMED_94: . 88%, 0 12%, Transportation 0%

UNNAMED_98: . 89%, 0 11%, 7.2 0%, 11.4 0%, Industrial 0%

UNNAMED_99: . 89%, 0 10%, Transportation 0%

UNNAMED_104: 0 94%, . 6%, Transportation 0%

UNNAMED_109: 0 92%, . 8%, Transportation 0%

UNNAMED_114: 0 92%, . 8%, 130.883 0%, Transportation 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UNNAMED_0 | category | 3 | 0 | 2024 1.0K; Note: Data is reported as 1; Year 1 |
| UNNAMED_1 | state | 52 | 1 | TX 65; WI 60; MO 46; FL 46 |
| UNNAMED_2 | who | 865 | 1 | 99999 83; 14354 7; 27058 5; 19156 5 |
| UNNAMED_3 | who | 859 | 1 | Adjustment 2024 83; PacifiCorp 7; High West Energy, Inc 5; Powder River Energy Corp 5 |
| UNNAMED_4 | who | 55 | 9 | MISO 258; PJM 116; SWPP 109; SOCO 54 |
| CAPACITY_MW | category | 3 | 84 | AC 691; DC 230; Type 1 |
| UNNAMED_6 | amount | 909 | 1 | . 12; 0.005 6; 0 6; 0.528 6 |
| UNNAMED_7 | amount | 644 | 1 | . 193; 0 12; 0.02 9; 0.2 6 |
| UNNAMED_8 | amount | 215 | 1 | . 639; 0 139; 0.1 4; -0.018 3 |
| UNNAMED_9 | category | 3 | 1 | . 791; 0 213; Transportation 1 |
| UNNAMED_10 | amount | 929 | 1 | 0 7; 0.126 6; 0.027 6; 0.15 6 |
| INSTALLATIONS | amount | 555 | 1 | . 95; 1 14; 8 13; 6 10 |
| UNNAMED_12 | amount | 207 | 1 | . 268; 1 59; 2 55; 5 44 |
| UNNAMED_13 | amount | 58 | 1 | . 686; 0 128; 1 36; 2 24 |
| UNNAMED_14 | category | 3 | 1 | . 822; 0 182; Transportation 1 |
| UNNAMED_15 | amount | 564 | 1 | . 83; 2 12; 4 11; 8 10 |
| ENERGY_SOLD_BACK_MWH | amount | 328 | 1 | . 595; 0 85; 34 3; 348.021 2 |
| UNNAMED_17 | amount | 231 | 1 | . 684; 0 93; 294.823 2; 1290.546 2 |
| UNNAMED_18 | amount | 36 | 1 | . 839; 0 130; 37.322 1; 3.3 1 |
| UNNAMED_19 | category | 4 | 1 | . 872; 0 131; 130.883 1; Transportation 1 |
| UNNAMED_20 | amount | 332 | 1 | 0 593; . 83; 385.343 2; 12.22 2 |
| VIRTUAL_CAPACITY_1_MW_AND_OVER_MW | amount | 35 | 1 | . 840; 0 132; 0.305 1; 0.595 1 |
| UNNAMED_22 | amount | 43 | 1 | . 843; 0 121; 2.695 1; 373.646 1 |
| UNNAMED_23 | amount | 13 | 1 | . 870; 0 124; 5.875 1; 0.611 1 |
| UNNAMED_24 | category | 3 | 1 | . 878; 0 126; Transportation 1 |
| UNNAMED_25 | amount | 51 | 1 | 0 949; 1.5 3; 1 3; 3 2 |
| VIRTUAL_CUSTOMERS_1_MW_AND_OVER | amount | 29 | 1 | . 855; 0 123; 99 1; 42 1 |
| UNNAMED_27 | amount | 31 | 1 | . 857; 0 113; 1 3; 3 3 |
| UNNAMED_28 | category | 7 | 1 | . 878; 0 116; 3 4; 1 4 |
| UNNAMED_29 | category | 3 | 1 | . 886; 0 118; Transportation 1 |
| UNNAMED_30 | amount | 42 | 1 | 0 873; . 83; 1 5; 3 3 |
| VIRTUAL_CAPACITY_UNDER_1_MW_MW | amount | 112 | 1 | . 767; 0 115; 0.1 4; 0.24 3 |
| UNNAMED_32 | amount | 74 | 1 | . 814; 0 117; 0.02 2; 0.046 2 |
| UNNAMED_33 | amount | 11 | 1 | . 861; 0 134; 0.003 2; 0.121 1 |
| UNNAMED_34 | category | 3 | 1 | . 870; 0 134; Transportation 1 |
| UNNAMED_35 | amount | 128 | 1 | 0 866; 0.1 4; 0.24 4; 0.074 2 |
| VIRTUAL_CUSTOMERS_UNDER_1_MW | amount | 84 | 1 | . 790; 0 111; 43 4; 40 3 |
| UNNAMED_37 | amount | 48 | 1 | . 829; 0 109; 3 8; 1 5 |
| UNNAMED_38 | category | 9 | 1 | . 871; 0 125; 1 3; 3 1 |
| UNNAMED_39 | category | 3 | 1 | . 879; 0 125; Transportation 1 |
| UNNAMED_40 | amount | 97 | 1 | 0 802; . 83; 1 5; 3 4 |
| PV_PAIRED_BATTERY_CAPACITY_MW | amount | 232 | 1 | . 719; 0 37; 0.005 6; 0.015 3 |
| UNNAMED_42 | amount | 94 | 1 | . 826; 0 60; 0.015 7; 0.02 4 |
| UNNAMED_43 | amount | 19 | 1 | . 899; 0 89; 1.001 1; 0.109 1 |
| UNNAMED_44 | category | 3 | 1 | . 921; 0 83; Transportation 1 |
| UNNAMED_45 | amount | 235 | 1 | 0 752; 0.005 5; 0.015 3; 0.129 3 |
| PV_PAIRED_INSTALLATIONS | amount | 134 | 1 | . 752; 0 36; 2 14; 1 14 |
| UNNAMED_47 | amount | 27 | 1 | . 853; 0 55; 1 30; 3 11 |
| UNNAMED_48 | category | 8 | 1 | . 913; 0 77; 1 10; 19 1 |
| UNNAMED_49 | category | 3 | 1 | . 932; 0 72; Transportation 1 |
| UNNAMED_50 | amount | 136 | 1 | 0 702; . 83; 2 14; 1 14 |
| PV_PAIRED_ENERGY_CAPACITY_MWH | amount | 110 | 1 | . 845; 0 52; 0.024 2; 1.644 1 |
| UNNAMED_52 | amount | 46 | 1 | . 892; 0 63; 0.038 2; 0.027 2 |
| UNNAMED_53 | category | 9 | 1 | . 922; 0 76; 1.001 1; 0.84 1 |
| UNNAMED_54 | category | 3 | 1 | . 935; 0 69; Transportation 1 |
| UNNAMED_55 | amount | 113 | 1 | 0 812; . 83; 0.114 2; 1.919 1 |
| NOT_PV_PAIRED_BATTERY_CAPACITY_MW | amount | 37 | 1 | . 907; 0 62; 0.28 2; 3.1 1 |
| UNNAMED_57 | amount | 21 | 1 | . 918; 0 67; -0.004 2; 0.02 1 |
| UNNAMED_58 | category | 5 | 1 | . 931; 0 71; 0.245 1; 1.341 1 |
| UNNAMED_59 | category | 3 | 1 | . 931; 0 73; Transportation 1 |
| UNNAMED_60 | amount | 42 | 1 | 0 961; 0.02 2; 0.28 2; 0.015 2 |
| NOT_PV_PAIRED_INSTALLATIONS | amount | 25 | 1 | . 917; 0 58; 3 3; 1 3 |
| UNNAMED_62 | category | 9 | 1 | . 927; 0 62; 1 9; 4 2 |
| UNNAMED_63 | category | 5 | 1 | . 939; 0 63; 2 1; 1 1 |
| UNNAMED_64 | category | 3 | 1 | . 940; 0 64; Transportation 1 |
| UNNAMED_65 | amount | 27 | 1 | 0 885; . 83; 1 9; 2 2 |
| NOT_PV_PAIRED_ENERGY_CAPACITY_MWH | amount | 19 | 1 | . 925; 0 62; 0.04 2; 0.108 1 |
| UNNAMED_67 | amount | 12 | 1 | . 931; 0 64; 0.02 1; 0.372 1 |
| UNNAMED_68 | category | 3 | 1 | . 940; 0 64; Industrial 1 |
| UNNAMED_69 | category | 3 | 1 | . 941; 0 63; Transportation 1 |
| UNNAMED_70 | amount | 22 | 1 | 0 901; . 83; 0.02 2; 0.48 1 |
| CAPACITY_MW_1 | amount | 139 | 1 | . 557; 0 74; 0.01 29; 0.002 28 |
| UNNAMED_72 | amount | 102 | 1 | . 707; 0 98; 0.002 22; 0.01 13 |
| UNNAMED_73 | amount | 30 | 1 | . 838; 0 133; 0.003 4; 0.004 2 |
| UNNAMED_74 | category | 3 | 1 | . 866; 0 138; Transportation 1 |
| UNNAMED_75 | amount | 165 | 1 | 0 507; . 83; 0.002 30; 0.01 26 |
| INSTALLATIONS_1 | amount | 59 | 1 | . 556; 1 101; 0 75; 2 53 |
| UNNAMED_77 | amount | 34 | 1 | . 707; 0 98; 1 74; 2 31 |
| UNNAMED_78 | category | 9 | 1 | . 838; 0 133; 1 22; 2 5 |
| UNNAMED_79 | category | 3 | 1 | . 866; 0 138; Transportation 1 |
| UNNAMED_80 | amount | 65 | 1 | 0 507; 1 112; . 83; 2 52 |
| ENERGY_SOLD_BACK_MWH_1 | amount | 84 | 1 | . 806; 0 117; 0.3 2; 2.637 1 |
| UNNAMED_82 | amount | 33 | 1 | . 850; 0 123; 0.002 2; 0.014 1 |
| UNNAMED_83 | category | 5 | 1 | . 883; 0 119; 6571.7 1; 4.56 1 |
| UNNAMED_84 | category | 3 | 1 | . 892; 0 112; Transportation 1 |
| UNNAMED_85 | amount | 92 | 1 | 0 830; . 83; 0.002 2; 0.3 2 |
| CAPACITY_MW_2 | amount | 53 | 1 | . 816; 0 113; 0.002 4; 0.02 3 |
| UNNAMED_87 | amount | 85 | 1 | . 816; 0 96; 0.4 4; 0.065 3 |
| UNNAMED_88 | amount | 35 | 1 | . 857; 0 113; 0.05 2; 6.715 2 |
| UNNAMED_89 | category | 3 | 1 | . 885; 0 119; Transportation 1 |
| UNNAMED_90 | amount | 115 | 1 | 0 779; . 83; 0.4 5; 0.003 4 |
| INSTALLATIONS_2 | amount | 26 | 1 | . 815; 0 114; 1 23; 2 17 |
| UNNAMED_92 | amount | 28 | 1 | . 816; 0 96; 1 38; 2 15 |
| UNNAMED_93 | amount | 13 | 1 | . 857; 0 113; 1 19; 5 3 |
| UNNAMED_94 | category | 3 | 1 | . 885; 0 119; Transportation 1 |
| UNNAMED_95 | amount | 38 | 1 | 0 779; . 83; 1 55; 2 25 |
| ENERGY_SOLD_BACK_MWH_2 | amount | 14 | 1 | . 877; 0 116; 223.522 1; 20.522 1 |
| UNNAMED_97 | amount | 15 | 1 | . 884; 0 108; 18.87 1; 0.702 1 |
| UNNAMED_98 | category | 5 | 1 | . 894; 0 108; 7.2 1; 11.4 1 |
| UNNAMED_99 | category | 3 | 1 | . 899; 0 105; Transportation 1 |
| UNNAMED_100 | amount | 23 | 1 | 0 901; . 83; 223.522 1; 20.522 1 |
| CAPACITY_MW_3 | amount | 900 | 1 | 0 12; 0.511 6; 0.007 6; 1.956 6 |
| UNNAMED_102 | amount | 649 | 1 | 0 187; 0.02 9; . 9; 0.086 7 |
| UNNAMED_103 | amount | 228 | 1 | 0 724; . 39; 0.004 3; 0.1 3 |
| UNNAMED_104 | category | 3 | 1 | 0 947; . 57; Transportation 1 |
| UNNAMED_105 | amount | 925 | 1 | -1.613 6; 0.126 6; 0.027 6; 0.15 6 |
| INSTALLATIONS_3 | amount | 554 | 1 | . 83; 1 13; 0 12; 8 10 |
| UNNAMED_107 | amount | 217 | 1 | 0 187; . 83; 1 57; 2 50 |
| UNNAMED_108 | amount | 59 | 1 | 0 717; . 83; 1 41; 2 27 |
| UNNAMED_109 | category | 3 | 1 | 0 921; . 83; Transportation 1 |
| UNNAMED_110 | amount | 579 | 1 | . 83; 3 13; 4 11; 9 9 |
| ENERGY_SOLD_BACK_MWH_3 | amount | 329 | 1 | 0 596; . 83; 34 3; 348.021 2 |
| UNNAMED_112 | amount | 230 | 1 | 0 693; . 83; 294.823 2; 1290.546 2 |
| UNNAMED_113 | amount | 38 | 1 | 0 885; . 83; 37.322 1; 3.3 1 |
| UNNAMED_114 | category | 4 | 1 | 0 920; . 83; 130.883 1; Transportation 1 |
| UNNAMED_115 | amount | 332 | 1 | 0 591; . 83; 385.343 2; 12.22 2 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:39:24.62133 1.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 69b52944-1515-4ab2-a9fb-4 1.0K |
| _SRC_FILE | who | 1 | 0 | Net_Metering_2024.xlsx 1.0K |
