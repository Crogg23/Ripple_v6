# PORTAL_CKA_HOUSTON_OPEN_DAT_18A3CA22AF

rows 28  columns 7  scan 3.9s

roles: audit 2, category 2, date 3, who 1

## when

PER_EFFECTIVE_START_DATE
  2014        14  ##############################
  2015        14  ##############################

PER_EFFECTIVE_END_DATE
  2015        14  ##############################
  2016        14  ##############################

INGESTED_AT
  2026        28  ##############################

## who

SRC_SHA256 by rows
        28  2cc7676bf51090b6c46eb8c743490f1acb5b16d18ddc58562062e91a52edf7bb

## who x when

SRC_SHA256 by PER_EFFECTIVE_START_DATE
  2cc7676bf51090b6c46eb8c743490f1acb5b16d1  2014:14 2015:14

## what

ENT_GROUP_NAME: CEADERS CORPORATION 8%, S P CHOICE VALET PARKING 8%, CASH PARKING 8%, P & K LLC 8%, TOWNE PARK VALET 8%, LAZ Parking Texas, LLC 8%, LANIER SHUTTLE and VALET, INC. 8%, CG PARKING SOLUTIONS 8%, CMV VALET 8%, Concord Excellent Valet Servic 8%, PANAM PARKING MANAGEMENT 8%, ASANTI VALET COMPANY 8%

PER_NUMBER: V003365 8%, V003364 8%, V003363 8%, V003362 8%, V003361 8%, V003360 8%, V003359 8%, V003358 8%, V003357 8%, V003356 8%, V003355 8%, V003353 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENT_GROUP_NAME | category | 28 | 0 | CEADERS CORPORATION 1; S P CHOICE VALET PARKING 1; CASH PARKING 1; P & K LLC 1 |
| PER_NUMBER | category | 28 | 0 | V003365 1; V003364 1; V003363 1; V003362 1 |
| PER_EFFECTIVE_START_DATE | date | 24 | 0 | 2015-02-10 00:00:00 2; 2015-01-16 00:00:00 2; 2014-05-29 00:00:00 2; 2014-05-19 00:00:00 2 |
| PER_EFFECTIVE_END_DATE | date | 24 | 0 | 2016-02-10 23:59:59 2; 2016-01-16 23:59:59 2; 2015-05-29 23:59:59 2; 2015-05-19 23:59:59 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:10:28.21811 28 |
| SOURCE_RUN_ID | audit | 1 | 0 | fa1b05aa-ea67-4cf7-bc13-3 28 |
| SRC_SHA256 | who | 1 | 0 | 2cc7676bf51090b6c46eb8c74 28 |
