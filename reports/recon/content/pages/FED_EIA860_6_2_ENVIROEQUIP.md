# FED_EIA860_6_2_ENVIROEQUIP

rows 4.4K  columns 52  scan 5.0s

roles: amount 4, audit 2, category 34, date 1, other 7, state 1, who 4

## when

_INGESTED_AT
  2026      4.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| STANDARD_SULFUR_RATE | 2.5K | 0 | 1.51 | 5.5K | 87.3K | 853.4K |
| STANDARD_SULFUR_PERCENT_SCRUBBED | 1.3K | 0 | 0 | 0.99 | 0.99 | 332.10 |
| STANDARD_NITROGEN_RATE | 2.9K | 0 | 0.68 | 2.2K | 220.0K | 714.0K |
| STANDARD_PARTICULATE_RATE | 2.8K | 0 | 0.10 | 238.77 | 2.5K | 44.1K |

## who

PLANT_NAME by rows
        17  Tennessee Eastman Operations
        16  RED-Rochester, LLC
        14  Celanese Acetate LLC
        13  Motiva Enterprises Port Arthur Refinery
        13  ExxonMobil Beaumont Refinery
        13  Archer Daniels Midland Clinton
        12  Midland Cogeneration Venture
        11  University of Illinois Abbott Power Plt
        11  Radford Army Ammunition Plant
        10  Shawnee
        10  Iowa State University
        10  UW Madison Charter Street Plant
        10  Archer Daniels Midland Peoria
        10  Johnsonville
        10  Barry
        10  Whiting Refinery
         9  Presque Isle
         9  Crystal River
         9  Kingston
         9  West County Energy Center

PLANT_NAME by dollars
      440.0K        3 rows  Powerlane Plant
       25.0K        6 rows  Waiau
       25.0K        6 rows  Kahe
       18.8K        4 rows  Lansing Smith
       10.0K        3 rows  Yorktown
       10.0K        2 rows  Honolulu
        8.0K        3 rows  George Neal North
        6.8K        5 rows  Bowater Newsprint Calhoun Operation
        6.6K        6 rows  Clifty Creek
        6.0K        3 rows  Urquhart
        5.6K        3 rows  Welsh
        5.3K        5 rows  Kyger Creek
        4.2K        9 rows  Crystal River
        4.0K        2 rows  Tolk
        4.0K        3 rows  Harrington
        3.8K        5 rows  Georgia-Pacific Cedar Springs
        3.4K        4 rows  Lake Catherine
        3.2K        2 rows  Graham
        2.9K        3 rows  Edge Moor
        2.3K        4 rows  Weston

UTILITY_NAME by rows
        88  Tennessee Valley Authority
        78  Florida Power & Light Co
        60  Virginia Electric & Power Co
        51  Georgia Power Co
        47  Entergy Louisiana LLC
        45  Duke Energy Carolinas, LLC
        43  Luminant Generation Company LLC
        36  Salt River Project
        36  Wheelabrator Environmental Systems
        36  Alabama Power Co
        35  Duke Energy Progress - (NC)
        34  Duke Energy Florida, LLC
        33  PacifiCorp
        32  DTE Electric Company
        32  NRG Texas Power LLC
        32  City of San Antonio - (TX)
        30  Wisconsin Electric Power Co
        29  Interstate Power and Light Co
        29  Archer Daniels Midland Co
        29  Consumers Energy Co - (MI)

UTILITY_NAME by dollars
      440.0K        3 rows  City of Greenville - (TX)
       60.0K       14 rows  Hawaiian Electric Co Inc
       18.8K       78 rows  Florida Power & Light Co
       12.9K       10 rows  MidAmerican Energy Co
       11.5K       60 rows  Virginia Electric & Power Co
        8.8K       18 rows  Southwestern Public Service Co
        8.3K       21 rows  Southwestern Electric Power Co
        6.8K        5 rows  Resolute Forest Products
        6.6K        6 rows  Indiana-Kentucky Electric Corp
        6.0K       19 rows  Dominion Energy South Carolina, Inc
        5.6K       36 rows  Wheelabrator Environmental Systems
        5.3K        5 rows  Ohio Valley Electric Corp
        4.9K       43 rows  Luminant Generation Company LLC
        4.3K       34 rows  Duke Energy Florida, LLC
        3.8K        5 rows  Georgia-Pacific Cedar Springs LLC
        3.5K       28 rows  Entergy Arkansas LLC
        2.9K        9 rows  Calpine Mid-Atlantic Generation LLC
        2.8K       15 rows  Cleco Power LLC
        2.4K       47 rows  Entergy Louisiana LLC
        2.3K       12 rows  Wisconsin Public Service Corp

