# PORTAL_CKA_WESTERN_PENNSYLV_69C80C6F70

rows 1.4K  columns 11  scan 3.1s

roles: amount 2, audit 2, date 1, id 6, who 1

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREA | 1.4K | 16.38M | 16.42M | 16.49M | 16.49M | 22.35B |
| PERIMETER | 1.4K | 16.3K | 16.4K | 16.4K | 16.4K | 22.26M |

## who

SRC_SHA256 by rows
      1.4K  10c8ccbd8bfb5186da1fb39c62b58efe7a4946bc8c13ca18c85281137af62182

SRC_SHA256 by dollars
      22.35B     1.4K rows  10c8ccbd8bfb5186da1fb39c62b58efe7a4946bc8c13ca18c85281137af6

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREA
  10c8ccbd8bfb5186da1fb39c62b58efe7a4946bc  2026:22.35B

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AREA | amount | 1.4K | 0 | 16454924.887221 7; 16454937.341175 7; 16454903.460131 7; 16454912.737562 7 |
| FID | id | 1.3K | 0 | 1361 7; 1360 7; 1359 7; 1358 7 |
| INDEX | id | 1.3K | 0 | 1122 7; 1121 7; 1120 7; 1119 7 |
| INDEX_ID | id | 1.3K | 0 | 1204 7; 1250 7; 1296 7; 1341 7 |
| PERIMETER | amount | 1.4K | 0 | 16375.49339782 7; 16375.500545471 7; 16375.482392856 7; 16375.489787557 7 |
| TILE | id | 1.3K | 1 | 0396 7; 0397 7; 0398 7; 0399 7 |
| TILENUM | id | 1.3K | 0 | 396 7; 397 7; 398 7; 399 7 |
| GEOMETRY | id | 1.3K | 0 | POLYGON ((577869.34062658 7; POLYGON ((576453.81295268 7; POLYGON ((575038.28472259 7; POLYGON ((573622.76016296 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:53:33.60377 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 15890de2-54f0-4f97-9072-6 1.4K |
| SRC_SHA256 | who | 1 | 0 | 10c8ccbd8bfb5186da1fb39c6 1.4K |
