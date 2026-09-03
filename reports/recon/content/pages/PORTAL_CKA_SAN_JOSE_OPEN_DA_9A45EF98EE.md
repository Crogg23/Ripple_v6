# PORTAL_CKA_SAN_JOSE_OPEN_DA_9A45EF98EE

rows 7  columns 18  scan 4.9s

roles: amount 3, audit 2, category 8, date 1, empty 3, who 2

## when

INGESTED_AT
  2026         7  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 7 | 6.14M | 6.16M | 6.18M | 6.18M | 43.10M |
| Y | 7 | 1.91M | 1.94M | 1.96M | 1.96M | 13.57M |
| HOSPITALAREA | 7 | 3.80 | 19.80 | 55.70 | 55.80 | 206.80 |

## who

LASTUPDATE by rows
         7  2024/06/14 17:05:25+00

LASTUPDATE by dollars
      43.10M        7 rows  2024/06/14 17:05:25+00

SRC_SHA256 by rows
         7  0e225208d9db02ca9f2c88284a6d647eb9bc4cf94800431be0315ad5496f6a89

SRC_SHA256 by dollars
      43.10M        7 rows  0e225208d9db02ca9f2c88284a6d647eb9bc4cf94800431be0315ad5496f

## who x when

LASTUPDATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  2024/06/14 17:05:25+00                    2026:43.10M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  0e225208d9db02ca9f2c88284a6d647eb9bc4cf9  2026:43.10M

## what

OBJECTID: 7 14%, 6 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

FACILITYID: 8 14%, 7 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

INTID: 8 14%, 7 14%, 5 14%, 4 14%, 3 14%, 2 14%, 1 14%

NAME: Valley Health Center Downtown 14%, Kaiser San Jose Medical Center 14%, Santa Clara Valley Medical Cen 14%, San Jose Medical Center 14%, Regional Medical Center 14%, O'Connor Hospital 14%, Good Samaritan Hospital 14%

STATUS: Open 86%, Closed 14%

FULLADDR: 777 E Santa Clara St 14%, 250 Hospital Pkwy 14%, 751 S Bascom Ave 14%, 280 Hospital Pkwy 14%, 225 N Jackson Ave 14%, 2105 Forest Ave 14%, 2425 Samaritan Dr 14%

ZIPCODE: 95119 29%, 95128 29%, 95113 14%, 95116 14%, 95124 14%

NOTES: 0 Beds 14%, 257 Beds 14%, 731 Beds 14%, 235 Beds 14%, 252 Beds 14%, 348 Beds 14%, 474 Beds 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 7 | 0 | 6161948.03479649 1; 6182984.22500749 1; 6144593.66629007 1; 6161533.39553392 1 |
| Y | amount | 7 | 0 | 1950642.40972807 1; 1912322.55559364 1; 1939743.71302156 1; 1950713.23898272 1 |
| OBJECTID | category | 7 | 0 | 7 1; 6 1; 5 1; 4 1 |
| FACILITYID | category | 7 | 0 | 8 1; 7 1; 5 1; 4 1 |
| INTID | category | 7 | 0 | 8 1; 7 1; 5 1; 4 1 |
| NAME | category | 7 | 0 | Valley Health Center Down 1; Kaiser San Jose Medical C 1; Santa Clara Valley Medica 1; San Jose Medical Center 1 |
| STATUS | category | 2 | 0 | Open 6; Closed 1 |
| HOSPITALAREA | amount | 7 | 0 | 3.8 1; 54.2 1; 55.8 1; 11.7 1 |
| FULLADDR | category | 7 | 0 | 777 E Santa Clara St 1; 250 Hospital Pkwy 1; 751 S Bascom Ave 1; 280 Hospital Pkwy 1 |
| ZIPCODE | category | 5 | 0 | 95119 2; 95128 2; 95113 1; 95116 1 |
| AGENCYURL | empty | 1 | 7 |  |
| PHONE | empty | 1 | 7 |  |
| EMAIL | empty | 1 | 7 |  |
| LASTUPDATE | who | 1 | 0 | 2024/06/14 17:05:25+00 7 |
| NOTES | category | 7 | 0 | 0 Beds 1; 257 Beds 1; 731 Beds 1; 235 Beds 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:21.19052 7 |
| SOURCE_RUN_ID | audit | 1 | 0 | f77561b4-b55c-4e87-8852-c 7 |
| SRC_SHA256 | who | 1 | 0 | 0e225208d9db02ca9f2c88284 7 |
