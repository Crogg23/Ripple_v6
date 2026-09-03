# FED_COURTLISTENER_COURTHOUSES

rows 3.4K  columns 14  scan 2.4s

roles: audit 2, category 5, date 1, empty 1, id 2, other 1, state 1, who 2

## when

_INGESTED_AT
  2026      3.4K  ##############################

## who

BUILDING_NAME by rows
         3  United States Patent and Trademark Office

_SRC_SHA256 by rows
      3.4K  ba6b39442687d6be453b01e50f1a3e1e2fe28f270eb44305f94364dc8b8ed102

## who x when

BUILDING_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  United States Patent and Trademark Offic  2026:3

_SRC_SHA256 by _INGESTED_AT  LOAD STAMP, not an event date
  ba6b39442687d6be453b01e50f1a3e1e2fe28f27  2026:3.4K

## where

STATE: TX 719, NY 509, OH 492, PA 278, FL 219, CA 179, VA 136, NJ 94, MI 75, KY 59, GA 55, DC 41

## what

COURT_SEAT: f 100%, t 0%

ADDRESS1: 600 Dulany Street 75%, 811 East Main Street 25%

CITY: Alexandria 33%, Lakeland 11%, Austin 11%, Edinburg 11%, Corpus Christi 11%, Lansing 11%, Baltimore 11%

ZIP_CODE: 22314 75%, 33801 25%

COUNTRY_CODE: US 100%, GB 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 3.3K | 0 | 3361 17; 3360 17; 3359 17; 3358 17 |
| COURT_SEAT | category | 2 | 3 | f 3.4K; t 6 |
| BUILDING_NAME | who | 1 | 3.4K | United States Patent and  3 |
| ADDRESS1 | category | 2 | 3.4K | 600 Dulany Street 3; 811 East Main Street 1 |
| ADDRESS2 | empty | 0 | 3.4K |  |
| CITY | category | 7 | 3.4K | Alexandria 3; Lakeland 1; Austin 1; Edinburg 1 |
| COUNTY | other | 1 | 3.4K | Polk 1 |
| STATE | state | 63 | 1 | TX 719; NY 509; OH 492; PA 278 |
| ZIP_CODE | category | 2 | 3.4K | 22314 3; 33801 1 |
| COUNTRY_CODE | category | 2 | 0 | US 3.4K; GB 1 |
| COURT_ID | id | 3.3K | 0 | txctapp13 18; fladistctapp6 17; bpai 17; ptab 17 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:03:51.782 3.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | c188d016-32d3-43e5-9c72-1 3.4K |
| _SRC_SHA256 | who | 1 | 0 | ba6b39442687d6be453b01e50 3.4K |
