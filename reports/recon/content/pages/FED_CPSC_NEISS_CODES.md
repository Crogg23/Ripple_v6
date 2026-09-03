# FED_CPSC_NEISS_CODES

rows 1.2K  columns 7  scan 2.2s

roles: amount 2, audit 2, category 1, id 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| STARTING_VALUE_FOR_FORMAT | 1.2K | 0 | 1.3K | 5.3K | 10.0K | 1.94M |
| ENDING_VALUE_FOR_FORMAT | 1.2K | 0 | 1.3K | 5.3K | 10.0K | 1.94M |

## who

_SRC_SHA256 by rows
      1.2K  55ded646da4b25137d2b2315d89c7a6641c06d0301c469157561531f7379da81

_SRC_SHA256 by dollars
       1.94M     1.2K rows  55ded646da4b25137d2b2315d89c7a6641c06d0301c469157561531f7379

## what

FORMAT_NAME: PROD 90%, DIAG 2%, BDYPT 2%, AGELTTWO 2%, LOC 1%, DISP 1%, RACE 1%, FIRE 0%, HISP 0%, SEX 0%, ALC_DRUG 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FORMAT_NAME | category | 11 | 0 | PROD 1.1K; DIAG 31; BDYPT 30; AGELTTWO 25 |
| STARTING_VALUE_FOR_FORMAT | amount | 1.2K | 0 | 0 9; 2 8; 1 8; 6 7 |
| ENDING_VALUE_FOR_FORMAT | amount | 1.2K | 0 | 0 9; 2 8; 1 8; 6 7 |
| FORMAT_VALUE_LABEL | id | 1.3K | 0 | FEMALE 7; MALE 7; UNKNOWN 7; NATIVE HAWAIIAN/PACIFIC I 7 |
| _INGESTED_AT | audit | 1 | 0 | 1787435728986819 1.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | fcde35a8-6c56-4191-95b9-1 1.2K |
| _SRC_SHA256 | who | 1 | 0 | 55ded646da4b25137d2b2315d 1.2K |
