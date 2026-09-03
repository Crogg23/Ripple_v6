# FED_FOREIGNASSISTANCE

rows 95.7K  columns 13  scan 1.8s

roles: audit 2, category 3, empty 5, other 2, who 1

## who

_SRC_SHA256 by rows
     95.7K  bb599147f88b9428518ff4a0c343652ca886c29e8adcda67a494b99715f8fe22

## what

MANAGING_AGENCY: 1 27%, 2 17%, 7 17%, 16 8%, 6 6%, 5 5%, 9 4%, 13 4%, 17 3%, 4 3%, 18 2%, 10 2%

FUNDING_AGENCY: 2 30%, 1 21%, 5 13%, 7 8%, 16 7%, 9 4%, 13 4%, 6 4%, 17 3%, 4 3%, 3 2%, 18 2%

TRANSACTION_TYPE: 2 60%, 3 40%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTRY | other | 259 | 0 | 1002 1.5K; 404 1.1K; 608 1.1K; 604 1.1K |
| MANAGING_AGENCY | category | 29 | 0 | 1 23.5K; 2 15.1K; 7 14.9K; 16 7.0K |
| FUNDING_AGENCY | category | 30 | 0 | 2 26.3K; 1 18.8K; 5 11.0K; 7 7.3K |
| USG_SECTOR | empty | 1 | 95.7K |  |
| DAC_CATEGORY | empty | 1 | 95.7K |  |
| OBLIGATION_AMOUNT | empty | 1 | 95.7K |  |
| DISBURSEMENT_AMOUNT | empty | 1 | 95.7K |  |
| FISCAL_YEAR | other | 83 | 0 | 2010 3.8K; 2009 3.6K; 2011 3.6K; 2012 3.5K |
| EIN | empty | 1 | 95.7K |  |
| TRANSACTION_TYPE | category | 2 | 0 | 2 57.2K; 3 38.4K |
| _INGESTED_AT | audit | 1 | 0 | 1783008610800015 95.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | a99494b4-9369-42e7-b3ee-e 95.7K |
| _SRC_SHA256 | who | 1 | 0 | bb599147f88b9428518ff4a0c 95.7K |
