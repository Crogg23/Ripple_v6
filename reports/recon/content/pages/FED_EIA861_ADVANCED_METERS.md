# FED_EIA861_ADVANCED_METERS

rows 2.7K  columns 50  scan 5.8s

roles: amount 34, audit 2, category 5, date 1, other 6, state 1, who 2

## when

_INGESTED_AT
  2026      2.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RESIDENTIAL | 2.7K | 0 | 0 | 112.9K | 1.31M | 16.90M |
| COMMERCIAL | 2.7K | 0 | 0 | 14.4K | 251.0K | 2.56M |
| INDUSTRIAL | 2.7K | 0 | 0 | 1.1K | 11.1K | 130.4K |
| TRANSPORTATION | 2.7K | 0 | 0 | 0 | 240 | 579 |
| TOTAL | 2.7K | 0 | 0 | 128.6K | 1.56M | 19.59M |
| RESIDENTIAL_1 | 2.7K | 0 | 1.8K | 1.08M | 5.38M | 123.76M |

## who

UTILITY_NAME by rows
        47  Adjustment 2024
        47  Tesla Inc.
        36  Sunrun Inc.
        16  TerraForm US Energy Services, LLC
        16  Greenbacker Renewable Energy Corporation
        13  WAPA-- Western Area Power Administration
         7  Greenskies Renewable Energy, LLC
         6  PacifiCorp
         6  SunPower Capital, LLC
         5  Tri-County Electric Coop, Inc (OK)
         5  Tennessee Valley Authority
         4  Empire District Electric Co
         4  Montana-Dakota Utilities Co
         3  Tri-State Electric Member Corp
         3  Northern States Power Co - Minnesota
         3  Haywood Electric Member Corp
         3  Otter Tail Power Co
         3  Southeast Electric Coop, Inc
         3  Southwestern Electric Coop Inc - (NM)
         3  Navajo Tribal Utility Authority

UTILITY_NAME by dollars
       1.56M        1 rows  NSTAR Electric Company
       1.38M        1 rows  Massachusetts Electric Co
       1.33M        1 rows  Connecticut Light & Power Co
       1.17M        1 rows  Niagara Mohawk Power Corp.
      830.1K        3 rows  MidAmerican Energy Co
      619.1K        1 rows  Los Angeles Department of Water & Power
      577.0K        1 rows  Public Service Co of NH
      518.6K        1 rows  The Narragansett Electric Co
      491.3K        1 rows  Northern Indiana Pub Serv Co
      415.3K        1 rows  Omaha Public Power District
      409.8K        2 rows  NorthWestern Energy LLC - (MT)
      337.3K       47 rows  Tesla Inc.
      329.2K        1 rows  Ohio Power Co
      318.2K        6 rows  PacifiCorp
      260.0K        3 rows  Northern States Power Co - Minnesota
      245.6K        1 rows  Withlacoochee River Elec Coop
      236.1K        1 rows  PUD No 1 of Clark County - (WA)
      191.8K        1 rows  Mississippi Power Co
      186.7K        3 rows  Southwestern Electric Power Co
      167.7K        1 rows  Central Hudson Gas & Elec Corp

_SRC_FILE by rows
      2.7K  Advanced_Meters_2024.xlsx

_SRC_FILE by dollars
      19.59M     2.7K rows  Advanced_Meters_2024.xlsx

