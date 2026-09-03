# PORTAL_CKA_SAN_JOSE_OPEN_DA_B6D7CBC686

rows 10.0K  columns 32  scan 4.3s

roles: amount 2, audit 2, category 8, date 1, empty 1, id 5, other 4, who 10

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| STREETMILES | 10.0K | 0 | 0.15 | 1.27 | 4.20 | 2.2K |
| SHAPE_LENGTH | 10.0K | 20 | 754.08 | 4.8K | 20.5K | 9.83M |

## who

STREETNAME by rows
        40  MONTEREY RD SB
        32  MONTEREY RD NB
        21  SAN FERNANDO ST E
        20  SENTER RD S
        20  ALMADEN RD
        17  CHERRY AV
        16  MERIDIAN AV
        15  CAPITOL AV N SB
        14  CAPITOL AV N NB
        13  KING RD S
        13  1ST ST N NB
        12  BLOSSOM HILL RD WB
        12  FOXWORTHY AV
        12  BLOSSOM HILL RD EB
        12  CAMDEN AV EB
        11  1ST ST N SB
        11  CHAPMAN ST
        11  SIERRA RD
        11  MORSE ST
        11  NARVAEZ AV

STREETNAME by dollars
       15.89       40 rows  MONTEREY RD SB
       15.42       32 rows  MONTEREY RD NB
       11.29       20 rows  SENTER RD S
       10.74       16 rows  MERIDIAN AV
        9.36       12 rows  BLOSSOM HILL RD WB
        8.56        9 rows  WHITE RD S
        8.37        6 rows  MONTEREY RD
        7.99       13 rows  KING RD S
        7.93        7 rows  HILLSDALE AV
        7.83       12 rows  BLOSSOM HILL RD EB
        7.51       17 rows  CHERRY AV
        7.19        8 rows  OAKLAND RD
        6.61       13 rows  1ST ST N NB
        6.40        8 rows  CURTNER AV
        6.24       11 rows  SIERRA RD
        6.18        7 rows  STEVENS CREEK BL EB
        6.15        7 rows  MOORPARK AV
        6.05        8 rows  SANTA TERESA BL NB
           6        9 rows  MCLAUGHLIN AV
        5.93       11 rows  1ST ST N SB

LASTMRTREATMENTTYPE by rows
      2.1K  CHIP SEAL
      1.9K  86-DIGOUTS & MICROSURFACING
      1.1K  CAPE SEAL (With DIG OUTS)
       925  40-2.0" MILL AND FILL
       472  3D-2" HMA MILL AND OVERLAY
       357  5D-2" MILL AND FILL
       333  SLURRY SEAL
       314  55-SEAL CRACKS & FOG SEAL
       249  1.5" MILL & FILL
       233  MICROSURFACING
       168  AC OVERLAY w/FABRIC <2.0 in
       159  54-RUB EMUL AGGR SLURRY (REAS)
       137  DIG-OUT & MICROSURFACE
       128  86-MICROSURFACING WITH DIGOUTS
       111  37-3" CIR WITH 2" OVERLAY
       106  2" OVERLAY
       103  2" MILL + 2" RHMA
        99  RUBBERIZED ASPHALT OVERLAY
        81  CIR + 2" RHMA
        79  65-MILL AND THIN OVELAY ( < 1 )

LASTMRTREATMENTTYPE by dollars
      359.66     1.9K rows  86-DIGOUTS & MICROSURFACING
      321.12     2.1K rows  CHIP SEAL
      182.67     1.1K rows  CAPE SEAL (With DIG OUTS)
      157.53      925 rows  40-2.0" MILL AND FILL
      125.09      333 rows  SLURRY SEAL
      124.14      233 rows  MICROSURFACING
       81.12      472 rows  3D-2" HMA MILL AND OVERLAY
       74.96      137 rows  DIG-OUT & MICROSURFACE
       60.27      357 rows  5D-2" MILL AND FILL
       58.62      128 rows  86-MICROSURFACING WITH DIGOUTS
       48.33      103 rows  2" MILL + 2" RHMA
       44.74       81 rows  CIR + 2" RHMA
       41.25      249 rows  1.5" MILL & FILL
       39.99      314 rows  55-SEAL CRACKS & FOG SEAL
       38.59       99 rows  RUBBERIZED ASPHALT OVERLAY
       36.68       76 rows  SLURRY SEAL - (With Prep)
       32.43      168 rows  AC OVERLAY w/FABRIC <2.0 in
       29.72      106 rows  2" OVERLAY
       28.16      111 rows  37-3" CIR WITH 2" OVERLAY
       28.06      159 rows  54-RUB EMUL AGGR SLURRY (REAS)

