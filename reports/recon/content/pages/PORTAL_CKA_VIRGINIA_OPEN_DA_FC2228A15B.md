# PORTAL_CKA_VIRGINIA_OPEN_DA_FC2228A15B

rows 4.9K  columns 16  scan 5.0s

roles: amount 4, audit 2, category 6, date 2, id 2, who 1

## when

DATE_AND_PICKUP_TIME
  2021       452  ############
  2022       802  #####################
  2023      1.1K  #############################
  2024      1.1K  ##############################
  2025      1.1K  #############################
  2026       320  #########

INGESTED_AT
  2026      4.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE_D | 4.9K | 36.56 | 38.01 | 39.16 | 90 | 185.8K |
| LONGITUDE_D | 4.9K | -122.99 | -78.70 | -77.41 | -23.50 | -383.9K |
| X | 4.9K | -122.99 | -78.70 | -77.40 | 0 | -384.6K |
| Y | 4.9K | 0 | 38.01 | 39.16 | 90 | 186.1K |

## who

SRC_SHA256 by rows
      4.9K  3ee53c821cfcb1079a568845a8af642ad977e99988f7833e8b39100ea395ce2d

SRC_SHA256 by dollars
     -384.6K     4.9K rows  3ee53c821cfcb1079a568845a8af642ad977e99988f7833e8b39100ea395

## who x when

SRC_SHA256 by DATE_AND_PICKUP_TIME, dollars = X
  3ee53c821cfcb1079a568845a8af642ad977e999  2021:-35.7K 2022:-63.2K 2023:-86.3K 2024:-88.6K 2025:-85.6K 2026:-25.0K

## what

DEER_AND_BEAR_REMOVAL: Deer 89%, Bear 6%, Other 5%, Notfound 0%

OTHER_WILDLIFE_TYPES: Coyote 31%, Raccoon 18%, Dog 10%, Fox 8%, Bobcat 7%, Otheranimal 6%, Opossum 6%, Bird 4%, Cat 4%, Groundhog 4%, Skunk 2%

ROUTE_NAME_AND_DIRECTION: I-64E 31%, I-64W 30%, I-81S 11%, I-81N 11%, I-66E 8%, I-66W 7%, I-81 N 0%, I-81 S 0%, I-64 E 0%, I-66 E 0%, I-66 east 0%

COUNTY: Rockbridge County 22%, Albemarle County 20%, Alleghany County 18%, Albemarle 8%, Fauquier County 8%, Augusta County 8%, Fauguier 5%, Rockbridge 4%, Augusta 3%, Louisa 3%, Allenghany 1%

DISTRICT: Staunton 56%, Culpeper 44%, Richmond 0%, Hampton Roads 0%

RESIDENCY: Lexington 47%, Charlottesville 28%, Warrenton 13%, Harrisonburg 8%, Louisa 3%, Edinburg 1%, Ashland 0%, Chesterfield 0%, Appomattox 0%, Franklin 0%, Petersburg 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 4.9K | 0 | 5576 25; 5575 25; 5574 25; 5573 25 |
| GLOBALID | id | 4.8K | 0 | 469fc54d-a06e-430d-833b-4 25; eb3acc68-c88e-4dd3-8072-0 25; 0742c68b-451e-4db1-8f4a-2 25; 52220bdc-58df-44ff-8ee0-7 25 |
| DATE_AND_PICKUP_TIME | date | 4.9K | 2 | 6/16/2026 2:39:43 PM 25; 6/15/2026 2:41:26 PM 25; 6/15/2026 2:21:53 PM 25; 6/15/2026 2:16:03 PM 25 |
| DEER_AND_BEAR_REMOVAL | category | 5 | 111 | Deer 4.3K; Bear 266; Other 222; Notfound 16 |
| OTHER_WILDLIFE_TYPES | category | 16 | 4.6K | Coyote 96; Raccoon 56; Dog 30; Fox 26 |
| ROUTE_NAME_AND_DIRECTION | category | 45 | 3.1K | I-64E 549; I-64W 537; I-81S 201; I-81N 198 |
| LATITUDE_D | amount | 4.9K | 12 | 38.8586228829323 25; 38.9098011664641 25; 38.826047003711 25; 38.8471937151075 25 |
| LONGITUDE_D | amount | 4.8K | 12 | -77.8318711986344 25; -77.9785372333287 25; -77.721883010009 25; -77.7716261317356 25 |
| COUNTY | category | 34 | 1.4K | Rockbridge County 742; Albemarle County 687; Alleghany County 599; Albemarle 284 |
| DISTRICT | category | 5 | 1.4K | Staunton 1.9K; Culpeper 1.5K; Richmond 17; Hampton Roads 1 |
| RESIDENCY | category | 12 | 1.4K | Lexington 1.6K; Charlottesville 984; Warrenton 447; Harrisonburg 275 |
| X | amount | 4.8K | 0 | -77.8318711986344 25; -77.9785372333287 25; -77.721883010009 25; -77.7716261317356 25 |
| Y | amount | 4.9K | 0 | 38.8586228829323 25; 38.9098011664641 25; 38.826047003711 25; 38.8471937151075 25 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:08:14.02796 4.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | b39501fa-55f8-48d3-b81d-b 4.9K |
| SRC_SHA256 | who | 1 | 0 | 3ee53c821cfcb1079a568845a 4.9K |
