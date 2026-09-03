# PORTAL_CKA_OPEN_DATA_SA_AFE18E40AF

rows 27  columns 8  scan 3.2s

roles: amount 3, audit 2, category 2, date 1, who 1

## when

INGESTED_AT
  2026        27  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 27 | 9.41 | 2.7K | 96.8K | 97.7K | 327.3K |
| SHAPE__AREA | 27 | 50.4K | 14.41M | 521.10M | 526.33M | 1.76B |
| SHAPE__LENGTH | 27 | 1.0K | 33.7K | 318.3K | 321.9K | 2.27M |

## who

SRC_SHA256 by rows
        27  ccec16fa3e00f949d3164457e66b4f3954995eacaf9b1bdd8a3774d2d418866a

SRC_SHA256 by dollars
      327.3K       27 rows  ccec16fa3e00f949d3164457e66b4f3954995eacaf9b1bdd8a3774d2d418

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = ACRES
  ccec16fa3e00f949d3164457e66b4f3954995eac  2026:327.3K

## what

OBJECTID: 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%

NAME: Comal 8%, Schertz 8%, Converse 8%, Elmendorf 8%, Helotes 8%, Boerne 8%, Fair Oaks 8%, St. Hedwig 8%, Garden Ridge 8%, Santa Clara 8%, Lytle 8%, New Braunfels 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 27 | 0 | 27 1; 26 1; 25 1; 24 1 |
| NAME | category | 27 | 0 | Comal 1; Schertz 1; Converse 1; Elmendorf 1 |
| ACRES | amount | 27 | 0 | 302.15 1; 8384.89470112 1; 889.33276396 1; 786.02552765 1 |
| SHAPE__AREA | amount | 27 | 0 | 1628911.30078125 1; 45039917.2148438 1; 4794661.5703125 1; 4194222.15234375 1 |
| SHAPE__LENGTH | amount | 27 | 0 | 6358.72932430101 1; 158784.61759319 1; 15638.594463775 1; 26227.1193869038 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:19:00.94153 27 |
| SOURCE_RUN_ID | audit | 1 | 0 | bf32d47e-7ed4-4130-b1c3-c 27 |
| SRC_SHA256 | who | 1 | 0 | ccec16fa3e00f949d3164457e 27 |
