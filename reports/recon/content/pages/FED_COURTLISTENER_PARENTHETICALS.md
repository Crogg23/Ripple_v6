# FED_COURTLISTENER_PARENTHETICALS

rows 6.41M  columns 9  scan 4.2s

roles: amount 1, audit 2, date 1, id 1, other 5

## when

_INGESTED_AT
  2026     6.41M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 6.41M | 0 | 0.50 | 0.92 | 1 | 3.71M |

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 6.32M | 0 | 6683097 4.3K; 7959891 4.3K; 8193392 4.3K; 9047895 4.3K |
| TEXT | other | 5.09M | 0 | holding that an appellant 4.5K; holding that appellant de 4.4K; “Threadbare recitals of t 4.4K; petitioner has burden of  4.3K |
| SCORE | amount | 53.6K | 0 | 0.5 889.3K; 0.7 348.8K; 0.8 293.8K; 0.9 173.4K |
| DESCRIBED_OPINION_ID | other | 1.22M | 0 | 9435339 17.3K; 9430599 13.4K; 9430664 12.4K; 9422386 8.7K |
| DESCRIBING_OPINION_ID | other | 1.87M | 0 | 11155014 4.3K; 11187980 4.3K; 11318542 4.3K; 11158796 4.3K |
| GROUP_ID | other | 3.70M | 6.2K | 147101061 16.7K; 147096435 13.3K; 146955660 12.3K; 146706970 8.7K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 01:55:15.710 6.41M |
| _SOURCE_RUN_ID | audit | 1 | 0 | c601b68f-a1bc-4f06-8690-b 6.41M |
| _SRC_SHA256 | other | 1 | 0 | 95e66c5601aba9da8befb0cc1 6.41M |
