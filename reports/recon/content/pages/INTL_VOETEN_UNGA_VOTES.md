# INTL_VOETEN_UNGA_VOTES

rows 1.82M  columns 14  scan 6.9s

roles: amount 4, audit 2, id 1, other 7

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AGREE | 1.82M | 0 | 0.84 | 1 | 1 | 1.48M |
| IDEALPOINTFP_X | 1.82M | -3.55 | -0.20 | 2.33 | 3.23 | -44.9K |
| IDEALPOINTFP_Y | 1.82M | -3.55 | -0.20 | 2.33 | 3.23 | -44.9K |
| IDEALPOINTDISTANCE | 1.82M | 0 | 0.79 | 3.73 | 6.36 | 1.80M |

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COL_0 | id | 1.80M | 0 | 540672 2.7K; 540671 2.7K; 540670 2.7K; 540669 2.7K |
| SESSION_X | other | 78 | 0 | 74 37.1K; 73 37.1K; 72 37.1K; 71 37.1K |
| CCODE1 | other | 204 | 0 | 90 11.3K; 100 11.3K; 130 11.3K; 140 11.3K |
| CCODE2 | other | 204 | 0 | 2 11.3K; 20 11.3K; 40 11.3K; 70 11.3K |
| AGREE | amount | 19.6K | 0 | 1 25.2K; 0.75 15.6K; 0.833333333333333 9.9K; 0.875 9.6K |
| YEAR | other | 79 | 0 | 2019 37.1K; 2018 37.1K; 2017 37.1K; 2016 37.1K |
| IDEALPOINTFP_X | amount | 11.3K | 0 | -0.09389293 2.8K; -0.7154537 2.8K; -0.3027819 2.8K; 0.08356728 2.8K |
| NVOTESFP_X | other | 165 | 0 | 74 60.1K; 69 58.4K; 88 58.3K; 72 56.7K |
| IDEALPOINTFP_Y | amount | 11.3K | 0 | -0.1282441 2.7K; 0.5595163 2.7K; 0.4650167 2.7K; -0.1566431 2.7K |
| NVOTESFP_Y | other | 165 | 0 | 74 60.1K; 69 58.4K; 88 58.3K; 72 56.7K |
| IDEALPOINTDISTANCE | amount | 890.5K | 0 | 0.000534699999999999 2.7K; 0.5051496 2.7K; 0.5596959 2.7K; 0.1065942 2.7K |
| INGESTED_AT | audit | 1 | 0 | 1782616925610560 1.82M |
| SOURCE_RUN_ID | audit | 1 | 0 | a423a1b2-dfc2-4bc7-aaf5-7 1.82M |
| SRC_SHA256 | other | 1 | 0 | 81384b39e403718194967d384 1.82M |
