# PORTAL_CKA_WESTERN_PENNSYLV_D179E603D1

rows 90  columns 43  scan 4.7s

roles: amount 10, audit 2, category 11, date 3, empty 1, other 16, who 1

## when

CREATED_DATE
  2020        90  ##############################

LAST_EDITED_DATE
  2020        90  ##############################

INGESTED_AT
  2026        90  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PGHDB_SDE_NEIGHBORHOOD_2010_ARE | 89 | 2.87M | 11.98M | 60.02M | 74.47M | 1.44B |
| SQMILES | 90 | 0.10 | 0.45 | 2.15 | 2.68 | 55.42 |
| SHAPE__AREA | 90 | 2.88M | 12.37M | 60.04M | 74.62M | 1.54B |
| ACRES | 90 | 66.11 | 283.87 | 1.4K | 1.7K | 35.5K |
| SHAPE_AR_1 | 90 | 0 | 11.85M | 59.85M | 74.47M | 1.44B |
| INTPTLON10 | 89 | -80.08 | -79.99 | -79.89 | -79.88 | -7.1K |

## who

SRC_SHA256 by rows
        90  a8d8b7bf9f878dea471f3d375df2ae5ec0fc7aa95d492c1047df8624a9693e39

SRC_SHA256 by dollars
       55.42       90 rows  a8d8b7bf9f878dea471f3d375df2ae5ec0fc7aa95d492c1047df8624a969

## who x when

SRC_SHA256 by CREATED_DATE, dollars = SQMILES
  a8d8b7bf9f878dea471f3d375df2ae5ec0fc7aa9  2020:55.42

## what

STATEFP10: 42 100%

PLANNERASSIGN: Nancy Hirsch 20%, Nazia Tarannum 18%, Thomas Scharff 13%, Austin Herzog 9%, Vacant, contact Ose Akinlotan  9%, Christian Umbach 8%, Adriana Bowman 8%, Ose Akinlotan 7%, Alex Peppers 7%, Stephanie Joy Everett 2%

FUNCSTAT10: S 100%

MTFCC10: G5030 100%

BLKGRPCE10: 1 43%, 2 29%, 3 18%, 4 8%, 5 2%

NAMELSAD10: Block Group 1 43%, Block Group 2 29%, Block Group 3 18%, Block Group 4 8%, Block Group 5 2%

COUNTYFP10: 003 100%

AWATER10: 0 87%, 81747 1%, 163168 1%, 329216 1%, 473795 1%, 416134 1%, 586785 1%, 225010 1%, 5234 1%, 854869 1%, 138447 1%, 20843 1%

UNIQUE_ID: 19 12%, 57 12%, 23 11%, 6 10%, 113 10%, 81 9%, 25 8%, 21 8%, 24 8%, 94 7%, 18 3%, 0 2%

SECTORS: 4 16%, 3 10%, 12 10%, 7 8%, 15 8%, 13 8%, 11 8%, 6 8%, 10 6%, 1 6%, 5 6%, 2 5%

