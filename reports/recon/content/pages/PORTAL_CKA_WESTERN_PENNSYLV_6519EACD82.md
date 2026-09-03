# PORTAL_CKA_WESTERN_PENNSYLV_6519EACD82

rows 179  columns 7  scan 2.1s

roles: audit 2, category 1, date 1, empty 1, other 2, who 1

## when

INGESTED_AT
  2026       179  ##############################

## who

SRC_SHA256 by rows
       179  011abdb5df05173a414edadada8e36eb39c7aa9efd7c9fc3dedcf36b9ee1a78f

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  011abdb5df05173a414edadada8e36eb39c7aa9e  2026:179

## what

TIF_NAME: CENTER TRIANGLE - LAZARUS 38%, SOUTH SIDE WORKS 16%, FIFTH & MARKET 16%, STATION SQUARE 7%, FEDERAL NORTH 7%, PITTSBURGH TECHNOLOGY CENTER 6%, PENN LIBERTY PLAZA 3%, MELLON CLIENT SERVICE CENTER 2%, FULTON BUILDING 2%, CENTER NEGLEY 2%, ROBINSON MALL AND PERIPHERAL D 1%, HOME DEPOT 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 180 | 0 | 179 1; 178 1; 177 1; 176 1 |
| MAP_BLOCK_LOT | other | 180 | 0 | 9-L-17 1; 9-L-31 1; 9-K-97 1; 29-J-227 1 |
| TIF_NAME | category | 15 | 0 | CENTER TRIANGLE - LAZARUS 67; SOUTH SIDE WORKS 29; FIFTH & MARKET 28; STATION SQUARE 12 |
| NOTES | empty | 1 | 179 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:16:57.54779 179 |
| SOURCE_RUN_ID | audit | 1 | 0 | b134d452-13e9-42ec-84c4-c 179 |
| SRC_SHA256 | who | 1 | 0 | 011abdb5df05173a414edadad 179 |