NEW_SOURCE_REVIEW_PERMIT by rows
        12  MI-ROP-B6527-2020
         9  PSD-FL-354
         9  20328
         8  1861-AOP-R6
         8  6056
         7  P0012789
         6  1842-AOP-R7
         6  41953 PSD-TX-951
         6  V99-18
         6  19166
         6  TV45-02A
         6  1280-00090
         5  9654A; PSDTX833M3; N60M2
         5  8-2699-00126/00001
         5  PSD-01-01
         5  PSD-LA-93(M7)
         5  PSD-LA-538(M-4)
         5  85060030
         5  MI-ROP-A0884-2021b
         5  45642

NEW_SOURCE_REVIEW_PERMIT by dollars
        4.2K        2 rows  383
        3.9K        1 rows  07-A-951-P
        3.7K        2 rows  4381 PSD-TX-3
        3.0K        1 rows  05-A-878-P
        2.5K        2 rows  5129/PSDTX017M2
        2.3K        2 rows  07-SDD-301
        2.3K        1 rows  2629
        2.0K        1 rows  6030
        2.0K        1 rows  6029
        1.9K        1 rows  75-A-357-P7
        1.9K        1 rows  97-058-TV
        1.9K        1 rows  4381-PSD-TX-3
        1.7K        1 rows  05-A-031-P3
        1.5K        1 rows  1388/PSDTX631M1
        1.4K        2 rows  60163
        1.3K        1 rows  05-A-655-P3
        1.2K        1 rows  229
        1.2K        1 rows  3687
        1.2K        1 rows  50370
        1.1K        2 rows  2360-00030-V4

_SRC_FILE by rows
      4.4K  6_2_EnviroEquip_Y2024.xlsx

_SRC_FILE by dollars
      714.0K     4.4K rows  6_2_EnviroEquip_Y2024.xlsx

## who x when

PLANT_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = STANDARD_NITROGEN_RATE
  Archer Daniels Midland Clinton            2026:0.60
  Archer Daniels Midland Peoria             2026:10
  Barry                                     2026:3.24
  Bowater Newsprint Calhoun Operation       2026:6.8K
  Celanese Acetate LLC                      2026:0.37
  Clifty Creek                              2026:6.6K
  Crystal River                             2026:4.2K
  ExxonMobil Beaumont Refinery              2026:293.52
  George Neal North                         2026:8.0K
  Honolulu                                  2026:10.0K
  Iowa State University                     2026:251
  Johnsonville                              2026:0
  Kahe                                      2026:25.0K
  Kingston                                  2026:0
  Lansing Smith                             2026:18.8K
  Midland Cogeneration Venture              2026:893.24
  Motiva Enterprises Port Arthur Refinery   2026:402.24
  Powerlane Plant                           2026:440.0K
  Presque Isle                              2026:3.10
  RED-Rochester, LLC                        2026:4.92
  Radford Army Ammunition Plant             2026:0.06
  Shawnee                                   2026:10.80
  Tennessee Eastman Operations              2026:1.30
  UW Madison Charter Street Plant           2026:10
  University of Illinois Abbott Power Plt   2026:47
  Urquhart                                  2026:6.0K
  Waiau                                     2026:25.0K
  West County Energy Center                 2026:0
  Whiting Refinery                          2026:0.10
  Yorktown                                  2026:10.0K

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = STANDARD_NITROGEN_RATE
  Alabama Power Co                          2026:8.91
  Archer Daniels Midland Co                 2026:2
  City of Greenville - (TX)                 2026:440.0K
  City of San Antonio - (TX)                2026:1.3K
  Consumers Energy Co - (MI)                2026:171.84
  DTE Electric Company                      2026:1.92
  Dominion Energy South Carolina, Inc       2026:6.0K
  Duke Energy Carolinas, LLC                2026:52.86
  Duke Energy Florida, LLC                  2026:4.3K
  Duke Energy Progress - (NC)               2026:96.08
  Entergy Louisiana LLC                     2026:2.4K
  Florida Power & Light Co                  2026:18.8K
  Georgia Power Co                          2026:55.05
  Georgia-Pacific Cedar Springs LLC         2026:3.8K
  Hawaiian Electric Co Inc                  2026:60.0K
  Indiana-Kentucky Electric Corp            2026:6.6K
  Interstate Power and Light Co             2026:888.82
  Luminant Generation Company LLC           2026:4.9K
  MidAmerican Energy Co                     2026:12.9K
  NRG Texas Power LLC                       2026:604.29
  Ohio Valley Electric Corp                 2026:5.3K
  PacifiCorp                                2026:831.66
  Resolute Forest Products                  2026:6.8K
  Salt River Project                        2026:164.02
  Southwestern Electric Power Co            2026:8.3K
  Southwestern Public Service Co            2026:8.8K
  Tennessee Valley Authority                2026:100.24
  Virginia Electric & Power Co              2026:11.5K
  Wheelabrator Environmental Systems        2026:5.6K
  Wisconsin Electric Power Co               2026:21.51

