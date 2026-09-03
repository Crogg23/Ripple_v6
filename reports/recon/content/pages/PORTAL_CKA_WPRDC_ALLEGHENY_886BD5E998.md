# PORTAL_CKA_WPRDC_ALLEGHENY_886BD5E998

rows 10.0K  columns 15  scan 2.7s

roles: audit 2, category 3, date 1, id 4, other 4, who 2

## when

INGESTED_AT
  2026     10.0K  ##############################

## who

TRACTCE by rows
        35  000300
        34  011400
        34  010400
        33  010100
        33  010500
        32  000500
        32  010800
        30  011200
        28  000100
        27  010700
        27  000200
        27  011500
        27  011000
        25  011300
        25  011600
        25  011900
        24  010900
        24  000800
        23  950200
        23  000600

SRC_SHA256 by rows
     10.0K  c5b4154440d9564bb375873d38983ddc3d535917efaa2f68232dd58ac535a39f

## who x when

TRACTCE by INGESTED_AT  LOAD STAMP, not an event date
  000100                                    2026:28
  000200                                    2026:27
  000300                                    2026:35
  000500                                    2026:32
  000600                                    2026:23
  000800                                    2026:24
  010100                                    2026:33
  010400                                    2026:34
  010500                                    2026:33
  010700                                    2026:27
  010800                                    2026:32
  010900                                    2026:24
  011000                                    2026:27
  011200                                    2026:30
  011300                                    2026:25
  011400                                    2026:34
  011500                                    2026:27
  011600                                    2026:25
  011900                                    2026:25
  950200                                    2026:23

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  c5b4154440d9564bb375873d38983ddc3d535917  2026:10.0K

## what

BLKGRPCE: 1 34%, 2 32%, 3 21%, 4 10%, 5 3%, 6 1%, 7 0%, 8 0%, 0 0%

NAMELSAD: Block Group 1 34%, Block Group 2 32%, Block Group 3 21%, Block Group 4 10%, Block Group 5 3%, Block Group 6 1%, Block Group 7 0%, Block Group 8 0%, Block Group 0 0%

NAME: 1 34%, 2 32%, 3 21%, 4 10%, 5 3%, 6 1%, 7 0%, 8 0%, 0 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BLKGRPCE | category | 9 | 0 | 1 3.4K; 2 3.2K; 3 2.1K; 4 963 |
| ALAND | id | 10.2K | 0 | 75579241 50; 264795 50; 30606 50; 50034347 50 |
| AWATER | other | 4.1K | 0 | 0 5.8K; 1957533 22; 13595 22; 305238 22 |
| GEOID | id | 9.9K | 0 | 421150324012 50; 420454106013 50; 421010125023 50; 421239712001 50 |
| STATEFP | other | 1 | 0 | 42 10.0K |
| NAMELSAD | category | 9 | 0 | Block Group 1 3.4K; Block Group 2 3.2K; Block Group 3 2.1K; Block Group 4 963 |
| LSAD | other | 1 | 0 | BG 10.0K |
| TRACTCE | who | 2.6K | 0 | 971200 51; 010802 51; 012800 51; 014102 51 |
| COUNTYFP | other | 68 | 0 | 101 1.3K; 003 1.1K; 091 616; 017 420 |
| AFFGEOID | id | 10.0K | 0 | 1500000US421150324012 50; 1500000US420454106013 50; 1500000US421010125023 50; 1500000US421239712001 50 |
| NAME | category | 9 | 0 | 1 3.4K; 2 3.2K; 3 2.1K; 4 963 |
| DATASPATIAL_WKB | id | 10.2K | 0 | \x00000000030000000100000 50; \x00000000030000000100000 50; \x00000000030000000100000 50; \x00000000030000000100000 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:22:38.73112 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 273acd75-631c-48c3-83bd-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | c5b4154440d9564bb375873d3 10.0K |
