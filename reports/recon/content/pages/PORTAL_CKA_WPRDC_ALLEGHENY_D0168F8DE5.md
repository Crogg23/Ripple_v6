# PORTAL_CKA_WPRDC_ALLEGHENY_D0168F8DE5

rows 17  columns 13  scan 3.2s

roles: amount 1, audit 2, category 6, date 1, empty 2, other 1, who 1

## when

INGESTED_AT
  2026        17  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERIMETER | 17 | 6.8K | 113.4K | 332.3K | 349.5K | 1.96M |

## who

SRC_SHA256 by rows
        17  82bf7b3ab0ddfbbf15ee6e85385a919700572831d3f07aee638cdc3bbf47624c

SRC_SHA256 by dollars
       1.96M       17 rows  82bf7b3ab0ddfbbf15ee6e85385a919700572831d3f07aee638cdc3bbf47

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = PERIMETER
  82bf7b3ab0ddfbbf15ee6e85385a919700572831  2026:1.96M

## what

FID: 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%

POLY: 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%

SUBCLASS_2: 1 29%, 5 18%, 3 12%, 8 12%, 2 12%, 6 6%, 7 6%, 4 6%

BASIN: Upper Ohio/Allegheny/Monongahe 29%, Lower Ohio River 18%, Upper Allegheny River 12%, Shallow-Cut Monongahela River 12%, Lower Northern Allegheny River 12%, Saw Mill Run 6%, Thompson Run/Turtle Creek 6%, Chartiers Creek 6%

SYMBOL: 12 29%, 17 18%, 57 12%, 52 12%, 23 12%, 113 6%, 19 6%, 25 6%

DIRECTION: north 47%, south 29%, east 24%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 17 | 0 | 17 1; 16 1; 15 1; 14 1 |
| PERIMETER | amount | 17 | 0 | 124607.5 1; 40967.23 1; 138477.1 1; 32870.51 1 |
| POLY | category | 17 | 0 | 18 1; 17 1; 16 1; 15 1 |
| SUBCLASS | other | 1 | 0 | BASIN 17 |
| SUBCLASS_2 | category | 8 | 0 | 1 5; 5 3; 3 2; 8 2 |
| BASIN | category | 8 | 0 | Upper Ohio/Allegheny/Mono 5; Lower Ohio River 3; Upper Allegheny River 2; Shallow-Cut Monongahela R 2 |
| SYMBOL | category | 8 | 0 | 12 5; 17 3; 57 2; 52 2 |
| DIRECTION | category | 3 | 0 | north 8; south 5; east 4 |
| SHAPE_LENGTH | empty | 1 | 17 |  |
| SHAPE_AREA | empty | 1 | 17 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:15:27.93358 17 |
| SOURCE_RUN_ID | audit | 1 | 0 | e745c4f4-6f5f-4ce1-8be5-b 17 |
| SRC_SHA256 | who | 1 | 0 | 82bf7b3ab0ddfbbf15ee6e853 17 |
