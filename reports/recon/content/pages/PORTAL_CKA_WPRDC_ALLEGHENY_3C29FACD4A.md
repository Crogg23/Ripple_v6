# PORTAL_CKA_WPRDC_ALLEGHENY_3C29FACD4A

rows 2  columns 21  scan 3.9s

roles: amount 5, audit 2, category 6, date 1, empty 2, other 3, who 3

## when

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREA | 2 | 299.89 | 598.90 | 891.94 | 897.92 | 1.2K |
| F_18_AP_BL | 2 | 0.05 | 0.12 | 0.18 | 0.18 | 0.23 |
| F_NH18_WHT | 2 | 0.77 | 0.84 | 0.91 | 0.91 | 1.68 |
| SHAPE_LENGTH | 2 | 2.45 | 2.52 | 2.60 | 2.60 | 5.05 |
| SHAPE_AREA | 2 | 0.08 | 0.10 | 0.12 | 0.12 | 0.20 |

## who

POPULATION by rows
         2  705688

POPULATION by dollars
        1.2K        2 rows  705688

IDEAL_VALU by rows
         2  705688

IDEAL_VALU by dollars
        1.2K        2 rows  705688

SRC_SHA256 by rows
         2  2bf303dff4b3f3851304a68a89bf0d50297b97da92a986af4dab44cc15ba7561

SRC_SHA256 by dollars
        1.2K        2 rows  2bf303dff4b3f3851304a68a89bf0d50297b97da92a986af4dab44cc15ba

## who x when

POPULATION by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREA
  705688                                    2026:1.2K

IDEAL_VALU by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREA
  705688                                    2026:1.2K

## what

FID: 5 50%, 4 50%

ID: 16 50%, 15 50%

DISTRICT: 18 50%, 17 50%

F18_POP: 573418 50%, 556858 50%

F18_AP_BLK: 100919 50%, 29547 50%

NH18_WHT: 443692 50%, 508040 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 2 | 0 | 5 1; 4 1 |
| ID | category | 2 | 0 | 16 1; 15 1 |
| AREA | amount | 2 | 0 | 299.887604 1; 897.920532 1 |
| DISTRICT | category | 2 | 0 | 18 1; 17 1 |
| MEMBERS | other | 1 | 0 | 1 2 |
| LOCKED | empty | 1 | 2 |  |
| NAME | empty | 1 | 2 |  |
| POPULATION | who | 1 | 0 | 705688 2 |
| F18_POP | category | 2 | 0 | 573418 1; 556858 1 |
| F18_AP_BLK | category | 2 | 0 | 100919 1; 29547 1 |
| NH18_WHT | category | 2 | 0 | 443692 1; 508040 1 |
| IDEAL_VALU | who | 1 | 0 | 705688 2 |
| DEVIATION | other | 1 | 0 | 0 2 |
| F_DEVIATIO | other | 1 | 0 | 0 2 |
| F_18_AP_BL | amount | 2 | 0 | 0.175996 1; 0.05306 1 |
| F_NH18_WHT | amount | 2 | 0 | 0.773767 1; 0.912333 1 |
| SHAPE_LENGTH | amount | 2 | 0 | 2.44533152319432 1; 2.60180098500331 1 |
| SHAPE_AREA | amount | 2 | 0 | 0.082347528019924 1; 0.122153796696682 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:08:32.97013 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | bcc7af80-64db-40d6-91cc-3 2 |
| SRC_SHA256 | who | 1 | 0 | 2bf303dff4b3f3851304a68a8 2 |
