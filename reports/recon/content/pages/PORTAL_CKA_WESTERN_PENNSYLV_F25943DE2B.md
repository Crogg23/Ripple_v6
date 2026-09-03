# PORTAL_CKA_WESTERN_PENNSYLV_F25943DE2B

rows 160  columns 22  scan 3.6s

roles: amount 2, audit 2, category 5, date 1, empty 2, other 9, who 2

## when

INGESTED_AT
  2026       160  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 160 | 3.32 | 1.5K | 528.8K | 15.16M | 21.30M |
| SHAPE__LENGTH | 160 | 18.17 | 472.90 | 28.6K | 115.5K | 448.0K |

## who

SOURCE_CIT by rows
       160  STUDY1

SOURCE_CIT by dollars
      21.30M      160 rows  STUDY1

SRC_SHA256 by rows
       160  aab317f1bdc3ef53224ea243b8960ef0e08f75d2937799c7caf548b823d9fedf

SRC_SHA256 by dollars
      21.30M      160 rows  aab317f1bdc3ef53224ea243b8960ef0e08f75d2937799c7caf548b823d9

## who x when

SOURCE_CIT by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  STUDY1                                    2026:21.30M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  aab317f1bdc3ef53224ea243b8960ef0e08f75d2  2026:21.30M

## what

V_DATUM: NAVD88 100%

FLD_ZONE: AE 92%, A 8%

LEN_UNIT: FEET 100%

STATIC_BFE: -9999 89%, 726 2%, 727 2%, 729 1%, 724 1%, 731 1%, 732 1%, 733 1%, 742 1%, 746 1%, 728 1%, 735 1%

FLOODWAY: FLOODWAY 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VEL_UNIT | empty | 1 | 160 |  |
| V_DATUM | category | 2 | 142 | NAVD88 18 |
| FLD_AR_ID | other | 161 | 0 | 4084 1; 4083 1; 3928 1; 3927 1 |
| GLOBALID | other | 158 | 0 | dd9cc32e-8b7c-4f4e-9628-6 1; 332853b7-afa7-43f8-8564-7 1; 683e231a-f63f-4adf-9200-2 1; ea6c102a-0869-4f37-b85f-6 1 |
| VELOCITY | other | 1 | 0 | -9999 160 |
| DEPTH | other | 1 | 0 | -9999 160 |
| AR_REVERT | empty | 1 | 160 |  |
| SOURCE_CIT | who | 1 | 0 | STUDY1 160 |
| FLD_ZONE | category | 2 | 0 | AE 148; A 12 |
| DEP_REVERT | other | 1 | 0 | -9999 160 |
| SHAPE__AREA | amount | 161 | 0 | 41060.2890625 1; 17553.38671875 1; 273336.48828125 1; 2145.8671875 1 |
| SFHA_TF | other | 1 | 0 | T 160 |
| OBJECTID | other | 158 | 0 | 228 1; 227 1; 225 1; 224 1 |
| LEN_UNIT | category | 2 | 142 | FEET 18 |
| STATIC_BFE | category | 12 | 0 | -9999 142; 726 4; 727 3; 729 2 |
| SHAPE__LENGTH | amount | 160 | 0 | 5772.94966405799 1; 1765.07422260868 1; 10052.0746326875 1; 521.364705208831 1 |
| BFE_REVERT | other | 1 | 0 | -9999 160 |
| FLOODWAY | category | 2 | 156 | FLOODWAY 4 |
| DATASPATIAL_WKB | other | 160 | 0 | \x00000000030000000200000 1; \x00000000030000000100000 1; \x00000000030000000100002 1; \x00000000030000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:35:42.80265 160 |
| SOURCE_RUN_ID | audit | 1 | 0 | a940851f-bd1f-46fa-8085-7 160 |
| SRC_SHA256 | who | 1 | 0 | aab317f1bdc3ef53224ea243b 160 |
