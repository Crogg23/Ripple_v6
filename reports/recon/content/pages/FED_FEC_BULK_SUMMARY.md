# FED_FEC_BULK_SUMMARY

rows 7.9K  columns 34  scan 5.3s

roles: amount 11, audit 2, category 4, date 1, empty 5, other 9, who 2

## when

CVG_END_DT
  2023       698  ######
  2024      3.2K  ############################
  2025       688  ######
  2026      3.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TTL_RECEIPTS | 7.9K | -1.62M | 22.4K | 12.39M | 1.18B | 9.48B |
| TRANS_FROM_AUTH | 7.9K | 0 | 0 | 1.88M | 533.71M | 1.76B |
| TTL_DISB | 7.9K | -38.6K | 24.8K | 11.61M | 1.18B | 9.67B |
| COH_BOP | 7.9K | -430.2K | 15.66 | 4.69M | 775.78M | 2.55B |
| COH_COP | 7.9K | -775.78M | 1.8K | 5.81M | 775.78M | 2.70B |
| CAND_CONTRIB | 7.9K | 0 | 0 | 125.9K | 25.88M | 110.46M |

## who

CAND_NAME by rows
         9  WATERS, ALLEN
         6  EKPETE KAMA, ULOMA
         6  TARKANIAN, DANNY
         6  GRAYSON, ALAN MARK
         5  SINGH, HIRSH
         5  GLUCK, GEORGE
         4  CHERNY, ANDREI
         4  GALLEGO, RUBEN
         4  TEIJEIRO, ANNETTE
         4  WALKER, BRADLEY MARK MR.
         4  GUILLORY, ELBERT LEE
         4  AMASH, JUSTIN
         4  RODIMER, DAN
         4  TROTTER, JAMES SCOTT
         4  KLACIK, KIMBERLY
         4  KIM, ANDY
         4  BRADSHAW, MARQUITA
         4  AL-AQIDI, DALIA
         4  ROKITA, THEODORE EDWARD
         4  HEGAR, MARY JENNINGS MJ

CAND_NAME by dollars
       1.18B        1 rows  BIDEN, JOSEPH R JR
       1.18B        1 rows  HARRIS, KAMALA
     180.06M        4 rows  TRONE, DAVID
     136.97M        4 rows  GALLEGO, RUBEN
     122.51M        2 rows  BROWN, SHERROD
     111.89M        4 rows  SCHIFF, ADAM
     109.74M        4 rows  ALLRED, COLIN
      93.80M        2 rows  TESTER, R. JON
      90.23M        4 rows  ROSEN, JACKY
      82.32M        2 rows  CRUZ, RAFAEL EDWARD  TED
      67.64M        2 rows  OSSOFF, T. JONATHAN
      67.28M        1 rows  KENNEDY, ROBERT, F. JR., SHANAHAN, NICOLE
      66.20M        1 rows  RAMASWAMY, VIVEK
      58.79M        2 rows  CASEY, ROBERT P. JR.
      58.38M        1 rows  HALEY, NIKKI
      57.02M        3 rows  SLOTKIN, ELISSA
      52.58M        2 rows  BALDWIN, TAMMY
      46.53M        4 rows  SCOTT, TIMOTHY E.
      46.39M        2 rows  OCASIO-CORTEZ, ALEXANDRIA
      46.14M        2 rows  KELLY, MARK

_SRC_SHA256 by rows
      7.9K  ea96d2936f065b7093dbf4099fa55d22ee01108b4abbd4166c085ff13d4b44e8

_SRC_SHA256 by dollars
       9.48B     7.9K rows  ea96d2936f065b7093dbf4099fa55d22ee01108b4abbd4166c085ff13d4b

## who x when

CAND_NAME by CVG_END_DT, dollars = TTL_RECEIPTS
  AL-AQIDI, DALIA                           2024:4.54M 2026:1.93M
  ALLRED, COLIN                             2023:598.1K 2024:94.67M 2026:14.47M
  AMASH, JUSTIN                             2024:1.83M 2026:1.1K
  BIDEN, JOSEPH R JR                        2024:1.18B
  BRADSHAW, MARQUITA                        2024:79.5K 2026:1.8K
  BROWN, SHERROD                            2024:96.53M 2026:25.98M
  CHERNY, ANDREI                            2024:5.19M 2025:20.0K
  CRUZ, RAFAEL EDWARD  TED                  2024:74.05M 2026:8.27M
  EKPETE KAMA, ULOMA                        2024:271.0K 2026:12.0K
  GALLEGO, RUBEN                            2024:129.31M 2026:7.65M
  GLUCK, GEORGE                             2024:20.6K 2026:306.5K
  GRAYSON, ALAN MARK                        2024:2.50M 2026:534.2K
  GUILLORY, ELBERT LEE                      2024:385.7K 2026:0
  HARRIS, KAMALA                            2024:1.18B
  HEGAR, MARY JENNINGS MJ                   2024:0 2026:0
  KIM, ANDY                                 2024:24.88M 2026:2.71M
  KLACIK, KIMBERLY                          2024:339.7K 2026:18.12
  OSSOFF, T. JONATHAN                       2024:7.20M 2026:60.44M
  RODIMER, DAN                              2024:0 2026:0
  ROKITA, THEODORE EDWARD                   2024:14.94 2026:0
  ROSEN, JACKY                              2024:87.83M 2026:2.40M
  SCHIFF, ADAM                              2024:96.30M 2026:15.59M
  SINGH, HIRSH                              2023:41.4K 2024:0 2025:0
  TARKANIAN, DANNY                          2024:0 2026:0
  TEIJEIRO, ANNETTE                         2024:0 2026:0
  TESTER, R. JON                            2024:93.57M 2026:233.3K
  TRONE, DAVID                              2024:127.67M 2026:52.39M
  TROTTER, JAMES SCOTT                      2024:0 2025:0
  WALKER, BRADLEY MARK MR.                  2024:1.65M 2026:0
  WATERS, ALLEN                             2023:0 2024:86.3K 2025:0

