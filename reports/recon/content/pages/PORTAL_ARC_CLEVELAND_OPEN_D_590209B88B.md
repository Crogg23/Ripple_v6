# PORTAL_ARC_CLEVELAND_OPEN_D_590209B88B

rows 34  columns 22  scan 3.4s

roles: amount 5, audit 2, category 13, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        34  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERIMETER | 34 | 0 | 34.2K | 76.6K | 76.9K | 1.31M |
| INTERMED | 34 | 0 | 446.38 | 1.3K | 1.3K | 19.3K |
| SQ_MILES | 34 | 0 | 1.60 | 4.72 | 4.72 | 69.18 |
| SHAPE__AREA | 34 | 23.25M | 47.20M | 155.61M | 164.29M | 2.18B |
| SHAPE__LENGTH | 34 | 22.3K | 34.2K | 80.9K | 84.1K | 1.38M |

## who

SRC_SHA256 by rows
        34  735c00c718a20fc674ba875c3456027216d0bc7c58957db9cd0fd2cabbe4a3f2

SRC_SHA256 by dollars
       1.31M       34 rows  735c00c718a20fc674ba875c3456027216d0bc7c58957db9cd0fd2cabbe4

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERIMETER
  735c00c718a20fc674ba875c3456027216d0bc7c  2026:1.31M

## what

OBJECTID: 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%

CE_SPA90: 14 11%, 23 11%, 28 11%, 33 11%, 37 11%, 32 11%, 0 6%, 34 6%, 27 6%, 36 6%, 31 6%, 22 6%

CE_SPA90_I: 13 11%, 22 11%, 27 11%, 32 11%, 36 11%, 31 11%, 0 6%, 33 6%, 26 6%, 35 6%, 30 6%, 21 6%

SPA: 10 12%, 06 12%, 11 12%, 26 12%, 01 12%, 12 12%, 25 6%, 02 6%, 04 6%, 07 6%, 20 6%

SPANM: Ohio City 8%, Edgewater 8%, Clark-Fulton 8%, Cudell 8%, Union-Miles 8%, Detroit Shoreway 8%, Mount Pleasant 8%, Lee-Seville 8%, Hopkins 8%, Old Brooklyn 8%, Jefferson 8%, Kamm's 8%

DIST: 2 21%, 1 21%, 4 15%, 3 15%, 5 15%, 6 12%

CDMODELBLK: Yes 100%

LB_HOLD: Midland 22%, Forgotten Triangle 11%, Pershing & I-77 11%, Bvr/55&W/Main/Midtn 11%, Frank Avenue 11%, LguePk/Midtn/UpCh 11%, Superior5/White Mtrs 11%, Coit Rd / Coit II 11%

MB_HTF: 98 Great Homes 17%, Marvin 17%, Corlett 8%, Bridgeport 8%, Artisan Moreland 8%, Buhrer Rowley 8%, East Central / Fairfax 8%, Ashbury 8%, E Clark/Col Villge Spr Up 8%, Waterloo Village 8%

NPI_SII: Detroit-Shoreway 18%, Fairfax Renaissance 18%, Buckeye Area 18%, Famicos 18%, Slavic Village 9%, Tremont West 9%, Buckeye Area/Famicos 9%

TYPOLOGY: Stable/Transitional/Fragile 21%, Stable/Transitional/Fragile/Di 18%, Regional Choice/Stable/Transit 15%, Regional Choice/Stable 12%, Fragile/Distressed 12%, Transitional/Fragile 6%, Regional Choice/Stable/Transit 6%, Regional Choice 3%, Reg Choice/Stable/Transitional 3%, Fragile 3%

GLOBALID: 412fbd6a-21da-40d7-8a8c-f7e08f 8%, f922604c-6e40-4f40-a4a7-6f48e2 8%, f3410fd8-407d-4c5d-a1e6-d62837 8%, 4fdea8d0-6669-4b40-ba18-708649 8%, 508fe690-5e07-4625-bae2-8868d5 8%, 9f4fef6f-2a78-4d71-b531-299d94 8%, 01634adf-d45e-4619-abcc-af7d91 8%, bb0696d1-2372-4f3c-985f-2ba79b 8%, f6c29ed9-2cb2-4f31-943c-e80351 8%, 0203a842-dd1e-4509-b901-067631 8%, 3c56157f-f52b-4984-9d3e-74f3e9 8%, 8ce04c57-075d-4d65-adec-0d7366 8%

GEOMETRY: {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 34 | 0 | 34 1; 33 1; 32 1; 31 1 |
| AREA | empty | 1 | 34 |  |
| PERIMETER | amount | 28 | 0 | 22000.985 2; 26293.611 2; 25273.027 2; 46101.852 2 |
| CE_SPA90 | category | 28 | 0 | 14 2; 23 2; 28 2; 33 2 |
| CE_SPA90_I | category | 28 | 0 | 13 2; 22 2; 27 2; 32 2 |
| SPA | category | 28 | 1 | 10 2; 06 2; 11 2; 26 2 |
| SPANM | category | 33 | 0 | Ohio City 1; Edgewater 1; Clark-Fulton 1; Cudell 1 |
| DIST | category | 7 | 1 | 2 7; 1 7; 4 5; 3 5 |
| INTERMED | amount | 28 | 0 | 520.852 2; 370.07348 2; 280.00422 2; 815.9052 2 |
| SQ_MILES | amount | 28 | 0 | 1.8683 2; 1.32745 2; 1.00438 2; 2.92665 2 |
| CDMODELBLK | category | 2 | 12 | Yes 22 |
| LB_HOLD | category | 9 | 25 | Midland 2; Forgotten Triangle 1; Pershing & I-77 1; Bvr/55&W/Main/Midtn 1 |
| MB_HTF | category | 11 | 22 | 98 Great Homes 2; Marvin 2; Corlett 1; Bridgeport 1 |
| NPI_SII | category | 8 | 23 | Detroit-Shoreway 2; Fairfax Renaissance 2; Buckeye Area 2; Famicos 2 |
| TYPOLOGY | category | 11 | 1 | Stable/Transitional/Fragi 7; Stable/Transitional/Fragi 6; Regional Choice/Stable/Tr 5; Regional Choice/Stable 4 |
| GLOBALID | category | 34 | 0 | 412fbd6a-21da-40d7-8a8c-f 1; f922604c-6e40-4f40-a4a7-6 1; f3410fd8-407d-4c5d-a1e6-d 1; 4fdea8d0-6669-4b40-ba18-7 1 |
| SHAPE__AREA | amount | 34 | 0 | 30713829.336909294 1; 23251559.99279785 1; 26496558.295659065 1; 30305619.818725586 1 |
| SHAPE__LENGTH | amount | 33 | 0 | 25637.645975198408 1; 22324.03305746487 1; 24014.67270726368 1; 24144.04216109943 1 |
| GEOMETRY | category | 34 | 0 | {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:31:30.30993 34 |
| SOURCE_RUN_ID | audit | 1 | 0 | d5921ec7-f372-48b7-a468-6 34 |
| SRC_SHA256 | who | 1 | 0 | 735c00c718a20fc674ba875c3 34 |