## who x when

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL
  Adjustment 2024                           2026:0
  Connecticut Light & Power Co              2026:1.33M
  Empire District Electric Co               2026:0
  Greenbacker Renewable Energy Corporation  2026:0
  Greenskies Renewable Energy, LLC          2026:0
  Haywood Electric Member Corp              2026:0
  Los Angeles Department of Water & Power   2026:619.1K
  Massachusetts Electric Co                 2026:1.38M
  MidAmerican Energy Co                     2026:830.1K
  Montana-Dakota Utilities Co               2026:145.7K
  NSTAR Electric Company                    2026:1.56M
  Navajo Tribal Utility Authority           2026:0
  Niagara Mohawk Power Corp.                2026:1.17M
  Northern Indiana Pub Serv Co              2026:491.3K
  Northern States Power Co - Minnesota      2026:260.0K
  Omaha Public Power District               2026:415.3K
  Otter Tail Power Co                       2026:1.2K
  PacifiCorp                                2026:318.2K
  Public Service Co of NH                   2026:577.0K
  Southeast Electric Coop, Inc              2026:0
  Southwestern Electric Coop Inc - (NM)     2026:1.9K
  SunPower Capital, LLC                     2026:0
  Sunrun Inc.                               2026:0
  Tennessee Valley Authority                2026:0
  TerraForm US Energy Services, LLC         2026:0
  Tesla Inc.                                2026:337.3K
  The Narragansett Electric Co              2026:518.6K
  Tri-County Electric Coop, Inc (OK)        2026:0
  Tri-State Electric Member Corp            2026:21.7K
  WAPA-- Western Area Power Administration  2026:244

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL
  Advanced_Meters_2024.xlsx                 2026:19.59M

## where

STATE: MN 148, TX 138, IA 137, NE 111, WI 108, MO 104, IN 102, NC 101, KS 92, TN 88, GA 86, OH 84

## what

DATA_YEAR: 2024 100%, Note- Meters for the 'Behind t 0%

OWNERSHIP: Municipal 50%, Cooperative 33%, Investor Owned 7%, Behind the Meter 5%, Political Subdivision 3%, Federal 1%, State 0%

TRANSPORTATION_4: 0 99%, 1 1%, 2 0%, 6 0%, 18 0%, 7 0%, 71 0%, 16 0%, 65 0%, 419 0%, 34 0%, 90 0%

TRANSPORTATION_6: . 86%, 0 13%, 1 1%, 2 0%