_SRC_SHA256 by CVG_END_DT, dollars = TTL_RECEIPTS
  ea96d2936f065b7093dbf4099fa55d22ee01108b  2023:11.23M 2024:6.83B 2025:50.60M 2026:2.59B

## what

CAND_ICI: C 57%, O 26%, I 17%

PTY_CD: 2 48%, 1 44%, 3 8%

CAND_PTY_AFFILIATION: REP 48%, DEM 45%, IND 3%, LIB 1%, NPA 1%, DFL 0%, OTH 0%, UN 0%, GRE 0%, NNE 0%, W 0%, CON 0%

CYCLE: 2026 51%, 2024 49%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CAND_ID | other | 5.8K | 0 | S6WY00209 40; S6WY00191 40; S4WY00162 40; S0WY00137 40 |
| CAND_NAME | who | 5.5K | 0 | SWEARENGIN, PAULA JEAN 41; BRADSHAW, MARQUITA 41; WATERS, ALLEN 41; HAGEMAN, HARRIET 40 |
| CAND_ICI | category | 4 | 122 | C 4.5K; O 2.0K; I 1.3K |
| PTY_CD | category | 3 | 0 | 2 3.8K; 1 3.5K; 3 643 |
| CAND_PTY_AFFILIATION | category | 38 | 2 | REP 3.8K; DEM 3.5K; IND 230; LIB 96 |
| TTL_RECEIPTS | amount | 5.6K | 0 | 0 2.0K; 1000 32; 1555542.88 31; 2165 31 |
| TRANS_FROM_AUTH | amount | 1.1K | 0 | 0 6.7K; 181288.13 7; 331332.77 7; 311645.45 7 |
| TTL_DISB | amount | 6.2K | 0 | 0 1.2K; 4472.7 35; 123449.91 35; 5000 35 |
| TRANS_TO_AUTH | other | 367 | 0 | 0 7.4K; 5000 13; 10000 12; 2000 12 |
| COH_BOP | amount | 3.8K | 0 | 0 3.7K; 15779.1 23; 135359.8 23; 100 23 |
| COH_COP | amount | 5.2K | 0 | 0 2.2K; 11306.4 30; 10163.54 30; 448.59 30 |
| CAND_CONTRIB | amount | 1.4K | 0 | 0 5.9K; 100 49; 7000 33; 1000 29 |
| CAND_LOANS | other | 1.0K | 0 | 0 6.0K; 10000 49; 20000 49; 50000 42 |
| OTHER_LOANS | other | 86 | 0 | 0 7.8K; 10000 7; 100 5; 100000 5 |
| CAND_LOAN_REPAY | amount | 684 | 0 | 0 7.0K; 5000 22; 20000 16; 50000 12 |
| OTHER_LOAN_REPAY | amount | 58 | 0 | 0 7.9K; 15000 2; 50000 2; 2000 2 |
| DEBTS_OWED_BY | other | 2.1K | 0 | 0 4.6K; 10000 40; 20000 37; 250000 36 |
| TTL_INDIV_CONTRIB | amount | 4.7K | 0 | 0 2.7K; -2314.35 28; 996770.72 27; 2165 27 |
| CAND_OFFICE_ST | other | 57 | 0 | CA 777; TX 614; FL 541; NY 416 |
| CAND_OFFICE_DISTRICT | other | 55 | 60 | 00 1.6K; 02 642; 01 640; 03 567 |
| SPEC_ELECTION | empty | 1 | 7.9K |  |
| PRIM_ELECTION | empty | 1 | 7.9K |  |
| RUN_ELECTION | empty | 1 | 7.9K |  |
| GEN_ELECTION | empty | 1 | 7.9K |  |
| GEN_ELECTION_PRECENT | empty | 1 | 7.9K |  |
| OTHER_POL_CMTE_CONTRIB | amount | 1.9K | 0 | 0 5.3K; 5000 76; 1000 73; 2000 43 |
| POL_PTY_CONTRIB | amount | 327 | 0 | 0 7.2K; 5000 75; 1000 41; 62000 35 |
| CVG_END_DT | date | 691 | 0 | 12/31/2024 2.3K; 03/31/2026 2.1K; 05/13/2026 295; 04/29/2026 200 |
| INDIV_REFUNDS | other | 2.2K | 0 | 0 5.0K; 100 40; 1000 36; 250 34 |
| CMTE_REFUNDS | other | 363 | 0 | 0 6.8K; 1000 104; 5000 100; 2500 63 |
| CYCLE | category | 2 | 0 | 2026 4.1K; 2024 3.9K |
| _INGESTED_AT | audit | 1 | 0 | 1782768849184250 7.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 3e1fa928-9032-4446-a4f4-0 7.9K |
| _SRC_SHA256 | who | 1 | 0 | ea96d2936f065b7093dbf4099 7.9K |
