# FED_BJS_DATA

rows 1.0K  columns 40  scan 3.6s

roles: amount 3, audit 2, category 24, other 10, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| YEARQ | 1.0K | 2.0K | 2.0K | 2.0K | 2.0K | 1.99M |
| WGTVICCY | 1.0K | 2.0K | 4.6K | 11.0K | 38.0K | 4.92M |
| NEWWGT | 1.0K | 2.0K | 4.7K | 48.5K | 68.3K | 6.83M |

## who

_SRC_SHA256 by rows
      1.0K  3223dcf72493dd1e4ea7bde534bbc02cc5b50f6aedcd18b7aa85aac7673da6d4

_SRC_SHA256 by dollars
       1.99M     1.0K rows  3223dcf72493dd1e4ea7bde534bbc02cc5b50f6aedcd18b7aa85aac7673d

## what

AGER: 1 25%, 4 24%, 3 22%, 2 21%, 5 5%, 6 3%

SEX: 1 56%, 2 44%

HISPANIC: 2 91%, 1 8%, 98 0%

RACE: 1 82%, 2 16%, 3 2%, 4 1%

RACE_ETHNICITY: 1 74%, 2 16%, 6 8%, 3 2%, 4 1%

HINCOME1: 3 16%, 2 16%, 1 15%, 4 15%, 5 14%, 6 11%, 7 7%, 98 6%

MARITAL: 1 53%, 2 26%, 4 13%, 5 7%, 3 2%, 98 0%

MSA: 2 47%, 1 36%, 3 17%

EDUCATN1: 4 45%, 5 33%, 3 18%, 98 3%, 2 2%, 1 0%

NEWCRIME: 1 96%, 2 4%

NEWOFF: 4 57%, 3 23%, 2 10%, 1 5%, 5 4%

SERIOUSVIOLENT: 2 57%, 1 39%, 3 4%

NOTIFY: 2 55%, 1 44%, 3 1%, 98 0%

VICSERVICES: 2 94%, 1 6%, 98 0%, 3 0%

LOCATIONR: 3 44%, 1 24%, 4 13%, 5 11%, 2 9%

DIREL: 4 50%, 3 32%, 1 9%, 2 5%, 6 2%, 5 2%

WEAPON: 2 63%, 1 29%, 3 8%

WEAPCAT: 0 63%, 1 11%, 3 9%, 5 8%, 2 8%, 4 2%

INJURY: 0 76%, 1 24%

SERIOUS: 1 76%, 3 19%, 2 4%, 4 1%

TREATMENT: 0 76%, 1 13%, 2 11%

OFFENDERAGE: 3 37%, 4 28%, 2 20%, 5 8%, 98 6%, 1 1%

OFFENDERSEX: 1 82%, 2 14%, 4 3%, 3 2%, 98 0%

SERIES: 1 94%, 2 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| IDPER | other | 816 | 0 | 1658823195869999999999241 9; 1658823195579999999999241 8; 1657649103209999999999143 7; 1642495471589999999999162 7 |
| YEARQ | amount | 2 | 0 | 1993.1 589; 1993.2 411 |
| YEAR | other | 1 | 0 | 1993 1.0K |
| AGER | category | 6 | 0 | 1 253; 4 241; 3 217; 2 212 |
| SEX | category | 2 | 0 | 1 565; 2 435 |
| HISPANIC | category | 3 | 0 | 2 913; 1 84; 98 3 |
| RACE | category | 4 | 0 | 1 815; 2 158; 3 17; 4 10 |
| RACE_ETHNICITY | category | 5 | 0 | 1 737; 2 156; 6 84; 3 15 |
| HINCOME1 | category | 8 | 0 | 3 165; 2 156; 1 153; 4 150 |
| HINCOME2 | other | 1 | 0 | -1 1.0K |
| MARITAL | category | 6 | 0 | 1 527; 2 259; 4 127; 5 71 |
| POPSIZE | other | 1 | 0 | -1 1.0K |
| REGION | other | 1 | 0 | -1 1.0K |
| MSA | category | 3 | 0 | 2 467; 1 365; 3 168 |
| LOCALITY | other | 1 | 0 | -1 1.0K |
| EDUCATN1 | category | 6 | 0 | 4 448; 5 329; 3 175; 98 27 |
| EDUCATN2 | other | 1 | 0 | -1 1.0K |
| VETERAN | other | 1 | 0 | -2 1.0K |
| CITIZEN | other | 1 | 0 | -1 1.0K |
| NEWCRIME | category | 2 | 0 | 1 958; 2 42 |
| NEWOFF | category | 5 | 0 | 4 570; 3 229; 2 105; 1 54 |
| SERIOUSVIOLENT | category | 3 | 0 | 2 570; 1 388; 3 42 |
| NOTIFY | category | 4 | 0 | 2 553; 1 435; 3 11; 98 1 |
| VICSERVICES | category | 4 | 0 | 2 940; 1 57; 98 2; 3 1 |
| LOCATIONR | category | 5 | 0 | 3 438; 1 237; 4 129; 5 109 |
| DIREL | category | 6 | 0 | 4 497; 3 325; 1 88; 2 51 |
| WEAPON | category | 3 | 0 | 2 627; 1 290; 3 83 |
| WEAPCAT | category | 6 | 0 | 0 627; 1 106; 3 90; 5 83 |
| INJURY | category | 2 | 0 | 0 760; 1 240 |
| SERIOUS | category | 4 | 0 | 1 760; 3 192; 2 36; 4 12 |
| TREATMENT | category | 3 | 0 | 0 760; 1 130; 2 110 |
| OFFENDERAGE | category | 6 | 0 | 3 367; 4 282; 2 199; 5 77 |
| OFFENDERSEX | category | 5 | 0 | 1 815; 2 136; 4 31; 3 16 |
| OFFTRACENEW | other | 1 | 0 | -1 1.0K |
| WGTVICCY | amount | 804 | 0 | 4809.58205 13; 3181.39236 7; 4991.56543 7; 3355.87598 7 |
| SERIES | category | 2 | 0 | 1 941; 2 59 |
| NEWWGT | amount | 811 | 0 | 4809.58205 13; 3181.39236 7; 4991.56543 7; 3355.87598 7 |
| _INGESTED_AT | audit | 1 | 0 | 1783285013647483 1.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | f96e64fc-bbb5-44e9-973d-b 1.0K |
| _SRC_SHA256 | who | 1 | 0 | 3223dcf72493dd1e4ea7bde53 1.0K |
