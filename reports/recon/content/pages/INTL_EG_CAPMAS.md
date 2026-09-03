# INTL_EG_CAPMAS

rows 150  columns 10  scan 1.8s

roles: audit 2, category 1, empty 4, other 1, who 2

## who

SOURCE by rows
        50  https://egypt.opendataforafrica.org/sys/login/signup?lang=en&host=egyp
        50  /apps/data-catalog
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage
         1  https://egypt.opendataforafrica.org/sys/login?returnUrl=%2Fdata%3Fpage

_SRC_SHA256 by rows
       150  4f0bb7f4fb4eb888d0ba0e594d6ce7e9a49842e3b4374636bba1f2a5527fb109

## what

INDICATOR_NAME: Data Catalog 33%, Sign Up 33%, Login 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDICATOR_NAME | category | 3 | 0 | Data Catalog 50; Sign Up 50; Login 50 |
| CATEGORY | empty | 1 | 150 |  |
| YEAR | empty | 1 | 150 |  |
| VALUE | empty | 1 | 150 |  |
| UNIT | empty | 1 | 150 |  |
| SOURCE | who | 52 | 0 | /apps/data-catalog 50; https://egypt.opendatafor 50; https://egypt.opendatafor 1; https://egypt.opendatafor 1 |
| COUNTRY | other | 1 | 0 | Egypt 150 |
| _INGESTED_AT | audit | 1 | 0 | 1783020290739160 150 |
| _SOURCE_RUN_ID | audit | 1 | 0 | d453673d-8375-4b8b-9674-c 150 |
| _SRC_SHA256 | who | 1 | 0 | 4f0bb7f4fb4eb888d0ba0e594 150 |
