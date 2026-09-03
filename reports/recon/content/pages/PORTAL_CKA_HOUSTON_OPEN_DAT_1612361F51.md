# PORTAL_CKA_HOUSTON_OPEN_DAT_1612361F51

rows 37  columns 6  scan 2.4s

roles: audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        37  ##############################

## who

SRC_SHA256 by rows
        37  43c4b7cc3c418fa120a10c0eb6e2cdad8fffa7dc1be60b499f0d96ff9f0c198a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  43c4b7cc3c418fa120a10c0eb6e2cdad8fffa7dc  2026:37

## what

ESTABLISHMENT_NAME: Starbucks  14%, Barnaby's Café 14%, Mia’s Table  7%, Baba Yega  7%, Jimmy’s Ice House  7%, Taco Milagro Kirby  7%, Cottonwood  7%, Winston’s on Washington  7%, Mission Burritos 802  7%, Mission Burritos 801  7%, The King’s Head  7%, J. Black’s Houston‐Washington  7%

ADDRESS: 3131 Argonne  8%, 2607 Grant  8%, 2803 White Oak 8%, 2555 Kirby  8%, 3422 N. Shepherd  8%, 5111 Washington 8%, 1609 Durham  8%, 2245 W. Alabama  8%, 1809 Eldridge Parkway  8%, 110 S. Heights Blvd.  8%, 2820 White Oak  8%, 2000 Bagby Suite 106  8%

ZIP: 77006 30%, 77019 18%, 77007 15%, 77098 9%, 77002 6%, 77010 6%, 77018 3%, 77077 3%, 77040 3%, 77005 3%, 77008 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ESTABLISHMENT_NAME | category | 35 | 0 | Starbucks  2; Barnaby's Café 2; Mia’s Table  1; Baba Yega  1 |
| ADDRESS | category | 37 | 0 | 3131 Argonne  1; 2607 Grant  1; 2803 White Oak 1; 2555 Kirby  1 |
| ZIP | category | 13 | 3 | 77006 10; 77019 6; 77007 5; 77098 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:20:22.29610 37 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3249fc58-750b-41ea-8f89-2 37 |
| SRC_SHA256 | who | 1 | 0 | 43c4b7cc3c418fa120a10c0eb 37 |
