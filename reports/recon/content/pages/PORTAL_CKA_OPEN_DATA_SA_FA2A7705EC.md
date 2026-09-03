# PORTAL_CKA_OPEN_DATA_SA_FA2A7705EC

rows 3  columns 8  scan 3.6s

roles: amount 3, audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026         3  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SQMI | 3 | 9.85 | 35.03 | 183.32 | 186.35 | 231.23 |
| SHAPE__AREA | 3 | 274.62M | 976.62M | 5.11B | 5.20B | 6.45B |
| SHAPE__LENGTH | 3 | 116.7K | 536.4K | 1.77M | 1.80M | 2.45M |

## who

SRC_SHA256 by rows
         3  9550824e423fdab1803a1d11311b1d4dbd171690af25538b2008d3b70a251223

SRC_SHA256 by dollars
      231.23        3 rows  9550824e423fdab1803a1d11311b1d4dbd171690af25538b2008d3b70a25

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SQMI
  9550824e423fdab1803a1d11311b1d4dbd171690  2026:231.23

## what

OBJECTID: 3 33%, 2 33%, 1 33%

TIER: Tier I 33%, Tier II 33%, Tier III 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 3 | 0 | 3 1; 2 1; 1 1 |
| TIER | category | 3 | 0 | Tier I 1; Tier II 1; Tier III 1 |
| SQMI | amount | 3 | 0 | 186.35325899 1; 35.03164358 1; 9.85082501 1 |
| SHAPE__AREA | amount | 3 | 0 | 5195209913.77734 1; 976622265.886719 1; 274624141.568359 1 |
| SHAPE__LENGTH | amount | 3 | 0 | 1798527.61816934 1; 536400.110922496 1; 116724.554594238 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:00.63310 3 |
| SOURCE_RUN_ID | audit | 1 | 0 | d1a5973d-f4f0-42cf-96fe-2 3 |
| SRC_SHA256 | who | 1 | 0 | 9550824e423fdab1803a1d113 3 |
