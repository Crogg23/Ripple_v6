# PORTAL_CKA_OPEN_DATA_SA_DD50C64C64

rows 10  columns 10  scan 2.8s

roles: amount 2, audit 2, category 5, date 1, who 1

## when

INGESTED_AT
  2026        10  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 10 | 84.93M | 177.08M | 297.34M | 303.25M | 1.76B |
| SHAPE__LENGTH | 10 | 62.5K | 133.7K | 243.6K | 248.0K | 1.40M |

## who

SRC_SHA256 by rows
        10  1ccd7ceb510f85bcb19e53bfc10815f247b56a2f5be40050a5af34763a011093

SRC_SHA256 by dollars
       1.76B       10 rows  1ccd7ceb510f85bcb19e53bfc10815f247b56a2f5be40050a5af34763a01

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  1ccd7ceb510f85bcb19e53bfc10815f247b56a2f  2026:1.76B

## what

OBJECTID: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

DISTRICT: 5 10%, 3 10%, 8 10%, 1 10%, 10 10%, 4 10%, 2 10%, 9 10%, 6 10%, 7 10%

NAME: Teri Castillo 10%, Phyllis Viagran 10%, Ivalis Meza Gonzalez 10%, Sukh Kaur 10%, Marc Whyte 10%, Edward Mungia 10%, Jalen McKee Rodriguez 10%, Misty Spears 10%, Ric Galvan 10%, Marina Alderete Gavito 10%

SQMILES: 50 20%, 25 10%, 89 10%, 53 10%, 29 10%, 69 10%, 60 10%, 57 10%, 31 10%

GLOBALID: 300f7647-b745-450d-82bd-d94f29 10%, a468d3d0-8658-49f7-b7c4-b66ef5 10%, 956b6bcb-6771-413e-ae87-a4403a 10%, 871a6e0a-5b67-423d-bd64-88c639 10%, a44563bf-c50e-49d3-97d9-7d21ed 10%, b5834882-2127-43d8-b2c1-3e1ad6 10%, 5e8cff96-589f-49a1-9afb-0cf5f7 10%, c0255396-0bed-4ec9-a52e-0ce8ae 10%, 032089b4-acf2-4763-8d05-90dbe3 10%, 534ed3b4-4815-494e-adef-ef5d1c 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| DISTRICT | category | 10 | 0 | 5 1; 3 1; 8 1; 1 1 |
| NAME | category | 10 | 0 | Teri Castillo 1; Phyllis Viagran 1; Ivalis Meza Gonzalez 1; Sukh Kaur 1 |
| SQMILES | category | 9 | 0 | 50 2; 25 1; 89 1; 53 1 |
| GLOBALID | category | 10 | 0 | 300f7647-b745-450d-82bd-d 1; a468d3d0-8658-49f7-b7c4-b 1; 956b6bcb-6771-413e-ae87-a 1; 871a6e0a-5b67-423d-bd64-8 1 |
| SHAPE__AREA | amount | 10 | 0 | 84929268.9492188 1; 303253620.582031 1; 181018828.257813 1; 100514490.371094 1 |
| SHAPE__LENGTH | amount | 10 | 0 | 62461.8046878533 1; 248039.807989353 1; 137736.163637961 1; 85144.1290685976 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:55.07496 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | babbc57a-c152-4178-86a8-f 10 |
| SRC_SHA256 | who | 1 | 0 | 1ccd7ceb510f85bcb19e53bfc 10 |