DPWDIV: 1 21%, 2 21%, 3 20%, 5 19%, 4 18%, 0 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATEFP10 | category | 2 | 1 | 42 89 |
| CREATED_DATE | date | 1 | 0 | 2020-08-14T12:57:28Z 90 |
| PLANNERASSIGN | category | 10 | 0 | Nancy Hirsch 18; Nazia Tarannum 16; Thomas Scharff 12; Austin Herzog 8 |
| PGHDB_SDE_NEIGHBORHOOD_2010_ARE | amount | 91 | 1 | 6958774.0 1; 26083320.0 1; 16904768.0 1; 9529806.0 1 |
| FUNCSTAT10 | category | 2 | 1 | S 89 |
| MTFCC10 | category | 2 | 1 | G5030 89 |
| LAST_EDITED_DATE | date | 89 | 0 | 2020-08-14T12:59:50Z 1; 2020-08-14T13:02:33Z 1; 2020-08-14T12:59:44Z 1; 2020-08-14T13:02:58Z 1 |
| OBJECTID | other | 90 | 0 | 90 1; 89 1; 88 1; 87 1 |
| HOOD_NO | other | 90 | 0 | 33 1; 72 1; 30 1; 83 1 |
| SQMILES | amount | 89 | 0 | 0.24848933 1; 0.9243167 1; 0.60589038 1; 0.32464368 1 |
| LAST_EDITED_USER | other | 1 | 0 | SDE 90 |
| BLKGRPCE10 | category | 6 | 1 | 1 38; 2 26; 3 16; 4 7 |
| GLOBALID | other | 91 | 0 | c4f5d2e1-bcd6-4207-bdea-1 1; 39308990-70d5-4da6-b2a0-a 1; fbc3ab11-0429-476e-80fd-7 1; 2858633a-175e-459b-a4c9-9 1 |
| NAMELSAD10 | category | 6 | 1 | Block Group 1 38; Block Group 2 26; Block Group 3 16; Block Group 4 7 |
| FID_NEIGHB | other | 90 | 0 | 19 1; 15 1; 57 1; 67 1 |
| COUNTYFP10 | category | 2 | 1 | 003 89 |
| AWATER10 | category | 15 | 0 | 0 76; 81747 1; 163168 1; 329216 1 |
| SHAPE__AREA | amount | 91 | 0 | 6927485.050537109 1; 25768409.827545166 1; 16891265.381072998 1; 9050535.754821777 1 |
| ACRES | amount | 88 | 0 | 159.03317368 1; 591.56268818 1; 387.76984567 1; 207.77195592 1 |
| PAGE_NUMBER | other | 1 | 0 | 15 90 |
| SHAPE_AR_1 | amount | 91 | 0 | 6958774.07065 1; 26083318.9691 1; 16904767.616 1; 9529806.36398 1 |
| CREATED_USER | other | 1 | 0 | SDE 90 |
| INTPTLON10 | amount | 88 | 1 | -080.0039415 1; -079.9922422 1; -080.0409711 1; -079.9764621 1 |
| NEIGHBOR | other | 90 | 0 | 24 1; 72 1; 50 1; 56 1 |
| INTPTLAT10 | other | 91 | 1 | +40.4641570 1; +40.4302576 1; +40.4400199 1; +40.4416579 1 |
| FID_BLOCKG | other | 90 | 0 | 0 2; 31 1; 16 1; 153 1 |
| TEMP | empty | 1 | 90 |  |
| GEOID10 | other | 90 | 1 | 420032509002 1; 420031702001 1; 420035626002 1; 420030511001 1 |
| UNIQUE_ID | category | 12 | 0 | 19 11; 57 11; 23 10; 6 9 |
| PERIMETER | amount | 4 | 0 | 136797.97928478 39; 198927.41614216 30; 80995.80627227 18; 87456.39013128 3 |
| TRACTCE10 | other | 79 | 1 | 563000 3; 562600 2; 561700 2; 563100 2 |
| SHAPE_LE_1 | amount | 91 | 0 | 12677.555901 1; 34676.3550984 1; 21609.7993427 1; 19562.5780689 1 |
| NEIGHBOR_I | other | 89 | 0 | 2106 1; 2154 1; 2132 1; 2138 1 |
| SECTORS | category | 16 | 0 | 4 12; 3 8; 12 8; 7 6 |
| SHAPE__LENGTH | amount | 89 | 0 | 12621.964861583318 1; 34700.37196941885 1; 21714.648282560982 1; 17830.507786321778 1 |
| DPWDIV | category | 6 | 0 | 1 19; 2 19; 3 18; 5 17 |
| SHAPE_LENG | amount | 91 | 0 | 13652.2147116 1; 12037.8994561 1; 11480.1400026 1; 6208.94140454 1 |
| HOOD | other | 91 | 0 | Fineview 1; South Side Flats 1; Elliott 1; Terrace Village 1 |
| ALAND10 | other | 89 | 0 | 384629 1; 406640 1; 579141 1; 183645 1 |
| DATASPATIAL_WKB | other | 90 | 0 | \x00000000030000000100000 1; \x00000000030000000100000 1; \x00000000030000000100000 1; \x00000000030000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:30:36.87242 90 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3ed74eda-4531-4dcf-bae3-2 90 |
| SRC_SHA256 | who | 1 | 0 | a8d8b7bf9f878dea471f3d375 90 |