TRANSPORTATION_7: . 90%, 0 10%, 1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATA_YEAR | category | 2 | 0 | 2024 2.7K; Note- Meters for the 'Beh 1 |
| UTILITY_NUMBER | other | 2.4K | 1 | 99999 59; 57313 59; 59647 48; 60981 28 |
| UTILITY_NAME | who | 2.4K | 1 | Adjustment 2024 59; Tesla Inc. 59; Sunrun Inc. 48; TerraForm US Energy Servi 28 |
| OWNERSHIP | category | 7 | 48 | Municipal 1.3K; Cooperative 896; Investor Owned 192; Behind the Meter 128 |
| SHORT_FORM | other | 1 | 1.5K | Y 1.2K |
| STATE | state | 51 | 1 | MN 148; TX 138; IA 137; NE 111 |
| BA_CODE | other | 55 | 77 | MISO 651; SWPP 401; PJM 287; TVA 169 |
| RESIDENTIAL | amount | 1.0K | 1 | . 1.1K; 0 383; 1 16; 2 10 |
| COMMERCIAL | amount | 720 | 1 | . 1.2K; 0 383; 1 22; 2 15 |
| INDUSTRIAL | amount | 199 | 1 | . 1.5K; 0 525; 1 66; 3 47 |
| TRANSPORTATION | amount | 13 | 1 | . 2.3K; 0 427; 2 4; 1 3 |
| TOTAL | amount | 1.1K | 1 | . 844; 0 605; 1 22; 4 15 |
| RESIDENTIAL_1 | amount | 1.6K | 1 | . 884; 0 168; 1838434 9; 31874 9 |
| COMMERCIAL_1 | amount | 1.3K | 1 | . 924; 0 164; 1 14; 3 11 |
| INDUSTRIAL_1 | amount | 418 | 1 | . 1.3K; 0 198; 1 84; 2 69 |
| TRANSPORTATION_1 | amount | 24 | 1 | . 2.3K; 0 415; 1 8; 6 2 |
| TOTAL_1 | amount | 1.7K | 1 | . 767; 0 220; 1 13; 3 11 |
| RESIDENTIAL_2 | amount | 42 | 1 | . 2.4K; 0 283; 1 2; 5 2 |
| COMMERCIAL_2 | amount | 31 | 1 | . 2.4K; 0 290; 78 1; 4435 1 |
| INDUSTRIAL_2 | amount | 22 | 1 | . 2.4K; 0 290; 659 1; 68 1 |
| TRANSPORTATION_2 | amount | 5 | 1 | . 2.4K; 0 282; 356 1; 134 1 |
| TOTAL_2 | amount | 42 | 1 | . 2.4K; 0 323; 5 3; 1 2 |
| RESIDENTIAL_3 | amount | 356 | 1 | . 2.0K; 0 235; 2 20; 1 17 |
| COMMERCIAL_3 | amount | 344 | 1 | . 2.0K; 0 248; 1 24; 3 19 |
| INDUSTRIAL_3 | amount | 165 | 1 | . 2.1K; 0 317; 1 41; 4 19 |
| TRANSPORTATION_3 | amount | 17 | 1 | . 2.3K; 0 356; 1 6; 3 3 |
| TOTAL_3 | amount | 420 | 1 | . 1.9K; 0 236; 1 33; 2 18 |
| RESIDENTIAL_4 | other | 2.5K | 1 | 0 89; 1 15; 12 15; 4698 14 |
| COMMERCIAL_4 | other | 1.8K | 1 | 0 115; 1 22; 2 21; 3 19 |
| INDUSTRIAL_4 | other | 542 | 1 | 0 762; 1 128; 2 97; 3 97 |
| TRANSPORTATION_4 | category | 34 | 1 | 0 2.7K; 1 15; 2 5; 6 2 |
| TOTAL_4 | amount | 2.5K | 1 | 1 20; 6 20; 3 19; 4 19 |
| RESIDENTIAL_5 | amount | 1.6K | 1 | . 958; 0 98; 18407094 9; 501964 9 |
| COMMERCIAL_5 | amount | 1.6K | 1 | . 1.0K; 0 88; 8092451 9; 4 9 |
| INDUSTRIAL_5 | amount | 1.3K | 1 | . 1.3K; 0 172; 21630014 7; 540674 7 |
| TRANSPORTATION_5 | amount | 34 | 1 | . 2.3K; 0 397; 10321 1; 15176 1 |
| TOTAL_5 | amount | 1.7K | 1 | . 875; 0 115; 48139880 9; 4 9 |
| RESIDENTIAL_6 | amount | 642 | 1 | . 2.0K; 0 112; 1797244 4; 31874 4 |
| COMMERCIAL_6 | amount | 603 | 1 | . 2.0K; 0 112; 7 5; 271764 4 |
| INDUSTRIAL_6 | amount | 230 | 1 | . 2.0K; 0 165; 1 33; 2 28 |
| TRANSPORTATION_6 | category | 4 | 1 | . 2.4K; 0 350; 1 18; 2 1 |
| TOTAL_6 | amount | 649 | 1 | . 1.9K; 0 125; 12 5; 2072728 4 |
| RESIDENTIAL_7 | amount | 140 | 1 | . 2.3K; 0 277; 39252 1; 3243 1 |
| COMMERCIAL_7 | amount | 78 | 1 | . 2.4K; 0 293; 2 3; 8 2 |
| INDUSTRIAL_7 | amount | 47 | 1 | . 2.4K; 0 291; 1 6; 2 5 |
| TRANSPORTATION_7 | category | 3 | 1 | . 2.4K; 0 283; 1 1 |
| TOTAL_7 | amount | 157 | 1 | . 2.3K; 0 295; 1 5; 4013 2 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:47.52261 2.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | e70f2c31-6dc9-4715-88a6-e 2.7K |
| _SRC_FILE | who | 1 | 0 | Advanced_Meters_2024.xlsx 2.7K |
