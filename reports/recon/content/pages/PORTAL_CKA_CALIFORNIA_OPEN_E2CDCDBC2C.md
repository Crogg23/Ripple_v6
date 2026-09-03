# PORTAL_CKA_CALIFORNIA_OPEN_E2CDCDBC2C

rows 134  columns 11  scan 2.5s

roles: amount 2, audit 2, category 2, date 1, other 4, who 1

## when

INGESTED_AT
  2026       134  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 134 | -13.83M | -13.58M | -13.04M | -13.04M | -1.80B |
| Y | 134 | 3.84M | 4.43M | 5.08M | 5.12M | 579.51M |

## who

SRC_SHA256 by rows
       134  33a6e3a81e0cca5cea9496a34f3afbf10788952efa7a87f6344fbd1172f50acd

SRC_SHA256 by dollars
      -1.80B      134 rows  33a6e3a81e0cca5cea9496a34f3afbf10788952efa7a87f6344fbd1172f5

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  33a6e3a81e0cca5cea9496a34f3afbf10788952e  2026:-1.80B

## what

COUNTY: Los Angeles 18%, Alameda 11%, San Francisco 11%, San Diego 11%, San Luis Obispo 10%, Orange 9%, San Mateo 7%, Contra Costa 6%, Marin 5%, Solano 4%, Santa Cruz 4%, Sonoma 4%

NOTES: On the adjacent rock wall touc 74%, On the adjacent rock wall touc 11%, On the adjacent walking bridge 5%, Municipal Pier at Aquatic Park 5%, On the adjacent breakwater a f 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 136 | 0 | -13782471.6 1; -13771391.3 1; -13648343.8 1; -13619306.2 1 |
| Y | amount | 135 | 0 | 4783182.8 1; 4709439.2 1; 4611005.1 1; 4598777.8 1 |
| OBJECTID | other | 133 | 0 | 134 1; 133 1; 132 1; 131 1 |
| PIER | other | 135 | 0 | Noyo River Jetty 1; Point Arena Pier 1; Shollenberger Pier 1; Cullinan Ranch Fishing Pi 1 |
| COUNTY | category | 20 | 0 | Los Angeles 21; Alameda 13; San Francisco 12; San Diego 12 |
| LAT_DDM | other | 134 | 0 | 39° 25.68682321' N 1; 38° 54.87280741' N 1; 38° 13.39190362' N 1; 38° 08.21139470' N 1 |
| LONG_DDM | other | 132 | 0 | 123° 48.60214097' W 1; 123° 42.62997364' W 1; 122° 36.30871352' W 1; 122° 20.65777861' W 1 |
| NOTES | category | 6 | 115 | On the adjacent rock wall 14; On the adjacent rock wall 2; On the adjacent walking b 1; Municipal Pier at Aquatic 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:34:26.11739 134 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8fc62379-9745-46d5-84a6-3 134 |
| SRC_SHA256 | who | 1 | 0 | 33a6e3a81e0cca5cea9496a34 134 |
