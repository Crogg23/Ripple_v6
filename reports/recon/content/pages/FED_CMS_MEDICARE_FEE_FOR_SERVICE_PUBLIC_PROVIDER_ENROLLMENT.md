# FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT

rows 2.98M  columns 13  scan 4.4s

roles: audit 2, category 1, date 1, id 2, other 2, state 1, who 6

## when

_INGESTED_AT
  2026     2.98M  ##############################

## who

LAST_NAME by rows
     14.2K  SMITH
     13.2K  PATEL
     10.8K  JOHNSON
      9.4K  LEE
      8.2K  MILLER
      8.0K  WILLIAMS
      8.0K  BROWN
      7.5K  JONES
      7.0K  NGUYEN
      6.3K  DAVIS
      6.0K  KIM
      5.5K  ANDERSON
      5.5K  THOMAS
      4.8K  SHAH
      4.8K  WILSON
      4.6K  MARTIN
      4.4K  TAYLOR
      4.2K  KHAN
      4.2K  MOORE
      4.1K  THOMPSON

ORG_NAME by rows
      7.9K  WALGREEN CO
      2.8K  WAL-MART STORES EAST LP
      1.3K  WALMART INC
      1.2K  CVS PHARMACY INC
      1.1K  PUBLIX SUPER MARKETS INC
      1.0K  LUXOTTICA OF AMERICA INC
       738  HOLIDAY CVS LLC
       712  GARFIELD BEACH CVS LLC
       690  TOTAL RENAL CARE INC
       618  KROGER LIMITED PARTNERSHIP I
       614  SAFEWAY INC
       591  LINCARE INC
       523  CVS ALBANY LLC
       511  WAL-MART STORES TEXAS LLC
       446  SAMS EAST INC
       436  PENNSYLVANIA CVS PHARMACY LLC
       360  LONGS DRUG STORES CALIFORNIA LLC
       350  ALBERTSONS LLC
       338  NEW JERSEY CVS PHARMACY LLC
       337  NORTH CAROLINA CVS PHARMACY LLC

FIRST_NAME by rows
     36.1K  MICHAEL
     29.5K  DAVID
     26.5K  JOHN
     26.1K  JENNIFER
     21.3K  ROBERT
     20.8K  JAMES
     18.3K  SARAH
     17.7K  CHRISTOPHER
     17.7K  JESSICA
     17.5K  MATTHEW
     16.9K  DANIEL
     16.6K  ELIZABETH
     15.6K  WILLIAM
     14.5K  JOSEPH
     14.2K  MARK
     14.0K  ANDREW
     13.0K  EMILY
     13.0K  THOMAS
     12.6K  AMANDA
     12.1K  AMY

MDL_NAME by rows
    122.4K  M
    118.0K  A
     86.9K  L
     83.4K  J
     61.3K  R
     58.2K  E
     54.7K  S
     51.2K  C
     50.7K  D
     36.9K  K
     33.1K  B
     29.6K  P
     27.8K  T
     25.5K  N
     25.4K  G
     25.2K  MARIE
     24.9K  H
     24.5K  W
     18.8K  F
     16.9K  ANN

## who x when

LAST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  ANDERSON                                  2026:5.5K
  BROWN                                     2026:8.0K
  DAVIS                                     2026:6.3K
  JOHNSON                                   2026:10.8K
  JONES                                     2026:7.5K
  KHAN                                      2026:4.2K
  KIM                                       2026:6.0K
  LEE                                       2026:9.4K
  MARTIN                                    2026:4.6K
  MILLER                                    2026:8.2K
  MOORE                                     2026:4.2K
  NGUYEN                                    2026:7.0K
  PATEL                                     2026:13.2K
  SHAH                                      2026:4.8K
  SMITH                                     2026:14.2K
  TAYLOR                                    2026:4.4K
  THOMAS                                    2026:5.5K
  THOMPSON                                  2026:4.1K
  WILLIAMS                                  2026:8.0K
  WILSON                                    2026:4.8K