## where

STATE: TX 466, FL 268, CA 224, NY 180, PA 171, LA 168, IN 157, MI 153, VA 143, AL 142, WI 139, IL 139

## what

BOILER_STATUS: OP 68%, RE 29%, OS 1%, SB 1%, CN 0%, PL 0%, SC 0%, CO 0%, op 0%, TS 0%, OA 0%, re 0%

TYPE_OF_BOILER: N 62%, Db 18%, Da 11%, D 8%, Dc 2%

NEW_SOURCE_REVIEW: N 71%, Y 29%

NEW_SOURCE_REVIEW_MONTH: 12 13%, 3 13%, 9 11%, 6 11%, 2 10%, 1 8%, 5 7%, 7 7%, 10 7%, 4 7%, 8 6%

NEW_SOURCE_REVIEW_YEAR: 2020 11%, 2007 10%, 2019 10%, 2010 10%, 2009 9%, 2015 9%, 2008 9%, 2016 9%, 2022 8%, 2013 8%, 2014 8%

REGULATION_SULFUR: ST 54%, FD 21%, XX 19%, LO 5%

UNIT_SULFUR: DP 48%, DH 23%, DM 11%, SU 7%, OT 6%, SB 3%, DC 2%, SR 1%, DL 0%

PERIOD_SULFUR: DA 19%, OH 17%, MO 16%, TH 16%, NV 13%, YR 7%, OT 4%, NS 4%, PS 2%, DT 1%, WO 1%, FT 0%

SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_1: IF 27%, SS 27%, OT 15%, NP 11%, WA 9%, ND 5%, CF 5%

SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_2: IF 41%, WA 21%, SS 20%, OT 10%, ND 3%, NP 3%, CF 2%

SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_3: SS 30%, ND 19%, OT 17%, WA 15%, NP 11%, IF 9%

SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_1: IF 24%, SS 20%, NP 17%, OT 15%, ND 10%, WA 9%, CF 4%, SE 0%

SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_2: IF 31%, WA 25%, SS 21%, OT 11%, NP 6%, ND 5%, CF 1%

SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_3: NP 25%, OT 20%, ND 20%, WA 18%, IF 10%, SS 8%

REGULATION_NITROGEN: ST 55%, FD 33%, XX 6%, LO 6%

UNIT_NITROGEN: NP 51%, NM 24%, NH 18%, OT 7%, NO 0%, NL 0%

PERIOD_NITROGEN: MO 22%, OH 20%, YR 19%, DA 14%, TH 12%, NV 4%, OT 4%, PS 2%, NS 2%, FT 1%, DT 0%, EH 0%

NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_1: LN 37%, SR 21%, OV 8%, SN 7%, NH3 5%, FR 4%, OT 4%, NP 4%, LA 3%, CF 3%, STM 2%, AA 2%

NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_2: SR 25%, LN 19%, OV 19%, NH3 12%, SN 8%, FR 6%, LA 4%, AA 3%, H20 2%, STM 1%, CF 1%, OT 1%

NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_3: SR 34%, NH3 14%, OV 13%, SN 13%, LN 9%, LA 5%, OT 5%, H20 4%, AA 1%, FR 1%, FU 1%, ND 1%

NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_1: LN 30%, SR 21%, NP 8%, SN 8%, OV 6%, NH3 6%, OT 6%, ND 5%, FR 4%, CF 2%, LA 2%, AA 2%

NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_2: SR 24%, LN 19%, OV 19%, NH3 13%, SN 7%, FR 7%, LA 5%, AA 3%, ND 1%, OT 1%, STM 1%, H20 1%

NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_3: SR 29%, NH3 17%, SN 13%, OV 13%, LN 7%, H20 6%, LA 5%, OT 4%, FR 2%, ND 2%, AA 1%, FU 1%

REGULATION_PARTICULATE: ST 60%, FD 24%, XX 10%, LO 6%

