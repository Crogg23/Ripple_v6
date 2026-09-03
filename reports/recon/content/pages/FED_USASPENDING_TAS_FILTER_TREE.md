# FED_USASPENDING_TAS_FILTER_TREE

rows 92  columns 8  scan 2.2s

roles: amount 1, audit 2, empty 1, other 3, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| COUNT | 92 | 1 | 16 | 1.2K | 1.9K | 12.1K |

## who

SRC_SHA256 by rows
        92  dae43a06ea6e2cb7631147acfcfcdd46be02e08cf09245da36fd1be5fb1eccc5

SRC_SHA256 by dollars
       12.1K       92 rows  dae43a06ea6e2cb7631147acfcfcdd46be02e08cf09245da36fd1be5fb1e

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 93 | 0 | 519 1; 1133 1; 510 1; 077 1 |
| ANCESTORS | other | 1 | 0 | [] 92 |
| DESCRIPTION | other | 93 | 0 | Vietnam Education Foundat 1; United States Trade and D 1; United States Chemical Sa 1; U.S. International Develo 1 |
| COUNT | amount | 48 | 0 | 1 11; 15 6; 17 5; 16 5 |
| CHILDREN | empty | 0 | 92 |  |
| INGESTED_AT | audit | 1 | 0 | 1786134054361016 92 |
| SOURCE_RUN_ID | audit | 1 | 0 | bf236731-80ee-4f50-8bda-6 92 |
| SRC_SHA256 | who | 1 | 0 | dae43a06ea6e2cb7631147acf 92 |