ORG_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  ALBERTSONS LLC                            2026:350
  CVS ALBANY LLC                            2026:523
  CVS PHARMACY INC                          2026:1.2K
  GARFIELD BEACH CVS LLC                    2026:712
  HOLIDAY CVS LLC                           2026:738
  KROGER LIMITED PARTNERSHIP I              2026:618
  LINCARE INC                               2026:591
  LONGS DRUG STORES CALIFORNIA LLC          2026:360
  LUXOTTICA OF AMERICA INC                  2026:1.0K
  NEW JERSEY CVS PHARMACY LLC               2026:338
  NORTH CAROLINA CVS PHARMACY LLC           2026:337
  PENNSYLVANIA CVS PHARMACY LLC             2026:436
  PUBLIX SUPER MARKETS INC                  2026:1.1K
  SAFEWAY INC                               2026:614
  SAMS EAST INC                             2026:446
  TOTAL RENAL CARE INC                      2026:690
  WAL-MART STORES EAST LP                   2026:2.8K
  WAL-MART STORES TEXAS LLC                 2026:511
  WALGREEN CO                               2026:7.9K
  WALMART INC                               2026:1.3K

## where

STATE_CD: CA 260.6K, TX 208.0K, NY 197.0K, FL 186.1K, PA 126.8K, IL 109.7K, OH 108.9K, MI 98.3K, NC 96.6K, NJ 85.4K, GA 83.9K, MA 83.1K

## what

MULTIPLE_NPI_FLAG: N 99%, Y 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | other | 2.47M | 0 | 1700812815 4.0K; 1508511353 2.5K; 1013570241 2.5K; 1609512805 2.5K |
| MULTIPLE_NPI_FLAG | category | 2 | 0 | N 2.96M; Y 19.7K |
| PECOS_ASCT_CNTL_ID | other | 2.45M | 0 | 0941278253 11.4K; 3274438395 4.0K; 0941694376 2.5K; 3971983479 2.5K |
| ENRLMT_ID | id | 2.98M | 0 | I20250910003922 2.5K; I20250910003895 2.5K; I20250910003866 2.5K; I20250910003831 2.5K |
| PROVIDER_TYPE_CD | who | 323 | 0 | 14-50 420.8K; 12-70 240.4K; 14-97 197.8K; 14-11 145.1K |
| PROVIDER_TYPE_DESC | who | 315 | 0 | PRACTITIONER - NURSE PRAC 420.8K; PART B SUPPLIER - CLINIC/ 240.4K; PRACTITIONER - PHYSICIAN  197.8K; PRACTITIONER - INTERNAL M 145.1K |
| STATE_CD | state | 56 | 0 | CA 260.6K; TX 208.0K; NY 197.0K; FL 186.1K |
| FIRST_NAME | who | 141.4K | 432.3K | MICHAEL 36.1K; DAVID 29.5K; JOHN 26.6K; JENNIFER 26.1K |
| MDL_NAME | who | 70.9K | 1.42M | M 122.4K; A 118.0K; L 86.9K; J 83.4K |
| LAST_NAME | who | 408.8K | 432.3K | SMITH 14.2K; PATEL 13.8K; LEE 12.7K; WILLIAMS 11.5K |
| ORG_NAME | who | 293.1K | 2.55M | WALGREEN CO 8.3K; WAL-MART STORES EAST LP 3.2K; MONADNOCK COMMUNITY HOSPI 1.8K; MEMORIAL HEALTH PARTNERS  1.5K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 15:04:48.150 2.98M |
| _SOURCE_RUN_ID | audit id | 2.96M | 0 | 8eedfe20-6120-4640-a54a-3 2.5K; 0df6a6e1-245d-4dfb-8817-c 2.5K; aa49382a-951e-4f30-8d7d-5 2.5K; 28e0b863-bebe-4fa0-9029-f 2.5K |