UNIT_PARTICULATE: PB 59%, PH 23%, OP 9%, PC 6%, OT 2%, PG 1%, UG 1%

PERIOD_PARTICULATE: PS 23%, OH 22%, NV 13%, TH 10%, SM 8%, NS 5%, DT 4%, MO 4%, YR 4%, DA 3%, OT 2%, WO 1%

REGULATION_MERCURY: FD 44%, XX 34%, ST 21%, LO 1%

MERCURY_CONTROL_EXISTING_STRATEGY_1: ACI 30%, BP 16%, EK 11%, OT 11%, BR 7%, SP 7%, ND 5%, EC 3%, EW 3%, NP 3%, SD 2%, TR 2%

MERCURY_CONTROL_EXISTING_STRATEGY_2: SP 18%, BP 14%, EK 14%, ACI 12%, OT 12%, SD 11%, DSI 6%, EC 4%, BR 3%, LIJ 3%, TR 2%, CD 1%

MERCURY_CONTROL_EXISTING_STRATEGY_3: ACI 26%, OT 23%, SP 11%, SD 10%, EK 10%, DSI 6%, CD 3%, BP 3%, BR 3%, JB 2%, TR 1%, EW 1%

MERCURY_CONTROL_PROPOSED_STRATEGY_1: ACI 30%, BP 15%, OT 13%, EK 8%, ND 8%, BR 7%, SP 6%, NP 4%, EC 3%, EW 2%, JB 2%, SD 2%

MERCURY_CONTROL_PROPOSED_STRATEGY_2: SP 15%, OT 14%, EK 14%, BP 13%, ACI 13%, SD 9%, DSI 7%, BR 4%, LIJ 3%, EC 3%, TR 3%, EW 2%

MERCURY_CONTROL_PROPOSED_STRATEGY_3: OT 24%, ACI 20%, EK 14%, SD 12%, SP 10%, CD 5%, DSI 5%, BP 3%, BR 2%, TR 2%, EW 2%, ND 2%