LASTEDITOR by rows
     10.0K  JAY.VANBILJOUW

LASTEDITOR by dollars
        2.2K    10.0K rows  JAY.VANBILJOUW

CREATOR by rows
     10.0K  JAY.VANBILJOUW

CREATOR by dollars
        2.2K    10.0K rows  JAY.VANBILJOUW

## who x when

STREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = STREETMILES
  1ST ST N NB                               2026:6.61
  1ST ST N SB                               2026:5.93
  ALMADEN RD                                2026:5.58
  BLOSSOM HILL RD EB                        2026:7.83
  BLOSSOM HILL RD WB                        2026:9.36
  CAMDEN AV EB                              2026:4.62
  CAPITOL AV N NB                           2026:4.79
  CAPITOL AV N SB                           2026:5.15
  CHAPMAN ST                                2026:1.15
  CHERRY AV                                 2026:7.51
  CURTNER AV                                2026:6.40
  FOXWORTHY AV                              2026:4.10
  HILLSDALE AV                              2026:7.93
  KING RD S                                 2026:7.99
  MCLAUGHLIN AV                             2026:6
  MERIDIAN AV                               2026:10.74
  MONTEREY RD                               2026:8.37
  MONTEREY RD NB                            2026:15.42
  MONTEREY RD SB                            2026:15.89
  MOORPARK AV                               2026:6.15
  MORSE ST                                  2026:1.12
  NARVAEZ AV                                2026:2.26
  OAKLAND RD                                2026:7.19
  SAN FERNANDO ST E                         2026:2.78
  SANTA TERESA BL NB                        2026:6.05
  SENTER RD S                               2026:11.29
  SIERRA RD                                 2026:6.24
  STEVENS CREEK BL EB                       2026:6.18
  WHITE RD S                                2026:8.56

LASTMRTREATMENTTYPE by INGESTED_AT  LOAD STAMP, not an event date, dollars = STREETMILES
  1.5" MILL & FILL                          2026:41.25
  2" MILL + 2" RHMA                         2026:48.33
  2" OVERLAY                                2026:29.72
  37-3" CIR WITH 2" OVERLAY                 2026:28.16
  3D-2" HMA MILL AND OVERLAY                2026:81.12
  40-2.0" MILL AND FILL                     2026:157.53
  54-RUB EMUL AGGR SLURRY (REAS)            2026:28.06
  55-SEAL CRACKS & FOG SEAL                 2026:39.99
  5D-2" MILL AND FILL                       2026:60.27
  65-MILL AND THIN OVELAY ( < 1 )           2026:15.58
  86-DIGOUTS & MICROSURFACING               2026:359.66
  86-MICROSURFACING WITH DIGOUTS            2026:58.62
  AC OVERLAY w/FABRIC <2.0 in               2026:32.43
  CAPE SEAL (With DIG OUTS)                 2026:182.67
  CHIP SEAL                                 2026:321.12
  CIR + 2" RHMA                             2026:44.74
  DIG-OUT & MICROSURFACE                    2026:74.96
  MICROSURFACING                            2026:124.14
  RUBBERIZED ASPHALT OVERLAY                2026:38.59
  SLURRY SEAL                               2026:125.09
  SLURRY SEAL - (With Prep)                 2026:36.68

## what

FUNCTIONALCLASS: Residential 87%, Arterial 10%, Collector 3%

NATIONALHIGHWAYSYSTEM: 0 96%, 1 4%

PCIPUBLICCLASS: Good 59%, Fair 23%, Poor 18%

COUNCILDISTRICT: 10 15%, 9 13%, 6 11%, 8 11%, 4 10%, 1 10%, 2 9%, 5 8%, 7 7%, 3 7%

LASTUPDATE: 2024/10/07 23:07:31+00 55%, 2024/10/07 23:31:52+00 45%

STREETTYPE: Local 84%, Major 16%

COUNCILDISTRICTLIST: 10 15%, 9 13%, 6 11%, 8 11%, 4 10%, 1 10%, 2 9%, 5 8%, 7 7%, 3 7%

