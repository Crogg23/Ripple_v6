# PORTAL_CKA_WPRDC_ALLEGHENY_9AED398C25

rows 4  columns 8  scan 3.6s

roles: amount 1, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026         4  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERIMETER | 4 | 0 | 973.6K | 973.6K | 973.6K | 2.92M |

## who

SRC_SHA256 by rows
         4  7bc285f92bdd17bf1d54cfb8c62cb2a57249901564ad219459c480f97dce7ab3

SRC_SHA256 by dollars
       2.92M        4 rows  7bc285f92bdd17bf1d54cfb8c62cb2a57249901564ad219459c480f97dce

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERIMETER
  7bc285f92bdd17bf1d54cfb8c62cb2a572499015  2026:2.92M

## what

FID: 4 25%, 3 25%, 2 25%, 1 25%

HYDRO_CODE: 450 75%, 0 25%

NAME: Ohio River 33%, Monongahela River 33%, Allegheny River 33%

GEOMETRY: POLYGON ((598796.5980922091985 25%, POLYGON ((583477.7547498161438 25%, POLYGON ((583477.7520151133649 25%, POLYGON ((583680.1773915961384 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 4 | 0 | 4 1; 3 1; 2 1; 1 1 |
| HYDRO_CODE | category | 2 | 0 | 450 3; 0 1 |
| NAME | category | 4 | 1 | Ohio River 1; Monongahela River 1; Allegheny River 1 |
| PERIMETER | amount | 2 | 0 | 973644.208746 3; 0.0 1 |
| GEOMETRY | category | 4 | 0 | POLYGON ((598796.59809220 1; POLYGON ((583477.75474981 1; POLYGON ((583477.75201511 1; POLYGON ((583680.17739159 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:46.68477 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | f91edbde-7fa2-4f5f-8ab9-0 4 |
| SRC_SHA256 | who | 1 | 0 | 7bc285f92bdd17bf1d54cfb8c 4 |