STEAM_PLANT_TYPE: 1 43%, 2 28%, 4 21%, 3 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | other | 933 | 0 | 18642 88; 6452 78; 19876 62; 7140 51 |
| UTILITY_NAME | who | 905 | 1 | Tennessee Valley Authorit 88; Florida Power & Light Co 78; Virginia Electric & Power 62; Georgia Power Co 51 |
| PLANT_CODE | other | 1.6K | 1 | 50481 29; 57919 28; 56407 28; 52089 28 |
| PLANT_NAME | who | 1.6K | 1 | Tennessee Eastman Operati 29; Sonoco Products Co 28; West County Energy Center 28; Celanese Acetate LLC 28 |
| STATE | state | 51 | 1 | TX 466; FL 268; CA 224; NY 180 |
| BOILER_ID | other | 1.1K | 1 | 1 450; 2 389; 3 283; HRSG1 205 |
| BOILER_STATUS | category | 12 | 1 | OP 3.0K; RE 1.3K; OS 62; SB 32 |
| TYPE_OF_BOILER | category | 5 | 698 | N 2.3K; Db 669; Da 398; D 294 |
| NEW_SOURCE_REVIEW | category | 2 | 1.3K | N 2.2K; Y 918 |
| NEW_SOURCE_REVIEW_PERMIT | who | 489 | 3.5K | MI-ROP-B6527-2020 13; PSD-FL-354 11; 1861-AOP-R6 10; 20328 10 |
| NEW_SOURCE_REVIEW_MONTH | category | 13 | 3.5K | 12 117; 3 116; 9 97; 6 95 |
| NEW_SOURCE_REVIEW_YEAR | category | 48 | 3.5K | 2020 51; 2007 47; 2019 46; 2010 46 |
| REGULATION_SULFUR | category | 4 | 958 | ST 1.9K; FD 746; XX 674; LO 176 |
| STANDARD_SULFUR_RATE | amount | 548 | 2.0K | 0.2 153; 1.2 129; 29 111; 0.0006 64 |
| STANDARD_SULFUR_PERCENT_SCRUBBED | amount | 34 | 3.1K | 0 909; 0.9 70; 0.95 62; 0.75 61 |
| UNIT_SULFUR | category | 9 | 1.7K | DP 1.3K; DH 630; DM 300; SU 188 |
| PERIOD_SULFUR | category | 16 | 1.7K | DA 515; OH 479; MO 441; TH 434 |
| COMPLIANCE_YEAR_SULFUR | other | 79 | 1.6K | 2002 138; 2003 130; 1972 84; 1979 82 |
| SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_1 | category | 7 | 2.4K | IF 556; SS 555; OT 313; NP 227 |
| SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_2 | category | 7 | 4.2K | IF 109; WA 55; SS 53; OT 26 |
| SULFUR_DIOXIDE_CONTROL_EXISTING_STRATEGY_3 | category | 6 | 4.4K | SS 14; ND 9; OT 8; WA 7 |
| SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_1 | category | 8 | 2.6K | IF 437; SS 371; NP 316; OT 283 |
| SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_2 | category | 7 | 4.2K | IF 60; WA 48; SS 40; OT 21 |
| SULFUR_DIOXIDE_CONTROL_PROPOSED_STRATEGY_3 | category | 6 | 4.4K | NP 10; OT 8; ND 8; WA 7 |
| REGULATION_NITROGEN | category | 4 | 1.1K | ST 1.8K; FD 1.1K; XX 203; LO 194 |
| STANDARD_NITROGEN_RATE | amount | 544 | 1.5K | 0.2 157; 2 146; 0.1 140; 0 92 |
| UNIT_NITROGEN | category | 6 | 1.3K | NP 1.6K; NM 725; NH 558; OT 225 |
| PERIOD_NITROGEN | category | 16 | 1.4K | MO 681; OH 610; YR 574; DA 421 |
| COMPLIANCE_YEAR_NITROGEN | other | 78 | 1.3K | 2000 258; 2003 193; 2002 166; 1995 163 |
| NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_1 | category | 19 | 1.6K | LN 1.0K; SR 569; OV 226; SN 197 |
| NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_2 | category | 18 | 3.0K | SR 351; LN 269; OV 265; NH3 163 |
| NITROGEN_OXIDE_CONTROL_EXISTING_STRATEGY_3 | category | 18 | 3.9K | SR 177; NH3 72; OV 68; SN 66 |
| NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_1 | category | 19 | 2.0K | LN 678; SR 489; NP 193; SN 177 |
| NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_2 | category | 17 | 3.5K | SR 212; LN 175; OV 167; NH3 113 |
| NITROGEN_OXIDE_CONTROL_PROPOSED_STRATEGY_3 | category | 17 | 4.1K | SR 105; NH3 61; SN 46; OV 45 |
| REGULATION_PARTICULATE | category | 4 | 1.2K | ST 1.9K; FD 778; XX 306; LO 191 |
| STANDARD_PARTICULATE_RATE | amount | 467 | 1.6K | 0.1 389; 0.03 343; 20 70; 0.015 69 |
| UNIT_PARTICULATE | category | 7 | 1.6K | PB 1.6K; PH 639; OP 247; PC 160 |
| PERIOD_PARTICULATE | category | 16 | 1.7K | PS 605; OH 584; NV 356; TH 252 |
| COMPLIANCE_YEAR_PARTICULATE | other | 81 | 1.6K | 2002 148; 2016 136; 2015 127; 2003 125 |
| REGULATION_MERCURY | category | 4 | 2.3K | FD 935; XX 735; ST 442; LO 21 |
| COMPLIANCE_YEAR_MERCURY | other | 59 | 2.9K | 2016 444; 2015 329; 2014 58; 2001 48 |
| MERCURY_CONTROL_EXISTING_STRATEGY_1 | category | 18 | 3.3K | ACI 318; BP 169; EK 119; OT 116 |
| MERCURY_CONTROL_EXISTING_STRATEGY_2 | category | 18 | 3.9K | SP 91; BP 75; EK 71; ACI 65 |
| MERCURY_CONTROL_EXISTING_STRATEGY_3 | category | 16 | 4.2K | ACI 69; OT 63; SP 30; SD 28 |
| MERCURY_CONTROL_PROPOSED_STRATEGY_1 | category | 18 | 3.5K | ACI 265; BP 130; OT 119; EK 75 |
| MERCURY_CONTROL_PROPOSED_STRATEGY_2 | category | 17 | 4.0K | SP 59; OT 54; EK 52; BP 51 |
| MERCURY_CONTROL_PROPOSED_STRATEGY_3 | category | 14 | 4.2K | OT 47; ACI 40; EK 28; SD 23 |
| STEAM_PLANT_TYPE | category | 4 | 1 | 1 1.9K; 2 1.2K; 4 932; 3 371 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:32.38034 4.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 1282fc4a-769c-4011-a65e-3 4.4K |
| _SRC_FILE | who | 1 | 0 | 6_2_EnviroEquip_Y2024.xls 4.4K |
