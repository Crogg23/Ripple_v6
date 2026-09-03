# FED_COURTLISTENER_CITATIONS

rows 18.12M  columns 11  scan 6.1s

roles: audit 2, category 1, date 3, id 1, other 4, who 1

## when

DATE_CREATED
  2025    18.11M  ##############################
  2026     16.9K  

DATE_MODIFIED
  2025    18.11M  ##############################
  2026     16.9K  

_INGESTED_AT
  2026    18.12M  ##############################

## who

REPORTER by rows
     1.27M  WL
    561.6K  So. 2d
    524.5K  U.S. App. LEXIS
    509.7K  N.Y.S.2d
    506.6K  F.2d
    456.6K  U.S.
    385.8K  U.S. Dist. LEXIS
    349.4K  N.Y. App. Div. LEXIS
    337.9K  S. Ct.
    322.7K  A.2d
    319.3K  F. App'x
    318.8K  N.E.2d
    291.1K  A.D.2d
    282.7K  P.2d
    273.7K  S.W.2d
    262.9K  F.3d
    242.3K  S.E.2d
    217.3K  F. Supp.
    214.7K  A.D.
    187.9K  N.W.2d

## who x when

REPORTER by DATE_CREATED
  A.2d                                      2025:322.7K
  A.D.                                      2025:214.7K
  A.D.2d                                    2025:291.1K
  F. App'x                                  2025:319.3K
  F. Supp.                                  2025:217.3K
  F.2d                                      2025:506.6K
  F.3d                                      2025:262.9K
  N.E.2d                                    2025:318.8K
  N.W.2d                                    2025:187.9K
  N.Y. App. Div. LEXIS                      2025:349.4K
  N.Y.S.2d                                  2025:509.7K
  P.2d                                      2025:282.7K
  S. Ct.                                    2025:337.9K
  S.E.2d                                    2025:242.3K
  S.W.2d                                    2025:273.7K
  So. 2d                                    2025:561.6K
  U.S.                                      2025:456.5K 2026:67
  U.S. App. LEXIS                           2025:524.5K 2026:1
  U.S. Dist. LEXIS                          2025:385.8K
  WL                                        2025:1.27M

## what

TYPE: 2 46%, 3 19%, 1 15%, 7 7%, 6 6%, 4 5%, 8 2%, 5 0%, 9 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 17.82M | 0 | 19097417 12.8K; 19097410 12.8K; 19097403 12.8K; 19097396 12.8K |
| VOLUME | other | 1.3K | 0 | 1995 130.6K; 1996 129.7K; 1994 128.3K; 1992 127.9K |
| REPORTER | who | 995 | 0 | WL 1.27M; So. 2d 564.0K; U.S. App. LEXIS 525.8K; N.Y.S.2d 509.9K |
| PAGE | other | 1.03M | 0 | 144 35.7K; 44 35.7K; 56 35.7K; 34 35.7K |
| TYPE | category | 9 | 0 | 2 8.41M; 3 3.49M; 1 2.64M; 7 1.27M |
| CLUSTER_ID | other | 7.85M | 0 | 600794 23.0K; 764846 23.0K; 1206533 12.8K; 2521221 12.8K |
| DATE_CREATED | date | 128.6K | 0 | 2025-09-26 04:50:34.12004 18.00M; 2025-10-23 16:18:28.49672 555; 2025-10-23 16:14:06.46036 555; 2025-10-23 15:06:20.90068 555 |
| DATE_MODIFIED | date | 129.6K | 0 | 2025-09-26 04:50:34.13956 18.00M; 2025-10-24 17:23:12.22800 555; 2025-10-23 16:18:28.49673 555; 2025-10-23 16:14:06.46036 555 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:52:34.355 18.12M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 27798b3d-4974-47c9-a4b1-c 18.12M |
| _SRC_SHA256 | other | 1 | 0 | 9b1f1481a0259273f0a673f05 18.12M |
