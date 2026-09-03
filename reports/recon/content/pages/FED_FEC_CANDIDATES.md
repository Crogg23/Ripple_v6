# FED_FEC_CANDIDATES

rows 27.1K  columns 18  scan 2.9s

roles: audit 2, category 3, date 1, other 10, state 1, who 2

## when

_INGESTED_AT
  2026     27.1K  ##############################

## who

C13 by rows
       283  HOUSTON
       251  LAS VEGAS
       248  NEW YORK
       247  LOS ANGELES
       216  WASHINGTON
       208  CHICAGO
       194  DALLAS
       154  SAN ANTONIO
       150  AUSTIN
       139  PHOENIX
       128  DENVER
       127  ATLANTA
       126  MIAMI
       125  SAN DIEGO
       124  TUCSON
       118  INDIANAPOLIS
       118  BROOKLYN
       115  RALEIGH
       114  COLUMBUS
       107  ORLANDO

_SRC_SHA256 by rows
     27.1K  manifest:4:cn24.zip

## who x when

C13 by _INGESTED_AT  LOAD STAMP, not an event date
  ATLANTA                                   2026:127
  AUSTIN                                    2026:150
  BROOKLYN                                  2026:118
  CHICAGO                                   2026:208
  COLUMBUS                                  2026:114
  DALLAS                                    2026:194
  DENVER                                    2026:128
  HOUSTON                                   2026:283
  INDIANAPOLIS                              2026:118
  LAS VEGAS                                 2026:251
  LOS ANGELES                               2026:247
  MIAMI                                     2026:126
  NEW YORK                                  2026:248
  ORLANDO                                   2026:107
  PHOENIX                                   2026:139
  RALEIGH                                   2026:115
  SAN ANTONIO                               2026:154
  SAN DIEGO                                 2026:125
  TUCSON                                    2026:124
  WASHINGTON                                2026:216

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  manifest:4:cn24.zip                       2026:27.1K

## where

C14: CA 2.8K, TX 2.2K, FL 1.8K, NY 1.4K, OH 886, NC 865, IL 859, PA 856, GA 844, MI 799, NJ 745, AZ 708

## what

C6: H 68%, P 18%, S 14%

C8: C 68%, O 22%, I 9%

C9: N 50%, C 33%, P 16%, F 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C1 | other | 19.1K | 0 | H4OH11082 136; H6AL02167 136; H8OH15134 136; H8IL05131 136 |
| C2 | other | 18.1K | 0 | EVANS, ANTHONY GERALD JR 136; MATHIS, NATHAN 136; NEAL, RICK 136; SCHWARTZBERG , STEVE J 136 |
| C3 | other | 172 | 30 | REP 10.7K; DEM 9.7K; IND 2.0K; LIB 997 |
| C4 | other | 57 | 0 | 2020 6.7K; 2024 6.0K; 2022 5.6K; 2018 4.8K |
| C5 | other | 57 | 0 | US 4.8K; CA 2.2K; TX 1.8K; FL 1.5K |
| C6 | category | 3 | 0 | H 18.5K; P 4.8K; S 3.9K |
| C7 | other | 72 | 399 | 00 8.8K; 01 1.9K; 02 1.8K; 03 1.6K |
| C8 | category | 4 | 1.9K | C 17.3K; O 5.6K; I 2.4K |
| C9 | category | 5 | 4 | N 13.6K; C 9.1K; P 4.3K; F 97 |
| C10 | other | 14.5K | 5.5K | C00726034 109; C00652651 109; C00652750 109; C00818724 109 |
| C11 | other | 18.3K | 336 | 17713 INGLESIDE RD 135; 503 SHARPIE ROAD 135; 982 JAEGER STREET 135; 1906 W AINSLIE #3 135 |
| C12 | other | 2.1K | 23.7K | APT 1 28; APT 3 22; APT B 20; SUITE 400 18 |
| C13 | who | 5.1K | 10 | HOUSTON 283; LAS VEGAS 252; NEW YORK 248; LOS ANGELES 248 |
| C14 | state | 58 | 247 | CA 2.8K; TX 2.2K; FL 1.8K; NY 1.4K |
| C15 | other | 10.3K | 321 | 00000 141; 44119 135; 36352 135; 43206 135 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-24 02:11:49.000 27.1K |
| _SOURCE_RUN_ID | audit | 1 | 0 | db0e47f2-77ba-4f8d-b2a5-b 27.1K |
| _SRC_SHA256 | who | 1 | 0 | manifest:4:cn24.zip 27.1K |
