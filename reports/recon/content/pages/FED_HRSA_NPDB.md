# FED_HRSA_NPDB

rows 1.91M  columns 57  scan 4.6s

roles: amount 3, audit 2, category 26, empty 2, id 1, other 20, state 3

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYMENT | 532.7K | 50 | 105.0K | 1.95M | 37.50M | 137.80B |
| TOTALPMT | 282.0K | 50 | 165.0K | 2.28M | 105.00M | 94.86B |
| AALENGTH | 249.2K | 0 | 2 | 15.00 | 99 | 656.2K |

## where

WORKSTAT: CA 87.4K, NY 72.8K, TX 62.6K, FL 54.2K, PA 46.3K, WA 36.0K, MI 31.3K, NJ 30.6K, IL 28.8K, OH 27.4K, VA 20.9K, NC 20.6K

HOMESTAT: TX 131.0K, CA 109.1K, FL 80.7K, NY 61.4K, OH 60.5K, PA 48.4K, MI 46.8K, IL 46.0K, WA 41.3K, AZ 41.1K, LA 39.1K, NJ 38.8K

LICNSTAT: CA 165.4K, TX 164.1K, NY 111.9K, FL 106.3K, PA 83.5K, OH 75.8K, MI 65.3K, IL 59.8K, NJ 52.2K, VA 51.7K, AZ 48.6K, WA 47.2K

## what

RECTYPE: C 69%, P 15%, M 13%, A 3%

REPTYPE: 302 54%, 101 24%, 702 6%, 102 4%, 1302 3%, 301 2%, 703 2%, 604 2%, 402 1%, 1604 1%, 451 1%, 401 0%

ORIGYEAR: 2010 10%, 2011 9%, 2016 9%, 2015 9%, 2019 8%, 2012 8%, 2018 8%, 2017 8%, 2013 8%, 2014 8%, 2025 7%, 2008 7%

PRACTAGE: 40 30%, 50 24%, 30 23%, 60 12%, 20 7%, 70 3%, 80 1%, 10 0%

GRAD: 1990 22%, 2000 19%, 1980 19%, 1970 15%, 2010 12%, 1960 7%, 1950 3%, 2020 2%, 1940 1%, 1910 0%, 1930 0%, 1920 0%

ALGNNATR: 1 28%, 60 28%, 20 24%, 50 7%, 30 5%, 10 3%, 70 2%, 90 2%, 80 1%, 100 0%, 40 0%

OUTCOME: 9 28%, 3 15%, 6 14%, 5 12%, 4 11%, 7 10%, 8 4%, 2 3%, 1 2%, 10 1%

PAYNUMBR: S 95%, M 5%, U 0%

NUMBPRSN: 0 73%, 1 24%, 2 2%, 3 1%, 4 0%, 5 0%, 6 0%, 7 0%, 8 0%, 10 0%, 11 0%, 9 0%

PAYTYPE: S 90%, U 7%, J 3%, B 1%, O 0%

PYRRLTNS: 1 49%, P 36%, S 5%, 3 4%, O 2%, 4 2%, E 1%, 2 1%, G 0%, M 0%

PTAGE: 50 19%, 40 18%, 60 15%, 30 14%, 20 9%, 70 8%, 0 5%, 10 4%, 80 3%, 1 3%, -1 2%, 90 0%

PTSEX: F 56%, M 43%, U 0%

PTTYPE: O 48%, I 38%, B 7%, U 7%

AACLASS5: 1199 48%, 1140 20%, 1125 8%, 1173 7%, 1297 7%, 1296 2%, 1280 2%, 1179 1%, 1282 1%, 1135 1%, 1696 1%, 1295 1%

AALENTYP: I 61%, S 22%, P 17%

AASIGYR: 2010 13%, 2011 9%, 2016 9%, 2018 8%, 2015 8%, 2019 8%, 2012 8%, 2013 8%, 2017 7%, 2014 7%, 2025 7%, 2021 7%

ACCRRPTS: 0 100%, 1 0%

NPLICRPT: 0 30%, 1 22%, 2 20%, 3 9%, 4 7%, 5 4%, 6 3%, 7 2%, 8 1%, 9 1%, 10 1%, 11 0%

