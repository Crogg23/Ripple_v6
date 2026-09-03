# PORTAL_CKA_OPEN_DATA_SA_19461CBD4A

rows 19  columns 9  scan 3.2s

roles: amount 2, audit 2, category 3, date 2, who 1

## when

DATEDESIGNATED
  2006         4  ##############################
  2010         4  ##############################
  2015         1  ########

INGESTED_AT
  2026        19  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 19 | 10.35M | 106.03M | 678.53M | 731.72M | 3.16B |
| SHAPE__LENGTH | 19 | 18.8K | 55.3K | 149.8K | 153.9K | 1.24M |

## who

SRC_SHA256 by rows
        19  a7957a6843b5adc017cb971408a70d966a1ae2cda8a86888b1a5826c0d632bf1

SRC_SHA256 by dollars
       3.16B       19 rows  a7957a6843b5adc017cb971408a70d966a1ae2cda8a86888b1a5826c0d63

## who x when

SRC_SHA256 by DATEDESIGNATED, dollars = SHAPE__AREA
  a7957a6843b5adc017cb971408a70d966a1ae2cd  2006:226.77M 2010:1.54B 2015:119.75M

## what

OBJECTID: 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%

LOCATION: Upper Leon Creek 8%, Westwood Village Creek 8%, Mitchell Lake 8%, Maverick/Huesta Creek 8%, Upper Huebner Creek 8%, Leon Valley 8%, Stahl Road 8%, French Creek Tributary 8%, Mountain View Estates  8%, Lorence Creek 8%, Walzem Creek 8%, Marbach 410 Area 8%

ID: 19 8%, 2 8%, 20 8%, 3 8%, 1 8%, 0 8%, 17 8%, 5 8%, 13 8%, 7 8%, 16 8%, 4 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 19 | 0 | 19 1; 18 1; 17 1; 16 1 |
| LOCATION | category | 19 | 0 | Upper Leon Creek 1; Westwood Village Creek 1; Mitchell Lake 1; Maverick/Huesta Creek 1 |
| DATEDESIGNATED | date | 6 | 10 | 6/1/2010 4; 3/23/2006 2; 10/08/2015 1; 3/9/2006 1 |
| ID | category | 19 | 0 | 19 1; 2 1; 20 1; 3 1 |
| SHAPE__AREA | amount | 19 | 0 | 731715207.546875 1; 51246402.4453125 1; 263996226.03125 1; 329053587.414063 1 |
| SHAPE__LENGTH | amount | 19 | 0 | 153851.909103907 1; 63600.031921822 1; 93522.2498762633 1; 116734.929396841 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:02.84359 19 |
| SOURCE_RUN_ID | audit | 1 | 0 | 95406750-d673-4b5f-b56e-3 19 |
| SRC_SHA256 | who | 1 | 0 | a7957a6843b5adc017cb97140 19 |
