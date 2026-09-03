# PORTAL_CKA_WPRDC_ALLEGHENY_0B1BA76AC0

rows 7.2K  columns 23  scan 3.9s

roles: amount 4, audit 2, category 11, date 1, empty 1, id 3, other 1, who 1

## when

INGESTED_AT
  2026      7.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREA | 7.2K | 0.19 | 86.7K | 11.28M | 106.10M | 4.68B |
| PERIMETER | 7.2K | 2.31 | 1.4K | 51.1K | 507.0K | 27.28M |
| SHAPE__AREA | 7.2K | 0.19 | 86.7K | 11.28M | 106.10M | 4.68B |
| SHAPE__LENGTH | 7.2K | 2.31 | 1.4K | 51.1K | 507.0K | 27.28M |

## who

SRC_SHA256 by rows
      7.2K  97b1e3d806f4e1b33f5276095ab19a22188f1a55d4663ab13ef8632543157065

SRC_SHA256 by dollars
       4.68B     7.2K rows  97b1e3d806f4e1b33f5276095ab19a22188f1a55d4663ab13ef863254315

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREA
  97b1e3d806f4e1b33f5276095ab19a22188f1a55  2026:4.68B

## what

RECLAN: Y 100%

LEVEL: 35 25%, 15 19%, 1 13%, 20 8%, 0 7%, 3 6%, 25 6%, 2 5%, 10 5%, 8 4%, 11 2%, 13 1%

PREHIS: Y 100%

ROCKFALL: Y 100%

RILLS: Y 100%

MANFILL: Y 100%

POMEROY: Prehistoric Landslide 34%, Manmade Fill 26%, Recent Landslide 14%, Outcrop Area of Thick 'Red Bed 11%, Slopes with Conspicuous Soil C 8%, Relatively Stable Ground 6%, Steep Slopes Susceptible to Ro 1%, Ground with Highly Variable Sl 0%

SYMBOL: 52 34%, 7 26%, 6 14%, 2 11%, 41 8%, 0 6%, 51 1%, 32 0%, 16 0%, 19 0%

REDBED: Y 100%

CREEP: Y 100%

VSLOPE: Y 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RECLAN | category | 2 | 6.2K | Y 1.0K |
| AREA | amount | 7.4K | 0 | 23092.28 37; 839452 37; 160404.7 37; 75472.11 37 |
| LEVEL | category | 42 | 0 | 35 1.7K; 15 1.3K; 1 865; 20 540 |
| PREHIS | category | 2 | 4.6K | Y 2.6K |
| LANDSLID_I | other | 858 | 0 | 78 37; 77 37; 76 37; 75 37 |
| ROCKFALL | category | 2 | 7.1K | Y 114 |
| RILLS | category | 2 | 7.2K | Y 3 |
| MANFILL | category | 2 | 5.0K | Y 2.3K |
| PERIMETER | amount | 7.4K | 0 | 630.502 37; 5500.235 37; 1491.236 37; 1169.406 37 |
| POMEROY | category | 9 | 12 | Prehistoric Landslide 2.5K; Manmade Fill 1.8K; Recent Landslide 1.0K; Outcrop Area of Thick 'Re 795 |
| LANDSLID | id | 7.2K | 0 | 7244 37; 7243 37; 7242 37; 7241 37 |
| SYMBOL | category | 10 | 0 | 52 2.5K; 7 1.8K; 6 1.0K; 2 795 |
| DEBRIS | empty | 1 | 7.2K |  |
| REDBED | category | 2 | 5.0K | Y 2.2K |
| CREEP | category | 2 | 6.1K | Y 1.2K |
| VSLOPE | category | 2 | 7.2K | Y 45 |
| SHAPE__AREA | amount | 7.3K | 0 | 23092.274017334 37; 839452.206756592 37; 160404.704193115 37; 75472.1382446289 37 |
| OBJECTID | id | 7.2K | 0 | 7242 37; 7241 37; 7240 37; 7239 37 |
| SHAPE__LENGTH | amount | 7.3K | 0 | 630.502352109228 37; 5500.23542151234 37; 1491.23636634329 37; 1169.40579835412 37 |
| DATASPATIAL_WKB | id | 7.4K | 0 | \x00000000030000000100000 37; \x00000000030000000100000 37; \x00000000030000000100000 37; \x00000000030000000100000 37 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:15:14.42102 7.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 19c7c941-7006-4788-ae37-e 7.2K |
| SRC_SHA256 | who | 1 | 0 | 97b1e3d806f4e1b33f5276095 7.2K |