NPCLPRPT: 0 95%, 1 3%, 2 1%, 3 0%, 4 0%, 5 0%, 6 0%, 7 0%, 8 0%, 9 0%, 10 0%, 11 0%

NPPSMRPT: 0 99%, 1 0%, 2 0%, 3 0%, 4 0%, 5 0%

NPDEARPT: 0 98%, 1 2%, 2 0%, 3 0%, 4 0%, 5 0%, 6 0%, 9 0%, 12 0%, 13 0%, 8 0%, 7 0%

NPEXCRPT: 0 83%, 1 9%, 2 5%, 3 1%, 4 1%, 5 0%, 6 0%, 7 0%, 8 0%, 10 0%, 9 0%, 11 0%

NPGARPT: 0 96%, 1 3%, 2 1%, 3 0%, 4 0%, 5 0%, 6 0%, 7 0%, 11 0%, 8 0%

NPCTMRPT: 0 97%, 1 2%, 2 0%, 3 0%, 4 0%, 5 0%, 6 0%, 8 0%

FUNDPYMT: 0 96%, 1 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SEQNO | id | 1.91M | 0 | 467419 1.8K; 467418 1.8K; 467417 1.8K; 467416 1.8K |
| RECTYPE | category | 4 | 0 | C 1.33M; P 282.0K; M 250.7K; A 50.6K |
| REPTYPE | category | 22 | 0 | 302 1.03M; 101 449.7K; 702 113.3K; 102 83.0K |
| ORIGYEAR | category | 37 | 0 | 2010 92.7K; 2011 85.8K; 2016 83.1K; 2015 79.2K |
| WORKSTAT | state | 61 | 1.09M | CA 87.4K; NY 72.8K; TX 62.6K; FL 54.2K |
| WORKCTRY | empty | 0 | 1.91M |  |
| HOMESTAT | state | 61 | 552.0K | TX 131.0K; CA 109.1K; FL 80.7K; NY 61.4K |
| HOMECTRY | empty | 0 | 1.91M |  |
| LICNSTAT | state | 58 | 160.5K | CA 165.4K; TX 164.1K; NY 111.9K; FL 106.3K |
| LICNFELD | other | 163 | 0 | 10 571.9K; 100 349.3K; 140 203.7K; 30 113.1K |
| PRACTAGE | category | 8 | 81.5K | 40 546.4K; 50 439.9K; 30 429.8K; 60 223.2K |
| GRAD | category | 13 | 270.9K | 1990 354.1K; 2000 318.5K; 1980 317.2K; 1970 240.4K |
| ALGNNATR | category | 11 | 1.38M | 1 148.1K; 60 147.0K; 20 127.3K; 50 35.1K |
| ALEGATN1 | other | 91 | 1.38M | 101 87.2K; 999 85.3K; 306 80.5K; 305 37.3K |
| ALEGATN2 | other | 91 | 1.84M | 999 8.9K; 113 7.6K; 305 6.7K; 202 5.8K |
| OUTCOME | category | 10 | 1.63M | 9 78.5K; 3 42.1K; 6 38.5K; 5 34.9K |
| MALYEAR1 | other | 113 | 1.38M | 1994 19.2K; 1997 18.9K; 1995 18.8K; 1998 18.7K |
| MALYEAR2 | other | 82 | 1.82M | 1994 6.1K; 1993 5.7K; 1995 5.3K; 1992 5.1K |
| PAYMENT | amount | 218 | 1.38M | $97500 23.8K; $195000 23.1K; $22500 20.2K; $47500 19.9K |
| TOTALPMT | amount | 220 | 1.63M | $495000 14.7K; $245000 12.7K; $97500 12.0K; $195000 11.6K |
| PAYNUMBR | category | 3 | 1.38M | S 505.0K; M 27.6K; U 108 |
| NUMBPRSN | category | 30 | 12.8K | 0 1.38M; 1 463.2K; 2 39.0K; 3 10.3K |
| PAYTYPE | category | 5 | 1.38M | S 478.5K; U 36.3K; J 14.5K; B 3.2K |
| PYRRLTNS | category | 10 | 1.38M | 1 260.7K; P 189.1K; S 27.4K; 3 21.8K |
| PTAGE | category | 12 | 1.64M | 50 52.8K; 40 48.4K; 60 40.9K; 30 38.5K |
| PTSEX | category | 3 | 1.63M | F 159.0K; M 122.0K; U 1.0K |
| PTTYPE | category | 4 | 1.63M | O 134.2K; I 107.5K; B 20.9K; U 19.5K |
| AAYEAR | other | 55 | 532.7K | 2016 61.5K; 2019 61.3K; 2017 61.0K; 2015 59.7K |
| AACLASS1 | other | 210 | 532.7K | 1125 168.8K; 1135 153.8K; 1280 142.6K; 1140 104.9K |
| AACLASS2 | other | 152 | 1.70M | 1173 71.4K; 1199 32.6K; 1140 27.4K; 1125 18.1K |
| AACLASS3 | other | 87 | 1.87M | 1173 14.3K; 1199 7.0K; 1140 5.9K; 1125 2.7K |
| AACLASS4 | other | 59 | 1.91M | 1199 1.2K; 1173 848; 1140 773; 1125 282 |
| AACLASS5 | category | 28 | 1.91M | 1199 202; 1140 82; 1125 35; 1173 31 |
| BASISCD1 | other | 134 | 556.1K | 0 318.3K; 39 113.3K; 99 107.5K; 19 105.3K |
| BASISCD2 | other | 131 | 1.36M | 0 305.3K; F2 19.2K; 99 18.0K; A6 18.0K |
| BASISCD3 | other | 120 | 1.52M | 0 305.3K; F6 8.8K; F2 7.8K; 99 7.1K |
| BASISCD4 | other | 115 | 1.57M | 0 305.3K; F6 4.3K; H6 3.2K; 99 2.8K |
| BASISCD5 | other | 95 | 1.59M | 0 305.3K; H6 2.5K; F6 1.5K; 99 1.2K |
| AALENTYP | category | 3 | 771.6K | I 698.1K; S 249.2K; P 192.2K |
| AALENGTH | amount | 915 | 1.66M | 5.00 44.8K; 1.00 40.9K; 2.00 38.8K; 3.00 36.3K |
| AAEFYEAR | other | 80 | 532.7K | 2016 61.5K; 2019 61.5K; 2017 60.9K; 2015 59.7K |
| AASIGYR | category | 47 | 606.4K | 2010 103.4K; 2011 75.7K; 2016 73.3K; 2018 69.5K |
| TYPE | other | 90 | 0 | 300 898.3K; 500 320.9K; 16 119.6K; 95 114.7K |
| PRACTNUM | other | 978.3K | 0 | 197286 1.9K; 6268 1.8K; 105484 1.8K; 131299 1.8K |
| ACCRRPTS | category | 2 | 0 | 0 1.91M; 1 48 |
| NPMALRPT | other | 83 | 0 | 0 1.25M; 1 285.0K; 2 149.9K; 3 78.5K |
| NPLICRPT | category | 46 | 0 | 0 571.8K; 1 419.7K; 2 386.0K; 3 178.3K |
| NPCLPRPT | category | 18 | 0 | 0 1.81M; 1 59.6K; 2 26.3K; 3 9.0K |
| NPPSMRPT | category | 6 | 0 | 0 1.90M; 1 7.6K; 2 2.5K; 3 334 |
| NPDEARPT | category | 14 | 0 | 0 1.86M; 1 42.5K; 2 3.7K; 3 653 |
| NPEXCRPT | category | 15 | 0 | 0 1.58M; 1 180.4K; 2 99.4K; 3 24.6K |
| NPGARPT | category | 10 | 0 | 0 1.83M; 1 65.2K; 2 15.5K; 3 2.9K |
| NPCTMRPT | category | 8 | 0 | 0 1.86M; 1 43.6K; 2 9.0K; 3 2.0K |
| FUNDPYMT | category | 2 | 1.38M | 0 508.8K; 1 23.9K |
| _INGESTED_AT | audit | 1 | 0 | 1785966019261642 1.91M |
| _SOURCE_RUN_ID | audit | 1 | 0 | e0038c71-80b1-4a2b-a8a6-a 1.91M |
| _SRC_SHA256 | other | 1 | 0 | 1409fc66686b637033cf1d61d 1.91M |