CREATIONDATE: 2024/10/07 23:07:31+00 55%, 2024/10/07 23:31:52+00 45%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FUNCTIONALCLASS | category | 4 | 7 | Residential 8.7K; Arterial 973; Collector 295 |
| NATIONALHIGHWAYSYSTEM | category | 3 | 7 | 0 9.6K; 1 408 |
| OBJECTID | id | 9.9K | 0 | 62751 50; 62750 50; 62749 50; 62748 50 |
| FACILITYID | who | 10.1K | 0 | 60017 50; 60016 50; 60015 50; 60014 50 |
| INTID | id | 10.1K | 0 | 60017 50; 60016 50; 60015 50; 60014 50 |
| PAVENUM | id | 10.0K | 1 | 5990820 50; 5990810 50; 5990800 50; 5990790 50 |
| STREETNAME | who | 7.2K | 0 | MONTEREY RD SB 61; SARATOGA AV NB 59; SARATOGA AV SB 57; SENTER RD S 57 |
| STREETFROM | who | 3.9K | 0 | CAMDEN AV 101; SANTA TERESA BL 86; MERIDIAN AV 73; BRANHAM LN 71 |
| STREETTO | who | 3.5K | 0 | S END 908; E END 792; N END 585; W END 511 |
| STREETLENGTH | other | 1.8K | 0 | 300 91; 250 86; 230 77; 270 76 |
| STREETWIDTH | other | 90 | 0 | 32 5.4K; 26 929; 36 517; 30 408 |
| STREETAREA | other | 5.4K | 0 | 8001 53; 7362 52; 8163 51; 30663 51 |
| STREETMILES | amount | 5.5K | 0 | 0.05051136 53; 0.04647727 52; 0.05153409 51; 0.19357955 51 |
| PCICURRENT | other | 99 | 7 | 92 795; 90 532; 95 453; 91 408 |
| PCIPUBLICCLASS | category | 3 | 0 | Good 5.9K; Fair 2.3K; Poor 1.8K |
| PCIDATE | who | 1 | 0 | 2024/03/08 00:00:00+00 10.0K |
| LASTMRTREATMENTDATE | who | 556 | 260 | 2022/12/09 00:00:00+00 1.1K; 2021/12/15 00:00:00+00 759; 2023/12/05 00:00:00+00 616; 2010/09/15 00:00:00+00 380 |
| LASTMRTREATMENTTYPE | who | 62 | 260 | CHIP SEAL 2.1K; 86-DIGOUTS & MICROSURFACI 1.9K; CAPE SEAL (With DIG OUTS) 1.1K; 40-2.0" MILL AND FILL 925 |
| COUNCILDISTRICT | category | 10 | 0 | 10 1.5K; 9 1.3K; 6 1.1K; 8 1.1K |
| LASTUPDATE | category | 2 | 0 | 2024/10/07 23:07:31+00 5.5K; 2024/10/07 23:31:52+00 4.5K |
| LASTEDITOR | who | 1 | 0 | JAY.VANBILJOUW 10.0K |
| NOTES | empty | 1 | 10.0K |  |
| GLOBALID | id | 9.9K | 0 | {2EDBD442-B843-4FA8-99B6- 50; {662E2ECE-EB15-4464-8983- 50; {EC12D84A-0C49-4899-9498- 50; {FEBB3844-5D4C-464F-9086- 50 |
| ENTERPRISEID | id | 10.1K | 0 | DOT-CONI-0000060017 50; DOT-CONI-0000060016 50; DOT-CONI-0000060015 50; DOT-CONI-0000060014 50 |
| STREETTYPE | category | 2 | 0 | Local 8.4K; Major 1.6K |
| COUNCILDISTRICTLIST | category | 10 | 0 | 10 1.5K; 9 1.3K; 6 1.1K; 8 1.1K |
| CREATIONDATE | category | 2 | 0 | 2024/10/07 23:07:31+00 5.5K; 2024/10/07 23:31:52+00 4.5K |
| CREATOR | who | 1 | 0 | JAY.VANBILJOUW 10.0K |
| SHAPE_LENGTH | amount | 9.8K | 0 | 5124.88113724068 50; 2381.25614028896 50; 346.674042980688 50; 1824.31586440097 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:24:54.02741 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | b0b102a7-80a4-4bb6-8939-4 10.0K |
| SRC_SHA256 | who | 1 | 0 | 693fbdbd5dd5bb4db019ee16f 10.0K |
