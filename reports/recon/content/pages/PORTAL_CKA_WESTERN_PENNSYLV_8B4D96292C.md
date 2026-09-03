# PORTAL_CKA_WESTERN_PENNSYLV_8B4D96292C

rows 25  columns 14  scan 4.2s

roles: amount 3, audit 2, category 5, date 1, empty 1, who 3

## when

INGESTED_AT
  2026        25  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_AREA | 25 | 204.6K | 4.76M | 25.23M | 26.94M | 151.18M |
| RATES | 23 | 1 | 1.50 | 3.78 | 4 | 40.50 |
| SHAPE_LENGTH | 25 | 2.0K | 9.2K | 20.7K | 20.9K | 254.8K |

## who

HOURS by rows
        25  8AM - 6PM

HOURS by dollars
     151.18M       25 rows  8AM - 6PM

DAYS by rows
        25  Mon - Sat

DAYS by dollars
     151.18M       25 rows  Mon - Sat

SRC_SHA256 by rows
        25  54516a009bdd16610ba4cc6fb7a7e64df9e9ea1ca4c9deb7eec0135b03831f0a

SRC_SHA256 by dollars
     151.18M       25 rows  54516a009bdd16610ba4cc6fb7a7e64df9e9ea1ca4c9deb7eec0135b0383

## who x when

HOURS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  8AM - 6PM                                 2026:151.18M

DAYS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_AREA
  Mon - Sat                                 2026:151.18M

## what

AREA: Shadyside 14%, Squirrel Hill 14%, Carrick 7%, Bakery Square 7%, Knoxville 7%, Beechview 7%, West End 7%, Allentown 7%, Mellon Park Area 7%, Strip District 7%, Technology Center 7%, Lawrenceville 7%

ID: 0 100%

PARKINGLEN: 10 Hours 64%, 2 Hours 20%, Unlimited 16%

RATE: $1.50PH/10HRS M-Sat,8AM-10PM 22%, $1.5PH/10HRS M-Sat,8AM-10PM 22%, DYNAMIC RATE PRICING 11%, $2PH/10HRS M-Sat,8AM-10PM 11%, $3PH/2HRS M-SAT,8AM-6PM 6%, $3PH/10HRS M-Sat,8AM-10PM 6%, $1.5PH/10HRS M-SAT,8AM-6PM 6%, $1PH/10HRS M-Sat,8AM-10PM 6%, $4PH/2HRS M-SAT,8AM-6PM 6%, $3.00PH/4HRS M-SAT,8AM-6PM 6%

OBJECTID: 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%, 15 8%, 14 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA | category | 23 | 0 | Shadyside 2; Squirrel Hill 2; Carrick 1; Bakery Square 1 |
| ID | category | 2 | 7 | 0 18 |
| HOURS | who | 1 | 0 | 8AM - 6PM 25 |
| PARKINGLEN | category | 3 | 0 | 10 Hours 16; 2 Hours 5; Unlimited 4 |
| SHAPE_AREA | amount | 24 | 0 | 2495823.33334351 1; 204632.000793457 1; 2007968.78027344 1; 1168832.55651855 1 |
| RATE | category | 11 | 7 | $1.50PH/10HRS M-Sat,8AM-1 4; $1.5PH/10HRS M-Sat,8AM-10 4; DYNAMIC RATE PRICING 2; $2PH/10HRS M-Sat,8AM-10PM 2 |
| MAXHOURS | empty | 2 | 25 |  |
| DAYS | who | 1 | 0 | Mon - Sat 25 |
| OBJECTID | category | 25 | 0 | 25 1; 24 1; 23 1; 22 1 |
| RATES | amount | 6 | 0 | $1.50 11; $1.00 5; $2.00 3; $3.00 3 |
| SHAPE_LENGTH | amount | 25 | 0 | 6639.71588260412 1; 2219.18030682016 1; 5961.72941842612 1; 4731.97490494809 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:18:29.56376 25 |
| SOURCE_RUN_ID | audit | 1 | 0 | 315fc8d5-7114-4859-9bd9-2 25 |
| SRC_SHA256 | who | 1 | 0 | 54516a009bdd16610ba4cc6fb 25 |
