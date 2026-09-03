# PORTAL_CKA_OPEN_DATA_SA_F128E26A15

rows 32  columns 9  scan 3.5s

roles: amount 2, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026        32  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 32 | 2.07M | 2.12M | 2.17M | 2.17M | 67.87M |
| Y | 32 | 13.67M | 13.71M | 13.78M | 13.78M | 438.87M |

## who

SRC_SHA256 by rows
        32  1678f75dd5b88257c3dbaee37699542e31da4b9c9d0ba2abb0276469883b2245

SRC_SHA256 by dollars
      67.87M       32 rows  1678f75dd5b88257c3dbaee37699542e31da4b9c9d0ba2abb0276469883b

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  1678f75dd5b88257c3dbaee37699542e31da4b9c  2026:67.87M

## what

OBJECTID: 32 8%, 31 8%, 30 8%, 29 8%, 28 8%, 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%

SCHOOLNAME: El Dorado Elementary 8%, Villareal Elementary 8%, Neal Elementary 8%, Palo Alto College 8%, Adams Hill 8%, Camelot Elementary 8%, Burke Elementary  8%, Colonial Hills 8%, Huppertz Elementary 8%, Woodstone Elementary 8%, Adams Elementary 8%, Wheatley Middel School 8%

ADDRESS: 12634 El Sendero St 8%, 2902 White Tail 8%, 3407 Capitol Ave 8%, 1400 West Villaret Blvd 8%, 9627 Adams Hill Dr 8%, 7410 Ray Bon 8%, 10111 Terra Oaks 8%, 2627 Kerrybrook Court 8%, 247 Bangor 8%, 5602 Fountainwood 8%, 135 E Southcross Blvd 8%, 415 Gabriel St 8%

ZIPCODE: 78207 18%, 78233 12%, 78201 12%, 78230 12%, 78242 12%, 78228 6%, 78224 6%, 78218 6%, 78250 6%, 78214 6%, 78202 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 32 | 0 | 32 1; 31 1; 30 1; 29 1 |
| SCHOOLNAME | category | 32 | 0 | El Dorado Elementary 1; Villareal Elementary 1; Neal Elementary 1; Palo Alto College 1 |
| ADDRESS | category | 32 | 0 | 12634 El Sendero St 1; 2902 White Tail 1; 3407 Capitol Ave 1; 1400 West Villaret Blvd 1 |
| ZIPCODE | category | 23 | 4 | 78207 3; 78233 2; 78201 2; 78230 2 |
| X | amount | 32 | 0 | 2161120.39546305 1; 2099344.48194164 1; 2122923.90623939 1; 2114110.38515255 1 |
| Y | amount | 32 | 0 | 13748416.1936265 1; 13717083.8953988 1; 13723615.5519549 1; 13665643.3168497 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:19:30.20720 32 |
| SOURCE_RUN_ID | audit | 1 | 0 | 188718b0-0cbf-4e65-a72a-a 32 |
| SRC_SHA256 | who | 1 | 0 | 1678f75dd5b88257c3dbaee37 32 |
