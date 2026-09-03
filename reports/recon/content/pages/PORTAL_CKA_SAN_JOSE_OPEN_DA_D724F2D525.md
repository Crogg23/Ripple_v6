# PORTAL_CKA_SAN_JOSE_OPEN_DA_D724F2D525

rows 2  columns 20  scan 3.6s

roles: amount 3, audit 2, category 9, date 1, empty 2, other 2, who 2

## when

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 2 | 6.15M | 6.17M | 6.19M | 6.19M | 12.34M |
| Y | 2 | 1.91M | 1.93M | 1.95M | 1.95M | 3.87M |
| TOTALACREAGE | 1 | 10.49 | 10.49 | 10.49 | 10.49 | 10.49 |

## who

CLASS by rows
         2  POLICE

CLASS by dollars
       10.49        2 rows  POLICE

SRC_SHA256 by rows
         2  3348470e524ecfa067ba1ed88df444d1961d9c92644837487545877b68fcf70e

SRC_SHA256 by dollars
       10.49        2 rows  3348470e524ecfa067ba1ed88df444d1961d9c92644837487545877b68fc

## who x when

CLASS by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTALACREAGE
  POLICE                                    2026:10.49

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTALACREAGE
  3348470e524ecfa067ba1ed88df444d1961d9c92  2026:10.49

## what

OBJECTID: 168 50%, 159 50%

FACILITYID: 168 50%, 159 50%

INFORID: LOC-0661 50%, LOC-0159 50%

DESCRIPTION: SOUTH POLICE SUBSTATION - 6087 50%, POLICE ADMIN & ANNEX  (PAB) -  50%

NAME: SOUTH POLICE SUBSTATION  50%, POLICE ADMIN & ANNEX  (PAB) -  50%

ADDRESSLOCATION:  6087 GREAT OAKS PARKWAY 50%,  201 WEST MISSION STREET 50%

DISTRICT: 2 50%, 3 50%

LASTUPDATE: 2021/05/12 23:09:10+00 50%, 2023/02/15 23:51:49+00 50%

GLOBALID: {6B3A50A4-623C-4E06-B6FA-411ED 50%, {B78806E0-527E-4D12-BF56-B2947 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 2 | 0 | 6186567.52295889 1; 6153091.40027872 1 |
| Y | amount | 2 | 0 | 1914438.96933973 1; 1952795.36933281 1 |
| OBJECTID | category | 2 | 0 | 168 1; 159 1 |
| FACILITYID | category | 2 | 0 | 168 1; 159 1 |
| INFORID | category | 2 | 0 | LOC-0661 1; LOC-0159 1 |
| DESCRIPTION | category | 2 | 0 | SOUTH POLICE SUBSTATION - 1; POLICE ADMIN & ANNEX  (PA 1 |
| NAME | category | 2 | 0 | SOUTH POLICE SUBSTATION  1; POLICE ADMIN & ANNEX  (PA 1 |
| ADDRESSLOCATION | category | 2 | 0 |  6087 GREAT OAKS PARKWAY 1;  201 WEST MISSION STREET 1 |
| CITYOWNED | other | 1 | 0 | YES 2 |
| DISTRICT | category | 2 | 0 | 2 1; 3 1 |
| TOTALACREAGE | amount | 2 | 1 | 10.49 1 |
| CLASS | who | 1 | 0 | POLICE 2 |
| CATEGORY | other | 1 | 0 | PD 2 |
| SOURCEENTID | empty | 1 | 2 |  |
| LASTUPDATE | category | 2 | 0 | 2021/05/12 23:09:10+00 1; 2023/02/15 23:51:49+00 1 |
| NOTES | empty | 1 | 2 |  |
| GLOBALID | category | 2 | 0 | {6B3A50A4-623C-4E06-B6FA- 1; {B78806E0-527E-4D12-BF56- 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:05:59.10037 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | d16a55d3-24e5-409a-96b7-0 2 |
| SRC_SHA256 | who | 1 | 0 | 3348470e524ecfa067ba1ed88 2 |
