# PORTAL_CKA_IRELAND_NATIONAL_DC8E6F93C3

rows 3.5K  columns 13  scan 3.3s

roles: amount 1, audit 2, category 5, date 1, id 3, who 2

## when

INGESTED_AT
  2026      3.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LENGTH | 3.5K | 5.70 | 124.45 | 1.8K | 12.0K | 803.9K |

## who

STREETDESC by rows
        25  LT-91358
        25  R-829
        24  LT-30111
        22  LT-91685
        20  N-31
        20  R-119
        19  LT-30181
        17  LT-20263
        16  LT-60488
        16  LT-91616
        16  M-50
        14  LT-91354
        14  R-118
        14  R-113
        13  LT-91368
        13  LT-10261
        13  LT-91533
        12  LT-91555
        12  LT-91180
        12  LT-20265

STREETDESC by dollars
       18.3K       16 rows  M-50
       14.2K        7 rows  R-116
       13.0K       20 rows  R-119
       12.8K        4 rows  R-117
       10.4K       14 rows  R-113
        9.7K       14 rows  R-118
        7.6K       20 rows  N-31
        7.1K        6 rows  R-825
        5.9K       24 rows  LT-30111
        5.3K        5 rows  R-112
        5.2K        1 rows  LP-3020
        5.0K       25 rows  LT-91358
        4.8K       25 rows  R-829
        4.5K        5 rows  R-842
        4.0K       22 rows  LT-91685
        3.7K        7 rows  R-828
        3.4K        2 rows  LS-6052
        3.4K       11 rows  LT-20174
        3.3K        4 rows  R-827
        3.3K       11 rows  LT-30131

SRC_SHA256 by rows
      3.5K  2bbf9ce9cf6329b8785c01d2ac24d830e6995a17a47073f9f6be251b92fadc95

SRC_SHA256 by dollars
      803.9K     3.5K rows  2bbf9ce9cf6329b8785c01d2ac24d830e6995a17a47073f9f6be251b92fa

## who x when

STREETDESC by INGESTED_AT  LOAD STAMP, not an event date, dollars = LENGTH
  LP-3020                                   2026:5.2K
  LS-6052                                   2026:3.4K
  LT-10261                                  2026:1.0K
  LT-20174                                  2026:3.4K
  LT-20263                                  2026:2.4K
  LT-20265                                  2026:2.3K
  LT-30111                                  2026:5.9K
  LT-30181                                  2026:2.9K
  LT-60488                                  2026:1.7K
  LT-91180                                  2026:2.1K
  LT-91354                                  2026:2.7K
  LT-91358                                  2026:5.0K
  LT-91368                                  2026:2.6K
  LT-91533                                  2026:3.1K
  LT-91555                                  2026:1.4K
  LT-91616                                  2026:3.2K
  LT-91685                                  2026:4.0K
  M-50                                      2026:18.3K
  N-31                                      2026:7.6K
  R-112                                     2026:5.3K
  R-113                                     2026:10.4K
  R-116                                     2026:14.2K
  R-117                                     2026:12.8K
  R-118                                     2026:9.7K
  R-119                                     2026:13.0K
  R-825                                     2026:7.1K
  R-827                                     2026:3.3K
  R-828                                     2026:3.7K
  R-829                                     2026:4.8K
  R-842                                     2026:4.5K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LENGTH
  2bbf9ce9cf6329b8785c01d2ac24d830e6995a17  2026:803.9K

## what

ROADCLASS: LT 84%, LS 6%, R 4%, LP 4%, NP 1%, M 1%

ROADTYPE: T 84%, S 6%, P 5%, R 4%, M 1%

FOOTPATHTY: Cantilever 100%

AGEINYEARS: 114 100%

ENGINEERSA: EA 1 31%, EA 2 30%, EA 3 19%, Not taken in charge 11%, Laneways & Ped Ways 9%, M50 Motorway 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 3.5K | 0 | 3518 18; 3517 18; 3516 18; 3515 18 |
| ROADID | id | 3.6K | 0 | 3121494 18; 3121493 18; 3121492 18; 3121491 18 |
| SEGMENTID | id | 3.5K | 0 | L-99831-1 18; L-99830-1 18; L-99829-1 18; L-99828-1 18 |
| ROADCLASS | category | 6 | 0 | LT 3.0K; LS 216; R 153; LP 135 |
| LENGTH | amount | 3.5K | 0 | 120.97 18; 35.9008 18; 49.9368 18; 99.7939 18 |
| ROADTYPE | category | 6 | 4 | T 3.0K; S 215; P 162; R 149 |
| FOOTPATHTY | category | 2 | 54 | Cantilever 3.5K |
| AGEINYEARS | category | 2 | 2.9K | 114 598 |
| ENGINEERSA | category | 6 | 0 | EA 1 1.1K; EA 2 1.0K; EA 3 682; Not taken in charge 372 |
| STREETDESC | who | 1.9K | 31 | LT-91358 34; LT-91685 32; LT-30111 28; LT-91616 26 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:30:10.10557 3.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9af8a2a5-3e0c-4971-9bd8-7 3.5K |
| SRC_SHA256 | who | 1 | 0 | 2bbf9ce9cf6329b8785c01d2a 3.5K |
