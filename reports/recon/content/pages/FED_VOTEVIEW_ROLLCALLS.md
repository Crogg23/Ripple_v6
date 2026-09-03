# FED_VOTEVIEW_ROLLCALLS

rows 945.5K  columns 9  scan 2.5s

roles: amount 1, audit 2, category 3, other 3

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PROB | 854.0K | 0 | 100 | 100.00 | 100 | 80.81M |

## what

CONGRESS: 118 64%, 119 36%

CHAMBER: House 84%, Senate 16%

CAST_CODE: 1 56%, 6 40%, 9 4%, 7 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CONGRESS | category | 2 | 0 | 118 606.6K; 119 339.0K |
| CHAMBER | category | 2 | 0 | House 790.9K; Senate 154.6K |
| ROLLNUMBER | other | 1.2K | 0 | 324 3.0K; 326 3.0K; 325 3.0K; 330 3.0K |
| ICPSR | other | 639 | 0 | 21139 4.7K; 21140 4.7K; 21142 4.7K; 21167 4.7K |
| CAST_CODE | category | 4 | 0 | 1 527.9K; 6 382.8K; 9 34.4K; 7 480 |
| PROB | amount | 1.0K | 91.5K | 100.0 485.1K; 99.9 57.1K; 99.8 26.8K; 99.7 18.5K |
| _INGESTED_AT | audit | 1 | 0 | 1782772009785849 945.5K |
| _SOURCE_RUN_ID | audit | 1 | 0 | df8ca785-d502-4131-af09-2 945.5K |
| _SRC_SHA256 | other | 1 | 0 | baa0d2f1669143868be7b4c2c 945.5K |
