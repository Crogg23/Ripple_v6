# PORTAL_CKA_SAN_JOSE_OPEN_DA_D86291AAB8

rows 1.4K  columns 39  scan 3.6s

roles: amount 1, audit 2, category 8, date 1, empty 15, id 5, other 5, who 3

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 1.4K | 0.24 | 938.65 | 6.9K | 12.1K | 1.91M |

## who

ENCUMTYPE by rows
      1.4K  FreewayEOP

ENCUMTYPE by dollars
       1.91M     1.4K rows  FreewayEOP

CREATIONDATE by rows
      1.4K  1900/01/01 00:00:00+00

CREATIONDATE by dollars
       1.91M     1.4K rows  1900/01/01 00:00:00+00

SRC_SHA256 by rows
      1.4K  47295df076bd982f1e62b955e2aaf0f28d63aace51f2c58311c102152ff9dc33

SRC_SHA256 by dollars
       1.91M     1.4K rows  47295df076bd982f1e62b955e2aaf0f28d63aace51f2c58311c102152ff9

## who x when

ENCUMTYPE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  FreewayEOP                                2026:1.91M

CREATIONDATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  1900/01/01 00:00:00+00                    2026:1.91M

## what

TAXLINE: Yes 100%

LOTLINE: Yes 100%

CARTOGRAPHICLINE: Yes 100%

CONSTRUCTIONLINE: Yes 100%

CONFLICTLINE: Yes 100%

PLANCRT: MGE 99%, T-845 0%, T-756 0%, T-399 0%, T-1807 0%

PLANMOD: SVOLDTAYLOR 50%, T-9878 50%

LASTEDITOR: DSMITH 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 1.4K |
| CREATOR | other | 1 | 0 | DPW 1.4K |
| OBJECTID | id | 1.4K | 0 | 816715 7; 816691 7; 816685 7; 816557 7 |
| ENCUMID | id | 1.4K | 0 | 1000026194 7; 1000026147 7; 1000026141 7; 1000032447 7 |
| INTID | id | 1.4K | 0 | 1000026194 7; 1000026147 7; 1000026141 7; 1000032447 7 |
| ENCUMTYPE | who | 1 | 0 | FreewayEOP 1.4K |
| ENCUMSUBTYPE | empty | 1 | 1.4K |  |
| EASEMENT | empty | 1 | 1.4K |  |
| TAXLINE | category | 2 | 1.4K | Yes 6 |
| LOTLINE | category | 2 | 1.4K | Yes 6 |
| TRACTLINE | empty | 1 | 1.4K |  |
| PLANLINE | empty | 1 | 1.4K |  |
| ROADLINE | other | 1 | 0 | Yes 1.4K |
| RAILLINE | empty | 1 | 1.4K |  |
| BUILDINGLINE | empty | 1 | 1.4K |  |
| WATERLINE | empty | 1 | 1.4K |  |
| MUNICIPALLINE | empty | 1 | 1.4K |  |
| CENTERLINE | empty | 1 | 1.4K |  |
| GCELINE | empty | 1 | 1.4K |  |
| LCELINE | empty | 1 | 1.4K |  |
| OTHERLINE | empty | 1 | 1.4K |  |
| CLOSINGLINE | empty | 1 | 1.4K |  |
| CARTOGRAPHICLINE | category | 2 | 1 | Yes 1.4K |
| CONSTRUCTIONLINE | category | 2 | 1.4K | Yes 4 |
| CONFLICTLINE | category | 2 | 1.4K | Yes 4 |
| LEVELMIN | other | 1 | 0 | 0 1.4K |
| LEVELMAX | other | 1 | 0 | 0 1.4K |
| ROWWIDTH | empty | 1 | 1.4K |  |
| PLANCRT | category | 5 | 0 | MGE 1.4K; T-845 2; T-756 2; T-399 2 |
| PLANMOD | category | 3 | 1.4K | SVOLDTAYLOR 1; T-9878 1 |
| LASTUPDATE | other | 1.1K | 0 | 2005/10/25 12:20:58+00 221; 2006/08/14 10:08:03+00 12; 2006/07/28 15:36:25+00 8; 2005/12/01 15:03:02+00 8 |
| LASTEDITOR | category | 2 | 1.4K | DSMITH 1 |
| NOTES | empty | 1 | 1.4K |  |
| GLOBALID | id | 1.4K | 0 | {F15C7A52-64E0-4B8A-92F4- 7; {2235DCFA-C867-45F4-978F- 7; {ED9B9DA3-118E-424E-AC11- 7; {C548CE54-CC9A-4EA2-861F- 7 |
| ENTERPRISEID | id | 1.4K | 0 | DPW-ENCB-1000026194 7; DPW-ENCB-1000026147 7; DPW-ENCB-1000026141 7; DPW-ENCB-1000032447 7 |
| SHAPE_LENGTH | amount | 1.4K | 0 | 357.114847543892 7; 176.742189561134 7; 285.43144538935 7; 556.579846848633 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:53:54.29751 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | e0d0a279-cb6f-4d8f-ad7b-e 1.4K |
| SRC_SHA256 | who | 1 | 0 | 47295df076bd982f1e62b955e 1.4K |
